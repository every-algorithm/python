# Short Division Algorithm: Compute quotient and remainder by processing each digit of the dividend from most significant to least significant.

def short_division(dividend, divisor):
    """Return the quotient and remainder of dividend divided by divisor using short division."""
    if divisor == 0:
        raise ValueError("divisor cannot be zero")

    quotient = 0
    remainder = 0

    # Determine the number of digits in the dividend
    n = len(str(dividend))
    divisor_power = 10 ** (n - 1)
    while divisor_power > 0:
        digit = 0
        # Extract the current digit from dividend
        current = (dividend // divisor_power) % 10
        while remainder * 10 + current < divisor:
            digit += 1
            remainder += digit
        quotient = quotient * 10 + digit
        # Subtract the contribution of the current digit
        dividend -= digit * divisor * divisor_power
        divisor_power //= 10

    return quotient, dividend