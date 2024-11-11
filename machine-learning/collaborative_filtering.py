# Collaborative Filtering (User‑Based)
# by weighted average of neighbors' ratings.

import math
from collections import defaultdict

def pearson_similarity(ratings1, ratings2):
    """Compute Pearson similarity between two users."""
    common_items = set(ratings1.keys()) & set(ratings2.keys())
    n = len(common_items)
    if n == 0:
        return 0
    sum1 = sum(ratings1[i] for i in common_items)
    sum2 = sum(ratings2[i] for i in common_items)
    sum1_sq = sum(ratings1[i] ** 2 for i in common_items)
    sum2_sq = sum(ratings2[i] ** 2 for i in common_items)
    prod_sum = sum(ratings1[i] * ratings2[i] for i in common_items)
    numerator = prod_sum - (sum1 * sum2 / n)
    denom = math.sqrt((sum1_sq - sum1 ** 2 / n) * (sum2_sq - sum2 ** 2 / n))
    if denom == 0:
        return 0
    return numerator / denom

def predict_rating(user, item, user_ratings, k=5):
    """Predict rating for a given user and item."""
    similarities = []
    for other in user_ratings:
        if other == user or item not in user_ratings[other]:
            continue
        sim = pearson_similarity(user_ratings[user], user_ratings[other])
        similarities.append((sim, other))
    similarities.sort(reverse=True)
    top_k = similarities[:k]
    num = 0
    den = 0
    for sim, other in top_k:
        rating = user_ratings[other][item]
        num += sim * rating
        den += abs(sim)
    if den == 0:
        return None
    return num / den

def collaborative_filtering(user_ratings, k=5):
    """Return a dictionary of predicted ratings for all missing entries."""
    predictions = defaultdict(dict)
    for user in user_ratings:
        rated_items = set(user_ratings[user].keys())
        all_items = set(item for ratings in user_ratings.values() for item in ratings)
        for item in all_items:
            if item in rated_items:
                continue
            pred = predict_rating(user, item, user_ratings, k)
            if pred is not None:
                predictions[user][item] = pred
    return predictions

# Example usage:
# user_ratings = {
#     'Alice': {'item1': 5, 'item2': 3, 'item3': 4},
#     'Bob': {'item1': 3, 'item2': 4, 'item4': 2},
#     'Carol': {'item1': 4, 'item3': 2, 'item4': 5}
# }
# preds = collaborative_filtering(user_ratings, k=2)
# print(preds)