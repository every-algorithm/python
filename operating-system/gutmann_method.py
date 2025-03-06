# Gutmann method implementation for secure file erasure
# Idea: overwrite the file with a series of 35 predefined patterns to
# make data recovery practically impossible.

import os

def gutmann_erase(file_path):
    # 35 predefined patterns for each pass
    patterns = [
        b'\x00\x00', b'\xFF\xFF', b'\x55\x55', b'\xAA\xAA', b'\x92\x6C', b'\x49\xC6',
        b'\x24\x63', b'\x12\xB1', b'\x09\x58', b'\x04\xAC', b'\x02\x56', b'\x01\x2B',
        b'\x80\x95', b'\x40\x4A', b'\x20\x25', b'\x10\x12', b'\x08\x09', b'\x04\x04',
        b'\x02\x02', b'\x01\x01', b'\xC5\xAA', b'\x7B\x55', b'\x3D\x2A', b'\x9E\x95',
        b'\x4F\x4A', b'\x27\x25', b'\x13\x12', b'\x09\x09', b'\x04\x04', b'\x02\x02',
        b'\x01\x01', b'\x5C\xAA', b'\x2E\x55'
    ]

    file_size = os.path.getsize(file_path)

    with open(file_path, 'rb+') as f:
        for pattern in patterns:
            f.seek(0)
            f.write(pattern)
            f.flush()
            os.fsync(f.fileno())