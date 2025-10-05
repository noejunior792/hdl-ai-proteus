"""
Validation Utilities Module

This module provides validation functions for request data, configuration,
and input sanitization for the HDL AI Proteus application.
"""

import re
import os
from typing import Dict, Any, List, Optional, Tuple
from werkzeug.utils import secure_filename


def validate_request_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate incoming request data for HDL generation.
    
    Args:
        data: Request data dictionary
        
    Returns:
        Dictionary with validation result and message
    """
    # Check required fields
    required_fields = ['prompt', 'circuit_name', 'provider_config']
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            'valid': False,
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }
    
    # Validate prompt
    prompt_validation = validate_prompt(data['prompt'])
    if not prompt_validation['valid']:
        return prompt_validation
    
    # Validate circuit name
    circuit_name_validation = validate_circuit_name(data['circuit_name'])
    if not circuit_name_validation['valid']:
        return circuit_name_validation
    
    # Validate provider config
    provider_config_validation = validate_provider_config(data['provider_config'])
    if not provider_config_validation['valid']:
        return provider_config_validation
    
    # Validate generation parameters if provided
    if 'generation_params' in data:
        params_validation = validate_generation_params(data['generation_params'])
        if not params_validation['valid']:
            return params_validation
    
    return {'valid': True, 'message': 'Validation successful'}


def validate_prompt(prompt: str) -> Dict[str, Any]:
    """
    Validate prompt text.
    
    Args:
        prompt: Prompt string to validate
        
    Returns:
        Dictionary with validation result
    """
    if not isinstance(prompt, str):
        return {'valid': False, 'message': 'Prompt must be a string'}
    
    # Check length
    min_length = 10
    max_length = 10000
    
    if len(prompt) < min_length:
        return {
            'valid': False,
            'message': f'Prompt too short (minimum {min_length} characters)'
        }
    
    if len(prompt) > max_length:
        return {
            'valid': False,
            'message': f'Prompt too long (maximum {max_length} characters)'
        }
    
    # Check for potentially harmful content
    suspicious_patterns = [
        r'<script[^>]*>',
        r'javascript:',
        r'data:text/html',
        r'vbscript:',
        r'onload\s*=',
        r'onerror\s*=',
        r'eval\s*\(',
        r'exec\s*\('
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {
                'valid': False,
                'message': 'Prompt contains potentially harmful content'
            }
    
    return {'valid': True, 'message': 'Prompt is valid'}


def validate_circuit_name(circuit_name: str) -> Dict[str, Any]:
    """
    Validate circuit name.
    
    Args:
        circuit_name: Circuit name to validate
        
    Returns:
        Dictionary with validation result
    """
    if not isinstance(circuit_name, str):
        return {'valid': False, 'message': 'Circuit name must be a string'}
    
    # Check length
    if len(circuit_name) < 1:
        return {'valid': False, 'message': 'Circuit name cannot be empty'}
    
    if len(circuit_name) > 100:
        return {'valid': False, 'message': 'Circuit name too long (maximum 100 characters)'}
    
    # Check valid characters (alphanumeric, underscore, hyphen)
    if not re.match(r'^[a-zA-Z0-9_-]+$', circuit_name):
        return {
            'valid': False,
            'message': 'Circuit name can only contain letters, numbers, underscores, and hyphens'
        }
    
    # Check that it starts with a letter or underscore
    if not re.match(r'^[a-zA-Z_]', circuit_name):
        return {
            'valid': False,
            'message': 'Circuit name must start with a letter or underscore'
        }
    
    # Check for reserved keywords
    reserved_keywords = [
        'and', 'or', 'not', 'xor', 'nand', 'nor', 'xnor',
        'begin', 'end', 'if', 'then', 'else', 'case', 'when',
        'process', 'signal', 'variable', 'entity', 'architecture',
        'library', 'use', 'package', 'component', 'port', 'map',
        'module', 'endmodule', 'always', 'initial', 'wire', 'reg',
        'input', 'output', 'inout', 'parameter', 'assign'
    ]
    
    if circuit_name.lower() in reserved_keywords:
        return {
            'valid': False,
            'message': f'Circuit name "{circuit_name}" is a reserved keyword'
        }
    
    return {'valid': True, 'message': 'Circuit name is valid'}


def validate_provider_config(provider_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate provider configuration.
    
    Args:
        provider_config: Provider configuration dictionary
        
    Returns:
        Dictionary with validation result
    """
    if not isinstance(provider_config, dict):
        return {'valid': False, 'message': 'Provider config must be a dictionary'}
    
    # Check for provider type
    if 'provider_type' not in provider_config:
        return {'valid': False, 'message': 'provider_type is required in provider_config'}
    
    provider_type = provider_config['provider_type']
    
    # Validate based on provider type
    if provider_type in ['azure_openai', 'azure']:
        return validate_azure_config(provider_config)
    elif provider_type in ['openai', 'gpt']:
        return validate_openai_config(provider_config)
    elif provider_type in ['gemini', 'google_gemini']:
        return validate_gemini_config(provider_config)
    else:
        return {
            'valid': False,
            'message': f'Unsupported provider type: {provider_type}'
        }


