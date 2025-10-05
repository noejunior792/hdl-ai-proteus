# 📖 HDL AI Proteus - Complete Documentation

## 🚀 Overview

HDL AI Proteus is a powerful REST API that generates Hardware Description Language (HDL) code from natural language prompts using AI providers like Azure OpenAI, Google Gemini, and OpenAI. The generated code is automatically compiled, validated, and exported as Proteus project files ready for simulation.

### Key Features
- **Multiple AI Providers**: Azure OpenAI, Google Gemini, OpenAI, and more
- **Dual HDL Support**: VHDL and Verilog code generation
- **Automatic Compilation**: GHDL and Icarus Verilog integration
- **Proteus Export**: Direct .pdsprj file generation
- **Modular Architecture**: Easy to extend with new providers
- **Production Ready**: Docker, logging, error handling, and monitoring

---

## 🏗️ Architecture

### System Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   REST API       │───▶│  AI Providers   │
│   (Web/Mobile)  │    │   (Flask)        │    │  (Azure/Gemini) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  HDL Processor   │
                       │  (GHDL/Icarus)   │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Proteus Exporter │
                       │   (.pdsprj)      │
                       └──────────────────┘
```

### Directory Structure
```
alu-ai-proteus/
├── src/                    # Source code
│   ├── app.py             # Main Flask application
│   ├── config/            # Configuration management
│   ├── core/              # HDL processing logic
│   ├── providers/         # AI provider implementations
│   └── utils/             # Utilities (logging, validation)
├── docs/                  # Documentation
├── examples/              # Usage examples
├── logs/                  # Application logs
├── temp/                  # Temporary files
├── export/                # Generated projects
└── build/                 # Compilation artifacts
```

---

## 🌐 API Reference

### Base URL
```
http://localhost:5000
```

### Authentication
Currently, no API-level authentication is required. AI provider credentials are passed in each request.

### Content Type
All requests must use `Content-Type: application/json`

---

## 📋 Endpoints

### 1. Health Check
**GET** `/health`

Returns API status and basic information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-05T17:30:00.000Z",
  "service": "HDL AI Proteus",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. API Information
**GET** `/api/info`

Returns comprehensive API documentation and available features.

**Response:**
```json
{
  "name": "HDL AI Proteus",
  "version": "1.0.0",
  "description": "API for generating HDL code from natural language and exporting to Proteus projects",
  "environment": "development",
  "endpoints": {
    "/health": { "method": "GET", "description": "Health check endpoint" },
    "/generate": { "method": "POST", "description": "Generate HDL code and return Proteus project file" }
  },
  "supported_providers": ["azure_openai", "azure", "gemini", "google_gemini", "openai", "gpt"],
  "supported_languages": ["VHDL", "Verilog"],
  "max_request_size": 16777216,
  "default_provider": "azure_openai"
}
```

### 3. List Providers
**GET** `/api/providers`

Returns all available AI providers with their information.

**Response:**
```json
{
  "providers": {
    "azure_openai": {
      "name": "Azure OpenAI",
      "description": "Microsoft Azure OpenAI Service",
      "supported_models": ["gpt-4", "gpt-4o", "gpt-4o-mini", "gpt-35-turbo"],
      "required_fields": ["api_key", "endpoint", "api_version"]
    },
    "gemini": {
      "name": "Google Gemini",
      "description": "Google's Gemini AI models",
      "supported_models": ["gemini-pro", "gemini-pro-vision"],
      "required_fields": ["api_key"]
    }
  },
  "count": 6,
  "default_provider": "azure_openai"
}
```

### 4. Provider Configuration Template
**GET** `/api/providers/{provider_type}/template`

Returns the configuration template for a specific provider.

**Parameters:**
- `provider_type`: Provider identifier (e.g., "azure_openai", "gemini")

**Response for Azure OpenAI:**
```json
{
  "provider_type": "azure_openai",
  "description": "Azure OpenAI Service configuration",
  "required_fields": {
    "api_key": "Your Azure OpenAI API key",
    "endpoint": "Your Azure OpenAI endpoint URL",
    "api_version": "API version (e.g., 2024-05-01-preview)"
  },
  "optional_fields": {
    "model_name": "Model to use (default: gpt-4o)",
    "deployment_name": "Custom deployment name"
  },
  "example": {
    "provider_type": "azure_openai",
    "api_key": "your-api-key-here",
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
  }
}
```

### 5. Test Provider Connection
**POST** `/test-provider`

Tests connection to an AI provider without generating code.

**Request Body:**
```json
{
  "provider_config": {
    "provider_type": "azure_openai",
    "api_key": "your-api-key",
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
  }
}
```

**Success Response (200):**
```json
{
  "success": true,
  "provider": "azure_openai",
  "model": "gpt-4o",
  "message": "Connection successful",
  "response_time": 1.234
}
```

**Error Response (400):**
```json
{
  "success": false,
  "provider": "azure_openai",
  "error": "Invalid API key",
  "suggestion": "Please check your API credentials"
}
```

### 6. Generate HDL Code
**POST** `/generate`

Main endpoint that generates HDL code from natural language and returns a Proteus project file.

**Request Body:**
```json
{
  "prompt": "Create a 4-bit counter in VHDL with clock, reset, and enable inputs",
  "circuit_name": "counter_4bit",
  "provider_config": {
    "provider_type": "azure_openai",
    "api_key": "your-api-key",
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
  },
  "generation_params": {
    "temperature": 0.3,
    "max_tokens": 2000
  }
}
```

**Required Fields:**
- `prompt`: Natural language description of the circuit
- `circuit_name`: Name for the generated circuit (alphanumeric, underscores)
- `provider_config`: AI provider configuration object

**Optional Fields:**
- `generation_params`: AI generation parameters (temperature, max_tokens, etc.)

**Success Response (200):**
Returns a binary Proteus project file (.pdsprj) with metadata in headers:

**Response Headers:**
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=counter_4bit.pdsprj
X-HDL-Language: vhdl
X-Provider-Used: azure_openai
X-Compilation-Success: True
X-Generation-Metadata: {...}
```

