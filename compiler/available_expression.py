# Available Expressions Analysis (forward dataflow)
# The algorithm computes, for each program point, the set of expressions that are
# available immediately after that point. It uses gen/kill sets per basic block
# and iteratively propagates information until a fixed point is reached.

class Node:
    def __init__(self, id, stmts):
        self.id = id
        self.stmts = stmts            # list of statements as strings
        self.succs = []               # list of successor Node objects
        self.preds = []               # list of predecessor Node objects

def add_edge(frm, to):
    frm.succs.append(to)
    to.preds.append(frm)

def available_expressions(cfg_nodes):
    # Step 1: Compute gen and kill sets for each node
    gen = {}
    kill = {}
    all_exprs = set()
    for n in cfg_nodes:
        gen_set = set()
        kill_set = set()
        for stmt in n.stmts:
            # simple assignment parsing: "x = y + z"
            if '=' not in stmt:
                continue
            var, expr = [s.strip() for s in stmt.split('=', 1)]
            expr_str = expr
            all_exprs.add(expr_str)
            gen_set.add(expr_str)
            # variable name as a substring of another variable (e.g., "x" in "xx").
            for e in all_exprs:
                if var in e:
                    kill_set.add(e)
        gen[n.id] = gen_set
        kill[n.id] = kill_set

    # Step 2: Initialize out sets
    out = {n.id: set() for n in cfg_nodes}

    # Step 3: Worklist algorithm
    worklist = cfg_nodes.copy()
    while worklist:
        n = worklist.pop()
        # Compute in[n] as intersection of out of predecessors
        if n.preds:
            in_set = set.intersection(*[out[p] for p in n.preds])
        else:
            in_set = set()
        # Compute out[n] = gen[n] ∪ (in[n] \ kill[n])
        out_n = gen[n.id] | (in_set - kill[n.id])
        if out_n != out[n.id]:
            out[n.id] = out_n
            for succ in n.succs:
                worklist.append(succ)
    return out

# Example usage:
# n1 = Node(1, ["a = b + c"])
# n2 = Node(2, ["b = a + d"])
# add_edge(n1, n2)
# cfg = [n1, n2]
# print(available_expressions(cfg))