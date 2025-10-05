"""
Configuration Management Module

This module handles configuration loading, validation, and management
for the HDL AI Proteus application. It supports multiple configuration
sources including environment variables, JSON files, and direct dictionary input.
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    enabled: bool = False
    type: str = "sqlite"
    host: str = "localhost"
    port: int = 5432
    database: str = "hdl_proteus"
    username: str = ""
    password: str = ""
    connection_pool_size: int = 5


@dataclass
class ServerConfig:
    """Server configuration settings"""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    workers: int = 1
    timeout: int = 300
    max_content_length: int = 16 * 1024 * 1024  # 16MB
    cors_enabled: bool = True
    cors_origins: List[str] = field(default_factory=lambda: ["*"])


@dataclass
class CompilerConfig:
    """HDL compiler configuration"""
    ghdl_path: str = "ghdl"
    iverilog_path: str = "iverilog"
    work_directory: str = "build"
    timeout: int = 60
    additional_flags: Dict[str, List[str]] = field(default_factory=lambda: {
        "vhdl": ["-fsynopsys"],
        "verilog": []
    })


@dataclass
class ExportConfig:
    """Export configuration settings"""
    export_directory: str = "export"
    temp_directory: str = "temp"
    cleanup_temp_files: bool = True
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: List[str] = field(default_factory=lambda: [".vhdl", ".v", ".sv"])


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    file_path: str = "logs/hdl_proteus.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    console_enabled: bool = True


@dataclass
class SecurityConfig:
    """Security configuration"""
    api_key_required: bool = False
    api_key_header: str = "X-API-Key"
    rate_limiting_enabled: bool = False
    rate_limit_per_minute: int = 60
    max_prompt_length: int = 10000
    allowed_ips: List[str] = field(default_factory=list)
    blocked_ips: List[str] = field(default_factory=list)


@dataclass
class AppConfig:
    """Main application configuration"""
    app_name: str = "HDL AI Proteus"
    app_version: str = "1.0.0"
    environment: str = "development"
    secret_key: str = ""
    
    # Sub-configurations
    server: ServerConfig = field(default_factory=ServerConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    compiler: CompilerConfig = field(default_factory=CompilerConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    # Provider-specific settings
    default_provider: str = "azure_openai"
    provider_timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0


class ConfigManager:
    """
    Configuration manager for loading and managing application settings.
    
    Supports loading configuration from:
    - Environment variables
    - JSON configuration files
    - Direct dictionary input
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Optional path to JSON configuration file
        """
        self.config_file = config_file
        self._config: Optional[AppConfig] = None
        
    def load_config(self, config_dict: Optional[Dict[str, Any]] = None) -> AppConfig:
        """
        Load configuration from various sources.
        
        Args:
            config_dict: Optional configuration dictionary to override defaults
            
        Returns:
            Loaded AppConfig instance
        """
        # Start with default configuration
        config_data = {}
        
        # Load from file if specified
        if self.config_file and os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                file_config = json.load(f)
                config_data.update(file_config)
        
        # Load from environment variables
        env_config = self._load_from_environment()
        config_data.update(env_config)
        
        # Override with provided dictionary
        if config_dict:
            config_data = self._merge_configs(config_data, config_dict)
        
        # Create configuration objects
        self._config = self._create_config_from_dict(config_data)
        
        # Validate configuration
        self._validate_config()
        
        return self._config
    
    def get_config(self) -> AppConfig:
        """
        Get the current configuration.
        
        Returns:
            Current AppConfig instance
            
        Raises:
            RuntimeError: If configuration hasn't been loaded
        """
        if self._config is None:
            raise RuntimeError("Configuration not loaded. Call load_config() first.")
        return self._config
    
    def save_config(self, file_path: str) -> None:
        """
        Save current configuration to a JSON file.
        
        Args:
            file_path: Path to save configuration file
            
        Raises:
            RuntimeError: If configuration hasn't been loaded
        """
        if self._config is None:
            raise RuntimeError("No configuration to save. Call load_config() first.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Convert to dictionary and save
        config_dict = asdict(self._config)
        with open(file_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def _load_from_environment(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        env_config = {}
        
        # Server configuration
        server_host = os.getenv('SERVER_HOST')
        if server_host:
            env_config.setdefault('server', {})['host'] = server_host
        server_port = os.getenv('SERVER_PORT')
        if server_port is not None and server_port != '':
            env_config.setdefault('server', {})['port'] = int(server_port)
        server_debug = os.getenv('SERVER_DEBUG')
        if server_debug is not None and server_debug != '':
            env_config.setdefault('server', {})['debug'] = server_debug.lower() == 'true'
        
        # Application configuration
        app_name = os.getenv('APP_NAME')
        if app_name:
            env_config['app_name'] = app_name
        app_version = os.getenv('APP_VERSION')
        if app_version:
            env_config['app_version'] = app_version
        environment = os.getenv('ENVIRONMENT')
        if environment:
            env_config['environment'] = environment
        secret_key = os.getenv('SECRET_KEY')
        if secret_key:
            env_config['secret_key'] = secret_key
        default_provider = os.getenv('DEFAULT_PROVIDER')
        if default_provider:
            env_config['default_provider'] = default_provider
        
        # Compiler configuration
        ghdl_path = os.getenv('GHDL_PATH')
        if ghdl_path:
            env_config.setdefault('compiler', {})['ghdl_path'] = ghdl_path
        iverilog_path = os.getenv('IVERILOG_PATH')
        if iverilog_path:
            env_config.setdefault('compiler', {})['iverilog_path'] = iverilog_path
        
        # Export configuration
        export_directory = os.getenv('EXPORT_DIRECTORY')
        if export_directory:
            env_config.setdefault('export', {})['export_directory'] = export_directory
        temp_directory = os.getenv('TEMP_DIRECTORY')
        if temp_directory:
            env_config.setdefault('export', {})['temp_directory'] = temp_directory
        
        # Logging configuration
        log_level = os.getenv('LOG_LEVEL')
        if log_level:
            env_config.setdefault('logging', {})['level'] = log_level
        log_file_path = os.getenv('LOG_FILE_PATH')
        if log_file_path:
            env_config.setdefault('logging', {})['file_path'] = log_file_path
        
        # Security configuration
        api_key_required = os.getenv('API_KEY_REQUIRED')
        if api_key_required is not None and api_key_required != '':
            env_config.setdefault('security', {})['api_key_required'] = api_key_required.lower() == 'true'
        rate_limiting_enabled = os.getenv('RATE_LIMITING_ENABLED')
        if rate_limiting_enabled is not None and rate_limiting_enabled != '':
            env_config.setdefault('security', {})['rate_limiting_enabled'] = rate_limiting_enabled.lower() == 'true'
        
        return env_config
    
    def _merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge configuration dictionaries."""
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _create_config_from_dict(self, config_data: Dict[str, Any]) -> AppConfig:
        """Create AppConfig object from dictionary."""
        
        # Create sub-configurations
        server_config = ServerConfig(**config_data.get('server', {}))
        database_config = DatabaseConfig(**config_data.get('database', {}))
        compiler_config = CompilerConfig(**config_data.get('compiler', {}))
        export_config = ExportConfig(**config_data.get('export', {}))
        logging_config = LoggingConfig(**config_data.get('logging', {}))
        security_config = SecurityConfig(**config_data.get('security', {}))
        
        # Remove sub-config keys from main config
        main_config = {k: v for k, v in config_data.items() 
                      if k not in ['server', 'database', 'compiler', 'export', 'logging', 'security']}
        
        # Create main configuration
        app_config = AppConfig(
            server=server_config,
            database=database_config,
            compiler=compiler_config,
            export=export_config,
            logging=logging_config,
            security=security_config,
            **main_config
        )
        
        return app_config
    
    def _validate_config(self) -> None:
        """Validate the loaded configuration."""
        if not self._config:
            raise ValueError("No configuration to validate")
        
        # Validate server configuration
        if self._config.server.port < 1 or self._config.server.port > 65535:
            raise ValueError("Server port must be between 1 and 65535")
        
        # Validate directories exist or can be created
        directories = [
            self._config.compiler.work_directory,
            self._config.export.export_directory,
            self._config.export.temp_directory
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                raise ValueError(f"Cannot create directory '{directory}': {e}")
        
        # Validate logging directory
        if self._config.logging.file_enabled:
            log_dir = os.path.dirname(self._config.logging.file_path)
            if log_dir:
                try:
                    os.makedirs(log_dir, exist_ok=True)
                except Exception as e:
                    raise ValueError(f"Cannot create log directory '{log_dir}': {e}")
        
        # Validate provider
        valid_providers = ['azure_openai', 'gemini', 'openai', 'azure', 'google_gemini', 'gpt']
        if self._config.default_provider not in valid_providers:
            raise ValueError(f"Invalid default provider. Must be one of: {valid_providers}")
        
        # Generate secret key if not provided
        if not self._config.secret_key:
            import secrets
            self._config.secret_key = secrets.token_hex(32)


# Global configuration instance
_config_manager = ConfigManager()


def load_config(config_file: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None) -> AppConfig:
    """
    Load application configuration.
    
    Args:
        config_file: Optional path to JSON configuration file
        config_dict: Optional configuration dictionary
        
    Returns:
        Loaded AppConfig instance
    """
    global _config_manager
    if config_file:
        _config_manager = ConfigManager(config_file)
    return _config_manager.load_config(config_dict)


def get_config() -> AppConfig:
    """
    Get the current application configuration.
    
    Returns:
        Current AppConfig instance
    """
    return _config_manager.get_config()


def save_config(file_path: str) -> None:
    """
    Save current configuration to file.
    
    Args:
        file_path: Path to save configuration file
    """
    _config_manager.save_config(file_path)


# Configuration templates for different environments
CONFIG_TEMPLATES = {
    "development": {
        "environment": "development",
        "server": {
            "debug": True,
            "host": "localhost",
            "port": 5000
        },
        "logging": {
            "level": "DEBUG",
            "console_enabled": True
        },
        "security": {
            "api_key_required": False,
            "rate_limiting_enabled": False
        }
    },
    "production": {
        "environment": "production",
        "server": {
            "debug": False,
            "host": "0.0.0.0",
            "port": 8080,
            "workers": 4
        },
        "logging": {
            "level": "INFO",
            "console_enabled": False,
            "file_enabled": True
        },
        "security": {
            "api_key_required": True,
            "rate_limiting_enabled": True,
            "rate_limit_per_minute": 30
        }
    },
    "testing": {
        "environment": "testing",
        "server": {
            "debug": True,
            "host": "localhost",
            "port": 5001
        },
        "logging": {
            "level": "WARNING",
            "console_enabled": True,
            "file_enabled": False
        },
        "security": {
            "api_key_required": False,
            "rate_limiting_enabled": False
        }
    }
}


def create_config_template(environment: str = "development") -> Dict[str, Any]:
    """
    Create a configuration template for a specific environment.
    
    Args:
        environment: Environment name (development, production, testing)
        
    Returns:
        Configuration template dictionary
    """
    if environment not in CONFIG_TEMPLATES:
        raise ValueError(f"Unknown environment: {environment}. Available: {list(CONFIG_TEMPLATES.keys())}")
    
    return CONFIG_TEMPLATES[environment].copy()