**Error Response (400):**
```json
{
  "error": "Provider connection failed: Unable to connect to AI provider",
  "provider_type": "azure_openai",
  "suggestion": "Please check your API credentials and endpoint configuration"
}
```

---

## 🛠️ Usage Examples

### cURL Examples

#### Test Provider Connection
```bash
curl -X POST http://localhost:5000/test-provider \
     -H "Content-Type: application/json" \
     -d '{
       "provider_config": {
         "provider_type": "azure_openai",
         "api_key": "your-api-key",
         "endpoint": "https://your-resource.openai.azure.com/",
         "api_version": "2024-05-01-preview",
         "model_name": "gpt-4o-mini"
       }
     }'
```

#### Generate HDL Project
```bash
curl --fail -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "Create a 2-input AND gate in VHDL",
       "circuit_name": "and_gate",
       "provider_config": {
         "provider_type": "azure_openai",
         "api_key": "your-api-key",
         "endpoint": "https://your-resource.openai.azure.com/",
         "api_version": "2024-05-01-preview",
         "model_name": "gpt-4o-mini"
       }
     }' \
     --output and_gate.pdsprj
```

**⚠️ Important:** Always use `--fail` flag with `--output` to prevent error responses from being saved as files.

### Python Examples

#### Basic Request
```python
import requests

def generate_hdl_project(prompt, circuit_name, provider_config):
    url = "http://localhost:5000/generate"
    
    payload = {
        "prompt": prompt,
        "circuit_name": circuit_name,
        "provider_config": provider_config
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        # Save the Proteus project file
        with open(f"{circuit_name}.pdsprj", "wb") as f:
            f.write(response.content)
        
        # Extract metadata from headers
        print(f"HDL Language: {response.headers.get('X-HDL-Language')}")
        print(f"Provider: {response.headers.get('X-Provider-Used')}")
        print(f"Compilation: {response.headers.get('X-Compilation-Success')}")
        
        return True
    else:
        error = response.json()
        print(f"Error: {error.get('error')}")
        return False

# Usage
provider_config = {
    "provider_type": "azure_openai",
    "api_key": "your-api-key",
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
}

generate_hdl_project(
    "Create a flip-flop in VHDL",
    "flipflop_d",
    provider_config
)
```

