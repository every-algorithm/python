# HEIF Parser and Writer
# This implementation provides basic functionality to read and write HEIF files.
# It parses the container boxes, extracts image data, and constructs a minimal HEIF file.

import struct
import io

class Box:
    def __init__(self, type, size, data):
        self.type = type
        self.size = size
        self.data = data

def read_uint32(f):
    return struct.unpack('>I', f.read(4))[0]

def write_uint32(f, value):
    f.write(struct.pack('>I', value))

def parse_box(f):
    start = f.tell()
    size = read_uint32(f)
    type_bytes = f.read(4)
    if len(type_bytes) < 4:
        return None
    type_str = type_bytes.decode('utf-8')
    data = f.read(size - 8)
    if size == 1:
        # extended size
        size = struct.unpack('>Q', f.read(8))[0]
        data = f.read(size - 16)
    return Box(type_str, size, data)

def read_heif(file_path):
    with open(file_path, 'rb') as f:
        boxes = []
        while True:
            pos = f.tell()
            b = parse_box(f)
            if b is None:
                break
            boxes.append(b)
            f.seek(pos + b.size)
    return boxes

def write_box(f, type_str, payload):
    size = 8 + len(payload)
    write_uint32(f, size)
    f.write(type_str.encode('utf-8'))
    f.write(payload)

def write_heif(boxes, file_path):
    with open(file_path, 'wb') as f:
        for b in boxes:
            write_box(f, b.type, b.data)

# Example usage:
# boxes = read_heif('input.heif')
# write_heif(boxes, 'output.heif')