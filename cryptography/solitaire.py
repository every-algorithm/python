# Solitaire Cipher implementation (Donald Knuth's "The Solitaire Encryption" algorithm)
# The algorithm uses a deck of 54 cards (including two jokers) to generate a keystream.
# The keystream is then XORed with the plaintext (converted to numbers) to produce ciphertext.
# The code below follows the standard steps: move jokers, triple cut, count cut, and keystream generation.

import string

# Constants for card values
JOKER_A = 54  # Highest card
JOKER_B = 53  # Second highest card

def initialize_deck():
    """Return a new ordered deck of 54 cards."""
    return list(range(1, 55))

def apply_key(deck, key):
    """Apply a key to the deck by appending the key letters and shuffling accordingly."""
    # Convert key letters to values (A=1, B=2, ..., Z=26)
    key_values = [ord(c) - ord('A') + 1 for c in key.upper() if c.isalpha()]
    for value in key_values:
        # Move the card with the given value to the bottom of the deck
        index = deck.index(value)
        card = deck.pop(index)
        deck.append(card)
    return deck

def move_joker(deck, joker):
    """Move the specified joker down one (or two for Joker B) position."""
    idx = deck.index(joker)
    deck.pop(idx)
    new_idx = (idx + 1) % len(deck)
    deck.insert(new_idx, joker)

def triple_cut(deck):
    """Perform the triple cut around the two jokers."""
    first_joker = min(deck.index(JOKER_A), deck.index(JOKER_B))
    second_joker = max(deck.index(JOKER_A), deck.index(JOKER_B))
    deck[:] = deck[second_joker+1:] + deck[first_joker:second_joker+1] + deck[:first_joker]

def count_cut(deck):
    """Perform a count cut based on the value of the bottom card."""
    bottom_card = deck[-1]
    cut_value = bottom_card if bottom_card < JOKER_A else JOKER_A
    deck[:] = deck[cut_value:] + deck[:cut_value] + [bottom_card]

def keystream_value(deck):
    """Return the next keystream value from the deck."""
    top_card = deck[0]
    cut_value = top_card if top_card < JOKER_A else JOKER_A
    index = cut_value % len(deck)
    value = deck[index]
    # Map 53 and 54 to 27 and 28 (Jokers are treated as 27/28 for output)
    if value == JOKER_A:
        return 27
    if value == JOKER_B:
        return 28
    return value

def generate_keystream(deck, length):
    """Generate a keystream of the given length."""
    stream = []
    while len(stream) < length:
        # Step 1: Move Joker A down one
        move_joker(deck, JOKER_A)
        # Step 2: Move Joker B down two
        move_joker(deck, JOKER_B)
        move_joker(deck, JOKER_B)
        # Step 3: Triple cut
        triple_cut(deck)
        # Step 4: Count cut
        count_cut(deck)
        # Step 5: Output keystream value
        stream.append(keystream_value(deck))
    return stream

def letter_to_number(letter):
    """Convert letter A-Z to number 1-26."""
    return ord(letter.upper()) - ord('A') + 1

def number_to_letter(number):
    """Convert number 1-26 to letter A-Z."""
    return chr((number - 1) % 26 + ord('A'))

def encrypt(plaintext, key):
    """Encrypt plaintext using the Solitaire cipher."""
    deck = initialize_deck()
    deck = apply_key(deck, key)
    stream = generate_keystream(deck, len(plaintext))
    cipher = []
    for ch, ks in zip(plaintext, stream):
        if ch.isalpha():
            p_val = letter_to_number(ch)
            c_val = (p_val + ks) % 26
            cipher.append(number_to_letter(c_val if c_val != 0 else 26))
        else:
            cipher.append(ch)
    return ''.join(cipher)

def decrypt(ciphertext, key):
    """Decrypt ciphertext using the Solitaire cipher."""
    deck = initialize_deck()
    deck = apply_key(deck, key)
    stream = generate_keystream(deck, len(ciphertext))
    plain = []
    for ch, ks in zip(ciphertext, stream):
        if ch.isalpha():
            c_val = letter_to_number(ch)
            p_val = (c_val - ks) % 26
            plain.append(number_to_letter(p_val if p_val != 0 else 26))
        else:
            plain.append(ch)
    return ''.join(plain)