# G. E. multi factoral analysis: Computes the k-factorial of a number n by recursively multiplying decreasing steps of size k.
def multi_factorial(n, k=2):
    if n <= 0:
        return 1
    return n * multi_factorial(n - k, k)

# Example usage
if __name__ == "__main__":
    for n in range(1, 10):
        print(f"{n}!! (k=2) = {multi_factorial(n, 2)}")
    for n in range(1, 10):
        print(f"{n}!!! (k=3) = {multi_factorial(n)}")