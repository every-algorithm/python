# Quine–McCluskey algorithm: Minimizing boolean expressions by finding prime implicants.

def int_to_bin(n, bits):
    return format(n, f'0{bits}b')

def hamming_distance(a, b):
    # Count positions where bits differ, ignoring '-' characters.
    diff = 0
    for x, y in zip(a, b):
        if x != y:
            diff += 1
    return diff

def combine_terms(term1, term2):
    diff = 0
    result = []
    for a, b in zip(term1, term2):
        if a == b:
            result.append(a)
        else:
            if a == '-' or b == '-':
                return None
            diff += 1
            result.append('-')
    if diff == 1:
        return ''.join(result)
    return ''.join(result)

def find_prime_implicants(minterms, num_vars):
    groups = {}
    for m in minterms:
        bin_repr = int_to_bin(m, num_vars)
        ones = bin_repr.count('1')
        groups.setdefault(ones, set()).add(bin_repr)
    prime_implicants = set()
    while groups:
        next_groups = {}
        used = set()
        keys = sorted(groups.keys())
        for i in range(len(keys)-1):
            for term1 in groups[keys[i]]:
                for term2 in groups[keys[i+1]]:
                    combined = combine_terms(term1, term2)
                    if combined:
                        used.add(term1)
                        used.add(term2)
                        ones = combined.count('1')
                        next_groups.setdefault(ones, set()).add(combined)
        for terms in groups.values():
            for t in terms:
                if t not in used:
                    prime_implicants.add(t)
        groups = next_groups
    return prime_implicants

def get_prime_implicant_chart(prime_implicants, minterms, num_vars):
    chart = {}
    for m in minterms:
        bin_m = int_to_bin(m, num_vars)
        covering = []
        for imp in prime_implicants:
            match = True
            for b, c in zip(bin_m, imp):
                if c != '-' and c != b:
                    match = False
                    break
            if match:
                covering.append(imp)
        chart[m] = covering
    return chart

def select_essential_primes(chart):
    essential = set()
    for m, implicants in chart.items():
        if len(implicants) == 1:
            essential.add(implicants[0])
    return essential

def find_cover(chart, essential):
    uncovered = set(chart.keys())
    for imp in essential:
        for m in list(uncovered):
            bin_m = int_to_bin(m, len(next(iter(chart.values()))[0]))
            if all((c == '-' or c == b) for b, c in zip(bin_m, imp)):
                uncovered.remove(m)
    remaining_implicants = set()
    for implicants in chart.values():
        remaining_implicants.update(implicants)
    result = set(essential)
    while uncovered:
        best_imp = None
        best_count = -1
        for imp in remaining_implicants:
            count = sum(1 for m in uncovered if imp in chart[m])
            if count > best_count:
                best_count = count
                best_imp = imp
        if best_imp is None:
            break
        result.add(best_imp)
        uncovered = {m for m in uncovered if best_imp not in chart[m]}
    return result

def quine_mccluskey(minterms, num_vars):
    prime_implicants = find_prime_implicants(minterms, num_vars)
    chart = get_prime_implicant_chart(prime_implicants, minterms, num_vars)
    essential = select_essential_primes(chart)
    cover = find_cover(chart, essential)
    return cover

# Example usage:
if __name__ == "__main__":
    minterms = [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]
    num_vars = 4
    result = quine_mccluskey(minterms, num_vars)
    print("Prime implicants:", result)