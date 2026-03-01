# backend/ai_engine.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load HF token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Set HF_TOKEN in .env: HF_TOKEN=hf_...")

# OpenAI-compatible client pointing to Hugging Face
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

def generate_docstring(function_data: dict) -> str:
    """
    Generate Google-style docstrings using openai/gpt-oss-20b.
    """
    function_name = function_data.get("function_name", "unknown")
    parameters = function_data.get("parameters", [])
    logic = function_data.get("logic", [])
    
    # Context for model (function signature + logic preview)
    param_str = ", ".join(parameters)
    logic_preview = "\n".join(logic[:3]) if logic else "# Basic implementation"
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Python expert. Respond with ONLY a Google Python style docstring.\n\n"
                "Format MUST be:\n"
                "Args:\n"
                "    param (type): description\n"
                "Returns:\n"
                "    type: description\n"
                "Raises:\n"
                "    TypeError: condition\n\n"
                "Include Args, Returns, Raises. Use types like (int | float)."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Docstring for:\n\n"
                f"def {function_name}({param_str}):\n"
                f"{logic_preview}"
            ),
        },
    ]
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # YOUR REQUESTED MODEL
            messages=messages,
            max_tokens=350,
            temperature=0.1,
        )
        
        # Extract clean docstring
        raw = response.choices[0].message.content.strip()
        
        # Remove markdown/outer quotes if present
        if raw.startswith("```"):
            raw = raw.split("```", 2)[-1].strip()
        if raw.startswith('"""'):
            raw = raw[3:]
        if raw.endswith('"""'):
            raw = raw[:-3]
            
        return raw.strip()
        
    except Exception as e:
        print(f"Model error: {e}")
        # Fallback matching Gemini style
        if not parameters:
            parameters = ["param"]
        param_docs = ",\n    ".join(
            [f"{p} (int | float): Input operand" for p in parameters]
        )
        return (
            f"Performs {function_name} operation.\n"
            f"Args:\n"
            f"    {param_docs}\n"
            f"Returns:\n"
            f"    int | float: Result of {function_name} computation.\n"
            f"Raises:\n"
            f"    TypeError: Invalid input types."
        )
