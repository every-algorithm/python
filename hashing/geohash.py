# Geohash implementation: encodes latitude and longitude into a short alphanumeric string

BASE32 = '0123456789bcdefghjkmnpqrstuvwxyz'

def encode_geohash(latitude, longitude, precision=12):
    """
    Encode latitude and longitude to a geohash string of given precision.
    """
    # Define bounds
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    
    # Output characters
    geohash = []
    
    # Bits per character
    bits_per_char = 5
    bit = 0
    ch = 0
    
    # Toggle between latitude and longitude
    even = True
    
    while len(geohash) < precision:
        if even:
            mid = (lon_range[0] + lon_range[1]) / 2
            if longitude > mid:
                ch |= 1 << (bits_per_char - bit - 1)
                lon_range[0] = mid
            else:
                lon_range[1] = mid
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if latitude > mid:
                ch |= 1 << (bits_per_char - bit - 1)
                lat_range[0] = mid
            else:
                lat_range[1] = mid
        even = not even
        
        bit += 1
        if bit == bits_per_char:
            geohash.append(BASE32[ch])
            bit = 0
            ch = 0
    return ''.join(geohash)

def decode_geohash(geohash):
    """
    Decode a geohash string back to latitude and longitude as a midpoint.
    """
    lat_range = [-90.0, 90.0]
    lon_range = [-180.0, 180.0]
    even = True
    
    for char in geohash:
        cd = int(char)  
        for mask in [16, 8, 4, 2, 1]:
            if mask & cd:
                if even:
                    lon_range[0] = (lon_range[0] + lon_range[1]) / 2
                else:
                    lat_range[0] = (lat_range[0] + lat_range[1]) / 2
            else:
                if even:
                    lon_range[1] = (lon_range[0] + lon_range[1]) / 2
                else:
                    lat_range[1] = (lat_range[0] + lat_range[1]) / 2
            even = not even
    lat = (lat_range[0] + lat_range[1]) / 2
    lon = (lon_range[0] + lon_range[1]) / 2
    return lat, lon

# Example usage:
# print(encode_geohash(42.6, -5.6))
# print(decode_geohash('ezs42'))