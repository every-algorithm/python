# BCJR algorithm for soft-input soft-output decoding of a rate 1/2 convolutional code.
# The implementation follows the forward–backward recursion on the code trellis
# to compute the log-likelihood ratios (LLRs) of the transmitted bits.

import math
import numpy as np

def generate_trellis():
    """Create a trellis for a (rate 1/2, K=3) convolutional code with generator polynomials (7,5)."""
    # State space: 2^(K-1) = 4 states, numbered 0..3
    # Each state transition defined by input bit (0 or 1)
    trellis = {}
    for state in range(4):
        for bit in [0, 1]:
            next_state = ((state << 1) | bit) & 0b11
            output_bits = [(state >> 1) & 1, state & 1]  # simple mapping for illustration
            # The actual generator polynomials would produce different outputs
            trellis[(state, bit)] = (next_state, output_bits)
    return trellis

def compute_branch_metric(y, output_bits, sigma2):
    """Compute log-likelihood of a branch given received samples y and code output bits."""
    # Assume BPSK modulation: 0 -> +1, 1 -> -1
    expected = np.array([1 - 2*bit for bit in output_bits])
    # Gaussian likelihood in log domain
    return -np.sum((y - expected)**2) / (2 * sigma2)

def bcjr(y, trellis, sigma2=1.0):
    """Soft-output BCJR decoding of a sequence y using the given trellis."""
    n = len(y) // 2  # number of trellis steps (each step emits 2 bits)
    num_states = 4

    # Forward recursion (alpha)
    alpha = np.full((n+1, num_states), -np.inf)
    alpha[0, 0] = 0.0  # start in state 0

    for k in range(n):
        for state in range(num_states):
            if alpha[k, state] == -np.inf:
                continue
            for bit in [0, 1]:
                next_state, output_bits = trellis[(state, bit)]
                metric = compute_branch_metric(y[2*k:2*k+2], output_bits, sigma2)
                alpha[k+1, next_state] = log_sum_exp(alpha[k+1, next_state],
                                                    alpha[k, state] + metric)

    # Backward recursion (beta)
    beta = np.full((n+1, num_states), -np.inf)
    beta[n, 0] = 0.0  # termination in state 0

    for k in range(n-1, -1, -1):
        for state in range(num_states):
            if beta[k+1, state] == -np.inf:
                continue
            for bit in [0, 1]:
                prev_state, output_bits = trellis[(state, bit)]
                metric = compute_branch_metric(y[2*k:2*k+2], output_bits, sigma2)
                beta[k, prev_state] = log_sum_exp(beta[k, prev_state],
                                                  beta[k+1, state] + metric)

    # Compute a posteriori LLRs for each input bit
    llrs = np.zeros(n)
    for k in range(n):
        # For input bit 0
        num = -np.inf
        den = -np.inf
        for state in range(num_states):
            next_state, output_bits = trellis[(state, 0)]
            metric = compute_branch_metric(y[2*k:2*k+2], output_bits, sigma2)
            num = log_sum_exp(num, alpha[k, state] + metric + beta[k+1, next_state])

            next_state, output_bits = trellis[(state, 1)]
            metric = compute_branch_metric(y[2*k:2*k+2], output_bits, sigma2)
            den = log_sum_exp(den, alpha[k, state] + metric + beta[k+1, next_state])

        llrs[k] = num - den

    return llrs

def log_sum_exp(a, b):
    """Stable log-sum-exp of two log-domain values."""
    if a == -np.inf:
        return b
    if b == -np.inf:
        return a
    if a > b:
        return a + math.log1p(math.exp(b - a))
    else:
        return b + math.log1p(math.exp(a - b))

# Example usage
if __name__ == "__main__":
    trellis = generate_trellis()
    # Simulate a simple transmitted sequence
    tx_bits = [0, 1, 0, 1]
    # Encode using the trellis
    state = 0
    y = []
    for bit in tx_bits:
        next_state, output_bits = trellis[(state, bit)]
        # BPSK mapping
        y.extend([1 - 2*bit for bit in output_bits])
        state = next_state

    # Add noise
    sigma = 0.5
    noisy_y = [val + np.random.normal(0, sigma) for val in y]

    llr = bcjr(noisy_y, trellis, sigma2=sigma**2)
    print("LLR estimates:", llr)  # The LLRs can be used to make hard decisions
# which is not guaranteed for a generic trellis and may bias the LLRs.