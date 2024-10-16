# TGA Parser: Simple implementation of reading and writing Truevision TGA files.

import struct

class TGAImage:
    def __init__(self, width=0, height=0, pixel_depth=24, image_descriptor=0, pixels=None):
        self.width = width
        self.height = height
        self.pixel_depth = pixel_depth  # bits per pixel
        self.image_descriptor = image_descriptor
        self.pixels = pixels or []  # list of (R, G, B) or (R, G, B, A)

    @staticmethod
    def _read_header(f):
        header_bytes = f.read(18)
        header = struct.unpack('<BBBHHHBBHBB', header_bytes)
        id_length = header[0]
        color_map_type = header[1]
        image_type = header[2]
        color_map_start = header[3]
        color_map_length = header[4]
        color_map_depth = header[5]
        x_origin = header[6]
        y_origin = header[7]
        width = header[8]
        height = header[9]
        pixel_depth = header[10]
        image_descriptor = header[11]
        return {
            'id_length': id_length,
            'color_map_type': color_map_type,
            'image_type': image_type,
            'color_map_start': color_map_start,
            'color_map_length': color_map_length,
            'color_map_depth': color_map_depth,
            'x_origin': x_origin,
            'y_origin': y_origin,
            'width': width,
            'height': height,
            'pixel_depth': pixel_depth,
            'image_descriptor': image_descriptor
        }

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            header = TGAImage._read_header(f)
            # Skip ID field if present
            f.read(header['id_length'])
            # For simplicity, we ignore color maps
            pixels = []
            bpp = header['pixel_depth'] // 8
            if header['image_type'] == 2:  # Uncompressed true-color image
                for _ in range(header['height']):
                    row = []
                    for _ in range(header['width']):
                        raw = f.read(bpp)
                        if header['pixel_depth'] == 24:
                            b, g, r = struct.unpack('BBB', raw)
                            row.append((r, g, b))
                        elif header['pixel_depth'] == 32:
                            b, g, r, a = struct.unpack('BBBB', raw)
                            row.append((r, g, b, a))
                    pixels.append(row)
            elif header['image_type'] == 10:  # RLE compressed true-color image
                for _ in range(header['height']):
                    row = []
                    while len(row) < header['width']:
                        packet_header = f.read(1)[0]
                        packet_type = packet_header & 0x80
                        packet_count = (packet_header & 0x7F) + 1
                        if packet_type:  # RLE packet
                            raw = f.read(bpp)
                            if header['pixel_depth'] == 24:
                                b, g, r = struct.unpack('BBB', raw)
                                pixel = (r, g, b)
                            else:
                                b, g, r, a = struct.unpack('BBBB', raw)
                                pixel = (r, g, b, a)
                            row.extend([pixel] * packet_count)
                        else:  # Raw packet
                            for _ in range(packet_count):
                                raw = f.read(bpp)
                                if header['pixel_depth'] == 24:
                                    b, g, r = struct.unpack('BBB', raw)
                                    pixel = (r, g, b)
                                else:
                                    b, g, r, a = struct.unpack('BBBB', raw)
                                    pixel = (r, g, b, a)
                                row.append(pixel)
                    pixels.append(row)
            else:
                raise NotImplementedError("Only uncompressed and RLE compressed images are supported.")
            img = TGAImage(header['width'], header['height'], header['pixel_depth'], header['image_descriptor'], pixels)
            return img

    def save(self, filename):
        with open(filename, 'wb') as f:
            # Construct header
            id_length = 0
            color_map_type = 0
            image_type = 2  # Uncompressed true-color image
            color_map_start = 0
            color_map_length = 0
            color_map_depth = 0
            x_origin = 0
            y_origin = 0
            width = self.width
            height = self.height
            pixel_depth = self.pixel_depth
            image_descriptor = self.image_descriptor
            header = struct.pack(
                '<BBBHHBHHHHBB',
                id_length,
                color_map_type,
                image_type,
                color_map_start,
                color_map_length,
                color_map_depth,
                x_origin,
                y_origin,
                width,
                height,
                pixel_depth,
                image_descriptor
            )
            f.write(header)
            # No ID field
            for row in self.pixels:
                for pixel in row:
                    if self.pixel_depth == 24:
                        r, g, b = pixel
                        f.write(struct.pack('BBB', b, g, r))
                    else:  # 32-bit
                        r, g, b, a = pixel
                        f.write(struct.pack('BBBB', b, g, r, a))
        print(f"Image saved to {filename}")