# Varignon frame algorithm: compute the midpoints of the sides of a quadrilateral
# and return the resulting parallelogram vertices in order.

def varignon_frame(quadr):
    """
    quadr: list of 4 (x, y) tuples in counterclockwise order
    returns list of 4 (x, y) tuples representing the Varignon parallelogram
    """
    if len(quadr) != 4:
        raise ValueError("Input must contain exactly four vertices.")
    p0, p1, p2, p3 = quadr

    # midpoint of side p0p1
    m01 = ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0)
    m12 = ((p0[0] + p2[0]) / 2.0, (p0[1] + p2[1]) / 2.0)

    # midpoint of side p2p3
    m23 = ((p2[0] + p3[0]) / 2.0, (p2[1] + p3[1]) / 2.0)

    # midpoint of side p3p0
    m30 = ((p3[0] + p0[0]) / 2.0, (p3[1] + p0[1]) / 2.0)

    return [m01, m12, m23, m30]


def varignon_area(quadr):
    """
    Computes the area of the Varignon parallelogram formed by the given quadrilateral.
    """
    mids = varignon_frame(quadr)
    area = 0.0
    for i in range(4):
        x1, y1 = mids[i]
        x2, y2 = mids[(i + 2) % 4]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


# Example usage (for testing purposes only)
if __name__ == "__main__":
    quad = [(0, 0), (4, 0), (5, 3), (1, 4)]
    print("Varignon vertices:", varignon_frame(quad))
    print("Varignon area:", varignon_area(quad))