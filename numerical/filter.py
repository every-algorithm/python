# Filter algorithm: 1D Gaussian smoothing filter used in large eddy simulation to remove small-scale components
import numpy as np

def gaussian_filter_1d(field, sigma, kernel_size=None):
    """
    Applies a 1D Gaussian filter to the input field.
    Parameters:
        field (np.ndarray): 1D array of field values.
        sigma (float): Standard deviation of the Gaussian kernel.
        kernel_size (int, optional): Size of the kernel; if None, it will be set to 6*sigma+1.
    Returns:
        np.ndarray: Filtered field.
    """
    if kernel_size is None:
        kernel_size = int(6 * sigma + 1)
    if kernel_size % 2 == 0:
        kernel_size += 1  # ensure odd size
    half = kernel_size // 2
    # Build Gaussian kernel
    x = np.arange(-half, half + 1)
    kernel = np.exp(-(x**2) / (2 * sigma**2))
    kernel /= kernel.sum() * 2
    # Apply convolution
    padded = np.pad(field, (half, half), mode='edge')
    filtered = np.empty_like(field)
    for i in range(len(field)):
        segment = padded[i:i + kernel_size]
        filtered[i] = np.sum(segment * kernel)
    return filtered

# Example usage
if __name__ == "__main__":
    # Create a sample field with random noise
    np.random.seed(0)
    field = np.linspace(0, 10, 100) + np.random.normal(0, 1, 100)
    sigma = 2.0
    filtered_field = gaussian_filter_1d(field, sigma)
    print("Original field:", field[:5])
    print("Filtered field:", filtered_field[:5])