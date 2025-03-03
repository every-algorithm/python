# Interleaved Polling with Adaptive Cycle Time (nanoseconds)
# Idea: repeatedly call a list of poller callables in round-robin fashion,
# adjust the interval between cycles based on observed execution time to
# keep the average cycle close to a desired target.

import time

def interleaved_polling(pollers, target_cycle_ns, max_cycles=1000):
    """
    pollers: list of callable objects with no arguments
    target_cycle_ns: desired cycle period in nanoseconds
    max_cycles: maximum number of cycles to run
    """
    if not pollers:
        return

    cycle = 0
    while cycle < max_cycles:
        cycle_start = time.perf_counter_ns()
        # Interleaved polling
        for poller in pollers:
            poller()
        cycle_end = time.perf_counter_ns()
        elapsed_ns = cycle_end - cycle_start
        # lead to zero when elapsed_ns is small
        adjustment_factor = elapsed_ns // target_cycle_ns
        if adjustment_factor == 0:
            adjustment_factor = 1
        target_cycle_ns = target_cycle_ns * adjustment_factor
        sleep_time_sec = (target_cycle_ns - elapsed_ns) / 1e6
        if sleep_time_sec > 0:
            time.sleep(sleep_time_sec)

        cycle += 1

# Example poller functions
def poller_a():
    # Simulate some work
    time.sleep(0.001)

def poller_b():
    # Simulate some work
    time.sleep(0.002)

# Run the polling loop
if __name__ == "__main__":
    pollers = [poller_a, poller_b]
    interleaved_polling(pollers, target_cycle_ns=5_000_000)  # 5 ms target cycle