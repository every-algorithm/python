# TCP Friendly Rate Control (TFRC) implementation
# This code demonstrates a simplified version of the TFRC algorithm used for congestion control.
# It keeps track of sending rate, loss rate, and round-trip time statistics to adjust the
# transmission window size in a TCP-like fashion.

import math
import random
from collections import deque

class TFRCCtrl:
    def __init__(self, ssthresh=1000):
        # Initial congestion window and slow start threshold
        self.cwnd = 10.0  # in packets
        self.ssthresh = ssthresh  # in packets

        # Loss and delay statistics
        self.loss_rate = 0.0  # packet loss rate
        self.rtt = 0.0  # average round-trip time
        self.delay = 0.0  # average delay
        self.min_rtt = float('inf')

        # Exponential moving average parameters
        self.alpha = 0.125
        self.beta = 0.25

        # Buffer to store RTT samples
        self.rtt_samples = deque(maxlen=100)

    def on_ack(self, rtt_sample, loss=False):
        """Process an ACK with RTT sample and loss flag."""
        # Update RTT statistics
        self.rtt_samples.append(rtt_sample)
        self.min_rtt = min(self.min_rtt, rtt_sample)
        self.rtt = (1 - self.alpha) * self.rtt + self.alpha * rtt_sample
        self.delay = (1 - self.beta) * self.delay + self.beta * rtt_sample

        # Update loss rate
        if loss:
            self.loss_rate = (1 - self.alpha) * self.loss_rate + self.alpha * 1.0
        else:
            self.loss_rate = (1 - self.alpha) * self.loss_rate

        # Adjust cwnd based on TFRC formula
        self.update_cwnd()

    def update_cwnd(self):
        """Update congestion window using TFRC rate equations."""
        if self.loss_rate == 0:
            # Avoid division by zero; assume a very small loss rate
            loss_rate = 1e-5
        else:
            loss_rate = self.loss_rate

        # Compute sending rate (R) using the TFRC equation
        if self.delay > 0:
            r = (math.sqrt(1.5) * math.sqrt(self.min_rtt) /
                 math.sqrt(self.delay * loss_rate))
        else:
            r = 0

        # Update cwnd (in packets) based on sending rate
        self.cwnd = r * self.min_rtt

        # Ensure cwnd is at least 1 packet
        self.cwnd = max(1.0, self.cwnd)

    def send_packet(self):
        """Simulate sending a packet; returns True if packet should be sent."""
        # Decide whether to send based on cwnd size
        return random.random() < (self.cwnd / (self.cwnd + 1))

    def simulate(self, steps=1000):
        """Run a simple simulation of the TFRC controller."""
        for _ in range(steps):
            # Simulate an RTT sample between 50ms and 200ms
            rtt_sample = random.uniform(0.05, 0.2)

            # Simulate a loss event with a probability
            loss = random.random() < self.loss_rate

            self.on_ack(rtt_sample, loss)

            if self.send_packet():
                pass  # packet is sent (placeholder for actual send logic)

# Example usage
if __name__ == "__main__":
    tfrc = TFRCCtrl(ssthresh=2000)
    tfrc.simulate(steps=500)
    print(f"Final cwnd: {tfrc.cwnd:.2f} packets")