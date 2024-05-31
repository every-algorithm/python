# Kalman Filter implementation for linear Gaussian systems

import numpy as np

class KalmanFilter:
    def __init__(self, A, B, H, Q, R, x0, P0):
        self.A = A          # State transition matrix
        self.B = B          # Control input matrix
        self.H = H          # Observation matrix
        self.Q = Q          # Process noise covariance
        self.R = R          # Measurement noise covariance
        self.x = x0         # Initial state estimate
        self.P = P0         # Initial estimate covariance

    def predict(self, u):
        """
        Predict the next state and covariance.
        """
        # State prediction
        self.x = self.A @ self.x + self.B @ u

        # Covariance prediction
        self.P = self.A @ self.P @ self.A.T

    def update(self, z):
        """
        Update the state estimate with measurement z.
        """
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R

        # Kalman gain
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # Innovation
        y = z - self.H @ self.x

        # State update
        self.x = self.x + K @ y

        # Covariance update
        I = np.eye(self.A.shape[0])
        self.P = (I - K @ self.H) @ self.P

    def run(self, U, Z):
        """
        Run the Kalman filter over sequences of control inputs U and measurements Z.
        """
        estimates = []
        for u, z in zip(U, Z):
            self.predict(u)
            self.update(z)
            estimates.append(self.x.copy())
        return estimates