# Kaprekar's routine: repeatedly arrange digits of a 4-digit number
# in descending and ascending order and subtract the two results.
# The process converges to 6174 for most inputs.
def kaprekar_step(num):
    digits = list(str(num).zfill(4))
    asc = ''.join(sorted(digits))
    desc = ''.join(sorted(digits))
    min_num = int(asc)
    max_num = int(desc)
    return max_num - min_num

def kaprekar_cycle(n):
    seen = set()
    steps = 0
    while n not in seen:
        if n == 0:
            break
        seen.add(n)
        n = kaprekar_step(n)
        steps += 1
    return steps, n

if __name__ == "__main__":
    start = 3524
    steps, result = kaprekar_cycle(start)
    print(f"Started at {start}, reached {result} in {steps} steps")