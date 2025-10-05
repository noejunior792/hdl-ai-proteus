# ⚙️ Configuration Guide

This guide covers all configuration options for HDL AI Proteus, including AI provider setup, environment variables, and advanced configuration.

## 📋 Table of Contents

1. [AI Provider Configuration](#-ai-provider-configuration)
2. [Environment Variables](#-environment-variables)
3. [Configuration Files](#-configuration-files)
4. [Security Best Practices](#-security-best-practices)
5. [Advanced Configuration](#-advanced-configuration)
6. [Troubleshooting](#-troubleshooting)

## 🤖 AI Provider Configuration

### Azure OpenAI

**Required Configuration:**
```json
{
  "provider_type": "azure_openai",
  "api_key": "your-azure-openai-key",
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-05-01-preview",
  "model_name": "gpt-4o-mini"
}
```

**Setup Steps:**
1. Create Azure OpenAI resource in Azure Portal
2. Get API key from "Keys and Endpoint" section
3. Note your endpoint URL (format: `https://[resource-name].openai.azure.com/`)
4. Deploy a model (recommended: `gpt-4o-mini` or `gpt-4`)

**Supported Models:**
- `gpt-4o-mini` (Recommended - cost-effective)
- `gpt-4o`
- `gpt-4`
- `gpt-4-32k`
- `gpt-35-turbo`

**API Versions:**
- `2024-05-01-preview` (Recommended)
- `2024-02-15-preview`
- `2023-12-01-preview`

### OpenAI

**Required Configuration:**
```json
{
  "provider_type": "openai",
  "api_key": "sk-your-openai-api-key",
  "model_name": "gpt-4"
}
```

**Setup Steps:**
1. Create account at https://platform.openai.com/
2. Generate API key in API keys section
3. Add billing method for usage beyond free tier

**Supported Models:**
- `gpt-4` (Recommended)
- `gpt-4-turbo`
- `gpt-3.5-turbo`
- `gpt-3.5-turbo-16k`

### Google Gemini

**Required Configuration:**
```json
{
  "provider_type": "gemini",
  "api_key": "your-gemini-api-key",
  "model_name": "gemini-pro"
}
```

**Setup Steps:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create new API key
4. Note the key for configuration

**Supported Models:**
- `gemini-pro` (Recommended)
- `gemini-pro-vision`
- `gemini-1.5-pro`

## 🌍 Environment Variables

### Server Configuration

```bash
# Server Settings
SERVER_HOST=0.0.0.0          # Server bind address
SERVER_PORT=5000             # Server port
SERVER_DEBUG=false           # Debug mode (true/false)

# Application Settings
DEFAULT_PROVIDER=azure_openai # Default AI provider
LOG_LEVEL=INFO               # Logging level (DEBUG/INFO/WARNING/ERROR)
LOG_FILE_ENABLED=true        # Enable file logging (true/false)

# Directory Configuration
TEMP_DIRECTORY=temp          # Temporary files directory
EXPORT_DIRECTORY=export      # Export directory for projects
BUILD_DIRECTORY=build        # Compilation artifacts directory

# Compiler Configuration
GHDL_PATH=ghdl              # Path to GHDL compiler
IVERILOG_PATH=iverilog      # Path to Icarus Verilog compiler

# Security Settings
MAX_CONTENT_LENGTH=10485760  # Max request size (10MB)
REQUEST_TIMEOUT=300          # Request timeout in seconds
```

### Setting Environment Variables

**Linux/macOS:**
```bash
export SERVER_PORT=8080
export LOG_LEVEL=DEBUG
python run.py
```

**Windows (Command Prompt):**
```cmd
set SERVER_PORT=8080
set LOG_LEVEL=DEBUG
python run.py
```

**Windows (PowerShell):**
```powershell
$env:SERVER_PORT="8080"
$env:LOG_LEVEL="DEBUG"
python run.py
```

### Using .env File

Create a `.env` file in the project root:

```bash
# Copy template
cp env.template .env

# Edit with your settings
nano .env
```

**Example .env:**
```env
# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=5000
SERVER_DEBUG=false

# Default Provider
DEFAULT_PROVIDER=azure_openai

# Logging
LOG_LEVEL=INFO
LOG_FILE_ENABLED=true

# Directories
TEMP_DIRECTORY=temp
EXPORT_DIRECTORY=export
BUILD_DIRECTORY=build

# Azure OpenAI (Optional - can be set per request)
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_VERSION=2024-05-01-preview
AZURE_OPENAI_MODEL=gpt-4o-mini

# OpenAI (Optional)
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4

# Gemini (Optional)
GEMINI_API_KEY=your-gemini-key
GEMINI_MODEL=gemini-pro
```

## 📄 Configuration Files

### JSON Configuration File

Create `config.json` in the project root:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "application": {
    "default_provider": "azure_openai",
    "max_content_length": 10485760,
    "request_timeout": 300
  },
  "logging": {
    "level": "INFO",
    "file_enabled": true,
    "file_path": "logs/hdl_proteus.log",
    "max_file_size": 10485760,
    "backup_count": 5
  },
  "directories": {
    "temp": "temp",
    "export": "export",
    "build": "build"
  },
  "compilers": {
    "ghdl_path": "ghdl",
    "iverilog_path": "iverilog"
  },
  "providers": {
    "azure_openai": {
      "api_key": "",
      "endpoint": "",
      "api_version": "2024-05-01-preview",
      "model_name": "gpt-4o-mini"
    },
    "openai": {
      "api_key": "",
      "model_name": "gpt-4"
    },
    "gemini": {
      "api_key": "",
      "model_name": "gemini-pro"
    }
  }
}
```

### YAML Configuration (Alternative)

Create `config.yaml`:

```yaml
server:
  host: "0.0.0.0"
  port: 5000
  debug: false

application:
  default_provider: "azure_openai"
  max_content_length: 10485760
  request_timeout: 300

logging:
  level: "INFO"
  file_enabled: true
  file_path: "logs/hdl_proteus.log"
  max_file_size: 10485760
  backup_count: 5

directories:
  temp: "temp"
  export: "export" 
  build: "build"

compilers:
  ghdl_path: "ghdl"
  iverilog_path: "iverilog"

providers:
  azure_openai:
    api_key: ""
    endpoint: ""
    api_version: "2024-05-01-preview"
    model_name: "gpt-4o-mini"
  
  openai:
    api_key: ""
    model_name: "gpt-4"
    
  gemini:
    api_key: ""
    model_name: "gemini-pro"
```

## 🔒 Security Best Practices

### API Key Management

**❌ Never do this:**
```javascript
// DON'T hardcode API keys in frontend code
const config = {
  api_key: "sk-your-actual-key-here"  // NEVER!
};
```

**✅ Do this instead:**

**Backend environment variables:**
```bash
export AZURE_OPENAI_KEY="your-key-here"
export OPENAI_API_KEY="sk-your-key-here"
```

**Frontend configuration service:**
```javascript
// Get config from secure backend endpoint
const config = await fetch('/api/config').then(r => r.json());
```

### Environment Variable Security

1. **Use .env files for local development:**
   ```bash
   # .env file (never commit to git)
   AZURE_OPENAI_KEY=your-secret-key
   ```

2. **Use system environment for production:**
   ```bash
   # In production deployment
   export AZURE_OPENAI_KEY="$SECRET_API_KEY"
   ```

3. **Add .env to .gitignore:**
   ```gitignore
   .env
   .env.local
   .env.*.local
   ```

### Request Validation

Configure request limits:
```json
{
  "security": {
    "max_content_length": 10485760,
    "request_timeout": 300,
    "max_prompt_length": 5000,
    "max_circuit_name_length": 100,
    "allowed_file_types": [".pdsprj"],
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 60
    }
  }
}
```

## ⚡ Advanced Configuration

### Custom Provider Templates

Create custom provider configurations:

```json
{
  "custom_azure_config": {
    "provider_type": "azure_openai",
    "endpoint": "https://my-custom-endpoint.openai.azure.com/",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini",
    "generation_params": {
      "temperature": 0.3,
      "max_tokens": 2000,
      "top_p": 0.95
    }
  }
}
```

### Generation Parameters

Fine-tune AI generation:

```json
{
  "generation_params": {
    "temperature": 0.3,        // Creativity (0.0-1.0)
    "max_tokens": 2000,        // Maximum response length
    "top_p": 0.95,            // Nucleus sampling
    "frequency_penalty": 0.0,  // Repetition penalty
    "presence_penalty": 0.0,   // Topic penalty
    "stop": ["\n\n"]          // Stop sequences
  }
}
```

### Compiler Configuration

Configure HDL compilers:

```json
{
  "compilers": {
    "ghdl": {
      "path": "/usr/local/bin/ghdl",
      "version": "3.0.0",
      "args": ["--std=08", "--work=work"],
      "timeout": 30
    },
    "iverilog": {
      "path": "/usr/bin/iverilog",
      "version": "11.0",
      "args": ["-g2012"],
      "timeout": 30
    }
  }
}
```

### Logging Configuration

Advanced logging setup:

```json
{
  "logging": {
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
      "standard": {
        "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
      },
      "detailed": {
        "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
      }
    },
    "handlers": {
      "console": {
        "class": "logging.StreamHandler",
        "level": "INFO",
        "formatter": "standard"
      },
      "file": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "DEBUG",
        "formatter": "detailed",
        "filename": "logs/hdl_proteus.log",
        "maxBytes": 10485760,
        "backupCount": 5
      }
    },
    "loggers": {
      "hdl_proteus": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
        "propagate": false
      }
    }
  }
}
```

## 🔧 Configuration Priority

Configuration is loaded in this order (later overrides earlier):

1. **Default values** (hardcoded in application)
2. **Configuration file** (`config.json` or `config.yaml`)
3. **Environment variables**
4. **Command line arguments**
5. **Request parameters** (for provider config)

Example priority:
```bash
# 1. Default: LOG_LEVEL=INFO
# 2. config.json: "level": "DEBUG"
# 3. Environment: export LOG_LEVEL=WARNING  # This wins
# 4. Command line: python run.py --log-level=ERROR  # This wins
```

## 🚨 Troubleshooting

### Common Configuration Issues

**1. API Key Not Working:**
```bash
# Test your key directly
curl -X POST http://localhost:5000/test-provider \
  -H "Content-Type: application/json" \
  -d '{"provider_config": YOUR_CONFIG}'
```

**2. Environment Variables Not Loading:**
```bash
# Check current environment
env | grep -E "(AZURE|OPENAI|GEMINI)"

# Verify .env file
cat .env
```

**3. Configuration File Not Found:**
```bash
# Check file location and permissions
ls -la config.json
cat config.json | jq  # Validate JSON
```

**4. Compiler Path Issues:**
```bash
# Test compiler availability
which ghdl
which iverilog

# Test with full path
export GHDL_PATH="/usr/local/bin/ghdl"
```

### Debugging Configuration

Enable configuration debugging:
```bash
export LOG_LEVEL=DEBUG
python run.py
```

Check the logs for configuration loading messages:
```bash
tail -f logs/hdl_proteus.log | grep -i config
```

### Configuration Validation

Validate your configuration:
```bash
# Check API info endpoint
curl http://localhost:5000/api/info

# List available providers
curl http://localhost:5000/api/providers

# Get provider template
curl http://localhost:5000/api/providers/azure_openai/template
```

## 📚 Configuration Examples

### Development Setup
```env
SERVER_DEBUG=true
LOG_LEVEL=DEBUG
DEFAULT_PROVIDER=azure_openai
AZURE_OPENAI_KEY=your-dev-key
```

### Production Setup
```env
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
SERVER_DEBUG=false
LOG_LEVEL=WARNING
LOG_FILE_ENABLED=true
DEFAULT_PROVIDER=azure_openai
```

### Multi-Provider Setup
```json
{
  "providers": {
    "primary": {
      "provider_type": "azure_openai",
      "api_key": "key1",
      "endpoint": "https://primary.openai.azure.com/"
    },
    "fallback": {
      "provider_type": "openai", 
      "api_key": "key2"
    },
    "experimental": {
      "provider_type": "gemini",
      "api_key": "key3"
    }
  }
}
```

---

For more configuration options, see the [API Documentation](DOCS.md) and [source code](../src/config/settings.py).