#### With Error Handling
```python
import requests
from typing import Dict, Any, Optional

class HDLGenerator:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
    
    def test_provider(self, provider_config: Dict[str, Any]) -> bool:
        """Test provider connection before generating code."""
        url = f"{self.base_url}/test-provider"
        
        try:
            response = requests.post(url, json={"provider_config": provider_config})
            result = response.json()
            
            if result.get("success"):
                print(f"✅ Provider connection successful: {result.get('model')}")
                return True
            else:
                print(f"❌ Provider connection failed: {result.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ Connection test error: {e}")
            return False
    
    def generate_project(self, prompt: str, circuit_name: str, 
                        provider_config: Dict[str, Any],
                        generation_params: Optional[Dict[str, Any]] = None) -> bool:
        """Generate HDL project with comprehensive error handling."""
        
        # Test provider first
        if not self.test_provider(provider_config):
            return False
        
        url = f"{self.base_url}/generate"
        payload = {
            "prompt": prompt,
            "circuit_name": circuit_name,
            "provider_config": provider_config
        }
        
        if generation_params:
            payload["generation_params"] = generation_params
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                # Save file
                filename = f"{circuit_name}.pdsprj"
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                # Show metadata
                print(f"✅ Project generated: {filename}")
                print(f"   Language: {response.headers.get('X-HDL-Language', 'unknown')}")
                print(f"   Provider: {response.headers.get('X-Provider-Used', 'unknown')}")
                print(f"   Compiled: {response.headers.get('X-Compilation-Success', 'unknown')}")
                
                return True
            else:
                error = response.json()
                print(f"❌ Generation failed: {error.get('error')}")
                if error.get('suggestion'):
                    print(f"   Suggestion: {error.get('suggestion')}")
                return False
                
        except Exception as e:
            print(f"❌ Request error: {e}")
            return False

# Usage
generator = HDLGenerator()

provider_config = {
    "provider_type": "azure_openai",
    "api_key": "your-api-key",
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
}

generation_params = {
    "temperature": 0.3,
    "max_tokens": 2000
}

generator.generate_project(
    "Create a 8-bit ALU in VHDL with add, subtract, and, or operations",
    "alu_8bit",
    provider_config,
    generation_params
)
```

### JavaScript/Frontend Examples

#### Basic Fetch API
```javascript
async function generateHDL(prompt, circuitName, providerConfig) {
    const url = 'http://localhost:5000/generate';
    
    const payload = {
        prompt: prompt,
        circuit_name: circuitName,
        provider_config: providerConfig
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            // Get metadata from headers
            const hdlLanguage = response.headers.get('X-HDL-Language');
            const provider = response.headers.get('X-Provider-Used');
            const compiled = response.headers.get('X-Compilation-Success');
            
            console.log(`Generated ${hdlLanguage} using ${provider}, compiled: ${compiled}`);
            
            // Download file
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${circuitName}.pdsprj`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            return true;
        } else {
            const error = await response.json();
            console.error('Generation failed:', error.error);
            if (error.suggestion) {
                console.log('Suggestion:', error.suggestion);
            }
            return false;
        }
    } catch (error) {
        console.error('Request failed:', error);
        return false;
    }
}

// Usage
const providerConfig = {
    provider_type: 'azure_openai',
    api_key: 'your-api-key',
    endpoint: 'https://your-resource.openai.azure.com/',
    api_version: '2024-05-01-preview',
    model_name: 'gpt-4o-mini'
};

generateHDL(
    'Create a traffic light controller in VHDL',
    'traffic_controller',
    providerConfig
);
```

---

## 🔧 Configuration

### Environment Variables

The API can be configured using environment variables:

```bash
# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_DEBUG=false

# Application Configuration
APP_NAME="HDL AI Proteus"
APP_VERSION="1.0.0"
ENVIRONMENT=production
SECRET_KEY=your-secret-key
DEFAULT_PROVIDER=azure_openai

# Compiler Configuration
GHDL_PATH=ghdl
IVERILOG_PATH=iverilog

# Directory Configuration
EXPORT_DIRECTORY=export
TEMP_DIRECTORY=temp

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/hdl_proteus.log

