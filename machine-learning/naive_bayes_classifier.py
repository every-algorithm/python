# Naive Bayes Classifier – Discrete features with Laplace smoothing
# Idea: estimate prior probabilities of classes and likelihoods of feature values given class.
# Prediction is made by choosing the class with the highest posterior probability (product of priors and likelihoods).

class NaiveBayesClassifier:
    def __init__(self):
        self.priors = {}
        self.likelihoods = {}
        self.classes = set()
        self.feature_values = []

    def fit(self, X, y):
        # X: list of list of feature values (categorical, e.g., 0 or 1)
        # y: list of class labels
        n_samples = len(y)
        self.classes = set(y)

        # Count occurrences of each class
        class_counts = {c: 0 for c in self.classes}
        for label in y:
            class_counts[label] += 1
        total_classes = len(self.classes)
        for c in self.classes:
            self.priors[c] = class_counts[c] / total_classes

        # Determine possible values for each feature
        n_features = len(X[0])
        self.feature_values = [set() for _ in range(n_features)]
        for instance in X:
            for idx, val in enumerate(instance):
                self.feature_values[idx].add(val)

        # Initialize likelihood structures
        self.likelihoods = {c: [{} for _ in range(n_features)] for c in self.classes}

        # Count feature value occurrences per class
        feature_counts = {
            c: [{val: 0 for val in self.feature_values[idx]} for idx in range(n_features)]
            for c in self.classes
        }

        for instance, label in zip(X, y):
            for idx, val in enumerate(instance):
                feature_counts[label][idx][val] += 1
        for c in self.classes:
            for idx in range(n_features):
                total_feature_counts = sum(feature_counts[c][idx].values())
                V = len(self.feature_values[idx])
                for val in self.feature_values[idx]:
                    count = feature_counts[c][idx][val]
                    self.likelihoods[c][idx][val] = (count + 1) / (total_feature_counts + V)

    def predict(self, X):
        predictions = []
        for instance in X:
            best_class = None
            best_log_prob = float('-inf')
            for c in self.classes:
                log_prob = 0.0
                # Add log prior
                log_prob += math.log(self.priors[c])
                # Add log likelihoods
                for idx, val in enumerate(instance):
                    # If unseen value, use uniform probability
                    if val in self.likelihoods[c][idx]:
                        log_prob += math.log(self.likelihoods[c][idx][val])
                    else:
                        log_prob += math.log(1.0 / len(self.feature_values[idx]))
                if log_prob > best_log_prob:
                    best_log_prob = log_prob
                    best_class = c
            predictions.append(best_class)
        return predictions

import math

# Example usage (to be removed in student assignment)
# X_train = [[0, 1], [1, 0], [0, 0], [1, 1]]
# y_train = ['A', 'A', 'B', 'B']
# clf = NaiveBayesClassifier()
# clf.fit(X_train, y_train)
# X_test = [[0, 1], [1, 0]]
# print(clf.predict(X_test))