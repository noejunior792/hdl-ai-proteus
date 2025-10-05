# HDL AI Proteus

HDL AI Proteus is a powerful, modular API that leverages artificial intelligence to generate hardware description language (HDL) code from natural language prompts. It features a flexible architecture supporting multiple AI providers and automatic compilation/export to Proteus-compatible project files.

## 🚀 Features

- **Multiple AI Providers**: Support for Azure OpenAI, Google Gemini, and OpenAI
- **Modular Architecture**: Easy to extend with new AI providers
- **HDL Support**: Generate both VHDL and Verilog code
- **Automatic Compilation**: Uses GHDL and Icarus Verilog for validation
- **Proteus Integration**: Exports ready-to-use `.pdsprj` files
- **RESTful API**: Clean, documented endpoints for easy integration
- **Comprehensive Validation**: Input sanitization and error handling
- **Configurable**: Environment-based configuration management
- **Extensible**: Plugin-style architecture for contributions

## 📋 Requirements

### System Dependencies
- Python 3.8+
- GHDL (for VHDL compilation)
- Icarus Verilog (for Verilog compilation)

### Python Dependencies
- Flask 2.3+
- requests 2.31+
- flask-cors 4.0+
- werkzeug 2.3+
- python-dotenv 1.0+

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/noejunior792/hdl-ai-proteus.git
cd hdl-ai-proteus
```

### 2. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3 python3-pip ghdl iverilog
```

**macOS (with Homebrew):**
```bash
brew install python ghdl icarus-verilog
```

### 3. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

### 4. Configure Environment (Optional)
```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your preferred settings
```

## 🎯 Quick Start

### Starting the API Server

**Option 1: Using the startup script (Recommended)**
```bash
python3 run.py
```

**Option 2: Using Make commands**
```bash
# Quick start (first time)
make quick-start

# Regular start
make run

# Development mode
make run-dev

# Production mode
make run-prod
```

**Option 3: Direct execution**
```bash
python3 src/app.py
```

The API will be available at `http://localhost:5000`

### Basic Usage Example

**Using curl:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 4-bit counter in VHDL with enable and reset signals",
    "circuit_name": "counter_4bit",
    "provider_config": {
      "provider_type": "azure_openai",
      "api_key": "your-azure-api-key",
      "endpoint": "https://your-resource.openai.azure.com/",
      "api_version": "2024-02-15-preview"
    }
  }' \
  --output counter_4bit.pdsprj
```

**Using Python:**
```python
import requests

data = {
    "prompt": "Create a 4-bit counter in VHDL with enable and reset signals",
    "circuit_name": "counter_4bit",
    "provider_config": {
        "provider_type": "azure_openai",
        "api_key": "your-azure-api-key",
        "endpoint": "https://your-resource.openai.azure.com/",
        "api_version": "2024-02-15-preview"
    }
}

response = requests.post("http://localhost:5000/generate", json=data)

if response.status_code == 200:
    with open("counter_4bit.pdsprj", "wb") as f:
        f.write(response.content)
    print("Project generated successfully!")
else:
    print(f"Error: {response.json()}")
```

## 🔌 Supported AI Providers

### Azure OpenAI
```json
{
  "provider_type": "azure_openai",
  "api_key": "your-azure-api-key",
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-02-15-preview",
  "model_name": "gpt-4o"
}
```

### Google Gemini
```json
{
  "provider_type": "gemini",
  "api_key": "your-gemini-api-key",
  "model_name": "gemini-1.5-pro"
}
```

### OpenAI
```json
{
  "provider_type": "openai",
  "api_key": "sk-your-openai-api-key",
  "model_name": "gpt-4"
}
```

## 📚 API Endpoints

### Health Check
```http
GET /health
```

### API Information
```http
GET /api/info
```

### List Providers
```http
GET /api/providers
```

### Provider Configuration Template
```http
GET /api/providers/{provider_type}/template
```

### Test Provider Connection
```http
POST /test-provider
```

### Generate HDL Project
```http
POST /generate
```

For detailed API documentation, see [`docs/api_context.json`](docs/api_context.json).

## 🏗️ Architecture

### Project Structure
```
alu-ai-proteus/
├── src/
│   ├── app.py             # Main Flask application
│   ├── providers/         # AI provider implementations
│   │   ├── __init__.py
│   │   ├── base_provider.py      # Abstract base class
│   │   ├── azure_provider.py     # Azure OpenAI implementation
│   │   ├── gemini_provider.py    # Google Gemini implementation
│   │   ├── openai_provider.py    # OpenAI implementation
│   │   └── provider_factory.py   # Provider factory
│   ├── core/              # Core processing logic
│   │   └── hdl_processor.py      # HDL parsing, compilation, export
│   ├── config/            # Configuration management
│   │   └── settings.py           # Settings and config loading
│   └── utils/             # Utility modules
│       ├── __init__.py
│       ├── logger.py             # Logging utilities
│       └── validators.py         # Input validation
├── docs/                  # Documentation
│   ├── api_context.json   # Complete API documentation for frontend
│   └── DOCS.md           # Comprehensive documentation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── nginx.conf           # Nginx configuration for production
├── env.template         # Environment variables template
├── build/               # Compilation artifacts (auto-generated)
├── export/              # Exported projects (auto-generated)
├── temp/                # Temporary files (auto-generated)
└── logs/                # Log files (auto-generated)
```

### Key Components

1. **Provider System**: Modular AI provider architecture
2. **HDL Processor**: Handles parsing, compilation, and export
3. **Configuration Manager**: Environment-based configuration
4. **Validation Layer**: Input sanitization and validation
5. **Logging System**: Comprehensive logging with rotation

## 🔧 Configuration

### Environment Variables
```bash
# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_DEBUG=false

