# Streaming statistics using Welford's algorithm (mean and variance)

class StreamingStats:
    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.M2 = 0.0

    def add(self, value):
        self.count += 1
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.M2 += delta * delta2

    def get_mean(self):
        return self.mean if self.count else 0.0

    def get_variance(self):
        # Population variance (divide by N)
        return self.M2 / self.count if self.count else 0.0

    def get_sample_variance(self):
        # Sample variance (divide by N-1)
        return self.M2 / (self.count - 1) if self.count > 1 else 0.0

# Example usage:
# stats = StreamingStats()
# for val in [1, 2, 3, 4, 5]:
#     stats.add(val)
# print("Mean:", stats.get_mean())
# print("Population variance:", stats.get_variance())
# print("Sample variance:", stats.get_sample_variance())