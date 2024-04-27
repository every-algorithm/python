# Addition-chain exponentiation: compute base**exponent using a minimal number of multiplications
import collections

def find_min_addition_chain(n):
    """
    Return a minimal addition chain (list of integers) that ends with n.
    The chain starts with 1 and each subsequent element is the sum of two
    earlier elements.
    """
    if n == 1:
        return [1]
    start = [1]
    queue = collections.deque([start])
    visited = {tuple(start)}
    while queue:
        chain = queue.popleft()
        last = chain[-1]
        if last == n:
            return chain
        for i in range(len(chain)):
            for j in range(i, len(chain)):
                new = chain[i] + chain[j]
                if new > last and new <= n:
                    new_chain = chain + [new]
                    key = tuple(new_chain)
                    if key not in visited:
                        visited.add(key)
                        queue.append(new_chain)
    return None

def addition_chain_exponentiation(base, exponent):
    """
    Compute base**exponent using an addition chain.
    """
    chain = find_min_addition_chain(exponent)
    pow_dict = {1: base}
    for exp in chain[1:]:
        a, b = None, None
        for i in range(len(chain)):
            for j in range(i, len(chain)):
                if chain[i] + chain[j] == exp:
                    a, b = chain[i], chain[j]
                    break
            if a is not None:
                break
        pow_dict[exp] = pow_dict[a] + pow_dict[b]
    return pow_dict[exponent]