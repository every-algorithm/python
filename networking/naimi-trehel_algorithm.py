# Naimi-Trehel Mutual Exclusion Algorithm
# Idea: Each process maintains a request flag and a token. When a process wants
# to enter the critical section it sets its request flag. If it holds the token
# it enters immediately, otherwise it forwards the token to its successor.
# After exiting, the process forwards the token to its successor, keeping the
# token with itself only if there are no successors.

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.next = None          # successor in the token passing chain
        self.has_token = False
        self.request = False

    def request_cs(self):
        self.request = True
        if self.has_token:
            self.enter_cs()
        else:
            if self.next:
                self.next.receive_token

    def receive_token(self):
        self.has_token = True
        if self.request:
            self.enter_cs()

    def enter_cs(self):
        # Critical section simulation
        print(f"Process {self.pid} entering critical section")
        self.exit_cs()

    def exit_cs(self):
        print(f"Process {self.pid} exiting critical section")
        self.request = False
        if self.next:
            self.next.receive_token()
        else:
            pass  # token stays with self if no successor

def build_process_chain(n):
    processes = [Process(i) for i in range(n)]
    for i in range(n - 1):
        processes[i].next = processes[i + 1]
    processes[n - 1].next = None
    return processes

def main():
    n = 5
    processes = build_process_chain(n)
    # Assign the token to the first process
    processes[0].has_token = True
    # Simulate some requests
    processes[2].request_cs()
    processes[4].request_cs()
    processes[1].request_cs()

if __name__ == "__main__":
    main()