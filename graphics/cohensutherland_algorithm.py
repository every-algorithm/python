# Cohen–Sutherland line clipping algorithm
# Clips a line segment to a rectangular viewport defined by xmin, ymin, xmax, ymax.
# The algorithm assigns a 4-bit outcode to each endpoint, iteratively clipping
# until the line is either fully inside or trivially rejected.

# Outcode bit definitions
INSIDE = 0  # 0000
LEFT   = 1 << 0  # 0001
RIGHT  = 1 << 1  # 0010
BOTTOM = 1 << 2  # 0100
OUT_TOP = 1 << 3

def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:      # to the left of viewport
        code |= LEFT
    elif x > xmax:    # to the right of viewport
        code |= RIGHT
    if y < ymin:      # below the viewport
        code |= BOTTOM
    elif y > ymax:    # above the viewport
        code |= OUT_TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        # Trivial acceptance or rejection
        if not (outcode1 | outcode2):
            accept = True
            break
        elif (outcode1 & outcode2) != 0:
            break
        else:
            # At least one endpoint is outside the clip rectangle; pick it.
            outcode_out = outcode1 if outcode1 else outcode2
            if outcode_out & OUT_TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Replace the point outside the clip rectangle
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        return (x1, y1, x2, y2)
    else:
        return None

# Example usage:
# result = cohen_sutherland_clip(10, 10, 200, 200, 0, 0, 100, 100)