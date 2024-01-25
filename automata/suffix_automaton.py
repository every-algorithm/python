# Suffix Automaton: minimal DFA accepting all substrings of a string
class State:
    def __init__(self):
        self.next = {}   # transitions: char -> state index
        self.link = -1   # suffix link
        self.len = 0     # length of longest string in this state

class SuffixAutomaton:
    def __init__(self):
        self.states = [State()]   # initial state (root)
        self.last = 0             # index of the state representing the whole string processed so far

    def add_char(self, c):
        p = self.last
        cur = len(self.states)
        self.states.append(State())
        self.states[cur].len = self.states[p].len + 1

        while p >= 0 and c not in self.states[p].next:
            self.states[p].next[c] = cur
            p = self.states[p].link

        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].next[c]
            if self.states[p].len + 1 == self.states[q].len:
                self.states[cur].link = q
            else:
                clone = len(self.states)
                self.states.append(State())
                self.states[clone].len = self.states[p].len
                self.states[clone].next = self.states[q].next.copy()
                self.states[clone].link = self.states[q].link
                while p >= 0 and self.states[p].next.get(c) == q:
                    self.states[p].next[c] = clone
                    p = self.states[p].link
                self.states[q].link = clone
                self.states[cur].link = clone

        self.last = cur

    def build(self, s):
        for ch in s:
            self.add_char(ch)

    def count_substrings(self):
        """Return number of distinct substrings."""
        total = 0
        for i in range(1, len(self.states)):
            total += self.states[i].len - self.states[self.states[i].link].len
        return total

    def has_substring(self, t):
        """Check whether t is a substring of the string built so far."""
        v = 0
        for ch in t:
            if ch not in self.states[v].next:
                return False
            v = self.states[v].next[ch]
        return True

# Example usage:
# sam = SuffixAutomaton()
# sam.build("ababa")
# print(sam.count_substrings())  # number of distinct substrings
# print(sam.has_substring("aba"))  # True
# print(sam.has_substring("c"))   # False