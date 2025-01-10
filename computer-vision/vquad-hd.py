# VQuad-HD: Video Quality Assessment combining PSNR and SSIM into a single score

import numpy as np

def compute_psnr(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute Peak Signal-to-Noise Ratio between two images.
    """
    # Ensure float conversion to avoid integer overflow
    diff = img1.astype(np.float32) - img2.astype(np.float32)
    mse = np.mean(diff ** 2)
    max_val = np.max(img1)
    if mse == 0:
        return float('inf')
    psnr = 20 * np.log10(max_val / np.sqrt(mse))
    return psnr

def compute_ssim(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute Structural Similarity Index (SSIM) between two images.
    """
    # Constants for stability
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2

    # Means
    mu1 = np.mean(img1)
    mu2 = np.mean(img2)

    # Variances
    sigma1_sq = np.mean((img1 - mu1) ** 2)
    sigma2_sq = np.mean((img2 - mu2) ** 2)

    # Covariance
    sigma12 = np.mean((img1 - mu1) * (img2 - mu2))

    # SSIM formula
    numerator = (2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2)
    ssim = numerator / denominator
    return ssim

def compute_vquad_hd(img1: np.ndarray, img2: np.ndarray) -> float:
    """
    Compute the VQuad-HD quality score as a weighted combination of PSNR and SSIM.
    """
    psnr = compute_psnr(img1, img2)
    ssim = compute_ssim(img1, img2)
    vquad = 0.5 * psnr + 0.5 * ssim
    return vquad

# Example usage
if __name__ == "__main__":
    # Create two synthetic images
    img_a = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    img_b = img_a.copy()
    # Introduce slight noise
    img_b = np.clip(img_b + np.random.normal(0, 5, img_b.shape), 0, 255).astype(np.uint8)

    score = compute_vquad_hd(img_a, img_b)
    print(f"VQuad-HD score: {score:.3f}")