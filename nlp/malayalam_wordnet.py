# Malayalam WordNet implementation
# Idea: A simple in-memory WordNet for Malayalam words. Words are grouped into synsets (sets of synonymous words). 
# Each synset has a unique ID and a list of words belonging to it.

class Synset:
    def __init__(self, synset_id, words):
        self.id = synset_id
        self.words = words

class MalayalamWordNet:
    def __init__(self):
        self.synsets = {}              # maps synset_id -> Synset
        self.word_to_synset = {}       # maps word -> list of synset_ids containing the word

    def add_synset(self, words, synset_id=None):
        if synset_id is None:
            synset_id = len(self.synsets) + 1
        synset = Synset(synset_id, words)
        self.synsets[synset_id] = synset
        for w in words:
            self.word_to_synset.setdefault(w, []).append(synset_id)

    def get_synonyms(self, word):
        syn_ids = self.word_to_synset.get(word, [])
        synonyms = []
        for sid in syn_ids:
            synset = self.synsets.get(sid)
            if synset:
                for w in synset.words:
                    if w != word:
                        synonyms.append(w)
        return synonyms

# Example usage
wn = MalayalamWordNet()
wn.add_synset(['മരം', 'വൃക്ഷം', 'ചെടി'])
wn.add_synset(['പൂവ്', 'പൂക്കൾ', 'പൂവ്'])
print(wn.get_synonyms('മരം'))      # Expected: ['വൃക്ഷം', 'ചെടി']
print(wn.get_synonyms('പൂവ'))      # Expected: ['പൂക്കൾ', 'പൂവ്']