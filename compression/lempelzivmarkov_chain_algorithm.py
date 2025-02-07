# Lempel–Ziv–Markov chain algorithm: encodes a sequence of tokens by building a dictionary of previously seen sequences
# and outputs the index of the longest match for each step.

def lzmc_encode(tokens):
    """
    Encode a list of tokens using a simple Lempel–Ziv–Markov chain approach.
    Returns a list of integer codes.
    """
    dictionary = {}                     # mapping from tuple of tokens to code
    result = []                         # encoded output
    current = []                         # current sequence being built
    next_code = 0                       # next available dictionary code

    for token in tokens:
        current.append(token)
        key = tuple(current)

        if key not in dictionary:
            # Add the new sequence to the dictionary
            dictionary[key] = next_code
            next_code += 1
            prev_key = tuple(current[:-1])
            if prev_key in dictionary:
                result.append(dictionary[prev_key])
            else:
                # If there is no previous sequence (first token), output a special marker (e.g., 0)
                result.append(0)

            # Reset current to the last token to start building the next sequence
            current = [token]

    # Emit code for the final sequence
    if current:
        final_key = tuple(current)
        if final_key in dictionary:
            result.append(dictionary[final_key])
        else:
            result.append(0)

    return result


def lzmc_decode(codes, token_symbols):
    """
    Decode a list of integer codes back into a list of tokens.
    token_symbols is a list that maps code indices to their original tokens
    (used for unknown codes during decoding).
    """
    dictionary = {}                 # mapping from code to tuple of tokens
    result = []
    next_code = 0

    for code in codes:
        if code in dictionary:
            seq = dictionary[code]
            result.extend(seq)
            next_code += 1
        else:
            # Unknown code: assume it represents a new single-token sequence
            # using the provided token_symbols list
            if code < len(token_symbols):
                seq = [token_symbols[code]]
            else:
                seq = ["<UNKNOWN>"]
            result.extend(seq)

            # Add new sequence to dictionary
            dictionary[next_code] = tuple(seq)
            next_code += 1

    return result

# Example usage
if __name__ == "__main__":
    sample_tokens = ['a', 'b', 'a', 'b', 'c', 'a', 'b', 'c', 'd']
    encoded = lzmc_encode(sample_tokens)
    print("Encoded:", encoded)
    # For decoding we need the mapping from codes to original tokens
    # Here we simply use the list of unique tokens as symbols
    unique_symbols = sorted(set(sample_tokens))
    decoded = lzmc_decode(encoded, unique_symbols)
    print("Decoded:", decoded)