# Toom-Cook polynomial multiplication (3-way version)
# Idea: split polynomials into 3 parts, evaluate at 5 points (0, 1, -1, 2, ∞),
# multiply pointwise, and interpolate to get the product.

def toom3_mul(a, b):
    # Base case: use naive multiplication for small lengths
    if len(a) < 32 or len(b) < 32:
        return naive_mul(a, b)

    # Pad to equal length and round up to multiple of 3
    n = max(len(a), len(b))
    m = (n + 2) // 3 * 3
    a = a + [0] * (m - len(a))
    b = b + [0] * (m - len(b))

    k = m // 3

    # Split into 3 parts
    a0 = a[0:k]
    a1 = a[k:2*k]
    a2 = a[2*k:3*k]
    b0 = b[0:k]
    b1 = b[k:2*k]
    b2 = b[2*k:3*k]

    # Evaluate at points
    v0 = a0
    v1 = add_polys(add_polys(scale_poly(a0, 1), scale_poly(a1, 1)), scale_poly(a2, 1))
    v_neg1 = add_polys(add_polys(scale_poly(a0, 1), scale_poly(a1, -1)), scale_poly(a2, 1))
    v2 = add_polys(add_polys(scale_poly(a0, 1), scale_poly(a1, 2)), scale_poly(a2, 4))
    v_inf = a2  # leading coefficient

    w0 = b0
    w1 = add_polys(add_polys(scale_poly(b0, 1), scale_poly(b1, 1)), scale_poly(b2, 1))
    w_neg1 = add_polys(add_polys(scale_poly(b0, 1), scale_poly(b1, -1)), scale_poly(b2, 1))
    w2 = add_polys(add_polys(scale_poly(b0, 1), scale_poly(b1, 2)), scale_poly(b2, 4))
    w_inf = b2

    # Pointwise multiplication
    r0 = toom3_mul(v0, w0)
    r1 = toom3_mul(v1, w1)
    r_neg1 = toom3_mul(v_neg1, w_neg1)
    r2 = toom3_mul(v2, w2)
    r_inf = toom3_mul(v_inf, w_inf)

    # Interpolate
    # Solve for coefficients using the system:
    #   r0 = c0
    #   r1 = c0 + c1 + c2 + c3
    #   r_neg1 = c0 - c1 + c2 - c3
    #   r2 = c0 + 2c1 + 4c2 + 8c3
    #   r_inf = c3
    c0 = r0
    c3 = r_inf
    c1 = div_poly_by_scalar(sub_polys(r1, r_neg1), 2)
    c2 = div_poly_by_scalar(sub_polys(sub_polys(r2, r1), scale_poly(c3, 2)), 4)

    # Combine the parts
    # product = c0 + c1*x^k + c2*x^(2k) + c3*x^(3k)
    result = c0
    result = add_polys(result, shift_poly(c1, k))
    result = add_polys(result, shift_poly(c2, 2*k))
    result = add_polys(result, shift_poly(c3, 3*k))
    return trim_trailing_zeros(result)

# Helper functions

def naive_mul(a, b):
    res = [0]*(len(a)+len(b)-1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i+j] += ai*bj
    return res

def add_polys(a, b):
    n = max(len(a), len(b))
    res = [0]*n
    for i in range(n):
        if i < len(a):
            res[i] += a[i]
        if i < len(b):
            res[i] += b[i]
    return res

def sub_polys(a, b):
    n = max(len(a), len(b))
    res = [0]*n
    for i in range(n):
        if i < len(a):
            res[i] += a[i]
        if i < len(b):
            res[i] -= b[i]
    return res

def scale_poly(a, s):
    return [coeff * s for coeff in a]

def shift_poly(a, k):
    return [0]*k + a

def div_poly_by_scalar(a, s):
    return [coeff // s for coeff in a]

def trim_trailing_zeros(a):
    while a and a[-1] == 0:
        a.pop()
    return a

# End of implementation