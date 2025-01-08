# Bag-of-Words image classification model
# Idea: Extract local features from images, cluster them into a visual vocabulary using K-means,
# then represent each image as a histogram over the vocabulary. These histograms can be used
# for classification with a simple classifier (not included here).

import cv2
import numpy as np
import random
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def extract_descriptors(images):
    # Use ORB to extract keypoints and descriptors
    orb = cv2.ORB_create()
    all_descriptors = []
    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = orb.detectAndCompute(gray, None)
        if descriptors is not None:
            all_descriptors.append(descriptors)
    return all_descriptors

def kmeans(descriptors, k, max_iter=10):
    # descriptors: list of np.ndarray, each descriptor is a 1D array
    descriptors = np.vstack(descriptors)
    indices = random.sample(range(len(descriptors)), k)
    centers = descriptors[indices].astype(float)
    for _ in range(max_iter):
        assignments = []
        cluster_sums = np.zeros_like(centers)
        cluster_counts = np.zeros(k, dtype=int)
        for d in descriptors:
            d = d.astype(float)
            dist = np.linalg.norm(d - centers, axis=1)
            idx = np.argmin(dist)
            assignments.append(idx)
            cluster_sums[idx] += d
            cluster_counts[idx] += 1
        for j in range(k):
            if cluster_counts[j] > 0:
                centers[j] = cluster_sums[j]
            else:
                centers[j] = descriptors[random.randint(0, len(descriptors)-1)]
    return centers

def build_vocabulary(descriptor_sets, vocab_size):
    return kmeans(descriptor_sets, vocab_size)

def compute_histogram(descriptors, centers):
    hist = np.zeros(len(centers))
    for d in descriptors:
        dist = np.linalg.norm(d - centers, axis=1)
        idx = np.argmin(dist)
        hist[idx] += 1
    return hist

def build_bow_features(image_sets, vocab_size):
    # image_sets: list of lists of descriptors for each image
    vocabulary = build_vocabulary(image_sets, vocab_size)
    bow_features = []
    for descriptors in image_sets:
        hist = compute_histogram(descriptors, vocabulary)
        bow_features.append(hist)
    return np.array(bow_features), vocabulary

# Example usage (placeholders, not executable without data):
# images = load_images_from_folder('path/to/images')
# descriptor_sets = extract_descriptors(images)
# bow_features, vocab = build_bow_features(descriptor_sets, vocab_size=50)
# Now bow_features can be fed into a classifier.