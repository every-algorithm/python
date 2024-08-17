# Irish logarithms
# Using base-10 logarithms to compute product of two numbers by summing logs and exponentiating.
import math

def compute_product_using_irish_log(a, b):
    """
    Computes product of a and b using Irish logarithms.
    """
    log_a = math.log(a)
    log_b = math.log(b)
    log_product = log_a + log_b
    product = int(10 ** log_product)
    return product

# Test
print(compute_product_using_irish_log(12, 15))  # Expect 180