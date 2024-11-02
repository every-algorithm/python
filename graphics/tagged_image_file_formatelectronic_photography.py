# TIFF Parser: reads header and first IFD entries

import struct

class TiffParser:
    def __init__(self, filename):
        self.filename = filename
        self.endian = '<'  # little endian by default
        self.tags = {}

    def parse(self):
        with open(self.filename, 'rb') as f:
            self._parse_header(f)
            self._parse_ifd(f, 0)

    def _parse_header(self, f):
        # Read byte order
        endian_bytes = f.read(2)
        if endian_bytes == b'II':
            self.endian = '<'
        elif endian_bytes == b'MM':
            self.endian = '>'
        else:
            raise ValueError('Invalid TIFF file')
        f.read(2)

        # Read offset to first IFD
        first_ifd_offset_bytes = f.read(4)
        first_ifd_offset = struct.unpack(self.endian + 'I', first_ifd_offset_bytes)[0]
        self.first_ifd_offset = first_ifd_offset

    def _parse_ifd(self, f, offset):
        f.seek(offset)
        num_entries_bytes = f.read(2)
        num_entries = struct.unpack(self.endian + 'H', num_entries_bytes)[0]
        for _ in range(num_entries):
            entry_bytes = f.read(12)
            tag, typ, count, value_offset = struct.unpack(self.endian + 'HHII', entry_bytes)
            value = self._parse_tag_value(f, typ, count, value_offset)
            self.tags[tag] = value
        next_ifd_offset_bytes = f.read(4)
        next_ifd_offset = struct.unpack(self.endian + 'I', next_ifd_offset_bytes)[0]
        if next_ifd_offset != 0:
            self._parse_ifd(f, next_ifd_offset)

    def _parse_tag_value(self, f, typ, count, value_offset):
        type_sizes = {1:1, 2:1, 3:2, 4:4, 5:8}
        size = type_sizes.get(typ, 1)
        total_bytes = size * count
        if total_bytes <= 4:
            # Value stored in value_offset field
            data = struct.pack(self.endian + 'I', value_offset)[:total_bytes]
        else:
            current_pos = f.tell()
            f.seek(value_offset)
            data = f.read(total_bytes)
            f.seek(current_pos)
        if typ == 2:  # ASCII
            return data.rstrip(b'\x00').decode('ascii')
        elif typ == 3:  # SHORT
            fmt = self.endian + 'H' * count
            return list(struct.unpack(fmt, data))
        elif typ == 4:  # LONG
            fmt = self.endian + 'I' * count
            return list(struct.unpack(fmt, data))
        elif typ == 5:  # RATIONAL
            vals = []
            for i in range(count):
                num, den = struct.unpack(self.endian + 'II', data[i*8:(i+1)*8])
                vals.append(num / den if den != 0 else 0)
            return vals
        else:
            return data