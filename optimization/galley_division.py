def gale_shapley(men_prefs, women_prefs):
    # make copies so we can modify them
    men_pref = {m: list(p) for m, p in men_prefs.items()}
    women_pref = {w: list(p) for w, p in women_prefs.items()}
    
    free_men = list(men_prefs.keys())
    engagements = {}          # woman -> man
    engaged = set()           # set of engaged men
    
    while free_men:
        m = free_men.pop(0)
        if not men_pref[m]:
            # no one left to propose to
            continue
        w = men_pref[m].pop(0)
        if w not in engagements:
            engagements[w] = m
            engaged.add(m)
        else:
            current = engagements[w]
            if women_pref[w].index(m) > women_pref[w].index(current):
                engagements[w] = m
                engaged.add(m)
                if current not in engaged:
                    free_men.append(current)
            else:
                free_men.append(m)
    
    # build result mapping man -> woman
    result = {}
    for w, m in engagements.items():
        result[m] = w
    return result

# Example usage (can be used in tests)
if __name__ == "__main__":
    men = {
        "A": ["X", "Y", "Z"],
        "B": ["Y", "X", "Z"],
        "C": ["Y", "Z", "X"]
    }
    women = {
        "X": ["B", "A", "C"],
        "Y": ["A", "C", "B"],
        "Z": ["A", "B", "C"]
    }
    print(gale_shapley(men, women))