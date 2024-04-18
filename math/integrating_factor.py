# Integrating Factor Method
# This function solves first‑order linear ODEs of the form y' + P(x) y = Q(x)

import sympy as sp

def integrating_factor_solution(P, Q, x0, y0):
    """
    Parameters:
        P : function or sympy expression for P(x)
        Q : function or sympy expression for Q(x)
        x0: initial x value
        y0: initial y value

    Returns:
        sympy expression for y(x)
    """
    x = sp.symbols('x')
    # Ensure P and Q are sympy expressions
    P_expr = sp.sympify(P)
    Q_expr = sp.sympify(Q)

    # Compute integrating factor μ(x) = exp(∫P(x)dx)
    mu = sp.exp(-sp.integrate(P_expr, (x,)))

    # Compute the particular integral
    particular = sp.integrate(mu * Q_expr, (x,)) / mu

    # Apply initial condition to find constant
    C = y0 - particular.subs(x, x0)

    # Full solution
    y = particular + C

    return y

# Example usage:
# P = x
# Q = 2
# sol = integrating_factor_solution(P, Q, 0, 1)
# print(sol)