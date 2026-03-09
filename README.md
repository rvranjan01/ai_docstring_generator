# AI Docstring Generator

![Python version](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A lightweight full‑stack tool that automatically generates Google‑style Python docstrings for functions within a `.py` file using AI.

---

## 🚀 What the project does

Upload a Python file via the web UI, and the backend will:

1. Parse the code with Python's AST to discover functions.
2. Send each function's signature and logic preview to an AI engine (OpenAI/Gemini via Hugging Face).
3. Insert the returned docstrings into the original source and offer the documented file for download.

The frontend provides a simple drag‑and‑drop interface with a preview of generated documentation.

## 💡 Why it’s useful

- **Speeds up documentation** by providing a starting point for your docstrings.
- **Enforces consistent style** (Google Python pattern) across projects.
- **Improves code comprehension** for collaborators and maintainers.
- **Demonstrates integration** of FastAPI, AST parsing, and large‑language‑model APIs.

## 🗂️ Project structure

```
ai_docstring_generator/
├── backend/            # FastAPI server and AI logic
│   ├── ai_engine.py    # AI prompt and client setup
│   ├── main.py         # FastAPI app + upload endpoint
│   ├── parser.py       # AST-based code analyzer
│   └── requirements.txt
├── frontend/           # Minimal HTML/JS UI
│   ├── index.html
│   ├── script.js
│   └── style.css
├── func.py             # example code snippet
├── hi.py               # placeholder file
├── test.txt            # misc test data
└── README.md           # you are reading this
```

## ⚙️ Prerequisites

- Python 3.10 or newer
- `pip` package manager
- An API key from one of:
  - Hugging Face inference (for `openai` compatible endpoint)
  - OpenAI

## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone <repository-url>
   cd ai_docstring_generator
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate    # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Configure credentials**
   Create a `.env` file at the project root containing either:
   ```env
   HF_TOKEN=hf_<your_token>        # Hugging Face API key
   # or
   OPENAI_API_KEY=sk-...           # OpenAI key
   ```
   The backend chooses whichever is available.

## ▶️ Running the app

1. **Start backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Use the frontend**
   - Open `frontend/index.html` in a browser (no server required).
   - Upload a `.py` file and watch as docstrings are generated.

3. **Download results**
   Reviewed docstrings can be previewed or downloaded as a new file.

## 🧪 Example

**Source file**
```python

def add(a, b):
    return a + b
```

**Backend output**
```json
{
  "function_name": "add",
  "parameters": ["a", "b"],
  "docstring": "\"\"\"Add two numbers.\n\nArgs:\n    a (int): First addend.\n    b (int): Second addend.\n\nReturns:\n    int: Sum of `a` and `b`.\n\"\"\""
}
```

## ❓ Getting help

- Open issues or feature requests on this repository.
- Refer to [FastAPI docs](https://fastapi.tiangolo.com/) for backend customization.
- Hugging Face inference documentation: https://huggingface.co/docs/api-inference

<!-- ## 🤝 Contribution & Maintenance

Contributions are welcome! For details, refer to a future [`CONTRIBUTING.md`](CONTRIBUTING.md) or open an issue. -->

<!-- **Maintainer:** *(add your name or team here)* -->

<!-- ## 📄 License

This project is released under the [MIT License](LICENSE).

--- -->

