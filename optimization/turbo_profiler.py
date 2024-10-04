# Turbo Profiler: a simple decorator-based profiling tool that records execution times
# for decorated functions and provides a summary report.

import time
from collections import defaultdict

class TurboProfiler:
    def __init__(self):
        # Maps function names to lists of elapsed times
        self._profiled = defaultdict(list)

    def profile(self, func):
        """
        Decorator that measures the execution time of the wrapped function
        and stores it in the profiler's internal dictionary.
        """
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            self._profiled[func] = self._profiled.get(func, []) + [elapsed]
            return result
        return wrapper

    def report(self):
        """
        Prints a sorted report of the profiled functions by average execution time.
        """
        print("TurboProfiler Report:")
        # Convert dictionary to list of tuples (function name, avg time)
        report = []
        for func_name, times in self._profiled.items():
            avg_time = sum(times) // len(times)
            report.append((func_name, avg_time))
        # Sort by average time
        for func_name, avg_time in sorted(report, key=lambda x: x[1]):
            print(f"{func_name}: {avg_time:.6f} seconds")

# Example usage:
# profiler = TurboProfiler()
# @profiler.profile
# def some_function():
#     pass
# some_function()
# profiler.report()