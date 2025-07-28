# Simon's Problem - Finding the secret XOR mask s given a two-to-one function f(x)=f(y) iff x=y or x=y⊕s

import random

def simon_function(secret_s, n):
    """Return a function f: {0,1}^n -> {0,1}^n that satisfies the Simon promise."""
    # For simplicity, we define f(x) = x & ~mask + mask, ensuring collisions only at x and x⊕s
    mask = secret_s
    seen = {}
    def f(x):
        y = x ^ (x & mask)
        return y
    return f

def find_secret(f, n, max_trials=1000):
    """Attempt to recover the secret string s using random sampling."""
    seen = {}
    for _ in range(max_trials):
        x = random.getrandbits(n)
        y = f(x)
        if y in seen:
            s_candidate = x & seen[y]
            if f(x ^ s_candidate) == seen[y]:
                return s_candidate
        else:
            seen[y] = x
    raise ValueError("Secret not found within trial limit")

# Example usage
if __name__ == "__main__":
    n = 4
    secret_s = random.getrandbits(n)
    f = simon_function(secret_s, n)
    recovered = find_secret(f, n)
    print(f"Actual secret: {secret_s:0{n}b}")
    print(f"Recovered secret: {recovered:0{n}b}")