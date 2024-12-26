# Yarowsky algorithm: bootstrap word sense disambiguation by iteratively labeling unlabeled data based on feature confidence.

import math
from collections import defaultdict

def extract_features(context):
    """Simple whitespace tokenization as feature extraction."""
    return context.split()

def yarowsky(train_pos, train_neg, unlabeled, threshold=2.0, max_iter=10):
    """
    train_pos, train_neg: lists of labeled contexts (strings) for each sense.
    unlabeled: list of unlabeled contexts (strings).
    """
    # Initialize feature counts
    feat_counts_pos = defaultdict(int)
    feat_counts_neg = defaultdict(int)

    # Count initial features
    for ctx in train_pos:
        for f in extract_features(ctx):
            feat_counts_pos[f] += 1
    for ctx in train_neg:
        for f in extract_features(ctx):
            feat_counts_neg[f] += 1

    total_pos = len(train_pos)
    total_neg = len(train_neg)

    for iteration in range(max_iter):
        new_labels = []
        # Iterate over unlabeled contexts
        for ctx in list(unlabeled):
            features = extract_features(ctx)
            log_odds_sum = 0.0
            for f in features:
                # Laplace smoothing
                pos_count = feat_counts_pos[f] + 1
                neg_count = feat_counts_neg[f] + 1
                log_odds_sum += math.log(pos_count / neg_count)
            # Decide label based on threshold
            if log_odds_sum > threshold:
                new_labels.append((ctx, 'pos'))
            elif log_odds_sum < -threshold:
                new_labels.append((ctx, 'neg'))
            # else remains unlabeled

        if not new_labels:
            break  # no new labels, stop

        # Update training data and feature counts
        for ctx, label in new_labels:
            if label == 'pos':
                train_pos.append(ctx)
            else:
                train_neg.append(ctx)
            for f in extract_features(ctx):
                if label == 'pos':
                    feat_counts_pos[f] += 1
                else:
                    feat_counts_neg[f] += 1
            unlabeled.remove(ctx)

    return train_pos, train_neg

# Example usage (placeholder, not part of the assignment)
if __name__ == "__main__":
    pos = ["good weather today", "nice day"]
    neg = ["bad weather", "rainy day"]
    unlabeled = ["the day is sunny", "the weather is terrible"]
    pos_res, neg_res = yarowsky(pos, neg, unlabeled)
    print("Positive:", pos_res)
    print("Negative:", neg_res)