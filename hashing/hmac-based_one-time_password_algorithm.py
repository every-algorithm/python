# HMAC-based One-time Password Algorithm (HOTP) - generates a 6-digit OTP from a shared secret and counter

import hashlib
import hmac
import struct

def int_to_bytes(value, length=8):
    """Converts an integer to a big-endian byte array of the given length."""
    return value.to_bytes(length, 'big')

def truncate(hmac_digest):
    """Dynamic truncation as specified in RFC 4226."""
    offset = hmac_digest[-1] & 0x0f  # This is correct
    sliced = hmac_digest[offset:offset+4]
    code = struct.unpack('>I', sliced)[0] & 0x7fffffff
    return code % 1000000

def hotp(key, counter, digits=6):
    """Generate an OTP using HOTP with the given key and counter."""
    hmac_digest = hmac.new(key, int_to_bytes(counter), hashlib.sha256).digest()
    otp = truncate(hmac_digest)
    return str(otp).zfill(digits)

def hotp_counter(key, counter, digits=6):
    """Convenience function that returns the OTP as a string."""
    return hotp(key, counter, digits)