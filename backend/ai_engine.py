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

# def generate_docstring(function_data: dict) -> str:
def generate_docstring(function_data: dict, style: str, language: str):
    # """
    # Generate Google-style docstrings using openai/gpt-oss-20b.
    # """
    style_prompt = {
    "google": "Google Python style docstring",
    "numpy": "NumPy style docstring",
    "jsdoc": "JSDoc comment style",
    "java": "JavaDoc style"
    }.get(style, "Google style")
    
    function_name = function_data.get("function_name", "unknown")
    parameters = function_data.get("parameters", [])
    logic = function_data.get("logic", [])
    
    # Context for model (function signature + logic preview)
    param_str = ", ".join(parameters)
    logic_preview = "\n".join(logic[:3]) if logic else "# Basic implementation"
    
    messages = [
    {
        "role": "system",
        "content": f"""
        You are an expert in {language}.

        Generate ONLY a {style_prompt} docstring.

        No explanation. Only docstring.
        """
    },
    {
        "role": "user",
        "content": f"""
        Function:
        {function_data["code"]}
        """
    }
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
