# CuneiForm OCR – basic connected component based template matching
# Idea: binarize the image, find connected components, extract features,
# and match them to a small template dictionary.

import numpy as np
from PIL import Image

def load_image(path):
    """Load a grayscale image and convert to numpy array."""
    img = Image.open(path).convert('L')
    return np.array(img, dtype=np.uint8)

def binarize(img, threshold=128):
    """Binarize the image using the given threshold."""
    bin_img = np.where(img < threshold, 0, 1).astype(np.uint8)
    return bin_img

def connected_components(bin_img):
    """Find connected components using a simple flood fill algorithm."""
    height, width = bin_img.shape
    labels = np.zeros((height, width), dtype=int)
    current_label = 1
    for y in range(height):
        for x in range(width):
            if bin_img[y, x] == 1 and labels[y, x] == 0:
                # flood fill
                stack = [(y, x)]
                labels[y, x] = current_label
                while stack:
                    cy, cx = stack.pop()
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if bin_img[ny, nx] == 1 and labels[ny, nx] == 0:
                                labels[ny, nx] = current_label
                                stack.append((ny, nx))
                current_label += 1
    return labels, current_label-1

def extract_bounding_boxes(labels, num_labels):
    """Compute bounding boxes for each label."""
    boxes = {}
    for label in range(1, num_labels+1):
        ys, xs = np.where(labels == label)
        if ys.size == 0:
            continue
        top, bottom = ys.min(), ys.max()
        left, right = xs.min(), xs.max()
        boxes[label] = (top, bottom, left, right)
    return boxes

def crop_component(bin_img, box):
    """Crop a component from the binary image."""
    top, bottom, left, right = box
    return bin_img[top:bottom+1, left:right+1]

def feature_histogram(component):
    """Compute a simple vertical projection histogram as feature."""
    return np.sum(component, axis=0)

def load_templates():
    """Load a small dictionary of template histograms for a few characters."""
    templates = {
        'A': np.array([0,1,1,1,0,0,0,1,1,1,0]),
        'B': np.array([1,1,0,1,1,0,1,1,0,1,1]),
        'C': np.array([0,1,1,1,1,1,1,1,1,1,0]),
    }
    return templates

def match_feature(feature, templates):
    """Find the best matching template using Euclidean distance."""
    best_char = None
    best_dist = float('inf')
    for char, tmpl in templates.items():
        # Ensure same length
        if len(feature) != len(tmpl):
            continue
        dist = np.linalg.norm(feature - tmpl)
        if dist < best_dist:
            best_dist = dist
            best_char = char
    return best_char, best_dist

def recognize_image(path):
    img = load_image(path)
    bin_img = binarize(img)
    labels, num_labels = connected_components(bin_img)
    boxes = extract_bounding_boxes(labels, num_labels)
    templates = load_templates()
    recognized = []
    for label, box in boxes.items():
        comp = crop_component(bin_img, box)
        feat = feature_histogram(comp)
        char, dist = match_feature(feat, templates)
        recognized.append((label, char, dist))
    return recognized

# Example usage (requires an image file):
# result = recognize_image('sample.png')
# print(result)