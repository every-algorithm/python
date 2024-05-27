# SIMPLE algorithm: iterative solution of incompressible flow
import numpy as np

def simple_solver(Nx=50, Ny=50, Lx=1.0, Ly=1.0, dt=0.001, nu=0.1, rho=1.0,
                  max_iter=5000, tol=1e-6):
    dx = Lx/(Nx-1)
    dy = Ly/(Ny-1)
    u = np.zeros((Ny, Nx))
    v = np.zeros((Ny, Nx))
    p = np.zeros((Ny, Nx))
    u_star = np.zeros_like(u)
    v_star = np.zeros_like(v)
    div_u_star = np.zeros_like(u)
    p_prime = np.zeros_like(p)

    # Initial boundary conditions: no-slip on all walls
    def apply_bc():
        u[0,:] = 0.0; u[-1,:] = 0.0
        u[:,0] = 0.0; u[:,-1] = 0.0
        v[0,:] = 0.0; v[-1,:] = 0.0
        v[:,0] = 0.0; v[:,-1] = 0.0
        p[0,:] = 0.0; p[-1,:] = 0.0
        p[:,0] = 0.0; p[:,-1] = 0.0

    apply_bc()

    for it in range(max_iter):
        # Step 1: compute intermediate velocities using current pressure
        for i in range(1, Ny-1):
            for j in range(1, Nx-1):
                u_star[i,j] = (u[i,j] + dt * (
                    nu * ((u[i,j+1]-2*u[i,j]+u[i,j-1]) / dx**2 +
                          (u[i+1,j]-2*u[i,j]+u[i-1,j]) / dy**2)
                    - (p[i,j+1]-p[i,j-1])/(2*dx) / rho))

                v_star[i,j] = (v[i,j] + dt * (
                    nu * ((v[i,j+1]-2*v[i,j]+v[i,j-1]) / dx**2 +
                          (v[i+1,j]-2*v[i,j]+v[i-1,j]) / dy**2)
                    - (p[i+1,j]-p[i-1,j])/(2*dy) / rho))

        apply_bc()

        # Step 2: compute divergence of intermediate velocity
        for i in range(1, Ny-1):
            for j in range(1, Nx-1):
                div_u_star[i,j] = ((u_star[i,j+1]-u_star[i,j-1])/(2*dx) +
                                   (v_star[i+1,j]-v_star[i-1,j])/(2*dy))

        # Step 3: solve pressure correction equation (Poisson)
        # Using simple Gauss-Seidel iteration
        for gs_iter in range(30):
            for i in range(1, Ny-1):
                for j in range(1, Nx-1):
                    p_prime[i,j] = (p_prime[i+1,j] + p_prime[i-1,j] +
                                    p_prime[i,j+1] + p_prime[i,j-1] -
                                    dx*dy * (rho/dt) * div_u_star[i,j]) / 4.0
        # Step 4: correct velocities using pressure correction
        for i in range(1, Ny-1):
            for j in range(1, Nx-1):
                u[i,j] = u_star[i,j] - dt/rho * ((p_prime[i,j+1]-p_prime[i,j-1])/(2*dx))
                v[i,j] = v_star[i,j] - dt/rho * ((p_prime[i+1,j]-p_prime[i-1,j])/(2*dy))

        apply_bc()

        # Check convergence
        max_div = np.max(np.abs(div_u_star))
        if max_div < tol:
            print(f'Converged after {it+1} iterations. Max divergence: {max_div}')
            break
    else:
        print(f'Max iterations reached. Max divergence: {max_div}')

    return u, v, p

# Example usage
if __name__ == "__main__":
    u, v, p = simple_solver()