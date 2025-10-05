# 📝 Examples

Quick examples for using HDL AI Proteus API.

## 📁 Files

- **`frontend_example.html`** - Web interface
- **`curl_examples.sh`** - Command-line examples  
- **`python_examples.py`** - Python client

## 🚀 Quick Start

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start API
python run.py

# 3. Try examples
python3 python_examples.py
# or open frontend_example.html in browser
```

## 🔧 Basic Configuration

Replace `your-api-key` with your actual credentials:

```json
{
  "provider_type": "azure_openai",
  "api_key": "your-azure-openai-key", 
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-05-01-preview",
  "model_name": "gpt-4o-mini"
}
```

## 📚 Documentation

For detailed guides and troubleshooting, see **[docs/](../docs/README.md)**:

- [Quick Start Guide](../docs/QUICK_START.md) - Setup with virtual environment
- [Configuration Guide](../docs/CONFIGURATION.md) - Provider setup  
- [Examples Guide](../docs/EXAMPLES.md) - Comprehensive usage patterns
- [Troubleshooting](../docs/TROUBLESHOOTING.md) - Common issues

## 🎯 Test Generation

```bash
curl --fail -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a 2-input AND gate in VHDL", "circuit_name": "and_gate", "provider_config": YOUR_CONFIG}' \
  --output and_gate.pdsprj
```

**Need help?** Check [troubleshooting guide](../docs/TROUBLESHOOTING.md) or test API health: `curl http://localhost:5000/health`
