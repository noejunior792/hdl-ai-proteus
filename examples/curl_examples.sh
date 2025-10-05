#!/bin/bash

# HDL AI Proteus - cURL Examples
# Comprehensive examples of using the API with cURL commands

set -e

# Configuration
API_BASE_URL="http://localhost:5000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${1}${2}${NC}"
}

print_header() {
    echo ""
    print_color $PURPLE "============================================"
    print_color $PURPLE "$1"
    print_color $PURPLE "============================================"
}

print_command() {
    print_color $BLUE "Command:"
    echo "$1"
    echo ""
}

# Example Azure OpenAI configuration
AZURE_CONFIG='{
  "provider_type": "azure_openai",
  "api_key": "your-azure-openai-api-key",
  "endpoint": "https://your-resource.openai.azure.com/",
  "api_version": "2024-05-01-preview",
  "model_name": "gpt-4o-mini"
}'

# Example Google Gemini configuration  
GEMINI_CONFIG='{
  "provider_type": "gemini",
  "api_key": "your-gemini-api-key",
  "model_name": "gemini-pro"
}'

# Example OpenAI configuration
OPENAI_CONFIG='{
  "provider_type": "openai",
  "api_key": "your-openai-api-key",
  "model_name": "gpt-4",
  "organization": "your-org-id"
}'

print_header "HDL AI PROTEUS - cURL EXAMPLES"
print_color $GREEN "This file contains comprehensive examples of using the HDL AI Proteus API with cURL"
print_color $YELLOW "⚠️  Replace the API keys and endpoints with your actual credentials before running"

print_header "1. HEALTH CHECK"
print_color $GREEN "Check if the API is running and healthy"

CMD='curl -s http://localhost:5000/health | jq'
print_command "$CMD"

print_header "2. API INFORMATION"
print_color $GREEN "Get comprehensive API information and available features"

CMD='curl -s http://localhost:5000/api/info | jq'
print_command "$CMD"

print_header "3. LIST AVAILABLE PROVIDERS"
print_color $GREEN "Get all available AI providers and their information"

CMD='curl -s http://localhost:5000/api/providers | jq'
print_command "$CMD"

print_header "4. GET PROVIDER CONFIGURATION TEMPLATE"
print_color $GREEN "Get configuration template for Azure OpenAI"

CMD='curl -s http://localhost:5000/api/providers/azure_openai/template | jq'
print_command "$CMD"

print_color $GREEN "Get configuration template for Google Gemini"

CMD='curl -s http://localhost:5000/api/providers/gemini/template | jq'
print_command "$CMD"

print_header "5. TEST PROVIDER CONNECTION"
print_color $GREEN "Test Azure OpenAI connection"

CMD="curl -X POST http://localhost:5000/test-provider \\
     -H \"Content-Type: application/json\" \\
     -d '$AZURE_CONFIG' | jq"
print_command "$CMD"

print_color $GREEN "Test Google Gemini connection"

CMD="curl -X POST http://localhost:5000/test-provider \\
     -H \"Content-Type: application/json\" \\
     -d '$GEMINI_CONFIG' | jq"
print_command "$CMD"

print_header "6. GENERATE HDL PROJECTS"
print_color $GREEN "Generate a 4-bit counter in VHDL"

CMD="curl --fail -X POST http://localhost:5000/generate \\
     -H \"Content-Type: application/json\" \\
     -d '{
       \"prompt\": \"Create a 4-bit counter in VHDL with clock, reset, and enable inputs. The counter should increment on each rising edge of the clock when enable is active. Use IEEE.STD_LOGIC_1164 and IEEE.NUMERIC_STD libraries.\",
       \"circuit_name\": \"counter_4bit\",
       \"provider_config\": $AZURE_CONFIG,
       \"generation_params\": {
         \"temperature\": 0.3,
         \"max_tokens\": 2000
       }
     }' \\
     --output counter_4bit.pdsprj"
