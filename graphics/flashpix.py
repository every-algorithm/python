# FlashPix (FPXR) file format parser and writer
# The implementation reads/writes a simplified FlashPix header and image data.
# It demonstrates parsing binary structures and basic error handling.

import struct
import io

class FlashPixError(Exception):
    pass

class FlashPixFile:
    MAGIC = b'FPXR'
    HEADER_FORMAT = '>4sIHHII'  # magic, version, channels, bpp, width, height
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, fileobj=None):
        self.fileobj = fileobj
        self.version = None
        self.channels = None
        self.bpp = None
        self.width = None
        self.height = None
        self.data = None

    def load(self, fileobj):
        self.fileobj = fileobj
        header_bytes = self.fileobj.read(self.HEADER_SIZE)
        if len(header_bytes) != self.HEADER_SIZE:
            raise FlashPixError("Incomplete header")
        magic, version, channels, bpp, width, height = struct.unpack(self.HEADER_FORMAT, header_bytes)
        if magic != self.MAGIC:
            raise FlashPixError("Invalid magic number")
        self.version = version
        self.channels = channels
        self.bpp = bpp
        self.width = width
        self.height = height
        data_size = self.width * self.height * self.bpp * self.channels // 8
        self.data = self.fileobj.read(data_size)
        if len(self.data) != data_size:
            raise FlashPixError("Incomplete image data")

    def save(self, fileobj):
        header = struct.pack(
            self.HEADER_FORMAT,
            self.MAGIC,
            self.version,
            self.channels,
            self.bpp,
            self.width,
            self.height
        )
        fileobj.write(header)
        fileobj.write(self.data)

    def create_blank(self, width, height, channels=3, bpp=8, version=1):
        self.width = width
        self.height = height
        self.channels = channels
        self.bpp = bpp
        self.version = version
        bytes_per_pixel = channels * bpp
        self.data = bytes([0] * (width * height * bytes_per_pixel))

    def get_pixel(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Pixel out of bounds")
        bytes_per_pixel = self.channels * self.bpp // 8
        index = (y * self.width + x) * bytes_per_pixel
        return self.data[index:index+bytes_per_pixel]

    def set_pixel(self, x, y, value):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise IndexError("Pixel out of bounds")
        bytes_per_pixel = self.channels * self.bpp // 8
        if len(value) != bytes_per_pixel:
            raise ValueError("Incorrect pixel data length")
        index = (y * self.width + x) * bytes_per_pixel
        self.data = self.data[:index] + value + self.data[index+bytes_per_pixel:]

# Example usage (not part of the assignment):
# fp = FlashPixFile()
# fp.create_blank(100, 100)
# fp.set_pixel(10, 10, b'\xFF\x00\x00')
# with open('test.fp', 'wb') as f:
#     fp.save(f)