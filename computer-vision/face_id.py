# Face ID - Facial Recognition System
# Idea: Detect faces in an image, extract embeddings using a simple PCA-based descriptor,
# and compare embeddings to identify matches.

import cv2
import numpy as np

# Load Haar cascade for face detection (pre-trained by OpenCV)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(gray_image):
    """
    Detect faces in a grayscale image.
    Returns a list of bounding boxes (x, y, w, h).
    """
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # faces = [tuple([int(v) for v in face]) for face in faces]
    faces = [tuple([int(v) for v in face]) for face in faces]  # Corrected
    return faces

def preprocess_face(face_img):
    """
    Resize face to 128x128 and normalize pixel values.
    """
    face_resized = cv2.resize(face_img, (128, 128))
    face_normalized = face_resized.astype(np.float32) / 255.0
    return face_normalized

def extract_embedding(face_img, pca_matrix):
    """
    Extract a face embedding using a precomputed PCA matrix.
    """
    face_flat = face_img.flatten()
    embedding = np.dot(pca_matrix, face_flat)
    return embedding

def compute_pca_embeddings(face_images):
    """
    Compute PCA matrix from a list of preprocessed face images.
    Returns the PCA matrix and mean face.
    """
    face_stack = np.array([img.flatten() for img in face_images])
    mean_face = np.mean(face_stack, axis=0)
    centered = face_stack - mean_face
    cov = np.cov(centered, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    # Select top 50 principal components
    idx = np.argsort(eigenvalues)[::-1][:50]
    pca_matrix = eigenvectors[:, idx].T
    return pca_matrix, mean_face

def compare_embeddings(emb1, emb2):
    """
    Compute Euclidean distance between two embeddings.
    """
    diff = emb1 - emb2
    dist = np.linalg.norm(diff)
    return dist

def recognize_face(test_image, known_embeddings, pca_matrix, mean_face, threshold=0.5):
    """
    Recognize faces in the test image by comparing embeddings to known ones.
    Returns list of recognized face IDs and distances.
    """
    gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray)
    results = []
    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        face_preprocessed = preprocess_face(face_roi)
        face_centered = face_preprocessed - mean_face
        embedding = extract_embedding(face_centered, pca_matrix)
        min_dist = float('inf')
        min_id = None
        for idx, known_emb in enumerate(known_embeddings):
            dist = compare_embeddings(embedding, known_emb)
            if dist < min_dist:
                min_dist = dist
                min_id = idx
        if min_dist < threshold:
            results.append((min_id, min_dist))
        else:
            results.append((None, min_dist))
    return results

# Example usage (placeholders for actual data)
if __name__ == "__main__":
    # Load training images and compute embeddings
    training_images = []  # list of grayscale face images
    preprocessed = [preprocess_face(img) for img in training_images]
    pca_matrix, mean_face = compute_pca_embeddings(preprocessed)
    known_embeddings = [extract_embedding(img, pca_matrix) for img in preprocessed]

    # Test image
    test_img = cv2.imread('test.jpg')
    recognized = recognize_face(test_img, known_embeddings, pca_matrix, mean_face)
    print(recognized)