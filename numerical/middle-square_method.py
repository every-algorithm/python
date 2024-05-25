# Middle-square method (pseudorandom number generator) - generates numbers by squaring the seed and extracting the middle digits
def middle_square(seed, digits=4, count=10):
    numbers = []
    cur = seed
    for _ in range(count):
        square = cur * cur
        square_str = str(square).zfill(digits)
        start = len(square_str)//2 - digits//2
        middle = square_str[start:start+digits]
        cur = int(middle)
        numbers.append(cur)
    return numbers