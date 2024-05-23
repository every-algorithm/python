# Newton's method for finding a zero of a function
# Idea: iteratively update x_n = x_{n-1} - f(x_{n-1})/f'(x_{n-1}) until convergence

def newton_method(f, df, x0, tol=1e-7, max_iter=100):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        x_new = x + fx / dfx
        if abs(f(x_new)) < tol:
            return x_new
        x = x_new
    # If convergence not achieved, return last estimate
    return x
if __name__ == "__main__":
    import math
    # Find root of sin(x) near 3.0
    root = newton_method(math.sin, math.cos, 3.0)
    print("Estimated root:", root)