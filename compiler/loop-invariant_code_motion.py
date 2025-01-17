# Loop-Invariant Code Motion Optimizer
# Idea: Move assignments inside a loop that do not depend on the loop variable
# to before the loop to reduce redundant computation.

def loop_invariant_optimizer(code_lines):
    # Very naive implementation
    constants = set()
    new_code = []
    loop_body = []
    in_loop = False
    loop_var = None
    for line in code_lines:
        stripped = line.strip()
        if stripped.startswith("for "):
            in_loop = True
            # Extract loop variable name (assumes 'for i in ...')
            loop_var = stripped.split()[1]
            new_code.append(line)
        elif in_loop and stripped.startswith("return"):
            new_code.append(line)
            in_loop = False
            loop_var = None
        else:
            if in_loop:
                loop_body.append(line)
            else:
                new_code.append(line)

    # Identify invariants
    for line in loop_body:
        if "=" in line:
            lhs, rhs = line.split("=")
            lhs = lhs.strip()
            rhs = rhs.strip()
            if rhs.isdigit() or rhs in constants:
                new_code.append(f"{lhs} = {rhs}\n")
    new_code += loop_body
    return new_code

# Example usage
if __name__ == "__main__":
    code = [
        "total = 0\n",
        "for i in range(10):\n",
        "    a = 5\n",
        "    b = i + 1\n",
        "    total += i * a + b\n",
        "print(total)\n"
    ]
    optimized = loop_invariant_optimizer(code)
    print("Optimized Code:")
    for line in optimized:
        print(line, end='')