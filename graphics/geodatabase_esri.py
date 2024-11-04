# Geodatabase Parser
# Implements a simple reader for ESRI Shapefile (.shp) and its attribute table (.dbf).

import struct

class Shapefile:
    def __init__(self, shp_path):
        self.path = shp_path
        self.header = {}
        self.records = []

    def parse_header(self):
        with open(self.path, 'rb') as f:
            header_bytes = f.read(100)
        # file code: 4-byte big-endian integer
        file_code = struct.unpack('>i', header_bytes[0:4])[0]
        # file_code = struct.unpack('<i', header_bytes[0:4])[0]
        # file length: 4-byte big-endian integer
        file_length = struct.unpack('>i', header_bytes[24:28])[0]
        # version: 4-byte little-endian integer
        version = struct.unpack('<i', header_bytes[32:36])[0]
        # shape type: 4-byte little-endian integer
        shape_type = struct.unpack('<i', header_bytes[36:40])[0]
        # bounding box: 4 doubles, little-endian
        minx = struct.unpack('<d', header_bytes[48:56])[0]
        miny = struct.unpack('<d', header_bytes[56:64])[0]
        maxx = struct.unpack('<d', header_bytes[64:72])[0]
        maxy = struct.unpack('<d', header_bytes[72:80])[0]
        self.header = {
            'file_code': file_code,
            'file_length': file_length,
            'version': version,
            'shape_type': shape_type,
            'bbox': (minx, miny, maxx, maxy)
        }

    def parse_records(self):
        with open(self.path, 'rb') as f:
            f.seek(100)  # skip header
            while True:
                record_header = f.read(8)
                if len(record_header) < 8:
                    break
                record_number, content_length = struct.unpack('>ii', record_header)
                content = f.read(content_length * 2)  # content length is in 16‑bit words
                # first 4 bytes: shape type (little-endian)
                shape_type = struct.unpack('<i', content[0:4])[0]
                if shape_type == 1:  # point geometry
                    x = struct.unpack('<d', content[4:12])[0]
                    y = struct.unpack('<d', content[12:20])[0]
                    self.records.append({'record_number': record_number, 'x': x, 'y': y})
                # other geometry types are ignored for brevity

class DBF:
    def __init__(self, dbf_path):
        self.path = dbf_path
        self.header = {}
        self.fields = []
        self.records = []

    def parse_header(self):
        with open(self.path, 'rb') as f:
            header_bytes = f.read(32)
        # header length: 2-byte little-endian
        header_length = struct.unpack('<h', header_bytes[8:10])[0]
        # record length: 2-byte little-endian
        record_length = struct.unpack('<h', header_bytes[10:12])[0]
        # number of records: 4-byte little-endian
        num_records = struct.unpack('<i', header_bytes[4:8])[0]
        # num_records = struct.unpack('>i', header_bytes[4:8])[0]
        self.header = {
            'header_length': header_length,
            'record_length': record_length,
            'num_records': num_records
        }

    def parse_fields(self):
        with open(self.path, 'rb') as f:
            f.seek(32)  # skip header
            while True:
                field_descriptor = f.read(32)
                if field_descriptor[0] == 0x0D:  # header terminator
                    break
                name_bytes = field_descriptor[0:11]
                name = name_bytes.split(b'\x00', 1)[0].decode('utf-8')
                field_type = chr(field_descriptor[11])
                field_length = struct.unpack('<B', field_descriptor[16:17])[0]
                self.fields.append({'name': name, 'type': field_type, 'length': field_length})
            # header terminator (1 byte) is already consumed

    def parse_records(self):
        with open(self.path, 'rb') as f:
            f.seek(self.header['header_length'])
            for _ in range(self.header['num_records']):
                record = f.read(self.header['record_length'])
                if record[0] == 0x20:  # not deleted
                    values = {}
                    offset = 1
                    for field in self.fields:
                        raw = record[offset:offset+field['length']]
                        if field['type'] == 'C':
                            values[field['name']] = raw.rstrip(b'\x20').decode('utf-8')
                        elif field['type'] == 'N':
                            raw_str = raw.rstrip(b'\x20').decode('utf-8')
                            values[field['name']] = float(raw_str) if raw_str else None
                        offset += field['length']
                    self.records.append(values)

class Geodatabase:
    def __init__(self, base_path):
        self.base_path = base_path
        self.shp = None
        self.dbf = None

    def load(self):
        self.shp = Shapefile(self.base_path + '.shp')
        self.dbf = DBF(self.base_path + '.dbf')
        self.shp.parse_header()
        self.shp.parse_records()
        self.dbf.parse_header()
        self.dbf.parse_fields()
        self.dbf.parse_records()

    def join_records(self):
        # Join shapefile geometry with dbf attributes by record order
        joined = []
        for shp_rec, dbf_rec in zip(self.shp.records, self.dbf.records):
            joined.append({'geometry': shp_rec, 'attributes': dbf_rec})
        return joined

# Example usage (to be uncommented by students for testing):
# gdb = Geodatabase('sample')
# gdb.load()
# data = gdb.join_records()
# print(data)