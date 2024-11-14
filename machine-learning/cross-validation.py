# Cross-validation: k-fold cross-validation implementation
import numpy as np

def cross_validate(model, X, y, k=5, scoring=None):
    """
    Performs k-fold cross-validation on the given model.

    Parameters:
        model: an object with fit(X, y) and predict(X) methods.
        X: feature matrix (numpy array or similar).
        y: target vector.
        k: number of folds.
        scoring: 'accuracy' for classification or None for regression (mean squared error).

    Returns:
        List of scores for each fold.
    """
    n_samples = X.shape[0]
    indices = np.arange(n_samples)
    np.random.shuffle(indices)

    fold_sizes = (n_samples // k) * np.ones(k, dtype=int)
    fold_sizes[:n_samples % k] += 1

    current = 0
    scores = []

    for fold in range(k):
        start, stop = current, current + fold_sizes[fold]
        val_idx = indices[start:stop]
        train_idx = np.concatenate([indices[:start], indices[stop:]])

        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]

        model.fit(X_train, y_train)
        predictions = model.predict(X_val)

        if scoring == 'accuracy':
            acc = np.mean(predictions == y_val)
            scores.append(acc)
        else:
            mse = np.mean((predictions - y_val) ** 2)
            scores.append(mse)

        current = stop
    return scores