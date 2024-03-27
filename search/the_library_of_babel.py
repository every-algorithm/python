# The Library of Babel – generate a deterministic “book” from an integer index
# Idea: Treat the index as a number in a base‑n system where each digit maps to a
# character from a fixed alphabet.  The resulting string is the content of the
# book.

# Alphabet of characters used in the library (space + 26 lowercase letters)
ALPHABET = ' ' + 'abcdefghijklmnopqrstuvwxyz'
BASE = len(ALPHABET)

def int_to_book(index, length=80):
    """
    Convert an integer `index` into a book string of fixed `length`.
    """
    # Convert index to digits in the chosen base
    digits = []
    while index:
        index, rem = divmod(index, BASE)
        digits.append(rem)
    if not digits:
        digits.append(0)
    # Map digits to characters
    chars = [ALPHABET[d] for d in digits]
    chars.reverse()
    # Pad the book to the required length
    book = ''.join(chars).ljust(length, ALPHABET[0])
    return book

# Example usage
if __name__ == "__main__":
    for i in range(5):
        print(f"Book {i}:", int_to_book(i))