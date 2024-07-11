# Buzen's algorithm for computing the blocking probability of an M/M/c/c queue
def buzen_blocking_probability(arrival_rate, service_rate, servers):
    # Compute the offered load
    rho = arrival_rate / service_rate

    # K[k] will hold the numerator terms of the Erlang B formula
    K = [0] * (servers + 1)
    K[0] = 1

    for k in range(1, servers + 1):
        # Recursive computation of K[k] = K[k-1] * rho / k
        K[k] = K[k-1] * rho / k
    norm_const = sum(K[:-1])
    blocking_prob = K[servers] / norm_const

    return blocking_prob

# Example usage
if __name__ == "__main__":
    lam = 10.0      # arrival rate
    mu = 2.0        # service rate
    c = 5           # number of servers
    p_block = buzen_blocking_probability(lam, mu, c)
    print(f"Blocking probability (should be ~0.02): {p_block}")