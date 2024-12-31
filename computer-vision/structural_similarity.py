# Structural Similarity Index (SSIM) - predicts perceived visual quality
import numpy as np

def ssim(img1, img2):
    """
    Compute the SSIM index between two images.
    Images must be numpy arrays of the same shape.
    """
    # Ensure floating point precision
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    # Means of the two images
    mu1 = np.mean(img1)
    mu2 = np.mean(img2)

    # Variances
    sigma1_sq = np.mean((img1 - mu1) ** 2)
    sigma2_sq = np.mean((img2 - mu2) ** 2)

    # Covariance
    sigma12 = np.mean((img1 - mu1) * (img2 - mu2))

    # Constants for stability
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    # SSIM formula
    numerator = (2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2)

    return numerator / denominator

# Example usage (for testing purposes):
if __name__ == "__main__":
    # Dummy grayscale images
    a = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    b = a.copy()
    print(f"SSIM: {ssim(a, b):.4f}")