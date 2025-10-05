#!/usr/bin/env python3
"""
HDL AI Proteus - Python Examples

This file contains comprehensive examples of using the HDL AI Proteus API 
with Python requests library, including error handling, file management,
and advanced usage patterns.

Requirements:
    pip install requests

Usage:
    python3 python_examples.py
"""

import requests
import json
import os
import time
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path


class HDLProteusAPI:
    """
    Python client for HDL AI Proteus API
    
    This class provides a convenient interface for interacting with the
    HDL AI Proteus API, including provider testing, HDL generation,
    and file management.
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the HDL AI Proteus API
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'HDL-Proteus-Python-Client/1.0'
        })
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            Dictionary containing health status information
            
        Raises:
            requests.RequestException: If API is unreachable
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to check API health: {e}")
    
    def get_api_info(self) -> Dict[str, Any]:
        """
        Get comprehensive API information.
        
        Returns:
            Dictionary containing API information and capabilities
        """
        response = self.session.get(f"{self.base_url}/api/info")
        response.raise_for_status()
        return response.json()
    
    def list_providers(self) -> Dict[str, Any]:
        """
        List all available AI providers.
        
        Returns:
            Dictionary containing provider information
        """
        response = self.session.get(f"{self.base_url}/api/providers")
        response.raise_for_status()
        return response.json()
    
    def get_provider_template(self, provider_type: str) -> Dict[str, Any]:
        """
        Get configuration template for a specific provider.
        
        Args:
            provider_type: Type of provider (e.g., 'azure_openai', 'gemini')
            
        Returns:
            Dictionary containing provider configuration template
        """
        response = self.session.get(f"{self.base_url}/api/providers/{provider_type}/template")
        response.raise_for_status()
        return response.json()
    
    def test_provider(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test connection to an AI provider.
        
        Args:
            provider_config: Provider configuration dictionary
            
        Returns:
            Dictionary containing test results
            
        Raises:
            Exception: If provider test fails
        """
        payload = {"provider_config": provider_config}
        response = self.session.post(f"{self.base_url}/test-provider", json=payload)
        
        result = response.json()
        
        if not response.ok or not result.get('success', False):
            error_msg = result.get('error', 'Unknown error')
            suggestion = result.get('suggestion', '')
            raise Exception(f"Provider test failed: {error_msg}. {suggestion}")
        
        return result
    
    def generate_hdl(
        self,
        prompt: str,
        circuit_name: str,
        provider_config: Dict[str, Any],
        generation_params: Optional[Dict[str, Any]] = None,
        output_dir: str = ".",
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Generate HDL code and download Proteus project file.
        
        Args:
            prompt: Natural language description of the circuit
            circuit_name: Name for the generated circuit
            provider_config: AI provider configuration
            generation_params: Optional generation parameters
            output_dir: Directory to save the generated file
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary containing generation results and metadata
            
        Raises:
            Exception: If generation fails
        """
        # Validate inputs
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        if not circuit_name.strip() or not circuit_name.replace('_', '').isalnum():
            raise ValueError("Circuit name must contain only alphanumeric characters and underscores")
        
        # Test provider connection first
        print(f"🔍 Testing provider connection...")
        try:
            test_result = self.test_provider(provider_config)
            print(f"✅ Provider connection successful: {test_result.get('model', 'unknown')}")
        except Exception as e:
            raise Exception(f"Provider test failed: {e}")
        
        # Prepare payload
        payload = {
            "prompt": prompt,
            "circuit_name": circuit_name,
            "provider_config": provider_config
        }
        
        if generation_params:
            payload["generation_params"] = generation_params
        
        print(f"🚀 Generating HDL code for '{circuit_name}'...")
        print(f"   Prompt length: {len(prompt)} characters")
        print(f"   Provider: {provider_config.get('provider_type', 'unknown')}")
        
        start_time = time.time()
        
        # Make request
        response = self.session.post(
            f"{self.base_url}/generate",
            json=payload,
            timeout=timeout
        )
        
        generation_time = time.time() - start_time
        
        if not response.ok:
            error_data = response.json()
            error_msg = error_data.get('error', 'Unknown error')
            suggestion = error_data.get('suggestion', '')
            raise Exception(f"Generation failed: {error_msg}. {suggestion}")
        
        # Extract metadata from headers
        metadata = {
            'hdl_language': response.headers.get('X-HDL-Language', 'unknown'),
            'provider_used': response.headers.get('X-Provider-Used', 'unknown'),
            'compilation_success': response.headers.get('X-Compilation-Success', 'false').lower() == 'true',
            'generation_metadata': response.headers.get('X-Generation-Metadata', '{}'),
            'file_size': len(response.content),
            'total_time': generation_time
        }
        
        # Save file
        output_path = Path(output_dir) / f"{circuit_name}.pdsprj"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Generation completed successfully!")
        print(f"   File: {output_path} ({metadata['file_size']} bytes)")
        print(f"   Language: {metadata['hdl_language'].upper()}")
        print(f"   Provider: {metadata['provider_used']}")
        print(f"   Compilation: {'✅ Success' if metadata['compilation_success'] else '❌ Failed'}")
        print(f"   Total time: {generation_time:.2f}s")
        
        return {
            'file_path': str(output_path),
            'metadata': metadata,
            'success': True
        }


# Example configurations
EXAMPLE_CONFIGS = {
    'azure_openai': {
        'provider_type': 'azure_openai',
        'api_key': 'your-azure-openai-api-key',
        'endpoint': 'https://your-resource.openai.azure.com/',
        'api_version': '2024-05-01-preview',
        'model_name': 'gpt-4o-mini'
    },
    'gemini': {
        'provider_type': 'gemini',
        'api_key': 'your-gemini-api-key',
        'model_name': 'gemini-pro'
    },
    'openai': {
        'provider_type': 'openai',
        'api_key': 'your-openai-api-key',
        'model_name': 'gpt-4',
        'organization': 'your-org-id'  # Optional
    }
}

# Example prompts
EXAMPLE_PROMPTS = [
    {
        'name': 'counter_4bit',
        'prompt': 'Create a 4-bit counter in VHDL with clock, reset, and enable inputs. The counter should increment on each rising edge of the clock when enable is active. Use IEEE.STD_LOGIC_1164 and IEEE.NUMERIC_STD libraries.',
        'language': 'VHDL'
    },
    {
        'name': 'and_gate',
        'prompt': 'Create a simple 2-input AND gate in VHDL with inputs a and b, and output y. Use IEEE.STD_LOGIC_1164 library.',
        'language': 'VHDL'
    },
    {
        'name': 'alu_8bit',
        'prompt': 'Design an 8-bit ALU in Verilog with the following operations: ADD, SUB, AND, OR. Inputs: a[7:0], b[7:0], op[1:0]. Outputs: result[7:0], zero_flag. Operation codes: 00=ADD, 01=SUB, 10=AND, 11=OR.',
        'language': 'Verilog'
    },
    {
        'name': 'shift_register',
        'prompt': 'Create an 8-bit shift register in VHDL with parallel load capability. Inputs: clk, reset, load, shift_en, parallel_in[7:0], serial_in. Outputs: parallel_out[7:0], serial_out.',
        'language': 'VHDL'
    },
    {
        'name': 'dff_async_reset',
        'prompt': 'Create a D flip-flop in Verilog with asynchronous reset. Inputs: d, clk, reset_n. Outputs: q, q_n.',
        'language': 'Verilog'
    }
]


def example_basic_usage():
    """Basic usage example with error handling."""
    print("🔧 Basic Usage Example")
    print("=" * 50)
    
    # Initialize API client
    api = HDLProteusAPI()
    
    try:
        # Check API health
        health = api.check_health()
        print(f"✅ API is healthy: {health['service']} v{health['version']}")
        
        # Get API info
        info = api.get_api_info()
        print(f"📊 Supported providers: {', '.join(info['supported_providers'])}")
        print(f"📊 Supported languages: {', '.join(info['supported_languages'])}")
        
        # Example provider config (replace with your credentials)
        provider_config = {
            'provider_type': 'azure_openai',
            'api_key': 'your-api-key-here',
            'endpoint': 'https://your-resource.openai.azure.com/',
            'api_version': '2024-05-01-preview',
            'model_name': 'gpt-4o-mini'
        }
        
        # Generate a simple circuit
        result = api.generate_hdl(
            prompt="Create a 2-input OR gate in VHDL",
            circuit_name="or_gate_example",
            provider_config=provider_config,
            output_dir="generated_projects"
        )
        
        print(f"🎉 Success! File saved to: {result['file_path']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_batch_generation():
    """Example of generating multiple circuits in batch."""
    print("\n🔄 Batch Generation Example")
    print("=" * 50)
    
    api = HDLProteusAPI()
    
    # Provider configuration (replace with your credentials)
    provider_config = EXAMPLE_CONFIGS['azure_openai']
    
    # Generation parameters
    generation_params = {
        'temperature': 0.3,
        'max_tokens': 2000
    }
    
    results = []
    
    for example in EXAMPLE_PROMPTS[:3]:  # Generate first 3 examples
        try:
            print(f"\n🚀 Generating {example['name']} ({example['language']})...")
            
            result = api.generate_hdl(
                prompt=example['prompt'],
                circuit_name=example['name'],
                provider_config=provider_config,
                generation_params=generation_params,
                output_dir="batch_generated"
            )
            
            results.append({
                'name': example['name'],
                'success': True,
                'file_path': result['file_path'],
                'metadata': result['metadata']
            })
            
            # Rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Failed to generate {example['name']}: {e}")
            results.append({
                'name': example['name'],
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n📊 Batch Generation Summary")
    print("=" * 30)
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print("\n✅ Generated files:")
        for result in successful:
            metadata = result['metadata']
            print(f"  • {result['name']}: {metadata['hdl_language']} ({metadata['file_size']} bytes)")
    
    if failed:
        print("\n❌ Failed generations:")
        for result in failed:
            print(f"  • {result['name']}: {result['error']}")


def example_advanced_features():
    """Example showcasing advanced features."""
    print("\n🚀 Advanced Features Example")
    print("=" * 50)
    
    api = HDLProteusAPI()
    
    try:
        # Get provider templates
        print("📋 Available provider templates:")
        providers_info = api.list_providers()
        
        for provider_type in providers_info['providers'].keys():
            try:
                template = api.get_provider_template(provider_type)
                print(f"  • {provider_type}: {template['description']}")
                
                required_fields = template.get('required_fields', {})
                print(f"    Required: {list(required_fields.keys())}")
                
            except Exception as e:
                print(f"  • {provider_type}: Error getting template - {e}")
        
        # Test multiple providers (if configured)
        print(f"\n🔍 Testing provider connections:")
        
        for provider_name, config in EXAMPLE_CONFIGS.items():
            try:
                result = api.test_provider(config)
                print(f"  ✅ {provider_name}: {result['model']} ({result['response_time']:.2f}s)")
            except Exception as e:
                print(f"  ❌ {provider_name}: {e}")
        
        # Generate with custom parameters
        print(f"\n⚙️ Generating with custom parameters:")
        
        custom_params = {
            'temperature': 0.1,  # More deterministic
            'max_tokens': 3000
        }
        
        provider_config = EXAMPLE_CONFIGS['azure_openai']
        
        result = api.generate_hdl(
            prompt="Create a comprehensive 4-bit CPU in VHDL with instruction set architecture including ADD, SUB, LOAD, STORE instructions",
            circuit_name="cpu_4bit_advanced",
            provider_config=provider_config,
            generation_params=custom_params,
            output_dir="advanced_projects"
        )
        
        # Parse generation metadata
        metadata_str = result['metadata'].get('generation_metadata', '{}')
        try:
            detailed_metadata = json.loads(metadata_str)
            print(f"\n📊 Detailed Generation Metadata:")
            for key, value in detailed_metadata.items():
                print(f"  • {key}: {value}")
        except json.JSONDecodeError:
            print(f"  Could not parse detailed metadata")
        
    except Exception as e:
        print(f"❌ Error in advanced features demo: {e}")


def example_error_handling():
    """Example demonstrating comprehensive error handling."""
    print("\n🛡️ Error Handling Examples")
    print("=" * 50)
    
    api = HDLProteusAPI()
    
    # Test different error scenarios
    error_scenarios = [
        {
            'name': 'Invalid Provider Type',
            'config': {
                'provider_type': 'invalid_provider',
                'api_key': 'fake-key'
            },
            'prompt': 'Create an AND gate',
            'circuit_name': 'test_circuit'
        },
        {
            'name': 'Missing Required Fields',
            'config': {
                'provider_type': 'azure_openai',
                'api_key': 'fake-key'
                # Missing endpoint and api_version
            },
            'prompt': 'Create an AND gate',
            'circuit_name': 'test_circuit'
        },
        {
            'name': 'Invalid Circuit Name',
            'config': EXAMPLE_CONFIGS['azure_openai'],
            'prompt': 'Create an AND gate',
            'circuit_name': 'invalid-name!'
        },
        {
            'name': 'Empty Prompt',
            'config': EXAMPLE_CONFIGS['azure_openai'],
            'prompt': '',
            'circuit_name': 'test_circuit'
        }
    ]
    
    for scenario in error_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        try:
            api.generate_hdl(
                prompt=scenario['prompt'],
                circuit_name=scenario['circuit_name'],
                provider_config=scenario['config']
            )
            print(f"  ⚠️ Unexpected success!")
        except ValueError as e:
            print(f"  ✅ Validation error caught: {e}")
        except Exception as e:
            print(f"  ✅ Error caught: {e}")


def example_file_management():
    """Example showing file management best practices."""
    print("\n📁 File Management Example")
    print("=" * 50)
    
    # Create organized directory structure
    base_dir = Path("hdl_projects")
    subdirs = ["basic_gates", "counters", "alu_designs", "memory_elements"]
    
    for subdir in subdirs:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Created directory structure in: {base_dir}")
    
    # Generate circuits in organized folders
    api = HDLProteusAPI()
    provider_config = EXAMPLE_CONFIGS['azure_openai']
    
    organized_examples = [
        {
            'folder': 'basic_gates',
            'circuits': [
                ('and_gate_2input', 'Create a 2-input AND gate in VHDL'),
                ('or_gate_2input', 'Create a 2-input OR gate in VHDL'),
                ('nand_gate_2input', 'Create a 2-input NAND gate in VHDL')
            ]
        },
        {
            'folder': 'counters',
            'circuits': [
                ('counter_4bit', 'Create a 4-bit up counter in VHDL'),
                ('counter_8bit_updown', 'Create an 8-bit up/down counter in VHDL')
            ]
        }
    ]
    
    try:
        for category in organized_examples:
            folder = category['folder']
            print(f"\n📂 Generating {folder} circuits:")
            
            for circuit_name, prompt in category['circuits']:
                output_dir = base_dir / folder
                
                try:
                    result = api.generate_hdl(
                        prompt=prompt,
                        circuit_name=circuit_name,
                        provider_config=provider_config,
                        output_dir=str(output_dir)
                    )
                    print(f"  ✅ {circuit_name}")
                    
                except Exception as e:
                    print(f"  ❌ {circuit_name}: {e}")
        
        # List generated files
        print(f"\n📊 Generated Project Structure:")
        for subdir in subdirs:
            subdir_path = base_dir / subdir
            if subdir_path.exists():
                files = list(subdir_path.glob("*.pdsprj"))
                if files:
                    print(f"  📁 {subdir}/ ({len(files)} files)")
                    for file in files:
                        size_kb = file.stat().st_size / 1024
                        print(f"    📄 {file.name} ({size_kb:.1f} KB)")
    
    except Exception as e:
        print(f"❌ Error in file management demo: {e}")


def main():
    """Main function demonstrating all examples."""
    print("🔧 HDL AI Proteus - Python Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use the HDL AI Proteus API")
    print("⚠️  Make sure to replace API keys with your actual credentials!")
    print()
    
    # Run examples
    try:
        example_basic_usage()
        example_batch_generation()
        example_advanced_features()
        example_error_handling()
        example_file_management()
        
        print("\n🎉 All examples completed!")
        print("\n📚 Next steps:")
        print("  1. Replace example API keys with your actual credentials")
        print("  2. Customize prompts for your specific requirements")
        print("  3. Integrate the HDLProteusAPI class into your projects")
        print("  4. Check generated .pdsprj files in Proteus software")
        
    except KeyboardInterrupt:
        print("\n🛑 Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()