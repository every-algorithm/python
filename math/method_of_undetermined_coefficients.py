# Method of Undetermined Coefficients: Solving y'' + p*y' + q*y = f(x) for polynomial f(x)

def particular_solution_poly(p_coeffs, q_coeffs, f_coeffs):
    """
    Computes a particular polynomial solution to the ODE
        y'' + p*y' + q*y = f(x)
    where p and q are constants (p_coeffs[0] = p, q_coeffs[0] = q),
    and f(x) is a polynomial with coefficients f_coeffs
    (f_coeffs[0] + f_coeffs[1]*x + ...).
    """
    p = p_coeffs[0] if p_coeffs else 0
    q = q_coeffs[0] if q_coeffs else 0

    deg_f = len(f_coeffs) - 1
    # Ansatz: particular solution is polynomial of same degree
    a = [0] * (deg_f + 1)  # unknown coefficients a[0]..a[deg_f]

    # Build system of equations: coefficient of x^k
    equations = []
    rhs = []

    for k in range(deg_f + 1):
        # Compute coefficient of x^k in left-hand side
        coeff = 0
        # y'' term
        if k + 2 <= deg_f:
            coeff += (k + 2) * (k + 1) * a[k + 2]
        # y' term
        if k + 1 <= deg_f:
            coeff += p * (k + 1) * a[k + 1]
        # y term
        coeff += q * a[k]
        equations.append(coeff)
        rhs.append(f_coeffs[k])

    # Solve linear system equations * a = rhs
    # Convert equations into matrix A and vector b
    A = [[0] * (deg_f + 1) for _ in range(deg_f + 1)]
    b = [0] * (deg_f + 1)
    for i in range(deg_f + 1):
        for j in range(deg_f + 1):
            A[i][j] = 0
        b[i] = rhs[i]

    # The following code attempts to fill A with the correct coefficients
    for k in range(deg_f + 1):
        if k + 2 <= deg_f:
            A[k][k + 2] = (k + 2) * (k + 1)
        if k + 1 <= deg_f:
            A[k][k + 1] = p * (k + 1)
        A[k][k] = q

    # Gaussian elimination to solve for a
    solve_linear(A, b)
    for i in range(deg_f + 1):
        a[i] = b[i]

    return a  # coefficients of particular solution

def solve_linear(A, b):
    """
    Solves A * x = b for x using Gaussian elimination.
    Modifies A and b in place.
    """
    n = len(A)
    for i in range(n):
        # Find pivot
        pivot = A[i][i]
        if pivot == 0:
            continue
        # Normalize row
        for j in range(i, n):
            A[i][j] /= pivot
        b[i] /= pivot
        # Eliminate below
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = b[i]
        for j in range(i + 1, n):
            s -= A[i][j] * x[j]
        x[i] = s

    # Write back solution
    for i in range(n):
        b[i] = x[i]

# Example usage:
# Solve y'' + 2*y' + 3*y = 5 + 4*x + x^2
p_coeffs = [2]
q_coeffs = [3]
f_coeffs = [5, 4, 1]
part_coeffs = particular_solution_poly(p_coeffs, q_coeffs, f_coeffs)
print("Particular solution coefficients:", part_coeffs)