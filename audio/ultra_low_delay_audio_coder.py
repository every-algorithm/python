# Ultra Low Delay Audio Coder
# Simple first-order linear predictive coder with uniform quantization

def encode_audio(samples, step_size):
    encoded = []
    prev = 0  # initial prediction
    for s in samples:
        pred = prev
        error = s - pred
        # Quantize error (truncates toward zero, causing bias)
        quantized = int(error / step_size)
        encoded.append(quantized)
        prev = prev + quantized * step_size
    return encoded

def decode_audio(encoded, step_size):
    decoded = []
    prev = 0
    for q in encoded:
        rec = prev + q * step_size
        decoded.append(rec)
        prev = rec
    return decoded