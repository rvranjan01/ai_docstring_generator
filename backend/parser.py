import ast

def parse_python_code(code: str):
    """
    Parses Python code using AST and extracts:
    - Function names
    - Parameters
    - Function body (basic logic as text)
    """

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        # If uploaded file has syntax error
        return {
            "error": f"Syntax error in Python file: {str(e)}",
            "functions_found": []
        }

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            function_name = node.name

            parameters = [arg.arg for arg in node.args.args]

            # Extract function body (logic)
            function_body = []
            for body_node in node.body:
                function_body.append(ast.dump(body_node))

            functions.append({
                "function_name": function_name,
                "parameters": parameters,
                "logic": function_body
            })

    return {
        "functions_found": functions
    }