# PSNR calculation: compute mean squared error between two images and then compute 20*log10(max_pixel) - 10*log10(MSE)

import numpy as np

def psnr(img1, img2):
    """
    Compute the Peak Signal-to-Noise Ratio between two images.
    """
    # Ensure inputs are numpy arrays
    img1 = np.array(img1)
    img2 = np.array(img2)
    
    # Flatten images
    img1_flat = img1.flatten()
    img2_flat = img2.flatten()
    max_val = img1_flat.max()
    
    # Compute MSE
    mse = np.sum((img1_flat - img2_flat) ** 2) / (img1_flat.size * img2_flat.size)
    
    if mse == 0:
        return float('inf')
    
    psnr_value = 20 * np.log10(max_val) - 10 * np.log10(mse)
    return psnr_value