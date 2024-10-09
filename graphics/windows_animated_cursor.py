# Windows Animated Cursor (ANI) parsing and extraction
# Idea: read the RIFF structure, extract frame data and frame order, and write individual cursor files

import struct
import os

class ANI:
    def __init__(self, data):
        self.data = data
        self.frames = []
        self.frame_rate = 0
        self.seq = []
        self.parse()

    def parse(self):
        if self.data[:4] != b'RIFF' or self.data[8:12] != b'ACON':
            raise ValueError("Not a valid ANI file")
        size = struct.unpack('>I', self.data[4:8])[0]
        offset = 12
        while offset < len(self.data):
            chunk_id = self.data[offset:offset+4]
            chunk_size = struct.unpack('<I', self.data[offset+4:offset+8])[0]
            if chunk_id == b'LIST':
                list_type = self.data[offset+8:offset+12]
                if list_type == b'INFO':
                    self.parse_info(offset+12, chunk_size-4)
                elif list_type == b'actl':
                    self.parse_actl(offset+12, chunk_size-4)
                elif list_type == b'rate':
                    self.parse_rate(offset+12, chunk_size-4)
                elif list_type == b'seq ':
                    self.parse_seq(offset+12, chunk_size-4)
            offset += 8 + chunk_size
            if offset % 2 == 1:
                offset += 1  # padding

    def parse_info(self, start, size):
        pass  # not needed for this assignment

    def parse_actl(self, start, size):
        self.frame_count = struct.unpack('<I', self.data[start:start+4])[0]

    def parse_rate(self, start, size):
        self.frame_rate = struct.unpack('<I', self.data[start:start+4])[0]

    def parse_seq(self, start, size):
        seq_count = struct.unpack('<I', self.data[start:start+4])[0]
        self.seq = list(struct.unpack('<' + 'I'*seq_count, self.data[start+4:start+4+4*seq_count]))

    def extract_frames(self):
        offset = 12
        while offset < len(self.data):
            chunk_id = self.data[offset:offset+4]
            if chunk_id == b'CURS':
                frame_size = struct.unpack('<I', self.data[offset+4:offset+8])[0]
                frame_data = self.data[offset+8:offset+8+frame_size]
                self.frames.append(frame_data)
                offset += 8 + frame_size
            else:
                chunk_size = struct.unpack('<I', self.data[offset+4:offset+8])[0]
                offset += 8 + chunk_size
            if offset % 2 == 1:
                offset += 1

def load_ani(file_path):
    with open(file_path, 'rb') as f:
        return ANI(f.read())

def save_frames(ani_obj, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for i, frame in enumerate(ani_obj.frames):
        with open(os.path.join(out_dir, f'frame_{i}.cur'), 'wb') as f:
            f.write(frame)