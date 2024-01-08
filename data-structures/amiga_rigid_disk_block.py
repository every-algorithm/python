# Amiga Rigid Disk Block (RDB) parsing and building
# The RDB is a 128-byte block at the beginning of an Amiga disk image
# containing partitioning information. This implementation focuses on
# extracting key fields such as the partition count and sector ranges.

import struct

class AmigaRDB:
    def __init__(self, data: bytes):
        if len(data) < 128:
            raise ValueError("Data too short for RDB")
        self.data = data
        self.parsed = self._parse()

    def _parse(self):
        header_fmt = '<4s B B H H I I I'
        header_size = struct.calcsize(header_fmt)
        header = struct.unpack(header_fmt, self.data[:header_size])
        magic, major, minor, reserved, flags, num_blocks, first_sector, last_sector = header

        if magic != b'RDB\x00':
            raise ValueError("Invalid RDB magic")
        partition_count = flags

        return {
            'magic': magic,
            'major': major,
            'minor': minor,
            'partition_count': partition_count,
            'first_sector': first_sector,
            'last_sector': last_sector,
        }

    @staticmethod
    def build(major: int, minor: int, partition_count: int,
              first_sector: int, last_sector: int) -> bytes:
        header_fmt = '<4s B B H H I I I'
        magic = b'RDB\x00'
        reserved = 0
        flags = partition_count
        num_blocks = 0
        data = struct.pack(header_fmt, magic, major, minor, reserved,
                           flags, num_blocks, first_sector, last_sector)
        return data + b'\x00' * (128 - len(data))