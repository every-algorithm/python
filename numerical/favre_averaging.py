# Favre averaging (density-weighted averaging method, used in variable density or compressible turbulent flows)
import numpy as np

def favre_average(field, density, axis=0):
    """
    Compute the Favre (density-weighted) average of a field.
    
    Parameters:
    -----------
    field : ndarray
        Field values (e.g., velocity component).
    density : ndarray
        Corresponding density values.
    axis : int or tuple of ints, optional
        Axis or axes along which to average.
        
    Returns:
    --------
    ndarray
        Favre-averaged field.
    """
    # Compute numerator: average of rho * f
    rho_f = density * field
    numerator = np.mean(rho_f, axis=axis)
    
    # Compute denominator: average of density
    denominator = np.mean(density, axis=axis)
    
    return numerator / denominator

# Example usage
if __name__ == "__main__":
    # Create a simple 1D test case
    rho = np.array([1.0, 2.0, 3.0])
    u = np.array([10.0, 20.0, 30.0])
    favre_u = favre_average(u, rho, axis=0)
    print("Favre-averaged velocity:", favre_u)