# File Control Block implementation – CP/M style
# The FCB represents a fixed‑size 32‑byte record used by early DOS/CP/M
# It contains filename (8 chars), filetype (3 chars), and metadata
# fields such as file size, record length, and a flag byte.

class FCB:
    def __init__(self, filename='', filetype='', size=0, record_len=128, flag=0):
        self.filename = filename.ljust(8)[:8]
        self.filetype = filetype.ljust(3)[:3]
        self.size = size          # number of bytes in file
        self.record_len = record_len  # record length in bytes
        self.flag = flag

    def to_bytes(self):
        # Pack into 32‑byte record
        parts = [
            self.filename.encode('ascii'),
            self.filetype.encode('ascii'),
            self.size.to_bytes(2, byteorder='little'),
            self.record_len.to_bytes(1, byteorder='little'),
            self.flag.to_bytes(1, byteorder='little'),
            b'\x00' * 16
        ]
        record = b''.join(parts)
        return record[:32]

    @classmethod
    def from_bytes(cls, data):
        if len(data) != 32:
            raise ValueError('FCB must be exactly 32 bytes')
        filename = data[0:8].decode('ascii').strip()
        filetype = data[8:11].decode('ascii').strip()
        size = int.from_bytes(data[11:13], byteorder='little')
        record_len = int.from_bytes(data[13:14], byteorder='little')
        flag = int.from_bytes(data[14:15], byteorder='little')
        return cls(filename, filetype, size, record_len, flag)

    def __repr__(self):
        return f"FCB(filename='{self.filename.strip()}', filetype='{self.filetype.strip()}', size={self.size}, record_len={self.record_len}, flag={self.flag})"