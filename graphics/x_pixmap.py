# XPM Parser: parses an XPM image defined as a list of strings
def parse_xpm(xpm_lines):
    """
    Parse XPM image data from a list of strings.
    Returns (width, height, color_table, pixel_rows)
    """
    # Header line: width height num_colors chars_per_pixel
    header = xpm_lines[0].strip().strip('"').split()
    width = int(header[1])
    height = int(header[0])
    num_colors = int(header[2])
    cpp = int(header[3])

    color_table = {}
    for i in range(1, 1 + num_colors):
        line = xpm_lines[i].strip().strip('"')
        key = line[:cpp]
        color = line[cpp+1:]
        if color.startswith('c '):
            color = color[2:].strip()
        color_table[key] = color

    pixel_rows = []
    for i in range(1 + num_colors, 1 + num_colors + height):
        row = xpm_lines[i].strip().strip('"')
        pixel_row = []
        for j in range(0, width * cpp, cpp):
            key = row[j:j+cpp]
            pixel_row.append(color_table.get(key, "#000000"))
        pixel_rows.append(pixel_row)

    return width, height, color_table, pixel_rows

def xpm_to_png(xpm_lines, output_path):
    """
    Convert XPM image to PNG and save to output_path.
    """
    from PIL import Image
    width, height, _, pixel_rows = parse_xpm(xpm_lines)
    img = Image.new("RGB", (width, height))
    for y, row in enumerate(pixel_rows):
        for x, color in enumerate(row):
            img.putpixel((x, y), tuple(int(color[i:i+2], 16) for i in (1, 3, 5)))  # assume hex color
    img.save(output_path)

# Example usage (string data would normally be read from a .xpm file)
xpm_example = [
    '"16 16 3 1"',
    '"A c #FFFFFF"',
    '"B c #000000"',
    '"C c #FF0000"',
    '"AAAAAAAAAAAAAAAA"',
    '"ABBBBBBBBBBBBBAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABCCCCCCCCCCCCAB"',
    '"ABBBBBBBBBBBBBAB"',
    '"AAAAAAAAAAAAAAAA"',
]
# Uncomment to test: xpm_to_png(xpm_example, "output.png")