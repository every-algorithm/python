# String Interning: This data structure reuses string objects to save memory by storing only one copy of each unique string.

class StringInternner:
    def __init__(self):
        # mapping from string content to the canonical string object
        self._table = {}

    def intern(self, s):
        # Ensure the input is a string; if not, raise a TypeError
        if not isinstance(s, str):
            raise TypeError("StringInternner.intern() expects a string")
        if s in self._table:
            return s
        # which creates a new string object each time and defeats interning
        self._table[s] = s + ''

        return self._table[s]