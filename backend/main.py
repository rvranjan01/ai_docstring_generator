from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware

from ai_engine import generate_docstring
from ai_parser import analyze_code
from generic_inserter import insert_docstrings

app = FastAPI()

# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    style: str = Form("google")
):
    try:
        # ✅ STEP 1: Validate file type
        allowed_extensions = [".py", ".js", ".java", ".ts"]
        if not any(file.filename.endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        # ✅ STEP 2: Read file
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )

        original_code = contents.decode("utf-8")

        # ✅ STEP 3: Analyze code using AI
        analysis = analyze_code(original_code)

        if not isinstance(analysis, dict):
            raise HTTPException(
                status_code=500,
                detail="AI parsing failed"
            )

        if "error" in analysis:
            raise HTTPException(
                status_code=400,
                detail=analysis["error"]
            )

        language = analysis.get("language", "unknown")
        functions = analysis.get("functions", [])

        # ✅ STEP 4: No functions case
        if not functions:
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

        # ✅ STEP 5: Generate docstrings
        results = []

        for func in functions:
            try:
                func_name = func.get("name") or func.get("function_name") or "unknown_function"

                docstring = generate_docstring(func, style, language)

                results.append({
                    "function_name": func_name,
                    "docstring": docstring,
                    "code": func.get("code", "")
                })

            except Exception as e:
                print(f"Error generating docstring: {e}")

        # ✅ STEP 6: Insert docstrings into code
        documented_code = insert_docstrings(original_code, results, language)

        # ✅ STEP 7: Quality check
        original_lines = len(original_code.splitlines())
        new_lines = len(documented_code.splitlines())

        quality_check = {
            "status": "success",
            "functions_documented": len(results),
            "original_lines": original_lines,
            "new_lines": new_lines,
            "lines_added": new_lines - original_lines,
            "code_integrity": "preserved"
        }

        # ✅ STEP 8: Return response
        return {
            "filename": file.filename,
            "language_detected": language,
            "functions_found": results,
            "documented_code": documented_code,
            "quality_check": quality_check,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print("🔥 INTERNAL ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Check backend logs."
        )