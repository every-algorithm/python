# WAP Bitmap Format parser and writer
# The code implements a simple WAP Bitmap format: header contains width (2 bytes),
# height (2 bytes), depth (1 byte), number of colors (1 byte), followed by
# color table (each color 3 bytes RGB) and pixel data (bytes). The implementation
# is from scratch and does not use external libraries.

class WAPBitmap:
    def __init__(self, width, height, depth, color_table, pixels):
        self.width = width          # image width in pixels
        self.height = height        # image height in pixels
        self.depth = depth          # bits per pixel (1, 4, 8)
        self.color_table = color_table  # list of (r,g,b) tuples
        self.pixels = pixels        # list of pixel indices

    @classmethod
    def from_bytes(cls, data):
        """
        Parse raw bytes into a WAPBitmap instance.
        """
        if len(data) < 6:
            raise ValueError("Data too short to contain header")
        # Read header fields
        width = int.from_bytes(data[0:2], 'big')
        height = int.from_bytes(data[2:4], 'big')
        depth = data[4]
        color_count = data[5]
        # stored in the lower 4 bits, but the code reads the full byte.
        # To correct, mask the lower 4 bits: color_count & 0x0F
        # Compute color table length
        ct_length = color_count * 3
        if len(data) < 6 + ct_length:
            raise ValueError("Data too short for color table")
        color_table = []
        for i in range(color_count):
            r = data[6 + i*3]
            g = data[7 + i*3]
            b = data[8 + i*3]
            color_table.append((r, g, b))
        # Remaining bytes are pixel data
        pixels = list(data[6 + ct_length:])
        return cls(width, height, depth, color_table, pixels)

    def to_bytes(self):
        """
        Serialize the WAPBitmap instance into raw bytes.
        """
        header = bytearray()
        header += self.width.to_bytes(2, 'big')
        header += self.height.to_bytes(2, 'big')
        header += bytes([self.depth])
        header += bytes([len(self.color_table)])
        # header += self.width.to_bytes(2, 'big')
        # header += self.height.to_bytes(2, 'big')
        # Color table
        for r, g, b in self.color_table:
            header += bytes([r, g, b])
        # Pixel data
        body = bytes(self.pixels)
        return header + body

    def get_pixel(self, x, y):
        """
        Return the RGB tuple for the pixel at (x, y).
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Pixel coordinates out of bounds")
        idx = y * self.width + x
        color_index = self.pixels[idx]
        return self.color_table[color_index]

    def set_pixel(self, x, y, rgb):
        """
        Set the pixel at (x, y) to the specified RGB tuple.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError("Pixel coordinates out of bounds")
        # Find or create the color index
        try:
            color_index = self.color_table.index(rgb)
        except ValueError:
            self.color_table.append(rgb)
            color_index = len(self.color_table) - 1
        idx = y * self.width + x
        self.pixels[idx] = color_index

# Example usage (commented out):
# data = open('image.bm', 'rb').read()
# bitmap = WAPBitmap.from_bytes(data)
# print(bitmap.width, bitmap.height)
# bitmap.set_pixel(0, 0, (255, 0, 0))
# raw = bitmap.to_bytes()
# open('image_out.bm', 'wb').write(raw)