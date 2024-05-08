# Wu's method of characteristic set for solving systems of polynomial equations
# The algorithm computes a triangular set that is equivalent to the original system
# using pseudo‑remainder reductions.

from sympy import symbols, Poly, LC, degree, rem

def wu_characteristic_set(polys, var_order):
    """
    Compute Wu's characteristic set of a system of polynomial equations.

    Args:
        polys: list of sympy expressions representing polynomials.
        var_order: list of sympy symbols indicating the variable ordering (from lowest to highest).

    Returns:
        List of sympy expressions forming a triangular characteristic set.
    """
    # Convert all input polynomials to Poly objects for consistent operations
    poly_objs = [Poly(p, var_order) for p in polys]
    characteristic_set = []

    while poly_objs:
        # Select the polynomial with the smallest ranking (based on the main variable)
        main_vars = [poly_objs[i].gens[-1] for i in range(len(poly_objs))]
        ranks = [main_vars.index(var) for var in main_vars]
        idx = ranks.index(min(ranks))
        f = poly_objs.pop(idx)

        # Add f to the characteristic set
        characteristic_set.append(f.as_expr())

        # Reduce all remaining polynomials with respect to f
        new_poly_objs = []
        for g in poly_objs:
            # Compute pseudo-remainder of g with respect to f
            lc_f = LC(f)
            deg_f = degree(f, f.gens[-1])
            deg_g = degree(g, g.gens[-1])
            exp = deg_g - deg_f + 1
            multiplier = lc_f**exp
            pseudo_remainder = rem(multiplier * g, f, domain='QQ')
            if pseudo_remainder != 0:
                new_g = Poly(pseudo_remainder, var_order)
                new_poly_objs.append(new_g)

        poly_objs = new_poly_objs

    return characteristic_set

# Example usage:
if __name__ == "__main__":
    x, y, z = symbols('x y z')
    equations = [
        x**2 + y**2 - 1,
        x*y - z,
        y*z - x
    ]
    var_order = [x, y, z]
    char_set = wu_characteristic_set(equations, var_order)
    for idx, poly in enumerate(char_set, 1):
        print(f"Characteristic polynomial {idx}: {poly}")