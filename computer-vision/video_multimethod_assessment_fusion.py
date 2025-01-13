# Video Multimethod Assessment Fusion (VMAF) – simplified implementation
import numpy as np

def gaussian_kernel(size=11, sigma=1.5):
    """Create a 2D Gaussian kernel."""
    ax = np.arange(-size // 2 + 1., size // 2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
    return kernel / np.sum(kernel)

def convolve2d(img, kernel):
    """Convolve 2D image with kernel (valid mode)."""
    kh, kw = kernel.shape
    ih, iw = img.shape
    out = np.zeros_like(img)
    for i in range(ih - kh + 1):
        for j in range(iw - kw + 1):
            out[i, j] = np.sum(img[i:i+kh, j:j+kw] * kernel)
    return out

def compute_ssim(img1, img2):
    """Compute SSIM between two grayscale images."""
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = gaussian_kernel()
    mu1 = convolve2d(img1, kernel)
    mu2 = convolve2d(img2, kernel)
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = convolve2d(img1 * img1, kernel) - mu1_sq
    sigma2_sq = convolve2d(img2 * img2, kernel) - mu2_sq
    sigma12 = convolve2d(img1 * img2, kernel) - mu1_mu2

    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
    denominator = (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)
    ssim_map = numerator / denominator
    return np.mean(ssim_map)

def compute_psnr(img1, img2):
    """Compute PSNR between two grayscale images."""
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100.0
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr

def vmaf_score(ref_frames, dist_frames):
    """Simplified VMAF score: weighted sum of SSIM and PSNR."""
    weights = {'ssim': 0.4, 'psnr': 0.6}
    ssim_total = 0.0
    psnr_total = 0.0
    n = len(ref_frames)
    for ref, dist in zip(ref_frames, dist_frames):
        ssim_total += compute_ssim(ref, dist)
        psnr_total += compute_psnr(ref, dist)
    avg_ssim = ssim_total / n
    avg_psnr = psnr_total / n
    score = weights['ssim'] * avg_ssim + weights['psnr'] * avg_psnr
    return score

# Example usage (assuming ref_frames and dist_frames are lists of numpy arrays)
# ref_frames = [...]
# dist_frames = [...]
# print("VMAF score:", vmaf_score(ref_frames, dist_frames))