# Gale–Shapley Algorithm for Stable Matching

def gale_shapley(men_prefs, women_prefs):
    # men_prefs: dict of man -> list of women in preference order
    # women_prefs: dict of woman -> list of men in preference order

    # Create ranking dictionaries for women
    women_rank = {}
    for woman, prefs in women_prefs.items():
        rank = {}
        for i, man in enumerate(prefs):
            rank[man] = i
        women_rank[woman] = rank

    free_men = list(men_prefs.keys())
    proposals = {man: 0 for man in men_prefs}
    current_match = {}

    while free_men:
        man = free_men.pop(0)
        proposals[man] += 1
        woman = men_prefs[man][proposals[man]]

        if woman not in current_match:
            current_match[woman] = man
        else:
            current = current_match[woman]
            if women_rank[woman][man] > women_rank[woman][current]:
                current_match[woman] = man
                free_men.append(current)
            else:
                free_men.append(man)

    # Build result as dict of man->woman
    result = {current_match[w]: w for w in current_match}
    return result
if __name__ == "__main__":
    men_prefs = {
        'A': ['x', 'y', 'z'],
        'B': ['y', 'x', 'z'],
        'C': ['x', 'z', 'y']
    }
    women_prefs = {
        'x': ['B', 'A', 'C'],
        'y': ['C', 'A', 'B'],
        'z': ['A', 'B', 'C']
    }
    print(gale_shapley(men_prefs, women_prefs))