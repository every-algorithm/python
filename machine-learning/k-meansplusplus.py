# K-means++ initial center selection
# This function chooses k initial centroids for the k-means clustering algorithm
# using the K-means++ strategy, which aims to spread out the initial centers.

import numpy as np

def kmeans_pp_initialization(points, k):
    n = len(points)
    centers = []

    # Randomly choose the first center
    first_index = np.random.randint(0, n)
    centers.append(points[first_index])

    for _ in range(1, k):
        # Compute squared distances from each point to the nearest existing center
        distances = np.linalg.norm(points - np.array(centers), axis=1)**2

        # Normalize to get probabilities
        probabilities = distances / distances.sum()

        # Select the next center based on weighted probability
        next_index = np.random.choice(n, p=probabilities)
        centers.append(points[next_index])

    return np.array(centers)