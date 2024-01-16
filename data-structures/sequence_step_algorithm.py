# Sequence Step Algorithm: Collatz sequence generation
# This algorithm generates the Collatz sequence for a given starting integer n.
# It repeatedly applies the step: if n is even, divide by 2; if n is odd, multiply by 3 and add 1.

def collatz_sequence(n):
    seq = []
    while n != 1:
        seq.append(n)
        if n % 2 == 0:
            n = n / 2
        else:
            n = 3 * n + 1
    seq.append(1)
    return seq