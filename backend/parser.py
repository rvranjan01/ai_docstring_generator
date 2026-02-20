import ast

def parse_python_code(code: str):
    """
    Parses Python code using AST and extracts
    function names and parameters.
    """

    tree = ast.parse(code)

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            parameters = [arg.arg for arg in node.args.args]

            functions.append({
                "function_name": function_name,
                "parameters": parameters
            })

    return functions
