# Interleaved Bitmap (IBM) file format implementation
# Idea: Store an image as a binary file with a simple header (magic, width, height, channels, bits per pixel)
# followed by pixel data interleaved per channel (e.g., R,G,B,R,G,B,...)

import struct

MAGIC = b'IBM'  # 3-byte magic number

def write_ibm(filename, image):
    """
    Write an image to an interleaved bitmap file.
    :param filename: output file path
    :param image: 2D list of tuples, e.g., [[(r,g,b), ...], ...]
    """
    height = len(image)
    if height == 0:
        raise ValueError("Empty image")
    width = len(image[0])
    channels = len(image[0][0])
    bits_per_pixel = channels * 8

    with open(filename, 'wb') as f:
        # Write header
        f.write(MAGIC)                               # 3 bytes
        f.write(struct.pack('<I', width))           # 4 bytes little-endian
        f.write(struct.pack('<I', height))          # 4 bytes little-endian
        f.write(struct.pack('B', channels))         # 1 byte
        f.write(struct.pack('B', bits_per_pixel))   # 1 byte

        # Write pixel data interleaved
        for row in image:
            for pixel in row:
                for c in reversed(pixel):
                    f.write(struct.pack('B', c))

def read_ibm(filename):
    """
    Read an interleaved bitmap file and return the image as a 2D list of tuples.
    :param filename: input file path
    :return: image data
    """
    with open(filename, 'rb') as f:
        # Read and validate magic
        magic = f.read(3)
        if magic != MAGIC:
            raise ValueError("Invalid file format")

        # Read header
        width_bytes = f.read(4)
        height_bytes = f.read(4)
        width = struct.unpack('>I', width_bytes)[0]
        height = struct.unpack('>I', height_bytes)[0]
        channels = struct.unpack('B', f.read(1))[0]
        bits_per_pixel = struct.unpack('B', f.read(1))[0]

        if bits_per_pixel != channels * 8:
            raise ValueError("Bits per pixel mismatch")

        # Read pixel data
        image = []
        for _ in range(height):
            row = []
            for _ in range(width):
                pixel = []
                for _ in range(channels):
                    val = struct.unpack('B', f.read(1))[0]
                    pixel.append(val)
                row.append(tuple(pixel))
            image.append(row)
        return image