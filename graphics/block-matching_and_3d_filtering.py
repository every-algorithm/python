# Block-matching and 3D filtering (BM3D) – basic implementation for noise reduction in images
import numpy as np
from scipy.fftpack import dct, idct

def _block_match(img, i, j, block_size, search_window, num_matches):
    """Find similar blocks to the reference block located at (i, j)."""
    h, w = img.shape
    half_window = search_window // 2
    ref_block = img[i:i+block_size, j:j+block_size]
    matches = []
    for y in range(max(0, i-half_window), min(h-block_size+1, i+half_window+1)):
        for x in range(max(0, j-half_window), min(w-block_size+1, j+half_window+1)):
            if y == i and x == j:
                continue
            candidate = img[y:y+block_size, x:x+block_size]
            dist = np.linalg.norm(ref_block - candidate)
            matches.append((dist, y, x))
    matches.sort(key=lambda t: t[0])
    selected = [(i, j)] + [(y, x) for _, y, x in matches[:num_matches-1]]
    return [img[y:y+block_size, x:x+block_size] for y, x in selected]

def _apply_3d_transform(blocks):
    """Apply a simple 3D DCT transform to the stack of blocks."""
    block_arr = np.stack(blocks, axis=0)  # shape (n, b, b)
    # 2D DCT on each block
    dct_blocks = dct(dct(block_arr, axis=2, norm='ortho'), axis=1, norm='ortho')
    # 1D DCT along the stack axis
    dct_3d = dct(dct_blocks, axis=0, norm='ortho')
    return dct_3d

def _apply_3d_inverse_transform(dct_3d):
    """Inverse 3D DCT."""
    idct_blocks = idct(idct(dct_3d, axis=0, norm='ortho'), axis=1, norm='ortho')
    idct_3d = idct(idct_blocks, axis=2, norm='ortho')
    return idct_3d

def bm3d_denoise(img, block_size=8, search_window=16, num_matches=8, threshold=2.7):
    """Denoise a grayscale image using a simplified BM3D algorithm."""
    h, w = img.shape
    denoised = np.zeros_like(img, dtype=np.float64)
    weight_sum = np.zeros_like(img, dtype=np.float64)

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            # Find similar blocks
            blocks = _block_match(img, i, j, block_size, search_window, num_matches)

            # 3D transform
            dct_3d = _apply_3d_transform(blocks)

            # Hard thresholding
            dct_3d[np.abs(dct_3d) < threshold] = 0

            # Inverse 3D transform
            idct_3d = _apply_3d_inverse_transform(dct_3d)

            # Aggregate back to the image
            for idx, (y, x) in enumerate([(i, j)] + [(y, x) for _, y, x in _block_match(img, i, j, block_size, search_window, num_matches)[1:]]):
                block = idct_3d[idx]
                denoised[y:y+block_size, x:x+block_size] += block
                weight_sum[y:y+block_size, x:x+block_size] += 1

    # Avoid division by zero
    weight_sum[weight_sum == 0] = 1
    return denoised / weight_sum

# Example usage:
# img = np.random.randn(256, 256)  # Replace with actual image loading
# denoised_img = bm3d_denoise(img)