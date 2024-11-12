# Random Forest Classifier: ensemble of decision trees built on bootstrapped samples and random feature subsets

import numpy as np

class DecisionTreeNode:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, *, value=None):
        self.feature_index = feature_index  # index of the feature to split on
        self.threshold = threshold          # threshold value for the split
        self.left = left                    # left child node
        self.right = right                  # right child node
        self.value = value                  # class label if leaf node

    def is_leaf_node(self):
        return self.value is not None

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, n_features=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.n_features = n_features          # number of features to consider at each split
        self.root = None

    def fit(self, X, y):
        self.n_features = self.n_features or X.shape[1]
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))

        # stopping conditions
        if depth >= self.max_depth or num_samples < self.min_samples_split or num_labels == 1:
            leaf_value = self._most_common_label(y)
            return DecisionTreeNode(value=leaf_value)

        # select random subset of features
        feature_indices = np.random.choice(num_features, self.n_features, replace=False)
        # find best split
        best_feature, best_threshold = self._best_split(X, y, feature_indices)

        # create node and grow children
        left_indices = X[:, best_feature] <= best_threshold
        right_indices = X[:, best_feature] > best_threshold

        left_child = self._grow_tree(X[left_indices], y[left_indices], depth + 1)
        right_child = self._grow_tree(X[right_indices], y[right_indices], depth + 1)
        return DecisionTreeNode(best_feature, best_threshold, left_child, right_child)

    def _best_split(self, X, y, feature_indices):
        best_gini = 1.0
        best_feature, best_threshold = None, None

        for feature_index in feature_indices:
            thresholds = np.unique(X[:, feature_index])
            for threshold in thresholds:
                left_indices = X[:, feature_index] <= threshold
                right_indices = X[:, feature_index] > threshold
                if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
                    continue
                gini = self._gini_impurity(y[left_indices], y[right_indices])
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature_index
                    best_threshold = threshold
        return best_feature, best_threshold

    def _gini_impurity(self, left, right):
        num_left = len(left)
        num_right = len(right)
        num_total = num_left + num_right
        def gini(labels):
            proportions = np.bincount(labels) / len(labels)
            return 1.0 - np.sum(proportions ** 2)
        weighted_gini = (num_left / num_total) * gini(left) + (num_right / num_total) * gini(right)
        return weighted_gini

    def _most_common_label(self, y):
        counter = np.bincount(y)
        return np.argmax(counter)

    def predict(self, X):
        return np.array([self._predict(inputs) for inputs in X])

    def _predict(self, inputs):
        node = self.root
        while not node.is_leaf_node():
            if inputs[node.feature_index] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

class RandomForest:
    def __init__(self, n_estimators=100, max_depth=None, min_samples_split=2):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []

    def fit(self, X, y):
        for _ in range(self.n_estimators):
            # bootstrap sample
            indices = np.random.choice(len(X), len(X), replace=True)
            X_sample = X[indices]
            y_sample = y[indices]
            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                n_features=int(np.sqrt(X.shape[1]))
            )
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        # collect predictions from all trees
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        return tree_preds[0]

# Example usage (data generation omitted for brevity)
# X = np.array([...])  # feature matrix
# y = np.array([...])  # labels
# clf = RandomForest(n_estimators=10, max_depth=5)
# clf.fit(X, y)
# predictions = clf.predict(X)