# Application Configuration
DEFAULT_PROVIDER=azure_openai
LOG_LEVEL=INFO

# Directories
TEMP_DIRECTORY=temp
EXPORT_DIRECTORY=export

# Compiler Paths (if not in PATH)
GHDL_PATH=ghdl
IVERILOG_PATH=iverilog
```

### Configuration File
You can also use a JSON configuration file:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "default_provider": "azure_openai",
  "logging": {
    "level": "INFO",
    "file_enabled": true
  }
}
```

## 🤝 Contributing

### Adding New AI Providers

1. **Create Provider Class**: Inherit from `BaseAIProvider`
```python
from src.providers.base_provider import BaseAIProvider, AIProviderConfig, AIResponse

class MyAIProvider(BaseAIProvider):
    def generate_code(self, prompt: str, **kwargs) -> AIResponse:
        # Implementation here
        pass
    
    def validate_config(self) -> bool:
        # Validation logic here
        pass
    
    def get_provider_info(self) -> Dict[str, Any]:
        # Provider information
        pass
```

2. **Register Provider**: Add to `provider_factory.py`
```python
from .my_ai_provider import MyAIProvider

class ProviderFactory:
    _providers = {
        # ... existing providers
        'my_ai': MyAIProvider,
    }
```

3. **Update Documentation**: Add provider info to `api_context.json`

### Development Setup

1. **Install in Development Mode**
```bash
pip install -e .
```

2. **Run Tests** (when available)
```bash
python -m pytest tests/
```

3. **Code Style**
- Follow PEP 8
- Use type hints
- Document all public methods
- Add logging for important operations

## 📖 Examples

### VHDL Counter Example
```json
{
  "prompt": "Create a 4-bit up/down counter in VHDL with enable, reset, and direction control signals. Include clock input and count output.",
  "circuit_name": "updown_counter_4bit",
  "provider_config": {
    "provider_type": "azure_openai",
    "api_key": "your-api-key",
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-02-15-preview"
  },
  "generation_params": {
    "temperature": 0.3,
    "max_tokens": 1500
  }
}
```

### Verilog ALU Example
```json
{
  "prompt": "Design a 8-bit ALU in Verilog with operations: ADD, SUB, AND, OR, XOR, NOT, SHL, SHR. Include operation select input and zero flag output.",
  "circuit_name": "alu_8bit",
  "provider_config": {
    "provider_type": "gemini",
    "api_key": "your-gemini-api-key",
    "model_name": "gemini-1.5-pro"
  }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **"ghdl: command not found"**
   - Install GHDL: `sudo apt install ghdl`
   - Or set custom path: `GHDL_PATH=/path/to/ghdl`

2. **"iverilog: command not found"**
   - Install Icarus Verilog: `sudo apt install iverilog`
   - Or set custom path: `IVERILOG_PATH=/path/to/iverilog`

3. **API Key Errors**
   - Verify API key format for your provider
   - Check endpoint URL format
   - Ensure API quota is not exceeded

4. **Compilation Errors**
   - Check generated HDL syntax
   - Verify compiler versions
   - Review error logs for details

### Debugging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python3 src/app.py
```

Check logs directory for detailed error information.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [GHDL](https://github.com/ghdl/ghdl) for VHDL compilation
- [Icarus Verilog](http://iverilog.icarus.com/) for Verilog compilation
- [Flask](https://flask.palletsprojects.com/) for the web framework
- AI providers: Azure OpenAI, Google Gemini, OpenAI

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/noejunior792/hdl-ai-proteus/issues)
- **Documentation**: [`docs/api_context.json`](docs/api_context.json) and [`docs/DOCS.md`](docs/DOCS.md)
- **Examples**: See usage examples in documentation

---

**Made with ❤️ for the HDL community**