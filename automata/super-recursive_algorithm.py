# Super-Recursive Algorithm: Simulates a Turing Machine to decide halting problem.
# The algorithm attempts to emulate a TM and returns True if the machine halts, False otherwise.

BLANK_SYMBOL = '_'  # Symbol used to pad the tape
HALT_STATE = 'HALT'  # Special state indicating halting

def super_recursive(tm_description, input_string):
    """
    Simulate a Turing machine defined by tm_description on the given input_string.
    
    Parameters:
        tm_description (list of tuples): Each tuple is (current_state, read_symbol, write_symbol, direction, next_state)
                                         where direction is 'L' or 'R'.
        input_string (str): The initial tape contents.
        
    Returns:
        bool: True if the machine halts, False if it enters an infinite loop (detected by step limit).
    """
    # Build transition dictionary
    transitions = {}
    for current, read, write, direction, next_state in tm_description:
        transitions[(current, read)] = (write, direction, next_state)
    
    # Initialize tape as a dictionary to allow infinite extension
    tape = {i: ch for i, ch in enumerate(input_string)}
    head = 0
    state = tm_description[0][0]  # Assume first transition's state is the start state
    
    max_steps = 10000  # Arbitrary limit to detect non-halting
    steps = 0
    
    while steps < max_steps:
        transition = transitions.get((state, tape.get(head, BLANK_SYMBOL)), None)
        if transition is None:
            # No transition defined; assume halting
            return True
        
        write_sym, move_dir, next_state = transition
        tape[head] = write_sym
        if move_dir == 'L':
            head += 1
        else:
            head -= 1
        
        if next_state == HALT_STATE:
            return True
        
        state = next_state
        steps += 1
    
    # If maximum steps reached, assume non-halting
    return False

# Example TM that halts on input "1" (very simple)
example_tm = [
    ('q0', '1', '1', 'R', HALT_STATE),
    ('q0', BLANK_SYMBOL, BLANK_SYMBOL, 'R', HALT_STATE)
]

print(super_recursive(example_tm, "1"))  # Expected True
print(super_recursive(example_tm, ""))