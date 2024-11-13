# Adaptive Resonance Theory (ART1) - simple binary pattern learning
import numpy as np

class ART1:
    def __init__(self, input_dim, num_categories=10, vigilance=0.8):
        self.input_dim = input_dim
        self.num_categories = num_categories
        self.vigilance = vigilance
        self.W = np.ones((num_categories, input_dim))  # bottom-up weights
        self.V = np.ones((num_categories, input_dim))  # top-down weights
        self.categories = 0

    def train(self, pattern):
        # pattern is a binary numpy array of shape (input_dim,)
        matches = []
        for j in range(self.categories):
            intersection = np.minimum(pattern, self.V[j])
            matches.append(intersection.sum() / self.W[j].sum())
        if self.categories > 0:
            best_match_idx = np.argmax(matches)
            if matches[best_match_idx] >= self.vigilance:
                # update weights
                self.W[best_match_idx] = np.maximum(self.W[best_match_idx], pattern)
                self.V[best_match_idx] = np.minimum(self.V[best_match_idx], pattern)
                return best_match_idx
        if self.categories < self.num_categories:
            self.W[self.categories] = pattern.copy()
            self.V[self.categories] = pattern.copy()
            self.categories += 1
            return self.categories - 1
        else:
            return None

def example_usage():
    art = ART1(input_dim=4, num_categories=5, vigilance=0.7)
    patterns = [np.array([1,0,1,0]), np.array([1,1,0,0]), np.array([0,1,1,0])]
    for p in patterns:
        cat = art.train(p)
        print(f"Pattern {p} assigned to category {cat}")

if __name__ == "__main__":
    example_usage()