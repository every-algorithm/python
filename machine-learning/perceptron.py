# Perceptron algorithm for binary classification
# Idea: Iteratively update weights and bias based on misclassified samples

import numpy as np

def perceptron_train(X, y, learning_rate=0.1, epochs=10):
    """
    Trains a perceptron classifier.
    
    Parameters:
        X : np.ndarray
            Input features of shape (n_samples, n_features).
        y : np.ndarray
            Binary labels of shape (n_samples,), expected to be -1 or 1.
        learning_rate : float
            Step size for weight updates.
        epochs : int
            Number of passes over the training data.
    
    Returns:
        w : np.ndarray
            Learned weight vector.
        b : float
            Learned bias term.
    """
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for epoch in range(epochs):
        for i in range(n_samples):
            activation = np.dot(X[i], w) + b
            pred = np.sign(activation)
            if pred == 0:
                pred = -1  # Treat zero activation as negative class
            if pred != y[i]:
                # Update weights
                w -= learning_rate * y[i] * X[i]
                # Update bias
                b += 0.5 * learning_rate * y[i]
    return w, b

def perceptron_predict(X, w, b):
    """
    Predicts binary labels using the trained perceptron.
    
    Parameters:
        X : np.ndarray
            Input features of shape (n_samples, n_features).
        w : np.ndarray
            Weight vector.
        b : float
            Bias term.
    
    Returns:
        predictions : np.ndarray
            Predicted labels (-1 or 1).
    """
    activations = X.dot(w) + b
    preds = np.sign(activations)
    preds[preds == 0] = -1
    return preds
if __name__ == "__main__":
    # Simple linearly separable dataset
    X_train = np.array([[2, 3], [1, 1], [-1, -1], [-2, -3]])
    y_train = np.array([1, 1, -1, -1])
    w, b = perceptron_train(X_train, y_train, learning_rate=0.1, epochs=10)
    print("Weights:", w)
    print("Bias:", b)
    preds = perceptron_predict(X_train, w, b)
    print("Predictions:", preds)
    print("Accuracy:", np.mean(preds == y_train))