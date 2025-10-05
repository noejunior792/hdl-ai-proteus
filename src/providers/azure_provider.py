import requests
from typing import Dict, Any, Optional
from .base_provider import BaseAIProvider, AIProviderConfig, AIResponse


class AzureOpenAIProvider(BaseAIProvider):
    """
    Azure OpenAI provider for generating HDL code.
    
    This provider uses Azure OpenAI service to generate VHDL/Verilog code
    from natural language descriptions.
    """

    def __init__(self, config: AIProviderConfig):
        """
        Initialize Azure OpenAI provider.
        
        Args:
            config: Configuration object with Azure OpenAI settings
        """
        super().__init__(config)
        self.deployment_name = config.additional_params.get('deployment_name', 'gpt-4o') if config.additional_params else 'gpt-4o'
        
    def validate_config(self) -> bool:
        """
        Validate Azure OpenAI configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing
        """
        required_fields = ['api_key', 'endpoint', 'api_version']
        missing_fields = []
        
        for field in required_fields:
            value = getattr(self.config, field, None)
            if not value:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing required Azure OpenAI configuration: {', '.join(missing_fields)}")
        
        # Validate endpoint format
        if not self.config.endpoint.startswith('https://'):
            raise ValueError("Azure endpoint must start with 'https://'")
        
        if not self.config.endpoint.endswith('/'):
            self.config.endpoint += '/'
            
        return True

    def generate_code(self, prompt: str, **kwargs) -> AIResponse:
        """
        Generate HDL code using Azure OpenAI.
        
        Args:
            prompt: Natural language description of the circuit
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
            
        Returns:
            AIResponse object containing generated code and metadata
            
        Raises:
            Exception: If API call fails or returns invalid response
        """
        self.validate_config()
        
        # Override config with kwargs if provided
        temperature = kwargs.get('temperature', self.config.temperature)
        max_tokens = kwargs.get('max_tokens', self.config.max_tokens)
        deployment_name = kwargs.get('deployment_name', self.deployment_name)
        
        # Construct API URL
        url = (
            f"{self.config.endpoint}openai/deployments/{deployment_name}/"
            f"chat/completions?api-version={self.config.api_version}"
        )
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "api-key": self.config.api_key,
        }
        
        # Prepare request data
        data = {
            "messages": self.prepare_messages(prompt),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        # Add any additional parameters from config
        if self.config.additional_params:
            for key, value in self.config.additional_params.items():
                if key not in ['deployment_name'] and key not in data:
                    data[key] = value
        
        try:
            # Make API request
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            # Parse response
            response_data = response.json()
            
            # Extract content
            content = response_data["choices"][0]["message"]["content"]
            
            # Extract usage information if available
            usage = response_data.get("usage", {})
            
            # Create metadata
            metadata = {
                "deployment_name": deployment_name,
                "api_version": self.config.api_version,
                "endpoint": self.config.endpoint,
                "request_id": response.headers.get("x-request-id"),
                "response_time": response.elapsed.total_seconds()
            }
            
            return AIResponse(
                content=content,
                provider="azure_openai",
                model=deployment_name,
                usage=usage,
                metadata=metadata
            )
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Azure OpenAI API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Invalid response format from Azure OpenAI: missing {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to generate code with Azure OpenAI: {str(e)}")

    def get_provider_info(self) -> Dict[str, Any]:
        """
        Get Azure OpenAI provider information.
        
        Returns:
            Dictionary containing provider information
        """
        return {
            "provider_name": "Azure OpenAI",
            "provider_type": "azure_openai",
            "supported_models": [
                "gpt-4",
                "gpt-4-32k",
                "gpt-4o",
                "gpt-4-turbo",
                "gpt-35-turbo",
                "gpt-35-turbo-16k"
            ],
            "required_config": [
                "api_key",
                "endpoint", 
                "api_version"
            ],
            "optional_config": [
                "deployment_name",
                "temperature",
                "max_tokens"
            ],
            "description": "Microsoft Azure OpenAI Service provider for HDL code generation",
            "documentation_url": "https://docs.microsoft.com/en-us/azure/cognitive-services/openai/"
        }

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Azure OpenAI service.
        
        Returns:
            Dictionary with connection test results
        """
        try:
            self.validate_config()
            
            # Simple test prompt
            test_prompt = "Generate a simple AND gate in VHDL"
            response = self.generate_code(test_prompt, max_tokens=100)
            
            return {
                "success": True,
                "message": "Connection successful",
                "provider": "azure_openai",
                "model": response.model,
                "response_time": response.metadata.get("response_time", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "provider": "azure_openai"
            }

    @classmethod
    def create_from_dict(cls, config_dict: Dict[str, Any]) -> 'AzureOpenAIProvider':
        """
        Create provider instance from configuration dictionary.
        
        Args:
            config_dict: Dictionary containing configuration parameters
            
        Returns:
            AzureOpenAIProvider instance
        """
        config = AIProviderConfig(
            provider_name="azure_openai",
            model_name=config_dict.get('model_name', 'gpt-4o'),
            api_key=config_dict['api_key'],
            endpoint=config_dict['endpoint'],
            api_version=config_dict['api_version'],
            temperature=config_dict.get('temperature', 0.7),
            max_tokens=config_dict.get('max_tokens', 2000),
            additional_params=config_dict.get('additional_params', {})
        )
        
        return cls(config)