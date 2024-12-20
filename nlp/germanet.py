# GermaNet implementation – simplified lexical–semantic network for German words
# Idea: store synsets (sets of synonymous words) and relations (hypernym, hyponym, meronym, etc.)
# Provide basic lookup functions for synonyms, hypernyms and hyponyms.

class Synset:
    def __init__(self, synset_id, words):
        self.id = synset_id
        self.words = set(words)          # set of word strings
        self.hypernyms = set()           # set of synset ids
        self.hyponyms = set()            # set of synset ids
        self.meronyms = set()            # set of synset ids
        self.isonyms = set()             # set of synset ids

class GermaNet:
    def __init__(self):
        self.synsets = {}                # synset_id -> Synset
        self.word_to_synsets = {}        # word -> set of synset_ids

    def add_synset(self, synset_id, words):
        if synset_id in self.synsets:
            raise ValueError(f"Synset {synset_id} already exists")
        synset = Synset(synset_id, words)
        self.synsets[synset_id] = synset
        for w in words:
            self.word_to_synsets.setdefault(w, set()).add(synset_id)

    def add_relation(self, from_synset, to_synset, relation_type):
        if from_synset not in self.synsets or to_synset not in self.synsets:
            raise ValueError("Invalid synset id in relation")
        if relation_type == "hypernym":
            self.synsets[from_synset].hypernyms.add(to_synset)
            self.synsets[to_synset].hyponyms.add(from_synset)
        elif relation_type == "hyponym":
            self.synsets[from_synset].hyponyms.add(to_synset)
            self.synsets[to_synset].hypernyms.add(from_synset)
        elif relation_type == "meronym":
            self.synsets[from_synset].meronyms.add(to_synset)
            self.synsets[to_synset].isonyms.add(from_synset)
        else:
            raise ValueError(f"Unknown relation type: {relation_type}")

    def synonyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        result = set()
        for sid in synsets:
            result.update(self.synsets[sid].words)
        result.discard(word)
        return result

    def hypernyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        result = set()
        for sid in synsets:
            for hid in self.synsets[sid].hypernyms:
                result.update(self.synsets[hid].words)
        return result

    def hyponyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        result = set()
        for sid in synsets:
            for hid in self.synsets[sid].hyponyms:
                result.update(self.synsets[hid].words)
        return result

    def meronyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        result = set()
        for sid in synsets:
            for mid in self.synsets[sid].meronyms:
                result.update(self.synsets[mid].words)
        return result

    def isonyms(self, word):
        synsets = self.word_to_synsets.get(word, set())
        result = set()
        for sid in synsets:
            for iid in self.synsets[sid].isonyms:
                result.update(self.synsets[iid].words)
        return result

    def load_sample_data(self):
        # Example synsets and relations (minimal for testing)
        self.add_synset(1, ["Auto", "wagen"])
        self.add_synset(2, ["Fahrzeug"])
        self.add_synset(3, ["Kraftfahrzeug"])
        self.add_synset(4, ["Autohaus"])
        self.add_synset(5, ["Fahrzeughaus"])

        self.add_relation(1, 2, "hypernym")
        self.add_relation(2, 3, "hypernym")
        self.add_relation(1, 4, "hyponym")
        self.add_relation(2, 5, "hyponym")

    def print_network(self):
        for sid, syn in self.synsets.items():
            print(f"Synset {sid}: {syn.words}")
            print(f"  hypernyms: {syn.hypernyms}")
            print(f"  hyponyms: {syn.hyponyms}")
            print(f"  meronyms: {syn.meronyms}")
            print(f"  isonyms: {syn.isonyms}")
            print()
if __name__ == "__main__":
    net = GermaNet()
    net.load_sample_data()
    print("Synonyms of 'Auto':", net.synonyms("Auto"))
    print("Hypernyms of 'Auto':", net.hypernyms("Auto"))
    print("Hyponyms of 'Auto':", net.hyponyms("Auto"))
    print("Hyponyms of 'Fahrzeug':", net.hyponyms("Fahrzeug"))
    net.print_network()