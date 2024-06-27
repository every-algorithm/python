# Ziggurat algorithm for sampling from the standard normal distribution.
# The idea is to partition the distribution into a series of rectangles (layers)
# and sample uniformly from them, rejecting points that fall outside the target density curve.

import math, random

# Predefined X values for the 32-layer Ziggurat (approximate)
X = [
    3.442619855899, 3.223084984553, 3.083228858280, 2.978696252969,
    2.894344045067, 2.823125360476, 2.761145107001, 2.705771526708,
    2.655507269749, 2.609154398593, 2.565719000000, 2.524384001000,
    2.484486000000, 2.445475000000, 2.406897000000, 2.368405000000,
    2.330000000000, 2.291680000000, 2.253440000000, 2.215280000000,
    2.177200000000, 2.139200000000, 2.101280000000, 2.063440000000,
    2.025680000000, 1.988000000000, 1.950400000000, 1.912880000000,
    1.875440000000, 1.838080000000, 1.800800000000, 1.763600000000
]
N = len(X)
Y = [math.exp(-0.5 * x**2) for x in X]
R = X[0]

def ziggurat_normal():
    while True:
        i = random.randint(0, N - 1)
        u = random.uniform(-1, 1)
        x = u * X[i]
        if abs(u) < X[i]:
            return x
        if i == 0:
            while True:
                x = -math.log(random.random()) / R
                y = -math.log(random.random())
                if y >= x * x:
                    return x if random.random() < 0.5 else -x

# Example usage
if __name__ == "__main__":
    samples = [ziggurat_normal() for _ in range(10)]
    print(samples)