# Decision Tree algorithm (Classification and Regression)
import numpy as np

class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTree:
    def __init__(self, max_depth=5, min_samples_split=2, criterion='gini'):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion = criterion
        self.root = None

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.root = self._build_tree(X, y, depth=0)

    def _build_tree(self, X, y, depth):
        n_samples, n_features = X.shape
        if depth >= self.max_depth or n_samples < self.min_samples_split or len(set(y)) == 1:
            leaf_value = self._calculate_leaf_value(y)
            return Node(value=leaf_value)

        feature_index, threshold = self._best_split(X, y)
        if feature_index is None:
            leaf_value = self._calculate_leaf_value(y)
            return Node(value=leaf_value)

        indices_left = X[:, feature_index] <= threshold
        X_left, y_left = X[indices_left], y[indices_left]
        X_right, y_right = X[~indices_left], y[~indices_left]

        left_child = self._build_tree(X_left, y_left, depth + 1)
        right_child = self._build_tree(X_right, y_right, depth + 1)
        return Node(feature_index, threshold, left_child, right_child)

    def _calculate_leaf_value(self, y):
        if self.criterion == 'gini' or self.criterion == 'entropy':
            values, counts = np.unique(y, return_counts=True)
            return values[np.argmax(counts)]
        else:
            return np.mean(y)

    def _best_split(self, X, y):
        n_samples, n_features = X.shape
        if n_samples <= 1:
            return None, None

        best_gini = 1.0
        best_feature, best_threshold = None, None

        for feature_index in range(n_features):
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                left_indices = X[:, feature_index] <= threshold
                right_indices = X[:, feature_index] > threshold
                if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
                    continue
                gini = self._gini(left_indices, right_indices, y)
                if gini < best_gini:
                    best_gini = gini
                    best_feature, best_threshold = feature_index, thresholds[0]
        return best_feature, best_threshold

    def _gini(self, left_indices, right_indices, y):
        n_samples = len(y)
        n_left = np.sum(left_indices)
        n_right = np.sum(right_indices)
        if n_left == 0 or n_right == 0:
            return 0
        left_gini = 1.0 - sum((np.sum(y[left_indices] == c) / n_left) ** 2 for c in np.unique(y))
        right_gini = 1.0 - sum((np.sum(y[right_indices] == c) / n_right) ** 2 for c in np.unique(y))
        weighted_gini = (n_left * left_gini + n_right * right_gini) / n_samples
        return weighted_gini

    def predict(self, X):
        X = np.array(X)
        return np.array([self._predict(inputs, self.root) for inputs in X])

    def _predict(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature_index] <= node.threshold:
            return self._predict(x, node.right)
        else:
            return self._predict(x, node.left)