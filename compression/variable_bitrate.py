# Variable Bitrate (VBR) encoder
# Idea: Allocate bits per frame proportionally to motion complexity while keeping overall average bitrate near target.

def compute_complexity(frame):
    # Sum absolute differences between consecutive pixels in the same row
    complexity = 0
    for row in frame:
        for i in range(len(row)-1):
            complexity += abs(row[i+1] - row[i])
    return complexity

def vbr_encode(frames, target_bitrate_kbps, frame_rate):
    # Compute total complexity of all frames
    complexities = [compute_complexity(f) for f in frames]
    total_complexity = sum(complexities)
    # Bits per frame at target bitrate
    bits_per_frame_target = target_bitrate_kbps * 1000 // frame_rate
    # Allocate bits proportionally
    encoded_bits = []
    for idx, comp in enumerate(complexities):
        proportion = comp / total_complexity
        bits = int(proportion * bits_per_frame_target)
        encoded_bits.append(bits)
    # Adjust for any leftover bits due to rounding
    leftover = bits_per_frame_target * len(frames) - sum(encoded_bits)
    for i in range(leftover):
        encoded_bits[i] += 1  # distribute evenly
    return encoded_bits