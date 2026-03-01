# backend/code_inserter.py
import ast
from typing import List, Dict

def _clean_docstring(raw_docstring: str) -> str:
    """
    Clean AI-generated docstring text before inserting into code.
    """
    # Strip leading/trailing whitespace
    text = raw_docstring.strip()
    
    # Remove markdown code fences
    if text.startswith("```"):
        lines = text.splitlines()
        # drop opening fence
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        # drop closing fence
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    
    # Remove outer triple quotes if the AI returned the docstring with them
    if text.startswith('"""') and text.endswith('"""'):
        text = text[3:-3].strip()
    elif text.startswith("'''") and text.endswith("'''"):
        text = text[3:-3].strip()
    
    # Clean up extra blank lines at start/end
    lines = [line.rstrip() for line in text.splitlines()]
    # remove leading empty lines
    while lines and not lines[0].strip():
        lines.pop(0)
    # remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop(-1)
    
    return "\n".join(lines).strip()

def insert_docstrings_into_code(original_code: str, docstrings: List[Dict]) -> str:
    """
    Insert cleaned docstrings into original Python code.
    """
    try:
        tree = ast.parse(original_code)
    except SyntaxError:
        return original_code
    
    # Clean all docstrings first
    docstring_map = {}
    for item in docstrings:
        clean_doc = _clean_docstring(item["docstring"])
        docstring_map[item["function_name"]] = clean_doc
    
    class DocstringInserter(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            # first recurse into nested definitions
            self.generic_visit(node)

            if node.name in docstring_map:
                clean_doc = docstring_map[node.name]
                if clean_doc:
                    # create a new Expr node containing the string constant
                    doc_node = ast.Expr(value=ast.Constant(value=clean_doc))

                    # if there is an existing docstring (first statement is a string literal), replace it
                    if (node.body and isinstance(node.body[0], ast.Expr) and
                        isinstance(node.body[0].value, ast.Constant) and
                        isinstance(node.body[0].value.value, str)):
                        node.body[0] = doc_node
                    else:
                        # otherwise insert at the top of the function body
                        node.body.insert(0, doc_node)
            return node
    
    modified_tree = DocstringInserter().visit(tree)
    ast.fix_missing_locations(modified_tree)
    return ast.unparse(modified_tree)
