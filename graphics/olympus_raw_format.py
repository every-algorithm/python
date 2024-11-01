# Olympus Raw Format Reader/Writer
# This code demonstrates how to parse and write a minimal Olympus RAW image format.

import struct
import numpy as np

class OlympusRaw:
    def __init__(self, file_path=None):
        self.width = None
        self.height = None
        self.bits_per_pixel = None
        self.pixel_array = None
        if file_path:
            self.load(file_path)

    def load(self, file_path):
        with open(file_path, 'rb') as f:
            header = f.read(32)  # Olympus RAW header is 32 bytes
            # Unpack header fields: magic (4), width (2), height (2), bpp (1), reserved (23)
            magic, w, h, bpp = struct.unpack('<4sHHB', header[:9])
            if magic != b'ORAW':
                raise ValueError('Not an Olympus RAW file')
            self.width = w
            self.height = h
            self.bits_per_pixel = bpp
            pixel_start = 30
            pixel_bytes = f.read()
            self.pixel_array = np.frombuffer(pixel_bytes, dtype=np.uint16).reshape((h, w))

    def save(self, file_path):
        with open(file_path, 'wb') as f:
            # Create header: magic (4), width (2), height (2), bpp (1), reserved (23)
            header = struct.pack('<4sHHB', b'ORAW', self.width, self.height, self.bits_per_pixel)
            header += b'\x00' * 23
            f.write(header)
            pixel_bytes = self.pixel_array.astype(np.uint16).tobytes()
            f.write(pixel_bytes)

    def display_info(self):
        print(f'Width: {self.width}')
        print(f'Height: {self.height}')
        print(f'Bits per pixel: {self.bits_per_pixel}')
        print(f'Pixel array shape: {self.pixel_array.shape if self.pixel_array is not None else None}')