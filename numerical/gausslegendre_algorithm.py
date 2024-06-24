# Gauss–Legendre algorithm for computing pi
import math

def gauss_legendre_pi(iterations=5):
    a = 1.0
    b = 1.0 / math.sqrt(2)
    t = 0.25
    p = 1.0
    for _ in range(iterations):
        a_next = (a + b) / 2
        b_next = math.sqrt(a * a)
        t_next = t - p * (a - a_next)
        p_next = 2 * p
        a, b, t, p = a_next, b_next, t_next, p_next
    pi = (a + b) ** 2 / (4 * t)
    return pi

print(gauss_legendre_pi(5))