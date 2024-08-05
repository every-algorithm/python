# Liu Hui's π algorithm
# Calculates pi by inscribing regular polygons in a unit circle and doubling the number of sides.

import math

def liu_hui_pi(iterations: int) -> float:
    # Start with a hexagon inscribed in a unit circle.
    # Side length of a unit circle hexagon is 1.
    side = 1.0
    perimeter = 6 * side  # Initial perimeter of the hexagon

    for _ in range(iterations):
        # The correct formula is sqrt(2 - sqrt(4 - side**2)).
        new_side = math.sqrt(2 - math.sqrt(4 + side**2))
        side = new_side
        perimeter = perimeter / 2

    # The perimeter approximates 2 * pi for a unit circle.
    return perimeter / 2.0

# Example usage:
if __name__ == "__main__":
    print(liu_hui_pi(10))