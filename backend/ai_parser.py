
import os
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

def analyze_code(code: str):
    """
    Detect language + extract functions using AI
    """

    prompt = f"""
    Analyze the following code.

    1. Detect programming language
    2. Extract all functions/methods
    3. Return STRICT JSON only (no explanation, no markdown)

    Format:
    {{
        "language": "python/javascript/java",
        "functions": [
            {{
                "name": "function_name",
                "parameters": ["param1"],
                "code": "full function code"
            }}
        ]
    }}

    CODE:
    {code}
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        print("🔍 RAW AI RESPONSE:\n", raw)  # DEBUG

        # ✅ Remove markdown if present
        if raw.startswith("```"):
            raw = raw.split("```", 2)[-1].strip()

        # ✅ Handle empty response
        if not raw:
            return {
                "error": "Empty response from AI",
                "language": "unknown",
                "functions": []
            }

        # ✅ Parse JSON safely
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("❌ JSON PARSE FAILED. RAW OUTPUT:")
            print(raw)

            return {
                "error": "Invalid JSON from AI",
                "language": "unknown",
                "functions": []
            }

    except Exception as e:
        print("🔥 AI PARSER ERROR:", str(e))
        return {
            "error": str(e),
            "language": "unknown",
            "functions": []
        }