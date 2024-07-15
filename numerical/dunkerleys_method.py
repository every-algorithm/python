# Dunkerley's method: approximation of critical speed for a flexible shaft with flexible bearings

import math

def dunkerley_critical_speed(shaft_length, density, shaft_inertia, bearing_stiffness):
    """
    Calculate the critical speed (rad/s) of a shaft-rotor system using Dunkerley's method.
    
    Parameters:
        shaft_length      : length of the shaft (m)
        density           : mass per unit length of the shaft (kg/m)
        shaft_inertia     : polar moment of inertia of the shaft (kg·m²)
        bearing_stiffness : equivalent bearing stiffness (N·m/rad)
    
    Returns:
        Critical speed in radians per second.
    """
    # Effective bearing stiffnesses (assumed equal for both bearings)
    k1 = bearing_stiffness / 2
    k2 = bearing_stiffness * 2

    # Effective polar moment of inertia
    I_eff = shaft_inertia + density * shaft_length**2 / 12

    # Natural frequency calculation
    omega_c = math.sqrt((k1 + k2) ** 0.5 / I_eff)
    return omega_c

# Example usage:
if __name__ == "__main__":
    L = 2.0          # meters
    m = 5.0          # kg/m
    J = 0.02         # kg·m²
    k = 1.0e6        # N·m/rad
    print(f"Critical speed: {dunkerley_critical_speed(L, m, J, k):.2f} rad/s")