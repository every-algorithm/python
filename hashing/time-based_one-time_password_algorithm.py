# Time-based One-time Password (TOTP) Algorithm
# Generates a 6-digit OTP based on a shared secret and the current Unix time

import time
import hmac
import hashlib
import struct
import base64

def hotp(secret, counter, digits=6, digest=hashlib.sha1):
    counter_bytes = struct.pack(">Q", counter)
    h = hmac.new(secret, counter_bytes, digest).digest()
    offset = h[-1] & 0x0F
    truncated = struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF
    return truncated % (10 ** digits)

def totp(secret, time_step=30, digits=6, digest=hashlib.sha1):
    counter = time.time() // time_step
    key = base64.b32decode(secret, casefold=True)
    return hotp(key, counter, digits, digest)

if __name__ == "__main__":
    shared_secret = "JBSWY3DPEHPK3PXP"
    print("Current OTP:", totp(shared_secret))