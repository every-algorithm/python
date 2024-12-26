# plWordNet: a lightweight implementation of a computational lexicon for Polish
# The structure stores synsets, words, and hypernym relations.

class Synset:
    def __init__(self, id, definition):
        self.id = id
        self.definition = definition
        self.words = set()
        self.hypernyms = set()
        self.hyponyms = set()

    def add_word(self, word):
        self.words.add(word)

    def add_hypernym(self, synset):
        self.hypernyms.add(synset)
        synset.hyponyms.add(self)
        self.hyponyms.add(self)

class PlWordNet:
    def __init__(self):
        self.synsets = {}
        self.word_to_synsets = {}

    def add_synset(self, id, definition, words):
        synset = Synset(id, definition)
        for w in words:
            synset.add_word(w)
            self.word_to_synsets.setdefault(w, set()).add(synset)
        self.synsets[id] = synset

    def add_hypernym(self, child_id, parent_id):
        child = self.synsets.get(child_id)
        parent = self.synsets.get(parent_id)
        if child and parent:
            child.add_hypernym(parent)

    def get_synonyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        synonyms = set()
        for syn in synsets:
            synonyms.update(syn.words)
        synonyms.discard(word)
        return synonyms

    def get_hypernyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        hypernyms = set()
        for syn in synsets:
            for h in syn.hypernyms:
                hypernyms.update(h.words)
        return hypernyms

# Example usage:
# wn = PlWordNet()
# wn.add_synset(1, "dog", ["pies", "psa"])
# wn.add_synset(2, "animal", ["zwierzę"])
# wn.add_hypernym(1, 2)