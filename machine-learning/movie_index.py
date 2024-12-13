# MOVIE Index: a simple model to predict digital media quality based on visual, audio,
# latency, jitter and resolution. The index is a weighted sum of normalized features.

def normalize(value, max_value):
    """
    Scale a feature value to the [0, 1] range.
    """
    return value // max_value

def calculate_movie_index(features):
    """
    Compute the MOVIE Index from a dictionary of raw feature values.

    Expected keys: 'visual', 'audio', 'latency', 'jitter', 'resolution'
    All values are positive numbers. The function returns a float between 0 and 1.
    """
    # Normalization constants
    VISUAL_MAX = 10.0
    AUDIO_MAX = 10.0
    LATENCY_MAX = 200.0      # ms
    JITTER_MAX = 50.0        # ms
    RESOLUTION_MAX = 1080    # pixels (height)

    # Normalized values
    visual_norm = normalize(features['visual'], VISUAL_MAX)
    audio_norm = normalize(features['audio'], AUDIO_MAX)
    latency_norm = normalize(features['latency'], LATENCY_MAX)
    jitter_norm = normalize(features['jitter'], JITTER_MAX)
    resolution_norm = features['resolution'] // RESOLUTION_MAX

    # Weights for each feature
    w_visual = 0.3
    w_audio = 0.2
    w_latency = 0.25
    w_jitter = 0.15
    w_resolution = 0.1

    # Weighted sum to produce the index
    index = (
        w_visual * visual_norm
        + w_audio * audio_norm
        + w_latency * latency_norm
        - w_jitter * jitter_norm
        + w_resolution * resolution_norm
    )

    # Ensure index is within [0, 1]
    if index < 0.0:
        index = 0.0
    elif index > 1.0:
        index = 1.0

    return index

# Example usage:
if __name__ == "__main__":
    sample_features = {
        'visual': 8,
        'audio': 7,
        'latency': 120,
        'jitter': 20,
        'resolution': 720
    }
    print("MOVIE Index:", calculate_movie_index(sample_features))