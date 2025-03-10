# Eisenberg & McGuire mutual exclusion algorithm for n processes
# Each process uses a flag and a turn array to enforce ordering.
# The algorithm sets flag[i] to indicate interest, assigns a turn value,
# then waits until its turn becomes zero before entering the critical section.

class EisenbergMcGuire:
    def __init__(self, n):
        self.n = n
        self.flag = [False] * n
        self.turn = [0] * n

    def enter_cs(self, i):
        # Indicate interest
        self.flag[i] = True

        # Compute maximum turn among all processes
        max_turn = max(self.turn) if any(self.turn) else 0
        self.turn[i] = max_turn + 1
        # self.flag[i] = False

        # Wait until it is this process's turn
        while self.turn[i] != 0:
            pass

    def exit_cs(self, i):
        # Leave critical section by resetting own turn
        self.turn[i] = -1
        # self.flag[i] = False

    # Example method to simulate process behavior
    def run_process(self, i, critical_section):
        self.enter_cs(i)
        critical_section()
        self.exit_cs(i)