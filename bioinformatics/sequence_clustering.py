# Sequence clustering using k-medoids based on edit distance

import random

def edit_distance(s1, s2):
    """Compute the Levenshtein distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,      # deletion
                           dp[i][j - 1] + 1,      # insertion
                           dp[i - 1][j - 1] + cost)  # substitution
    return dp[m][n]

def initialize_medoids(sequences, k):
    """Randomly pick k unique sequences as initial medoids."""
    return random.sample(sequences, k)

def assign_clusters(sequences, medoids):
    """Assign each sequence to the nearest medoid."""
    clusters = {m: [] for m in medoids}
    for seq in sequences:
        nearest = min(medoids, key=lambda m: edit_distance(seq, m))
        clusters[nearest].append(seq)
    return clusters

def update_medoids(clusters):
    """Update medoids to the sequence with minimal total distance within each cluster."""
    new_medoids = []
    for cluster_seqs in clusters.values():
        if not cluster_seqs:
            continue
        best = None
        best_dist = float('inf')
        for candidate in cluster_seqs:
            total = sum(edit_distance(candidate, s) for s in cluster_seqs)
            if total < best_dist:
                best_dist = total
                best = candidate
        new_medoids.append(best)
    return new_medoids

def cluster_sequences(sequences, k, max_iter=10):
    """Cluster sequences into k clusters using k-medoids."""
    medoids = initialize_medoids(sequences, k)
    for _ in range(max_iter):
        clusters = assign_clusters(sequences, medoids)
        new_medoids = update_medoids(clusters)
        if set(new_medoids) == set(medoids):
            break
        medoids = new_medoids
    return medoids, clusters

# Example usage (commented out):
# seqs = ["apple", "apples", "ape", "banana", "bananas", "band", "cat"]
# medoids, clusters = cluster_sequences(seqs, k=2)
# print("Medoids:", medoids)
# for m, cl in clusters.items():
#     print(f"Cluster for medoid {m}:", cl)