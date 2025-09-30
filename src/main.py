import os
import subprocess
import re
from azure_api import generate_code
from compiler import compile_code
from exporter import export_to_pdsprj

import sys

# Create directories if not exist
os.makedirs('generated', exist_ok=True)
os.makedirs('build', exist_ok=True)
os.makedirs('export', exist_ok=True)

# Ask for installing dependencies
choice = input("Do you want to install required dependencies (Python3, pip, GHDL, Icarus Verilog, requests)? (y/n) ")
if choice.lower() == 'y':
    print("Installing dependencies...")
    subprocess.call(['sudo', 'apt', 'update'])
    subprocess.call(['sudo', 'apt', 'upgrade', '-y'])
    subprocess.call(['sudo', 'apt', 'install', '-y', 'python3', 'python3-pip', 'ghdl', 'iverilog'])
    subprocess.call(['pip3', 'install', 'requests'])
    print("Dependencies installed.")

# Get user input
print("Enter the natural language prompt (press Ctrl+D on a new line to end):")
prompt = sys.stdin.read()
name = input("Enter a name for the circuit (no spaces): ")

print(f"Prompt sent: {prompt}")

# Generate code
try:
    content = generate_code(prompt)
    print("Code received from AI.")

    # Extract language and code
    match = re.search(r'```(vhdl|verilog)\n(.*?)\n```', content, re.DOTALL)
    if match:
        lang = match.group(1)
        code = match.group(2)
    else:
        lang = 'vhdl'  # Default to VHDL
        code = content

    if lang == 'vhdl':
        entity_match = re.search(r'entity\s+(\w+)\s+is', code, re.IGNORECASE)
        if entity_match:
            original_entity_name = entity_match.group(1)
            code = code.replace(original_entity_name, name)

    extension = 'vhdl' if lang == 'vhdl' else 'v'
    generated_file = f"generated/{name}.{extension}"

    with open(generated_file, 'w') as f:
        f.write(code)

    print(f"Code saved to {generated_file}")
except Exception as e:
    print(f"Error generating code: {e}")
    exit(1)

# Compile
print("Starting compilation...")
try:
    compile_code(name, extension, 'build')
    print("Compilation successful.")
except Exception as e:
    print(f"Compilation failure: {e}")
    exit(1)

# Export
print("Exporting to .pdsprj...")
try:
    export_to_pdsprj(name, generated_file, 'export', 'build')
    print("Export successful.")
except Exception as e:
    print(f"Export failure: {e}")
    exit(1)