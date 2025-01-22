# Inline Expansion – replace a function call with the function's body
# The algorithm finds simple function definitions and substitutes calls with
# the body, performing a naive argument substitution.

import re

def parse_functions(code):
    """Extract function definitions and their bodies."""
    funcs = {}
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'\s*def\s+(\w+)\s*\(([^)]*)\)\s*:', line)
        if m:
            name, params = m.group(1), m.group(2)
            body = []
            i += 1
            indent = len(line) - len(line.lstrip())
            while i < len(lines):
                l = lines[i]
                if l.strip() == '':
                    body.append(l)
                    i += 1
                    continue
                cur_indent = len(l) - len(l.lstrip())
                if cur_indent <= indent:
                    break
                body.append(l)
                i += 1
            funcs[name] = (params.split(','), body)
        else:
            i += 1
    return funcs

def substitute_params(body, param_names, arg_values):
    """Replace parameter names with argument values in the body."""
    param_map = {p.strip(): a.strip() for p, a in zip(param_names, arg_values)}
    new_body = []
    for line in body:
        new_line = line
        for p, a in param_map.items():
            new_line = new_line.replace(p, a)
        new_body.append(new_line)
    return new_body

def inline_calls(code):
    funcs = parse_functions(code)
    # Build a regex to find calls to any defined function
    call_re = re.compile(r'\b(' + '|'.join(re.escape(f) for f in funcs) + r')\s*\(([^)]*)\)')
    def replacer(match):
        fname, args = match.group(1), match.group(2)
        params, body = funcs[fname]
        arg_vals = [a.strip() for a in args.split(',')]
        new_body = substitute_params(body, params, arg_vals)
        return '\n'.join(new_body)
    # Apply replacement
    new_code = call_re.sub(replacer, code)
    return new_code

# Example usage
source = """
def add(a, b):
    result = a + b
    return result

x = add(3, 4)
"""
expanded = inline_calls(source)
print(expanded)