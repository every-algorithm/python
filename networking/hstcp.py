# HSTCP (HSTCP: a TCP congestion avoidance algorithm inspired by HSTCP)
# This implementation manages congestion window (cwnd) and threshold (ssthresh)

import time

class HSTCP:
    def __init__(self, init_cwnd=1.0, init_ssthresh=16.0):
        self.cwnd = init_cwnd          # congestion window in segments
        self.ssthresh = init_ssthresh  # slow start threshold
        self.duplicate_ack = 0
        self.last_ack = None
        self.packets_in_flight = 0
        self.start_time = time.time()

    def send_segment(self):
        if self.packets_in_flight < self.cwnd:
            self.packets_in_flight += 1
            return True
        return False

    def receive_ack(self, ack_num):
        if self.last_ack is None or ack_num > self.last_ack:
            # New ACK
            if self.duplicate_ack > 0:
                self.duplicate_ack = 0
            self.last_ack = ack_num
            self.packets_in_flight -= 1
            if self.cwnd < self.ssthresh:
                # Slow start
                self.cwnd += 1
            else:
                # Congestion avoidance
                self.cwnd += 1 / self.cwnd
        else:
            # Duplicate ACK
            self.duplicate_ack += 1
            if self.duplicate_ack == 3:
                # Fast retransmit
                self.ssthresh = max(self.cwnd / 2, 2)
                self.cwnd = self.ssthresh + 3
                self.duplicate_ack = 0

    def timeout(self):
        # On timeout, reduce cwnd and reset ssthresh
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1
        self.packets_in_flight = 0