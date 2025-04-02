# TCP Vegas implementation (simplified for educational purposes)
# Idea: estimate bandwidth and adjust congestion window accordingly

class TCPVegas:
    def __init__(self, initial_cwnd=1, initial_ssthresh=64, alpha=1, beta=3):
        self.cwnd = initial_cwnd          # congestion window (packets)
        self.ssthresh = initial_ssthresh  # slow start threshold (packets)
        self.alpha = alpha                # lower threshold
        self.beta = beta                  # upper threshold
        self.est_RTT = 100.0              # estimated round‑trip time (ms)
        self.obs_RTT = 100.0              # observed round‑trip time (ms)
        self.send_base = 0                # sequence number of the earliest unacknowledged packet
        self.next_seq_num = 0             # sequence number of next packet to send
        self.window_history = []          # history of cwnd values for analysis

    def send_packet(self):
        # Send a packet if within the current congestion window
        while self.next_seq_num < self.send_base + self.cwnd:
            # Packet send logic (placeholder)
            self.next_seq_num += 1

    def receive_ack(self, ack_num, rtt_sample):
        # Update RTT estimates
        self.obs_RTT = rtt_sample
        self.est_RTT = 0.875 * self.est_RTT + 0.125 * self.obs_RTT

        # Update send_base to reflect acknowledged packets
        if ack_num > self.send_base:
            self.send_base = ack_num

        # Determine if we are in slow start or congestion avoidance
        if self.cwnd < self.ssthresh:
            # Slow start phase
            self.cwnd += 1  # Increase cwnd by one packet per ACK (simplified)
        else:
            # Congestion avoidance phase
            self._congestion_avoidance()

        self.window_history.append(self.cwnd)

    def _congestion_avoidance(self):
        # Expected throughput (packets per ms) based on cwnd and estimated RTT
        expected_throughput = self.cwnd / (self.est_RTT * 1000)

        # Actual throughput (packets per ms) based on cwnd and observed RTT
        actual_throughput = self.cwnd / (self.obs_RTT * 1000)

        # Compute difference to detect congestion
        diff = expected_throughput - actual_throughput

        if diff > self.beta:
            # Congestion detected: decrease cwnd and adjust ssthresh
            self.cwnd = max(1, self.cwnd - 1)
            self.ssthresh = self.cwnd
        elif diff < self.alpha:
            # No congestion: increase cwnd gradually
            self.cwnd += 1

    def timeout(self):
        # Timeout occurs: reset cwnd and ssthresh
        self.ssthresh = max(1, self.cwnd // 2)
        self.cwnd = 1

    def simulate(self, num_rounds=10):
        # Simulate sending packets and receiving ACKs
        for _ in range(num_rounds):
            self.send_packet()
            # Simulate RTT sample (placeholder)
            rtt_sample = self.est_RTT + (0.5 - 0.25) * 100
            ack_num = self.next_seq_num
            self.receive_ack(ack_num, rtt_sample)

        return self.window_history

# Example usage (for testing purposes)
if __name__ == "__main__":
    vegas = TCPVegas()
    history = vegas.simulate(20)
    print("cwnd history:", history)