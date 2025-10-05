# 🚀 Quick Start Guide

This guide will get you up and running with HDL AI Proteus in just a few minutes.

## 📋 Prerequisites

- Python 3.8+ installed
- Git installed
- Internet connection for downloading dependencies

## 🛠️ Step 1: Clone and Setup

### 1.1 Clone the Repository
```bash
git clone https://github.com/noejunior792/hdl-ai-proteus.git
cd hdl-ai-proteus
```

### 1.2 Create and Activate Virtual Environment

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

### 1.3 Install Dependencies
```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

## 🔧 Step 2: Install HDL Compilers (Optional)

For HDL validation, install the compilers:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y ghdl iverilog
```

**macOS (with Homebrew):**
```bash
brew install ghdl icarus-verilog
```

**Skip for now:** You can use the API without compilers, but generated HDL won't be validated.

## 🎯 Step 3: Start the API

### 3.1 Start the Server
```bash
# Make sure virtual environment is activated
python run.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 3.2 Test the API
Open a new terminal and test:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "2024-01-XX..."}
```

## 🤖 Step 4: Your First HDL Generation

### 4.1 Prepare Your API Key

Get an API key from one of these providers:
- **Azure OpenAI** (Recommended): https://azure.microsoft.com/en-us/products/ai-services/openai-service
- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://makersuite.google.com/app/apikey

### 4.2 Test Provider Connection
```bash
curl -X POST http://localhost:5000/test-provider \
  -H "Content-Type: application/json" \
  -d '{
    "provider_config": {
      "provider_type": "azure_openai",
      "api_key": "YOUR_API_KEY_HERE",
      "endpoint": "https://your-resource.openai.azure.com/",
      "api_version": "2024-05-01-preview",
      "additional_params": {
        "deployment_name": "gpt-4o-mini"
      }
    }
  }'
```

Expected response:
```json
{"status": "success", "message": "Provider connection successful", ...}
```

### 4.3 Generate Your First Circuit
```bash
curl --fail -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a simple 2-input AND gate in VHDL",
    "circuit_name": "and_gate_simple",
    "provider_config": {
      "provider_type": "azure_openai",
      "api_key": "YOUR_API_KEY_HERE",
      "endpoint": "https://your-resource.openai.azure.com/",
      "api_version": "2024-05-01-preview",
      "additional_params": {
        "deployment_name": "gpt-4o-mini"
      }
    }
  }' \
  --output and_gate_simple.pdsprj
```

If successful, you'll have a `and_gate_simple.pdsprj` file ready for Proteus!

## 🌐 Step 5: Try the Web Interface

### 5.1 Open the Frontend
```bash
# Open in your browser
open examples/frontend_example.html
# or
xdg-open examples/frontend_example.html  # Linux
# or just double-click the file
```

### 5.2 Configure Provider
1. Select your AI provider
2. Enter your API credentials
3. Click "Test Connection"
4. If successful, you're ready to generate!

### 5.3 Generate HDL
1. Enter a prompt like: "Create a 4-bit counter with enable"
2. Set circuit name: "counter_4bit"
3. Click "Generate HDL"
4. Download the `.pdsprj` file when ready

## 🔄 Daily Usage

### Starting Your Development Session
```bash
# Navigate to project
cd hdl-ai-proteus

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Start API server
python run.py
```

### Stopping Your Session
```bash
# Stop API server
Ctrl+C

# Deactivate virtual environment
deactivate
```

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] API server starts without errors
- [ ] Health endpoint responds correctly
- [ ] Provider connection test passes
- [ ] First HDL generation completes
- [ ] Web interface loads and works

## 🚨 Troubleshooting

### Virtual Environment Issues
```bash
# If activation fails, try recreating
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API Connection Issues
```bash
# Check if API is running
curl http://localhost:5000/health

# Check the logs
tail -f logs/hdl_proteus.log
```

### Provider Authentication Issues
- Double-check your API key format
- Verify endpoint URL (Azure only)
- Check your API quota/billing status
- Try a different model name

### Permission Errors
```bash
# Make sure you have write permissions
ls -la
chmod +w .
```

## 📚 Next Steps

1. **Read the examples**: Check `examples/` for more usage patterns
2. **Explore the API**: Read `docs/DOCS.md` for complete API reference
3. **Try complex prompts**: Generate counters, ALUs, state machines
4. **Integrate**: Use the Python client or curl examples in your workflow

## 🎯 Common First Projects

Try generating these to get familiar:

1. **Simple Gates**: "Create a 2-input XOR gate in VHDL"
2. **Flip-Flop**: "Design a D flip-flop with reset in Verilog"  
3. **Counter**: "Make a 4-bit up counter with enable in VHDL"
4. **Decoder**: "Create a 3-to-8 decoder in Verilog"
5. **Multiplexer**: "Design a 4-to-1 mux with select signals in VHDL"

Happy HDL generation! 🎉