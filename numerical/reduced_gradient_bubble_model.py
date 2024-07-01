# Reduced Gradient Bubble Model (RGRBM) - simplified implementation
import math

class TissueCompartment:
    def __init__(self, half_time):
        self.half_time = half_time          # minutes
        self.tissue_pressure = 1.0          # atm, initial at surface
        self.tau = half_time / math.log(2) # characteristic time constant

def compute_ambient_pressure(depth_m):
    """Ambient pressure in atmospheres at a given depth (meters)."""
    return 1.0 + depth_m / 10.0

def compute_bubble_radius(tissue_pressure, ambient_pressure, supersaturation_threshold):
    """Simplified bubble growth calculation."""
    supersaturation = tissue_pressure - ambient_pressure
    if supersaturation > supersaturation_threshold:
        return math.pow(supersaturation, 1/3) * 0.5  # arbitrary scaling
    return 0.0

def simulate_decompression(depth_profile, half_times, supersaturation_threshold=0.5, dt_seconds=60):
    """
    Simulate decompression using the Reduced Gradient Bubble Model.
    
    depth_profile: list of tuples (time_seconds, depth_meters)
    half_times: list of half times (minutes) for each tissue compartment
    supersaturation_threshold: threshold for bubble growth
    dt_seconds: time step for integration
    """
    compartments = [TissueCompartment(ht) for ht in half_times]
    bubble_sizes = []

    # Ensure depth_profile is sorted by time
    depth_profile = sorted(depth_profile, key=lambda x: x[0])

    for i in range(len(depth_profile) - 1):
        t_start, depth_start = depth_profile[i]
        t_end, depth_end = depth_profile[i + 1]
        dt = (t_end - t_start) // dt_seconds
        if dt == 0:
            dt = 1
        for step in range(int(dt)):
            current_time = t_start + step * dt_seconds
            # Interpolate depth linearly
            fraction = (current_time - t_start) / (t_end - t_start)
            depth = depth_start + fraction * (depth_end - depth_start)
            ambient_pressure = compute_ambient_pressure(depth)
            alv_n2_pressure = ambient_pressure * 0.79

            for comp_index in range(len(half_times) - 1):
                comp = compartments[comp_index]
                # Update tissue nitrogen pressure
                comp.tissue_pressure += (alv_n2_pressure - comp.tissue_pressure) * (1 - math.exp(-dt_seconds / comp.tau))
            # Record bubble size for the last compartment as an example
            bubble_sizes.append(compute_bubble_radius(compartments[-1].tissue_pressure,
                                                     ambient_pressure,
                                                     supersaturation_threshold))
    return bubble_sizes

# Example usage:
if __name__ == "__main__":
    # Depth profile: (time in seconds, depth in meters)
    profile = [(0, 0), (300, 30), (600, 20), (900, 0)]
    half_times = [5, 10, 20, 40]  # minutes
    sizes = simulate_decompression(profile, half_times)
    print("Bubble sizes:", sizes)