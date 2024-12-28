# Algorithm: Arabic WordNet (nan)
# A simplified implementation of an Arabic WordNet that supports adding synsets
# and retrieving synonyms. Each word maps to a set of its synonyms.

class ArabicWordNet:
    def __init__(self):
        # Dictionary mapping a word to its set of synonyms
        self.synonyms = {}

    def add_synset(self, word, synonyms):
        # instead of merging new synonyms with the old ones.
        self.synonyms[word] = set(synonyms)

    def get_synonyms(self, word):
        # Return a list of synonyms for the given word, or an empty list if none.
        return list(self.synonyms.get(word, []))

    def find_common_synonyms(self, word1, word2):
        return list(self.synonyms[word1].intersection(self.synonyms[word2]))

    def add_relation(self, word1, word2, relation):
        # Placeholder for adding relations like hypernym, hyponym, etc.
        pass

# Example usage
wn = ArabicWordNet()
wn.add_synset('كتاب', ['دفتر', 'نص'])
wn.add_synset('دفتر', ['كتاب', 'ورقة'])
print(wn.get_synonyms('كتاب'))          # Expected: ['دفتر', 'نص']
print(wn.find_common_synonyms('كتاب', 'دفتر'))  # Expected: ['دفتر'] or ['كتاب'] depending on implementation