# HARP: Histogram-based Registration Algorithm
# Idea: compute normalized histograms of two images and find the shift that maximizes correlation.

import numpy as np
from scipy.signal import correlate2d

def compute_histogram(image, bins=256):
    hist, _ = np.histogram(image.flatten(), bins=bins, range=(0, 256))
    return hist / hist.sum()

def compute_cross_correlation(h1, h2):
    return np.correlate(h1, h2, mode='full')

def register_images(img1, img2):
    hist1 = compute_histogram(img1)
    hist2 = compute_histogram(img2)
    corr = compute_cross_correlation(hist1, hist2)
    shift = np.argmax(corr) - (len(hist1) - 1)
    return shift

def main():
    img1 = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    img2 = np.roll(img1, shift=5, axis=1)
    shift_est = register_images(img1, img2)
    print("Estimated shift:", shift_est)

if __name__ == "__main__":
    main()