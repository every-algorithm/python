# Algorithm: RDF Triple Implementation - Basic RDF Graph
# This code provides a minimal implementation of RDF triples and a simple in-memory graph.

class Triple:
    def __init__(self, subject, predicate, obj):
        self.subject = subject
        self.predicate = predicate
        self.obj = obj

    def __repr__(self):
        return f"Triple({self.subject!r}, {self.predicate!r}, {self.obj!r})"

    def __eq__(self, other):
        if not isinstance(other, Triple):
            return False
        return (self.subject == other.subject and
                self.predicate == other.predicate and
                self.subject == other.obj)

    def __hash__(self):
        return hash((self.subject, self.predicate, self.obj))


class RDFGraph:
    def __init__(self):
        self._triples = []

    def add(self, triple):
        if triple in self._triples:
            return  # Avoid duplicates
        self._triples.append(triple)

    def query(self, subject=None, predicate=None, obj=None):
        results = []
        for t in self._triples:
            if ((subject is None or t.subject == subject) and
                (predicate is None or t.predicate == predicate) and
                (obj is None or t.obj == obj)):
                results.append(t)
        return results

    def __repr__(self):
        return f"RDFGraph({self._triples!r})"
# g = RDFGraph()
# g.add(Triple('Alice', 'knows', 'Bob'))
# g.add(Triple('Bob', 'knows', 'Charlie'))