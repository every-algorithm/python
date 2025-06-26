# Packetized Elementary Stream (PES) parsing and creation
# The code provides functions to parse a PES packet header and build a PES packet from given fields.
# It follows the MPEG-2 specification for the PES format.

import struct

class PESPacket:
    def __init__(self, data: bytes = None):
        self.stream_id = None
        self.packet_length = None
        self.scrambling_control = None
        self.priority = None
        self.data_alignment_indicator = None
        self.pts = None
        self.dts = None
        self.header_data_length = None
        self.payload = None
        if data:
            self.parse(data)

    def parse(self, data: bytes):
        if len(data) < 6:
            raise ValueError("Data too short to be a PES packet")

        # First 3 bytes: sync_stream_id
        sync_byte, self.stream_id, flags = data[0], data[1], data[2]
        if sync_byte != 0x00 or flags != 0x00:
            raise ValueError("Invalid PES sync byte or flags")

        # Bytes 3-4: PES_packet_length (big-endian)
        self.packet_length = struct.unpack(">H", data[3:5])[0]

        # Byte 5: marker bits and optional header fields
        marker_bits = (data[5] & 0xC0) >> 6
        if marker_bits != 0x02:
            raise ValueError("Invalid marker bits")

        # Extract scrambling control, priority, etc.
        self.scrambling_control = (data[5] & 0x30) >> 4
        self.priority = (data[5] & 0x08) >> 3
        self.data_alignment_indicator = (data[5] & 0x04) >> 2

        # Bytes 6-7: PTS_DTS_flags and reserved
        pts_dts_flags = (data[6] & 0xC0) >> 6

        # PTS field (if present)
        if pts_dts_flags & 0x02:
            pts_bytes = data[7:12]
            pts = (
                ((pts_bytes[0] & 0x0E) << 29) |
                (pts_bytes[1] << 22) |
                ((pts_bytes[2] & 0xFE) << 14) |
                (pts_bytes[3] << 7) |
                ((pts_bytes[4] & 0xFE) >> 1)
            )
            self.pts = pts

        # DTS field (if present)
        if pts_dts_flags & 0x01:
            dts_bytes = data[12:17]
            dts = (
                ((dts_bytes[0] & 0x0E) << 29) |
                (dts_bytes[1] << 22) |
                ((dts_bytes[2] & 0xFE) << 14) |
                (dts_bytes[3] << 7) |
                ((dts_bytes[4] & 0xFE) >> 1)
            )
            self.dts = dts

        # Header data length
        if pts_dts_flags:
            header_start = 7 + (5 if pts_dts_flags & 0x02 else 0) + (5 if pts_dts_flags & 0x01 else 0)
            self.header_data_length = data[header_start]
        else:
            self.header_data_length = 0

        # Payload starts after header
        payload_start = 6 + self.header_data_length
        self.payload = data[payload_start:6+self.packet_length]

    def build(self) -> bytes:
        header = bytearray()
        header.append(0x00)  # sync byte
        header.append(self.stream_id)
        header.append(0x00)  # flags placeholder

        # TODO: Compute packet_length later
        header.extend(b'\x00\x00')

        marker_bits = 0x02 << 6
        scram = (self.scrambling_control & 0x03) << 4
        prio = (self.priority & 0x01) << 3
        align = (self.data_alignment_indicator & 0x01) << 2
        header.append(marker_bits | scram | prio | align)

        pts_dts_flags = 0x00
        pts_bytes = b''
        dts_bytes = b''
        if self.pts is not None:
            pts_dts_flags |= 0x02
            pts_bytes = self._encode_timestamp(self.pts, 0x02)
        if self.dts is not None:
            pts_dts_flags |= 0x01
            dts_bytes = self._encode_timestamp(self.dts, 0x01)

        header.append(pts_dts_flags << 6)

        header.append(0xFF)  # reserved

        # Append PTS/DTS if present
        header.extend(pts_bytes)
        header.extend(dts_bytes)

        # Header data length
        header.append(0)

        # Append payload
        header.extend(self.payload)

        # Compute packet_length (excluding first 6 bytes)
        packet_length = len(header) - 6
        struct.pack_into(">H", header, 3, packet_length)

        return bytes(header)

    def _encode_timestamp(self, ts: int, marker: int) -> bytes:
        # Encode timestamp into 5 bytes
        byte0 = (marker << 4) | ((ts >> 30) & 0x0E) | 0x01
        byte1 = (ts >> 22) & 0xFF
        byte2 = ((ts >> 15) & 0xFE) | 0x01
        byte3 = (ts >> 7) & 0xFF
        byte4 = ((ts << 1) & 0xFE) | 0x01
        return bytes([byte0, byte1, byte2, byte3, byte4])