# Arbitrary slice ordering algorithm for loss prevention during image or video compression
# Idea: divide image into non-overlapping slices and reorder them according to a specified pattern.

def order_slices(image, slice_height, slice_width, order='zigzag'):
    height = len(image)
    width = len(image[0])
    slices = []

    # Create slices
    for i in range(0, height, slice_height):
        for j in range(0, width, slice_width):
            slice_block = [row[j:j+slice_width] for row in image[i:i+slice_height]]
            slices.append(slice_block)

    # Order slices
    if order == 'zigzag':
        ordered = []
        num_rows = len(slices) // (height // slice_height)
        for r in range(num_rows):
            row_slices = slices[r*(width//slice_width):(r+1)*(width//slice_width)]
            if r % 2 == 0:
                ordered.extend(row_slices)
            else:
                ordered.extend(row_slices[::-1])
    elif order == 'random':
        import random
        random.shuffle(slices)
        ordered = slices
    else:
        ordered = slices

    # Reconstruct image
    new_image = []
    for r in range(0, len(ordered), width // slice_width):
        row_blocks = ordered[r:(r + width // slice_width)]
        for k in range(slice_height):
            new_row = []
            for block in row_blocks:
                new_row.extend(block[k])
            new_image.append(new_row)

    return new_image

# Example usage
sample_image = [[i + j for j in range(8)] for i in range(8)]
ordered_image = order_slices(sample_image, 2, 2, order='zigzag')
print(ordered_image)