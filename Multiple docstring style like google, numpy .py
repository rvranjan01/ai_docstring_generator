import inspect

def generate_docstring(func, style="google"):
    """
    Generate docstring for a function in different styles.

    Parameters
    ----------
    func : function
        Function object to generate docstring for
    style : str
        Style of docstring (google, numpy, sphinx)

    Returns
    -------
    str
        Generated docstring
    """

    sig = inspect.signature(func)
    params = sig.parameters
    return_type = sig.return_annotation

    if style.lower() == "google":
        doc = '"""\nSummary of the function.\n\nArgs:\n'
        for name, param in params.items():
            doc += f"    {name} ({param.annotation if param.annotation != inspect._empty else 'type'}): Description.\n"
        doc += "\nReturns:\n"
        doc += f"    {return_type if return_type != inspect._empty else 'type'}: Description.\n"
        doc += '"""'

    elif style.lower() == "numpy":
        doc = '"""\nSummary of the function.\n\nParameters\n----------\n'
        for name, param in params.items():
            doc += f"{name} : {param.annotation if param.annotation != inspect._empty else 'type'}\n"
            doc += "    Description.\n"
        doc += "\nReturns\n-------\n"
        doc += f"{return_type if return_type != inspect._empty else 'type'}\n"
        doc += "    Description.\n"
        doc += '"""'

    elif style.lower() == "sphinx":
        doc = '"""\nSummary of the function.\n\n'
        for name, param in params.items():
            doc += f":param {name}: Description\n"
            doc += f":type {name}: {param.annotation if param.annotation != inspect._empty else 'type'}\n"
        doc += f":return: Description\n"
        doc += f":rtype: {return_type if return_type != inspect._empty else 'type'}\n"
        doc += '"""'

    else:
        return "Unsupported docstring style."

    return doc


# Example function
def add(a: int, b: int) -> int:
    return a + b


# Generate docstrings
print("Google Style:\n")
print(generate_docstring(add, "google"))

print("\nNumPy Style:\n")
print(generate_docstring(add, "numpy"))

print("\nSphinx Style:\n")
print(generate_docstring(add, "sphinx"))