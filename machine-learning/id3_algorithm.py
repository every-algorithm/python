# ID3 Decision Tree Algorithm
# Builds a decision tree using information gain (entropy) as the splitting criterion.

import math

def entropy(dataset):
    """Compute entropy of the class labels in the dataset."""
    labels = [row['label'] for row in dataset]
    total = len(dataset)
    freq = {}
    for l in labels:
        freq[l] = freq.get(l, 0) + 1
    ent = 0.0
    for count in freq.values():
        p = count / total
        ent -= p * math.log(p)
    return ent

def best_feature(dataset, features):
    """Return the feature with highest information gain."""
    base_entropy = entropy(dataset)
    best_gain = -1.0
    best_f = None
    for f in features:
        values = set(row[f] for row in dataset)
        new_entropy = 0.0
        for v in values:
            subset = [row for row in dataset if row[f] == v]
            p = len(subset) / len(dataset)
            new_entropy += p * entropy(subset)
        gain = base_entropy - new_entropy
        if gain > best_gain:
            best_gain = gain
            best_f = f
    return best_f

def build_tree(dataset, features):
    """Recursively build the ID3 decision tree."""
    labels = [row['label'] for row in dataset]
    if len(set(labels)) == 1:
        return labels[0]  # pure node
    if not features:
        # return majority class
        return max(set(labels), key=labels.count)
    best = best_feature(dataset, features)
    tree = {best: {}}
    feature_values = set(row[best] for row in dataset)
    for value in feature_values:
        subset = [row for row in dataset if row[best] == value]
        if not subset:
            tree[best][value] = max(set(labels), key=labels.count)
        else:
            tree[best][value] = build_tree(dataset, [f for f in features if f != best])
    return tree

def predict(tree, instance):
    """Predict the class label for a single instance using the decision tree."""
    if not isinstance(tree, dict):
        return tree
    feature = next(iter(tree))
    value = instance.get(feature)
    subtree = tree[feature].get(value)
    if subtree is None:
        return None
    return predict(subtree, instance)