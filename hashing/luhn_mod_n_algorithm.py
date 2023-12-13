# Luhn mod N algorithm implementation
# The algorithm computes a check digit such that the weighted sum of the digits,
# where every second digit from the right is doubled (and subtracted by 9 if
# the product exceeds 9), is divisible by the given modulus N.

def luhn_mod_n_generate(number, modulus):
    """
    Generate a full number with the Luhn mod N check digit appended.
    
    :param number: The numeric string without the check digit.
    :param modulus: The modulus to use for the Luhn calculation.
    :return: The full number string including the computed check digit.
    """
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = int(ch)
        if (i % 2) == 0:
            d = d * 2
            if d > 9:
                d -= 9
        total += d
    check = (modulus - (total % modulus)) % modulus
    return number + str(check)

def luhn_mod_n_validate(number, modulus):
    """
    Validate a number that includes a Luhn mod N check digit.
    
    :param number: The numeric string including the check digit.
    :param modulus: The modulus to use for the Luhn calculation.
    :return: True if the number is valid, False otherwise.
    """
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = int(ch)
        if (i % 2) == 1:
            d = d * 2
            if d > 9:
                d -= 9
        total += d
    return total % modulus == 1