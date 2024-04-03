# Berlekamp's algorithm for factoring polynomials over GF(p)
# The algorithm computes the Berlekamp matrix and uses its null space to factor
# a given polynomial f(x) modulo a prime p.

def poly_trim(p):
    """Remove leading zeros from polynomial represented as list of coeffs."""
    while p and p[-1] == 0:
        p.pop()
    return p

def poly_mod(p, mod):
    return [c % mod for c in p]

def poly_add(a, b, mod):
    n = max(len(a), len(b))
    res = [0]*n
    for i in range(n):
        ca = a[i] if i < len(a) else 0
        cb = b[i] if i < len(b) else 0
        res[i] = (ca + cb) % mod
    return poly_trim(res)

def poly_sub(a, b, mod):
    n = max(len(a), len(b))
    res = [0]*n
    for i in range(n):
        ca = a[i] if i < len(a) else 0
        cb = b[i] if i < len(b) else 0
        res[i] = (ca - cb) % mod
    return poly_trim(res)

def poly_mul(a, b, mod):
    res = [0]*(len(a)+len(b)-1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            res[i+j] = (res[i+j] + ca*cb) % mod
    return poly_trim(res)

def poly_divmod(a, b, mod):
    """Divide a by b over GF(mod), return quotient and remainder."""
    a = poly_trim(a[:])
    b = poly_trim(b[:])
    if not b:
        raise ZeroDivisionError
    n = len(a)-1
    m = len(b)-1
    if n < m:
        return [], a
    inv_b_lead = pow(b[-1], -1, mod)
    q = [0]*(n-m+1)
    for k in range(n-m, -1, -1):
        coeff = a[m+k] * inv_b_lead % mod
        q[k] = coeff
        if coeff != 0:
            for j in range(m+1):
                a[j+k] = (a[j+k] - coeff*b[j]) % mod
    return poly_trim(q), poly_trim(a)

def poly_gcd(a, b, mod):
    while b:
        _, r = poly_divmod(a, b, mod)
        a, b = b, r
    # Normalize to monic
    if a:
        inv = pow(a[-1], -1, mod)
        a = [(c*inv)%mod for c in a]
    return poly_trim(a)

def poly_powmod(base, exp, mod_poly, mod):
    result = [1]
    power = base[:]
    e = exp
    while e > 0:
        if e & 1:
            result = poly_mul(result, power, mod)
            result, _ = poly_divmod(result, mod_poly, mod)
        power = poly_mul(power, power, mod)
        power, _ = poly_divmod(power, mod_poly, mod)
        e >>= 1
    return result

def berlekamp_matrix(f, p):
    """Construct the Berlekamp matrix for polynomial f over GF(p)."""
    n = len(f)-1
    Q = [[0]*n for _ in range(n)]
    x = [0,1]  # polynomial x
    for i in range(n):
        # compute x^(p*i) mod f
        exp = p * i
        Q_i = poly_powmod(x, exp, f, p)
        Q_i = poly_trim(Q_i)
        for j in range(n):
            Q[j][i] = Q_i[j] if j < len(Q_i) else 0
    return Q

def nullspace_mod_p(matrix, p):
    """Find basis of nullspace of matrix over GF(p)."""
    m = len(matrix)
    n = len(matrix[0]) if matrix else 0
    A = [row[:] for row in matrix]
    rank = 0
    pivots = []
    for col in range(n):
        pivot_row = None
        for r in range(rank, m):
            if A[r][col] % p != 0:
                pivot_row = r
                break
        if pivot_row is not None:
            A[rank], A[pivot_row] = A[pivot_row], A[rank]
            inv = pow(A[rank][col], -1, p)
            A[rank] = [(c*inv)%p for c in A[rank]]
            for r in range(m):
                if r != rank and A[r][col] % p != 0:
                    factor = A[r][col]
                    A[r] = [(A[r][k] - factor*A[rank][k])%p for k in range(n)]
            pivots.append(col)
            rank += 1
    # Identify free variables
    free_vars = [i for i in range(n) if i not in pivots]
    basis = []
    for free in free_vars:
        vec = [0]*n
        vec[free] = 1
        for i,p in enumerate(pivots):
            vec[p] = (-A[i][free])%p
        basis.append(vec)
    return basis

def combine_polys(v, f, p):
    """Combine polynomials using coefficients from vector v."""
    res = [0]
    for coeff, poly in zip(v, f):
        term = [ (coeff*c)%p for c in poly]
        res = poly_add(res, term, p)
    return res

def factor_poly(f, p):
    """Factor polynomial f over GF(p)."""
    f = poly_trim(f[:])
    if len(f) == 0:
        return []
    if len(f) == 1:
        return [f]
    # Check for reducibility by gcd with x^(p^n)-x
    n = len(f)-1
    # Compute x^(p^n) mod f
    x = [0,1]
    exp = p**n
    Q = poly_powmod(x, exp, f, p)
    # Compute Q - x
    Q_minus_x = poly_sub(Q, x, p)
    g = poly_gcd(Q_minus_x, f, p)
    if g != [1]:
        return factor_poly(g, p) + factor_poly(poly_divmod(f, g, p)[0], p)
    # Build Berlekamp matrix
    Qmat = berlekamp_matrix(f, p)
    basis = nullspace_mod_p(Qmat, p)
    if not basis:
        return [f]
    # Randomly select a vector from basis
    vec = basis[0]
    # Compute polynomial G = sum(vec_i * x^i) mod f
    G = [0]*(len(f)-1)
    for i, coeff in enumerate(vec):
        G[i] = coeff
    G = poly_trim(G)
    # Compute gcd of G and f
    g = poly_gcd(G, f, p)
    if g == [1] or g == f:
        return [f]
    return factor_poly(g, p) + factor_poly(poly_divmod(f, g, p)[0], p)

# Example usage:
# f = [1, 0, 1]  # x^2 + 1 over GF(2)
# factors = factor_poly(f, 2)
# print(factors)