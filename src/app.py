"""
HDL AI Proteus API Application

This is the main Flask application that provides a REST API for generating
HDL code from natural language prompts using various AI providers.

Features:
- Support for multiple AI providers (Azure OpenAI, Google Gemini, OpenAI)
- Modular and extensible architecture
- Automatic HDL compilation and project export
- Comprehensive error handling and logging
- Configuration management
- API documentation endpoints
"""

import os
import sys
import logging
import tempfile
import shutil
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import traceback

# Add current directory to path for imports  
sys.path.insert(0, os.path.dirname(__file__))

from providers import ProviderFactory, AIProviderConfig
from core.hdl_processor import HDLProcessor
from config.settings import load_config, get_config
from utils.logger import setup_logging
from utils.validators import validate_request_data, sanitize_circuit_name

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables
config = None
hdl_processor = None
logger = None


def initialize_app():
    """Initialize the application with configuration and logging."""
    global config, hdl_processor, logger
    
    # Load configuration into global manager
    config = load_config()
    
    # Setup logging
    setup_logging(config.logging)
    logger = logging.getLogger(__name__)
    
    # Configure Flask app
    app.config['SECRET_KEY'] = config.secret_key
    app.config['MAX_CONTENT_LENGTH'] = config.server.max_content_length
    
    # Enable CORS if configured
    if config.server.cors_enabled:
        CORS(app, origins=config.server.cors_origins)
    
    # Fix relative paths to be absolute from project root
    project_root = os.path.dirname(os.path.dirname(__file__))  # Go up from src/ to project root
    
    # Update paths to be absolute
    if not os.path.isabs(config.export.export_directory):
        config.export.export_directory = os.path.join(project_root, config.export.export_directory)
    if not os.path.isabs(config.export.temp_directory):
        config.export.temp_directory = os.path.join(project_root, config.export.temp_directory)
    if not os.path.isabs(config.compiler.work_directory):
        config.compiler.work_directory = os.path.join(project_root, config.compiler.work_directory)
    
    # Initialize HDL processor
    compiler_config = {
        'ghdl_path': config.compiler.ghdl_path,
        'iverilog_path': config.compiler.iverilog_path,
        'work_directory': config.compiler.work_directory,
        'timeout': config.compiler.timeout,
        'additional_flags': config.compiler.additional_flags
    }
    hdl_processor = HDLProcessor(compiler_config)
    
    # Ensure required directories exist
    os.makedirs(config.export.export_directory, exist_ok=True)
    os.makedirs(config.export.temp_directory, exist_ok=True)
    
    logger.info(f"HDL AI Proteus API initialized - Version {config.app_version}")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API status."""
    try:
        current_config = get_config()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': current_config.app_name,
            'version': current_config.app_version,
            'environment': current_config.environment
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/info', methods=['GET'])
def api_info():
    """API information and documentation endpoint."""
    try:
        current_config = get_config()
        available_providers = ProviderFactory.get_available_providers()
        
        return jsonify({
            'name': current_config.app_name,
            'version': current_config.app_version,
            'description': 'API for generating HDL code from natural language and exporting to Proteus projects',
            'environment': current_config.environment,
            'endpoints': {
                '/health': {
                    'method': 'GET',
                    'description': 'Health check endpoint'
                },
                '/api/info': {
                    'method': 'GET',
                    'description': 'API information and documentation'
                },
                '/api/providers': {
                    'method': 'GET',
                    'description': 'List available AI providers'
                },
                '/api/providers/{provider_type}/template': {
                    'method': 'GET',
                    'description': 'Get configuration template for specific provider'
                },
                '/generate': {
                    'method': 'POST',
                    'description': 'Generate HDL code and return Proteus project file',
                    'required_fields': [
                        'prompt',
                        'circuit_name',
                        'provider_config'
                    ]
                },
                '/test-provider': {
                    'method': 'POST',
                    'description': 'Test AI provider connection'
                }
            },
            'supported_providers': list(available_providers.keys()),
            'supported_languages': ['VHDL', 'Verilog'],
            'max_request_size': current_config.server.max_content_length,
            'default_provider': current_config.default_provider
        }), 200
    except Exception as e:
        logger.error(f"Error getting API info: {str(e)}")
        return jsonify({'error': f'Failed to get API info: {str(e)}'}), 500


@app.route('/api/providers', methods=['GET'])
def list_providers():
    """List all available AI providers with their information."""
    try:
        current_config = get_config()
        providers = ProviderFactory.get_available_providers()
        return jsonify({
            'providers': providers,
            'count': len(providers),
            'default_provider': current_config.default_provider
        }), 200
    except Exception as e:
        logger.error(f"Error listing providers: {str(e)}")
        return jsonify({'error': f'Failed to list providers: {str(e)}'}), 500


@app.route('/api/providers/<provider_type>/template', methods=['GET'])
def get_provider_template(provider_type):
    """Get configuration template for a specific provider."""
    try:
        if not ProviderFactory.is_provider_supported(provider_type):
            return jsonify({
                'error': f'Unsupported provider type: {provider_type}',
                'supported_providers': list(ProviderFactory.get_available_providers().keys())
            }), 400
        
        template = ProviderFactory.get_provider_config_template(provider_type)
        return jsonify(template), 200
        
    except Exception as e:
        logger.error(f"Error getting provider template: {str(e)}")
        return jsonify({'error': f'Failed to get provider template: {str(e)}'}), 500


@app.route('/test-provider', methods=['POST'])
def test_provider():
    """Test AI provider connection without generating code."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate provider configuration
        if 'provider_config' not in data:
            return jsonify({'error': 'provider_config is required'}), 400
        
        provider_config = data['provider_config']
        provider_type = provider_config.get('provider_type')
        
        if not provider_type:
            return jsonify({'error': 'provider_type is required in provider_config'}), 400
        
        # Test provider connection
        result = ProviderFactory.test_provider_connection(provider_type, provider_config)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error testing provider: {str(e)}")
        return jsonify({'error': f'Failed to test provider: {str(e)}'}), 500


