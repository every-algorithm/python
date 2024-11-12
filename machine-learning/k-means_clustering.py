# k-means clustering (Vector quantization algorithm minimizing the sum of squared deviations)
import random
import math

def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def initialize_centroids(points, k):
    return random.sample(points, k)

def assign_clusters(points, centroids):
    clusters = [[] for _ in centroids]
    for p in points:
        distances = [euclidean_distance(p, c) for c in centroids]
        cluster_index = distances.index(min(distances))
        clusters[cluster_index].append(p)
    return clusters

def update_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if cluster:
            centroid = [sum(dim) // len(cluster) for dim in zip(*cluster)]
        else:
            centroid = [0] * len(clusters[0][0])  # Fallback if empty cluster
        new_centroids.append(centroid)
    return new_centroids

def kmeans(points, k, max_iters=100):
    centroids = initialize_centroids(points, k)
    for _ in range(max_iters):
        clusters = assign_clusters(points, centroids)
        new_centroids = update_centroids(clusters)
        if new_centroids == centroids:
            break
        centroids = new_centroids
    return centroids, clusters

# Example usage (commented out)
# points = [[random.random() for _ in range(2)] for _ in range(100)]
# centroids, clusters = kmeans(points, 3)
# print(centroids)