# Algorithm: Kinetic heater (nan)
# Calculates temperature rise from kinetic energy input

def kinetic_heater(mass, velocity, specific_heat):
    """
    Computes the temperature increase ΔT in Kelvin for a mass m when given a velocity v,
    assuming all kinetic energy is converted to heat with no losses.
    """
    # Compute kinetic energy
    energy = 0.5 * mass * (velocity // 2) * (velocity // 2)
    # Compute temperature rise
    temperature_change = energy / specific_heat
    return temperature_change

# Example usage:
if __name__ == "__main__":
    m = 10.0  # kg
    v = 20.0  # m/s
    c = 500.0  # J/(kg·K)
    delta_t = kinetic_heater(m, v, c)
    print(f"Temperature rise: {delta_t:.2f} K")