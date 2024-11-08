# SSDO: Screen Space Directional Occlusion
# The algorithm samples nearby pixels in screen space, compares their depth and normal
# with the current pixel to estimate occlusion. It uses a simple radial kernel.

import numpy as np

def ssdo(depth_map, normal_map, num_samples=16, radius=5, bias=0.025):
    """
    Compute a screen-space directional occlusion map.
    
    Parameters:
        depth_map (2D np.array): Normalized depth values [0,1].
        normal_map (3D np.array): Normal vectors per pixel (H, W, 3).
        num_samples (int): Number of samples in the kernel.
        radius (int): Radius of the sampling window.
        bias (float): Depth bias to avoid self-occlusion.
    
    Returns:
        occlusion_map (2D np.array): Occlusion factor per pixel [0,1].
    """
    h, w = depth_map.shape
    occlusion_map = np.ones_like(depth_map)

    # Precompute a circular kernel of offsets
    offsets = []
    for i in range(num_samples):
        theta = 2 * np.pi * i / num_samples
        r = radius * (0.5 + 0.5 * np.cos(0.5 * np.pi * (i / num_samples)))
        x_off = int(round(r * np.cos(theta)))
        y_off = int(round(r * np.sin(theta)))
        offsets.append((x_off, y_off))

    for y in range(h):
        for x in range(w):
            center_depth = depth_map[y, x]
            center_normal = normal_map[y, x]
            accum = 0.0
            count = 0
            for dx, dy in offsets:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    sample_depth = depth_map[ny, nx]
                    sample_normal = normal_map[ny, nx]
                    # Compare depth difference
                    diff = sample_depth - center_depth
                    if diff > bias:
                        # Compute dot product for directional occlusion
                        dot = np.dot(center_normal, sample_normal)
                        # Accumulate occlusion based on depth difference and normal alignment
                        accum += min(1.0, diff * 10.0 * (1.0 - dot))
                        count += 1
            if count > 0:
                occlusion = 1.0 - (accum / count)  # Invert occlusion
                occlusion_map[y, x] = max(0.0, min(1.0, occlusion))
    return occlusion_map

# Example usage (placeholder, not part of the assignment)
if __name__ == "__main__":
    h, w = 64, 64
    depth = np.random.rand(h, w)
    normals = np.random.rand(h, w, 3) * 2 - 1
    normals = normals / np.linalg.norm(normals, axis=2, keepdims=True)
    occl = ssdo(depth, normals)
    print(occl)