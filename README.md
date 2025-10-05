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

### 2. Create and Activate Virtual Environment

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

**Windows:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

### 3. Install Python Dependencies
```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install HDL Compilers (Optional)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y ghdl iverilog
```

**macOS (with Homebrew):**
```bash
brew install ghdl icarus-verilog
```

**Note:** HDL compilers are optional for basic API usage but required for HDL validation.

### 5. Configure Environment (Optional)
```bash
# Copy and edit environment file
cp env.template .env
# Edit .env with your preferred settings
```

## 🎯 Quick Start

### Starting the API Server

**Make sure your virtual environment is activated first:**
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

**Option 1: Using the startup script (Recommended)**
```bash
python run.py
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
python src/app.py
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

For detailed API documentation, see [`docs/DOCS.md`](docs/DOCS.md) and [`docs/api_context.json`](docs/api_context.json).

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

For comprehensive examples and usage patterns, see:

- **[Quick Start Guide](docs/QUICK_START.md)** - Step-by-step setup with virtual environment
- **[Examples & Usage Patterns](docs/EXAMPLES.md)** - Web interface, Python client, batch processing
- **[Configuration Guide](docs/CONFIGURATION.md)** - Provider setup and environment variables
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Basic Usage
```bash
# Test API health
curl http://localhost:5000/health

# Generate simple circuit
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

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# If virtual environment activation fails
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Common Issues

1. **"No module named 'src'"** - Ensure virtual environment is activated and you're in project root
2. **API Key Errors** - Verify API key format and check provider documentation
3. **"ghdl/iverilog: command not found"** - Install HDL compilers or set custom paths
4. **Permission Errors** - Check directory permissions: `chmod 755 temp export build logs`

### Debugging

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python run.py
```

**For comprehensive troubleshooting, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [GHDL](https://github.com/ghdl/ghdl) for VHDL compilation
- [Icarus Verilog](http://iverilog.icarus.com/) for Verilog compilation
- [Flask](https://flask.palletsprojects.com/) for the web framework
- AI providers: Azure OpenAI, Google Gemini, OpenAI

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/noejunior792/hdl-ai-proteus/issues)
- **Documentation**: 
  - [Quick Start Guide](docs/QUICK_START.md) - Virtual environment setup and first steps
  - [Complete API Documentation](docs/DOCS.md) - Full API reference
  - [Configuration Guide](docs/CONFIGURATION.md) - Provider setup
  - [Examples Guide](docs/EXAMPLES.md) - Integration patterns
  - [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues
- **Examples**: See [examples/](examples/) directory for practical usage

---

**Made with ❤️ for the HDL community**