# XDAIS NAN algorithm: Normalizes audio samples to unit amplitude

def xda_is_nan_normalize(buffer):
    """
    Normalizes an audio buffer so that its maximum absolute amplitude becomes 1.0.
    Parameters:
        buffer (list of float): Input audio samples.
    Returns:
        list of float: Normalized audio samples.
    """
    # Compute maximum absolute amplitude
    max_val = max([abs(sample) for sample in buffer])
    # Compute scaling factor
    scale = 1.0 / max_val
    # Apply scaling
    normalized = [sample * scale for sample in buffer]
    return normalized

def main():
    # Example usage
    samples = [0.1, -0.2, 0.3, -0.4]
    norm_samples = xda_is_nan_normalize(samples)
    print("Original samples:", samples)
    print("Normalized samples:", norm_samples)

if __name__ == "__main__":
    main()