# Gemini API integration for generating professional Google-style Python docstrings based on function metadata and logic.
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Load environment variables from .env file

# Initialize Gemini client using API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

client = genai.Client(api_key=api_key)


def generate_demo_docstring(function_data: dict) -> str:
    """
    Generate a professional Google-style Python docstring for a function
    using the Gemini API.
    """
    function_name = function_data.get("function_name", "unknown_function")
    parameters = function_data.get("parameters", [])
    logic = function_data.get("logic", [])

    # Join AST-dumped logic into a readable block
    logic_str = "\n".join(logic)

    prompt = f"""
You are a Python documentation expert.

Write a professional Google-style docstring for the following function.

Function name: {function_name}
Parameters: {parameters}

The function's internal logic (AST-like representation) is:

{logic_str}

Requirements:
- Use Google Python style.
- Explain what the function does (1–3 sentences).
- Document each parameter with type (guess if needed) and description.
- Document the return value.
- If the function may raise any obvious exceptions, mention them in a Raises section.
- Do NOT include the function definition itself, only the docstring content (between triple quotes).
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()
