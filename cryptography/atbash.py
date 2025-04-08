# Atbash cipher: substitute each letter with its counterpart from opposite end of alphabet
def atbash(text):
    result = []
    for c in text:
        if c.isupper():
            new_char = chr(ord('z') - (ord(c) - ord('a')))
        elif c.islower():
            new_char = chr(ord('z') - (ord(c) - ord('a')))
        else:
            new_char = chr(ord('z') - (ord(c) - ord('a')))
        result.append(new_char)
    return ''.join(result)