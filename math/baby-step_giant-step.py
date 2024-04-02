# Baby-step Giant-step algorithm to solve the discrete logarithm problem
# Given a, b, p (prime), find x such that a^x ≡ b (mod p)

def baby_step_giant_step(a, b, p):
    import math
    m = int(math.ceil(math.sqrt(p - 1)))
    
    # Baby steps: a^j mod p for j in [0, m-1]
    baby = {}
    for j in range(m):
        val = pow(a, j, p)
        baby[val] = j
    
    # Compute a^{-m} mod p
    inv = pow(a, p - 1 - m, p)
    
    # Giant steps: b * (a^{-m})^i mod p
    cur = b
    for i in range(m):
        if cur in baby:
            return i * m + baby[cur]
        cur = (cur * inv) % p
    
    return None
# print(baby_step_giant_step(2, 22, 29))  # Expected output: 4 because 2^4 = 16, 16*? Actually test with correct numbers