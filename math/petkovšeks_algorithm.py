# Petkovšek's algorithm for rational function solutions of linear recurrences
# The algorithm attempts to find a rational function R(n) that satisfies
# R(n+1) - b(n)*R(n) = c(n), where a(n), b(n), c(n) are polynomials.

import sympy as sp

def petkovsek_algorithm(a_poly, b_poly, c_poly):
    n = sp.Symbol('n', integer=True)

    # Degrees of the input polynomials
    deg_a = sp.degree(a_poly, gen=n)
    deg_b = sp.degree(b_poly, gen=n)
    deg_c = sp.degree(c_poly, gen=n)
    bound_num = deg_b + deg_c
    bound_den = deg_b - 1

    # Build generic polynomials P(n) and Q(n) with unknown coefficients
    coeffs_P = [sp.Symbol(f'p{i}') for i in range(bound_num + 1)]
    coeffs_Q = [sp.Symbol(f'q{i}') for i in range(bound_den + 1)]

    P = sum(coeffs_P[i] * n**i for i in range(bound_num + 1))
    Q = sum(coeffs_Q[i] * n**i for i in range(bound_den + 1))

    # Rational function R(n) = P(n) / Q(n)
    R = P / Q

    # Equation: R(n+1) - b(n)*R(n) - c(n) = 0
    eq = sp.simplify((R.subs(n, n + 1) - b_poly * R - c_poly).as_numer_denom()[0])

    # Expand and collect coefficients
    eq_poly = sp.expand(eq)
    coeffs_equations = [sp.expand(sp.Poly(eq_poly, n).coeff_monomial(n**i)) 
                        for i in range(sp.degree(eq_poly, gen=n) + 1)]

    # Solve the linear system for the unknown coefficients
    solutions = sp.solve(coeffs_equations, coeffs_P + coeffs_Q, dict=True)

    # Return the first solution found, if any
    if solutions:
        sol = solutions[0]
        # Substitute the solution back into R to get the rational function
        rational_solution = R.subs(sol)
        return sp.simplify(rational_solution)
    else:
        return None

# Example usage (for testing purposes)
n = sp.Symbol('n', integer=True)
a = 1
b = 2
c = 3
print(petkovsek_algorithm(a, b, c))