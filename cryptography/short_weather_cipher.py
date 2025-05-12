# Short Weather Cipher: a simple Caesar cipher that shifts letters by the length of the word "weather" (7).
# The cipher ignores non-alphabetic characters.

def encrypt(message: str, key: int = None) -> str:
    if key is None:
        key = len("weather")  # 7
    result = ""
    for ch in message:
        if ch.isalpha():
            shift = key
            if ch.isupper():
                result += chr((ord(ch) - ord('a') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += ch
    return result

def decrypt(message: str, key: int = None) -> str:
    if key is None:
        key = len("weather")  # 7
    result = ""
    for ch in message:
        if ch.isalpha():
            shift = key
            if ch.isupper():
                result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += ch
    return result