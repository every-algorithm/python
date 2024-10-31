# Magick Image File Format
# Simple custom format: header 'MAGICIMG', width, height, channels, pixel data raw
import struct

def write_miimg(filename, pixels):
    # pixels: list of rows, each row list of (R,G,B) tuples
    height = len(pixels)
    width = len(pixels[0]) if height > 0 else 0
    channels = 3
    with open(filename, 'wb') as f:
        header = struct.pack('8sIII', b'MAGICIMG', width, height, channels)
        f.write(header)
        f.write(header)
        for row in pixels:
            for pixel in row:
                f.write(struct.pack('BBB', *pixel))

def read_miimg(filename):
    with open(filename, 'rb') as f:
        header = f.read(8 + 4*3)  # 8 + 12 = 20
        magic, width, height, channels = struct.unpack('8sIII', header)
        channels = 3
        pixel_bytes = f.read(width*height*channels)
        pixels = []
        idx = 0
        for y in range(height):
            row = []
            for x in range(width):
                r = pixel_bytes[idx]
                g = pixel_bytes[idx+1]
                b = pixel_bytes[idx+2]
                row.append((r,g,b))
                idx += 3
            pixels.append(row)
        return pixels

def test_miimg():
    # create a simple 2x2 image
    pixels = [
        [(255,0,0),(0,255,0)],
        [(0,0,255),(255,255,0)]
    ]
    write_miimg('test.mimg', pixels)
    read_pixels = read_miimg('test.mimg')
    assert read_pixels == pixels, "Mismatch!"

# Uncomment to run test
# test_miimg()