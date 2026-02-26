# AI Docstring Generator

![Python version](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## What the project does

**AI Docstring Generator** is a simple full‑stack application that automatically produces Google‑style Python docstrings for functions found in an uploaded `.py` file. The backend parses the code using Python's AST module, sends metadata to an AI engine (Gemini/OpenAI), and returns recommended docstrings which are then displayed in the frontend UI.

## Why the project is useful

- Accelerates documentation by generating initial docstrings.
- Promotes consistent formatting and style across codebases.
- Helps developers understand unfamiliar functions quickly.
- Demonstrates integration of FastAPI, AST parsing, and language model APIs.

## Project structure

```
ai_docstring_generator/
├── backend/            # FastAPI server and AI logic
│   ├── ai_engine.py    # Gemini/OpenAI integration & prompt logic
│   ├── main.py         # FastAPI application with upload endpoint
│   ├── parser.py       # AST-based Python parser
│   └── requirements.txt
├── frontend/           # Simple HTML/JS UI for file upload
│   ├── index.html
│   ├── script.js
│   └── style.css
├── func.py             # sample arithmetic script (demo purposes)
├── hi.py               # empty placeholder
├── test.txt            # miscellaneous/test data
└── README.md           # this documentation
```

## Prerequisites

- Python 3.10 or later
- `pip` package manager
- Gemini or OpenAI API key (stored in `.env` or environment variable)

## Installation

1. **Clone the repo**
   ```bash
   git clone <repository-url>
   cd ai_docstring_generator
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv            # or `venv` on Windows
   source .venv/bin/activate       # Linux/macOS
   .venv\Scripts\activate        # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure API credentials**
   Create a `.env` file in the project root with:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
   or set `OPENAI_API_KEY` if using the OpenAI client.

## Running the application

1. **Start the backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Open the frontend**
   - Open `frontend/index.html` in your browser (e.g. via live server extension or by double-clicking).
   - Click **Upload & Parse** after selecting a `.py` file.

3. **Review results**
   The page will list each function and the generated docstring.

## Example

**Input Python file**:
```python

def add(a, b):
    return a + b
```

**Backend response snippet**:
```json
{
  "function_name": "add",
  "parameters": ["a", "b"],
  "docstring": "\"\"\"\nAdd two numbers.\n\nArgs:\n    a (int): First addend.\n    b (int): Second addend.\n\nReturns:\n    int: Sum of `a` and `b`.\n\"\"\""
}
```

## Getting help

- File issues or feature requests on the GitHub repository.
- Check the FastAPI docs for backend development: https://fastapi.tiangolo.com/

## Contributing

Contributions are welcome! Please read a [`CONTRIBUTING.md`](CONTRIBUTING.md) file (when added) or open an issue to discuss improvements. Keep pull requests small and include tests where appropriate.

<!-- ## Maintainers

- Primary maintainer: *Your Name* – [you@example.com](mailto:you@example.com) -->

## License

Distributed under the [MIT License](LICENSE).

---

