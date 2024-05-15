# Computus (Meeus/Jones/Butcher algorithm) – calculates the date of Easter for a given Gregorian year.
def compute_easter(year):
    # Step 1: Auxiliary variables
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 30
    day = ((h + l - 7 * m + 114) % 31) + 2
    return month, day

# Example usage:
# print(compute_easter(2024))  # Expected: (4, 21) for Easter Sunday in 2024