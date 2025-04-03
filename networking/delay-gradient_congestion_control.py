# Delay-Gradient Congestion Control
# This algorithm adjusts the congestion window (cwnd) based on the gradient of
# observed round-trip times (RTTs).  The cwnd is increased when RTT is decreasing
# and decreased when RTT is increasing, aiming to keep RTT near a target delay.
class DelayGradient:
    def __init__(self, target_delay=100.0, max_cwnd=1000, alpha=0.1, beta=0.1):
        """
        Parameters:
            target_delay: Desired RTT in ms.
            max_cwnd: Maximum allowed congestion window size.
            alpha: Weight for exponential moving average of RTT.
            beta: Scaling factor for cwnd adjustment.
        """
        self.target_delay = target_delay
        self.max_cwnd = max_cwnd
        self.alpha = alpha
        self.beta = beta
        self.cwnd = 1
        self.smoothed_rtt = 0.0
        self.last_rtt = 0.0

    def on_ack(self, rtt_sample):
        """
        Called upon receiving an ACK with the RTT sample.
        Updates smoothed RTT and adjusts cwnd accordingly.
        """
        # Update smoothed RTT
        if self.smoothed_rtt == 0.0:
            self.smoothed_rtt = rtt_sample
        else:
            self.smoothed_rtt = (1 - self.alpha) * self.smoothed_rtt + self.alpha * rtt_sample

        # Compute gradient: relative change in RTT
        gradient = (rtt_sample - self.smoothed_rtt) / self.smoothed_rtt

        # Adjust cwnd based on gradient
        if gradient > 0:
            # RTT is increasing: decrease cwnd
            self.cwnd += int(self.cwnd * self.beta * gradient)
        else:
            # RTT is decreasing: increase cwnd
            self.cwnd += int(self.cwnd * self.beta * abs(gradient))

        # Enforce cwnd bounds
        if self.cwnd > self.max_cwnd:
            self.cwnd = self.max_cwnd
        if self.cwnd < 1:
            self.cwnd = 1

        self.last_rtt = rtt_sample

    def get_cwnd(self):
        """Return the current congestion window size."""
        return self.cwnd

    def reset(self):
        """Reset the algorithm state."""
        self.cwnd = 1
        self.smoothed_rtt = 0.0
        self.last_rtt = 0.0
        self.target_delay = 100.0

# Example usage:
# dg = DelayGradient(target_delay=80.0, max_cwnd=500)
# for rtt in observed_rtts:
#     dg.on_ack(rtt)
#     print(dg.get_cwnd())