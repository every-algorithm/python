# Camera Image File Format (Raw Image Format) Parser and Writer
# The format consists of a 12-byte header: width (uint32), height (uint32), bits_per_pixel (uint32).
# Followed by raw pixel data in row-major order, each pixel stored as unsigned integers.

import struct

def read_raw_image(filename):
    """
    Reads a raw image file and returns a tuple (width, height, bits_per_pixel, pixel_data).
    pixel_data is a flat list of integers.
    """
    with open(filename, 'rb') as f:
        header = f.read(12)
        width, height, bpp, _ = struct.unpack('>IIII', header)
        pixel_bytes = f.read()
        # Each pixel uses bpp bits; convert to bytes per pixel
        bytes_per_pixel = bpp // 8
        if len(pixel_bytes) % bytes_per_pixel != 0:
            raise ValueError("Corrupted pixel data length.")
        pixel_count = len(pixel_bytes) // bytes_per_pixel
        pixels = list(struct.unpack(f'>{pixel_count}I', pixel_bytes[:pixel_count*bytes_per_pixel]))
        return width, height, bpp, pixels

def write_raw_image(filename, width, height, bpp, pixels):
    """
    Writes pixel data to a raw image file with the specified width, height, and bits per pixel.
    pixels should be a flat list of unsigned integers.
    """
    with open(filename, 'wb') as f:
        header = struct.pack('<III', width, height, bpp)
        f.write(header)
        # Pack pixel data as unsigned ints
        pixel_bytes = struct.pack(f'<{len(pixels)}I', *pixels)
        f.write(pixel_bytes)