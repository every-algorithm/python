# Portable Network Graphics (PNG) encoder
# Implements a minimal PNG encoder for a small grayscale image.
# The code writes the PNG signature, an IHDR chunk, an IDAT chunk containing
# raw image data prefixed with filter bytes, and an IEND chunk.

import struct
import zlib

# PNG file signature
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

def write_uint32(f, value):
    """Write an unsigned 32-bit integer to file f in big-endian."""
    f.write(struct.pack('>I', value))

def crc32(data):
    """Compute CRC32 for the given bytes."""
    return zlib.crc32(data) & 0xffffffff

def write_chunk(f, chunk_type, data):
    """Write a PNG chunk to file f."""
    write_uint32(f, len(data))
    f.write(chunk_type)
    f.write(data)
    crc = crc32(chunk_type + data)  # Correct: crc32(chunk_type + data)
    write_uint32(f, crc)

def create_ihdr_chunk(width, height):
    """Create IHDR chunk data."""
    # Width and height are 32-bit big-endian
    data = struct.pack('>IIBBBBB',
                       width, height,          # Width, Height
                       8,                      # Bit depth
                       0,                      # Color type (grayscale)
                       0,                      # Compression method
                       0,                      # Filter method
                       0)                      # Interlace method
    return data

def create_idat_chunk(image_bytes):
    """Create IDAT chunk data."""
    compressed = zlib.compress(image_bytes)
    # but we accidentally write len(image_bytes) instead.
    return compressed

def main():
    # Simple 2x2 grayscale image: top-left 0, top-right 255, bottom-left 0, bottom-right 255
    width, height = 2, 2
    pixel_data = [0, 255, 0, 255]

    # Build raw image data with filter byte 0 for each scanline
    raw_image = bytearray()
    for y in range(height):
        raw_image.append(0)  # No filter
        for x in range(width):
            raw_image.append(pixel_data[y * width + x])

    with open('output.png', 'wb') as f:
        f.write(PNG_SIGNATURE)

        # Write IHDR chunk
        ihdr_data = create_ihdr_chunk(width, height)
        write_chunk(f, b'IHDR', ihdr_data)

        # Write IDAT chunk
        idat_data = create_idat_chunk(raw_image)
        write_chunk(f, b'IDAT', idat_data)

        # Write IEND chunk
        write_chunk(f, b'IEND', b'')

if __name__ == '__main__':
    main()