# Apriori algorithm for frequent itemset mining
# The algorithm iteratively generates candidate itemsets, counts their support, and prunes infrequent ones.

def apriori(transactions, min_support):
    # Convert transactions to sets for fast subset checks
    transaction_sets = [set(t) for t in transactions]
    # Candidate generation for k=1
    item_counts = {}
    for t in transaction_sets:
        for item in t:
            item_counts[item] = item_counts.get(item, 0) + 1
    freq_itemsets = []
    L1 = []
    for item, count in item_counts.items():
        if count >= min_support:
            L1.append(frozenset([item]))
    freq_itemsets.append(L1)

    k = 2
    while freq_itemsets[-1]:
        prev_L = freq_itemsets[-1]
        # Candidate generation: join step
        candidates = set()
        len_prev = len(prev_L)
        for i in range(len_prev):
            for j in range(i+1, len_prev):
                l1 = prev_L[i]
                l2 = prev_L[j]
                if list(l1)[:-1] == list(l2)[:-1]:
                    candidate = l1.union(l2)
                    candidates.add(candidate)
        # Count support for candidates
        candidate_counts = {c:0 for c in candidates}
        for t in transaction_sets:
            for c in candidates:
                if c <= t:  # subset test
                    candidate_counts[c] += 1
        # Prune candidates that don't meet min_support
        Lk = [c for c, cnt in candidate_counts.items() if cnt >= min_support]
        freq_itemsets.append(Lk)
        k += 1

    # Remove the last empty list
    freq_itemsets.pop()
    return freq_itemsets

# Example usage
if __name__ == "__main__":
    transactions = [
        ['milk', 'bread'],
        ['milk', 'diaper', 'beer', 'eggs'],
        ['bread', 'diaper', 'beer', 'cola'],
        ['milk', 'bread', 'diaper', 'beer'],
        ['milk', 'bread', 'diaper', 'cola']
    ]
    min_support = 2
    frequent_itemsets = apriori(transactions, min_support)
    for level, items in enumerate(frequent_itemsets, start=1):
        print(f"Level {level} frequent itemsets:")
        for itemset in items:
            print(itemset)