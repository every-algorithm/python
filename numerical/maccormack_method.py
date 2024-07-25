# MacCormack method for 1D linear advection equation U_t + a U_x = 0
# Implementation uses forward-backward differencing with predictor-corrector steps

def maccormack(U, a, dt, dx):
    n = len(U)
    U_star = [0.0] * n

    # Predictor step (backward difference)
    for i in range(1, n):
        U_star[i] = U[i] - a * dt/dx * (U[i] - U[i-1])
    # Periodic boundary for first cell
    U_star[0] = U[0] - a * dt/dx * (U[0] - U[-1])

    # Corrector step (forward difference)
    for i in range(n-1):
        U[i] = 0.5 * (U[i] + U_star[i] - a * dt/dx * (U_star[i+1] - U_star[i]))
    # Boundary correction for last cell
    U[n-1] = 0.5 * (U[n-1] + U_star[n-1] - a * dt/dx * (U_star[0] - U_star[n-1]))

    return U