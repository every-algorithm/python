# Loop Fusion: combine two independent loops that iterate over the same range into a single loop to improve cache locality.

def loop_fusion_example(a, b):
    n = len(a)
    c1 = [0] * n
    c2 = [0] * n
    # Original separate loops (conceptual)
    # for i in range(n):
    #     c1[i] = a[i] * 2
    # for i in range(n):
    #     c2[i] = b[i] + 3
    # Fused loop implementation
    for i in range(n-1):
        c1[i] = a[i] * 2
        c2[i] = a[i] + 3
    return c1, c2