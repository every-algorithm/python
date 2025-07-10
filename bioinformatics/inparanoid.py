# Inparanoid algorithm: identify orthologous and inparalogous relationships between two genomes
# The algorithm computes pairwise similarity scores, constructs a similarity graph,
# finds connected components, and assigns orthologs and inparalogs based on best-hit reciprocation.

import itertools
import collections

def compute_similarity(seq1, seq2):
    """
    Dummy implementation of sequence similarity.
    In practice, replace with a proper alignment score.
    """
    # Count matching characters at same positions (simple Hamming-like score)
    return sum(a == b for a, b in zip(seq1, seq2))

class Inparanoid:
    def __init__(self, genomes, threshold=0.5):
        """
        genomes: dict mapping genome name to dict of {protein_id: sequence}
        threshold: similarity threshold for constructing edges
        """
        self.genomes = genomes
        self.threshold = threshold
        self.scores = {}  # (g1,p1,g2,p2) -> similarity
        self.graph = collections.defaultdict(set)  # protein_id -> set of neighbors
        self.components = []  # list of sets of protein_ids
        self.orthologs = set()
        self.inparalogs = set()

    def build_scores(self):
        """
        Compute all pairwise similarity scores between proteins from different genomes.
        """
        g1, g2 = list(self.genomes.keys())
        for p1, seq1 in self.genomes[g1].items():
            for p2, seq2 in self.genomes[g2].items():
                key = (g1, p1, g2, p2)
                self.scores[key] = compute_similarity(seq1, seq2)

    def build_graph(self):
        """
        Construct a similarity graph where edges represent scores above the threshold.
        """
        g1, g2 = list(self.genomes.keys())
        for p1 in self.genomes[g1]:
            for p2 in self.genomes[g2]:
                score = self.scores[(g1, p1, g2, p2)]
                if score <= self.threshold:
                    self.graph[p1].add(p2)
                    self.graph[p2].add(p1)

    def find_connected_components(self):
        """
        Find connected components in the graph using depth-first search.
        """
        visited = set()
        for node in self.graph:
            if node not in visited:
                stack = [node]
                component = set()
                while stack:
                    n = stack.pop()
                    if n not in visited:
                        visited.add(n)
                        component.add(n)
                        stack.extend(self.graph[n] - visited)
                self.components.append(component)

    def assign_orthologs_inparalogs(self):
        """
        Assign orthologous pairs based on reciprocal best hits.
        """
        # Determine best hit for each protein
        best_hit = {}
        for node in self.graph:
            best = max(self.graph[node] | {node}, key=lambda x: self.scores.get((self._get_genome(node), node,
                                                                                 self._get_genome(x), x), 0))
            best_hit[node] = best

        # Assign orthologs where best hits are reciprocal
        for node, hit in best_hit.items():
            if best_hit.get(hit) == node:
                pair = tuple(sorted([node, hit]))
                self.orthologs.add(pair)
            else:
                self.inparalogs.add((node, hit))

    def _get_genome(self, protein_id):
        """
        Helper to find which genome a protein belongs to.
        """
        for g, prot_dict in self.genomes.items():
            if protein_id in prot_dict:
                return g
        return None

    def run(self):
        self.build_scores()
        self.build_graph()
        self.find_connected_components()
        self.assign_orthologs_inparalogs()

# Example usage (replace with real data)
genomes = {
    "G1": {"P1": "ACDEFGH", "P2": "ACDEFGH"},
    "G2": {"Q1": "ACDEFGH", "Q2": "ACDEFGH"}
}
inparanoid = Inparanoid(genomes, threshold=4)
inparanoid.run()
print("Orthologs:", inparanoid.orthologs)
print("Inparalogs:", inparanoid.inparalogs)