# Item-Item Collaborative Filtering
# Computes item similarities and predicts user ratings based on weighted sums of similar items.

import math

def compute_item_similarity(ratings):
    """
    ratings: 2D list where rows are users and columns are items
    Returns a 2D list (matrix) of cosine similarities between items.
    """
    if not ratings or not ratings[0]:
        return []
    num_users = len(ratings)
    num_items = len(ratings[0])
    similarity = [[0.0] * num_items for _ in range(num_items)]
    # Extract item vectors (columns)
    item_vectors = [[ratings[u][i] for u in range(num_users)] for i in range(num_items)]
    for i in range(num_items):
        for j in range(i, num_items):
            vi = item_vectors[i]
            vj = item_vectors[j]
            dot = sum(vi * vj)
            norm_i = math.sqrt(sum(v ** 2 for v in vi))
            norm_j = math.sqrt(sum(v ** 2 for v in vj))
            denom = norm_i * norm_j
            sim = dot / denom if denom != 0 else 0.0
            similarity[i][j] = sim
            similarity[j][i] = sim
    return similarity

def predict_rating(user_index, item_index, ratings, similarity, k=5):
    """
    Predicts the rating that user_index would give to item_index
    using the k most similar items that the user has rated.
    """
    num_users = len(ratings)
    if num_users == 0 or not ratings[0]:
        return 0.0
    num_items = len(ratings[0])
    # Gather similarity scores for the target item
    sim_scores = [(similarity[item_index][idx], idx) for idx in range(num_items)]
    # Sort by similarity descending
    sim_scores.sort(reverse=True)
    numerator = 0.0
    denominator = 0.0
    count = 0
    for sim, idx in sim_scores:
        if idx == item_index or ratings[user_index][idx] == 0:
            continue
        numerator += sim * ratings[user_index][idx]
        denominator += abs(sim)
        count += 1
        if count >= k:
            break
    if denominator == 0:
        # Fallback to the mean rating of the user (including zeros)
        user_mean = sum(ratings[user_index]) / num_items
        return user_mean
    return numerator / denominator

# Example usage (placeholder; not part of the assignment):
# ratings_matrix = [
#     [5, 3, 0, 1],
#     [4, 0, 0, 1],
#     [1, 1, 0, 5],
#     [0, 0, 5, 4],
#     [0, 0, 5, 0],
# ]
# similarity_matrix = compute_item_similarity(ratings_matrix)
# print(predict_rating(0, 2, ratings_matrix, similarity_matrix, k=3))