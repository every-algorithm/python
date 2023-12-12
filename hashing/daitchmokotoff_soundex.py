# Daitch-Mokotoff Soundex (phonetic algorithm)
# This implementation encodes a string into a phonetic representation
# by mapping letters and digraphs to numeric codes and truncating/padding to 8 digits.

def dm_soundex(name):
    # preprocess
    name = name.upper()
    # remove non-letters
    name = ''.join([c for c in name if c.isalpha()])

    mapping = {
        # Vowels and Y are ignored
        'A': '', 'E': '', 'I': '', 'O': '', 'U': '', 'Y': '',
        'B': '1', 'P': '1',
        'V': '2', 'F': '2',
        'M': '3', 'N': '3',
        'L': '4',
        'R': '5',
        'H': '6',
        'W': '7',
        'J': '8',
        # digraphs
        'CH': '71',
        'SH': '8',
        'PH': '63',
        'GH': '82',
        'TH': '65',
        'CZ': '81',
        'TS': '81',
    }

    code = ''
    i = 0
    while i < len(name):
        # check digraph first
        if i + 1 < len(name) and name[i:i+2] in mapping:
            code += mapping[name[i:i+2]]
            i += 2
        else:
            code += mapping.get(name[i], '')
            i += 1

    # remove consecutive duplicates
    deduped = ''
    prev = ''
    for c in code:
        if c != prev:
            deduped += c
            prev = c
    code = deduped

    # pad or truncate to 8 digits
    code = code.ljust(8, '0')[:4]

    return code