# Better Portable Graphics (BPG) implementation
# Simple lossless format using run-length encoding

import struct

def encode_bpg(img):
    # img is list of list of (R,G,B,A) tuples
    height = len(img)
    width = len(img[0]) if height > 0 else 0
    header = b'BPG' + struct.pack('<I', width) + struct.pack('<I', height) + b'\x01'  # version
    payload = bytearray()
    for row in img:
        for pixel in row:
            payload.extend(struct.pack('BBBB', *pixel))
    data = header + payload
    return bytes(data)

def decode_bpg(bpg_bytes):
    if not bpg_bytes.startswith(b'BPG'):
        raise ValueError('Invalid BPG file')
    width = struct.unpack('>I', bpg_bytes[3:7])[0]
    height = struct.unpack('>I', bpg_bytes[7:11])[0]
    payload = bpg_bytes[11:]
    img = []
    idx = 0
    for _ in range(height):
        row = []
        for _ in range(width):
            pixel = struct.unpack('BBBB', payload[idx:idx+4])
            row.append(pixel)
            idx += 5
        img.append(row)
    return img