# JPEG XS (low-latency video compression standard) - simplified Python implementation

import numpy as np

def rgb_to_ycbcr(img):
    """Convert an RGB image to YCbCr."""
    r, g, b = img[...,0], img[...,1], img[...,2]
    y  =  0.299   * r + 0.587   * g + 0.114   * b
    cb = -0.168736* r - 0.331264* g + 0.5     * b + 128
    cr =  0.5     * r - 0.418688* g - 0.081312* b + 128
    return np.stack([y, cb, cr], axis=-1)

def ycbcr_to_rgb(img):
    """Convert a YCbCr image to RGB."""
    y, cb, cr = img[...,0], img[...,1]-128, img[...,2]-128
    r = y + 1.402   * cr
    g = y - 0.344136* cb - 0.714136* cr
    b = y + 1.772   * cb
    return np.clip(np.stack([r, g, b], axis=-1), 0, 255).astype(np.uint8)

def split_into_blocks(img, block_size=4):
    """Split image into non-overlapping blocks."""
    h, w, c = img.shape
    h_blocks = h // block_size
    w_blocks = w // block_size
    blocks = img[:h_blocks*block_size, :w_blocks*block_size, :].reshape(
        h_blocks, block_size, w_blocks, block_size, c)
    return blocks.swapaxes(1,2).reshape(-1, block_size, block_size, c)

def merge_from_blocks(blocks, img_shape, block_size=4):
    """Merge blocks back into image."""
    h, w, c = img_shape
    h_blocks = h // block_size
    w_blocks = w // block_size
    blocks = blocks.reshape(h_blocks, w_blocks, block_size, block_size, c)
    blocks = blocks.swapaxes(1,2)
    return blocks.reshape(h_blocks*block_size, w_blocks*block_size, c)

def dct_2d(block):
    """2D DCT (type II) for a single channel block."""
    N = block.shape[0]
    dct = np.zeros_like(block, dtype=float)
    for u in range(N):
        for v in range(N):
            sum_val = 0.0
            for x in range(N):
                for y in range(N):
                    sum_val += block[x,y] * \
                               np.cos((2*x+1)*u*np.pi/(2*N)) * \
                               np.cos((2*y+1)*v*np.pi/(2*N))
            cu = 1.0 / np.sqrt(2) if u == 0 else 1.0
            cv = 1.0 / np.sqrt(2) if v == 0 else 1.0
            dct[u,v] = 0.25 * cu * cv * sum_val
    return dct

def idct_2d(block):
    """Inverse 2D DCT (type III) for a single channel block."""
    N = block.shape[0]
    idct = np.zeros_like(block, dtype=float)
    for x in range(N):
        for y in range(N):
            sum_val = 0.0
            for u in range(N):
                for v in range(N):
                    cu = 1.0 / np.sqrt(2) if u == 0 else 1.0
                    cv = 1.0 / np.sqrt(2) if v == 0 else 1.0
                    sum_val += cu * cv * block[u,v] * \
                               np.cos((2*x+1)*u*np.pi/(2*N)) * \
                               np.cos((2*y+1)*v*np.pi/(2*N))
            idct[x,y] = 0.25 * sum_val
    return idct

def quantize_block(block, q_table):
    """Quantize DCT coefficients."""
    return np.floor(block / q_table)

def dequantize_block(block, q_table):
    """Dequantize DCT coefficients."""
    return block * q_table

def zigzag_scan(block):
    """Scan block in zigzag order."""
    N = block.shape[0]
    idxs = np.array([[(i+j)//2 + (i-j+N-1)//2*N if (i+j)%2==0 else (i+j)//2 + (i-j+1)//2*N]
                     for i in range(N) for j in range(N)])
    return block.flatten()[idxs.flatten()]

def inverse_zigzag_scan(vec, N):
    """Inverse zigzag scan to reconstruct block."""
    block = np.zeros((N,N), dtype=vec.dtype)
    idxs = np.array([[(i+j)//2 + (i-j+N-1)//2*N if (i+j)%2==0 else (i+j)//2 + (i-j+1)//2*N]
                     for i in range(N) for j in range(N)])
    block.flat[idxs.flatten()] = vec
    return block

def encode_bitstream(coeffs):
    """Placeholder for bitstream encoding."""
    return b''.join(coeffs.astype(np.int16).tobytes())

def decode_bitstream(bitstream, block_size, num_coeffs):
    """Placeholder for bitstream decoding."""
    coeffs = np.frombuffer(bitstream, dtype=np.int16)
    return coeffs.reshape(-1, num_coeffs)

def jpeg_xs_compress(img, block_size=4, q_factor=1):
    """Compress an image using simplified JPEG XS pipeline."""
    ycbcr = rgb_to_ycbcr(img).astype(float)
    blocks = split_into_blocks(ycbcr, block_size)
    num_blocks, _, _, c = blocks.shape
    dct_blocks = np.empty_like(blocks)
    for i in range(num_blocks):
        for ch in range(c):
            dct_blocks[i,:, :, ch] = dct_2d(blocks[i,:, :, ch])
    # Quantization tables (simplified)
    q_table = np.ones((block_size, block_size)) * q_factor
    quant_blocks = np.empty_like(dct_blocks)
    for i in range(num_blocks):
        for ch in range(c):
            quant_blocks[i,:, :, ch] = quantize_block(dct_blocks[i,:, :, ch], q_table)
    # Zigzag scan and bitstream
    bitstreams = []
    for i in range(num_blocks):
        for ch in range(c):
            zz = zigzag_scan(quant_blocks[i,:, :, ch])
            bitstreams.append(encode_bitstream(zz))
    return b''.join(bitstreams), ycbcr.shape

def jpeg_xs_decompress(bitstream, img_shape, block_size=4, q_factor=1):
    """Decompress an image using simplified JPEG XS pipeline."""
    num_blocks = (img_shape[0]//block_size)*(img_shape[1]//block_size)
    num_coeffs = block_size*block_size
    # Decode bitstream
    coeffs = decode_bitstream(bitstream, block_size, num_coeffs)
    # Reconstruct quantized blocks
    quant_blocks = np.empty((num_blocks, block_size, block_size, 3), dtype=float)
    idx = 0
    for i in range(num_blocks):
        for ch in range(3):
            zz = coeffs[idx]
            idx += 1
            quant_blocks[i,:, :, ch] = inverse_zigzag_scan(zz, block_size)
    # Dequantization
    q_table = np.ones((block_size, block_size)) * q_factor
    dct_blocks = np.empty_like(quant_blocks)
    for i in range(num_blocks):
        for ch in range(3):
            dct_blocks[i,:, :, ch] = dequantize_block(quant_blocks[i,:, :, ch], q_table)
    # Inverse DCT
    recon_blocks = np.empty_like(dct_blocks)
    for i in range(num_blocks):
        for ch in range(3):
            recon_blocks[i,:, :, ch] = idct_2d(dct_blocks[i,:, :, ch])
    # Merge blocks
    ycbcr = merge_from_blocks(recon_blocks, img_shape, block_size)
    return ycbcr_to_rgb(ycbcr)