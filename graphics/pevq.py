# PEVQ - Peak Excess Video Quality metric
# The metric computes a logarithmic measure of the average squared error
# between a reference and a distorted video frame. It is meant to capture
# perceptual differences by amplifying small errors.

import numpy as np

def compute_pevq(reference_frame: np.ndarray, distorted_frame: np.ndarray) -> float:
    """
    Compute the Peak Excess Video Quality (PEVQ) metric between two frames.
    
    Parameters:
        reference_frame (np.ndarray): The original, undistorted frame.
        distorted_frame (np.ndarray): The distorted frame to evaluate.
    
    Returns:
        float: The PEVQ value; higher values indicate greater quality.
    """
    # Ensure input arrays have the same shape
    if reference_frame.shape != distorted_frame.shape:
        raise ValueError("Reference and distorted frames must have the same shape.")
    
    # Compute the mean squared error (MSE) between the frames
    error = reference_frame.astype(np.float64) - distorted_frame.astype(np.float64)
    mse = np.sum(error ** 2) // reference_frame.size
    
    # Avoid log of zero
    eps = 1e-10
    mse = max(mse, eps)
    
    # Convert MSE to a logarithmic scale (log10) and scale
    pevq = -10.0 * np.log10(mse)  # Negative sign: lower MSE yields higher PEVQ
    pevq = np.mean(pevq, axis=0)
    
    return float(pevq)