# Security Configuration
API_KEY_REQUIRED=false
RATE_LIMITING_ENABLED=false
```

### Provider Configuration

#### Azure OpenAI
```json
{
  "provider_type": "azure_openai",
  "api_key": "your-azure-openai-key",
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-05-01-preview",
  "model_name": "gpt-4o-mini"
}
```

#### Google Gemini
```json
{
  "provider_type": "gemini",
  "api_key": "your-gemini-api-key",
  "model_name": "gemini-pro"
}
```

#### OpenAI
```json
{
  "provider_type": "openai",
  "api_key": "your-openai-api-key",
  "model_name": "gpt-4",
  "organization": "your-org-id"
}
```

---

## 🚨 Error Handling

### Common Error Responses

#### Invalid Provider Configuration
```json
{
  "error": "Missing required field: api_key",
  "provider_type": "azure_openai",
  "required_fields": ["api_key", "endpoint", "api_version"]
}
```

#### Provider Connection Failed
```json
{
  "error": "Provider connection failed: Invalid API key",
  "provider_type": "azure_openai",
  "suggestion": "Please check your API credentials and endpoint configuration"
}
```

#### Invalid Request
```json
{
  "error": "Invalid circuit name. Use only alphanumeric characters and underscores",
  "field": "circuit_name",
  "provided_value": "my-circuit!"
}
```

#### Unsupported Provider
```json
{
  "error": "Unsupported provider type: invalid_provider",
  "supported_providers": ["azure_openai", "azure", "gemini", "google_gemini", "openai", "gpt"]
}
```

---

## 📊 Response Metadata

### Generation Metadata

The API includes rich metadata in response headers and JSON:

```json
{
  "circuit_name": "counter_4bit",
  "hdl_language": "vhdl",
  "provider_used": "azure_openai",
  "model_used": "gpt-4o",
  "compilation_success": true,
  "file_size": 2315,
  "generation_time": {
    "compilation": 0.053,
    "export": 0.003
  },
  "code_stats": {
    "original_entity_name": "Counter_4bit",
    "lines_of_code": 37,
    "has_testbench": false,
    "libraries_used": ["IEEE"],
    "signals_count": 4,
    "processes_count": 2
  }
}
```

---

## 🛡️ Best Practices

### Security
1. **Never hardcode API keys** in client-side code
2. **Use environment variables** for sensitive configuration
3. **Implement rate limiting** in production
4. **Use HTTPS** in production environments
5. **Validate and sanitize** all user inputs

### Performance
1. **Test provider connections** before generating code
2. **Use appropriate timeouts** for AI requests
3. **Implement caching** for repeated requests
4. **Monitor resource usage** and set limits

### Error Handling
1. **Always check HTTP status codes** before processing responses
2. **Use `curl --fail`** when downloading files
3. **Implement retry logic** for transient failures
4. **Log errors** for debugging and monitoring

### Code Generation
1. **Be specific** in prompts for better results
2. **Include target language** (VHDL/Verilog) in prompts
3. **Specify required libraries** and standards
4. **Test generated code** in simulation before production

---

## 🔍 Monitoring and Debugging

### Logs

Application logs are stored in `logs/hdl_proteus.log` and include:
- API requests and responses
- Provider connection attempts
- HDL compilation results
- Error traces and debugging information

### Health Monitoring

Use the `/health` endpoint for monitoring:
```bash
# Basic health check
curl http://localhost:5000/health

# Monitor in scripts
if curl -sf http://localhost:5000/health > /dev/null; then
    echo "API is healthy"
else
    echo "API is down"
fi
```

### Performance Metrics

Response headers include timing information:
- `X-Generation-Metadata`: Detailed performance and statistics
- Response time for AI provider calls
- Compilation and export timing

---

## 🐳 Deployment

### Docker
```bash
# Build image
docker build -t hdl-ai-proteus .

# Run container
docker run -p 5000:5000 \
  -e AZURE_OPENAI_KEY=your-key \
  -e AZURE_OPENAI_ENDPOINT=your-endpoint \
  hdl-ai-proteus
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Production Deployment
See `nginx.conf` and `gunicorn.conf.py` for production configuration examples.

---

## 🤝 Contributing

### Adding New Providers

1. Create provider class in `src/providers/`
2. Implement required methods (`generate_code`, `test_connection`)
3. Register in `ProviderFactory`
4. Add configuration template
5. Update documentation

### Testing

```bash
# Run comprehensive tests
python3 test_flow.py

# Test specific functionality
./test_curl.sh

# Test with make
make test
```

---

## 📞 Support

For issues, questions, or contributions:

1. Check the logs in `logs/hdl_proteus.log`
2. Test provider connectivity with `/test-provider`
3. Review this documentation
4. Check the examples in `examples/`

For more information, see:
- `README.md` - Quick start guide
- `COMMANDS.md` - Command reference
- `examples/` - Usage examples