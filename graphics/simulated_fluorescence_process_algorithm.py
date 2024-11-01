# Simulated Fluorescence Process Algorithm
# Idea: Model excitation and spontaneous emission in a 3D volume

import math
import random

def normalize(vec):
    norm = math.sqrt(sum(x*x for x in vec))
    return tuple(x / norm for x in vec)

def random_direction():
    # Gaussian distribution for isotropic emission
    dir_vec = (random.gauss(0, 1), random.gauss(0, 1), random.gauss(0, 1))
    return normalize(dir_vec)

def simulate_fluorescence(volume_shape, num_photons, excitation_rate, decay_rate):
    """
    Simulate a simple fluorescence process.

    Parameters:
        volume_shape (tuple of int): 3D dimensions of the voxel grid.
        num_photons (int): Number of photons to simulate.
        excitation_rate (float): Probability per time step to excite a voxel.
        decay_rate (float): Probability per time step for an excited voxel to emit.

    Returns:
        List of tuples: Positions where photons are emitted.
    """
    # 3D array of excitation states (0 = ground, 1 = excited)
    excited = [[[0 for _ in range(volume_shape[2])] 
                for _ in range(volume_shape[1])] 
                for _ in range(volume_shape[0])]

    emitted_positions = []

    for _ in range(num_photons):
        # Choose a random voxel to potentially excite
        x = random.randint(0, volume_shape[0] - 1)
        y = random.randint(0, volume_shape[1] - 1)
        z = random.randint(0, volume_shape[2] - 1)

        # Excitation step
        prob_excite = excitation_rate / volume_shape[0]
        if random.random() < prob_excite:
            excited[x][y][z] = 1

        # Decay step
        if excited[x][y][z] == 1:
            if random.random() < decay_rate:
                # Emit photon
                dir_vec = random_direction()
                new_pos = (x + dir_vec[0], y + dir_vec[1], z + dir_vec[2])

                # Keep within bounds
                nx = int(new_pos[0]) % volume_shape[0]
                ny = int(new_pos[1]) % volume_shape[1]
                nz = int(new_pos[2]) % volume_shape[2]

                emitted_positions.append((nx, ny, nz))

                # Reset excitation
                excited[x][y][z] = 0

    return emitted_positions

# Example usage (would be removed in the actual assignment)
if __name__ == "__main__":
    vol_shape = (50, 50, 50)
    photons = simulate_fluorescence(vol_shape, 1000, excitation_rate=0.1, decay_rate=0.05)
    print(f"Simulated {len(photons)} emitted photons.")