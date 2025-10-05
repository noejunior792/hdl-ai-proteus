from typing import Dict, Any, Type, Optional
from .base_provider import BaseAIProvider, AIProviderConfig
from .azure_provider import AzureOpenAIProvider
from .gemini_provider import GeminiProvider
from .openai_provider import OpenAIProvider


class ProviderFactory:
    """
    Factory class for creating AI provider instances.
    
    This factory allows dynamic creation of AI providers based on
    configuration parameters and supports registration of new providers.
    """
    
    # Registry of available providers
    _providers: Dict[str, Type[BaseAIProvider]] = {
        'azure_openai': AzureOpenAIProvider,
        'azure': AzureOpenAIProvider,  # Alias
        'gemini': GeminiProvider,
        'google_gemini': GeminiProvider,  # Alias
        'openai': OpenAIProvider,
        'gpt': OpenAIProvider,  # Alias
    }
    
    @classmethod
    def create_provider(cls, provider_type: str, config: Dict[str, Any]) -> BaseAIProvider:
        """
        Create an AI provider instance.
        
        Args:
            provider_type: Type of provider to create (e.g., 'azure_openai', 'gemini', 'openai')
            config: Configuration dictionary for the provider
            
        Returns:
            Configured AI provider instance
            
        Raises:
            ValueError: If provider type is not supported
            Exception: If provider creation fails
        """
        provider_type = provider_type.lower().strip()
        
        if provider_type not in cls._providers:
            available_providers = list(cls._providers.keys())
            raise ValueError(
                f"Unsupported provider type '{provider_type}'. "
                f"Available providers: {', '.join(available_providers)}"
            )
        
        provider_class = cls._providers[provider_type]
        
        try:
            # Use getattr to safely call create_from_dict method
            if hasattr(provider_class, 'create_from_dict'):
                return provider_class.create_from_dict(config)
            else:
                # Fallback to manual creation
                provider_config = AIProviderConfig(
                    provider_name=provider_type,
                    model_name=config.get('model_name', 'default'),
                    api_key=config['api_key'],
                    endpoint=config.get('endpoint'),
                    api_version=config.get('api_version'),
                    temperature=config.get('temperature', 0.7),
                    max_tokens=config.get('max_tokens', 2000),
                    additional_params=config.get('additional_params', {})
                )
                return provider_class(provider_config)
        except Exception as e:
            raise Exception(f"Failed to create {provider_type} provider: {str(e)}")
    
    @classmethod
    def create_provider_from_config(cls, provider_type: str, config: AIProviderConfig) -> BaseAIProvider:
        """
        Create an AI provider instance from AIProviderConfig.
        
        Args:
            provider_type: Type of provider to create
            config: AIProviderConfig instance
            
        Returns:
            Configured AI provider instance
            
        Raises:
            ValueError: If provider type is not supported
        """
        provider_type = provider_type.lower().strip()
        
        if provider_type not in cls._providers:
            available_providers = list(cls._providers.keys())
            raise ValueError(
                f"Unsupported provider type '{provider_type}'. "
                f"Available providers: {', '.join(available_providers)}"
            )
        
        provider_class = cls._providers[provider_type]
        return provider_class(config)
    
    @classmethod
    def register_provider(cls, provider_type: str, provider_class: Type[BaseAIProvider]) -> None:
        """
        Register a new AI provider.
        
        Args:
            provider_type: String identifier for the provider
            provider_class: Provider class that inherits from BaseAIProvider
            
        Raises:
            ValueError: If provider_class doesn't inherit from BaseAIProvider
        """
        if not issubclass(provider_class, BaseAIProvider):
            raise ValueError("Provider class must inherit from BaseAIProvider")
        
        cls._providers[provider_type.lower().strip()] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all available providers.
        
        Returns:
            Dictionary with provider information
        """
        providers_info = {}
        
        for provider_type, provider_class in cls._providers.items():
            try:
                # Create a temporary instance to get provider info
                temp_config = AIProviderConfig(
                    provider_name=provider_type,
                    model_name="temp",
                    api_key="temp"
                )
                temp_provider = provider_class(temp_config)
                providers_info[provider_type] = temp_provider.get_provider_info()
            except Exception:
                # If we can't create temp instance, provide basic info
                providers_info[provider_type] = {
                    "provider_name": provider_type,
                    "provider_type": provider_type,
                    "description": f"{provider_class.__name__} AI provider",
                    "error": "Could not retrieve detailed information"
                }
        
        return providers_info
    
    @classmethod
    def is_provider_supported(cls, provider_type: str) -> bool:
        """
        Check if a provider type is supported.
        
        Args:
            provider_type: Provider type to check
            
        Returns:
            True if provider is supported, False otherwise
        """
        return provider_type.lower().strip() in cls._providers
    
    @classmethod
    def get_provider_config_template(cls, provider_type: str) -> Dict[str, Any]:
        """
        Get configuration template for a specific provider.
        
        Args:
            provider_type: Provider type to get template for
            
        Returns:
            Dictionary with configuration template
            
        Raises:
            ValueError: If provider type is not supported
        """
        if not cls.is_provider_supported(provider_type):
            raise ValueError(f"Unsupported provider type: {provider_type}")
        
        provider_class = cls._providers[provider_type.lower().strip()]
        
        # Create temporary instance to get provider info
        try:
            temp_config = AIProviderConfig(
                provider_name=provider_type,
                model_name="temp",
                api_key="temp"
            )
            temp_provider = provider_class(temp_config)
            provider_info = temp_provider.get_provider_info()
            
            template = {
                "provider_type": provider_type,
                "required_config": {},
                "optional_config": {},
                "description": provider_info.get("description", ""),
                "supported_models": provider_info.get("supported_models", [])
            }
            
            # Add required config fields
            for field in provider_info.get("required_config", []):
                template["required_config"][field] = f"<{field}>"
            
            # Add optional config fields with defaults
            optional_defaults = {
                "temperature": 0.7,
                "max_tokens": 2000,
                "model_name": provider_info.get("supported_models", ["default"])[0] if provider_info.get("supported_models") else "default"
            }
            
            for field in provider_info.get("optional_config", []):
                template["optional_config"][field] = optional_defaults.get(field, f"<{field}>")
            
            return template
            
        except Exception as e:
            return {
                "provider_type": provider_type,
                "error": f"Could not generate template: {str(e)}",
                "required_config": {
                    "api_key": "<api_key>",
                    "model_name": "<model_name>"
                },
                "optional_config": {
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            }
    
    @classmethod
    def validate_provider_config(cls, provider_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate configuration for a specific provider.
        
        Args:
            provider_type: Provider type to validate config for
            config: Configuration dictionary to validate
            
        Returns:
            Dictionary with validation results
        """
        try:
            provider = cls.create_provider(provider_type, config)
            provider.validate_config()
            
            return {
                "valid": True,
                "message": "Configuration is valid",
                "provider_type": provider_type
            }
            
        except Exception as e:
            return {
                "valid": False,
                "message": str(e),
                "provider_type": provider_type
            }
    
    @classmethod
    def test_provider_connection(cls, provider_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test connection for a specific provider.
        
        Args:
            provider_type: Provider type to test
            config: Configuration dictionary
            
        Returns:
            Dictionary with connection test results
        """
        try:
            provider = cls.create_provider(provider_type, config)
            # Check if provider has test_connection method
            if hasattr(provider, 'test_connection'):
                return provider.test_connection()
            else:
                # Fallback test - try a simple generation
                try:
                    test_response = provider.generate_code("Simple test", max_tokens=10)
                    return {
                        "success": True,
                        "message": "Connection successful (basic test)",
                        "provider": provider_type,
                        "model": test_response.model
                    }
                except Exception as test_error:
                    return {
                        "success": False,
                        "message": f"Connection test failed: {str(test_error)}",
                        "provider": provider_type
                    }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to test connection: {str(e)}",
                "provider": provider_type
            }