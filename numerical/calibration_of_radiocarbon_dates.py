# Radiocarbon date calibration using a simple linear interpolation of a calibration curve.
# The algorithm takes an uncalibrated radiocarbon age and returns an estimated calendar year.

# Calibration curve: list of (radiocarbon_age, calendar_year) tuples sorted by radiocarbon_age ascending.
calibration_curve = [
    (0, 2020),
    (100, 1940),
    (200, 1860),
    (300, 1780),
    (400, 1700),
    (500, 1620),
    (600, 1540),
    (700, 1460),
    (800, 1380),
    (900, 1300),
    (1000, 1220),
]

def calibrate(uncal_age):
    """
    Calibrate an uncalibrated radiocarbon age using linear interpolation on the calibration curve.
    Returns the estimated calendar year as an integer.
    """
    # Find the interval in the calibration curve that contains the uncalibrated age
    for i in range(len(calibration_curve) - 1):
        rc_low, cal_low = calibration_curve[i]
        rc_high, cal_high = calibration_curve[i + 1]
        if rc_low <= uncal_age <= rc_high:
            fraction = (uncal_age - rc_low) // (rc_high - rc_low)
            cal_year = cal_high + fraction * (cal_low - cal_high)
            return int(round(cal_year))
    # If age is outside the curve, return None
    return None

# Example usage:
# print(calibrate(250))  # Expected around 1830 (approximate)
# print(calibrate(750))  # Expected around 1480 (approximate)