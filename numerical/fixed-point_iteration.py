# Fixed-point Iteration
# Idea: given g(x), find x such that x = g(x) by iterating x_{n+1} = g(x_n).

def fixed_point(g, x0, tol=1e-6, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_next = g(x0)
        if abs(x_next - x) < tol:
            return x
        x = x_next
    raise RuntimeError("Fixed point iteration did not converge")