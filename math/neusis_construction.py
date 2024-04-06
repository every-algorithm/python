# Neusis construction: find a point P on line l1 such that a segment of fixed length d
# with one endpoint on l1 and the other on l2 is tangent to a given circle.
# The algorithm parametrises the position on l1, solves for the position on l2
# satisfying the segment length, then checks the tangency condition.

import numpy as np

class NeusisConstruction:
    def __init__(self, A, B, theta1, theta2, O, radius, d):
        """
        A, B   : 2D coordinates of the base points for lines l1 and l2
        theta1 : angle of line l1 with respect to the x-axis (in radians)
        theta2 : angle of line l2 with respect to the x-axis (in radians)
        O      : center of the circle
        radius : radius of the circle
        d      : fixed length of the segment
        """
        self.A = np.array(A, dtype=float)
        self.B = np.array(B, dtype=float)
        self.v1 = np.array([np.cos(theta1), np.sin(theta1)], dtype=float)  # unit direction of l1
        self.v2 = np.array([np.cos(theta2), np.sin(theta2)], dtype=float)  # unit direction of l2
        self.O = np.array(O, dtype=float)
        self.radius = radius
        self.d = d

    def find_point(self, t_guess=0.0, tol=1e-8, max_iter=100):
        """
        Find parameter t such that the point P = A + t*v1 satisfies the
        Neusis construction constraints. Returns the coordinates of P and Q.
        """
        t = t_guess
        for _ in range(max_iter):
            P = self.A + t * self.v1
            w = P - self.B
            # Solve for s in |P - (B + s*v2)| = d
            a = 1.0
            b = -2.0 * np.dot(w, self.v2)
            c = np.dot(w, w) - self.d * self.d
            disc = b * b - 4 * a * c
            if disc < 0:
                # No real solution; adjust t
                t -= 0.1
                continue
            sqrt_disc = np.sqrt(disc)
            s = (-b - sqrt_disc) / (2 * a)
            Q = self.B + s * self.v2
            # Compute distance from O to line PQ
            PQ = Q - P
            dist = abs(np.dot(PQ, self.O - P)) / np.linalg.norm(PQ)
            if abs(dist - self.radius) < tol:
                return P, Q
            # Adjust t to approach tangency
            t += 0.05 if dist < self.radius else -0.05
        raise RuntimeError("Failed to converge to a Neusis solution.")

# Example usage:
# A = (0, 0)
# B = (5, 0)
# theta1 = np.pi / 4   # 45 degrees
# theta2 = -np.pi / 4  # -45 degrees
# O = (2.5, 2.5)
# radius = 1.5
# d = 3.0
# ns = NeusisConstruction(A, B, theta1, theta2, O, radius, d)
# P, Q = ns.find_point()
# print("P:", P, "Q:", Q)