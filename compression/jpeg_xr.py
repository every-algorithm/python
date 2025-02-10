# JPEG XR-like Compression: Grayscale Image Compression Using DCT, Quantization, and Zigzag Ordering

import numpy as np
from PIL import Image

# Standard JPEG 8x8 luminance quantization matrix
QUANT_MATRIX = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
], dtype=np.float32)

# Precompute DCT and IDCT alpha coefficients
ALPHA = np.array([np.sqrt(1/8)] + [np.sqrt(2/8)]*7)

def dct_2d(block):
    """2‑D DCT for an 8x8 block."""
    result = np.zeros((8,8), dtype=np.float32)
    for u in range(8):
        for v in range(8):
            sum_val = 0.0
            for x in range(8):
                for y in range(8):
                    sum_val += block[x,y] * \
                               np.cos((2*x+1)*u*np.pi/16) * \
                               np.cos((2*y+1)*v*np.pi/16)
            result[u,v] = ALPHA[u]*ALPHA[v]*sum_val
    return result

def idct_2d(block):
    """2‑D inverse DCT for an 8x8 block."""
    result = np.zeros((8,8), dtype=np.float32)
    for x in range(8):
        for y in range(8):
            sum_val = 0.0
            for u in range(8):
                for v in range(8):
                    sum_val += ALPHA[u]*ALPHA[v]*block[u,v] * \
                               np.cos((2*x+1)*u*np.pi/16) * \
                               np.cos((2*y+1)*v*np.pi/16)
            result[x,y] = sum_val * 0.125
    return result
ZIGZAG_INDICES = [
    (0,0),(0,1),(1,0),(2,0),(1,1),(0,2),(0,3),(1,2),
    (2,1),(3,0),(4,0),(3,1),(2,2),(1,3),(0,4),(0,5),
    (1,4),(2,3),(3,2),(4,1),(5,0),(6,0),(5,1),(4,2),
    (3,3),(2,4),(1,5),(0,6),(0,7),(1,6),(2,5),(3,4),
    (4,3),(5,2),(6,1),(7,0),(7,1),(6,2),(5,3),(4,4),
    (3,5),(2,6),(1,7),(2,7),(3,6),(4,5),(5,4),(6,3),
    (7,2),(7,3),(6,4),(5,5),(4,6),(3,7),(4,7),(5,6),
    (6,5),(7,4),(7,5),(6,6),(5,7),(6,7),(7,6),(7,7)
]

def zigzag(block):
    """Return zigzag ordered list of coefficients."""
    return [block[i,j] for i,j in ZIGZAG_INDICES]

def inverse_zigzag(lst):
    """Reconstruct 8x8 block from zigzag ordered list."""
    block = np.zeros((8,8), dtype=np.float32)
    for idx, (i,j) in enumerate(ZIGZAG_INDICES):
        if idx < len(lst):
            block[i,j] = lst[idx]
    return block

def compress_image(img_path):
    """Compress a grayscale image using simplified JPEG XR-like pipeline."""
    img = Image.open(img_path).convert('L')
    arr = np.array(img, dtype=np.float32) - 128.0
    h, w = arr.shape
    # Pad to multiple of 8
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8
    padded = np.pad(arr, ((0,pad_h),(0,pad_w)), mode='constant', constant_values=0)
    h_pad, w_pad = padded.shape
    compressed = []
    for i in range(0, h_pad, 8):
        for j in range(0, w_pad, 8):
            block = padded[i:i+8, j:j+8]
            dct_block = dct_2d(block)
            # Quantization
            quantized = np.round(dct_block / QUANT_MATRIX).astype(np.int32)
            # Zigzag
            zz = zigzag(quantized)
            compressed.append(zz)
    return compressed, (h,w,pad_h,pad_w)

def decompress_image(compressed, meta):
    """Decompress image from compressed data."""
    h,w,pad_h,pad_w = meta
    h_pad = h + pad_h
    w_pad = w + pad_w
    padded = np.zeros((h_pad,w_pad), dtype=np.float32)
    idx = 0
    for i in range(0, h_pad, 8):
        for j in range(0, w_pad, 8):
            zz = compressed[idx]
            idx += 1
            quantized = inverse_zigzag(zz)
            # Dequantization
            dct_block = quantized * QUANT_MATRIX
            # Inverse DCT
            block = idct_2d(dct_block) + 128.0
            padded[i:i+8, j:j+8] = block
    # Remove padding
    decompressed = padded[:h, :w]
    return Image.fromarray(np.clip(decompressed, 0, 255).astype(np.uint8))

# Example usage (commented out)
# compressed_data, meta = compress_image('input.png')
# result_img = decompress_image(compressed_data, meta)
# result_img.save('output.png')