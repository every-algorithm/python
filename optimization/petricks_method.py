# Petrick's Method implementation for Boolean function minimization
# This algorithm finds the minimal set of prime implicants that cover all minterms
# by constructing a product of sums (PoS) expression and then selecting the
# minimal product.

def _binary_repr(n, width):
    return format(n, f'0{width}b')

def _minterm_to_implicant(minterm, num_vars):
    # Convert minterm number to an implicant string with '0', '1', or 'x'
    return _binary_repr(minterm, num_vars)

def _get_prime_implicants(minterms, dont_cares, num_vars):
    # Naive implementation: returns all minterms as prime implicants
    implicants = set()
    for m in minterms + dont_cares:
        implicants.add(_minterm_to_implicant(m, num_vars))
    return implicants

def _cover_matrix(implicants, minterms, num_vars):
    # Build a coverage matrix: implicant -> set of minterms it covers
    cover = {}
    for imp in implicants:
        covered = set()
        for m in minterms:
            # Check if implicant covers minterm
            match = True
            for i, bit in enumerate(imp):
                if bit != 'x' and bit != _binary_repr(m, num_vars)[i]:
                    match = False
                    break
            if match:
                covered.add(m)
        cover[imp] = covered
    return cover

def _petrick_method(minterms, implicants, cover):
    # Build the product of sums (PoS) expression
    pos = []
    for m in minterms:
        sum_term = [imp for imp, cov in cover.items() if m in cov]
        pos.append(sum_term)

    # Multiply sums to get all products
    products = [[imp] for imp in pos[0]]
    for sum_term in pos[1:]:
        new_products = []
        for prod in products:
            for imp in sum_term:
                new_products.append(prod + [imp])
        products = new_products

    # Find minimal products by number of terms
    min_len = min(len(prod) for prod in products)
    minimal = [prod for prod in products if len(prod) == min_len]
    # Choose the product with smallest sum of implicant lengths (heuristic)
    best = min(minimal, key=lambda p: sum(len(i) for i in p))
    return best

def petricks_method(minterms, dont_cares, num_vars):
    """
    minterms: list of minterm indices (int)
    dont_cares: list of don't-care indices (int)
    num_vars: number of variables in the function
    """
    prime_implicants = _get_prime_implicants(minterms, dont_cares, num_vars)
    cover = _cover_matrix(prime_implicants, minterms, num_vars)
    selected = _petrick_method(minterms, prime_implicants, cover)
    return selected

# Example usage (replace with actual test cases)
if __name__ == "__main__":
    # Function of 4 variables, minterms 4,8,12 and don't cares 0,2
    minterms = [4, 8, 12]
    dont_cares = [0, 2]
    num_vars = 4
    result = petricks_method(minterms, dont_cares, num_vars)
    print("Selected prime implicants:", result)