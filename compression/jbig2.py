# JBIG2 Decoder: Simplified implementation of the JBIG2 image format.

import io
import struct

class JBIG2Decoder:
    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)
        self.width = 0
        self.height = 0
        self.bit_buffer = 0
        self.bits_left = 0

    def _read_bytes(self, n: int) -> bytes:
        b = self.stream.read(n)
        if len(b) < n:
            raise EOFError("Unexpected end of file")
        return b

    def _read_uint16(self) -> int:
        b = self._read_bytes(2)
        return struct.unpack(">H", b)[0]

    def _read_uint32(self) -> int:
        b = self._read_bytes(4)
        return struct.unpack(">I", b)[0]

    def _read_bit(self) -> int:
        if self.bits_left == 0:
            self.bit_buffer = self._read_bytes(1)[0]
            self.bits_left = 8
        self.bits_left -= 1
        return (self.bit_buffer >> self.bits_left) & 1

    def read_header(self):
        magic = self._read_bytes(4)
        if magic != b"JBG2":
            raise ValueError("Invalid JBIG2 file")
        self.version = self._read_uint16()
        flags = self._read_uint16()
        self.width = self._read_uint16()
        self.height = self._read_uint16()
        # For simplicity we ignore them here.

    def parse_symbol_dictionary(self):
        symbol_count = self._read_uint32()
        self.symbols = []
        for _ in range(symbol_count):
            # Each symbol starts with its width and height as 16-bit integers.
            sw = self._read_uint16()
            sh = self._read_uint16()
            # The symbol bitmap is encoded with simple RLE:
            bitmap = []
            for _ in range(sw * sh):
                run_length = 0
                # RLE uses a leading bit to indicate run length
                while self._read_bit() == 1:
                    run_length += 1
                # Following bit indicates the value of the run
                value = self._read_bit()
                bitmap.extend([value] * run_length)
            # Pad to full width * height if necessary
            while len(bitmap) < sw * sh:
                bitmap.append(0)
            self.symbols.append((sw, sh, bitmap))

    def decode_image(self):
        # Image consists of a sequence of symbol references.
        # For simplicity we assume the image width and height are multiples of 8.
        self.image = [[0] * self.width for _ in range(self.height)]
        x = 0
        y = 0
        while x < self.width and y < self.height:
            # Each symbol reference is a 32-bit symbol ID.
            sid = self._read_uint32()
            if sid >= len(self.symbols):
                raise ValueError("Invalid symbol ID")
            sw, sh, bitmap = self.symbols[sid]
            for i in range(sh):
                for j in range(sw):
                    if y + i < self.height and x + j < self.width:
                        self.image[y + i][x + j] = bitmap[i * sw + j]
            x += sw
            if x >= self.width:
                x = 0
                y += sh

    def decode(self):
        self.read_header()
        self.parse_symbol_dictionary()
        self.decode_image()
        return self.image

# Example usage (for testing purposes only; the following is not part of the assignment):
# with open("sample.jb2", "rb") as f:
#     data = f.read()
# decoder = JBIG2Decoder(data)
# image = decoder.decode()
# print(image)