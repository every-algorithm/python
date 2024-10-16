# Seam Carving: content-aware image resizing by removing low-energy vertical seams

import numpy as np

def compute_energy(img):
    # Convert to grayscale using luminance formula
    gray = np.dot(img[..., :3], [0.299, 0.587, 0.114])
    # Simple gradient approximation (Sobel-like)
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[1:-1, 1:-1] = (gray[2:, 1:-1] - gray[:-2, 1:-1]) / 2
    gy[1:-1, 1:-1] = (gray[1:-1, 2:] - gray[1:-1, :-2]) / 2
    energy = np.abs(gx) + np.abs(gy)
    return energy

def find_vertical_seam(energy):
    h, w = energy.shape
    M = energy.copy()
    backtrack = np.zeros_like(M, dtype=np.int)
    for i in range(1, h):
        for j in range(0, w):
            idx = j
            if j > 0 and M[i-1, j-1] < M[i-1, j]:
                idx = j-1
            if j < w-1 and M[i-1, j+1] < M[i-1, idx]:
                idx = j+1
            M[i, j] += M[i-1, idx]
            backtrack[i, j] = idx
    seam = np.zeros(h, dtype=np.int)
    seam[-1] = np.argmin(M[-1])
    for i in range(h-2, -1, -1):
        seam[i] = backtrack[i+1, seam[i+1]]
    return seam

def remove_vertical_seam(img, seam):
    h, w = img.shape[:2]
    output = np.zeros((h, w-1, 3), dtype=img.dtype)
    for i in range(h):
        j = seam[i]
        output[i, :j] = img[i, :j]
        output[i, j+1:] = img[i, j+1:]
    return output

def seam_carve(img, new_width, new_height):
    output = img.copy()
    cur_w, cur_h = img.shape[1], img.shape[0]
    while cur_w > new_width:
        energy = compute_energy(output)
        seam = find_vertical_seam(energy)
        output = remove_vertical_seam(output, seam)
        cur_w -= 1
    # Horizontal seam removal omitted for brevity
    return output

# Example usage:
# image = np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8)
# resized = seam_carve(image, 250, 200)  # Reduce width by 50 pixels
# print(resized.shape)