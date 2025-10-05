# 📚 Examples and Usage Patterns

This guide provides comprehensive examples and usage patterns for integrating HDL AI Proteus into various environments and workflows.

## 📋 Table of Contents

1. [Basic Examples](#-basic-examples)
2. [Frontend Integration](#-frontend-integration)
3. [Command Line Usage](#-command-line-usage)
4. [Python Integration](#-python-integration)
5. [Batch Processing](#-batch-processing)
6. [Advanced Use Cases](#-advanced-use-cases)
7. [Best Practices](#-best-practices)

## 🌟 Basic Examples

### Simple AND Gate (VHDL)
```bash
curl --fail -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a simple 2-input AND gate in VHDL with inputs a, b and output y",
    "circuit_name": "and_gate_2input",
    "provider_config": {
      "provider_type": "azure_openai",
      "api_key": "your-api-key",
      "endpoint": "https://your-resource.openai.azure.com/",
      "api_version": "2024-05-01-preview",
      "model_name": "gpt-4o-mini"
    }
  }' \
  --output and_gate_2input.pdsprj
```

### D Flip-Flop (Verilog)
```bash
curl --fail -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Design a D flip-flop in Verilog with clock, data input, reset, and Q output",
    "circuit_name": "d_flipflop",
    "provider_config": {
      "provider_type": "openai",
      "api_key": "sk-your-openai-key",
      "model_name": "gpt-4"
    }
  }' \
  --output d_flipflop.pdsprj
```

### 4-Bit Counter (VHDL)
```bash
curl --fail -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 4-bit up counter in VHDL with clock, enable, reset, and count output",
    "circuit_name": "counter_4bit",
    "provider_config": {
      "provider_type": "gemini",
      "api_key": "your-gemini-key",
      "model_name": "gemini-pro"
    }
  }' \
  --output counter_4bit.pdsprj
```

## 🌐 Frontend Integration

### HTML Frontend Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HDL AI Proteus - Web Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .config-section, .generation-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
        .form-group { margin: 10px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 3px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
        button:hover { background: #0056b3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .status { padding: 10px; margin: 10px 0; border-radius: 3px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <h1>🔧 HDL AI Proteus</h1>
    <p>Generate HDL code from natural language prompts</p>

    <!-- Provider Configuration Section -->
    <div class="config-section">
        <h2>🤖 AI Provider Configuration</h2>
        
        <div class="form-group">
            <label for="provider">Provider:</label>
            <select id="provider" onchange="updateConfigFields()">
                <option value="azure_openai">Azure OpenAI</option>
                <option value="openai">OpenAI</option>
                <option value="gemini">Google Gemini</option>
            </select>
        </div>

        <div class="form-group">
            <label for="apiKey">API Key:</label>
            <input type="password" id="apiKey" placeholder="Enter your API key">
        </div>

        <div class="form-group" id="endpointGroup">
            <label for="endpoint">Endpoint:</label>
            <input type="text" id="endpoint" placeholder="https://your-resource.openai.azure.com/">
        </div>

        <div class="form-group" id="apiVersionGroup">
            <label for="apiVersion">API Version:</label>
            <input type="text" id="apiVersion" value="2024-05-01-preview">
        </div>

        <div class="form-group">
            <label for="modelName">Model:</label>
            <input type="text" id="modelName" value="gpt-4o-mini">
        </div>

        <button onclick="testProvider()">Test Connection</button>
        <div id="connectionStatus"></div>
    </div>

    <!-- HDL Generation Section -->
    <div class="generation-section">
        <h2>⚡ HDL Generation</h2>
        
        <div class="form-group">
            <label for="prompt">Description:</label>
            <textarea id="prompt" rows="4" placeholder="Describe the circuit you want to generate (e.g., 'Create a 4-bit counter with enable and reset')"></textarea>
        </div>

        <div class="form-group">
            <label for="circuitName">Circuit Name:</label>
            <input type="text" id="circuitName" placeholder="e.g., counter_4bit">
        </div>

        <button onclick="generateHDL()" id="generateBtn">Generate HDL</button>
        <div id="generationStatus"></div>
    </div>

    <script>
        function updateConfigFields() {
            const provider = document.getElementById('provider').value;
            const endpointGroup = document.getElementById('endpointGroup');
            const apiVersionGroup = document.getElementById('apiVersionGroup');
            const modelName = document.getElementById('modelName');

            if (provider === 'azure_openai') {
                endpointGroup.style.display = 'block';
                apiVersionGroup.style.display = 'block';
                modelName.value = 'gpt-4o-mini';
            } else if (provider === 'openai') {
                endpointGroup.style.display = 'none';
                apiVersionGroup.style.display = 'none';
                modelName.value = 'gpt-4';
            } else if (provider === 'gemini') {
                endpointGroup.style.display = 'none';
                apiVersionGroup.style.display = 'none';
                modelName.value = 'gemini-pro';
            }
        }

        function getProviderConfig() {
            const provider = document.getElementById('provider').value;
            const config = {
                provider_type: provider,
                api_key: document.getElementById('apiKey').value,
                model_name: document.getElementById('modelName').value
            };

            if (provider === 'azure_openai') {
                config.endpoint = document.getElementById('endpoint').value;
                config.api_version = document.getElementById('apiVersion').value;
            }

            return config;
        }

        async function testProvider() {
            const status = document.getElementById('connectionStatus');
            status.innerHTML = '<div class="status info">Testing connection...</div>';

            try {
                const response = await fetch('/test-provider', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider_config: getProviderConfig() })
                });

                const result = await response.json();

                if (response.ok) {
                    status.innerHTML = '<div class="status success">✅ Connection successful!</div>';
                } else {
                    status.innerHTML = `<div class="status error">❌ Connection failed: ${result.error}</div>`;
                }
            } catch (error) {
                status.innerHTML = `<div class="status error">❌ Error: ${error.message}</div>`;
            }
        }

        async function generateHDL() {
            const prompt = document.getElementById('prompt').value;
            const circuitName = document.getElementById('circuitName').value;
            const status = document.getElementById('generationStatus');
            const btn = document.getElementById('generateBtn');

            if (!prompt || !circuitName) {
                status.innerHTML = '<div class="status error">Please fill in all fields</div>';
                return;
            }

            btn.disabled = true;
            btn.textContent = 'Generating...';
            status.innerHTML = '<div class="status info">Generating HDL code...</div>';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        prompt: prompt,
                        circuit_name: circuitName,
                        provider_config: getProviderConfig()
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    downloadFile(blob, `${circuitName}.pdsprj`);
                    status.innerHTML = '<div class="status success">✅ HDL generated successfully!</div>';
                } else {
                    const error = await response.json();
                    status.innerHTML = `<div class="status error">❌ Generation failed: ${error.error}</div>`;
                }
            } catch (error) {
                status.innerHTML = `<div class="status error">❌ Error: ${error.message}</div>`;
            } finally {
                btn.disabled = false;
                btn.textContent = 'Generate HDL';
            }
        }

        function downloadFile(blob, filename) {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }

        // Initialize form
        updateConfigFields();
    </script>
</body>
</html>
```

### JavaScript API Client

```javascript
class HDLProteusClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
    }

    async testProvider(providerConfig) {
        const response = await fetch(`${this.baseURL}/test-provider`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ provider_config: providerConfig })
        });
        return await response.json();
    }

    async generateHDL(prompt, circuitName, providerConfig, generationParams = {}) {
        const response = await fetch(`${this.baseURL}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt,
                circuit_name: circuitName,
                provider_config: providerConfig,
                generation_params: generationParams
            })
        });

        if (response.ok) {
            return await response.blob();
        } else {
            const error = await response.json();
            throw new Error(error.error);
        }
    }

    async getProviders() {
        const response = await fetch(`${this.baseURL}/api/providers`);
        return await response.json();
    }

    async getProviderTemplate(providerType) {
        const response = await fetch(`${this.baseURL}/api/providers/${providerType}/template`);
        return await response.json();
    }
}

// Usage example
const client = new HDLProteusClient();

const config = {
    provider_type: 'azure_openai',
    api_key: 'your-key',
    endpoint: 'https://your-resource.openai.azure.com/',
    api_version: '2024-05-01-preview',
    model_name: 'gpt-4o-mini'
};

try {
    const blob = await client.generateHDL(
        'Create a 4-bit counter',
        'counter_4bit',
        config
    );
    // Handle blob download
} catch (error) {
    console.error('Generation failed:', error.message);
}
```

## 🐚 Command Line Usage

### Basic Generation Script

```bash
#!/bin/bash

# HDL Generation Script
# Usage: ./generate.sh "prompt" "circuit_name" [provider]

PROMPT="$1"
CIRCUIT_NAME="$2"
PROVIDER="${3:-azure_openai}"

# API Configuration
API_BASE="http://localhost:5000"

# Provider configurations
case $PROVIDER in
    "azure_openai")
        CONFIG='{
            "provider_type": "azure_openai",
            "api_key": "'$AZURE_OPENAI_KEY'",
            "endpoint": "'$AZURE_OPENAI_ENDPOINT'",
            "api_version": "'${AZURE_OPENAI_VERSION:-2024-05-01-preview}'",
            "model_name": "'${AZURE_OPENAI_MODEL:-gpt-4o-mini}'"
        }'
        ;;
    "openai")
        CONFIG='{
            "provider_type": "openai",
            "api_key": "'$OPENAI_API_KEY'",
            "model_name": "'${OPENAI_MODEL:-gpt-4}'"
        }'
        ;;
    "gemini")
        CONFIG='{
            "provider_type": "gemini",
            "api_key": "'$GEMINI_API_KEY'",
            "model_name": "'${GEMINI_MODEL:-gemini-pro}'"
        }'
        ;;
    *)
        echo "Unknown provider: $PROVIDER"
        exit 1
        ;;
esac

# Validate inputs
if [ -z "$PROMPT" ] || [ -z "$CIRCUIT_NAME" ]; then
    echo "Usage: $0 \"prompt\" \"circuit_name\" [provider]"
    echo "Providers: azure_openai, openai, gemini"
    exit 1
fi

# Test provider connection
echo "Testing provider connection..."
TEST_RESULT=$(curl -s -X POST "$API_BASE/test-provider" \
    -H "Content-Type: application/json" \
    -d "{\"provider_config\": $CONFIG}")

if echo "$TEST_RESULT" | grep -q '"status":"success"'; then
    echo "✅ Provider connection successful"
else
    echo "❌ Provider connection failed:"
    echo "$TEST_RESULT" | jq -r '.error // .message // .'
    exit 1
fi

# Generate HDL
echo "Generating HDL for: $PROMPT"
HTTP_CODE=$(curl --fail -w "%{http_code}" -X POST "$API_BASE/generate" \
    -H "Content-Type: application/json" \
    -d "{
        \"prompt\": \"$PROMPT\",
        \"circuit_name\": \"$CIRCUIT_NAME\",
        \"provider_config\": $CONFIG
    }" \
    --output "$CIRCUIT_NAME.pdsprj" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ HDL generated successfully: $CIRCUIT_NAME.pdsprj"
    echo "📊 HTTP Status: $HTTP_CODE"
    
    # Verify file type
    FILE_TYPE=$(file "$CIRCUIT_NAME.pdsprj")
    if echo "$FILE_TYPE" | grep -q "Zip archive"; then
        echo "✅ File format verified: Valid Proteus project"
    else
        echo "⚠️  Warning: Unexpected file format: $FILE_TYPE"
    fi
else
    echo "❌ HDL generation failed"
    if [ -f "$CIRCUIT_NAME.pdsprj" ]; then
        echo "Error response:"
        cat "$CIRCUIT_NAME.pdsprj"
        rm "$CIRCUIT_NAME.pdsprj"
    fi
    exit 1
fi
```

### Batch Processing Example

```bash
#!/bin/bash

# Batch HDL Generation
# Generate multiple circuits from a list

# Circuit definitions: "name:prompt"
CIRCUITS=(
    "and_gate:Create a 2-input AND gate in VHDL"
    "or_gate:Create a 2-input OR gate in VHDL"
    "xor_gate:Create a 2-input XOR gate in VHDL"
    "nand_gate:Create a 2-input NAND gate in VHDL"
    "nor_gate:Create a 2-input NOR gate in VHDL"
    "not_gate:Create a NOT gate in VHDL"
    "buffer_gate:Create a buffer gate in VHDL"
    "d_flipflop:Create a D flip-flop with reset in Verilog"
    "jk_flipflop:Create a JK flip-flop with reset in Verilog"
    "counter_4bit:Create a 4-bit up counter with enable in VHDL"
)

# Configuration
API_BASE="http://localhost:5000"
PROVIDER_CONFIG='{
    "provider_type": "azure_openai",
    "api_key": "'$AZURE_OPENAI_KEY'",
    "endpoint": "'$AZURE_OPENAI_ENDPOINT'",
    "api_version": "2024-05-01-preview",
    "model_name": "gpt-4o-mini"
}'

# Create output directory
OUTPUT_DIR="generated_circuits_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

echo "🚀 Starting batch HDL generation..."
echo "📁 Output directory: $OUTPUT_DIR"
echo "🔧 Circuits to generate: ${#CIRCUITS[@]}"

# Test provider first
echo "Testing provider connection..."
if ! curl -s -X POST "$API_BASE/test-provider" \
    -H "Content-Type: application/json" \
    -d "{\"provider_config\": $PROVIDER_CONFIG}" | grep -q '"status":"success"'; then
    echo "❌ Provider connection failed"
    exit 1
fi

# Generate circuits
SUCCESS_COUNT=0
FAIL_COUNT=0

for circuit in "${CIRCUITS[@]}"; do
    IFS=':' read -r name prompt <<< "$circuit"
    
    echo "Generating: $name"
    
    if curl --fail -X POST "$API_BASE/generate" \
        -H "Content-Type: application/json" \
        -d "{
            \"prompt\": \"$prompt\",
            \"circuit_name\": \"$name\",
            \"provider_config\": $PROVIDER_CONFIG
        }" \
        --output "$name.pdsprj" 2>/dev/null; then
        
        echo "✅ $name.pdsprj"
        ((SUCCESS_COUNT++))
    else
        echo "❌ Failed: $name"
        [ -f "$name.pdsprj" ] && rm "$name.pdsprj"
        ((FAIL_COUNT++))
    fi
    
    # Rate limiting - wait between requests
    sleep 2
done

echo ""
echo "📊 Batch generation complete!"
echo "✅ Successful: $SUCCESS_COUNT"
echo "❌ Failed: $FAIL_COUNT"
echo "📁 Files in: $PWD"

# List generated files
echo ""
echo "Generated files:"
ls -la *.pdsprj 2>/dev/null || echo "No files generated"
```

## 🐍 Python Integration

### Simple Python Client

```python
import requests
import json
from typing import Dict, Any, Optional

class HDLProteusAPI:
    """Simple Python client for HDL AI Proteus API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
    def test_provider(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Test provider connection"""
        response = self.session.post(
            f"{self.base_url}/test-provider",
            json={"provider_config": provider_config}
        )
        return response.json()
    
    def generate_hdl(self, 
                    prompt: str, 
                    circuit_name: str, 
                    provider_config: Dict[str, Any],
                    generation_params: Optional[Dict[str, Any]] = None) -> bytes:
        """Generate HDL and return project file content"""
        
        data = {
            "prompt": prompt,
            "circuit_name": circuit_name,
            "provider_config": provider_config
        }
        
        if generation_params:
            data["generation_params"] = generation_params
            
        response = self.session.post(
            f"{self.base_url}/generate",
            json=data
        )
        
        if response.status_code == 200:
            return response.content
        else:
            error = response.json()
            raise Exception(f"Generation failed: {error.get('error', 'Unknown error')}")
    
    def get_providers(self) -> Dict[str, Any]:
        """Get list of available providers"""
        response = self.session.get(f"{self.base_url}/api/providers")
        return response.json()
    
    def get_provider_template(self, provider_type: str) -> Dict[str, Any]:
        """Get configuration template for provider"""
        response = self.session.get(f"{self.base_url}/api/providers/{provider_type}/template")
        return response.json()
    
    def save_project(self, content: bytes, filename: str) -> None:
        """Save project content to file"""
        with open(filename, 'wb') as f:
            f.write(content)

# Usage examples
def main():
    # Initialize client
    api = HDLProteusAPI()
    
    # Azure OpenAI configuration
    azure_config = {
        "provider_type": "azure_openai",
        "api_key": "your-azure-key",
        "endpoint": "https://your-resource.openai.azure.com/",
        "api_version": "2024-05-01-preview",
        "model_name": "gpt-4o-mini"
    }
    
    # Test connection
    test_result = api.test_provider(azure_config)
    if test_result.get("status") != "success":
        print(f"Provider test failed: {test_result}")
        return
    
    print("✅ Provider connection successful")
    
    # Generate simple circuits
    circuits = [
        ("and_gate", "Create a 2-input AND gate in VHDL"),
        ("counter_4bit", "Create a 4-bit up counter with enable and reset in VHDL"),
        ("alu_simple", "Create a simple 4-bit ALU with ADD and SUB operations in Verilog")
    ]
    
    for name, prompt in circuits:
        try:
            print(f"Generating {name}...")
            content = api.generate_hdl(prompt, name, azure_config)
            filename = f"{name}.pdsprj"
            api.save_project(content, filename)
            print(f"✅ Saved {filename}")
        except Exception as e:
            print(f"❌ Failed to generate {name}: {e}")

if __name__ == "__main__":
    main()
```

### Advanced Python Client with Error Handling

```python
import requests
import json
import time
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

class HDLProteusAdvancedAPI:
    """Advanced Python client with retry logic and comprehensive error handling"""
    
    def __init__(self, 
                 base_url: str = "http://localhost:5000",
                 timeout: int = 300,
                 max_retries: int = 3,
                 retry_delay: int = 5):
        
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        self.session = requests.Session()
        self.session.timeout = timeout
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                
                if response.status_code < 500:  # Don't retry client errors
                    return response
                    
                if attempt < self.max_retries:
                    self.logger.warning(f"Server error {response.status_code}, retrying in {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries:
                    self.logger.warning(f"Request failed, retrying in {self.retry_delay}s: {e}")
                    time.sleep(self.retry_delay)
                else:
                    raise
        
        return response
    
    def health_check(self) -> bool:
        """Check if API is healthy"""
        try:
            response = self._make_request("GET", "/health")
            return response.status_code == 200
        except Exception:
            return False
    
    def test_provider(self, provider_config: Dict[str, Any]) -> Dict[str, Any]:
        """Test provider connection with validation"""
        # Validate config first
        required_fields = ["provider_type", "api_key"]
        for field in required_fields:
            if field not in provider_config:
                raise ValueError(f"Missing required field: {field}")
        
        response = self._make_request(
            "POST", "/test-provider",
            json={"provider_config": provider_config}
        )
        
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(f"Provider test failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    def generate_hdl(self, 
                    prompt: str, 
                    circuit_name: str, 
                    provider_config: Dict[str, Any],
                    generation_params: Optional[Dict[str, Any]] = None,
                    validate_name: bool = True) -> bytes:
        """Generate HDL with comprehensive validation"""
        
        # Input validation
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        if not circuit_name or not circuit_name.strip():
            raise ValueError("Circuit name cannot be empty")
        
        if validate_name:
            self._validate_circuit_name(circuit_name)
        
        # Test provider connection first
        self.logger.info("Testing provider connection...")
        self.test_provider(provider_config)
        
        # Prepare request data
        data = {
            "prompt": prompt.strip(),
            "circuit_name": circuit_name.strip(),
            "provider_config": provider_config
        }
        
        if generation_params:
            data["generation_params"] = generation_params
        
        # Generate HDL
        self.logger.info(f"Generating HDL for: {circuit_name}")
        response = self._make_request(
            "POST", "/generate",
            json=data
        )
        
        if response.status_code == 200:
            # Verify response is binary (ZIP file)
            content_type = response.headers.get('content-type', '')
            if 'application/zip' not in content_type and 'application/octet-stream' not in content_type:
                raise Exception("Received non-binary response - generation may have failed")
            
            return response.content
        else:
            error = response.json()
            raise Exception(f"Generation failed: {error.get('error', 'Unknown error')}")
    
    def _validate_circuit_name(self, name: str) -> None:
        """Validate circuit name format"""
        import re
        
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            raise ValueError(
                "Circuit name must start with letter or underscore, "
                "and contain only letters, numbers, and underscores"
            )
        
        if len(name) > 100:
            raise ValueError("Circuit name too long (max 100 characters)")
    
    def batch_generate(self, 
                      circuits: List[Dict[str, Any]], 
                      provider_config: Dict[str, Any],
                      output_dir: Optional[str] = None,
                      delay_between_requests: int = 2) -> Dict[str, Any]:
        """Generate multiple circuits in batch"""
        
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        
        results = {
            "successful": [],
            "failed": [],
            "total": len(circuits)
        }
        
        # Test provider once
        self.test_provider(provider_config)
        
        for i, circuit in enumerate(circuits):
            name = circuit["name"]
            prompt = circuit["prompt"]
            generation_params = circuit.get("generation_params")
            
            self.logger.info(f"Generating {i+1}/{len(circuits)}: {name}")
            
            try:
                content = self.generate_hdl(
                    prompt, name, provider_config, 
                    generation_params, validate_name=False
                )
                
                filename = f"{name}.pdsprj"
                if output_dir:
                    filepath = output_path / filename
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    results["successful"].append({"name": name, "file": str(filepath)})
                else:
                    results["successful"].append({"name": name, "content": content})
                
                self.logger.info(f"✅ Generated {name}")
                
            except Exception as e:
                self.logger.error(f"❌ Failed to generate {name}: {e}")
                results["failed"].append({"name": name, "error": str(e)})
            
            # Rate limiting
            if i < len(circuits) - 1:
                time.sleep(delay_between_requests)
        
        return results

# Usage example
def advanced_usage_example():
    """Demonstrate advanced usage patterns"""
    
    # Initialize client
    api = HDLProteusAdvancedAPI(
        base_url="http://localhost:5000",
        timeout=300,
        max_retries=3,
        retry_delay=5
    )
    
    # Check API health
    if not api.health_check():
        print("❌ API is not healthy")
        return
    
    # Configuration
    config = {
        "provider_type": "azure_openai",
        "api_key": "your-key",
        "endpoint": "https://your-resource.openai.azure.com/",
        "api_version": "2024-05-01-preview",
        "model_name": "gpt-4o-mini"
    }
    
    # Batch generation
    circuits = [
        {
            "name": "and_gate_2input",
            "prompt": "Create a 2-input AND gate in VHDL with inputs a, b and output y"
        },
        {
            "name": "counter_4bit_advanced",
            "prompt": "Create a 4-bit up/down counter in VHDL with enable, reset, direction control",
            "generation_params": {
                "temperature": 0.3,
                "max_tokens": 2000
            }
        },
        {
            "name": "alu_8bit",
            "prompt": "Design an 8-bit ALU in Verilog with ADD, SUB, AND, OR, XOR operations"
        }
    ]
    
    # Generate batch
    results = api.batch_generate(
        circuits, 
        config, 
        output_dir="generated_projects",
        delay_between_requests=3
    )
    
    # Print results
    print(f"\n📊 Batch generation complete!")
    print(f"✅ Successful: {len(results['successful'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    for success in results['successful']:
        print(f"  ✅ {success['name']} -> {success['file']}")
    
    for failure in results['failed']:
        print(f"  ❌ {failure['name']}: {failure['error']}")

if __name__ == "__main__":
    advanced_usage_example()
```

## 🚀 Advanced Use Cases

### Custom Circuit Templates

```python
# Circuit template system
CIRCUIT_TEMPLATES = {
    "counter": {
        "base_prompt": "Create a {bits}-bit {direction} counter in {language}",
        "features": {
            "enable": "with enable signal",
            "reset": "with reset signal", 
            "load": "with parallel load",
            "overflow": "with overflow detection"
        },
        "defaults": {
            "bits": 4,
            "direction": "up",
            "language": "VHDL"
        }
    },
    "alu": {
        "base_prompt": "Design a {bits}-bit ALU in {language}",
        "operations": ["ADD", "SUB", "AND", "OR", "XOR", "NOT", "SHL", "SHR"],
        "features": {
            "flags": "with zero and carry flags",
            "overflow": "with overflow detection"
        },
        "defaults": {
            "bits": 8,
            "language": "Verilog"
        }
    }
}

def generate_from_template(template_name: str, **kwargs) -> str:
    """Generate prompt from template"""
    template = CIRCUIT_TEMPLATES[template_name]
    
    # Merge with defaults
    params = {**template["defaults"], **kwargs}
    
    # Build base prompt
    prompt = template["base_prompt"].format(**params)
    
    # Add operations (for ALU)
    if "operations" in template and "operations" in kwargs:
        ops = kwargs["operations"]
        prompt += f" with operations: {', '.join(ops)}"
    
    # Add features
    if "features" in template and "features" in kwargs:
        features = kwargs["features"]
        for feature in features:
            if feature in template["features"]:
                prompt += f" {template['features'][feature]}"
    
    return prompt

# Usage
counter_prompt = generate_from_template(
    "counter",
    bits=8,
    direction="up/down",
    features=["enable", "reset"]
)
# Result: "Create a 8-bit up/down counter in VHDL with enable signal with reset signal"
```

### Integration with Design Workflows

```python
class DesignWorkflow:
    """Integration with design workflow tools"""
    
    def __init__(self, api_client):
        self.api = api_client
        self.project_history = []
    
    def design_and_simulate(self, prompt: str, name: str, config: dict):
        """Complete design and simulation workflow"""
        
        # 1. Generate HDL
        print(f"🔧 Generating {name}...")
        content = self.api.generate_hdl(prompt, name, config)
        
        # 2. Save project
        project_file = f"{name}.pdsprj"
        with open(project_file, 'wb') as f:
            f.write(content)
        
        # 3. Extract and validate HDL (if enabled)
        hdl_files = self.extract_hdl_from_project(project_file)
        
        # 4. Run simulation (if tools available)
        sim_results = self.run_simulation(hdl_files)
        
        # 5. Record in history
        self.project_history.append({
            "name": name,
            "prompt": prompt,
            "project_file": project_file,
            "hdl_files": hdl_files,
            "simulation_results": sim_results,
            "timestamp": time.time()
        })
        
        return {
            "project_file": project_file,
            "hdl_files": hdl_files,
            "simulation_results": sim_results
        }
    
    def extract_hdl_from_project(self, project_file: str) -> List[str]:
        """Extract HDL files from Proteus project"""
        import zipfile
        
        hdl_files = []
        try:
            with zipfile.ZipFile(project_file, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    if file_info.filename.endswith(('.vhd', '.vhdl', '.v')):
                        # Extract HDL file
                        hdl_content = zip_ref.read(file_info)
                        hdl_filename = f"extracted_{file_info.filename}"
                        with open(hdl_filename, 'wb') as f:
                            f.write(hdl_content)
                        hdl_files.append(hdl_filename)
        except Exception as e:
            print(f"⚠️ Could not extract HDL files: {e}")
        
        return hdl_files
    
    def run_simulation(self, hdl_files: List[str]) -> Dict[str, Any]:
        """Run basic HDL simulation"""
        results = {}
        
        for hdl_file in hdl_files:
            try:
                if hdl_file.endswith(('.vhd', '.vhdl')):
                    # VHDL simulation with GHDL
                    result = self.simulate_vhdl(hdl_file)
                elif hdl_file.endswith('.v'):
                    # Verilog simulation with Icarus
                    result = self.simulate_verilog(hdl_file)
                
                results[hdl_file] = result
            except Exception as e:
                results[hdl_file] = {"error": str(e)}
        
        return results
    
    def simulate_vhdl(self, vhdl_file: str) -> Dict[str, Any]:
        """Simulate VHDL with GHDL"""
        import subprocess
        
        try:
            # Analyze
            subprocess.run(['ghdl', '-a', '--std=08', vhdl_file], 
                         check=True, capture_output=True)
            
            # Find entity name (simplified)
            with open(vhdl_file, 'r') as f:
                content = f.read().lower()
                import re
                match = re.search(r'entity\s+(\w+)\s+is', content)
                entity = match.group(1) if match else "unknown"
            
            # Elaborate
            subprocess.run(['ghdl', '-e', '--std=08', entity], 
                         check=True, capture_output=True)
            
            return {"status": "success", "entity": entity}
        
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.stderr.decode()}
    
    def simulate_verilog(self, verilog_file: str) -> Dict[str, Any]:
        """Simulate Verilog with Icarus"""
        import subprocess
        
        try:
            # Compile
            output_file = f"{verilog_file}.out"
            subprocess.run(['iverilog', '-o', output_file, verilog_file], 
                         check=True, capture_output=True)
            
            return {"status": "success", "output": output_file}
        
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.stderr.decode()}
    
    def generate_test_report(self) -> str:
        """Generate HTML test report"""
        html = """
        <html>
        <head><title>HDL Generation Report</title></head>
        <body>
        <h1>HDL Generation Report</h1>
        <table border="1">
        <tr><th>Name</th><th>Status</th><th>Files</th><th>Simulation</th></tr>
        """
        
        for project in self.project_history:
            sim_status = "✅" if any(
                r.get("status") == "success" 
                for r in project["simulation_results"].values()
            ) else "❌"
            
            html += f"""
            <tr>
                <td>{project['name']}</td>
                <td>Generated</td>
                <td>{len(project['hdl_files'])}</td>
                <td>{sim_status}</td>
            </tr>
            """
        
        html += "</table></body></html>"
        
        with open("generation_report.html", "w") as f:
            f.write(html)
        
        return "generation_report.html"

# Usage
workflow = DesignWorkflow(HDLProteusAPI())
result = workflow.design_and_simulate(
    "Create a 4-bit counter with enable",
    "counter_test",
    azure_config
)
report = workflow.generate_test_report()
```

## 📋 Best Practices

### 1. Error Handling
- Always test provider connection before generation
- Use `--fail` flag with cURL to avoid saving error responses
- Implement retry logic for transient failures
- Check file types after download

### 2. Security
- Never hardcode API keys in client-side code
- Use environment variables for sensitive configuration
- Validate all user inputs before sending to API
- Implement rate limiting for batch operations

### 3. Performance
- Cache provider configurations when possible
- Use appropriate timeouts based on prompt complexity
- Implement exponential backoff for retries
- Monitor generation times and optimize prompts

### 4. File Management
- Verify file types after download
- Organize projects in logical directory structures
- Clean up temporary files after processing
- Use meaningful circuit names

### 5. Prompt Engineering
- Be specific about requirements (inputs, outputs, behavior)
- Specify HDL language (VHDL vs Verilog)
- Include timing and reset requirements
- Mention specific features needed

### Example Best Practice Prompt
```
Create a 4-bit synchronous up counter in VHDL with the following specifications:
- Clock input: clk (rising edge triggered)
- Enable input: en (active high)
- Reset input: rst (active high, synchronous)
- Count output: count (4-bit unsigned)
- Behavior: Counter increments on rising clock edge when enabled
- Reset: Counter resets to 0000 when reset is asserted
```

---

For more examples and detailed usage patterns, see the individual example files in the `examples/` directory and the complete API documentation in `DOCS.md`.