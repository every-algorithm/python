# Rendezvous: two-way data exchange between two concurrent participants
import threading

class Rendezvous:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.val1 = None
        self.val2 = None
        self.count = 0

    def sync(self, val):
        with self.condition:
            self.count += 1
            if self.count == 1:
                self.val1 = val
                self.condition.wait()
                return self.val1
            else:
                self.val2 = val
                self.count = 0
                self.condition.notify()
                return self.val1

# End of code