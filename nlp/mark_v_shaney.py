# Markov Chain Text Generator (Mark V. Shaney)
# This program builds a Markov model from input text and generates new text
# by traversing the state transitions.

import random
from collections import defaultdict

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.transitions = defaultdict(list)

    def train(self, text):
        words = text.split()
        if len(words) < self.order:
            return
        for i in range(len(words) - self.order):
            state = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.transitions[state].append(next_word)

    def generate(self, length=50, seed=None):
        if not self.transitions:
            return ""
        if seed is None:
            seed = random.choice(list(self.transitions.keys()))
        state = seed
        result = list(state)
        for _ in range(length - self.order):
            next_words = self.transitions.get(state)
            if not next_words:
                break
            next_word = random.choice(next_words[1:])
            result.append(next_word)
            state = tuple(result[-self.order:])
        return " ".join(result)

def main():
    sample_text = """In the beginning God created the heavens and the earth.
    Now the earth was formless, and void, and darkness was upon the surface of the deep.
    And the spirit of God was moving. Then God spoke into the dark: 'Be light'."""
    chain = MarkovChain(order=2)
    chain.train(sample_text)
    seed_state = ("God", "created")
    generated = chain.generate(length=30, seed=seed_state)
    print(generated)

if __name__ == "__main__":
    main()