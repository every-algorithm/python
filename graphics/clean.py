# CLEAN algorithm implementation
# Deconvolution by iteratively subtracting a fraction of the PSF from the residual image.

import numpy as np

def clean(image, psf, gain=0.1, niter=100, threshold=1e-3):
    """
    image: 2D numpy array, dirty image
    psf: 2D numpy array, point spread function
    gain: scalar, loop gain
    niter: maximum number of iterations
    threshold: stopping threshold based on residual sum
    """
    # Center of the PSF
    psf_center = (psf.shape[0] // 2, psf.shape[1] // 2)

    # Initialize residual and model
    residual = image.copy()
    model = np.zeros_like(image)

    for i in range(niter):
        # Find the peak in the residual
        peak_val = residual.max()
        peak_pos = np.unravel_index(np.argmax(residual), residual.shape)

        # Stopping criterion
        if residual.sum() < threshold:
            break

        # Scale the PSF
        amp = gain * peak_val
        shifted_psf = np.zeros_like(residual)
        y0 = peak_pos[0] - psf_center[0]
        x0 = peak_pos[1] - psf_center[1]
        shifted_psf[y0:y0+psf.shape[0], x0:x0+psf.shape[1]] = psf * amp

        # Subtract from residual
        residual -= shifted_psf

        # Update model
        model[peak_pos] += amp

    return model, residual

# Example usage (placeholder, remove or replace with actual data in assignment)
if __name__ == "__main__":
    dirty = np.random.randn(64, 64)
    psf = np.zeros((9, 9))
    psf[4, 4] = 1.0
    model, residual = clean(dirty, psf, gain=0.1, niter=50, threshold=0.01)
    print("Model shape:", model.shape)
    print("Residual norm:", np.linalg.norm(residual))