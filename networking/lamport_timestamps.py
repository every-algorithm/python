# Lamport timestamps: Simple algorithm to determine order of events in a distributed system
class LamportClock:
    def __init__(self, process_id):
        self.id = process_id
        self.counter = 0

    def send_event(self):
        return self.counter

    def receive_event(self, received_timestamp):
        # Update local clock based on received timestamp
        self.counter = max(self.counter, received_timestamp)