@app.route('/generate', methods=['POST'])
def generate_hdl():
    """Main endpoint to generate HDL code and return Proteus project."""
    session_id = str(uuid.uuid4())
    session_dir = None
    
    try:
        # Get and validate request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        validation_result = validate_request_data(data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        current_config = get_config()
        prompt = data['prompt']
        circuit_name = sanitize_circuit_name(data['circuit_name'])
        provider_config_data = data['provider_config']
        provider_type = provider_config_data.get('provider_type', current_config.default_provider)
        
        # Additional parameters
        generation_params = data.get('generation_params', {})
        
        logger.info(f"Processing request for circuit '{circuit_name}' using {provider_type} provider")
        
        # Create session directory
        session_dir = os.path.join(current_config.export.temp_directory, session_id)
        generated_dir = os.path.join(session_dir, 'generated')
        build_dir = os.path.join(session_dir, 'build')
        export_dir = os.path.join(session_dir, 'export')
        
        for directory in [session_dir, generated_dir, build_dir, export_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Test provider connection first
        logger.info(f"Testing provider connection: {provider_type}")
        try:
            connection_test = ProviderFactory.test_provider_connection(provider_type, provider_config_data)
            if not connection_test['success']:
                logger.error(f"Provider connection failed: {connection_test.get('error', 'Unknown error')}")
                return jsonify({
                    'error': f'Provider connection failed: {connection_test.get("error", "Unable to connect to AI provider")}',
                    'provider_type': provider_type,
                    'suggestion': 'Please check your API credentials and endpoint configuration'
                }), 400
        except Exception as e:
            logger.error(f"Provider connection test error: {str(e)}")
            return jsonify({
                'error': f'Provider connection test failed: {str(e)}',
                'provider_type': provider_type,
                'suggestion': 'Please verify your provider configuration'
            }), 400
        
        logger.info(f"Provider connection successful: {provider_type}")
        
        # Create AI provider
        try:
            provider = ProviderFactory.create_provider(provider_type, provider_config_data)
        except Exception as e:
            return jsonify({'error': f'Failed to create AI provider: {str(e)}'}), 400
        
        # Generate HDL code
        try:
            ai_response = provider.generate_code(prompt, **generation_params)
            logger.info(f"AI response received from {provider_type}")
        except Exception as e:
            return jsonify({'error': f'Failed to generate code: {str(e)}'}), 500
        
        # Process HDL code
        try:
            hdl_code = hdl_processor.parse_hdl_code(ai_response.content, circuit_name)
            logger.info(f"HDL code parsed successfully: {hdl_code.language.upper()}")
        except Exception as e:
            return jsonify({'error': f'Failed to parse HDL code: {str(e)}'}), 500
        
        # Compile HDL code
        try:
            compilation_result = hdl_processor.compile_hdl(hdl_code, session_id)
            if not compilation_result.success:
                logger.warning(f"Compilation failed: {compilation_result.error_message}")
                # Continue with export even if compilation fails
        except Exception as e:
            logger.error(f"Compilation error: {str(e)}")
            # Create a failed compilation result
            from core.hdl_processor import CompilationResult
            compilation_result = CompilationResult(
                success=False,
                entity_name=circuit_name,
                language=hdl_code.language,
                build_files=[],
                error_message=str(e)
            )
        
        # Export project
        try:
            export_result = hdl_processor.export_project(
                hdl_code, compilation_result, export_dir, session_id
            )
            
            if not export_result.success:
                return jsonify({'error': f'Failed to export project: {export_result.error_message}'}), 500
                
        except Exception as e:
            return jsonify({'error': f'Failed to export project: {str(e)}'}), 500
        
        # Prepare response metadata
        response_metadata = {
            'circuit_name': circuit_name,
            'hdl_language': hdl_code.language,
            'provider_used': provider_type,
            'model_used': ai_response.model,
            'compilation_success': compilation_result.success,
            'file_size': export_result.file_size,
            'generation_time': {
                'compilation': compilation_result.compilation_time,
                'export': export_result.export_time
            }
        }
        
        # Add compilation warnings/errors to metadata
        if compilation_result.warnings:
            response_metadata['warnings'] = compilation_result.warnings
        if not compilation_result.success:
            response_metadata['compilation_error'] = compilation_result.error_message
        
        # Add HDL metadata
        if hdl_code.metadata:
            response_metadata['code_stats'] = hdl_code.metadata
        
        logger.info(f"Project generated successfully: {circuit_name}.pdsprj ({export_result.file_size} bytes)")
        
        # Return the file with metadata in headers
        response = send_file(
            export_result.file_path,
            as_attachment=True,
            download_name=f"{circuit_name}.pdsprj",
            mimetype='application/octet-stream'
        )
        
        # Add metadata to response headers
        response.headers['X-HDL-Language'] = hdl_code.language
        response.headers['X-Provider-Used'] = provider_type
        response.headers['X-Compilation-Success'] = str(compilation_result.success)
        response.headers['X-Generation-Metadata'] = str(response_metadata)
        
        return response
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_hdl: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'session_id': session_id
        }), 500
        
    finally:
        # Cleanup session directory
        if session_dir and current_config.export.cleanup_temp_files:
            try:
                shutil.rmtree(session_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Failed to cleanup session directory: {str(e)}")


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors."""
    current_config = get_config()
    return jsonify({
        'error': 'Request entity too large',
        'max_size': current_config.server.max_content_length,
        'message': 'The request payload is too large'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            '/health',
            '/api/info',
            '/api/providers',
            '/api/providers/{provider_type}/template',
            '/generate',
            '/test-provider'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.now().isoformat()
    }), 500


def cleanup_on_startup():
    """Clean up temporary files on startup."""
    try:
        current_config = get_config()
        temp_dir = current_config.export.temp_directory
        if os.path.exists(temp_dir):
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    os.remove(item_path)
        logger.info("Temporary files cleaned up")
    except Exception as e:
        logger.warning(f"Failed to cleanup temporary files: {str(e)}")


if __name__ == '__main__':
    try:
        # Initialize the application
        initialize_app()
        
        # Cleanup old files
        cleanup_on_startup()
        
        # Get configuration
        current_config = get_config()
        
        # Run the Flask app
        app.run(
            host=current_config.server.host,
            port=current_config.server.port,
            debug=current_config.server.debug,
            threaded=True
        )
        
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        sys.exit(1)