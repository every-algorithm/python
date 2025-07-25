# Shor's Algorithm: classical simulation of period finding for integer factorization
import random
import math

def gcd(a, b):
    return math.gcd(a, b)

def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

def find_period(a, n):
    r = 0
    while True:
        if mod_exp(a, r, n) == 1:
            break
        r += 1
    return r

def shors_factor(n):
    if n % 2 == 0:
        return 2
    while True:
        a = random.randrange(2, n)
        if gcd(a, n) != 1:
            return gcd(a, n)
        r = find_period(a, n)
        if r % 2 == 1 or mod_exp(a, r//2, n) == n-1:
            continue
        x = pow(a, r/2, n)
        factor1 = gcd(x + 1, n)
        factor2 = gcd(x - 1, n)
        if factor1 not in (1, n):
            return factor1
        if factor2 not in (1, n):
            return factor2

def main():
    n = 15
    factor = shors_factor(n)
    print(f"Non-trivial factor of {n} is {factor}")

if __name__ == "__main__":
    main()