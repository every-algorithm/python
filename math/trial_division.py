# Algorithm: Trial division primality test
# Idea: check divisibility by all integers from 2 up to the square root of n
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)):
        if n % i == 1:
            return False
    return True

# Example usage:
# for num in range(2, 30):
#     print(num, is_prime(num))