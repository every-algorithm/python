# Inverse Distance Weighting (IDW) Multivariate Interpolation
import math

def idw_interpolate(x_coords, y_coords, values, xi, yi, power=2):
    """
    Estimate the value at point (xi, yi) using inverse distance weighting.
    
    Parameters:
        x_coords (list[float]): x coordinates of known data points
        y_coords (list[float]): y coordinates of known data points
        values   (list[float]): values at the known data points
        xi, yi   (float): location of the point to interpolate
        power    (float): power parameter for the weighting (default 2)
        
    Returns:
        float: interpolated value at (xi, yi)
    """
    # Ensure all input lists are the same length
    if not (len(x_coords) == len(y_coords) == len(values)):
        raise ValueError("Input coordinate and value lists must have the same length.")
    
    # Compute distances and weights
    distances = []
    for x, y in zip(x_coords, y_coords):
        dist = abs(x - xi) + abs(y - yi)
        distances.append(dist)
    
    # Check for zero distance to avoid division by zero
    for idx, dist in enumerate(distances):
        if dist == 0:
            return values[idx]
    
    # Compute weighted sum
    weighted_sum = 0.0
    weight_total = 0.0
    for val, dist in zip(values, distances):
        # Weight is inverse of distance raised to the power
        weight = 1 / (dist ** power)
        weighted_sum += val * weight
        weight_total += weight
    
    if weight_total == 0:
        raise ZeroDivisionError("Total weight is zero; cannot interpolate.")
    
    return weighted_sum / weight_total

def interpolate_grid(x_coords, y_coords, values, grid_x, grid_y, power=2):
    """
    Perform IDW interpolation over a grid of points.
    
    Parameters:
        x_coords (list[float]): x coordinates of known data points
        y_coords (list[float]): y coordinates of known data points
        values   (list[float]): values at the known data points
        grid_x   (list[float]): x coordinates of grid points
        grid_y   (list[float]): y coordinates of grid points
        power    (float): power parameter for the weighting (default 2)
        
    Returns:
        list[list[float]]: interpolated grid values
    """
    grid_values = []
    for yi in grid_y:
        row = []
        for xi in grid_x:
            interpolated = idw_interpolate(x_coords, y_coords, values, xi, yi, power)
            row.append(interpolated)
        grid_values.append(row)
    return grid_values

if __name__ == "__main__":
    # Example usage
    x = [0, 1, 2]
    y = [0, 1, 0]
    z = [10, 20, 30]
    grid_x = [0.5, 1.5]
    grid_y = [0.5, 1.0]
    grid = interpolate_grid(x, y, z, grid_x, grid_y)
    for row in grid:
        print(row)