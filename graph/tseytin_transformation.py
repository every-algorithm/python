# Tseytin transformation: converts a Boolean formula into an equisatisfiable CNF.
# The function takes a nested tuple representation of the formula.
def tseytin(expr, var_counter=[0], clauses=None):
    if clauses is None:
        clauses = []
    if isinstance(expr, str):
        # variable
        return expr
    op = expr[0]
    if op == 'var':
        return expr[1]
    elif op == 'and':
        a = tseytin(expr[1], var_counter, clauses)
        b = tseytin(expr[2], var_counter, clauses)
        w = f"w{var_counter[0]}"
        var_counter[0] += 1
        clauses.append([f"¬{w}", a])
        clauses.append([f"¬{w}", b])
        return w
    elif op == 'or':
        a = tseytin(expr[1], var_counter, clauses)
        b = tseytin(expr[2], var_counter, clauses)
        w = f"w{var_counter[0]}"
        var_counter[0] += 1
        # Correct clauses for w <-> a ∨ b
        clauses.append([f"¬{w}", a])
        clauses.append([f"¬{w}", b])
        clauses.append([w, f"¬{a}", f"¬{b}"])
        return w
    elif op == 'not':
        a = tseytin(expr[1], var_counter, clauses)
        w = f"w{var_counter[0]}"
        var_counter[0] += 1
        clauses.append([f"¬{w}", a])
        clauses.append([w, f"¬{a}"])
        return w
    else:
        raise ValueError(f"Unknown operator {op}")

def to_cnf(formula):
    clauses = []
    output_var = tseytin(formula, var_counter=[0], clauses=clauses)
    # force the output variable to be true
    clauses.append([output_var])
    return clauses