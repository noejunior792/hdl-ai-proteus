from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class AIResponse:
    """Standardized response from AI providers"""
    content: str
    provider: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AIProviderConfig:
    """Configuration for AI providers"""
    provider_name: str
    model_name: str
    api_key: str
    endpoint: Optional[str] = None
    api_version: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    additional_params: Optional[Dict[str, Any]] = None


class BaseAIProvider(ABC):
    """
    Abstract base class for AI providers.
    
    This class defines the interface that all AI providers must implement
    to generate HDL code from natural language prompts.
    """

    def __init__(self, config: AIProviderConfig):
        """
        Initialize the AI provider with configuration.
        
        Args:
            config: Configuration object containing provider settings
        """
        self.config = config
        self.system_prompt = (
            "You are a hardware design assistant. Generate VHDL or Verilog code "
            "for the given circuit description. When generating VHDL, use the "
            "IEEE.NUMERIC_STD.ALL library for arithmetic operations and avoid "
            "using the non-standard IEEE.STD_LOGIC_UNSIGNED or IEEE.STD_LOGIC_ARITH "
            "libraries. Always include proper entity/module declarations and "
            "architecture/implementation blocks. Ensure the code is syntactically "
            "correct and follows best practices."
        )

    @abstractmethod
    def generate_code(self, prompt: str, **kwargs) -> AIResponse:
        """
        Generate HDL code from a natural language prompt.
        
        Args:
            prompt: Natural language description of the circuit
            **kwargs: Additional provider-specific parameters
            
        Returns:
            AIResponse object containing the generated code and metadata
            
        Raises:
            Exception: If code generation fails
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate the provider configuration.
        
        Returns:
            True if configuration is valid, False otherwise
            
        Raises:
            ValueError: If required configuration is missing
        """
        pass

    @abstractmethod
    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get information about the provider.
        
        Returns:
            Dictionary containing provider information
        """
        pass

    def set_system_prompt(self, prompt: str) -> None:
        """
        Set a custom system prompt.
        
        Args:
            prompt: Custom system prompt for the AI
        """
        self.system_prompt = prompt

    def get_system_prompt(self) -> str:
        """
        Get the current system prompt.
        
        Returns:
            Current system prompt string
        """
        return self.system_prompt

    def prepare_messages(self, user_prompt: str) -> List[Dict[str, str]]:
        """
        Prepare messages for the AI provider.
        
        Args:
            user_prompt: User's natural language prompt
            
        Returns:
            List of message dictionaries
        """
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def extract_code_from_response(self, content: str) -> tuple[str, str]:
        """
        Extract HDL code and language from AI response.
        
        Args:
            content: Raw content from AI response
            
        Returns:
            Tuple of (language, code)
        """
        import re
        
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