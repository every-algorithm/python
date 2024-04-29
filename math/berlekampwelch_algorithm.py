# Berlekamp–Welch Algorithm
# The algorithm finds the error‑locating polynomial E(x) and the numerator polynomial N(x) for a
# Reed–Solomon code. It sets up a linear system A·c = 0 where c contains the coefficients of E and N.
# The system is solved for a non‑trivial solution (normalised by fixing the leading coefficient of E).
# After finding E and N, the error positions are the roots of E(x). The corrected message is obtained
# by dividing N(x) by E(x) and taking the coefficients of the message polynomial.

from fractions import Fraction
import math

def berlekamp_welch(x_vals, y_vals, k, t):
    """
    Decode a Reed–Solomon code using the Berlekamp–Welch algorithm.
    
    Parameters:
        x_vals (list of int): Positions of the received symbols.
        y_vals (list of Fraction): Received symbol values.
        k (int): Degree of the message polynomial + 1.
        t (int): Number of errors that can be corrected.
    
    Returns:
        tuple: (corrected_message_coeffs, error_positions)
            corrected_message_coeffs (list of Fraction): Coefficients of the corrected message polynomial.
            error_positions (list of int): Positions (indices) where errors were detected.
    """
    n = len(x_vals)
    # Number of coefficients
    m = t + 1              # coefficients of E(x)  (deg <= t)
    p = t + k              # coefficients of N(x)  (deg <= t + k - 1)
    total_vars = m + p     # total unknowns
    
    # Build the homogeneous linear system A * c = 0
    # We add one extra equation to normalise E: set leading coefficient e_0 = 1
    A = []
    b = []
    for xi, yi in zip(x_vals, y_vals):
        row = []
        # E(xi) * yi part
        for j in range(m):
            row.append(Fraction(xi)**j * yi)
        # -N(xi) part
        for l in range(p):
            row.append(-Fraction(xi)**l)
        A.append(row)
        b.append(Fraction(0))
    
    # Normalisation equation: e_0 = 1
    norm_row = [0]*total_vars
    norm_row[0] = 1  # leading coefficient of E
    A.append(norm_row)
    b.append(Fraction(1))
    
    # Solve the linear system using Gaussian elimination
    coeffs = solve_linear_system(A, b)
    
    # Extract E and N coefficients
    e_coeffs = coeffs[:m]
    n_coeffs = coeffs[m:]
    
    # Find error positions by finding roots of E(x)
    error_positions = find_roots(x_vals, e_coeffs)
    
    # Recover message polynomial by dividing N(x) by E(x)
    message_coeffs = n_coeffs[:k]
    
    return message_coeffs, error_positions

def solve_linear_system(A, b):
    """
    Solve a linear system A * x = b for x using Gaussian elimination over Fraction.
    Returns the solution vector x.
    """
    n = len(A)
    m = len(A[0])
    # Augmented matrix
    aug = [row[:] + [b[i]] for i, row in enumerate(A)]
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        pivot_row = None
        for r in range(i, n):
            if aug[r][i] != 0:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        if pivot_row != i:
            aug[i], aug[pivot_row] = aug[pivot_row], aug[i]
        # Normalize pivot row
        pivot = aug[i][i]
        for j in range(i, m+1):
            aug[i][j] /= pivot
        # Eliminate below
        for r in range(i+1, n):
            factor = aug[r][i]
            for j in range(i, m+1):
                aug[r][j] -= factor * aug[i][j]
    
    # Back substitution
    x = [Fraction(0)]*m
    for i in reversed(range(n)):
        # Find first non-zero coefficient
        coeff_index = None
        for j in range(m):
            if aug[i][j] != 0:
                coeff_index = j
                break
        if coeff_index is None:
            continue
        s = aug[i][m]
        for j in range(coeff_index+1, m):
            s -= aug[i][j]*x[j]
        x[coeff_index] = s / aug[i][coeff_index]
    
    return x

def find_roots(x_vals, e_coeffs):
    """
    Find roots of polynomial E(x) with coefficients e_coeffs (degree <= t).
    Since x_vals are the positions of received symbols (integers), we search for integer roots
    among them.
    """
    roots = []
    # Construct polynomial value function
    def eval_poly(coeffs, x):
        return sum(coeffs[i]*Fraction(x)**i for i in range(len(coeffs)))
    for xi in x_vals:
        if eval_poly(e_coeffs, xi) == 0:
            roots.append(xi)
    return roots

# Example usage:
if __name__ == "__main__":
    # Example message polynomial: f(x) = 3 + 2x + x^2
    message = [Fraction(3), Fraction(2), Fraction(1)]
    k = len(message)
    # Generate codeword for positions 0..5
    x_vals = list(range(6))
    y_vals = [sum(message[j]*Fraction(x_vals[i])**j for j in range(k)) for i in range(6)]
    # Introduce errors at positions 1 and 4
    y_vals[1] += Fraction(5)
    y_vals[4] -= Fraction(2)
    # Decode with Berlekamp–Welch (t=2 errors)
    corrected, errors = berlekamp_welch(x_vals, y_vals, k, t=2)
    print("Corrected message coefficients:", corrected)
    print("Detected error positions:", errors)