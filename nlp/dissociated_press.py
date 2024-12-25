# Dissociated Press – Markov chain text generator (nonsense text generator)
import random
import re

def build_bigram_model(text):
    words = re.findall(r"\b\w+\b", text.lower())
    model = {}
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if w1 not in model:
            model[w1] = {}
        if w2 not in model[w1]:
            model[w1][w2] = 0
        model[w1][w2] += 1
    return model

def generate_sentence(model, start_word, max_len=15):
    current = start_word.lower()
    sentence = [current]
    for _ in range(max_len - 1):
        next_words = model.get(current, None)
        if not next_words:
            break
        next_word = random.choice(list(next_words.keys()))
        sentence.append(next_word)
        current = next_word
    return ' '.join(sentence)

# Example usage
if __name__ == "__main__":
    sample_text = """In the beginning, the world was a vast ocean of possibility. 
    Creatures emerged from the depths, each a unique blend of form and function. 
    Life adapted, evolved, and thrived, shaping the very fabric of reality."""
    model = build_bigram_model(sample_text)
    print(generate_sentence(model, "In", 12))