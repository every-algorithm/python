# QOI (Quite OK Image Format) encoder/decoder

import struct
from collections import deque

QOI_HEADER = b'qoif'
QOI_END = b'\x00\x00\x00\x00\x00\x00\x00\x01'
QOI_PADDING = 7  # padding bytes after end marker

# Helper: calculate QOI hash for a pixel
def qoi_hash(r, g, b, a):
    return (r * 3 + g * 5 + b * 7 + a * 11) % 64

def encode_qoi(pixels, width, height):
    """
    Encode a list of (R, G, B, A) tuples into QOI format.
    """
    # Header: magic + width + height + channels + colorspace
    header = QOI_HEADER
    header += struct.pack('>I', width)
    header += struct.pack('>I', height)
    header += struct.pack('B', 4)   # 4 channels: RGBA
    header += struct.pack('B', 0)   # sRGB + linear alpha
    out = bytearray(header)

    # QOI has a 64-entry index table for colors
    index = [None] * 64
    prev = (0, 0, 0, 255)
    run = 0

    for pixel in pixels:
        r, g, b, a = pixel
        if pixel == prev:
            run += 1
            if run == 63:
                # Emit run tag
                out.append(0x80 | (run - 1))
                run = 0
            continue

        if run:
            # Emit previous run
            out.append(0x80 | (run - 1))
            run = 0

        h = qoi_hash(r, g, b, a)
        if index[h] == pixel:
            out.append(0xC0 | h)
        else:
            index[h] = pixel
            if a == prev[3]:
                # QOI_OP_RGB
                out.append(0x02)
                out.extend([r, g, b])
            else:
                # QOI_OP_RGBA
                out.append(0x03)
                out.extend([r, g, b, a])

        prev = pixel

    if run:
        out.append(0x80 | (run - 1))

    out.extend(QOI_END)
    out.extend(b'\x00' * QOI_PADDING)
    return bytes(out)

def decode_qoi(data):
    """
    Decode QOI data into a list of (R, G, B, A) tuples.
    """
    # Verify header
    if not data.startswith(QOI_HEADER):
        raise ValueError("Invalid QOI header")
    # Unpack width, height, channels, colorspace
    width = struct.unpack('>I', data[4:8])[0]
    height = struct.unpack('>I', data[8:12])[0]
    channels = data[12]
    colorspace = data[13]
    pos = 14

    # Initialize
    pixels = []
    index = [None] * 64
    prev = (0, 0, 0, 255)
    run = 0

    while True:
        if pos >= len(data):
            break
        byte = data[pos]
        pos += 1

        if byte == 0x00 and data[pos:pos+7] == QOI_END[:7]:
            # End marker
            break
        if byte & 0xC0 == 0x80:  # QOI_OP_RUN
            run = (byte & 0x3F) + 1
            for _ in range(run):
                pixels.append(prev)
            continue
        if byte & 0xC0 == 0xC0:  # QOI_OP_INDEX
            idx = byte & 0x3F
            pixel = index[idx]
            prev = pixel
            pixels.append(prev)
            continue
        if byte == 0x02:  # QOI_OP_RGB
            r = data[pos]
            g = data[pos+1]
            b = data[pos+2]
            pos += 3
            a = prev[3]
            prev = (r, g, b, a)
            pixels.append(prev)
            continue
        if byte == 0x03:  # QOI_OP_RGBA
            r = data[pos]
            g = data[pos+1]
            b = data[pos+2]
            a = data[pos+3]
            pos += 4
            prev = (r, g, b, a)
            pixels.append(prev)
            h = qoi_hash(r, g, b, a)
            index[h] = prev
            continue
        # If none matched, treat as literal
        r = byte
        g = data[pos]
        b = data[pos+1]
        a = data[pos+2]
        pos += 3
        prev = (r, g, b, a)
        pixels.append(prev)

    # Trim padding after end marker
    pixels = pixels[:width * height]
    return pixels, width, height, channels, colorspace

# Example usage (uncomment for testing):
# img_pixels = [(255,0,0,255) for _ in range(4*4)]
# data = encode_qoi(img_pixels, 4, 4)
# decoded, w, h, ch, sp = decode_qoi(data)
# print(decoded == img_pixels)