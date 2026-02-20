from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_python_code

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
    print(f"Parsed Data: {parsed_data}")
    print(f"File Name: {file.filename}")
    print(f"File Size: {len(contents)} bytes")
    print(code)

    return {
        "filename": file.filename,
        "functions_found": parsed_data
    }

    

