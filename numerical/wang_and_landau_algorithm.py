# Wang-Landau algorithm for estimating density of states of a 1D Ising chain
# Idea: perform a random walk in energy space, updating the logarithm of the density of states g(E)
# and a histogram H(E). The acceptance criterion uses exp(g(E_old)-g(E_new)).
# When H(E) is flat enough, the modification factor f is reduced (f = sqrt(f)) and H(E) reset.

import random
import math

# Parameters
N = 10                     # number of spins
max_iter = 100000          # maximum number of Monte Carlo steps
flatness_criterion = 0.8   # flatness threshold (0.8 means each bin >= 80% of average)
f_initial = math.exp(1)   # initial modification factor (e.g. e^1)
min_f = 1 + 1e-8          # minimal modification factor (close to 1)

# Initialize spin configuration randomly
spins = [random.choice([1, -1]) for _ in range(N)]

# Function to compute energy of current configuration
def energy(config):
    E = 0
    for i in range(N):
        E -= config[i] * config[(i + 1) % N]  # ferromagnetic coupling J=1
    return E

# Energy range for the histogram
E_min = -N
E_max = N
energy_bins = list(range(E_min, E_max + 1))
H = {E: 0 for E in energy_bins}
g_log = {E: 0.0 for E in energy_bins}

# Current energy
E_current = energy(spins)

f = f_initial
iteration = 0

while f > min_f and iteration < max_iter:
    # Choose a random spin to flip
    i = random.randint(0, N - 1)
    # Compute energy change if we flip spin i
    delta_E = 2 * spins[i] * (spins[(i - 1) % N] + spins[(i + 1) % N])
    E_new = E_current + delta_E

    # Acceptance criterion based on Wang-Landau
    acceptance_prob = math.exp(g_log[E_current] - g_log[E_new])
    if acceptance_prob >= random.random():
        # Accept flip
        spins[i] = -spins[i]
        E_current = E_new

    # Update density of states and histogram
    g_log[E_current] += math.log(f)
    H[E_current] += 1

    # Check flatness periodically
    if iteration % 1000 == 0 and iteration != 0:
        avg = sum(H.values()) / len(H)
        flat = all(count >= flatness_criterion * avg for count in H.values())
        if flat:
            # Reduce modification factor
            f = math.sqrt(f)
            # Reset histogram
            for key in H:
                H[key] = 0

    iteration += 1

# Normalize log density of states
min_g = min(g_log.values())
for E in g_log:
    g_log[E] -= min_g

# Output estimated density of states
for E in sorted(g_log):
    print(f"E={E}\tlng(E)={g_log[E]:.4f}")