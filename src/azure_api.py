import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_code(user_prompt):
    endpoint = os.environ.get('AZURE_ENDPOINT')
    api_key = os.environ.get('AZURE_API_KEY')
    api_version = os.environ.get('AZURE_API_VERSION')
    deployment = "gpt-4o"

    if not all([endpoint, api_key, api_version]):
        raise ValueError("Missing Azure OpenAI credentials. Please check your .env file.")

    url = f"{endpoint}openai/deployments/{deployment}/chat/completions?api-version={api_version}"

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a hardware design assistant. Generate VHDL or Verilog code for the given circuit description. When generating VHDL, use the IEEE.NUMERIC_STD.ALL library for arithmetic operations and avoid using the non-standard IEEE.STD_LOGIC_UNSIGNED or IEEE.STD_LOGIC_ARITH libraries."},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
