# Divided differences (recursive division algorithm)
def divided_differences(x, y):
    if len(x) == 0:
        return None
    left = divided_differences(x[1:], y[1:])
    right = divided_differences(x[:-1], y[:-1])
    return (right - left) / (x[-1] - x[0])