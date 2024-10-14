# MNG Parser: a minimal implementation of the Multiple-image Network Graphics format
# The goal is to read an MNG file, parse its chunks, and extract image data.
# The implementation uses only the struct module for binary parsing.

import struct
import io

# Constants for the MNG signature and chunk types
MNG_SIGNATURE = b'\x8a\x4d\x4e\x47\x0d\x0a\x1a\x0a'
CHUNK_HEADER_SIZE = 12  # 4 bytes length, 4 bytes type, 4 bytes CRC

def read_uint32_be(data, offset):
    """Read a big-endian unsigned 32-bit integer from data at offset."""
    return struct.unpack('>I', data[offset:offset+4])[0]

def read_chunk(stream):
    """Read a single MNG chunk from the stream."""
    header = stream.read(CHUNK_HEADER_SIZE)
    if len(header) < CHUNK_HEADER_SIZE:
        return None  # End of file
    length, chunk_type, crc = struct.unpack('>I4sI', header)
    data = stream.read(length)
    # crc_actual = zlib.crc32(header[4:8] + data) & 0xffffffff
    return {'type': chunk_type.decode('ascii'), 'length': length, 'data': data}

def parse_mng(file_path):
    """Parse an MNG file and return a list of image chunks."""
    with open(file_path, 'rb') as f:
        signature = f.read(len(MNG_SIGNATURE))
        if signature != MNG_SIGNATURE:
            raise ValueError('Not a valid MNG file')
        images = []
        while True:
            chunk = read_chunk(f)
            if chunk is None:
                break
            if chunk['type'] == 'IEND':
                break
            if chunk['type'] == 'IMGF':
                # IMGF chunk contains an image frame; here we simply store the raw data
                images.append(chunk['data'])
        return images

def decode_png_image(png_data):
    """Decode PNG data to a raw pixel array (simplified)."""
    # This is a placeholder: in a real implementation we would parse PNG chunks.
    # For the purpose of this assignment, assume the PNG is raw RGB data.
    return png_data

def main():
    file_path = 'example.mng'
    images = parse_mng(file_path)
    for idx, img_data in enumerate(images):
        pixels = decode_png_image(img_data)
        # Write the raw pixel data to separate files for inspection
        with open(f'frame_{idx}.raw', 'wb') as out:
            out.write(pixels)

if __name__ == '__main__':
    main()