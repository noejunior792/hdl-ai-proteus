"""
AI Providers Package

This package contains implementations of various AI providers for generating
HDL (Hardware Description Language) code from natural language prompts.

Available Providers:
- AzureOpenAIProvider: Microsoft Azure OpenAI Service
- GeminiProvider: Google Gemini AI
- OpenAIProvider: OpenAI GPT models

Usage:
    from providers import ProviderFactory, AzureOpenAIProvider
    
    # Create provider using factory
    config = {
        'api_key': 'your-api-key',
        'endpoint': 'your-endpoint',
        'api_version': '2024-02-15-preview',
        'model_name': 'gpt-4o'
    }
    provider = ProviderFactory.create_provider('azure_openai', config)
    
    # Generate HDL code
    response = provider.generate_code("Create a 4-bit counter in VHDL")
    print(response.content)
"""

from .base_provider import BaseAIProvider, AIProviderConfig, AIResponse
from .azure_provider import AzureOpenAIProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider
from .provider_factory import ProviderFactory

__all__ = [
    'BaseAIProvider',
    'AIProviderConfig', 
    'AIResponse',
    'AzureOpenAIProvider',
    'GeminiProvider',
    'OpenAIProvider',
    'ProviderFactory'
]

__version__ = "1.0.0"
__author__ = "HDL AI Proteus Team"