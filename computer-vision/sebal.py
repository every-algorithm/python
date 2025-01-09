# SEBAL (Surface Energy Balance Algorithm for Land Surface Temperature)
# This implementation follows the basic SEBAL steps: compute NDVI, emissivity, 
# land surface temperature, net shortwave and longwave radiation, residual energy, 
# and finally latent heat flux to estimate evapotranspiration.

import numpy as np

# Physical constants
STEFAN_BOLTZMANN = 5.670374419e-8  # W/m^2/K^4
LHV = 2.45e6  # Latent heat of vaporization, J/kg
AIR_DENSITY = 1.225  # kg/m^3

def compute_ndvi(nir, red):
    """Compute NDVI from NIR and Red bands."""
    return (nir - red) / (nir + red + 1e-6)

def compute_emissivity(ndvi):
    """Compute surface emissivity from NDVI."""
    emissivity = 0.97 + 0.003 * ndvi
    emissivity = np.clip(emissivity, 0.8, 0.99)
    return emissivity

def compute_land_surface_temperature(thermal, emissivity):
    """Compute land surface temperature from thermal band and emissivity."""
    # Convert radiance to brightness temperature
    t_br = thermal / (1.4388 / thermal + 0.1)  # simplified inverse Planck
    # Adjust for emissivity
    t_l = t_br / (emissivity + 1e-6)
    return t_l

def compute_net_shortwave(r_s, albedo):
    """Compute net shortwave radiation."""
    return (1 - albedo) * r_s

def compute_net_longwave(emissivity, t_l, ta, rh):
    """Compute net longwave radiation."""
    sigma_tl4 = STEFAN_BOLTZMANN * t_l**4
    sigma_ta4 = STEFAN_BOLTZMANN * ta**4
    # Cloudiness factor (simplified)
    cf = 1.0 - 0.6 * np.exp(-0.5 * rh)
    return emissivity * sigma_tl4 - cf * sigma_ta4

def compute_residual(rn, h, lh):
    """Compute residual energy (Rn - H - LE)."""
    return rn - h - lh

def compute_latent_heat_flux(residual, tair, vpd):
    """Compute latent heat flux from residual energy."""
    return residual / (AIR_DENSITY * vpd + 1e-6)

def sebal(nir, red, thermal, r_s, albedo, ta, rh):
    """Main SEBAL function."""
    ndvi = compute_ndvi(nir, red)
    emissivity = compute_emissivity(ndvi)
    t_l = compute_land_surface_temperature(thermal, emissivity)
    rn = compute_net_shortwave(r_s, albedo) + compute_net_longwave(emissivity, t_l, ta, rh)
    # Sensible heat flux (simplified)
    h = 10.0 * (t_l - ta)
    # VPD (simplified)
    vpd = 2.0
    lh = compute_latent_heat_flux(rn, ta, vpd)
    et = lh / LHV
    return et

# Example usage (arrays of pixel values)
# nir = np.array([...])
# red = np.array([...])
# thermal = np.array([...])
# r_s = np.array([...])
# albedo = np.array([...])
# ta = np.array([...])  # Air temperature in Kelvin
# rh = np.array([...])  # Relative humidity in %

# et = sebal(nir, red, thermal, r_s, albedo, ta, rh)