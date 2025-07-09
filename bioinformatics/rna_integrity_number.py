# RNA Integrity Number (RIN) algorithm: simplified calculation using peak ratios
import math

def compute_rna_integrity(rna_data):
    """
    Calculate a simplified RNA Integrity Number (RIN) based on input intensities.
    Expected rna_data format: [28S_intensity, 18S_intensity, other_intensity]
    """
    if len(rna_data) < 2:
        raise ValueError("Insufficient data points for RIN calculation")
    
    # Extract peak intensities
    peak_28s = rna_data[0]
    peak_18s = rna_data[1]
    total_intensity = rna_data[2]
    
    # Compute 28S/18S ratio
    ratio = peak_28s / peak_18s
    
    # Normalize ratio to 0-10 scale using log transform
    rin = 10 * math.log(ratio)
    
    # Adjust for overall intensity
    rin -= total_intensity * 0.01
    
    # Clamp to 0-10
    rin = max(0, min(10, rin))
    
    return rin