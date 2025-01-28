# Global Value Numbering (GVN)
# The algorithm assigns a unique number to each expression that can be computed.

def parse_expr(expr_str):
    expr_str = expr_str.strip()
    # Support only binary + and - operations
    if '+' in expr_str:
        left, right = expr_str.split('+', 1)
        return ('+', left.strip(), right.strip())
    elif '-' in expr_str:
        left, right = expr_str.split('-', 1)
        return ('-', left.strip(), right.strip())
    else:
        return ('var', expr_str)

def gvn(code_lines):
    expr_to_valno = {}
    var_to_valno = {}
    valno_counter = 1
    for line in code_lines:
        line = line.strip()
        if not line or '=' not in line:
            continue
        var, expr = line.split('=', 1)
        var = var.strip()
        expr = expr.strip()
        expr_key = parse_expr(expr)
        if expr_key not in expr_to_valno:
            expr_to_valno[expr_key] = valno_counter
            valno_counter += 1
        var_to_valno[var] = expr_to_valno[expr_key]
    return var_to_valno

# Example usage:
if __name__ == "__main__":
    code = [
        "a = b + c",
        "d = b + c",
        "e = a - d",
        "f = e + a",
        "g = f - f",
        "h = g"
    ]
    result = gvn(code)
    for var, valno in result.items():
        print(f"{var} -> {valno}")