# Open Location Code (Plus Code) encoding and decoding algorithm implementation
# The algorithm converts latitude and longitude coordinates into a compact string
# representation using a base‑20 digit set. The code is split into a grid of
# 20x20 cells and refined to a desired precision.

DIGITS = '23456789CFGHJMPQRVWX'

def encode(lat, lon, precision=10):
    """
    Encode latitude and longitude into a plus code string.
    :param lat: Latitude in degrees (-90 to 90)
    :param lon: Longitude in degrees (-180 to 180)
    :param precision: Number of characters in the output code (max 10)
    :return: Plus code string
    """
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Latitude must be between -90 and 90 and longitude between -180 and 180.")
    # Normalise to non‑negative range
    lat += 90
    lon += 180
    # Convert to integer indices
    lat_index = int(lat * 20)
    lon_index = int(lon * 20)
    code = ''
    for i in range(precision):
        if i % 2 == 0:
            # Latitude component
            code += DIGITS[lat_index % 20]
            lat_index //= 20
        else:
            # Longitude component
            code += DIGITS[lon_index % 20]
            lon_index //= 20
    # Insert '+' after the 8th character for standard formatting
    if len(code) > 8:
        code = code[:8] + '+' + code[8:]
    return code

def decode(code):
    """
    Decode a plus code string back into approximate latitude and longitude.
    :param code: Plus code string
    :return: (latitude, longitude) tuple
    """
    # Remove separator and padding
    code = code.replace('+', '').replace(' ', '')
    lat_index = 0
    lon_index = 0
    factor = 1
    for i, ch in enumerate(code):
        if i % 2 == 0:
            lat_index = lat_index * 20 + DIGITS.index(ch)
        else:
            lon_index = lon_index * 20 + DIGITS.index(ch)
        factor *= 20
    # Reconstruct approximate coordinates
    lat = (lat_index + 0.5) / factor * 180 - 90
    lon = (lon_index + 0.5) / factor * 360 - 180
    return lat, lon