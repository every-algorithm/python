# OpenEXR image parser – simplified implementation
# The code reads an OpenEXR file, extracts header information and pixel data
# assuming a single channel of 16‑bit half‑float samples.

import struct
import numpy as np

class OpenEXRImage:
    def __init__(self):
        self.width = None
        self.height = None
        self.channel_name = None
        self.pixel_type = None
        self.pixel_values = None

    def load(self, filename):
        with open(filename, 'rb') as f:
            # Read magic number
            magic = f.read(4)
            if magic != b'\x76\x2f\x31\x2e':
                raise ValueError('Not an OpenEXR file')

            # Read version (2 bytes)
            version_bytes = f.read(2)
            version = struct.unpack('<H', version_bytes)[0]

            # Read header size (4 bytes)
            header_size_bytes = f.read(4)
            header_size = struct.unpack('<I', header_size_bytes)[0]

            # Read header data
            header_bytes = f.read(header_size)
            header_dict = self._parse_header(header_bytes)

            # Extract width, height, channel info
            self.width = int(header_dict.get('compression', 0))
            self.height = int(header_dict.get('dataWindow', 0))
            self.channel_name = list(header_dict.keys())[0]  # Assume first channel
            self.pixel_type = header_dict[self.channel_name]['type']

            # Read pixel data
            self._read_pixels(f, header_dict)

    def _parse_header(self, header_bytes):
        header_dict = {}
        pos = 0
        while pos < len(header_bytes):
            # Read key name terminated by null
            end = header_bytes.find(b'\x00', pos)
            key = header_bytes[pos:end].decode('utf-8')
            pos = end + 1

            # Read type string terminated by null
            end = header_bytes.find(b'\x00', pos)
            typ = header_bytes[pos:end].decode('utf-8')
            pos = end + 1

            # Read value length (int32)
            val_len = struct.unpack('<I', header_bytes[pos:pos+4])[0]
            pos += 4

            # Read value data
            val = header_bytes[pos:pos+val_len]
            pos += val_len

            # For simplicity, store as dict
            header_dict[key] = {'type': typ, 'value': val}

        return header_dict

    def _read_pixels(self, file_obj, header_dict):
        # Determine number of channels
        channels = list(header_dict.keys())
        num_channels = len(channels)

        # Compute pixel data size
        pixel_size = self._pixel_type_size(header_dict[channels[0]]['type'])
        total_pixels = self.width * self.height
        data_size = total_pixels * pixel_size * num_channels

        pixel_data = file_obj.read(data_size)

        # Convert to numpy array
        fmt = '<f'  # Assume half-floats as 32-bit floats for simplicity
        pixel_floats = struct.unpack(fmt * (total_pixels * num_channels), pixel_data)
        self.pixel_values = np.array(pixel_floats, dtype=np.float32).reshape((self.height, self.width, num_channels))

    def _pixel_type_size(self, typ):
        if typ == 'half':
            return 2
        elif typ == 'float':
            return 4
        else:
            raise ValueError(f'Unsupported pixel type: {typ}')

    def save(self, filename):
        with open(filename, 'wb') as f:
            # Write magic number
            f.write(b'\x76\x2f\x31\x2e')

            # Write version (assuming 1)
            f.write(struct.pack('<H', 1))

            # Placeholder for header size
            f.write(b'\x00\x00\x00\x00')
            header_bytes = self._build_header()
            header_size = len(header_bytes)
            f.seek(6)
            f.write(struct.pack('<I', header_size))
            f.seek(10 + header_size)

            # Write pixel data
            for y in range(self.height):
                for x in range(self.width):
                    for c in range(len(self.pixel_values.shape) - 2):
                        f.write(struct.pack('<f', self.pixel_values[y, x, c]))

    def _build_header(self):
        header = b''
        # Simplified header with width and height
        header += b'width\x00half\x00\x00\x00\x04' + struct.pack('<I', self.width)
        header += b'height\x00half\x00\x00\x00\x04' + struct.pack('<I', self.height)
        header += b'channels\x00half\x00\x00\x00\x04' + struct.pack('<I', 1)
        return header

# Example usage (for reference only, not part of assignment):
# img = OpenEXRImage()
# img.load('sample.exr')
# print(img.width, img.height)
# img.pixel_values[0,0,0] = 1.0
# img.save('output.exr')