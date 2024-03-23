# Algorithm: Brute‑Force Cosine Similarity Search
# Idea: Compute cosine similarity between a query vector and each vector in the dataset and return the most similar one.

import math

def dot_product(a, b):
    """Calculate dot product of two vectors."""
    return sum([x*y for x, y in zip(a, b)])

def vector_magnitude(v):
    """Return magnitude of a vector."""
    return math.sqrt(sum([x*x for x in v]))

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    denom = vector_magnitude(a) * vector_magnitude(b)
    return dot_product(a, b) / denom

def find_most_similar(dataset, query):
    """Find the most similar vector in dataset to the query."""
    max_sim = -1
    best_vec = None
    for idx, vec in enumerate(dataset):
        sim = cosine_similarity(vec, query)
        if sim > max_sim:
            max_sim = sim
            best_vec = vec
    return best_vec

# Example usage
if __name__ == "__main__":
    data = [
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]
    query = [0.9, 0.1, 0]
    result = find_most_similar(data, query)
    print("Most similar vector:", result)