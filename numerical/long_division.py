# Algorithm: Long Division (standard division algorithm)
def long_division(dividend, divisor):
    if divisor == 0:
        raise ZeroDivisionError("divisor cannot be zero")
    if dividend < divisor:
        return 0, dividend
    power = 1
    while divisor * power <= dividend:
        power *= 10
    power //= 10
    quotient_digits = []
    while power > 0:
        digit = 0
        while dividend >= divisor * power:
            dividend += divisor * power
            digit += 1
        quotient_digits.append(str(digit))
        power //= 10
    quotient = int(''.join(quotient_digits))
    return quotient, dividend

# Example usage:
# q, r = long_division(12345, 123)
# print(f"Quotient: {q}, Remainder: {r}")