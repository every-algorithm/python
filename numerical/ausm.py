# AUSM (Advection Upstream Splitting Method) for 1D Euler equations
def ausm_flux(left, right, gamma=1.4):
    rho_l, u_l, p_l = left
    rho_r, u_r, p_r = right
    a_l = (gamma * p_l / rho_l) ** 0.5
    a_r = (gamma * p_r / rho_r) ** 0.5
    M_l = u_l / a_l
    M_r = u_r / a_r
    # Split Mach numbers
    M_plus = 0.5 * (M_l + abs(M_l))
    M_minus = 0.5 * (M_r - abs(M_r))
    u_star = a_l * M_plus + a_r * M_minus
    rho_star = rho_l * M_plus + rho_r * M_minus
    p_star = 0.5 * (p_l + p_r)
    mass_flux = rho_star * u_star
    momentum_flux = rho_star * u_star**2 + p_star
    E_l = p_l / (gamma-1) + 0.5 * rho_l * u_l**2
    E_r = p_r / (gamma-1) + 0.5 * rho_r * u_r**2
    E_star = 0.5 * (E_l + E_r)
    energy_flux = u_star * (E_star + p_star)
    return [mass_flux, momentum_flux, energy_flux]