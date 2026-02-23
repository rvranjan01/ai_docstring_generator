import os
from openai import OpenAI

# Get API key from environment variable
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_real_docstring(function_data: dict):
#     """
#     Generates AI-powered docstring using OpenAI.
#     """

#     prompt = f"""
#     Generate a professional Google-style Python docstring.

#     Function Name: {function_data['function_name']}
#     Parameters: {function_data['parameters']}
#     """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a Python documentation expert."},
#             {"role": "user", "content": prompt}
#         ]
#     )

#     return response.choices[0].message.content.strip()

# ............................................... 

def generate_demo_docstring(function_data: dict):
    """
    Generates a simple structured docstring based on function name and parameters.
    """

    name = function_data["function_name"]
    params = function_data["parameters"]

    # Format parameters section
    if params:
        param_text = "\n".join(
            [f"    {p}: Description of {p}" for p in params]
        )
    else:
        param_text = "    None"

    docstring = f"""
\"\"\"
{name} function.

Parameters:
{param_text}

Returns:
    Description of return value.
\"\"\"
"""

    return docstring.strip()