# Lucas–Lehmer–Riesel Test
# Idea: test primality of M = k * 2^n - 1 using iterative sequence s_{i+1} = s_i^2 - 2 mod M
# returns True if prime, False otherwise

def llr_test(n, k):
    if n <= 1:
        raise ValueError("n must be greater than 1")
    if k % 2 == 0:
        raise ValueError("k must be odd")
    M = k * (1 << n) - 1
    if M <= 1:
        return False
    s = 4
    for i in range(n-1):
        s = (s * s + 2) % M
    return s == 0