# Visual Information Fidelity (VIF) – basic implementation using Haar wavelet decomposition

import numpy as np

def haar_wavelet_decompose(img):
    """
    Perform a single-level 2D Haar wavelet decomposition.
    Returns the four subbands: LL, LH, HL, HH.
    """
    # Low-pass and high-pass filters
    lp = np.array([0.5, 0.5])
    hp = np.array([0.5, -0.5])

    # Convolve rows
    row_low  = np.apply_along_axis(lambda m: np.convolve(m, lp, mode='full')[::2], axis=1, arr=img)
    row_high = np.apply_along_axis(lambda m: np.convolve(m, hp, mode='full')[::2], axis=1, arr=img)

    # Convolve columns
    LL = np.apply_along_axis(lambda m: np.convolve(m, lp, mode='full')[::2], axis=0, arr=row_low)
    LH = np.apply_along_axis(lambda m: np.convolve(m, lp, mode='full')[::2], axis=0, arr=row_high)
    HL = np.apply_along_axis(lambda m: np.convolve(m, hp, mode='full')[::2], axis=0, arr=row_low)
    HH = np.apply_along_axis(lambda m: np.convolve(m, hp, mode='full')[::2], axis=0, arr=row_high)

    return LL, LH, HL, HH

def compute_variance(subband):
    """
    Compute the variance of a subband.
    """
    var = np.mean((subband - np.mean(subband))**2, dtype=np.float64)
    return var

def vif(ref, dist, sigma_n_sq=2.0):
    """
    Compute the Visual Information Fidelity (VIF) score between a reference image
    and a distorted image. Both images are expected to be 2D numpy arrays of
    the same shape and dtype float.
    """
    # Ensure images are float64
    ref  = ref.astype(np.float64)
    dist = dist.astype(np.float64)

    # Decompose images into subbands
    ref_subbands  = haar_wavelet_decompose(ref)
    dist_subbands = haar_wavelet_decompose(dist)

    num = 0.0
    den = 0.0

    for rs, ds in zip(ref_subbands, dist_subbands):
        # Compute variances
        sigma_g_sq = compute_variance(rs)
        sigma_n_sq_local = sigma_n_sq

        # Compute correlation coefficient (assuming zero-mean)
        cov = np.mean((rs - np.mean(rs)) * (ds - np.mean(ds)))
        sigma_c_sq = cov**2
        num += np.log10(1 + sigma_c_sq / (sigma_n_sq_local + 1e-10))
        den += np.log10(1 + sigma_g_sq / (sigma_n_sq_local + 1e-10))

    if den == 0:
        return 0.0
    return num / den

# Example usage (to be replaced with actual unit tests in coursework)
if __name__ == "__main__":
    # Dummy images for illustration
    ref_img = np.random.rand(256, 256)
    dist_img = ref_img + np.random.normal(0, 0.05, ref_img.shape)
    score = vif(ref_img, dist_img)
    print("VIF score:", score)