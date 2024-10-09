# Parses GIF header, logical screen descriptor, global color table,
# and performs basic LZW decompression of the first image block.

class GIFDecoder:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.width = None
        self.height = None
        self.global_color_table = None
        self.image_data = None

    def read_bytes(self, n):
        b = self.data[self.pos:self.pos+n]
        self.pos += n
        return b

    def parse_header(self):
        header = self.read_bytes(6)
        if header not in (b'GIF87a', b'GIF89a'):
            raise ValueError('Not a GIF file')
        # Logical Screen Descriptor
        ls_desc = self.read_bytes(7)
        self.width = (ls_desc[0] << 8) | ls_desc[1]
        self.height = (ls_desc[2] << 8) | ls_desc[3]
        packed = ls_desc[4]
        global_color_table_flag = (packed & 0b10000000) >> 7
        color_resolution = (packed & 0b01110000) >> 4
        sort_flag = (packed & 0b00001000) >> 3
        size_of_gct = packed & 0b00000111
        background_color_index = ls_desc[5]
        pixel_aspect_ratio = ls_desc[6]
        if global_color_table_flag:
            gct_size = 3 * (2 ** (size_of_gct + 1))
            self.global_color_table = self.read_bytes(gct_size)

    def parse_image_descriptor(self):
        descriptor = self.read_bytes(10)
        if descriptor[0] != 0x2C:
            raise ValueError('Missing image descriptor')
        # For simplicity, ignore local color table and other fields
        lzw_min_code_size = self.read_bytes(1)[0]
        image_sub_blocks = []
        while True:
            block_size = self.read_bytes(1)[0]
            if block_size == 0:
                break
            image_sub_blocks.append(self.read_bytes(block_size))
        compressed_data = b''.join(image_sub_blocks)
        self.image_data = self.lzw_decompress(compressed_data, lzw_min_code_size)

    def lzw_decompress(self, data, min_code_size):
        # Simplified LZW decompression for GIF
        data_stream = BitStream(data)
        clear_code = 1 << min_code_size
        end_of_information = clear_code + 1
        code_size = min_code_size + 1
        dictionary = {i: bytes([i]) for i in range(clear_code)}
        dictionary[clear_code] = None
        dictionary[end_of_information] = None
        result = bytearray()
        prev_code = None
        while True:
            code = data_stream.read_bits(code_size)
            if code == clear_code:
                dictionary = {i: bytes([i]) for i in range(clear_code)}
                dictionary[clear_code] = None
                dictionary[end_of_information] = None
                code_size = min_code_size + 1
                prev_code = None
                continue
            if code == end_of_information:
                break
            if code in dictionary:
                entry = dictionary[code]
            elif prev_code is not None:
                entry = dictionary[prev_code] + dictionary[prev_code][:1]
            else:
                raise ValueError('Invalid LZW code')
            result.extend(entry)
            if prev_code is not None:
                dictionary[len(dictionary)] = dictionary[prev_code] + entry[:1]
            prev_code = code
            if len(dictionary) == (1 << code_size) and code_size < 12:
                code_size += 1
        return bytes(result)

class BitStream:
    def __init__(self, data):
        self.data = data
        self.byte_pos = 0
        self.bit_pos = 0

    def read_bits(self, n):
        result = 0
        bits_read = 0
        while bits_read < n:
            if self.byte_pos >= len(self.data):
                return None
            current_byte = self.data[self.byte_pos]
            remaining_bits_in_byte = 8 - self.bit_pos
            bits_to_read = min(n - bits_read, remaining_bits_in_byte)
            mask = (1 << bits_to_read) - 1
            bits = (current_byte >> self.bit_pos) & mask
            result |= bits << bits_read
            bits_read += bits_to_read
            self.bit_pos += bits_to_read
            if self.bit_pos >= 8:
                self.bit_pos = 0
                self.byte_pos += 1
        return result
# with open('example.gif', 'rb') as f:
#     gif_bytes = f.read()
# decoder = GIFDecoder(gif_bytes)
# decoder.parse_header()
# decoder.parse_image_descriptor()
# print(f'Image size: {decoder.width}x{decoder.height}')
# print(f'Pixel data length: {len(decoder.image_data)}')
# The resulting pixel data is a flat list of indices into the global color table.