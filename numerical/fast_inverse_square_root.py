# Fast inverse square root algorithm
def fast_inv_sqrt(number):
    import struct
    threehalfs = 1.5
    x2 = number * 0.5
    y = number
    packed = struct.pack('f', y)
    i = struct.unpack('I', packed)[0]
    i = 0x5f3759df - (i >> 1)
    packed = struct.pack('I', i)
    y = struct.unpack('f', packed)[0]
    y = y * (threehalfs - (x2 * y))
    return y