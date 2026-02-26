# AI Docstring Generator

A full-stack AI-powered system to automatically generate high-quality Python docstrings by analyzing uploaded Python files using AST and OpenAI language models.  
This project is actively developed as an **ongoing team project** with GitHub collaboration workflows.

---

## 🚀 Project Overview

This tool allows users to:

✔ Upload a Python `.py` file through a web interface  
✔ Validate and parse the code using Python’s AST  
✔ Extract function names and parameters  
✔ Generate descriptive docstrings using real AI (OpenAI API)  
✔ Display results dynamically on the frontend

The backend is built using FastAPI, while the frontend uses HTML, CSS, and JavaScript.

---

## 🧱 Project Structure
    ai_docstring_generator/
    ├── backend/
    │ ├── main.py # FastAPI server
    │ ├── parser.py # AST parsing logic
    │ └── ai_engine.py # AI docstring generator logic
    ├── frontend/
    │ ├── index.html # File upload UI
    │ ├── script.js # JavaScript for API requests
    │ └── style.css # Basic styling
    ├── requirements.txt # Dependencies
    └── README.md # Project documentation

---

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, Uvicorn, AST  
**AI:** OpenAI API (GPT-3.5 / GPT-4 models)  
**Frontend:** HTML, CSS, JavaScript  
**Tools:** Git & GitHub (collaboration)  

---

## 📥 Installation & Setup

### Clone the repository

    git clone https://github.com/rvranjan01/ai_docstring_generator.git
    cd ai_docstring_generator

### Create Virtual Environment (Recommended)

    Windows
        python -m venv venv
        venv\Scripts\activate
    Linux / Mac
        python3 -m venv venv
        source venv/bin/activate

### Install Requirements
    pip install -r requirements.txt

    If missing, install dependencies manually:
        pip install fastapi uvicorn openai python-multipart

---

## 🔐 OpenAI API Configuration (Real AI)

    Go to https://platform.openai.com/api-keys
        and generate an API key

    Set it as environment variable

        Windows
            setx OPENAI_API_KEY "your_openai_api_key_here"
        Mac / Linux
            export OPENAI_API_KEY="your_openai_api_key_here"

    Close and reopen your terminal after setting the variable.

    Or else You can use .env for AI API key.

---

## ▶️ Running the Server

    In project root:
        python -m uvicorn app.main:app --reload
    Server starts at:
        http://127.0.0.1:8000
    Swagger API docs at:
        http://127.0.0.1:8000/docs

## 🧠 Running the Frontend using " Go Live " option

    Open frontend/index.html in a browser
    Choose a Python file
    Click Upload & Parse
    View the generated docstrings on the page
    Make sure FastAPI is running before uploading.

---

## 🧪 Example Input
    def add(a, b):
        return a + b

## 📤 Example Output (AI Generated)
    """
    Add two numbers.

    Args:
        a (int): First number
        b (int): Second number

    Returns:
        int: Sum of a and b
    """
---

# ⭐ Contribution

    Feel free to explore, contribute, or star the repo!