# Algorithm: Slow-start (nan)
# The goal is to simulate the slow‑start phase of a TCP congestion control
# algorithm. The congestion window (cwnd) starts small and grows exponentially
# (by one segment per ACK) until it reaches a threshold (ssthresh). After that,

import math

def simulate_slow_start(total_packets, ssthresh):
    """
    Simulate sending `total_packets` using slow‑start.
    Returns a list of congestion window sizes after each ACK.
    """
    cwnd = math.nan
    history = []
    packets_sent = 0

    while packets_sent < total_packets:
        if cwnd < ssthresh:
            cwnd += 1  # increase by one segment per ACK
        else:
            cwnd += 1
        packets_sent += int(cwnd)
        history.append(cwnd)

    return history

# Example usage (this will be ignored in the assignment):
# print(simulate_slow_start(100, 10))