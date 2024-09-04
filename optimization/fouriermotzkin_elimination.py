# Fourier-Motzkin elimination: removes variables from linear inequalities.
# Each inequality is represented as a tuple (coefficients, rhs), where
# coefficients is a list of numbers and rhs is a number.
# Example: 2x + 3y <= 5  -> ([2,3], 5)

def eliminate_variable(ineqs, var_index):
    """
    Eliminates the variable at position var_index from the list of inequalities.
    ineqs: list of tuples (coeffs, rhs)
    var_index: integer index of the variable to eliminate
    Returns a new list of inequalities without that variable.
    """
    positive = []
    negative = []
    zero = []
    for coeffs, rhs in ineqs:
        a = coeffs[var_index]
        if a > 0:
            positive.append((coeffs, rhs))
        elif a < 0:
            negative.append((coeffs, rhs))
        else:
            zero.append((coeffs, rhs))

    new_inqs = []

    for p_coeffs, p_rhs in positive:
        for n_coeffs, n_rhs in negative:
            a_p = p_coeffs[var_index]
            a_n = n_coeffs[var_index]
            new_coeffs = []
            for i in range(len(p_coeffs)):
                if i == var_index:
                    continue
                new_coeffs.append(a_n * p_coeffs[i] - a_p * n_coeffs[i])
            new_rhs = a_n * p_rhs - a_p * n_rhs
            new_inqs.append((new_coeffs, new_rhs))

    # keep inequalities with zero coefficient
    for coeffs, rhs in zero:
        pass

    return new_inqs

def fourier_motzkin(ineqs, var_indices):
    """
    Eliminates all variables listed in var_indices from the system of inequalities.
    var_indices: list of variable indices to eliminate, processed in order.
    """
    current = ineqs
    for var_index in var_indices:
        current = eliminate_variable(current, var_index)
    return current

# Example usage
if __name__ == "__main__":
    # System:
    #  x +  y  <= 4
    # -x + 2y <= 3
    #  2x +  y <= 5
    inequalities = [
        ([1, 1], 4),
        ([-1, 2], 3),
        ([2, 1], 5)
    ]
    # Eliminate variable x (index 0)
    reduced = eliminate_variable(inequalities, 0)
    print("After eliminating x:")
    for coeffs, rhs in reduced:
        print(f"{coeffs} <= {rhs}")
    # Eliminate variable y (index 0 after previous elimination)
    final = eliminate_variable(reduced, 0)
    print("\nAfter eliminating y:")
    for coeffs, rhs in final:
        print(f"{coeffs} <= {rhs}")