

import re

def insert_docstrings(code: str, results: list, language: str):
    """
    Insert docstrings above function definitions using regex
    """

    for func in results:
        func_name = func.get("function_name")
        doc = func.get("docstring", "")

        if not func_name or not doc:
            continue

        # Choose comment style
        if language == "python":
            doc_block = f'"""\n{doc}\n"""'
            pattern = rf"(def\s+{func_name}\s*\(.*?\):)"
        elif language in ["javascript", "typescript"]:
            doc_block = f"/**\n{doc}\n*/"
            pattern = rf"(function\s+{func_name}\s*\(.*?\))"
        elif language == "java":
            doc_block = f"/**\n{doc}\n*/"
            pattern = rf"(\b{func_name}\s*\(.*?\)\s*\{{)"
        else:
            doc_block = f"/*\n{doc}\n*/"
            pattern = rf"({func_name}\s*\(.*?\))"

        # Insert docstring above function
        def replacer(match):
            return f"{doc_block}\n{match.group(1)}"

        code = re.sub(pattern, replacer, code, count=1)

    return code