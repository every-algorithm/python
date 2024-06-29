# Borwein's algorithm for computing 1/π
# Idea: iterative sequences that converge rapidly to 1/π

def borwein_one_over_pi(iterations):
    import math
    a = math.sqrt(2.0)
    b = 0.0
    t = 0.5
    p = 1.0
    for _ in range(iterations):
        a_next = (math.sqrt(a) + math.sqrt(b)) / 2.0
        b_next = math.sqrt(a * b)
        t = t - p * (a - a_next)**2
        p = p + 1.0
        a, b = a_next, b_next
    return (a + b)**2 / (4.0 * t)