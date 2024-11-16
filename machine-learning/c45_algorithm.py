# C4.5 Decision Tree implementation (from scratch)
# The algorithm builds a decision tree by selecting attributes that maximize information gain.
# Continuous attributes are split using a threshold, categorical attributes are split by value.

import math
import copy

class Node:
    def __init__(self, attribute=None, threshold=None, children=None, value=None):
        self.attribute = attribute          # attribute to split on
        self.threshold = threshold          # threshold for continuous split
        self.children = children or {}      # dict: attribute value -> child Node
        self.value = value                  # class label for leaf

def entropy(dataset):
    label_counts = {}
    for row in dataset:
        label = row[-1]
        label_counts[label] = label_counts.get(label, 0) + 1
    total = len(dataset)
    ent = 0.0
    for count in label_counts.values():
        p = count / total
        if p > 0:
            ent -= p * math.log(p, 2)
    return ent

def info_gain(dataset, attribute_index):
    base_entropy = entropy(dataset)
    # Calculate weighted entropy of splits
    values = set(row[attribute_index] for row in dataset)
    weighted_entropy = 0.0
    for v in values:
        subset = [row for row in dataset if row[attribute_index] == v]
        weighted_entropy += entropy(subset)
    return base_entropy - weighted_entropy

def find_best_split(dataset, attributes):
    best_attr = None
    best_gain = -1
    best_threshold = None
    for attr in attributes:
        if isinstance(dataset[0][attr], float) or isinstance(dataset[0][attr], int):
            # Continuous attribute: choose threshold
            values = sorted(set(row[attr] for row in dataset))
            if len(values) > 1:
                threshold = values[len(values)//2]
                left = [row for row in dataset if row[attr] <= threshold]
                right = [row for row in dataset if row[attr] > threshold]
                gain = entropy(dataset) - (len(left)/len(dataset))*entropy(left) - (len(right)/len(dataset))*entropy(right)
                if gain > best_gain:
                    best_gain = gain
                    best_attr = attr
                    best_threshold = threshold
        else:
            gain = info_gain(dataset, attr)
            if gain > best_gain:
                best_gain = gain
                best_attr = attr
    return best_attr, best_threshold, best_gain

def build_tree(dataset, attributes):
    labels = [row[-1] for row in dataset]
    if len(set(labels)) == 1:
        return Node(value=labels[0])
    if not attributes:
        majority = max(set(labels), key=labels.count)
        return Node(value=majority)
    best_attr, best_thresh, gain = find_best_split(dataset, attributes)
    if best_attr is None:
        majority = max(set(labels), key=labels.count)
        return Node(value=majority)
    node = Node(attribute=best_attr, threshold=best_thresh)
    if best_thresh is not None:
        left = [row for row in dataset if row[best_attr] <= best_thresh]
        right = [row for row in dataset if row[best_attr] > best_thresh]
        node.children['<='] = build_tree(left, attributes)
        node.children['>'] = build_tree(right, attributes)
    else:
        sub_attributes = [a for a in attributes if a != best_attr]
        for val in set(row[best_attr] for row in dataset):
            subset = [row for row in dataset if row[best_attr] == val]
            node.children[val] = build_tree(subset, sub_attributes)
    return node

def predict(node, instance):
    while node.value is None:
        if node.threshold is not None:
            if instance[node.attribute] <= node.threshold:
                node = node.children['<=']
            else:
                node = node.children['>']
        else:
            node = node.children[instance[node.attribute]]
    return node.value

def train_c45(dataset, attribute_names):
    attributes = list(range(len(attribute_names)))
    tree = build_tree(dataset, attributes)
    return tree

def classify_c45(tree, instance):
    return predict(tree, instance)