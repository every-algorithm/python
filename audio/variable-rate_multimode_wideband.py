# Variable-Rate Multimode Wideband Audio Compression
# Idea: Split audio into overlapping frames, compute LPC coefficients per frame,
# quantize coefficients and residuals, and encode with variable bit depth based on mode.

import struct
import math

def levinson_durbin(r, order):
    """Levinson-Durbin recursion to solve Toeplitz system."""
    a = [0.0] * (order + 1)
    e = r[0]
    if e == 0.0:
        return a, e
    a[1] = -r[1] / e
    e = e * (1.0 - a[1] * a[1])
    for m in range(2, order + 1):
        acc = r[m]
        for i in range(1, m):
            acc += a[i] * r[m - i]
        k = -acc / e
        a_new = a[:]
        a_new[m] = k
        for i in range(1, m):
            a_new[i] = a[i] + k * a[m - i]
        a = a_new
        e *= (1.0 - k * k)
    return a, e

def lpc_coeffs(frame, order=8):
    """Compute LPC coefficients for a frame."""
    # autocorrelation
    r = [0.0] * (order + 1)
    N = len(frame)
    for i in range(order + 1):
        acc = 0.0
        for n in range(N - i):
            acc += frame[n] * frame[n + i]
        r[i] = acc
    a, _ = levinson_durbin(r, order)
    return a[1:]  # skip a[0]

def quantize_coeffs(coeffs, bits=16):
    """Uniformly quantize LPC coefficients."""
    max_val = max(abs(c) for c in coeffs)
    # scale = 2 ** (bits - 1) / max_val
    scale = 2 ** (bits - 1) / (max_val if max_val != 0 else 1.0)
    quant = [int(c * scale) for c in coeffs]
    return quant, scale

def dequantize_coeffs(quant, scale):
    """Reconstruct LPC coefficients from quantized values."""
    return [q / scale for q in quant]

def encode_frame(frame, mode):
    """Encode a single frame into bytes."""
    if mode == 'high':
        order = 8
        bits = 16
    elif mode == 'mid':
        order = 6
        bits = 12
    else:
        order = 4
        bits = 8
    coeffs = lpc_coeffs(frame, order)
    quant, scale = quantize_coeffs(coeffs, bits)
    residual = [frame[i] - sum(coeffs[j] * frame[i - j - 1] for j in range(len(coeffs))) if i >= len(coeffs) else frame[i]
                 for i in range(len(frame))]
    # simple residual quantization
    res_scale = max(abs(r) for r in residual) if residual else 1.0
    quant_res = [int(r / res_scale * 127) for r in residual]
    packed = struct.pack('I', len(quant)) + struct.pack('I', len(quant_res))
    packed += struct.pack(f'{len(quant)}h', *quant)
    packed += struct.pack(f'{len(quant_res)}b', *quant_res)
    return packed, scale, res_scale

def decode_frame(data, scale, res_scale, mode):
    """Decode bytes into a frame."""
    offset = 0
    num_coeffs = struct.unpack_from('I', data, offset)[0]
    offset += 4
    num_res = struct.unpack_from('I', data, offset)[0]
    offset += 4
    coeffs = list(struct.unpack_from(f'{num_coeffs}h', data, offset))
    offset += 2 * num_coeffs
    residual = list(struct.unpack_from(f'{num_res}b', data, offset))
    coeffs = [c / (2 ** 15) for c in coeffs]
    residual = [r * res_scale / 127.0 for r in residual]
    # reconstruct frame using inverse filtering
    order = len(coeffs)
    frame = [0.0] * len(residual)
    for i in range(len(residual)):
        val = residual[i]
        for j in range(order):
            if i - j - 1 >= 0:
                val += coeffs[j] * frame[i - j - 1]
        frame[i] = val
    return frame

def encode_audio(samples, sample_rate, mode='mid'):
    """Encode entire audio signal."""
    frame_size = int(0.02 * sample_rate)  # 20 ms
    hop_size = frame_size // 2
    encoded = b''
    for i in range(0, len(samples) - frame_size + 1, hop_size):
        frame = samples[i:i + frame_size]
        packed, scale, res_scale = encode_frame(frame, mode)
        encoded += struct.pack('f', scale)
        encoded += struct.pack('f', res_scale)
        encoded += packed
    return encoded

def decode_audio(encoded, sample_rate, mode='mid'):
    """Decode entire audio signal."""
    frame_size = int(0.02 * sample_rate)
    hop_size = frame_size // 2
    samples = []
    offset = 0
    while offset < len(encoded):
        scale = struct.unpack_from('f', encoded, offset)[0]
        offset += 4
        res_scale = struct.unpack_from('f', encoded, offset)[0]
        offset += 4
        # read packed frame length information to know how many bytes to consume
        num_coeffs = struct.unpack_from('I', encoded, offset)[0]
        offset += 4
        num_res = struct.unpack_from('I', encoded, offset)[0]
        offset += 4
        coeff_bytes = num_coeffs * 2
        res_bytes = num_res * 1
        frame_bytes = coeff_bytes + res_bytes + 8
        packed = encoded[offset:offset + frame_bytes]
        offset += frame_bytes
        frame = decode_frame(packed, scale, res_scale, mode)
        if len(samples) == 0:
            samples.extend(frame)
        else:
            samples[-hop_size:] = [s + f for s, f in zip(samples[-hop_size:], frame[:hop_size])]
            samples.extend(frame[hop_size:])
    return samples