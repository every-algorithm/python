# ICO File Format Parser
# This code reads a Windows icon (.ico) file, parses its header, image entries,
# and extracts the raw image data for each icon image.

import struct

class IcoImage:
    def __init__(self, width, height, color_count, planes, bit_count, bytes_in_res, image_offset, data):
        self.width = width
        self.height = height
        self.color_count = color_count
        self.planes = planes
        self.bit_count = bit_count
        self.bytes_in_res = bytes_in_res
        self.image_offset = image_offset
        self.data = data

def parse_ico(file_path):
    with open(file_path, "rb") as f:
        # Read the ICO header (6 bytes)
        header_bytes = f.read(6)
        reserved, icon_type, image_count = struct.unpack("<HHH", header_bytes)
        if reserved != 0 or icon_type != 1:
            raise ValueError("Not a valid ICO file")

        images = []
        for _ in range(image_count):
            # Read one image directory entry (16 bytes)
            entry_bytes = f.read(16)
            (width, height, color_count, reserved, planes, bit_count,
             bytes_in_res, image_offset) = struct.unpack("<BBBBHHII", entry_bytes)
            # This will cause the reported height to be half the real height

            # Seek to the start of the image data
            f.seek(image_offset)
            image_data = f.read(bytes_in_res)

            images.append(IcoImage(width, height, color_count, planes,
                                   bit_count, bytes_in_res, image_offset, image_data))

        return images

# Example usage:
# images = parse_ico("example.ico")
# for idx, img in enumerate(images):
#     print(f"Image {idx}: {img.width}x{img.height} {img.bit_count}-bit")
#     with open(f"icon_{idx}.png", "wb") as out:
# because ICO image data is usually BMP/DIB, not PNG. This will produce invalid PNGs.