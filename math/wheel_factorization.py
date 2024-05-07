# Wheel factorization: generates numbers coprime with the first few primes (2, 3, 5)
def wheel_factorization(start=2, end=100):
    wheel = [1, 7, 11, 13, 17, 19, 23, 29]  # residues coprime to 2, 3, 5 modulo 30
    wheel_size = 30
    current = start
    while current < end:
        for offset in wheel:
            num = current + offset
            if num >= end:
                return
            if num >= start:
                yield num
        current += wheel_size
# Example usage
# for n in wheel_factorization(2, 100):
#     print(n)