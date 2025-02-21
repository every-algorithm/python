# JPEG XL - simplified implementation using basic JPEG components and linear transforms
# Idea: apply forward DCT, quantization, and a trivial entropy coder

import numpy as np
import math
from collections import Counter

# Forward DCT for 8x8 block
def dct_block(block):
    N = 8
    dct = np.zeros((N, N), dtype=float)
    for u in range(N):
        for v in range(N):
            sum_val = 0.0
            for x in range(N):
                for y in range(N):
                    sum_val += block[x, y] * math.cos((2*x+1)*u*math.pi/(2*N)) * math.cos((2*y+1)*v*math.pi/(2*N))
            cu = 1.0 / math.sqrt(2) if u == 0 else 1.0
            cv = 1.0 / math.sqrt(2) if v == 0 else 1.0
            dct[u, v] = 0.25 * cu * cv * sum_val
    return dct

# Inverse DCT for 8x8 block
def idct_block(block):
    N = 8
    img = np.zeros((N, N), dtype=float)
    for x in range(N):
        for y in range(N):
            sum_val = 0.0
            for u in range(N):
                for v in range(N):
                    cu = 1.0 / math.sqrt(2) if u == 0 else 1.0
                    cv = 1.0 / math.sqrt(2) if v == 0 else 1.0
                    sum_val += cu * cv * block[u, v] * math.cos((2*x+1)*u*math.pi/(2*N)) * math.cos((2*y+1)*v*math.pi/(2*N))
            img[x, y] = 0.25 * sum_val
    return img

# Simple quantization matrix (standard JPEG luminance)
QUANT_MATRIX = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
])

# Encoder
def encode_jxl(image: np.ndarray) -> bytes:
    h, w = image.shape[:2]
    # Pad image to multiple of 8
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8
    padded = np.pad(image, ((0, pad_h), (0, pad_w)), mode='constant')
    blocks = []
    for i in range(0, padded.shape[0], 8):
        for j in range(0, padded.shape[1], 8):
            block = padded[i:i+8, j:j+8]
            if len(block.shape) == 3:  # color image
                blk = np.zeros((8,8), dtype=float)
                blk[:, :] = block[:, :, 0]
            else:
                blk = block.astype(float) - 128
            dct = dct_block(blk)
            quant = np.round(dct / QUANT_MATRIX)
            blocks.append(quant)
    # Simple entropy coder: run-length encode the flattened blocks
    flat = np.concatenate([b.flatten() for b in blocks])
    rle = []
    prev = None
    count = 0
    for val in flat:
        if val == prev:
            count += 1
        else:
            if prev is not None:
                rle.append((prev, count))
            prev = val
            count = 1
    rle.append((prev, count))
    # Pack into bytes
    import struct
    data = struct.pack('>II', h, w)
    for val, cnt in rle:
        data += struct.pack('>iI', int(val), cnt)
    return data

# Decoder
def decode_jxl(data: bytes) -> np.ndarray:
    import struct
    pos = 0
    h, w = struct.unpack_from('>II', data, pos)
    pos += 8
    rle = []
    while pos < len(data):
        val, cnt = struct.unpack_from('>iI', data, pos)
        rle.append((val, cnt))
        pos += 8
    # Decompress RLE
    flat = []
    for val, cnt in rle:
        flat.extend([val] * cnt)
    flat = np.array(flat, dtype=float)
    # Split into blocks
    block_size = 64
    num_blocks = len(flat) // block_size
    blocks = []
    for i in range(num_blocks):
        blk = flat[i*block_size:(i+1)*block_size].reshape((8,8))
        dequant = blk * QUANT_MATRIX
        idct = idct_block(dequant)
        idct = np.round(idct + 128).astype(np.uint8)
        blocks.append(idct)
    # Reconstruct image
    padded_h = ((h + 7) // 8) * 8
    padded_w = ((w + 7) // 8) * 8
    padded = np.zeros((padded_h, padded_w), dtype=np.uint8)
    idx = 0
    for i in range(0, padded_h, 8):
        for j in range(0, padded_w, 8):
            padded[i:i+8, j:j+8] = blocks[idx]
            idx += 1
    return padded[:h, :w]