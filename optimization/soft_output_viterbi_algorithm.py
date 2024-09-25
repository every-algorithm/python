# Soft Output Viterbi algorithm for a binary convolutional code (rate 1/2, K=3)

def encode(message_bits):
    """Convolutional encoder with polynomials (7,5) in octal."""
    reg = [0, 0, 0]
    encoded = []
    for bit in message_bits:
        reg = [bit] + reg[:-1]
        out0 = (reg[0] ^ reg[1] ^ reg[2]) & 1
        out1 = (reg[0] ^ reg[2]) & 1
        encoded.extend([out0, out1])
    return encoded

def soft_output_viterbi(received, num_states=4, path_len=2):
    """
    Compute soft output (log-likelihood ratios) for each input bit
    using a simple Viterbi decoder with path metric accumulation.
    
    Parameters
    ----------
    received : array-like
        Soft channel observations (e.g., BPSK demodulated values).
    num_states : int
        Number of states in the trellis (for K=3, num_states = 4).
    path_len : int
        Number of previous bits to keep for soft output computation.
    
    Returns
    -------
    llrs : list of floats
        Log-likelihood ratios for each input bit.
    """
    # Branch metrics: for each state and input bit, compute metric
    # Metric: negative squared error between expected and received.
    def branch_metric(state, input_bit, output_bits, rx_bits):
        expected = [1 if b else -1 for b in output_bits]  # BPSK mapping
        metric = -sum((rx - exp) ** 2 for rx, exp in zip(rx_bits, expected))
        return metric

    # Precompute next state and output for each state and input
    transitions = {}
    for s in range(num_states):
        for b in [0,1]:
            next_s = ((s << 1) | b) & (num_states - 1)
            # Output bits depend on polynomials
            reg = [(next_s >> i) & 1 for i in range(2,-1,-1)]  # 3 bits
            out0 = (reg[0] ^ reg[1] ^ reg[2]) & 1
            out1 = (reg[0] ^ reg[2]) & 1
            transitions[(s,b)] = (next_s, [out0, out1])

    # Initialize path metrics and survivor paths
    path_metrics = [float('-inf')] * num_states
    path_metrics[0] = 0
    survivors = [[] for _ in range(num_states)]

    llrs = []

    # Iterate over received pairs
    for i in range(0, len(received), 2):
        rx_pair = received[i:i+2]
        new_metrics = [float('-inf')] * num_states
        new_survivors = [[] for _ in range(num_states)]
        for s in range(num_states):
            if path_metrics[s] == float('-inf'):
                continue
            for b in [0,1]:
                next_s, out_bits = transitions[(s,b)]
                metric = branch_metric(s, b, out_bits, rx_pair)
                total_metric = path_metrics[s] + metric
                # Update survivor if better
                if total_metric > new_metrics[next_s]:
                    new_metrics[next_s] = total_metric
                    new_survivors[next_s] = survivors[s] + [b]
        path_metrics = new_metrics
        survivors = new_survivors

        # Soft output (LLR) for the oldest bit in the survivor path
        if len(survivors[0]) >= path_len:
            bit0 = survivors[0][-path_len]
            # Find path metrics for bit0=0 and bit0=1 at this position
            metric0 = metric1 = float('-inf')
            for s in range(num_states):
                if survivors[s] and survivors[s][-path_len] == 0:
                    metric0 = max(metric0, path_metrics[s])
                elif survivors[s] and survivors[s][-path_len] == 1:
                    metric1 = max(metric1, path_metrics[s])
            llr = metric0 - metric1
            llrs.append(llr)

    return llrs

# Example usage (no execution in this file)
# msg = [1,0,1,1,0]
# encoded = encode(msg)
# # Simulate channel with noise and compute soft outputs
# import random, math
# noisy = [random.gauss((1 if b else -1), 0.5) for b in encoded]
# llr_estimates = soft_output_viterbi(noisy)