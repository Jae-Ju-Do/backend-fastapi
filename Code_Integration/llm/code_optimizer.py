import re


def read_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        c_code = file.read()
    return c_code


def clean_function_body(body):
    cleaned_body = '\n'.join(line for line in body.splitlines() if line.strip())
    return cleaned_body


def extract_function(code):
    pattern = re.compile(r'/\* Function: (\w+) \*/(.*?)\n(?=/\* Function: |\Z)', re.DOTALL)
    functions = pattern.findall(code)

    cleaned_functions = []
    for func_name, func_body in functions:
        cleaned_functions.append((func_name, clean_function_body(func_body)))

    return cleaned_functions


def merge_function(function):
    merge_code = ""
    for func_name, func_body in function:
        merge_code = merge_code + func_body + "\n\n"

    return merge_code


def extract_called_functions(body):
    called_functions = []
    matches = re.findall(r'(\w+)\(', body)
    called_functions.extend(matches)
    return called_functions


def code_optimizer(c_code):
    functions = extract_function(c_code)
    merge_code = merge_function(functions)
    return merge_code
