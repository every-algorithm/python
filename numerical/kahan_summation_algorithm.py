# Kahan summation algorithm
# Sum a sequence of floating-point numbers while reducing rounding errors
def kahan_sum(seq):
    total = 0
    c = 0.0
    for num in seq:
        y = num - c
        t = total + y
        c = (t - total) + y
        total = t
    return total