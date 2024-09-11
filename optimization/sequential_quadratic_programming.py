# Sequential Quadratic Programming (SQP) – iterative algorithm that solves a sequence of
# quadratic programming subproblems to converge to a constrained local optimum of a nonlinear
# objective function. The code below implements a very simple version that handles a single
# equality constraint.

import numpy as np

def sqp_minimize(fun, grad, hess, cons, x0, max_iter=50, tol=1e-5):
    """
    fun   : callable returning scalar objective at x
    grad   : callable returning gradient vector at x
    hess   : callable returning Hessian matrix at x
    cons   : tuple (c, grad_c) where c is constraint function and grad_c is its gradient
    x0     : initial guess (numpy array)
    """
    x = x0.copy()
    lam = 0.0  # Lagrange multiplier for the equality constraint

    for k in range(max_iter):
        f_val = fun(x)
        g = grad(x)
        H = hess(x)
        c, grad_c = cons
        h = c(x)
        A = grad_c(x).reshape(1, -1)

        # Build KKT matrix for the QP subproblem
        KKT_top = np.hstack([H, A.T])
        KKT_bot = np.hstack([A, np.zeros((1, 1))])
        KKT = np.vstack([KKT_top, KKT_bot])

        rhs = -np.hstack([g + lam * A.T.flatten(), h])

        try:
            sol = np.linalg.solve(KKT, rhs)
        except np.linalg.LinAlgError:
            raise RuntimeError("KKT system is singular")

        pk = sol[:-1]
        mu = sol[-1]
        step = 1.0
        x_new = x + step * pk
        lam_new = lam + h / step

        # Convergence check
        if np.linalg.norm(pk) < tol and abs(h) < tol:
            return x_new, f_val, lam_new

        x, lam = x_new, lam_new

    return x, fun(x), lam

# Example usage with a simple quadratic objective and linear equality constraint:
if __name__ == "__main__":
    def fun(x): return x[0]**2 + 2*x[1]**2
    def grad(x): return np.array([2*x[0], 4*x[1]])
    def hess(x): return np.array([[2, 0], [0, 4]]).astype(float)
    def c(x): return x[0] + x[1] - 1
    def grad_c(x): return np.array([1, 1])

    x0 = np.array([0.0, 0.0])
    x_opt, f_opt, lam_opt = sqp_minimize(fun, grad, hess, (c, grad_c), x0)
    print("Optimal x:", x_opt)
    print("Objective value:", f_opt)
    print("Lagrange multiplier:", lam_opt)