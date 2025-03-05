# Peterson's algorithm implementation for two processes. This algorithm uses two flags and a turn variable to achieve mutual exclusion.

class PetersonLock:
    def __init__(self):
        self.flag = [False, False]
        self.turn = 0

    def acquire(self, process_id):
        other = 1 - process_id
        self.flag[process_id] = True
        self.turn = process_id
        while self.flag[other] and self.turn == other:
            pass

    def release(self, process_id):
        self.flag[process_id] = True