print_command "$CMD"

print_color $GREEN "Generate a 2-input AND gate in VHDL"

CMD="curl --fail -X POST http://localhost:5000/generate \\
     -H \"Content-Type: application/json\" \\
     -d '{
       \"prompt\": \"Create a simple 2-input AND gate in VHDL with inputs a and b, and output y. Use IEEE.STD_LOGIC_1164 library.\",
       \"circuit_name\": \"and_gate\",
       \"provider_config\": $AZURE_CONFIG
     }' \\
     --output and_gate.pdsprj"
print_command "$CMD"

print_color $GREEN "Generate an 8-bit ALU in Verilog"

CMD="curl --fail -X POST http://localhost:5000/generate \\
     -H \"Content-Type: application/json\" \\
     -d '{
       \"prompt\": \"Design an 8-bit ALU in Verilog with the following operations: ADD, SUB, AND, OR. Inputs: a[7:0], b[7:0], op[1:0]. Outputs: result[7:0], zero_flag. Operation codes: 00=ADD, 01=SUB, 10=AND, 11=OR.\",
       \"circuit_name\": \"alu_8bit\",
       \"provider_config\": $GEMINI_CONFIG,
       \"generation_params\": {
         \"temperature\": 0.2,
         \"max_tokens\": 3000
       }
     }' \\
     --output alu_8bit.pdsprj"
print_command "$CMD"

print_color $GREEN "Generate a shift register in VHDL"

CMD="curl --fail -X POST http://localhost:5000/generate \\
     -H \"Content-Type: application/json\" \\
     -d '{
       \"prompt\": \"Create an 8-bit shift register in VHDL with parallel load capability. Inputs: clk, reset, load, shift_en, parallel_in[7:0], serial_in. Outputs: parallel_out[7:0], serial_out.\",
       \"circuit_name\": \"shift_register_8bit\",
       \"provider_config\": $OPENAI_CONFIG
     }' \\
     --output shift_register_8bit.pdsprj"
print_command "$CMD"

print_header "7. ADVANCED EXAMPLES WITH RESPONSE HEADERS"
print_color $GREEN "Generate project and view response metadata"

CMD="curl --fail -D headers.txt -X POST http://localhost:5000/generate \\
     -H \"Content-Type: application/json\" \\
     -d '{
       \"prompt\": \"Create a D flip-flop in VHDL with asynchronous reset\",
       \"circuit_name\": \"dff_async_reset\",
       \"provider_config\": $AZURE_CONFIG
     }' \\
     --output dff_async_reset.pdsprj && \\
     echo \"=== Response Headers ===\" && \\
     cat headers.txt && \\
     echo \"=== HDL Language ===\" && \\
     grep \"X-HDL-Language:\" headers.txt && \\
     echo \"=== Provider Used ===\" && \\
     grep \"X-Provider-Used:\" headers.txt && \\
     echo \"=== Compilation Status ===\" && \\
     grep \"X-Compilation-Success:\" headers.txt"
print_command "$CMD"

print_header "8. ERROR HANDLING EXAMPLES"
print_color $RED "These examples show how errors are handled"

print_color $YELLOW "Example: Invalid provider type"
CMD='curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '\''{
       "prompt": "Create an AND gate",
       "circuit_name": "test",
       "provider_config": {
         "provider_type": "invalid_provider"
       }
     }'\'' | jq'
print_command "$CMD"

print_color $YELLOW "Example: Missing required fields"
CMD='curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '\''{
       "prompt": "Create an AND gate",
       "circuit_name": "test",
       "provider_config": {
         "provider_type": "azure_openai",
         "api_key": "some-key"
       }
     }'\'' | jq'
print_command "$CMD"

print_color $YELLOW "Example: Invalid circuit name"
CMD='curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '\''{
       "prompt": "Create an AND gate",
       "circuit_name": "invalid-name!",
       "provider_config": {
         "provider_type": "azure_openai",
         "api_key": "key",
         "endpoint": "https://test.com",
         "api_version": "2024-05-01-preview"
       }
     }'\'' | jq'
