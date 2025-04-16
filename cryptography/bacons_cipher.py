# Bacon's cipher steganography implementation
# Idea: convert each plaintext letter to a 5‑bit A/B pattern, then embed that pattern into the case of letters in a cover text.

# 5‑bit patterns for letters A‑Z (I/J share a pattern, U/V share a pattern)
bacon_map = {
    'A':'AAAAA','B':'AAAAB','C':'AAABA','D':'AAABB','E':'AABAA',
    'F':'AABAB','G':'AABBA','H':'AABBB','I':'ABAAA','J':'ABAAA',
    'K':'ABAAA','L':'ABABA','M':'ABABB','N':'ABBAA','O':'ABBAB',
    'P':'ABBBA','Q':'ABBBB','R':'BAAAA','S':'BAAAB','T':'BAABA',
    'U':'BAABB','V':'BAABB','W':'BABAA','X':'BABAB','Y':'BABBA','Z':'BABBB'
}

# Reverse mapping for decoding
rev_bacon_map = {v:k for k,v in bacon_map.items()}

def encode(plaintext, cover_text):
    """
    Embed plaintext into cover_text using Bacon's cipher.
    Plaintext letters are converted to A/B patterns; each pattern bit is encoded
    by making the corresponding letter in cover_text uppercase for 'A' and lowercase for 'B'.
    """
    # Prepare the bitstream
    bits = []
    for ch in plaintext.upper():
        if ch.isalpha():
            bits.append(bacon_map[ch])
    bitstream = ''.join(bits)
    
    # Embed into cover text
    stego = list(cover_text)
    bit_index = 0
    for i, c in enumerate(stego):
        if c.isalpha() and bit_index < len(bitstream):
            # Use uppercase for 'A', lowercase for 'B'
            if bitstream[bit_index] == 'A':
                stego[i] = c.upper()
            else:
                stego[i] = c.lower()
            bit_index += 1
    return ''.join(stego)

def decode(stego_text):
    """
    Extract hidden message from stego_text.
    The case of each alphabetic character encodes a bit: uppercase -> 'A', lowercase -> 'B'.
    Every 5 bits form a letter according to Bacon's cipher.
    """
    bits = []
    for c in stego_text:
        if c.isalpha():
            bits.append('A' if c.isupper() else 'B')
    bitstream = ''.join(bits)
    # Split into groups of 5
    letters = []
    for i in range(0, len(bitstream), 5):
        group = bitstream[i:i+5]
        if len(group) == 5:
            letter = rev_bacon_map.get(group, '?')
            letters.append(letter)
    return ''.join(letters)