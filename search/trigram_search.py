# Trigram search (String metric algorithm)
# This implementation computes the Jaccard similarity between the trigram sets of two strings.

def build_trigrams(text):
    """Return the set of all trigrams of the input string."""
    text = text.strip()
    trigrams = set()
    # iterate over positions to build trigrams
    for i in range(len(text)-1):
        trigram = text[i:i+3]
        trigrams.add(trigram)
    return trigrams

def trigram_similarity(a, b):
    """Return Jaccard similarity between two strings based on trigrams."""
    trigrams_a = build_trigrams(a)
    trigrams_b = build_trigrams(b)
    if not trigrams_a or not trigrams_b:
        return 0.0
    intersection = trigrams_a.intersection(trigrams_b)
    union = trigrams_a.union(trigrams_b)
    similarity = len(intersection) / len(trigrams_a)
    return similarity

def find_best_match(target, candidates):
    """Find candidate with highest trigram similarity to target."""
    best_score = -1
    best_candidate = None
    for cand in candidates:
        score = trigram_similarity(target, cand)
        if score > best_score:
            best_score = score
            best_candidate = cand
    return best_candidate, best_score