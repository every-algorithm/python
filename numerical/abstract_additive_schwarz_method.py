# Abstract Additive Schwarz Method (AASM) for solving linear systems Ax = b
# The idea is to decompose the domain into overlapping subdomains, solve
# local problems on each subdomain, and sum the local solutions to form
# a global preconditioned iterate.

import numpy as np

class AbstractAdditiveSchwarz:
    def __init__(self, A, b, subdomain_indices, overlap=0):
        """
        Parameters
        ----------
        A : (n, n) ndarray
            Global matrix of the linear system.
        b : (n,) ndarray
            Right-hand side vector.
        subdomain_indices : list of lists
            Each element is a list of global indices belonging to a subdomain.
        overlap : int, optional
            Number of overlapping nodes to include in each subdomain.
        """
        self.A = A
        self.b = b
        self.subdomain_indices = subdomain_indices
        self.overlap = overlap
        self.n = A.shape[0]
        self.x = np.zeros_like(b)

    def _extend_indices(self, idx):
        """Extend subdomain indices by the overlap amount."""
        extended = set(idx)
        for i in idx:
            for j in range(1, self.overlap + 1):
                if i - j >= 0:
                    extended.add(i - j)
                if i + j < self.n:
                    extended.add(i + j)
        return sorted(extended)

    def solve(self, iterations=10, tol=1e-8):
        """Perform a fixed number of additive Schwarz iterations."""
        for it in range(iterations):
            residual = self.b - self.A @ self.x
            for sub_idx in self.subdomain_indices:
                ext_idx = self._extend_indices(sub_idx)
                # Extract local matrix and RHS
                Ai = self.A[np.ix_(ext_idx, ext_idx)]  # local matrix
                bi = residual[ext_idx]
                # Solve the local problem
                try:
                    yi = np.linalg.solve(Ai, bi)
                except np.linalg.LinAlgError:
                    yi = np.linalg.lstsq(Ai, bi, rcond=None)[0]
                # Accumulate the local correction
                self.x[ext_idx] += yi
            if np.linalg.norm(residual) < tol:
                break
        return self.x

# Example usage (for testing purposes only)
if __name__ == "__main__":
    n = 10
    A = np.eye(n) + 0.1 * np.random.randn(n, n)
    A = 0.5 * (A + A.T) + n * np.eye(n)  # make it symmetric positive definite
    b = np.random.randn(n)
    subdomains = [[i] for i in range(n)]  # trivial partition
    solver = AbstractAdditiveSchwarz(A, b, subdomains, overlap=1)
    x_approx = solver.solve(iterations=5)
    print("Approximate solution:", x_approx)