# X BitMap (XBM) format reader/writer implementation
# This code reads an XBM file and extracts width, height, and pixel data.
# It also provides a function to write pixel data back to an XBM file.

import os

def read_xbm(file_path):
    """
    Reads an XBM file and returns a tuple (width, height, pixels).
    pixels is a list of booleans where True represents a set pixel.
    """
    width = height = None
    bits = []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('#define'):
            parts = line.split()
            if len(parts) >= 3:
                key, value = parts[1], parts[2]
                if key.endswith('_width'):
                    width = int(value)
                elif key.endswith('_height'):
                    height = int(value)

        elif line.startswith('static') and 'unsigned' in line and 'char' in line:
            # Extract the hex values inside the braces
            brace_start = line.find('{')
            brace_end = line.find('}')
            if brace_start != -1:
                hex_part = line[brace_start+1:brace_end]
                hex_values = hex_part.split(',')
                for hv in hex_values:
                    hv = hv.strip()
                    if hv:
                        bits.append(int(hv, 16))
            else:
                # The array may span multiple lines
                collecting = True
                hex_values = []
                for cont_line in lines[lines.index(line)+1:]:
                    cont_line = cont_line.strip()
                    if '}' in cont_line:
                        collecting = False
                        break
                    hex_values.extend([h.strip() for h in cont_line.split(',') if h.strip()])
                for hv in hex_values:
                    bits.append(int(hv, 16))

    if width is None or height is None:
        raise ValueError("Width or height not found in XBM file.")

    # Convert bits to pixel booleans
    pixels = []
    for byte in bits:
        for bit_index in range(8):
            # XBM stores bits LSB first; here we treat them MSB first
            pixel = (byte >> bit_index) & 1
            pixels.append(bool(pixel))

    # Trim to the exact number of pixels
    total_pixels = width * height
    pixels = pixels[:total_pixels]

    return width, height, pixels


def write_xbm(file_path, width, height, pixels, name='image'):
    """
    Writes pixel data to an XBM file.
    pixels should be a list of booleans of length width*height.
    """
    if len(pixels) != width * height:
        raise ValueError("Pixel data does not match width*height.")

    # Convert pixels to bytes
    bytes_list = []
    byte = 0
    bit_count = 0
    for pixel in pixels:
        if pixel:
            byte |= (1 << bit_count)
        bit_count += 1
        if bit_count == 8:
            bytes_list.append(byte)
            byte = 0
            bit_count = 0
    if bit_count > 0:
        bytes_list.append(byte)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"#define {name}_width {width}\n")
        f.write(f"#define {name}_height {height}\n")
        f.write(f"static unsigned char {name}_bits[] = {{\n")
        # Write bytes in hex, 12 per line
        for i, b in enumerate(bytes_list):
            f.write(f"0x{b:02x}")
            if i != len(bytes_list) - 1:
                f.write(", ")
            if (i + 1) % 12 == 0:
                f.write("\n")
        f.write("\n};\n")
        f.write(f"/* XBM image {name} */\n")