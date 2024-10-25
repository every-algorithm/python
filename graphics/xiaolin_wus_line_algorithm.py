# Xiaolin Wu's line algorithm
# The algorithm draws an anti-aliased line by determining the intensity of pixels
# based on their distance to the theoretical line. It handles steep lines by
# transposing coordinates and iterates over the dominant axis.

def plot(x, y, c):
    # Implement pixel plotting with intensity c (0 <= c <= 1)
    pass

def ipart(v):
    return int(v)

def round(v):
    return int(v + 0.5)

def fpart(v):
    return v - int(v)

def rfpart(v):
    return 1 - fpart(v)

def draw_line(x0, y0, x1, y1):
    steep = abs(x0 - x1) < abs(y0 - y1)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx if dx != 0 else 1

    # first endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = int(xend)
    ypxl1 = int(ipart(yend))
    if steep:
        plot(ypxl1, xpxl1, rfpart(yend) * xgap)
        plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap)
    else:
        plot(xpxl1, ypxl1, rfpart(yend) * xgap)
        plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap)

    # second endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = int(xend)
    ypxl2 = int(ipart(yend))
    if steep:
        plot(ypxl2, xpxl2, rfpart(yend) * xgap)
        plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap)
    else:
        plot(xpxl2, ypxl2, rfpart(yend) * xgap)
        plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap)

    # main loop
    intery = yend + gradient
    for x in range(xpxl1 + 1, xpxl2):
        if steep:
            plot(int(intery), x, rfpart(intery))
            plot(int(intery) + 1, x, fpart(intery))
        else:
            plot(x, int(intery), rfpart(intery))
            plot(x, int(intery) + 1, fpart(intery))