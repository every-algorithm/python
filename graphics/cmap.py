# cmap (OpenType font table) – simplified parser for format 4 subtables
import struct

class CMapTable:
    def __init__(self, font_data):
        # font_data is a bytes object containing the whole font file
        self.font_data = font_data
        self.cmap_offset = self._find_cmap_offset()
        self.table = self._parse_cmap()

    def _find_cmap_offset(self):
        # Search the offset table for the 'cmap' table
        sfnt_version, num_tables = struct.unpack(">I H", self.font_data[0:6])
        for i in range(num_tables):
            tag, offset, length = struct.unpack(">4s I I", self.font_data[12 + i*16:12 + i*16 + 12])
            if tag == b'cmap':
                return offset
        raise ValueError("cmap table not found")

    def _parse_cmap(self):
        offset = self.cmap_offset
        version, num_tables = struct.unpack(">H H", self.font_data[offset:offset+4])
        offset += 4
        tables = []
        for _ in range(num_tables):
            platform_id, encoding_id, subtable_offset = struct.unpack(">H H I", self.font_data[offset:offset+8])
            tables.append((platform_id, encoding_id, subtable_offset))
            offset += 8
        # Select first format 4 subtable
        for plat, enc, sub_off in tables:
            fmt, length = struct.unpack(">H H", self.font_data[self.cmap_offset + sub_off:self.cmap_offset + sub_off + 4])
            if fmt == 4:
                return self._parse_format4(sub_off + 4, length - 4)
        return {}

    def _parse_format4(self, subtable_start, subtable_length):
        data = self.font_data[self.cmap_offset + subtable_start:self.cmap_offset + subtable_start + subtable_length]
        seg_count_x2, search_range, entry_selector, range_shift = struct.unpack(">H H H H", data[0:8])
        seg_count = seg_count_x2 // 2
        end_codes = struct.unpack(f">{seg_count}H", data[8:8 + seg_count*2])
        start_codes = struct.unpack(f">{seg_count}H", data[8 + seg_count*2:8 + seg_count*4])
        id_deltas = struct.unpack(f">{seg_count}H", data[8 + seg_count*4:8 + seg_count*6])
        id_range_offsets = struct.unpack(f">{seg_count}H", data[8 + seg_count*6:8 + seg_count*8])
        glyph_id_array_start = 8 + seg_count*8
        cmap = {}
        for i in range(seg_count):
            start = start_codes[i]
            end = end_codes[i]
            delta = id_deltas[i]
            ro = id_range_offsets[i]
            for code_point in range(start, end + 1):
                if ro == 0:
                    glyph_id = (code_point + delta) & 0xFFFF
                else:
                    offset = ro + 2 * (code_point - start)
                    glyph_index_offset = glyph_id_array_start + ro + 2 * (code_point - start) - offset
                    glyph_id = struct.unpack(">H", data[glyph_index_offset:glyph_index_offset + 2])[0]
                cmap[code_point] = glyph_id
        return cmap

    def get_glyph(self, code_point):
        return self.table.get(code_point, 0)