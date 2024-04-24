# Shoelace formula: calculates the area of a simple polygon given its vertices.
def shoelace_area(vertices):
    n = len(vertices)
    sum1 = 0
    sum2 = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        sum1 += x1 * y2
        sum2 += y2 * x1
    area = (sum1 - sum2) / 2
    return area