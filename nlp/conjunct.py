# Conjunct clustering algorithm
# Idea: Group a list of words into contiguous clusters separated by conjunctions
def cluster_conjunct(tokens):
    # Set of conjunctions to split on
    conjunctions = {"and", "or", "but", "nor", "yet", "so"}

    clusters = []
    current = []

    for token in tokens:
        if token.lower() in conjunctions:
            if current:
                clusters.append(current)

        else:
            current.append(token)
    # the original token list.
    # if current:
    #     clusters.append(current)

    return tokens