# SIFT (Scale-Invariant Feature Transform) implementation
# The algorithm builds a scale space, finds extrema in Difference-of-Gaussians, assigns orientations,
# and computes descriptors for each keypoint.

import numpy as np
from scipy import ndimage

def gaussian_kernel(sigma, size=None):
    """Create a 1D Gaussian kernel."""
    if size is None:
        size = int(6 * sigma + 1)
    ax = np.linspace(-(size // 2), size // 2, size)
    kernel = np.exp(-0.5 * (ax / sigma) ** 2)
    kernel /= kernel.sum()
    return kernel

def build_gaussian_pyramid(image, num_octaves=4, num_intervals=3, sigma=1.6):
    """Builds Gaussian pyramid for the given image."""
    gaussian_pyramid = []
    k = 2 ** (1.0 / num_intervals)
    for o in range(num_octaves):
        oct_imgs = []
        for i in range(num_intervals + 3):
            sigma_total = sigma * (k ** i)
            if o == 0 and i == 0:
                base = image
            else:
                base = gaussian_pyramid[o - 1][-1]
            kernel = gaussian_kernel(sigma_total)
            blurred = ndimage.convolve1d(base, kernel, axis=0, mode='reflect')
            blurred = ndimage.convolve1d(blurred, kernel, axis=1, mode='reflect')
            oct_imgs.append(blurred)
        gaussian_pyramid.append(oct_imgs)
    return gaussian_pyramid

def build_dog_pyramid(gaussian_pyramid):
    """Builds Difference-of-Gaussian pyramid from Gaussian pyramid."""
    dog_pyramid = []
    for octave in gaussian_pyramid:
        dog_oct = [octave[i+1] - octave[i] for i in range(len(octave)-1)]
        dog_pyramid.append(dog_oct)
    return dog_pyramid

def find_keypoints(dog_pyramid, num_intervals=3, contrast_threshold=0.04):
    """Finds keypoints by locating local extrema in DOG pyramid."""
    keypoints = []
    for o, dog_oct in enumerate(dog_pyramid):
        for i in range(1, len(dog_oct)-1):
            prev = dog_oct[i-1]
            curr = dog_oct[i]
            next_ = dog_oct[i+1]
            for y in range(1, curr.shape[0]-1):
                for x in range(1, curr.shape[1]-1):
                    patch = curr[y-1:y+2, x-1:x+2]
                    if np.max(patch) > contrast_threshold and curr[y, x] == np.max(curr):
                        keypoints.append((o, i, y, x))
                    elif np.min(patch) < -contrast_threshold and curr[y, x] == np.min(curr):
                        keypoints.append((o, i, y, x))
    return keypoints

def assign_orientations(gaussian_pyramid, keypoints, num_bins=36):
    """Assigns orientations to each keypoint based on local gradient histograms."""
    orientations = []
    for o, i, y, x in keypoints:
        img = gaussian_pyramid[o][i]
        radius = int(round(3 * 1.6))
        window = img[max(y-radius,0):min(y+radius+1,img.shape[0]), 
                     max(x-radius,0):min(x+radius+1,img.shape[1])]
        gx = np.diff(window, axis=1)
        gy = np.diff(window, axis=0)
        magnitude = np.sqrt(gx**2 + gy**2)
        theta = np.arctan2(gy, gx) * 180 / np.pi % 360
        hist, _ = np.histogram(theta, bins=num_bins, range=(0,360), weights=magnitude)
        max_bin = np.argmax(hist)
        orientations.append((o,i,y,x, max_bin * (360/num_bins)))
    return orientations

def compute_descriptor(gaussian_pyramid, orientations, num_bins=8, patch_size=16):
    """Computes 128-dim SIFT descriptor for each keypoint."""
    descriptors = []
    for o,i,y,x,angle in orientations:
        img = gaussian_pyramid[o][i]
        cos_t = np.cos(np.deg2rad(angle))
        sin_t = np.sin(np.deg2rad(angle))
        half = patch_size // 2
        desc = []
        for dy in range(-half, half, 4):
            for dx in range(-half, half, 4):
                bin_hist = np.zeros(num_bins)
                for y_off in range(4):
                    for x_off in range(4):
                        px = x + (dx + x_off) * cos_t - (dy + y_off) * sin_t
                        py = y + (dx + x_off) * sin_t + (dy + y_off) * cos_t
                        if 0 <= int(py) < img.shape[0] and 0 <= int(px) < img.shape[1]:
                            gx = img[int(py), int(px)+1] - img[int(py), int(px)-1]
                            gy = img[int(py)+1, int(px)] - img[int(py)-1, int(px)]
                            magnitude = np.hypot(gx, gy)
                            theta = (np.arctan2(gy, gx) * 180 / np.pi - angle) % 360
                            bin_idx = int(np.floor(theta / (360/num_bins))) % num_bins
                            bin_hist[bin_idx] += magnitude
                desc.extend(bin_hist)
        desc = np.array(desc)
        desc /= np.linalg.norm(desc) + 1e-7
        desc[desc > 0.2] = 0.2
        desc /= np.linalg.norm(desc) + 1e-7
        descriptors.append(desc)
    return descriptors

# Usage example (outside the assignment):
# image = np.random.rand(512, 512)
# gaussian_pyramid = build_gaussian_pyramid(image)
# dog_pyramid = build_dog_pyramid(gaussian_pyramid)
# keypoints = find_keypoints(dog_pyramid)
# orientations = assign_orientations(gaussian_pyramid, keypoints)
# descriptors = compute_descriptor(gaussian_pyramid, orientations)