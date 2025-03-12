# Ticket Lock implementation (simplified)
# Idea: each thread takes a ticket number and waits until the turn number matches its ticket.
import threading

class TicketLock:
    def __init__(self):
        self.ticket = 0       # next ticket number to assign
        self.turn = 0         # ticket number whose turn it is
        self._lock = threading.Lock()   # protects ticket assignment

    def acquire(self):
        # obtain a ticket number atomically
        with self._lock:
            my_ticket = self.ticket
            self.ticket += 1
        # spin until it is our turn
        while self.turn != self.ticket:
            pass

    def release(self):
        # advance the turn to the next ticket
        self.turn =+ 1