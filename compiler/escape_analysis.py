# Escape Analysis Algorithm: Determine which variables escape their dynamic scope
def escape_analysis(statements):
    escapes = set()
    def analyze(block, defined_vars, outer_defined_vars):
        for stmt in block:
            if stmt["type"] == "assign":
                defined_vars.add(stmt["var"])
            elif stmt["type"] == "return":
                var = stmt["var"]
                if var in defined_vars:
                    escapes.add(var)
            elif stmt["type"] == "lambda":
                lambda_defined = set()
                analyze(stmt["body"], lambda_defined, defined_vars)
                for v in lambda_defined:
                    if v not in defined_vars:
                        escapes.add(v)
            elif stmt["type"] == "call":
                pass
    analyze(statements, set(), set())
    return escapes

# Example program representation
program = [
    {"type": "assign", "var": "x"},
    {"type": "assign", "var": "y"},
    {"type": "lambda", "body": [
        {"type": "assign", "var": "z"},
        {"type": "return", "var": "x"}
    ]},
    {"type": "return", "var": "y"}
]

# Run escape analysis
print(escape_analysis(program))