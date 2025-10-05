# 📝 HDL AI Proteus - Examples

This directory contains practical examples for using the HDL AI Proteus API in different environments.

## 📁 Quick Overview

- **`frontend_example.html`** - Complete web interface with provider configuration and HDL generation
- **`curl_examples.sh`** - Command-line examples using cURL for API testing and batch processing  
- **`python_examples.py`** - Python client library with error handling and advanced features

## 🚀 Quick Start

### 1. Start the API
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python run.py
```

### 2. Test with cURL
```bash
# Check API health
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

### 3. Try the Web Interface
Open `frontend_example.html` in your browser or serve it locally:
```bash
python3 -m http.server 8080
# Visit: http://localhost:8080/frontend_example.html
```

### 4. Use Python Client
```bash
python3 python_examples.py
```

## 🔧 Configuration

**Replace placeholder credentials with your actual API keys:**

### Azure OpenAI
```json
{
  "provider_type": "azure_openai",
  "api_key": "your-azure-openai-key",
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-05-01-preview",
  "model_name": "gpt-4o-mini"
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

### Google Gemini
```json
{
  "provider_type": "gemini",
  "api_key": "your-gemini-api-key",
  "model_name": "gemini-pro"
}
```

## 📚 Comprehensive Documentation

For detailed guides, advanced usage patterns, and troubleshooting:

- **[Quick Start Guide](../docs/QUICK_START.md)** - Step-by-step setup with virtual environment
- **[Configuration Guide](../docs/CONFIGURATION.md)** - Provider setup and environment variables
- **[Examples & Usage Patterns](../docs/EXAMPLES.md)** - Comprehensive integration examples
- **[Troubleshooting Guide](../docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Complete API Documentation](../docs/DOCS.md)** - Full API reference

## ⚠️ Important Notes

1. **Always test provider connection first** using `/test-provider` endpoint
2. **Use `--fail` flag with cURL** to avoid saving error responses as `.pdsprj` files  
3. **Never hardcode API keys** in client-side code - use environment variables
4. **Verify downloaded files** with `file *.pdsprj` (should show "Zip archive")

## 🎯 Example Prompts

Try these for your first generations:

- "Create a 2-input AND gate in VHDL with inputs a, b and output y"
- "Design a D flip-flop with reset in Verilog"
- "Create a 4-bit up counter with enable and reset in VHDL"
- "Make a 2-to-1 multiplexer in Verilog with select signal"

## 🆘 Need Help?

- Check the [Troubleshooting Guide](../docs/TROUBLESHOOTING.md) for common issues
- Review [Configuration Guide](../docs/CONFIGURATION.md) for provider setup
- See [Examples Guide](../docs/EXAMPLES.md) for advanced usage patterns
- Test API health: `curl http://localhost:5000/health`

Happy HDL generation! 🎉