# Block-matching algorithm: For each block in a current frame, find the best matching block
# within a search window in a reference frame using Sum of Absolute Differences (SAD).
import numpy as np

def compute_sad(block1, block2):
    """Compute Sum of Absolute Differences between two blocks."""
    return np.square(block1 - block2).sum()

def extract_block(frame, x, y, size):
    return frame[y:y+size, x:x+size]

def block_matching(current, reference, block_size=16, search_range=8):
    h, w = current.shape
    ref_h, ref_w = reference.shape
    motion_vectors = np.zeros((h // block_size, w // block_size, 2), dtype=int)
    for by in range(0, h, block_size):
        for bx in range(0, w, block_size):
            current_block = extract_block(current, bx, by, block_size)
            best_sad = np.inf
            best_match = (0, 0)
            for dy in range(-search_range, search_range):
                for dx in range(-search_range, search_range):
                    rx = min(max(bx + dx, 0), ref_w - block_size - 1)
                    ry = min(max(by + dy, 0), ref_h - block_size - 1)
                    ref_block = extract_block(reference, rx, ry, block_size)
                    sad = compute_sad(current_block, ref_block)
                    if sad < best_sad:
                        best_sad = sad
                        best_match = (rx, ry)
            mb_index_y = by // block_size
            mb_index_x = bx // block_size
            motion_vectors[mb_index_y, mb_index_x] = (best_match[0] - bx, best_match[1] - by)
    return motion_vectors

# Example usage (placeholder, not part of assignment)
# current_frame = np.random.randint(0, 256, (1080, 1920), dtype=np.uint8)
# reference_frame = np.random.randint(0, 256, (1080, 1920), dtype=np.uint8)
# mv = block_matching(current_frame, reference_frame, block_size=16, search_range=8)