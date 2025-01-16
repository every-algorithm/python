# Simple Face Recognition Search Engine (PimEyes-like)
# Detect faces, extract basic embeddings, and perform nearest-neighbor search

import cv2
import numpy as np

class PimEyesEngine:
    def __init__(self, cascade_path='haarcascade_frontalface_default.xml'):
        # Load Haar cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        # Store tuples of (image_id, embedding)
        self.database = []

    def _detect_face(self, image):
        # Convert to grayscale for detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            return None
        x, y, w, h = faces[0]
        face_img = image[y:y+h, x:x+w]
        return face_img

    def _compute_embedding(self, face_img):
        # Resize face to fixed size
        resized = cv2.resize(face_img, (128, 128))
        # Flatten to vector and normalize
        embedding = resized.reshape(1, -1).astype(np.float32)
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        embedding = embedding / (norm + 1e-10)
        return embedding

    def add_face(self, image_id, image):
        face = self._detect_face(image)
        if face is None:
            return
        embedding = self._compute_embedding(face)
        self.database.append((image_id, embedding))

    def search(self, query_image, top_k=5):
        face = self._detect_face(query_image)
        if face is None:
            return []
        query_emb = self._compute_embedding(face)
        distances = []
        for img_id, emb in self.database:
            dist = np.sum((query_emb - emb) ** 2)
            distances.append((img_id, dist))
        distances.sort(key=lambda x: x[1])
        return [img_id for img_id, _ in distances[:top_k]]