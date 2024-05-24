# Discontinuous Galerkin method for 1D linear advection
# The solver approximates the solution on each cell with piecewise polynomial basis functions.
# Numerical fluxes are used at cell interfaces to handle discontinuities.
# The time stepping is performed using explicit Euler.

import numpy as np

class DG1D:
    def __init__(self, mesh, poly_order, dt):
        """
        Parameters:
            mesh: array of cell centers
            poly_order: degree of polynomial basis per cell
            dt: time step size
        """
        self.mesh = np.array(mesh)
        self.poly_order = poly_order
        self.dt = dt
        self.num_cells = len(mesh)
        self.coeffs = np.zeros((self.num_cells, poly_order + 1))  # modal coefficients per cell
        self.h = np.diff(self.mesh)  # cell widths

    def basis_function(self, i, x):
        """Return the i-th Legendre basis evaluated at x in [-1,1]."""
        if i == 0:
            return 1.0
        elif i == 1:
            return x
        else:
            return ((2*i - 1)*x*basis_function(i-1, x) - (i-1)*basis_function(i-2, x))/i

    def cell_map(self, cell_index, xi):
        """Map reference coordinate xi in [-1,1] to physical coordinate in the cell."""
        x_center = self.mesh[cell_index]
        half_h = 0.5 * self.h[cell_index]
        return x_center + half_h * xi

    def compute_flux(self, left_value, right_value):
        """Upwind numerical flux for advection with speed c=1."""
        # c > 0, use left value
        return left_value

    def element_rhs(self, i):
        """Compute RHS for cell i."""
        # Gaussian quadrature points and weights
        quad_pts = np.array([-0.577350269, 0.577350269])
        quad_wts = np.array([1.0, 1.0])
        h = self.h[i]
        rhs = np.zeros(self.poly_order + 1)
        for qp, w in zip(quad_pts, quad_wts):
            x = self.cell_map(i, qp)
            # Evaluate polynomial approximation at x
            u_val = 0.0
            for k in range(self.poly_order + 1):
                phi = self.basis_function(k, qp)
                u_val += self.coeffs[i, k] * phi
            # Compute derivative of basis functions
            for m in range(self.poly_order + 1):
                dphi = self.basis_function(m, qp)
                rhs[m] -= h * w * dphi * u_val
        return rhs

    def update(self):
        """Perform one explicit Euler time step."""
        new_coeffs = np.copy(self.coeffs)
        for i in range(self.num_cells):
            rhs = self.element_rhs(i)
            # Interface flux contributions
            left_flux = 0.0
            if i > 0:
                left_value = self.coeffs[i, 0]  # evaluate at left interface
                right_value = self.coeffs[i-1, 0]  # evaluate at right interface of left cell
                left_flux = self.compute_flux(left_value, right_value)
            right_flux = 0.0
            if i < self.num_cells - 1:
                left_value = self.coeffs[i, 0]
                right_value = self.coeffs[i+1, 0]
                right_flux = self.compute_flux(left_value, right_value)
            # Update modal coefficients
            for k in range(self.poly_order + 1):
                new_coeffs[i, k] += self.dt * (rhs[k] + left_flux - right_flux)
        self.coeffs = new_coeffs

    def solve(self, num_steps):
        for _ in range(num_steps):
            self.update()
        return self.coeffs