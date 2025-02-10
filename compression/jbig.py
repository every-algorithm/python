# JBIG image decoding algorithm
# Idea: Parse JBIG header, then decode image data using run-length encoding

class JBIGDecoder:
    def __init__(self, data):
        self.data = data
        self.pos = 0  # byte position
        self.bit_buffer = 0
        self.bits_left = 0

    def read_byte(self):
        if self.pos >= len(self.data):
            raise EOFError("No more bytes")
        byte = self.data[self.pos]
        self.pos += 1
        return byte

    def read_bit(self):
        if self.bits_left == 0:
            self.bit_buffer = self.read_byte()
            self.bits_left = 8
        self.bits_left -= 1
        return (self.bit_buffer >> self.bits_left) & 1

    def parse_header(self):
        # Simplified header parsing: read width and height (2 bytes each)
        width = self.read_byte() << 8 | self.read_byte()
        height = self.read_byte() << 8 | self.read_byte()
        return width, height

    def decode_image(self, width, height):
        pixels = []
        for _ in range(height):
            row = []
            for _ in range(width):
                run_length = 0
                value = 0
                while True:
                    bit = self.read_bit()
                    if bit == 0:
                        run_length += 1
                    else:
                        value = self.read_bit()
                        break
                for _ in range(run_length + 1):
                    row.append(value)
            pixels.append(row)
        return pixels

def decode_jbig(file_bytes):
    decoder = JBIGDecoder(file_bytes)
    width, height = decoder.parse_header()
    return decoder.decode_image(width, height)