def validate_azure_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Azure OpenAI configuration."""
    required_fields = ['api_key', 'endpoint', 'api_version']
    
    for field in required_fields:
        if field not in config or not config[field]:
            return {'valid': False, 'message': f'Missing required field: {field}'}
    
    # Validate endpoint format
    endpoint = config['endpoint']
    if not endpoint.startswith('https://'):
        return {'valid': False, 'message': 'Azure endpoint must start with https://'}
    
    if not re.match(r'https://[a-zA-Z0-9-]+\.openai\.azure\.com/?', endpoint):
        return {'valid': False, 'message': 'Invalid Azure OpenAI endpoint format'}
    
    # Validate API version format
    api_version = config['api_version']
    if not re.match(r'\d{4}-\d{2}-\d{2}(-preview)?', api_version):
        return {'valid': False, 'message': 'Invalid API version format (should be YYYY-MM-DD or YYYY-MM-DD-preview)'}
    
    return {'valid': True, 'message': 'Azure config is valid'}


def validate_openai_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate OpenAI configuration."""
    required_fields = ['api_key', 'model_name']
    
    for field in required_fields:
        if field not in config or not config[field]:
            return {'valid': False, 'message': f'Missing required field: {field}'}
    
    # Validate API key format
    api_key = config['api_key']
    if not api_key.startswith('sk-'):
        return {'valid': False, 'message': 'OpenAI API key should start with sk-'}
    
    return {'valid': True, 'message': 'OpenAI config is valid'}


def validate_gemini_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Gemini configuration."""
    required_fields = ['api_key', 'model_name']
    
    for field in required_fields:
        if field not in config or not config[field]:
            return {'valid': False, 'message': f'Missing required field: {field}'}
    
    # Validate model name format
    model_name = config['model_name']
    if not model_name.startswith('gemini-'):
        return {'valid': False, 'message': 'Gemini model name should start with gemini-'}
    
    return {'valid': True, 'message': 'Gemini config is valid'}


def validate_generation_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate generation parameters.
    
    Args:
        params: Generation parameters dictionary
        
    Returns:
        Dictionary with validation result
    """
    if not isinstance(params, dict):
        return {'valid': False, 'message': 'Generation params must be a dictionary'}
    
    # Validate temperature
    if 'temperature' in params:
        temp = params['temperature']
        if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
            return {'valid': False, 'message': 'Temperature must be a number between 0 and 2'}
    
    # Validate max_tokens
    if 'max_tokens' in params:
        max_tokens = params['max_tokens']
        if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 8000:
            return {'valid': False, 'message': 'max_tokens must be an integer between 1 and 8000'}
    
    # Validate top_p
    if 'top_p' in params:
        top_p = params['top_p']
        if not isinstance(top_p, (int, float)) or top_p < 0 or top_p > 1:
            return {'valid': False, 'message': 'top_p must be a number between 0 and 1'}
    
    return {'valid': True, 'message': 'Generation params are valid'}


def sanitize_circuit_name(circuit_name: str) -> str:
    """
    Sanitize circuit name to be safe for file system usage.
    
    Args:
        circuit_name: Original circuit name
        
    Returns:
        Sanitized circuit name
    """
    # Use werkzeug's secure_filename as base
    safe_name = secure_filename(circuit_name)
    
    # Replace spaces and special characters with underscores
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', safe_name)
    
    # Remove multiple consecutive underscores
    safe_name = re.sub(r'_+', '_', safe_name)
    
    # Remove leading/trailing underscores
    safe_name = safe_name.strip('_')
    
    # Ensure it starts with a letter or underscore
    if safe_name and not re.match(r'^[a-zA-Z_]', safe_name):
        safe_name = f'circuit_{safe_name}'
    
    # Ensure it's not empty
    if not safe_name:
        safe_name = 'unnamed_circuit'
    
    # Limit length
    if len(safe_name) > 50:
        safe_name = safe_name[:50].rstrip('_')
    
    return safe_name


def validate_file_size(file_path: str, max_size: int = 100 * 1024 * 1024) -> bool:
    """
    Validate file size.
    
    Args:
        file_path: Path to file
        max_size: Maximum allowed size in bytes (default 100MB)
        
    Returns:
        True if file size is valid, False otherwise
    """
    try:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            return size <= max_size
        return False
    except Exception:
        return False


def validate_ip_address(ip: str) -> bool:
    """
    Validate IP address format.
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid IP address, False otherwise
    """
    import ipaddress
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def sanitize_log_input(text: str) -> str:
    """
    Sanitize text for safe logging (prevent log injection).
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove control characters and newlines
    sanitized = re.sub(r'[\r\n\t\x00-\x1f\x7f-\x9f]', ' ', text)
    
    # Limit length
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000] + '...'
    
    return sanitized


def validate_environment_variables() -> List[str]:
    """
    Validate required environment variables.
    
    Returns:
        List of missing environment variables
    """
    required_vars = [
        'SECRET_KEY',
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return missing_vars


def is_safe_filename(filename: str) -> bool:
    """
    Check if filename is safe for file system operations.
    
    Args:
        filename: Filename to check
        
    Returns:
        True if filename is safe, False otherwise
    """
    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    
    # Check for reserved names (Windows)
    reserved_names = [
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    ]
    
    if filename.upper() in reserved_names:
        return False
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        return False
    
    return True