# 🔧 Troubleshooting Guide

This guide helps you diagnose and resolve common issues with HDL AI Proteus.

## 📋 Table of Contents

1. [Quick Diagnostics](#-quick-diagnostics)
2. [Installation Issues](#-installation-issues)
3. [API Connection Problems](#-api-connection-problems)
4. [Provider Authentication Issues](#-provider-authentication-issues)
5. [HDL Generation Failures](#-hdl-generation-failures)
6. [Compilation Errors](#-compilation-errors)
7. [File and Path Issues](#-file-and-path-issues)
8. [Performance Issues](#-performance-issues)
9. [Frontend/Web Interface Issues](#-fronendweb-interface-issues)
10. [Logging and Debug Information](#-logging-and-debug-information)
11. [Frequently Asked Questions](#-frequently-asked-questions)

## 🚀 Quick Diagnostics

### System Health Check

Run this quick diagnostic script to check your setup:

```bash
#!/bin/bash
echo "🔍 HDL AI Proteus Health Check"
echo "================================"

# Check Python
echo -n "Python version: "
python3 --version 2>/dev/null || echo "❌ Python not found"

# Check virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not activated"
fi

# Check dependencies
echo -n "Flask: "
python3 -c "import flask; print(f'✅ {flask.__version__}')" 2>/dev/null || echo "❌ Not installed"

echo -n "Requests: "
python3 -c "import requests; print(f'✅ {requests.__version__}')" 2>/dev/null || echo "❌ Not installed"

# Check HDL compilers
echo -n "GHDL: "
ghdl --version 2>/dev/null | head -1 || echo "❌ Not found"

echo -n "Icarus Verilog: "
iverilog -V 2>/dev/null | head -1 || echo "❌ Not found"

# Check API
echo -n "API Health: "
curl -s http://localhost:5000/health >/dev/null 2>&1 && echo "✅ Running" || echo "❌ Not responding"

# Check directories
for dir in temp export build logs; do
    if [ -d "$dir" ]; then
        echo "✅ Directory $dir exists"
    else
        echo "⚠️  Directory $dir missing"
    fi
done

echo ""
echo "Run with: bash health_check.sh"
```

### Quick API Test

```bash
# Test API endpoints
curl -s http://localhost:5000/health | jq
curl -s http://localhost:5000/api/info | jq
curl -s http://localhost:5000/api/providers | jq
```

## 🛠️ Installation Issues

### Virtual Environment Problems

**Issue: `python3 -m venv` fails**
```bash
# Ubuntu/Debian - install venv module
sudo apt install python3-venv

# Alternative: use virtualenv
pip3 install virtualenv
virtualenv venv
```

**Issue: Virtual environment activation fails**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv

# Linux/macOS activation
source venv/bin/activate

# Windows activation
venv\Scripts\activate

# Verify activation
which python  # Should show venv path
```

**Issue: Permission denied when creating venv**
```bash
# Check permissions
ls -la
chmod +w .

# Use --system-site-packages if needed
python3 -m venv --system-site-packages venv
```

### Dependency Installation Problems

**Issue: `pip install -r requirements.txt` fails**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -v -r requirements.txt

# Clear pip cache if corrupted
pip cache purge
```

**Issue: SSL certificate errors**
```bash
# Upgrade certificates
pip install --upgrade certifi

# Use trusted hosts (temporary fix)
pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
```

**Issue: Compiler/build tools missing**
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# macOS
xcode-select --install

# Windows
# Install Microsoft C++ Build Tools
```

### HDL Compiler Installation

**GHDL Installation Issues:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ghdl

# macOS with Homebrew
brew install ghdl

# From source (if package unavailable)
git clone https://github.com/ghdl/ghdl.git
cd ghdl
./configure --prefix=/usr/local
make
sudo make install
```

**Icarus Verilog Installation Issues:**
```bash
# Ubuntu/Debian
sudo apt install iverilog

# macOS with Homebrew
brew install icarus-verilog

# From source
wget http://iverilog.icarus.com/pub/icarus/iverilog-11.0.tar.gz
tar -xzf iverilog-11.0.tar.gz
cd iverilog-11.0
./configure
make
sudo make install
```

## 🌐 API Connection Problems

### API Won't Start

**Issue: Port already in use**
```bash
# Check what's using port 5000
lsof -i :5000
netstat -tulpn | grep :5000

# Kill existing process
sudo kill -9 <PID>

# Or use different port
export SERVER_PORT=8080
python run.py
```

**Issue: Module import errors**
```bash
# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Ensure you're in project directory
pwd
ls -la src/

# Activate virtual environment
source venv/bin/activate

# Install in development mode
pip install -e .
```

**Issue: Permission denied on directories**
```bash
# Check directory permissions
ls -la temp/ export/ build/ logs/

# Fix permissions
chmod 755 temp export build logs
sudo chown $USER:$USER temp export build logs
```

### API Connection Timeouts

**Issue: Requests timing out**
```bash
# Check if API is actually running
ps aux | grep python
netstat -tulpn | grep 5000

# Test with longer timeout
curl --max-time 30 http://localhost:5000/health

# Check system resources
top
df -h
```

**Issue: API responding slowly**
```bash
# Check system load
uptime
iostat 1 5

# Check disk space
df -h

# Monitor API logs
tail -f logs/hdl_proteus.log
```

## 🔐 Provider Authentication Issues

### Azure OpenAI Problems

**Issue: Authentication failed**
```bash
# Verify credentials format
echo "API Key format: ${AZURE_OPENAI_KEY:0:10}...${AZURE_OPENAI_KEY: -5}"
echo "Endpoint: $AZURE_OPENAI_ENDPOINT"

# Test directly with curl
curl -H "api-key: $AZURE_OPENAI_KEY" \
     "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2024-05-01-preview"
```

**Common Azure OpenAI issues:**
- **Wrong endpoint format**: Must be `https://your-resource.openai.azure.com/`
- **Missing deployment**: Model must be deployed in Azure
- **Wrong API version**: Use `2024-05-01-preview` or newer
- **Regional restrictions**: Check if your region supports the service

**Issue: Model not found**
```bash
# List available deployments
curl -H "api-key: $AZURE_OPENAI_KEY" \
     "$AZURE_OPENAI_ENDPOINT/openai/deployments?api-version=2024-05-01-preview" | jq
```

### OpenAI Problems

**Issue: Invalid API key**
```bash
# Check key format (should start with sk-)
echo "Key format: ${OPENAI_API_KEY:0:5}..."

# Test key directly
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models | jq
```

**Common OpenAI issues:**
- **Wrong key format**: Must start with `sk-`
- **Expired key**: Check if key is still valid
- **Billing issues**: Verify account has credits
- **Rate limits**: Too many requests too quickly

### Google Gemini Problems

**Issue: Authentication failed**
```bash
# Test Gemini API directly
curl -H "x-goog-api-key: $GEMINI_API_KEY" \
     "https://generativelanguage.googleapis.com/v1/models" | jq
```

**Common Gemini issues:**
- **API not enabled**: Enable Generative AI API in Google Cloud Console
- **Wrong model name**: Use `gemini-pro` or `gemini-1.5-pro`
- **Quota exceeded**: Check API quotas in console

### Testing Provider Configuration

**Create a test script:**
```bash
#!/bin/bash
# test_provider.sh

PROVIDER_CONFIG='{
    "provider_type": "azure_openai",
    "api_key": "'$AZURE_OPENAI_KEY'",
    "endpoint": "'$AZURE_OPENAI_ENDPOINT'",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
}'

echo "Testing provider configuration..."
curl -X POST http://localhost:5000/test-provider \
     -H "Content-Type: application/json" \
     -d "{\"provider_config\": $PROVIDER_CONFIG}" | jq

if [ $? -eq 0 ]; then
    echo "✅ Provider test completed"
else
    echo "❌ Provider test failed"
fi
```

## ⚡ HDL Generation Failures

### Generation Timeout

**Issue: Request times out during generation**
```bash
# Increase timeout in curl
curl --max-time 600 -X POST http://localhost:5000/generate ...

# Check server timeout settings
export REQUEST_TIMEOUT=600
python run.py
```

**Issue: Complex prompts failing**
```bash
# Simplify prompt
# Instead of: "Create a complex 32-bit RISC processor with pipeline stages..."
# Try: "Create a simple 4-bit ALU with ADD and SUB operations"

# Break complex designs into smaller parts
# Generate basic components first, then combine
```

### Invalid Response Format

**Issue: Received HTML instead of ZIP file**
```bash
# Check what was actually returned
file *.pdsprj
hexdump -C *.pdsprj | head

# Look for error in response
cat *.pdsprj | grep -i error
```

**Issue: JSON error response saved as .pdsprj**
```bash
# Always use --fail with curl
curl --fail -X POST http://localhost:5000/generate ...

# Check response headers
curl -D headers.txt -X POST http://localhost:5000/generate ...
cat headers.txt
```

### Generation Quality Issues

**Issue: Generated HDL has syntax errors**
```bash
# Use more specific prompts
# Bad: "Create a counter"
# Good: "Create a 4-bit synchronous up counter in VHDL with clock, enable, reset, and 4-bit output"

# Try different models
# gpt-4 usually better than gpt-3.5-turbo for HDL

# Adjust generation parameters
"generation_params": {
    "temperature": 0.2,  # Lower for more deterministic output
    "max_tokens": 2000   # Higher for complex circuits
}
```

**Issue: HDL doesn't meet requirements**
```bash
# Be very specific in prompts
# Include:
# - Input/output signal names and types
# - Clocking requirements (rising/falling edge)
# - Reset behavior (sync/async, active high/low)
# - Specific functionality requirements
```

## 🔨 Compilation Errors

### GHDL Compilation Issues

**Issue: GHDL syntax errors**
```bash
# Check GHDL version
ghdl --version

# Try different VHDL standards
ghdl -a --std=93 file.vhd    # VHDL-93
ghdl -a --std=08 file.vhd    # VHDL-2008

# Enable verbose output
ghdl -a -v file.vhd
```

**Common GHDL errors:**
- **Library issues**: Add `--work=work` parameter
- **Standard mismatch**: Specify correct `--std` version
- **Path issues**: Use absolute paths if needed

### Icarus Verilog Issues

**Issue: Icarus compilation errors**
```bash
# Check iverilog version
iverilog -V

# Try different Verilog standards
iverilog -g2001 file.v      # Verilog-2001
iverilog -g2012 file.v      # SystemVerilog-2012

# Verbose compilation
iverilog -v file.v
```

**Common Icarus errors:**
- **Module not found**: Check module names match filenames
- **Syntax version**: Specify correct `-g` parameter
- **Include paths**: Add `-I` for include directories

### Compilation Environment

**Issue: Compilers not found**
```bash
# Check compiler paths
which ghdl
which iverilog

# Set custom paths if needed
export GHDL_PATH=/usr/local/bin/ghdl
export IVERILOG_PATH=/usr/local/bin/iverilog

# Test with full paths
/usr/local/bin/ghdl --version
/usr/local/bin/iverilog -V
```

## 📁 File and Path Issues

### Directory Problems

**Issue: Permission denied on temp/export directories**
```bash
# Check permissions
ls -la temp/ export/ build/

# Fix ownership
sudo chown -R $USER:$USER temp export build logs

# Fix permissions
chmod -R 755 temp export build logs
```

**Issue: Directories not created**
```bash
# Create manually
mkdir -p temp export build logs

# Check if API creates them
python3 -c "
from src.config.settings import Settings
settings = Settings()
print('Temp dir:', settings.temp_directory)
print('Export dir:', settings.export_directory)
"
```

### File Type Issues

**Issue: Downloaded files are not ZIP archives**
```bash
# Check file type
file *.pdsprj

# Should show: "Zip archive data"
# If not, check for errors in file content
cat *.pdsprj | head -20
```

**Issue: Cannot open .pdsprj in Proteus**
```bash
# Verify it's a valid ZIP
unzip -t *.pdsprj

# Extract and examine contents
unzip -l *.pdsprj
mkdir extracted
cd extracted
unzip ../*.pdsprj
ls -la
```

### Path Resolution Issues

**Issue: Relative path errors**
```bash
# Check current working directory
pwd

# Ensure you're in project root
cd /path/to/hdl-ai-proteus

# Use absolute paths if needed
export TEMP_DIRECTORY=/full/path/to/temp
export EXPORT_DIRECTORY=/full/path/to/export
```

## 🚀 Performance Issues

### Slow Generation Times

**Issue: HDL generation takes too long**
```bash
# Monitor system resources during generation
top -p $(pgrep -f "python.*app.py")

# Check network latency to AI provider
ping api.openai.com
curl -w "@curl-format.txt" -s -o /dev/null https://api.openai.com/v1/models

# Create curl-format.txt:
#     time_namelookup:  %{time_namelookup}\n
#     time_connect:     %{time_connect}\n
#     time_total:       %{time_total}\n
```

**Optimization strategies:**
- Use faster models (gpt-4o-mini vs gpt-4)
- Reduce max_tokens for simple circuits
- Lower temperature for more focused output
- Cache provider connections

### Memory Issues

**Issue: High memory usage**
```bash
# Monitor memory usage
free -h
ps aux | grep python | head -10

# Check for memory leaks
valgrind --tool=memcheck python run.py

# Restart API periodically for long-running instances
```

### Disk Space Issues

**Issue: Running out of disk space**
```bash
# Check disk usage
df -h
du -sh temp/ export/ build/ logs/

# Clean up old files
find temp/ -type f -mtime +7 -delete
find export/ -type f -mtime +30 -delete
find logs/ -type f -mtime +30 -delete

# Rotate logs
logrotate -f /etc/logrotate.conf
```

## 🌐 Frontend/Web Interface Issues

### Browser Compatibility

**Issue: Frontend not working in browser**
```javascript
// Check browser console for errors
// Press F12 -> Console tab

// Common fixes:
// 1. Enable JavaScript
// 2. Disable ad blockers
// 3. Clear browser cache
// 4. Try different browser
```

**Issue: CORS errors**
```bash
# Start API with CORS enabled
export FLASK_CORS_ENABLED=true
python run.py

# Or configure specific origins
export FLASK_CORS_ORIGINS="http://localhost:8000,file://"
```

### File Download Issues

**Issue: Downloads not working**
```javascript
// Check if fetch API is supported
if (!window.fetch) {
    console.error('Fetch API not supported');
}

// Check browser download permissions
// Ensure pop-up blockers don't interfere

// Alternative download method:
function downloadFileAlternative(blob, filename) {
    if (window.navigator.msSaveOrOpenBlob) {
        // IE/Edge
        window.navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        // Modern browsers
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    }
}
```

### Local File Access

**Issue: Cannot open local HTML file**
```bash
# Start local web server instead
python3 -m http.server 8000

# Then visit: http://localhost:8000/examples/frontend_example.html

# Or use Node.js
npx http-server . -p 8000
```

## 📊 Logging and Debug Information

### Enable Debug Logging

```bash
# Set debug level
export LOG_LEVEL=DEBUG
python run.py

# Or in Python code
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### Log File Analysis

```bash
# Watch logs in real-time
tail -f logs/hdl_proteus.log

# Search for errors
grep -i error logs/hdl_proteus.log
grep -i exception logs/hdl_proteus.log

# Show recent entries
tail -100 logs/hdl_proteus.log

# Filter by timestamp
grep "2024-01-15" logs/hdl_proteus.log
```

### API Request Debugging

```bash
# Enable verbose curl output
curl -v -X POST http://localhost:5000/generate ...

# Save response headers
curl -D response_headers.txt -X POST http://localhost:5000/generate ...

# Test with different HTTP methods
curl -X GET http://localhost:5000/health
curl -X POST http://localhost:5000/api/info
```

### Provider Debug Information

```bash
# Test individual providers
python3 -c "
from src.providers.azure_provider import AzureOpenAIProvider
provider = AzureOpenAIProvider({
    'api_key': 'your-key',
    'endpoint': 'your-endpoint',
    'api_version': '2024-05-01-preview'
})
print('Provider info:', provider.get_provider_info())
print('Config valid:', provider.validate_config())
"
```

## ❓ Frequently Asked Questions

### General Questions

**Q: What AI providers are supported?**
A: Currently Azure OpenAI, OpenAI, and Google Gemini. See [CONFIGURATION.md](CONFIGURATION.md) for setup details.

**Q: Can I use this offline?**
A: No, the API requires internet connection to communicate with AI providers.

**Q: What HDL languages are supported?**
A: VHDL and Verilog. Specify the language in your prompt.

**Q: How much does it cost to use?**
A: Costs depend on your AI provider's pricing. The API itself is free.

### Technical Questions

**Q: Why do I get "Provider connection failed"?**
A: Check your API keys, endpoints, and internet connection. Test with the `/test-provider` endpoint first.

**Q: Why is the generated HDL file corrupted?**
A: Always use `curl --fail` to avoid saving error responses as project files.

**Q: Can I generate complex processors?**
A: Start with simple components. Current AI models work best with focused, specific prompts.

**Q: Why does compilation fail?**
A: Generated HDL may need manual review. AI-generated code isn't always syntactically perfect.

### Usage Questions

**Q: How do I improve generation quality?**
A: Use specific, detailed prompts. Include signal names, timing requirements, and behavioral specifications.

**Q: Can I batch generate multiple circuits?**
A: Yes, see the batch processing examples in [EXAMPLES.md](EXAMPLES.md).

**Q: How do I integrate this into my design workflow?**
A: See the Python integration examples and workflow automation patterns.

**Q: Is the generated HDL production-ready?**
A: AI-generated HDL should be reviewed, tested, and validated before production use.

### Error-Specific Questions

**Q: "ModuleNotFoundError: No module named 'src'"**
A: Ensure you're in the project root directory and virtual environment is activated.

**Q: "ConnectionError: HTTPSConnectionPool"**
A: Check internet connection and AI provider service status.

**Q: "FileNotFoundError: [Errno 2] No such file or directory: 'ghdl'"**
A: Install GHDL or set `GHDL_PATH` environment variable.

**Q: "PermissionError: [Errno 13] Permission denied"**
A: Fix directory permissions with `chmod 755` and `chown $USER:$USER`.

## 🆘 Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Run the health check script**
3. **Check the logs**: `tail -f logs/hdl_proteus.log`
4. **Test with simple examples first**
5. **Verify your provider credentials**

### Information to Include

When reporting issues, include:

- **System information**: OS, Python version
- **Error messages**: Complete error output
- **Steps to reproduce**: Exact commands/code used
- **Configuration**: Provider type, model used (remove API keys)
- **Log snippets**: Relevant log entries
- **File information**: Output of `file *.pdsprj`

### Debug Information Script

```bash
#!/bin/bash
# debug_info.sh - Collect debug information

echo "=== HDL AI Proteus Debug Information ==="
echo "Date: $(date)"
echo "System: $(uname -a)"
echo "Python: $(python3 --version)"
echo "Working directory: $(pwd)"
echo ""

echo "=== Environment ==="
env | grep -E "(AZURE|OPENAI|GEMINI|SERVER|LOG)" || echo "No relevant env vars"
echo ""

echo "=== Virtual Environment ==="
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo "Python path: $(which python3)"
echo ""

echo "=== Dependencies ==="
pip list | grep -E "(flask|requests|cors)" || echo "Dependencies not found"
echo ""

echo "=== Directories ==="
ls -la temp/ export/ build/ logs/ 2>/dev/null || echo "Some directories missing"
echo ""

echo "=== Recent Logs ==="
tail -20 logs/hdl_proteus.log 2>/dev/null || echo "No log file found"
echo ""

echo "=== API Status ==="
curl -s http://localhost:5000/health 2>/dev/null || echo "API not responding"
```

### Community Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check [DOCS.md](DOCS.md) for complete API reference
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for usage patterns
- **Configuration**: Review [CONFIGURATION.md](CONFIGURATION.md) for setup help

---

**Remember**: Most issues are configuration-related. Double-check your API keys, endpoints, and environment setup first!