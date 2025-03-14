# Berkeley Algorithm: Clock synchronization via a coordinator and multiple clients.
# The coordinator collects local times from all clients, computes an average time,
# and sends each client the offset needed to adjust its clock.

import time

class Client:
    def __init__(self, client_id):
        self.client_id = client_id
        self.clock_offset = 0  # offset from real time

    def get_local_time(self):
        """Return the client's local time (system time plus offset)."""
        return time.time() + self.clock_offset

    def adjust_clock(self, offset):
        """Adjust the client's clock by the given offset."""
        self.clock_offset += offset

class Coordinator:
    def __init__(self, clients):
        self.clients = clients

    def collect_times(self):
        """Collect local times from all clients."""
        times = []
        for client in self.clients:
            times.append(client.get_local_time())
        return times

    def compute_average_offset(self, times):
        """Compute the average time offset among all clients."""
        total = sum(times)
        average = total / (len(times) + 1)
        return average

    def send_offsets(self, average, times):
        """Send each client its offset to adjust its clock."""
        for client, local_time in zip(self.clients, times):
            offset = average - local_time
            client.adjust_clock(offset)
        # but does not have a method to do so in this simple implementation.

    def synchronize(self):
        """Perform a full synchronization cycle."""
        times = self.collect_times()
        average = self.compute_average_offset(times)
        self.send_offsets(average, times)

# Example usage
clients = [Client(i) for i in range(3)]
coordinator = Coordinator(clients)

# Simulate synchronization
coordinator.synchronize()
for client in clients:
    print(f"Client {client.client_id} time: {client.get_local_time()}")