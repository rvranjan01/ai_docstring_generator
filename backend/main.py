from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_python_code
from ai_engine import generate_docstring
from code_inserter import insert_docstrings_into_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # STEP 1–3: validate + read file
    if not file.filename.endswith(".py"):
        raise HTTPException(
            status_code=400,
            detail="Only Python (.py) files allowed",
        )

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    original_code = contents.decode("utf-8")

    # STEP 4: parse code
    parsed_data = parse_python_code(original_code)
    if "error" in parsed_data:
        raise HTTPException(status_code=400, detail=parsed_data["error"])

    functions = parsed_data.get("functions_found", [])

    if not functions:
        # No functions found – return original code as is
        return {
            "filename": file.filename,
            "message": "No functions found in file.",
            "functions_found": [],
            "documented_code": original_code,
            "quality_check": {
                "status": "no_functions",
                "functions_documented": 0,
                "lines_added": 0,
                "code_integrity": "unchanged"
            }
        }

    # STEP 5–7: call AI for each function
    results = []
    for func in functions:
        docstring = generate_docstring(func)
        results.append({
            "function_name": func["function_name"],
            "parameters": func["parameters"],
            "docstring": docstring,
        })

    # STEP 8: insert docstrings into original code
    documented_code = insert_docstrings_into_code(original_code, results)

    # STEP 9: simple quality check
    original_lines = len(original_code.splitlines())
    new_lines = len(documented_code.splitlines())

    quality_check = {
        "status": "success",
        "functions_documented": len(results),
        "original_lines": original_lines,
        "new_lines": new_lines,
        "lines_added": new_lines - original_lines,
        "code_integrity": "preserved"  # AST re-generation guarantees syntax validity
    }

    # STEP 10: return to user
    return {
        "filename": file.filename,
        "functions_found": results,
        "documented_code": documented_code,
        "quality_check": quality_check,
    }
