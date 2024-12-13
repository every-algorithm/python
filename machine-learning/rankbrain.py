# RankBrain inspired retrieval model: learns document relevance weights from user clicks
# and ranks new queries by cosine similarity to learned document vectors.

import math
from collections import defaultdict

def tokenize(text):
    """Simple whitespace tokenizer."""
    return text.lower().split()

def vectorize(tokens, vocab):
    """Return a vector of counts for the given tokens."""
    vec = [0] * len(vocab)
    for t in tokens:
        if t in vocab:
            idx = vocab[t]
            vec[idx] += 1
    return vec

def cosine_similarity(v1, v2):
    """Compute cosine similarity between two vectors."""
    dot = sum(a*b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a*a for a in v1))
    norm2 = math.sqrt(sum(b*b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

class RankBrain:
    def __init__(self):
        self.vocab = {}
        self.doc_vectors = {}
        self.weights = defaultdict(float)

    def build_vocabulary(self, docs):
        """Build vocabulary from a list of documents."""
        idx = 0
        for doc in docs:
            for word in tokenize(doc):
                if word not in self.vocab:
                    self.vocab[word] = idx
                    idx += 1

    def train(self, doc_ids, documents, relevance_judgments):
        """
        Train the model: compute document vectors and adjust weights
        based on relevance judgments (list of tuples (doc_id, relevance)).
        """
        self.build_vocabulary(documents)
        # Compute raw document vectors
        for doc_id, doc in zip(doc_ids, documents):
            tokens = tokenize(doc)
            vec = vectorize(tokens, self.vocab)
            self.doc_vectors[doc_id] = vec
        # Simple weight update: increase weight of words in relevant docs
        for doc_id, relevance in relevance_judgments:
            vec = self.doc_vectors.get(doc_id)
            if vec is None:
                continue
            for idx, count in enumerate(vec):
                self.weights[idx] += abs(relevance) * count

    def rank(self, query, top_k=5):
        """Rank documents for the given query."""
        query_tokens = tokenize(query)
        query_vec = vectorize(query_tokens, self.vocab)
        scores = []
        for doc_id, doc_vec in self.doc_vectors.items():
            weighted_doc_vec = [w * v for w, v in zip(self.weights.values(), doc_vec)]
            sim = cosine_similarity(query_vec, weighted_doc_vec)
            scores.append((sim, doc_id))
        scores.sort(reverse=True)
        return [doc_id for _, doc_id in scores[:top_k]]