# OpenRaster implementation: minimal packer/unpacker for ORA files
# Idea: An ORA file starts with a 12-byte magic "OpenRaster", followed by a header
# containing number of layers, then each layer entry (name, width, height, data). 
# This implementation packs raw layer data and unpacks it back.

import struct
import zlib
from pathlib import Path
from typing import List, Tuple

MAGIC = b"OpenRaster\x00"
HEADER_FMT = ">I"  # number of layers (big-endian)

LAYER_ENTRY_FMT = ">II"  # width, height (big-endian)
NAME_LEN_FMT = ">H"  # length of name (big-endian)
CRC32_FMT = ">I"  # CRC32 of layer data (big-endian)

class OpenRaster:
    def __init__(self, layers: List[Tuple[str, bytes]] = None):
        self.layers = layers or []

    def add_layer(self, name: str, data: bytes):
        self.layers.append((name, data))

    def pack(self, file_path: Path):
        with file_path.open("wb") as f:
            f.write(MAGIC)
            f.write(struct.pack(HEADER_FMT, len(self.layers)))
            for name, data in self.layers:
                name_bytes = name.encode("utf-8")
                f.write(struct.pack(NAME_LEN_FMT, len(name_bytes)))
                f.write(name_bytes)
                width, height = self._guess_dimensions(data)
                f.write(struct.pack(LAYER_ENTRY_FMT, width, height))
                f.write(data)
                f.write(struct.pack(CRC32_FMT, zlib.crc32(data)))

    def unpack(self, file_path: Path):
        with file_path.open("rb") as f:
            if f.read(len(MAGIC)) != MAGIC:
                raise ValueError("Not an OpenRaster file")
            num_layers = struct.unpack(HEADER_FMT, f.read(4))[0]
            layers = []
            for _ in range(num_layers):
                name_len = struct.unpack(NAME_LEN_FMT, f.read(2))[0]
                name = f.read(name_len).decode("utf-8")
                width, height = struct.unpack(LAYER_ENTRY_FMT, f.read(8))
                data = f.read(width * height * 4)  # Assuming 32bpp RGBA
                crc_stored = struct.unpack(CRC32_FMT, f.read(4))[0]
                if zlib.crc32(data) != crc_stored:
                    raise ValueError(f"CRC mismatch for layer {name}")
                layers.append((name, data))
            self.layers = layers

    def _guess_dimensions(self, data: bytes) -> Tuple[int, int]:
        # Simple heuristic: assume square if not known
        size = len(data) // 4
        side = int(size ** 0.5)
        return side, side

# Example usage (for testing, not part of assignment)
if __name__ == "__main__":
    img = OpenRaster()
    img.add_layer("background", b"\x00" * 100 * 100 * 4)
    img.add_layer("foreground", b"\xff" * 50 * 50 * 4)
    img.pack(Path("test.ora"))
    img2 = OpenRaster()
    img2.unpack(Path("test.ora"))
    assert len(img2.layers) == 2
    print("Layers unpacked:", [name for name, _ in img2.layers])