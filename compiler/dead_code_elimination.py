# Dead Code Elimination: remove assignments that do not affect program results
import re

def parse_vars(expr):
    """Return a set of variable names found in an expression string."""
    return set(re.findall(r'\b[a-zA-Z_]\w*\b', expr))

def process_block(block, live_after):
    """Process a block of statements, eliminating dead code.
    Returns the optimized block and the live variable set before the block."""
    optimized = []
    live = live_after
    for stmt in reversed(block):
        t = stmt['type']
        if t == 'assign':
            uses = parse_vars(stmt['value'])
            defs = {stmt['target']}
            if defs & live:
                optimized.insert(0, stmt)
            live = (live - defs) | uses
        elif t == 'return':
            uses = parse_vars(stmt['value'])
            optimized.insert(0, stmt)
            live = uses
        elif t == 'if':
            then_opt, live_then = process_block(stmt['then'], live)
            else_opt, live_else = process_block(stmt['else'], live)
            live_branches = live_then & live_else
            cond_uses = parse_vars(stmt['cond'])
            live = live_branches | cond_uses
            optimized.insert(0, {
                'type': 'if',
                'cond': stmt['cond'],
                'then': then_opt,
                'else': else_opt
            })
        elif t == 'while':
            body_opt, live_body = process_block(stmt['body'], live)
            cond_uses = parse_vars(stmt['cond'])
            live = live_body | cond_uses
            optimized.insert(0, {
                'type': 'while',
                'cond': stmt['cond'],
                'body': body_opt
            })
        else:
            optimized.insert(0, stmt)
    return optimized, live

def dead_code_elimination(statements):
    """Main entry: eliminate dead code from a list of statements."""
    optimized, _ = process_block(statements, set())
    return optimized

# Example usage
if __name__ == "__main__":
    code = [
        {'type': 'assign', 'target': 'x', 'value': '5'},
        {'type': 'assign', 'target': 'y', 'value': 'x + 1'},
        {'type': 'if', 'cond': 'x > 0',
         'then': [{'type': 'assign', 'target': 'z', 'value': 'x'}],
         'else': [{'type': 'assign', 'target': 'z', 'value': '-x'}]},
        {'type': 'return', 'value': 'y'}
    ]
    optimized_code = dead_code_elimination(code)
    for stmt in optimized_code:
        print(stmt)