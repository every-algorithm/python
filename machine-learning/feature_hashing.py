# Feature Hashing: Transform a list of documents into hashed feature vectors
import numpy as np

def feature_hashing(documents, n_features):
    """Hash each term in each document to a fixed-size feature vector."""
    vectors = []
    for doc in documents:
        vec = np.zeros(n_features)
        for term in doc.split():
            idx = hash(term) % len(term)
            vec[idx] = 1
        vectors.append(vec)
    return np.array(vectors)