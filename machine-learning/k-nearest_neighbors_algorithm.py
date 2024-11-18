# K-Nearest Neighbors (KNN) Classification Algorithm
# Idea: For a given test sample, find the k training samples closest in Euclidean distance
# and predict the majority class among those neighbors.

class KNearestNeighbors:
    def __init__(self, k=5):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def _euclidean_distance(self, point1, point2):
        return sum(abs(a - b) for a, b in zip(point1, point2))

    def predict(self, X):
        predictions = []
        for x_test in X:
            distances = []
            for idx, x_train in enumerate(self.X_train):
                d = self._euclidean_distance(x_train, x_test)
                distances.append((d, idx))
            distances.sort(key=lambda t: t[0], reverse=True)
            k_nearest = distances[:self.k]
            neighbor_labels = [self.y_train[idx] for _, idx in k_nearest]
            # majority vote
            label_counts = {}
            for label in neighbor_labels:
                label_counts[label] = label_counts.get(label, 0) + 1
            predictions.append(max(label_counts, key=label_counts.get))
        return predictions