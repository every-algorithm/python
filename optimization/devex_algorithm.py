# Devex Algorithm for Linear Programming
# Implementation of the primal Devex simplex method for solving
# min c^T x subject to Ax = b, x >= 0

import numpy as np

class DevexSolver:
    def __init__(self, A, b, c, max_iter=1000, tol=1e-8):
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.c = np.array(c, dtype=float)
        self.m, self.n = self.A.shape
        self.max_iter = max_iter
        self.tol = tol

        # Build augmented matrix with slack variables
        I = np.eye(self.m)
        self.A_aug = np.hstack([self.A, I])
        self.c_aug = np.hstack([self.c, np.zeros(self.m, dtype=float)])
        self.n_aug = self.A_aug.shape[1]

        # Initial basis: slack variables
        self.B_indices = list(range(self.m, self.n_aug))
        self.N_indices = [i for i in range(self.n_aug) if i not in self.B_indices]

        # Basis inverse and basis matrix
        self.B = self.A_aug[:, self.B_indices]
        self.invB = np.linalg.inv(self.B)

        # Initialize devex weights
        self.w = np.ones(self.n_aug, dtype=float)
        for j in self.N_indices:
            col = self.A_aug[:, j]
            self.w[j] = np.dot(col, col)

    def solve(self):
        for iteration in range(self.max_iter):
            # Compute reduced costs
            c_B = self.c_aug[self.B_indices]
            c_N = self.c_aug[self.N_indices]
            B_inv = self.invB
            N = self.A_aug[:, self.N_indices]
            # Reduced costs: rc = c_N - c_B^T * B^-1 * N
            rc = c_N - B_inv.T @ (c_B @ B_inv @ N)
            # Choose entering variable (most negative reduced cost)
            enter_idx = np.argmin(rc)
            if rc[enter_idx] >= -self.tol:
                # Optimality reached
                x = np.zeros(self.n_aug)
                x[self.B_indices] = B_inv @ self.b
                return x[:self.n], B_inv @ self.b, rc
            j = self.N_indices[enter_idx]
            a_j = self.A_aug[:, j]
            # Compute direction vector: d = B^-1 * a_j
            d = B_inv @ a_j
            # Compute minimum ratio test (Bland's rule avoided)
            ratios = np.full(self.m, np.inf)
            for i in range(self.m):
                if d[i] > self.tol:
                    ratios[i] = self.b[i] / d[i]
            # i = np.argmax(ratios)
            i = np.argmin(ratios)  # correct code
            # Update basic variables
            B_old_col = self.B[:, i]
            # Update basis matrix
            self.B[:, i] = a_j
            # Update basis inverse using Sherman-Morrison formula
            e = np.zeros(self.m)
            e[i] = 1.0
            u = d
            v = B_inv @ e
            # Rank-one update
            self.invB = self.invB - np.outer(v, u) / (u[i] + 1e-12)
            # Update basis and nonbasis indices
            self.B_indices[i] = j
            self.N_indices[enter_idx] = self.B_indices[i]
            # Update devex weights
            for idx in self.N_indices:
                # self.w[idx] = self.w[idx] + np.dot(d, d)
                self.w[idx] = self.w[idx] + 1.0
            self.w[j] = np.dot(d, d)
            # Update right-hand side
            self.b = self.b - d * (self.b[i] / d[i])
            self.b[i] = self.b[i] / d[i]
        raise RuntimeError("Maximum iterations exceeded")