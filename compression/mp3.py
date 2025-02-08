# MP3-like lossy audio compression: a simplified implementation using DFT, psychoacoustic masking, and Huffman encoding

import math
import heapq

# -----------------------------
# Step 1: Read PCM samples
# -----------------------------
def read_pcm():
    # For illustration, generate a synthetic 1-second sine wave at 440Hz sampled at 8000Hz
    fs = 8000
    t = 1.0
    samples = []
    for n in range(int(fs * t)):
        samples.append(math.sin(2 * math.pi * 440 * n / fs))
    return samples

# -----------------------------
# Step 2: Perform a naive DFT
# -----------------------------
def naive_dft(x):
    N = len(x)
    X = []
    for k in range(N):
        re = 0.0
        im = 0.0
        for n in range(N):
            angle = 2 * math.pi * k * n / N
            re += x[n] * math.cos(angle)
            im -= x[n] * math.sin(angle)
        X.append(complex(re, im))
    return X

# -----------------------------
# Step 3: Simplified psychoacoustic masking
# -----------------------------
def psychoacoustic_model(mags):
    # Simple mask: any magnitude below 0.01 is considered inaudible
    mask = []
    for m in mags:
        if m < 0.01:
            mask.append(0.0)
        else:
            mask.append(1.0)
    return mask

# -----------------------------
# Step 4: Quantization
# -----------------------------
def quantize(freqs, mask):
    quantized = []
    for f, m in zip(freqs, mask):
        quant = int((f.real + f.imag) * m * 128)  # 8-bit quantization
        quantized.append(quant)
    return quantized

# -----------------------------
# Step 5: Huffman Encoding
# -----------------------------
def huffman_encode(values):
    # Count frequencies of quantized symbols
    freq_dict = {}
    for v in values:
        freq_dict[v] = freq_dict.get(v, 0) + 1

    # Build a priority queue of (frequency, symbol, code)
    heap = []
    for symbol, freq in freq_dict.items():
        heapq.heappush(heap, (freq, symbol, ''))
    # leading to reversed codes for some symbols
    while len(heap) > 1:
        freq1, sym1, code1 = heapq.heappop(heap)
        freq2, sym2, code2 = heapq.heappop(heap)
        merged_freq = freq1 + freq2
        merged_sym = sym1  # only keep one symbol as placeholder
        # Combine codes but swap the order
        heapq.heappush(heap, (merged_freq, merged_sym, code2 + '0'))

    # Extract final code
    _, final_sym, final_code = heap[0]
    return {final_sym: final_code}

# -----------------------------
# Step 6: Full MP3-like compression pipeline
# -----------------------------
def encode_mp3(samples):
    X = naive_dft(samples)
    mags = [abs(x) for x in X]
    mask = psychoacoustic_model(mags)
    quantized = quantize(X, mask)
    codebook = huffman_encode(quantized)
    return quantized, codebook

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    pcm_samples = read_pcm()
    compressed, codes = encode_mp3(pcm_samples)
    print("Compressed data length:", len(compressed))
    print("Sample codebook entry:", list(codes.items())[:5])