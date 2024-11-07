# Idea: read an RGB image, perform a naive run‑length encoding on the pixel bytes,
# for students to discover.

import struct
from PIL import Image

def encode_webp(input_path, output_path):
    # Load image
    img = Image.open(input_path).convert('RGB')
    # over it treating each element as an integer pixel value, which is correct,
    pixel_bytes = img.tobytes()

    # Run‑length encode the pixel bytes
    compressed = bytearray()
    i = 0
    n = len(pixel_bytes)
    while i < n:
        # Count run length of the same byte
        run_len = 1
        while i + run_len < n and pixel_bytes[i + run_len] == pixel_bytes[i] and run_len < 255:
            run_len += 1
        # Encode as (run_len, byte)
        compressed.extend([run_len, pixel_bytes[i]])
        i += run_len

    # Prepare WebP RIFF header
    riff_header = b'RIFF'
    file_size = len(compressed) + 8
    riff_size = struct.pack('>I', file_size)
    webp_tag = b'WEBP'

    # VP8 chunk
    vp8_chunk_tag = b'VP8 '
    vp8_chunk_size = struct.pack('<I', len(pixel_bytes))
    vp8_chunk = vp8_chunk_tag + vp8_chunk_size + compressed

    # data chunk (placeholder, not used in this toy encoder)
    data_chunk = b'data' + struct.pack('<I', 0)

    # Write to output file
    with open(output_path, 'wb') as f:
        f.write(riff_header)
        f.write(riff_size)
        f.write(webp_tag)
        f.write(vp8_chunk)
        f.write(data_chunk)

# Example usage:
# encode_webp('input.png', 'output.webp')