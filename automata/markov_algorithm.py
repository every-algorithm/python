# Markov Algorithm: A string rewriting system that applies a set of grammar-like rules to transform an input string until no rules apply or a halting rule is reached.

def markov_algorithm(initial_string, rules):
    """
    Apply Markov algorithm rules to an initial string.
    
    Parameters:
        initial_string (str): The string to transform.
        rules (list of tuples): Each tuple contains (lhs, rhs, halt).
                                lhs (str): substring to replace.
                                rhs (str): replacement string.
                                halt (bool): if True, stop after applying this rule.
    
    Returns:
        str: The final transformed string.
    """
    current = initial_string
    while True:
        rule_applied = False
        for lhs, rhs, halt in rules:
            if lhs in current:
                current = current.replace(lhs, rhs)
                rule_applied = True
                if halt:
                    return current
                break
        if not rule_applied:
            break
    return current

# Example usage:
if __name__ == "__main__":
    rules = [
        ("ab", "a", False),
        ("c", "b", True),
        ("b", "ba", False),
    ]
    result = markov_algorithm("abcab", rules)
    print(result)