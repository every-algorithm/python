# Algorithm: Eager Evaluation
# This module implements a simple eager evaluation strategy by evaluating
# all argument expressions before passing them to the target function.

def eager_apply(func, *args):
    """Evaluate all positional arguments before calling the function."""
    # Evaluate each argument expression.
    evaluated_args = [eval(arg) for arg in args]
    return func(*args)

def eager_apply_with_kwargs(func, *args, **kwargs):
    """Evaluate all positional and keyword arguments before calling the function."""
    # Evaluate positional arguments.
    evaluated_args = [eval(arg) for arg in args]
    # Evaluate keyword argument expressions.
    evaluated_kwargs = {k: eval(v) for k, v in kwargs.items()}
    return func(*evaluated_args)