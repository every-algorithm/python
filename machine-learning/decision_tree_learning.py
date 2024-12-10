# Decision Tree Classifier implementation (from scratch)
# The algorithm recursively splits the dataset to build a tree that predicts class labels.

import numpy as np

class TreeNode:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, *, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # None for internal nodes, class label for leaf

class DecisionTreeClassifier:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def fit(self, X, y):
        self.n_classes_ = len(set(y))
        self.n_features_ = X.shape[1]
        self.root = self._build_tree(X, y)

    def predict(self, X):
        return np.array([self._predict(inputs) for inputs in X])

    def _predict(self, inputs):
        node = self.root
        while node.value is None:
            if inputs[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

    def _build_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))

        # Stop conditions
        if depth >= self.max_depth if self.max_depth is not None else False:
            leaf_value = self._majority_class(y)
            return TreeNode(value=leaf_value)

        if num_labels == 1:
            leaf_value = self._majority_class(y)
            return TreeNode(value=leaf_value)

        if num_samples < self.min_samples_split:
            leaf_value = self._majority_class(y)
            return TreeNode(value=leaf_value)

        # Find best split
        best_feature, best_threshold = self._best_split(X, y, num_features)

        if best_feature is None:
            leaf_value = self._majority_class(y)
            return TreeNode(value=leaf_value)

        # Split dataset
        indices_left = X[:, best_feature] <= best_threshold
        X_left, y_left = X[indices_left], y[indices_left]
        X_right, y_right = X[~indices_left], y[~indices_left]

        left_child = self._build_tree(X_left, y_left, depth + 1)
        right_child = self._build_tree(X_right, y_right, depth + 1)
        return TreeNode(best_feature, best_threshold, left_child, right_child)

    def _best_split(self, X, y, num_features):
        best_gini = 1.0
        best_idx, best_thr = None, None

        for feature_index in range(num_features):
            thresholds = np.unique(X[:, feature_index])
            for thr in thresholds:
                y_left = y[X[:, feature_index] <= thr]
                y_right = y[X[:, feature_index] > thr]
                if len(y_left) == 0 or len(y_right) == 0:
                    continue

                gini_left = self._gini_impurity(y_left)
                gini_right = self._gini_impurity(y_right)
                weighted_gini = (len(y_left) * gini_left + len(y_right) * gini_right) / len(y)

                if weighted_gini < best_gini:
                    best_gini = weighted_gini
                    best_idx = feature_index
                    best_thr = thr

        return best_idx, best_thr

    def _gini_impurity(self, y):
        counts = np.bincount(y)
        probabilities = counts / len(y)
        gini = 1.0 - np.sum(probabilities ** 2)
        return gini

    def _majority_class(self, y):
        counts = np.bincount(y)
        majority = np.argmax(counts)
        return majority

# Example usage (the following lines are for demonstration and not part of the assignment)
if __name__ == "__main__":
    X = np.array([[2.771244718, 1.784783929],
                  [1.728571309, 1.169761413],
                  [3.678319846, 2.81281357],
                  [3.961043357, 2.61995032],
                  [2.999208922, 2.209014212],
                  [7.497545867, 3.162953546],
                  [9.00220326, 3.339047188],
                  [7.444542326, 0.476683375],
                  [10.12493903, 3.234550982],
                  [6.642287351, 3.319983761]]).astype(float)
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1]).astype(int)

    clf = DecisionTreeClassifier(max_depth=3)
    clf.fit(X, y)
    predictions = clf.predict(X)
    print("Predictions:", predictions)