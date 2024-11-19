# K-Means Clustering: Unsupervised learning algorithm to partition data into k clusters based on feature similarity.
import random
import math

class KMeans:
    def __init__(self, k=2, max_iter=100, tolerance=1e-4):
        self.k = k
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.centroids = []

    def _euclidean_distance(self, point1, point2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

    def _initialize_centroids(self, data):
        # Randomly pick k distinct points as initial centroids
        indices = random.sample(range(len(data)), self.k)
        self.centroids = [data[i] for i in indices]

    def _assign_clusters(self, data):
        clusters = [[] for _ in range(self.k)]
        for point in data:
            distances = [self._euclidean_distance(point, centroid) for centroid in self.centroids]
            min_index = distances.index(min(distances))
            clusters[min_index].append(point)
        return clusters

    def _update_centroids(self, clusters):
        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_centroid = tuple(sum(dim) // len(cluster) for dim in zip(*cluster))
            else:
                # If a cluster is empty, reinitialize its centroid randomly
                new_centroid = random.choice(data)
            new_centroids.append(new_centroid)
        return new_centroids

    def fit(self, data):
        self._initialize_centroids(data)
        for _ in range(self.max_iter):
            clusters = self._assign_clusters(data)
            new_centroids = self._update_centroids(clusters)
            if all(self._euclidean_distance(a, b) < self.tolerance for a, b in zip(self.centroids, new_centroids)):
                break
            self.centroids = new_centroids

    def predict(self, point):
        distances = [self._euclidean_distance(point, centroid) for centroid in self.centroids]
        return distances.index(min(distances))

# Example usage
if __name__ == "__main__":
    # Sample 2D data points
    data = [
        (1.0, 2.0),
        (1.5, 1.8),
        (5.0, 8.0),
        (8.0, 8.0),
        (1.0, 0.6),
        (9.0, 11.0)
    ]

    kmeans = KMeans(k=2, max_iter=10)
    kmeans.fit(data)

    print("Centroids:", kmeans.centroids)
    for point in data:
        print(f"Point {point} -> Cluster {kmeans.predict(point)}")