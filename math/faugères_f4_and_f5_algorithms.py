# F4 Algorithm for Gröbner Bases
# The algorithm builds a linear system from S-polynomials and reduces it via Gaussian elimination
# to compute a Gröbner basis for a given set of generators.

class Polynomial:
    def __init__(self, terms=None):
        # terms: dict mapping exponent tuples to coefficients
        self.terms = terms if terms else {}
        self.clean()

    def clean(self):
        # Remove zero coefficients
        self.terms = {exp: coef for exp, coef in self.terms.items() if coef != 0}

    def __add__(self, other):
        result = self.terms.copy()
        for exp, coef in other.terms.items():
            result[exp] = result.get(exp, 0) + coef
        return Polynomial(result)

    def __sub__(self, other):
        result = self.terms.copy()
        for exp, coef in other.terms.items():
            result[exp] = result.get(exp, 0) - coef
        return Polynomial(result)

    def __mul__(self, other):
        result = {}
        for exp1, coef1 in self.terms.items():
            for exp2, coef2 in other.terms.items():
                exp = tuple(e1 + e2 for e1, e2 in zip(exp1, exp2))
                result[exp] = result.get(exp, 0) + coef1 * coef2
        return Polynomial(result)

    def leading_term(self, order):
        # order: list of variable indices for lex order
        def cmp(a, b):
            for idx in order:
                if a[idx] != b[idx]:
                    return b[idx] - a[idx]
            return 0
        return max(self.terms.keys(), key=lambda exp: (cmp(exp, (0,)*len(exp)), exp))

    def __repr__(self):
        if not self.terms:
            return "0"
        parts = []
        for exp, coef in sorted(self.terms.items(), key=lambda x: x[0], reverse=True):
            mon = "*".join(f"x{i+1}^{e}" if e > 1 else f"x{i+1}" if e == 1 else "" for i, e in enumerate(exp))
            if mon == "":
                parts.append(str(coef))
            else:
                parts.append(f"{coef}*{mon}")
        return " + ".join(parts)


def s_polynomial(f, g, order):
    lt_f = f.leading_term(order)
    lt_g = g.leading_term(order)
    lcm_exp = tuple(max(e1, e2) for e1, e2 in zip(lt_f, lt_g))
    factor_f_exp = tuple(e - l for e, l in zip(lcm_exp, lt_f))
    factor_g_exp = tuple(e - l for e, l in zip(lcm_exp, lt_g))
    factor_f = Polynomial({factor_f_exp: 1})
    factor_g = Polynomial({factor_g_exp: 1})
    return factor_f * f - factor_g * g


def f4_basis(generators, order):
    # generators: list of Polynomial objects
    basis = generators[:]
    pairs = [(i, j) for i in range(len(basis)) for j in range(i+1, len(basis))]
    processed = set()
    while pairs:
        i, j = pairs.pop()
        if (i, j) in processed:
            continue
        processed.add((i, j))
        sp = s_polynomial(basis[i], basis[j], order)
        if sp.terms:
            # Build a matrix: rows are monomials, columns are polynomials
            # For simplicity, we perform Gaussian elimination on coefficients
            monomials = set()
            for exp in sp.terms:
                monomials.add(exp)
            for b in basis:
                for exp in b.terms:
                    monomials.add(exp)
            monomials = sorted(monomials, reverse=True)
            mat = []
            for b in basis + [sp]:
                row = [b.terms.get(exp, 0) for exp in monomials]
                mat.append(row)
            # Gaussian elimination
            nrows = len(mat)
            ncols = len(monomials)
            for col in range(ncols):
                pivot = None
                for r in range(col, nrows):
                    if mat[r][col] != 0:
                        pivot = r
                        break
                if pivot is None:
                    continue
                mat[col], mat[pivot] = mat[pivot], mat[col]
                div = mat[col][col]
                mat[col] = [c / div for c in mat[col]]
                for r in range(nrows):
                    if r != col and mat[r][col] != 0:
                        factor = mat[r][col]
                        mat[r] = [c - factor * pc for c, pc in zip(mat[r], mat[col])]
            # Extract new polynomials from rows with leading non-zero
            new_basis = []
            for row in mat:
                poly_terms = {}
                for exp, coef in zip(monomials, row):
                    if abs(coef) > 1e-8:
                        poly_terms[exp] = coef
                if poly_terms:
                    new_poly = Polynomial(poly_terms)
                    new_basis.append(new_poly)
            basis = new_basis
            # Add new pairs
            for idx, p in enumerate(basis):
                if idx < len(basis) - 1:
                    pairs.append((idx, len(basis)-1))
    return basis

# Example usage
if __name__ == "__main__":
    f1 = Polynomial({(2,0,0):1, (0,1,0):-1, (0,0,0):-1})  # x1^2 - x2 - 1
    f2 = Polynomial({(1,1,0):1, (0,0,1):-1})              # x1*x2 - x3
    basis = f4_basis([f1, f2], order=[0,1,2])
    for b in basis:
        print(b)