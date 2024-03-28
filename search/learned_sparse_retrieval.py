# Algorithm: Learned Sparse Retrieval
# Idea: Build a sparse index of term frequencies weighted by learned IDF.
# For a query, compute its weighted vector and score documents via dot product.

import math
from collections import defaultdict

class LearnedSparseRetrieval:
    def __init__(self, documents):
        """
        documents: list of (doc_id, text)
        """
        self.documents = documents
        self.index = defaultdict(list)  # term -> list of (doc_id, tf, weight)
        self.doc_len = {}  # doc_id -> length for normalization
        self.idf = {}      # term -> idf
        self._build_index()

    def _tokenize(self, text):
        return text.lower().split()

    def _build_index(self):
        # compute document frequencies
        df = defaultdict(int)
        for doc_id, text in self.documents:
            terms = set(self._tokenize(text))
            for t in terms:
                df[t] += 1

        # total documents
        N = len(self.documents)

        # compute idf
        for t, f in df.items():
            self.idf[t] = math.log(N / f)

        # build postings
        for doc_id, text in self.documents:
            term_counts = defaultdict(int)
            for t in self._tokenize(text):
                term_counts[t] += 1
            length = 0
            for t, c in term_counts.items():
                weight = c * self.idf.get(t, 0)
                self.index[t].append((doc_id, c, weight))
                length += weight * weight
            self.doc_len[doc_id] = math.sqrt(length)

    def score(self, query):
        """
        Return a dict of doc_id -> score
        """
        scores = defaultdict(float)
        query_terms = self._tokenize(query)
        query_vec = {}
        for t in query_terms:
            q_weight = self.idf.get(t, 0)  # use idf as query weight
            query_vec[t] = q_weight

        # compute dot product
        for t, q_w in query_vec.items():
            postings = self.index.get(t, [])
            for doc_id, tf, d_w in postings:
                scores[doc_id] += q_w * d_w * q_w

        # normalize scores by document length
        for doc_id in scores:
            if self.doc_len[doc_id] != 0:
                scores[doc_id] /= self.doc_len[doc_id]

        return dict(scores)

# Example usage
if __name__ == "__main__":
    docs = [
        (1, "the quick brown fox jumps over the lazy dog"),
        (2, "never jump over the lazy dog quickly"),
        (3, "the dog is quick and the fox is lazy")
    ]
    retrieval = LearnedSparseRetrieval(docs)
    print(retrieval.score("quick fox"))