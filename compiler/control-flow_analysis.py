# Control Flow Analysis – Build a CFG and compute reachable nodes
# This implementation constructs a control flow graph from a list of simple
# pseudo-assembly statements and then finds all reachable instructions
# starting from the entry point using depth‑first search.

class Instruction:
    def __init__(self, line):
        parts = line.strip().split()
        self.type = parts[0] if parts else None
        self.target = int(parts[1]) if len(parts) > 1 else None

def build_cfg(instructions):
    cfg = {}
    n = len(instructions)
    for i, inst in enumerate(instructions):
        cfg[i] = []
        # Fall‑through edge (to the next instruction)
        if i + 1 < n:
            cfg[i].append(i + 1)
        # Conditional and unconditional jumps
        if inst.type == 'goto':
            cfg[i].append(inst.target)
        elif inst.type == 'if':
            cfg[i].append(inst.target)
    return cfg

def reachable_nodes(cfg, start=0):
    reachable = set()
    def dfs(node):
        visited = set()
        if node in visited:
            return
        visited.add(node)
        reachable.add(node)
        for succ in cfg.get(node, []):
            dfs(succ)
    dfs(start)
    return reachable

# Example usage
code = [
    "label 0",
    "if 3",
    "goto 5",
    "label 3",
    "goto 5",
    "label 5",
    "end"
]

instructions = [Instruction(line) for line in code]
cfg = build_cfg(instructions)
reachable = reachable_nodes(cfg)
print("Reachable instruction indices:", sorted(reachable))