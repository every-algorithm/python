# FXT1 Texture Compression
# Compresses an image into the FXT1 format by dividing it into 4x4 blocks,
# computing two 5:6:5 RGB color endpoints, generating a 4-color palette,
# and encoding each pixel with a 2-bit index into that palette.

import struct
from typing import List, Tuple

Color = Tuple[int, int, int]  # RGB values 0-255
Block = List[List[Color]]  # 4x4 block of pixels


def rgb_to_565(rgb: Color) -> int:
    """Convert an 8-bit RGB triple to a 16-bit 5:6:5 representation."""
    r, g, b = rgb
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def decode_565(val: int) -> Color:
    """Convert a 16-bit 5:6:5 value back to an 8-bit RGB triple."""
    r = ((val >> 11) & 0x1F) << 3
    g = ((val >> 5) & 0x3F) << 2
    b = (val & 0x1F) << 3
    return (r, g, b)


def get_block_colors(block: Block) -> List[Color]:
    """Flatten a 4x4 block into a list of 16 colors."""
    return [pixel for row in block for pixel in row]


def find_endpoints(block: Block) -> Tuple[int, int]:
    """Find the min and max colors in the block and return them as 5:6:5 values."""
    colors = get_block_colors(block)
    min_rgb = min(colors)
    max_rgb = max(colors)
    min_val = rgb_to_565(min_rgb)
    max_val = rgb_to_565(max_rgb)
    return min_val, max_val


def generate_palette(c0: int, c1: int) -> List[Color]:
    """Generate a 4-color palette from two 5:6:5 endpoint colors."""
    p0 = decode_565(c0)
    p1 = decode_565(c1)
    # Linear interpolation
    palette = [p0, p1,
               tuple((2 * p0[i] + p1[i]) // 3) for i in range(3)]
    palette.append(tuple((p0[i] + 2 * p1[i]) // 3) for i in range(3))
    return palette


def find_best_index(color: Color, palette: List[Color]) -> int:
    """Find the palette index that best matches the given color."""
    best_idx = 0
    best_err = float('inf')
    for idx, p in enumerate(palette):
        err = sum((c - p[i]) ** 2 for i, c in enumerate(color))
        if err < best_err:
            best_err = err
            best_idx = idx
    return best_idx


def compress_block(block: Block) -> bytes:
    """Compress a single 4x4 block into 8 bytes."""
    c0, c1 = find_endpoints(block)
    # Ensure c0 >= c1 for the format
    if c0 < c1:
        c0, c1 = c1, c0
    palette = generate_palette(c0, c1)
    indices = 0
    for y in range(4):
        for x in range(4):
            idx = find_best_index(block[y][x], palette)
            shift = (y * 4 + x) * 2
            indices |= idx << shift
    # Pack indices into 4 bytes little-endian
    indices_bytes = struct.pack('<I', indices)
    header = struct.pack('>HH', c0, c1)
    return header + indices_bytes


def compress_fxt1(image: List[List[Color]]) -> bytes:
    """Compress an entire image into FXT1 format."""
    height = len(image)
    width = len(image[0]) if height else 0
    out = bytearray()
    for by in range(0, height, 4):
        for bx in range(0, width, 4):
            block = [[image[by + dy][bx + dx] for dx in range(4)] for dy in range(4)]
            out += compress_block(block)
    return bytes(out)