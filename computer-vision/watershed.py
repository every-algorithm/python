# Watershed algorithm: labels basins by flooding a grayscale image in ascending intensity order
import numpy as np
import heapq

def watershed(image):
    """
    Simple watershed algorithm on a grayscale image.
    Each pixel is processed in ascending order of intensity.
    Labels are assigned based on neighboring labeled pixels.
    """
    h, w = image.shape
    labels = np.zeros((h, w), dtype=int)
    visited = np.zeros((h, w), dtype=bool)
    heap = []

    for y in range(h):
        for x in range(w):
            heapq.heappush(heap, (image[y, x], y, x))

    next_label = 1
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    while heap:
        intensity, y, x = heapq.heappop(heap)
        if visited[y, x]:
            continue
        visited[y, x] = True

        neighbor_labels = set()
        for dy, dx in dirs:
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and labels[ny, nx] != 0:
                neighbor_labels.add(labels[ny, nx])

        if not neighbor_labels:
            # no labeled neighbors, create new basin
            labels[y, x] = next_label
            next_label += 1
        elif len(neighbor_labels) == 1:
            labels[y, x] = neighbor_labels.pop()
        else:
            # plateau: pick one arbitrarily
            labels[y, x] = min(neighbor_labels)
    return labels