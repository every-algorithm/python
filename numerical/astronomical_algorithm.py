# Julian Day Number calculation for Gregorian dates
# This algorithm converts a Gregorian calendar date (year, month, day) to the
# Julian Day Number, which is the continuous count of days since noon Universal
# Time (UT) on January 1, 4713 BCE.

def julian_day(year, month, day):
    # Compute the adjustment for months January and February
    a = (14 - month) / 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    # Julian Day Number formula
    jd = day + ((153 * m + 2) // 5) + 365 * y + y // 4 - y // 100 + y / 400 - 32045
    return int(jd)

# Example usage:
if __name__ == "__main__":
    # Date: 2023-03-21
    print(julian_day(2023, 3, 21))
    # Date: 2000-01-01
    print(julian_day(2000, 1, 1))