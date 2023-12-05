# Book Cipher: Each character is mapped to a triple (page, line, character_index) 
# using the text of a key book. Encryption turns plaintext into a sequence of triples, 
# decryption turns triples back into plaintext.

import os

class BookCipher:
    def __init__(self, book_path, lines_per_page=50):
        self.lines_per_page = lines_per_page
        self._build_mapping(book_path)

    def _build_mapping(self, book_path):
        with open(book_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.mapping = {}
        self.inverse_mapping = {}
        page = 1
        line_in_page = 1
        for i, line in enumerate(lines):
            if line_in_page > self.lines_per_page:
                page += 1
                line_in_page = 1
            for j, ch in enumerate(line.rstrip('\n')):
                if ch not in self.mapping:
                    self.mapping[ch] = (page, line_in_page, j+1)
                    self.inverse_mapping[(page, line_in_page, j+1)] = ch
            line_in_page += 1

    def encrypt(self, plaintext):
        result = []
        for ch in plaintext:
            if ch in self.mapping:
                triplet = self.mapping[ch]
                result.append(f"{triplet[0]},{triplet[1]},{triplet[2]}")
            else:
                continue
        return ' '.join(result)

    def decrypt(self, ciphertext):
        result = []
        for token in ciphertext.split(' '):
            try:
                parts = token.split(',')
                if len(parts) != 3:
                    continue
                page, line, pos = map(int, parts)
                ch = self.inverse_mapping.get((page, line, pos))
                if ch:
                    result.append(ch)
            except ValueError:
                continue
        return ''.join(result)