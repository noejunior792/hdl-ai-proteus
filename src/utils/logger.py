"""
Logging Utility Module

This module provides centralized logging configuration and utilities
for the HDL AI Proteus application.
"""

import os
import logging
import logging.handlers
from typing import Dict, Any
from pathlib import Path


def setup_logging(logging_config) -> None:
    """
    Setup application logging based on configuration.
    
    Args:
        logging_config: LoggingConfig object or dictionary containing logging configuration
    """
    # Handle both LoggingConfig object and dictionary
    if hasattr(logging_config, '__dict__'):
        # It's a LoggingConfig dataclass object
        config = logging_config
        log_file_path = config.file_path
        log_level = getattr(logging, config.level.upper())
        log_format = config.format
        console_enabled = config.console_enabled
        file_enabled = config.file_enabled
        max_bytes = config.max_file_size
        backup_count = config.backup_count
    else:
        # It's a dictionary
        log_file_path = logging_config.get('file_path', 'logs/hdl_proteus.log')
        log_level = getattr(logging, logging_config.get('level', 'INFO').upper())
        log_format = logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_enabled = logging_config.get('console_enabled', True)
        file_enabled = logging_config.get('file_enabled', True)
        max_bytes = logging_config.get('max_file_size', 10 * 1024 * 1024)  # 10MB
        backup_count = logging_config.get('backup_count', 5)
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Console handler
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    if file_enabled:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("Logging system initialized")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return logging.getLogger(self.__class__.__name__)


def log_api_request(logger: logging.Logger, request_data: Dict[str, Any]) -> None:
    """
    Log API request information.
    
    Args:
        logger: Logger instance
        request_data: Request data dictionary
    """
    circuit_name = request_data.get('circuit_name', 'unknown')
    provider_type = request_data.get('provider_config', {}).get('provider_type', 'unknown')
    prompt_length = len(request_data.get('prompt', ''))
    
    logger.info(
        f"API Request - Circuit: {circuit_name}, Provider: {provider_type}, "
        f"Prompt Length: {prompt_length} chars"
    )


def log_generation_metrics(logger: logging.Logger, metrics: Dict[str, Any]) -> None:
    """
    Log code generation metrics.
    
    Args:
        logger: Logger instance
        metrics: Metrics dictionary
    """
    logger.info(
        f"Generation Metrics - Language: {metrics.get('language', 'unknown')}, "
        f"Lines: {metrics.get('lines_of_code', 0)}, "
        f"Compilation: {'SUCCESS' if metrics.get('compilation_success', False) else 'FAILED'}, "
        f"Export Time: {metrics.get('export_time', 0):.2f}s"
    )


def log_error_with_context(logger: logging.Logger, error: Exception, context: Dict[str, Any]) -> None:
    """
    Log error with additional context information.
    
    Args:
        logger: Logger instance
        error: Exception that occurred
        context: Additional context information
    """
    logger.error(
        f"Error: {str(error)} | Context: {context}",
        exc_info=True
    )


def configure_third_party_loggers() -> None:
    """Configure logging levels for third-party libraries."""
    # Reduce noise from third-party libraries
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.WARNING)