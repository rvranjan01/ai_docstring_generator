from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_python_code
from ai_engine import generate_demo_docstring

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  # File Upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    

    # File Validation
    if not file.filename.endswith(".py"):
        raise HTTPException(
            status_code=400, 
            detail="Only Python (.py) files allowed")

    contents = await file.read()
    
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    # Read File Contents

    code = contents.decode("utf-8")

    # Parse Code (AST)

    parsed_data = parse_python_code(code)


    results = []

    for func in parsed_data["functions_found"]:
        docstring = generate_demo_docstring(func)

    results.append({
        "function_name": func["function_name"],
        "parameters": func["parameters"],
        "docstring": docstring
    })

    return {
        "filename": file.filename,
        "functions_found": results
    }