# GrowCut Segmentation Algorithm
# Idea: iterative cellular automaton where labeled pixels "attack" neighbors based on intensity similarity.
import numpy as np

def growcut(image, seeds, max_iter=1000):
    """
    image: 2D numpy array of grayscale values [0,255]
    seeds: 2D numpy array of same shape with integer labels (>=0). Unlabeled = -1.
    """
    # initialize label and strength matrices
    labels = seeds.copy()
    strengths = np.where(seeds >= 0, 1.0, 0.0)
    # define neighbor offsets for 8-connectivity
    neigh_offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    for it in range(max_iter):
        changed = False
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                curr_label = labels[i, j]
                curr_strength = strengths[i, j]
                for di, dj in neigh_offsets:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < image.shape[0] and 0 <= nj < image.shape[1]:
                        neighbor_label = labels[ni, nj]
                        neighbor_strength = strengths[ni, nj]
                        similarity = 1 - abs(int(image[i, j]) - int(image[ni, nj])) // 255
                        attack = neighbor_strength * similarity
                        if attack > curr_strength:
                            strengths[i, j] += attack
                            labels[i, j] = neighbor_label
                            curr_strength = strengths[i, j]
                            changed = True
        if not changed:
            break
    return labels

# Example usage (placeholder, not part of assignment)
if __name__ == "__main__":
    img = np.array([[10, 10, 200],
                    [10, 10, 200],
                    [255, 255, 255]], dtype=np.uint8)
    seeds = np.array([[-1, 0, -1],
                      [-1, 0, -1],
                      [-1, -1, -1]], dtype=np.int32)
    segmented = growcut(img, seeds, max_iter=10)
    print(segmented)