# 📝 HDL AI Proteus - Examples

This directory contains comprehensive examples and usage patterns for the HDL AI Proteus API. These examples demonstrate how to integrate the API into various environments and use cases.

## 📁 Files Overview

### 🌐 Frontend Integration
- **`frontend_example.html`** - Complete web interface example
  - Interactive provider configuration
  - Real-time HDL generation
  - File download management
  - Error handling and status display

### 🐚 Command Line Examples
- **`curl_examples.sh`** - Comprehensive cURL command examples
  - API health and info endpoints
  - Provider testing and configuration
  - HDL generation with various parameters
  - Error handling scenarios
  - Batch processing workflows

### 🐍 Python Integration
- **`python_examples.py`** - Complete Python client library
  - `HDLProteusAPI` class for easy integration
  - Error handling and validation
  - Batch generation capabilities
  - File management best practices
  - Advanced features demonstration

## 🚀 Quick Start

### 1. Web Interface
Open `frontend_example.html` in a web browser:
```bash
# Serve locally (optional)
python3 -m http.server 8080
# Then visit: http://localhost:8080/frontend_example.html
```

### 2. cURL Commands
Make the script executable and run:
```bash
chmod +x curl_examples.sh
./curl_examples.sh  # View examples (don't execute)

# Or run individual commands:
curl -s http://localhost:5000/health | jq
```

### 3. Python Client
Install dependencies and run:
```bash
pip install requests
python3 python_examples.py
```

## 🔧 Configuration

### API Credentials
Replace placeholder credentials in examples with your actual API keys:

**Azure OpenAI:**
```json
{
  "provider_type": "azure_openai",
  "api_key": "your-azure-openai-key",
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-05-01-preview",
  "model_name": "gpt-4o-mini"
}
```

**Google Gemini:**
```json
{
  "provider_type": "gemini",
  "api_key": "your-gemini-api-key",
  "model_name": "gemini-pro"
}
```

**OpenAI:**
```json
{
  "provider_type": "openai",
  "api_key": "your-openai-api-key",
  "model_name": "gpt-4"
}
```

### Environment Variables
For security, use environment variables:
```bash
export AZURE_OPENAI_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_VERSION="2024-05-01-preview"
export AZURE_OPENAI_MODEL="gpt-4o-mini"
```

## 📋 Example Use Cases

### Basic HDL Generation
```python
from python_examples import HDLProteusAPI

api = HDLProteusAPI()
result = api.generate_hdl(
    prompt="Create a 4-bit counter in VHDL",
    circuit_name="counter_4bit",
    provider_config=your_config
)
```

### Batch Processing
```bash
# Generate multiple circuits
circuits=("and_gate:Create AND gate" "or_gate:Create OR gate")
for circuit in "${circuits[@]}"; do
    IFS=':' read -r name prompt <<< "$circuit"
    curl --fail -X POST http://localhost:5000/generate \
         -H "Content-Type: application/json" \
         -d "{\"prompt\":\"$prompt\",\"circuit_name\":\"$name\",\"provider_config\":$CONFIG}" \
         --output "$name.pdsprj"
done
```

### Frontend Integration
```javascript
// Test provider connection
const testResult = await fetch('/test-provider', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({provider_config: config})
});

// Generate HDL if test successful
if (testResult.ok) {
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            prompt: userPrompt,
            circuit_name: circuitName,
            provider_config: config
        })
    });
    
    if (response.ok) {
        const blob = await response.blob();
        downloadFile(blob, `${circuitName}.pdsprj`);
    }
}
```

## 🎯 Best Practices

### Error Handling
1. **Always test provider connection first** using `/test-provider`
2. **Use `--fail` flag with cURL** when downloading files
3. **Check HTTP status codes** before processing responses
4. **Handle timeouts** for long-running generations

### Security
1. **Never hardcode API keys** in client-side code
2. **Use environment variables** for sensitive configuration
3. **Validate user inputs** before sending to API
4. **Implement rate limiting** for batch operations

### Performance
1. **Cache provider configurations** when possible
2. **Implement retry logic** for transient failures
3. **Use appropriate timeouts** based on prompt complexity
4. **Monitor generation times** and optimize prompts

### File Management
1. **Verify file types** after download (`file *.pdsprj`)
2. **Organize projects** in logical directory structures
3. **Check file sizes** for reasonableness
4. **Clean up temporary files** after processing

## 🔍 Troubleshooting

### Common Issues

**API Connection Failed:**
```bash
# Check API status
curl -s http://localhost:5000/health

# Verify API is running
python3 ../run.py  # Start API if needed
```

**Provider Authentication Failed:**
```bash
# Test provider separately
curl -X POST http://localhost:5000/test-provider \
     -H "Content-Type: application/json" \
     -d '{"provider_config": YOUR_CONFIG}'
```

**Invalid Circuit Names:**
- Use only alphanumeric characters and underscores
- Start with letter or underscore
- Example: `counter_4bit`, `alu_simple`, `flip_flop_d`

**File Download Issues:**
- Always use `curl --fail` with `--output`
- Check response headers for error status
- Verify file type: `file *.pdsprj` should show "Zip archive"

### Debug Mode
Enable detailed logging in Python:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

api = HDLProteusAPI()
# API calls will now show detailed debug information
```

## 📊 Response Metadata

The API returns rich metadata in response headers:

```bash
# View all headers
curl -D headers.txt http://localhost:5000/generate ...

# Extract specific metadata
grep "X-HDL-Language:" headers.txt
grep "X-Provider-Used:" headers.txt
grep "X-Compilation-Success:" headers.txt
grep "X-Generation-Metadata:" headers.txt
```

## 🔗 Related Documentation

- **[../docs/DOCS.md](../docs/DOCS.md)** - Complete API documentation
- **[../docs/api_context.json](../docs/api_context.json)** - API context for developers
- **[../README.md](../README.md)** - Project overview and setup
- **[../COMMANDS.md](../COMMANDS.md)** - Command reference

## 🤝 Contributing

To add new examples:

1. Follow existing naming conventions
2. Include comprehensive error handling
3. Add configuration examples
4. Document any new patterns or techniques
5. Test with multiple providers when possible

## 📞 Support

If you encounter issues with these examples:

1. Check the main API logs: `../logs/hdl_proteus.log`
2. Verify your provider credentials
3. Test with simple prompts first
4. Review the main documentation

For questions or contributions, see the main project repository.