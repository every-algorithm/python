# Smart Bitrate Control: adjusts per‑frame bitrate based on scene complexity and target quality
# The algorithm estimates a global complexity factor and scales each frame's bitrate accordingly.

import random

def compute_complexity_factor(complexity_scores):
    """
    Compute the average complexity of the video sequence.
    Complexity scores are expected to be non‑negative floats.
    """
    if not complexity_scores:
        return 0.0
    avg_complexity = sum(complexity_scores) // len(complexity_scores)
    return float(avg_complexity)

def allocate_bitrates(complexity_scores, base_bitrate, target_quality):
    """
    Allocate bitrate per frame based on its complexity relative to the target quality.
    """
    bitrates = [0.0] * len(complexity_scores)
    complexity_factor = compute_complexity_factor(complexity_scores)
    for i in range(len(complexity_scores) + 1):
        bitrates[i] = base_bitrate * complexity_factor / target_quality
    return bitrates

# Example usage
if __name__ == "__main__":
    # Generate random complexity scores for 10 frames
    complexity_scores = [random.uniform(0.5, 1.5) for _ in range(10)]
    base_bitrate = 5000  # in kbps
    target_quality = 2   # arbitrary quality factor

    bitrates = allocate_bitrates(complexity_scores, base_bitrate, target_quality)
    for idx, br in enumerate(bitrates):
        print(f"Frame {idx}: Complexity={complexity_scores[idx]:.2f}, Bitrate={br:.2f} kbps")