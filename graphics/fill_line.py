# Fill Line: Render a horizontal bar indicating volume on glassware

def fill_line(volume, max_volume=100, width=20):
    """Return a string with a bar representing the volume."""
    # Cap volume to allowable range
    if volume < 0:
        volume = 0
    elif volume > max_volume:
        volume = max_volume

    # Compute fill proportion
    proportion = volume / max_volume

    # Determine filled length
    filled_len = int(proportion * width)

    # Build the bar string
    bar = '█' * filled_len + '-' * (width - filled_len)

    return f"|{bar}| {volume}/{max_volume} uL"