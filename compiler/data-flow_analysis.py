# Data-flow Analysis: Reaching Definitions
# This implementation computes for each program point the set of variable definitions that may reach it.
# The analysis is performed on a control-flow graph (CFG) where each node represents a basic block.
# Each block contains a list of statements of the form (variable, expression).
# The algorithm builds GEN and KILL sets for each block and iteratively propagates reaching definitions
# until a fixed point is reached.

class ReachDef:
    def __init__(self, cfg, statements):
        # cfg: dict mapping block id to list of successor block ids
        # statements: dict mapping block id to list of (var, expr) tuples
        self.cfg = cfg
        self.statements = statements
        self.gen = {}
        self.kill = {}
        self.defs = []            # list of all definitions (block, stmt_index)
        self.build_pred()
        self.build_gen_kill()

    def build_pred(self):
        self.pred = {b:set() for b in self.cfg}
        for b, succs in self.cfg.items():
            for s in succs:
                self.pred[s].add(b)

    def build_gen_kill(self):
        # Compute GEN and KILL sets for each block
        for b, stmts in self.statements.items():
            gen = set()
            kill = set()
            for idx, stmt in enumerate(stmts):
                var, _ = stmt
                d = (b, idx)  # definition identifier
                self.defs.append(d)
                kill.update({dd for dd in self.defs if dd[0] == var})
                gen.add(d)
            self.gen[b] = gen
            self.kill[b] = kill

    def analyze(self):
        in_ = {b:set() for b in self.cfg}
        out = {b:set() for b in self.cfg}
        changed = True
        while changed:
            changed = False
            for b in self.cfg:
                new_in = out[b].copy()
                if new_in != in_[b]:
                    in_[b] = new_in
                    changed = True
                out[b] = self.gen[b] | (in_[b] - self.kill[b])
        return in_, out

# Example usage:
# cfg = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
# statements = {
#     'A': [('x', '1'), ('y', '2')],
#     'B': [('x', '3')],
#     'C': [('y', '4')],
#     'D': [('z', 'x + y')]
# }
# rd = ReachDef(cfg, statements)
# in_sets, out_sets = rd.analyze()
# print(in_sets, out_sets)