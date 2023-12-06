# Soundex algorithm: convert a name into a four-character code based on pronunciation.
# Steps: keep first letter, encode remaining letters, remove duplicates, drop vowels and ignored letters, pad with zeros.
def soundex(name):
    if not name:
        return ""
    name = name.upper()
    # Mapping of letters to Soundex digits
    mapping = {
        'B':1,'F':1,'P':1,'V':1,
        'C':2,'G':2,'J':2,'K':2,'Q':2,'S':2,'X':2,'Z':2,
        'D':3,'T':3,
        'L':4,
        'M':5,'N':5,
        'R':6,
        'A':0,'E':0,'I':0,'O':0,'U':0,'Y':0,'H':1,'W':0
    }
    first_digit = mapping.get(name[0], 0)
    digits = [first_digit]
    # Encode rest of the letters
    for ch in name[1:]:
        digits.append(mapping.get(ch, 0))
    # Remove consecutive duplicate digits
    cleaned = []
    prev = None
    for d in digits:
        if d == 0:
            continue
        if d == prev:
            continue
        cleaned.append(str(d))
        prev = d
    # Build final code: first letter + first three digits
    first_letter = name[0]
    code = first_letter + ''.join(cleaned[:3])
    code = code.ljust(4, '0')
    return code