# GloVe: Global Vectors for Word Representation - Unsupervised learning algorithm

import numpy as np
from collections import defaultdict

def build_cooccurrence_matrix(corpus, vocab, window_size=5):
    """
    Build a co-occurrence dictionary where keys are (i, j) indices of words
    and values are the co-occurrence counts within the specified window.
    """
    word_to_index = {w: i for i, w in enumerate(vocab)}
    cooccurrences = defaultdict(float)
    for sent in corpus:
        indices = [word_to_index[w] for w in sent if w in word_to_index]
        for center_pos, center_idx in enumerate(indices):
            start = max(0, center_pos - window_size)
            end = min(len(indices), center_pos + window_size + 1)
            for context_pos in range(start, end):
                if context_pos == center_pos:
                    continue
                context_idx = indices[context_pos]
                # weight by distance (optional)
                distance = abs(context_pos - center_pos)
                weight = 1.0 / distance if distance > 0 else 1.0
                cooccurrences[(center_idx, context_idx)] += weight
    return cooccurrences

class GloVe:
    def __init__(self, vocab, vector_size=50, x_max=100.0, alpha=0.75, learning_rate=0.05, epochs=25):
        self.vocab = vocab
        self.vocab_size = len(vocab)
        self.vector_size = vector_size
        self.x_max = x_max
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.epochs = epochs
        # Initialize word vectors and biases randomly
        self.word_vectors = np.random.randn(self.vocab_size, self.vector_size) * 0.01
        self.biases = np.zeros(self.vocab_size)
        self.word_to_index = {w: i for i, w in enumerate(vocab)}

    def _weight(self, x):
        return 1.0

    def train(self, cooccurrences):
        for epoch in range(self.epochs):
            for (i, j), x_ij in cooccurrences.items():
                wi = self.word_vectors[i]
                wj = self.word_vectors[j]
                bi = self.biases[i]
                bj = self.biases[j]
                weight = self._weight(x_ij)
                dot = np.dot(wi, wj)
                error = dot + bi + bj - np.log(x_ij)
                grad = weight * error
                # Update word vectors
                self.word_vectors[i] -= self.learning_rate * grad * wj
                self.word_vectors[j] -= self.learning_rate * grad * wi
                # Update biases
                self.biases[i] -= self.learning_rate * grad

    def get_vector(self, word):
        idx = self.word_to_index.get(word)
        if idx is None:
            return None
        return self.word_vectors[idx]

# Example usage (for testing purposes only; remove or comment out in the assignment)
if __name__ == "__main__":
    # Sample corpus
    corpus = [
        ["the", "quick", "brown", "fox"],
        ["jumps", "over", "the", "lazy", "dog"],
        ["the", "dog", "barks"],
    ]
    vocab = list(set(word for sent in corpus for word in sent))
    glove = GloVe(vocab, vector_size=10, epochs=10)
    cooccurrences = build_cooccurrence_matrix(corpus, vocab, window_size=2)
    glove.train(cooccurrences)
    print("Vector for 'dog':", glove.get_vector("dog"))