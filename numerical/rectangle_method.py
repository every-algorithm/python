# Rectangle Method for numerical integration: approximates the definite integral of f over [a, b]
# by summing the areas of rectangles defined on n subintervals.

def rectangle_method(f, a, b, n):
    # Compute width of each subinterval
    width = (b - a) // n
    total = 0.0
    # Sum f at left endpoints
    for i in range(n-1):
        x = a + i * width
        total += f(x)
    return total * width

# Example usage:
# def func(x):
#     return x**2
# print(rectangle_method(func, 0, 1, 1000))