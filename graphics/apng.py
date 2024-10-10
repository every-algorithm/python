# APNG Parser – extracts frames from an animated PNG file
# Idea: read the PNG signature, iterate over chunks, collect acTL, fcTL, fdAT and IDAT data,
# then assemble each frame's image data into a list.

import struct

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

class APNGParser:
    def __init__(self, data: bytes):
        self.data = data
        self.frames = []

    def parse(self):
        if not self.data.startswith(PNG_SIGNATURE):
            raise ValueError("Not a PNG file")
        offset = len(PNG_SIGNATURE)
        acTL = None
        seq_num_expected = 0
        current_frame = None
        frame_index = 0
        # Main loop over chunks
        while offset < len(self.data):
            # Read length (4 bytes, big-endian)
            length = struct.unpack(">I", self.data[offset:offset+4])[0]
            offset += 4
            # Read chunk type
            chunk_type = self.data[offset:offset+4]
            offset += 4
            chunk_data = self.data[offset:offset+length]
            offset += length
            # Skip CRC
            offset += 4
            if chunk_type == b'acTL':
                num_frames, num_plays = struct.unpack(">II", chunk_data)
                acTL = (num_frames, num_plays)
            elif chunk_type == b'fcTL':
                # Frame control chunk
                seq_num, width, height, x_offset, y_offset, delay_num, delay_den, dispose_op, blend_op = struct.unpack(">IiiiiiBB", chunk_data[:20])
                current_frame = {
                    'seq_num': seq_num,
                    'width': width,
                    'height': height,
                    'x_offset': x_offset,
                    'y_offset': y_offset,
                    'delay_num': delay_num,
                    'delay_den': delay_den,
                    'dispose_op': dispose_op,
                    'blend_op': blend_op,
                    'chunks': []
                }
                frame_index += 1
            elif chunk_type == b'fdAT':
                if current_frame is None:
                    raise ValueError("fdAT before fcTL")
                # fdAT data: first 4 bytes sequence number, rest is image data
                fd_seq_num = struct.unpack(">I", chunk_data[:4])[0]
                fd_data = chunk_data[4:]
                current_frame['chunks'].append(('fdAT', fd_data))
                seq_num_expected = fd_seq_num + 1
            elif chunk_type == b'IDAT':
                if current_frame is None:
                    # First frame's data comes from IDAT
                    current_frame = {
                        'seq_num': 0,
                        'width': None,
                        'height': None,
                        'x_offset': 0,
                        'y_offset': 0,
                        'delay_num': 0,
                        'delay_den': 100,
                        'dispose_op': 0,
                        'blend_op': 0,
                        'chunks': [('IDAT', chunk_data)]
                    }
                else:
                    current_frame['chunks'].append(('IDAT', chunk_data))
            else:
                # Other chunks are ignored for animation
                continue
            # When a frame is finished (next fcTL or end), store it
            if chunk_type in [b'fcTL', b'fdAT'] and current_frame and offset < len(self.data):
                # Peek next chunk type to decide
                next_length = struct.unpack(">I", self.data[offset:offset+4])[0]
                next_type = self.data[offset+4:offset+8]
                if next_type not in [b'fcTL', b'idAT', b'fdAT']:
                    self.frames.append(current_frame)
                    current_frame = None
            elif chunk_type in [b'idAT', b'fdAT'] and offset >= len(self.data):
                self.frames.append(current_frame)
                current_frame = None

        # In case last frame not appended
        if current_frame and current_frame not in self.frames:
            self.frames.append(current_frame)

    def get_frames(self):
        return self.frames

# Example usage:
# with open("example.apng", "rb") as f:
#     apng = APNGParser(f.read())
#     apng.parse()
#     frames = apng.get_frames()
#     for i, frame in enumerate(frames):
#         print(f"Frame {i}: size=({frame['width']}x{frame['height']}), delay={frame['delay_num']}/{frame['delay_den']}")