print_command "$CMD"

print_header "9. BATCH GENERATION SCRIPT"
print_color $GREEN "Example script to generate multiple circuits"

BATCH_SCRIPT='#!/bin/bash

# Batch generation script
CIRCUITS=(
  "and_gate:Create a 2-input AND gate in VHDL"
  "or_gate:Create a 2-input OR gate in VHDL" 
  "xor_gate:Create a 2-input XOR gate in VHDL"
  "nand_gate:Create a 2-input NAND gate in VHDL"
)

for circuit in "${CIRCUITS[@]}"; do
  IFS=':' read -r name prompt <<< "$circuit"
  echo "Generating $name..."
  
  curl --fail -X POST http://localhost:5000/generate \
       -H "Content-Type: application/json" \
       -d "{
         \"prompt\": \"$prompt\",
         \"circuit_name\": \"$name\",
         \"provider_config\": '$AZURE_CONFIG'
       }" \
       --output "$name.pdsprj" && \
       echo "✅ $name generated successfully" || \
       echo "❌ $name generation failed"
  
  sleep 2  # Rate limiting
done'

print_command "$BATCH_SCRIPT"

print_header "10. TESTING WORKFLOW"
print_color $GREEN "Complete workflow for testing the API"

WORKFLOW='#!/bin/bash

echo "1. Checking API health..."
curl -s http://localhost:5000/health | jq

echo -e "\n2. Getting API info..."
curl -s http://localhost:5000/api/info | jq .name,.version,.supported_providers

echo -e "\n3. Testing provider connection..."
curl -X POST http://localhost:5000/test-provider \
     -H "Content-Type: application/json" \
     -d '\''$AZURE_CONFIG'\'' | jq

echo -e "\n4. Generating test circuit..."
curl --fail -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d '\''{
       "prompt": "Create a simple LED blinker in VHDL",
       "circuit_name": "led_blinker",
       "provider_config": $AZURE_CONFIG
     }'\'' \
     --output led_blinker.pdsprj && \
     echo "✅ Test circuit generated successfully" && \
     file led_blinker.pdsprj'

print_command "$WORKFLOW"

print_header "IMPORTANT NOTES"
print_color $RED "⚠️  ALWAYS use --fail flag with --output to prevent error responses from being saved as files"
print_color $YELLOW "📝 Replace placeholder API keys and endpoints with your actual credentials"
print_color $GREEN "🔍 Use 'jq' for pretty JSON formatting (install with: sudo apt install jq)"
print_color $BLUE "📊 Check response headers for metadata about generation results"
print_color $PURPLE "🔄 Implement rate limiting when making multiple requests"

print_header "CONFIGURATION EXAMPLES"

print_color $GREEN "Save your configuration in environment variables:"
echo 'export AZURE_OPENAI_KEY="your-api-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_VERSION="2024-05-01-preview"
export AZURE_OPENAI_MODEL="gpt-4o-mini"'

echo ""
print_color $GREEN "Then use in requests:"
echo 'curl --fail -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d "{
       \"prompt\": \"Create a counter\",
       \"circuit_name\": \"counter\",
       \"provider_config\": {
         \"provider_type\": \"azure_openai\",
         \"api_key\": \"$AZURE_OPENAI_KEY\",
         \"endpoint\": \"$AZURE_OPENAI_ENDPOINT\",
         \"api_version\": \"$AZURE_OPENAI_VERSION\",
         \"model_name\": \"$AZURE_OPENAI_MODEL\"
       }
     }" \
     --output counter.pdsprj'

echo ""
print_color $BLUE "For more examples and documentation, see:"
print_color $BLUE "- docs/DOCS.md"
print_color $BLUE "- examples/frontend_example.html"
print_color $BLUE "- test_flow.py"