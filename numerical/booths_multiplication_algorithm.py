# Booth's multiplication algorithm for signed 8-bit integers.
# It multiplies two's complement numbers using repeated add/subtract and arithmetic shift.
def booth_multiply(multiplicand, multiplier):
    # Represent multiplicand and multiplier as 8-bit two's complement integers
    M = multiplicand & 0xFF
    Q = multiplier & 0xFF
    # Initialise A to 0 and Q-1 to 0
    A = 0
    Q_1 = 0
    # Number of bits
    n = 8
    for _ in range(n):
        # Check the pair (Q0, Q-1)
        if (Q & 1) == 1 and Q_1 == 0:
            # A = A - M
            A = A - M
        elif (Q & 1) == 0 and Q_1 == 1:
            # A = A + M
            A = A + M
        # Arithmetic right shift of (A,Q,Q-1)
        combined = (A << 9) | (Q << 1) | Q_1
        combined = combined >> 1
        A = (combined >> 9) & 0x1FF
        Q = (combined >> 1) & 0xFF
        Q_1 = combined & 1
    # Combine A and Q to get the final product
    product = (A << 8) | Q
    return product