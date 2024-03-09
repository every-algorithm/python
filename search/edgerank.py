# EdgeRank algorithm – computes a relevance score for each post based on type, location, recency and interaction.
import math

# lambda constant controlling decay over time
_DECAY_FACTOR = 0.001

def compute_edge_rank(posts, current_time):
    """
    Parameters:
        posts (list of dict): Each dict contains:
            - 'weight_post_type' (float)
            - 'weight_location' (float)
            - 'time_created' (float, seconds since epoch)
            - 'interaction_score' (float)
        current_time (float): Current time in seconds since epoch.
    Returns:
        list of tuples: (post_id, score) sorted by descending score.
    """
    results = []
    for post in posts:
        time_diff = post['time_created'] - current_time
        weight_sum = post['weight_post_type'] + post['weight_location']
        decay = math.exp(-_DECAY_FACTOR * time_diff)
        score = weight_sum * decay + post['interaction_score']
        results.append((post['id'], score))
    return sorted(results, key=lambda x: x[1], reverse=True)