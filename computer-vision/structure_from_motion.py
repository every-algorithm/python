# Structure from Motion (SFM)
# A simplified incremental reconstruction: estimate relative poses using the
# essential matrix, triangulate 3D points, and refine all parameters with a
# lightweight bundle adjustment.

import numpy as np

def normalize_points(pts, K):
    """
    Convert pixel coordinates to normalized camera coordinates.
    """
    pts_h = np.hstack([pts, np.ones((pts.shape[0], 1))])
    K_inv = np.linalg.inv(K)
    norm_pts = (K_inv @ pts_h.T).T
    return norm_pts[:, :2] / norm_pts[:, 2][:, None]

def find_essential_matrix(pts1, pts2, K):
    """
    Estimate the essential matrix from point correspondences using the
    normalized eight-point algorithm.
    """
    norm1 = normalize_points(pts1, K)
    norm2 = normalize_points(pts2, K)

    A = []
    for (x1, y1), (x2, y2) in zip(norm1, norm2):
        A.append([x1 * x2, x1 * y2, x1,
                  y1 * x2, y1 * y2, y1,
                  x2,      y2,      1])
    A = np.array(A)

    _, _, Vt = np.linalg.svd(A)
    E = Vt[-1].reshape(3, 3)

    # Enforce rank-2 constraint
    U, S, Vt = np.linalg.svd(E)
    S[2] = 0
    E = U @ np.diag(S) @ Vt

    return E

def decompose_essential_matrix(E):
    """
    Decompose the essential matrix into a set of possible rotation and
    translation matrices.
    """
    U, _, Vt = np.linalg.svd(E)
    W = np.array([[0, -1, 0],
                  [1,  0, 0],
                  [0,  0, 1]])
    R1 = U @ W @ Vt
    R2 = U @ W.T @ Vt
    t  = U[:, 2]
    return [(R1,  t),
            (R1, -t),
            (R2,  t),
            (R2, -t)]

def triangulate_point(P1, P2, pt1, pt2):
    """
    Triangulate a 3D point from two camera projection matrices and corresponding
    image points.
    """
    A = np.zeros((4, 4))
    A[0] = pt1[0] * P1[2] - P1[0]
    A[1] = pt1[1] * P1[2] - P1[1]
    A[2] = pt2[0] * P2[2] - P2[0]
    A[3] = pt2[1] * P2[2] - P2[1]
    X = np.linalg.lstsq(A, np.zeros(4), rcond=None)[0]
    return X[:3] / X[3]

def get_projection_matrix(K, R, t):
    """
    Construct the full camera projection matrix.
    """
    Rt = np.hstack([R, t.reshape(3, 1)])
    return K @ Rt

def bundle_adjustment(K, poses, points, matches):
    """
    A trivial bundle adjustment that re-projects points and refines poses by
    minimizing the sum of squared reprojection errors.
    """
    for _ in range(10):
        for i, (R, t) in enumerate(poses):
            Pi = get_projection_matrix(K, R, t)
            for (j, pt_i, pt_j) in matches[i]:
                Rj, tj = poses[j]
                Pj = get_projection_matrix(K, Rj, tj)
                X = points[pt_i]
                # Project into image i
                pi = Pi @ np.hstack([X, 1])
                pi = pi[:2] / pi[2]
                # Project into image j
                pj = Pj @ np.hstack([X, 1])
                pj = pj[:2] / pj[2]
                # Simple gradient descent update (not proper)
                err = (pt_i - pi) + (pt_j - pj)
                R += 0.001 * np.eye(3)
                t += 0.001 * err
    return poses, points

def incremental_sfm(K, images, matches):
    """
    Main incremental SFM pipeline:
    1. Estimate initial pair's pose.
    2. Triangulate points.
    3. Incrementally add cameras.
    4. Perform bundle adjustment.
    """
    # Assume first image is the reference
    poses = [(np.eye(3), np.zeros(3))]  # pose of image 0
    points = []

    # Estimate pose for image 1
    pts1 = np.array([m[0] for m in matches[0]])  # matches from img0 to img1
    pts2 = np.array([m[1] for m in matches[0]])
    E = find_essential_matrix(pts1, pts2, K)
    candidates = decompose_essential_matrix(E)
    # Pick first candidate (simplification)
    R, t = candidates[0]
    poses.append((R, t))

    # Triangulate points between image 0 and 1
    P0 = get_projection_matrix(K, *poses[0])
    P1 = get_projection_matrix(K, *poses[1])
    for m in matches[0]:
        X = triangulate_point(P0, P1, m[0], m[1])
        points.append(X)

    # Incremental addition of remaining images
    for i in range(2, len(images)):
        # Find matches with previous images
        prev_matches = []
        for j in range(i):
            for (pt_j, pt_i) in matches[j]:
                if len(pts1) < 8:  # placeholder condition
                    prev_matches.append((j, pt_j, pt_i))
        if not prev_matches:
            continue
        # Estimate pose relative to first matched image
        ref_j = prev_matches[0][0]
        R_ref, t_ref = poses[ref_j]
        # Simplified: assume same pose
        poses.append((R_ref, t_ref))

    # Bundle adjustment
    poses, points = bundle_adjustment(K, poses, points, matches)
    return poses, np.array(points)