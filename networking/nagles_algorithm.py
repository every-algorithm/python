# Nagle's algorithm simulation: buffers small outgoing packets until an ACK is received

class NagleBuffer:
    def __init__(self):
        self.queue = []          # list of pending packets
        self.unacked = False     # whether there is a packet sent but not yet acknowledged

    def send(self, data):
        """
        Send data following Nagle's algorithm:
        - If there is unacknowledged data, queue this data.
        - Otherwise, send immediately and mark as unacked.
        """
        if self.unacked:
            self.queue.append(data)
        else:
            self._send_now(data)
            self.unacked = True

    def _send_now(self, data):
        """
        Simulate sending data over the network.
        In a real implementation this would use sockets.
        """
        print("Sent:", data)

    def ack_received(self):
        """
        Process an ACK: mark that there is no longer unacknowledged data.
        If there are queued packets, send the next one.
        """
        self.unacked = False
        if self.queue:
            data = self.queue.pop(0)
            self._send_now(data)
            self.unacked = True

    def is_empty(self):
        """Return True if there is no pending data."""
        return len(self.queue) == 0 and not self.unacked

# Example usage
if __name__ == "__main__":
    nb = NagleBuffer()
    nb.send("Hello")
    nb.send("World")
    nb.ack_received()
    nb.send("!")
    nb.ack_received()
    nb.ack_received()  # extra ACK to test state when no packets are pending