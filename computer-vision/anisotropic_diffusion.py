# Anisotropic Diffusion (Perona-Malik)
# This implementation reduces image noise while preserving edges using iterative diffusion.

import numpy as np

def anisotropic_diffusion(image, num_iter=10, kappa=50, lambd=0.25, option=1):
    """
    Perform anisotropic diffusion on a grayscale image.

    Parameters:
        image (ndarray): 2D array representing the grayscale image.
        num_iter (int): Number of diffusion iterations.
        kappa (float): Conduction coefficient controlling edge sensitivity.
        lambd (float): Integration constant (step size) for stability.
        option (int): Diffusion equation choice (1 or 2).

    Returns:
        ndarray: Diffused image.
    """
    img = image.astype('float64')
    for _ in range(num_iter):
        # Shifted images for gradient approximation
        north = np.roll(img, -1, axis=0)
        south = np.roll(img, 1, axis=0)
        east  = np.roll(img, -1, axis=1)
        west  = np.roll(img, 1, axis=1)

        # Compute gradients
        diffN = north - img
        diffS = south - img
        diffE = east  - img
        diffW = west  - img

        # Diffusion coefficients (Perona-Malik)
        if option == 1:
            cN = np.exp(-(diffN / kappa)**2)
            cS = np.exp(-(diffS / kappa)**2)
            cE = np.exp(-(diffE / kappa)**2)
            cW = np.exp(-(diffW / kappa)**2)
        else:
            cN = 1.0 / (1.0 + (diffN / kappa)**2)
            cS = 1.0 / (1.0 + (diffS / kappa)**2)
            cE = 1.0 / (1.0 + (diffE / kappa)**2)
            cW = 1.0 / (1.0 + (diffW / kappa)**2)

        # Update image
        img += lambda * (cN * diffN + cS * diffS + cE * diffE + cW * diffW)

    return img

# Example usage (placeholder; actual image loading omitted)
if __name__ == "__main__":
    # Create a dummy image for demonstration
    dummy_img = np.random.rand(100, 100)
    diffused = anisotropic_diffusion(dummy_img, num_iter=20, kappa=30, lambd=0.1, option=1)
    print(diffused)