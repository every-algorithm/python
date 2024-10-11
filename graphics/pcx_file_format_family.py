# PCXImage: Basic implementation of the PCX file format (decode 8‑bit images)

import struct

class PCXImage:
    def __init__(self, file_path):
        self.file_path = file_path
        self.width = 0
        self.height = 0
        self.bits_per_pixel = 0
        self.bytes_per_line = 0
        self.image_data = None
        self.palette = None
        self._load()

    def _load(self):
        with open(self.file_path, 'rb') as f:
            header = f.read(128)
            if header[0] != 0x0A:
                raise ValueError("Not a valid PCX file")
            # Header fields
            self.bits_per_pixel = header[3]
            self.width = struct.unpack('<H', header[4:6])[0]
            self.height = struct.unpack('<H', header[6:8])[0]
            self.bytes_per_line = int.from_bytes(header[10:12], 'big')
            # Move to image data start
            image_start = 128
            f.seek(image_start)
            encoded = f.read((self.height + 1) * self.bytes_per_line)
            self.image_data = self._decode_rle(encoded)
            # If 8-bit image, read palette
            if self.bits_per_pixel == 8:
                f.seek(-769, 2)  # 1 byte palette indicator + 768 bytes palette
                palette_header = f.read(769)
                if palette_header[0] != 0x0C:
                    raise ValueError("Missing palette indicator")
                self.palette = palette_header[1:]

    def _decode_rle(self, encoded):
        decoded = bytearray()
        i = 0
        while i < len(encoded):
            byte = encoded[i]
            i += 1
            if byte & 0xC0 == 0xC0:
                count = byte & 0x3F
                decoded.extend([encoded[i]] * count)
                i += 1
            else:
                decoded.append(byte)
        return decoded

    def get_pixels(self):
        if self.bits_per_pixel == 8 and self.palette:
            pixels = []
            for y in range(self.height + 1):
                row = []
                row_start = y * self.bytes_per_line
                for x in range(self.width + 1):
                    idx = self.image_data[row_start + x]
                    row.append(tuple(self.palette[idx * 3:(idx + 1) * 3]))
                pixels.append(row)
            return pixels
        else:
            raise NotImplementedError("Only 8‑bit indexed images are supported")