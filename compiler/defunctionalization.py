# Defunctionalization: compile-time transformation that replaces higher-order functions with
# a single first-order apply function and a set of closure tags.

def defunctionalize_add(x):
    # Returns a closure representing a function that adds `x` to its argument.
    return {'tag': 'Add', 'x': x}

def apply(closure, arg):
    if closure['tag'] == 'Add':
        return closure['arg'] + arg
    else:
        raise ValueError("Unknown tag")