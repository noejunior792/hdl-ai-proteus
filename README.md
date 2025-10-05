# HDL AI Proteus

Generate HDL code from natural language using AI providers (Azure OpenAI, OpenAI, Google Gemini).

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/noejunior792/hdl-ai-proteus.git
cd hdl-ai-proteus
```

### 2. Virtual Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start API
```bash
python run.py
# API runs on http://localhost:5000
```

### 4. Generate HDL
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

## 🤖 Supported Providers

- **Azure OpenAI** (recommended)
- **OpenAI** 
- **Google Gemini**

## 📚 Documentation

**Complete guides available in [docs/](docs/README.md):**

- **[Quick Start Guide](docs/QUICK_START.md)** - Detailed setup with virtual environment
- **[Configuration Guide](docs/CONFIGURATION.md)** - Provider setup and environment variables
- **[Examples Guide](docs/EXAMPLES.md)** - Integration patterns for web, CLI, Python
- **[API Documentation](docs/DOCS.md)** - Complete API reference
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 📁 Project Structure

```
alu-ai-proteus/
├── src/                   # API source code
├── docs/                  # Complete documentation
├── examples/              # Usage examples (HTML, Python, cURL)
├── requirements.txt       # Python dependencies
└── run.py                # Start script
```

## 🔧 Optional: HDL Compilers

For HDL validation (optional):
```bash
# Ubuntu/Debian
sudo apt install ghdl iverilog

# macOS
brew install ghdl icarus-verilog
```

## 🐛 Troubleshooting

- **Virtual environment issues**: Delete `venv` folder and recreate
- **API key errors**: Check [Configuration Guide](docs/CONFIGURATION.md)
- **Generation failures**: See [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- **Debug mode**: `export LOG_LEVEL=DEBUG && python run.py`

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 📞 Support

- **Documentation**: [docs/README.md](docs/README.md)
- **Examples**: [examples/](examples/) directory
- **Issues**: [GitHub Issues](https://github.com/noejunior792/hdl-ai-proteus/issues)

---

**Made with ❤️ for the HDL community**