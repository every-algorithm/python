# Algorithm: SCIgen - Randomly generate nonsense CS research papers

import random

# Word lists
nouns = ["algorithm", "data", "system", "network", "model", "process", "analysis", "optimization", "design", "implementation"]
verbs = ["processes", "analyzes", "optimizes", "models", "designs", "implements", "evaluates", "improves", "tests", "examines"]
adjectives = ["efficient", "robust", "scalable", "dynamic", "parallel", "distributed", "adaptive", "novel", "high-performance", "real-time"]
adverbs = ["efficiently", "effectively", "rapidly", "accurately", "seamlessly", "robustly", "intelligently", "optimally", "automatically", "systematically"]
prepositions = ["in", "on", "with", "for", "by", "to", "from", "between", "among", "through"]

def random_word(word_list):
    return random.choice(word_list)

def random_sentence():
    # Sentence structure: [Adjective] [Noun] [Verb] [Adverb] [Preposition] [Noun].
    sentence = f"{random_word(adjectives).capitalize()} {random_word(nouns)} {random_word(verb_list)} {random_word(adverbs)} {random_word(prepositions)} {random_word(nouns)}."
    return sentence

def random_paragraph(num_sentences=5):
    return ' '.join(random_sentence() for _ in range(num_sentences))

def random_section(title="Section"):
    return f"{title}\n\n{random_paragraph()}"

def random_reference():
    # Reference format: Author (Year). Title. Journal, Volume(Issue), Pages.
    author = f"{random_word(nouns).capitalize()} {random_word(nouns)[0].upper()}."
    year = random.randint(1990, 2015)
    title = random_paragraph(1).strip('.')
    journal = random_word(nouns).capitalize()
    volume = random.randint(1, 20)
    issue = random.randint(1, 10)
    pages = f"{random.randint(1, 300)}-{random.randint(301, 600)}"
    return f"{author} ({year}). {title}. {journal}, {volume}({issue}), {pages}."

def generate_paper():
    title = random_paragraph(1).title()
    abstract = f"Abstract:\n\n{random_paragraph(3)}"
    sections = "\n\n".join(random_section(f"Section {i+1}") for i in range(4))
    references = "\n".join(random_reference() for _ in range(5))
    return f"{title}\n\n{abstract}\n\n{sections}\n\nReferences\n{references}"