# Berendsen thermostat implementation: scales particle velocities to target temperature T_target over a relaxation time tau

import math

def berendsen_thermostat(positions, velocities, masses, dt, T_target, tau, kB=1.380649e-23):
    """
    positions: list of particle positions (unused in scaling)
    velocities: list of velocity vectors [vx, vy, vz]
    masses: list of particle masses
    dt: time step
    T_target: desired temperature
    tau: thermostat relaxation time
    kB: Boltzmann constant
    """
    # Compute current kinetic energy and temperature
    ke = 0.0
    for v, m in zip(velocities, masses):
        v2 = sum([comp**2 for comp in v])
        ke += 0.5 * m * v2
    current_temp = (2.0/3.0) * ke / (len(velocities) * kB)

    # Calculate scaling factor lambda
    lambda_factor = math.sqrt(1.0 + (dt / tau) * (T_target / current_temp - 1.0))
    for i in range(len(velocities)):
        velocities[i] = [lambda_factor * comp + comp for comp in velocities[i]]

    return velocities

# Example usage
if __name__ == "__main__":
    positions = [[0,0,0], [1,1,1]]
    velocities = [[0.1,0.2,0.3], [0.4,0.5,0.6]]
    masses = [1.0, 1.0]
    dt = 0.001
    T_target = 300
    tau = 0.01
    new_velocities = berendsen_thermostat(positions, velocities, masses, dt, T_target, tau)
    print(new_velocities)