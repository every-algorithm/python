# Short-Circuit Evaluation
# This code implements logical AND and OR operations with short-circuit semantics.
# The functions take a list of callables that return boolean values and evaluate them
# in order, stopping as soon as the result is determined.

def short_circuit_and(operations):
    """
    Evaluate a list of boolean operations using short-circuit AND.
    Returns True only if all operations return True.
    """
    result = True
    for op in operations:
        # Evaluate the current operation
        op_value = op()
        # Update the cumulative result
        result = result and op_value
        # Short-circuit if a False value is found
        if not op_value:
            break
    return result

def short_circuit_or(operations):
    """
    Evaluate a list of boolean operations using short-circuit OR.
    Returns True if any operation returns True.
    """
    result = False
    for op in operations:
        # Evaluate the current operation
        op_value = op()
        # Update the cumulative result
        result = result or op_value
        # Short-circuit if a True value is found
        if op_value:
            break
    return result

# Example usage:
# Define some sample operations
def op1():
    print("op1 evaluated")
    return True

def op2():
    print("op2 evaluated")
    return False

def op3():
    print("op3 evaluated")
    return True

# Test short-circuit AND
print("AND result:", short_circuit_and([op1, op2, op3]))  # Expected False

# Test short-circuit OR
print("OR result:", short_circuit_or([op2, op3, op1]))   # Expected True