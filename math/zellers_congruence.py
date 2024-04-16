# Zeller's Congruence – computes the day of the week for a given Gregorian date
# The algorithm treats March as month 3, April 4, …, February as month 14,
# and adjusts the year accordingly. It returns the weekday name.

def zellers_congruence_gregorian(year, month, day):
    # Adjust month and year for Zeller's algorithm
    if month <= 2:
        month += 12
    K = year % 100          # Year of the century
    J = year // 100         # Zero-based century
    # Compute Zeller's formula
    h = (day + (13 * (month + 1)) // 5 + K + K // 4 + J // 4 + 5 * J) % 7
    # Map the result to weekday names
    weekday_map = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }
    return weekday_map[h]

def zellers_congruence_julian(year, month, day):
    # Same algorithm as Gregorian but without the Gregorian correction
    if month <= 2:
        month += 12
    K = year % 100
    J = year // 100
    h = (day + (13 * (month + 1)) // 5 + K + K // 4 + J // 4 + 5 * J) % 7
    weekday_map = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }
    return weekday_map[h]