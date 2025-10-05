"""
HDL Processor Module

This module handles the processing of HDL (Hardware Description Language) code,
including parsing, validation, compilation, and project generation.
"""

import os
import re
import subprocess
import tempfile
import zipfile
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class HDLCode:
    """Container for HDL code and metadata"""
    content: str
    language: str  # 'vhdl' or 'verilog'
    entity_name: str
    file_extension: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CompilationResult:
    """Result of HDL compilation"""
    success: bool
    entity_name: str
    language: str
    build_files: List[str]
    error_message: Optional[str] = None
    warnings: List[str] = None
    compilation_time: float = 0.0


@dataclass
class ProjectExport:
    """Result of project export"""
    success: bool
    file_path: str
    file_size: int
    export_time: float = 0.0
    error_message: Optional[str] = None


class HDLProcessor:
    """
    Processes HDL code from AI generation to final project export.
    
    This class handles:
    - Parsing and validation of generated HDL code
    - Entity/module name extraction and replacement
    - HDL compilation using appropriate tools
    - Project packaging for Proteus
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize HDL processor.
        
        Args:
            config: Configuration dictionary containing compiler paths and settings
        """
        self.config = config
        self.ghdl_path = config.get('ghdl_path', 'ghdl')
        self.iverilog_path = config.get('iverilog_path', 'iverilog')
        self.work_directory = config.get('work_directory', 'build')
        self.timeout = config.get('timeout', 60)
        self.additional_flags = config.get('additional_flags', {
            'vhdl': ['-fsynopsys'],
            'verilog': []
        })
        
        # Ensure work directory exists
        os.makedirs(self.work_directory, exist_ok=True)
    
    def parse_hdl_code(self, ai_response_content: str, circuit_name: str) -> HDLCode:
        """
        Parse HDL code from AI response and extract metadata.
        
        Args:
            ai_response_content: Raw content from AI response
            circuit_name: Desired name for the circuit
            
        Returns:
            HDLCode object with parsed information
            
        Raises:
            ValueError: If code cannot be parsed or is invalid
        """
        logger.info(f"Parsing HDL code for circuit: {circuit_name}")
        
        # Extract language and code using regex
        language, code = self._extract_code_and_language(ai_response_content)
        
        # Clean and validate the code
        code = self._clean_code(code)
        self._validate_basic_syntax(code, language)
        
        # Extract and replace entity/module name
        original_name = self._extract_entity_name(code, language)
        if original_name and original_name != circuit_name:
            code = self._replace_entity_name(code, original_name, circuit_name, language)
        
        # Determine file extension
        file_extension = 'vhdl' if language == 'vhdl' else 'v'
        
        # Create metadata
        metadata = {
            'original_entity_name': original_name,
            'lines_of_code': len(code.split('\n')),
            'has_testbench': self._detect_testbench(code, language),
            'libraries_used': self._extract_libraries(code, language),
            'signals_count': self._count_signals(code, language),
            'processes_count': self._count_processes(code, language)
        }
        
        logger.info(f"Successfully parsed {language.upper()} code with {metadata['lines_of_code']} lines")
        
        return HDLCode(
            content=code,
            language=language,
            entity_name=circuit_name,
            file_extension=file_extension,
            metadata=metadata
        )
    
    def compile_hdl(self, hdl_code: HDLCode, session_id: str) -> CompilationResult:
        """
        Compile HDL code using appropriate compiler.
        
        Args:
            hdl_code: HDL code to compile
            session_id: Unique session identifier for isolation
            
        Returns:
            CompilationResult with compilation status and artifacts
        """
        import time
        start_time = time.time()
        
        logger.info(f"Starting compilation of {hdl_code.language.upper()} code for entity: {hdl_code.entity_name}")
        
        # Create session-specific build directory
        build_dir = os.path.join(self.work_directory, session_id)
        os.makedirs(build_dir, exist_ok=True)
        
        # Write HDL file
        hdl_file = os.path.join(build_dir, f"{hdl_code.entity_name}.{hdl_code.file_extension}")
        with open(hdl_file, 'w', encoding='utf-8') as f:
            f.write(hdl_code.content)
        
        try:
            if hdl_code.language == 'vhdl':
                result = self._compile_vhdl(hdl_code.entity_name, hdl_file, build_dir)
            elif hdl_code.language == 'verilog':
                result = self._compile_verilog(hdl_code.entity_name, hdl_file, build_dir)
            else:
                raise ValueError(f"Unsupported HDL language: {hdl_code.language}")
            
            result.compilation_time = time.time() - start_time
            
            if result.success:
                logger.info(f"Compilation successful in {result.compilation_time:.2f}s")
            else:
                logger.error(f"Compilation failed: {result.error_message}")
            
            return result
            
        except Exception as e:
            logger.error(f"Compilation error: {str(e)}")
            return CompilationResult(
                success=False,
                entity_name=hdl_code.entity_name,
                language=hdl_code.language,
                build_files=[],
                error_message=str(e),
                compilation_time=time.time() - start_time
            )
    
    def export_project(self, hdl_code: HDLCode, compilation_result: CompilationResult, 
                      export_dir: str, session_id: str) -> ProjectExport:
        """
        Export compiled project as Proteus-compatible file.
        
        Args:
            hdl_code: Original HDL code
            compilation_result: Result from compilation
            export_dir: Directory to export project to
            session_id: Session identifier
            
        Returns:
            ProjectExport with export status and file information
        """
        import time
        start_time = time.time()
        
        logger.info(f"Exporting project for entity: {hdl_code.entity_name}")
        
        os.makedirs(export_dir, exist_ok=True)
        
        try:
            # Create project archive
            project_file = os.path.join(export_dir, f"{hdl_code.entity_name}.pdsprj")
            
            with zipfile.ZipFile(project_file, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add HDL source file
                build_dir = os.path.join(self.work_directory, session_id)
                hdl_file = os.path.join(build_dir, f"{hdl_code.entity_name}.{hdl_code.file_extension}")
                
                if os.path.exists(hdl_file):
                    zip_file.write(hdl_file, f"{hdl_code.entity_name}.{hdl_code.file_extension}")
                
                # Add compilation artifacts
                if compilation_result.success:
                    for build_file in compilation_result.build_files:
                        if os.path.exists(build_file):
                            arc_name = os.path.basename(build_file)
                            zip_file.write(build_file, arc_name)
                
                # Add project metadata
                metadata = {
                    'project_name': hdl_code.entity_name,
                    'hdl_language': hdl_code.language,
                    'generated_by': 'HDL AI Proteus',
                    'compilation_success': compilation_result.success,
                    'metadata': hdl_code.metadata
                }
                
                zip_file.writestr('project_info.json', 
                                 self._create_json_string(metadata))
                
                # Add README for project
                readme_content = self._generate_project_readme(hdl_code, compilation_result)
                zip_file.writestr('README.txt', readme_content)
            
            file_size = os.path.getsize(project_file)
            export_time = time.time() - start_time
            
            logger.info(f"Project exported successfully: {project_file} ({file_size} bytes)")
            
            return ProjectExport(
                success=True,
                file_path=project_file,
                file_size=file_size,
                export_time=export_time
            )
            
        except Exception as e:
            logger.error(f"Export error: {str(e)}")
            return ProjectExport(
                success=False,
                file_path="",
                file_size=0,
                export_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def _extract_code_and_language(self, content: str) -> Tuple[str, str]:
        """Extract HDL code and determine language from AI response."""
        # Try to find code blocks with language specification
        pattern = r'```(vhdl|verilog|systemverilog)\s*\n(.*?)\n```'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            language = match.group(1).lower()
            code = match.group(2).strip()
            # Normalize language names
            if language in ['verilog', 'systemverilog']:
                language = 'verilog'
            return language, code
        
        # If no code block found, try to detect language from keywords
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in ['entity', 'architecture', 'library ieee']):
            return 'vhdl', content.strip()
        elif any(keyword in content_lower for keyword in ['module', 'endmodule', 'always', 'wire']):
            return 'verilog', content.strip()
        
        # Default to VHDL if can't determine
        return 'vhdl', content.strip()
    
    def _clean_code(self, code: str) -> str:
        """Clean and normalize HDL code."""
        # Remove excessive whitespace
        lines = [line.rstrip() for line in code.split('\n')]
        # Remove empty lines at start and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        
        return '\n'.join(lines)
    
    def _validate_basic_syntax(self, code: str, language: str) -> None:
        """Perform basic syntax validation."""
        if language == 'vhdl':
            if not re.search(r'\bentity\s+\w+\s+is', code, re.IGNORECASE):
                raise ValueError("VHDL code must contain an entity declaration")
            if not re.search(r'\barchitecture\s+\w+\s+of\s+\w+\s+is', code, re.IGNORECASE):
                raise ValueError("VHDL code must contain an architecture declaration")
        elif language == 'verilog':
            if not re.search(r'\bmodule\s+\w+', code, re.IGNORECASE):
                raise ValueError("Verilog code must contain a module declaration")
            if not re.search(r'\bendmodule\b', code, re.IGNORECASE):
                raise ValueError("Verilog code must contain an endmodule statement")
    
    def _extract_entity_name(self, code: str, language: str) -> Optional[str]:
        """Extract entity/module name from HDL code."""
        if language == 'vhdl':
            match = re.search(r'\bentity\s+(\w+)\s+is', code, re.IGNORECASE)
            return match.group(1) if match else None
        elif language == 'verilog':
            match = re.search(r'\bmodule\s+(\w+)', code, re.IGNORECASE)
            return match.group(1) if match else None
        return None
    
    def _replace_entity_name(self, code: str, old_name: str, new_name: str, language: str) -> str:
        """Replace entity/module name in HDL code."""
        if language == 'vhdl':
            # Replace in entity declaration
            code = re.sub(rf'\bentity\s+{re.escape(old_name)}\s+is',
                         f'entity {new_name} is', code, flags=re.IGNORECASE)
            # Replace in architecture declaration
            code = re.sub(rf'\barchitecture\s+(\w+)\s+of\s+{re.escape(old_name)}\s+is',
                         rf'architecture \1 of {new_name} is', code, flags=re.IGNORECASE)
        elif language == 'verilog':
            # Replace module name
            code = re.sub(rf'\bmodule\s+{re.escape(old_name)}\b',
                         f'module {new_name}', code, flags=re.IGNORECASE)
        
        return code
    
    def _detect_testbench(self, code: str, language: str) -> bool:
        """Detect if code contains testbench elements."""
        code_lower = code.lower()
        if language == 'vhdl':
            return any(keyword in code_lower for keyword in ['testbench', 'tb_', '_tb', 'test_'])
        elif language == 'verilog':
            return any(keyword in code_lower for keyword in ['testbench', 'tb_', '_tb', 'initial', '$monitor'])
        return False
    
    def _extract_libraries(self, code: str, language: str) -> List[str]:
        """Extract used libraries from HDL code."""
        libraries = []
        if language == 'vhdl':
            # Find library declarations
            lib_matches = re.findall(r'\blibrary\s+(\w+)', code, re.IGNORECASE)
            use_matches = re.findall(r'\buse\s+([\w.]+)', code, re.IGNORECASE)
            libraries.extend(lib_matches)
            libraries.extend([use.split('.')[0] for use in use_matches])
        elif language == 'verilog':
            # Find include statements
            inc_matches = re.findall(r'`include\s+"([^"]+)"', code)
            libraries.extend(inc_matches)
        
        return list(set(libraries))  # Remove duplicates
    
    def _count_signals(self, code: str, language: str) -> int:
        """Count signal/wire declarations in HDL code."""
        if language == 'vhdl':
            signals = re.findall(r'\bsignal\s+\w+', code, re.IGNORECASE)
            return len(signals)
        elif language == 'verilog':
            wires = re.findall(r'\bwire\s+', code, re.IGNORECASE)
            regs = re.findall(r'\breg\s+', code, re.IGNORECASE)
            return len(wires) + len(regs)
        return 0
    
    def _count_processes(self, code: str, language: str) -> int:
        """Count processes/always blocks in HDL code."""
        if language == 'vhdl':
            processes = re.findall(r'\bprocess\b', code, re.IGNORECASE)
            return len(processes)
        elif language == 'verilog':
            always_blocks = re.findall(r'\balways\b', code, re.IGNORECASE)
            return len(always_blocks)
        return 0
    
    def _compile_vhdl(self, entity_name: str, hdl_file: str, build_dir: str) -> CompilationResult:
        """Compile VHDL code using GHDL."""
        build_files = []
        warnings = []
        
        try:
            # Analyze (compile) the VHDL file
            analyze_cmd = [
                self.ghdl_path, '-a',
                f'--workdir={build_dir}'
            ] + self.additional_flags.get('vhdl', []) + [hdl_file]
            
            result = subprocess.run(analyze_cmd, capture_output=True, text=True, timeout=self.timeout)
            
            if result.returncode != 0:
                return CompilationResult(
                    success=False,
                    entity_name=entity_name,
                    language='vhdl',
                    build_files=build_files,
                    error_message=result.stderr
                )
            
            if result.stderr:
                warnings.append(result.stderr)
            
            # Elaborate the design
            elaborate_cmd = [
                self.ghdl_path, '-e',
                f'--workdir={build_dir}',
                entity_name
            ]
            
            result = subprocess.run(elaborate_cmd, capture_output=True, text=True, timeout=self.timeout)
            
            if result.returncode != 0:
                return CompilationResult(
                    success=False,
                    entity_name=entity_name,
                    language='vhdl',
                    build_files=build_files,
                    error_message=result.stderr
                )
            
            if result.stderr:
                warnings.append(result.stderr)
            
            # Collect build artifacts
            for file in os.listdir(build_dir):
                file_path = os.path.join(build_dir, file)
                if os.path.isfile(file_path):
                    build_files.append(file_path)
            
            return CompilationResult(
                success=True,
                entity_name=entity_name,
                language='vhdl',
                build_files=build_files,
                warnings=warnings
            )
            
        except subprocess.TimeoutExpired:
            return CompilationResult(
                success=False,
                entity_name=entity_name,
                language='vhdl',
                build_files=build_files,
                error_message=f"Compilation timeout after {self.timeout} seconds"
            )
        except Exception as e:
            return CompilationResult(
                success=False,
                entity_name=entity_name,
                language='vhdl',
                build_files=build_files,
                error_message=str(e)
            )
    
    def _compile_verilog(self, entity_name: str, hdl_file: str, build_dir: str) -> CompilationResult:
        """Compile Verilog code using Icarus Verilog."""
        build_files = []
        warnings = []
        
        try:
            # Compile with Icarus Verilog
            output_file = os.path.join(build_dir, f"{entity_name}.out")
            compile_cmd = [
                self.iverilog_path,
                '-o', output_file
            ] + self.additional_flags.get('verilog', []) + [hdl_file]
            
            result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=self.timeout)
            
            if result.returncode != 0:
                return CompilationResult(
                    success=False,
                    entity_name=entity_name,
                    language='verilog',
                    build_files=build_files,
                    error_message=result.stderr
                )
            
            if result.stderr:
                warnings.append(result.stderr)
            
            # Collect build artifacts
            for file in os.listdir(build_dir):
                file_path = os.path.join(build_dir, file)
                if os.path.isfile(file_path):
                    build_files.append(file_path)
            
            return CompilationResult(
                success=True,
                entity_name=entity_name,
                language='verilog',
                build_files=build_files,
                warnings=warnings
            )
            
        except subprocess.TimeoutExpired:
            return CompilationResult(
                success=False,
                entity_name=entity_name,
                language='verilog',
                build_files=build_files,
                error_message=f"Compilation timeout after {self.timeout} seconds"
            )
        except Exception as e:
            return CompilationResult(
                success=False,
                entity_name=entity_name,
                language='verilog',
                build_files=build_files,
                error_message=str(e)
            )
    
    def _create_json_string(self, data: Dict[str, Any]) -> str:
        """Create JSON string from data."""
        import json
        return json.dumps(data, indent=2, default=str)
    
    def _generate_project_readme(self, hdl_code: HDLCode, compilation_result: CompilationResult) -> str:
        """Generate README content for the project."""
        readme = f"""HDL AI Proteus Project - {hdl_code.entity_name}
{'=' * (30 + len(hdl_code.entity_name))}

Project Information:
- Entity/Module Name: {hdl_code.entity_name}
- HDL Language: {hdl_code.language.upper()}
- Generated by: HDL AI Proteus
- Compilation Status: {'SUCCESS' if compilation_result.success else 'FAILED'}

File Contents:
- {hdl_code.entity_name}.{hdl_code.file_extension}: Main HDL source file
- project_info.json: Project metadata
- README.txt: This file

"""
        
        if hdl_code.metadata:
            readme += f"""Code Statistics:
- Lines of Code: {hdl_code.metadata.get('lines_of_code', 'N/A')}
- Signals/Wires: {hdl_code.metadata.get('signals_count', 'N/A')}
- Processes/Always Blocks: {hdl_code.metadata.get('processes_count', 'N/A')}
- Libraries Used: {', '.join(hdl_code.metadata.get('libraries_used', [])) or 'None'}
- Contains Testbench: {'Yes' if hdl_code.metadata.get('has_testbench', False) else 'No'}

"""
        
        if compilation_result.warnings:
            readme += f"""Compilation Warnings:
{chr(10).join(compilation_result.warnings)}

"""
        
        if not compilation_result.success:
            readme += f"""Compilation Error:
{compilation_result.error_message}

"""
        
        readme += """Usage Instructions:
1. Extract this .pdsprj file to access the HDL source code
2. Import the HDL file into your preferred simulation tool
3. Verify the design meets your requirements
4. Modify as needed for your specific application

Note: This project was generated using AI and should be reviewed
before use in production applications.
"""
        
        return readme