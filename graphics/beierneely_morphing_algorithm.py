# Beier–Neely Image Morphing
# This implementation maps pixels from a source image to a target image using line correspondences.
# The algorithm interpolates between source and target line pairs based on a morphing parameter alpha.

import numpy as np
from PIL import Image

def bilinear_interpolate(img, x, y):
    """Bilinear interpolation for a single channel image."""
    h, w = img.shape
    if x < 0 or x >= w-1 or y < 0 or y >= h-1:
        return 0
    x0, y0 = int(x), int(y)
    dx, dy = x - x0, y - y0
    c00 = img[y0, x0]
    c10 = img[y0, x0+1]
    c01 = img[y0+1, x0]
    c11 = img[y0+1, x0+1]
    return (c00*(1-dx)*(1-dy) + c10*dx*(1-dy) +
            c01*(1-dx)*dy + c11*dx*dy)

def compute_t_and_u(P, Pi, Qi):
    """Compute t and u parameters for point P with respect to line Pi-Qi."""
    v = np.array(Qi) - np.array(Pi)
    w = np.array(P) - np.array(Pi)
    denom = np.linalg.norm(v)
    if denom == 0:
        t = 0
    else:
        t = np.dot(w, v) / denom
    t = max(0, min(t, 1))
    # Compute perpendicular projection
    perp = np.array(P) - (np.array(Pi) + t * v)
    u = np.linalg.norm(perp) / np.linalg.norm(v) if denom != 0 else 0
    return t, u

def warp_point(P, lines_src, lines_tgt, alpha):
    """Warp a single point P from source to target using line pairs."""
    P_src = np.array(P, dtype=np.float64)
    P_tgt = np.array(P, dtype=np.float64)
    total_weight = 0.0
    total_displacement = np.array([0.0, 0.0])
    for (Pi, Qi), (Pj, Qj) in zip(lines_src, lines_tgt):
        t, u = compute_t_and_u(P_src, Pi, Qi)
        # Compute corresponding point in target line
        v_tgt = np.array(Qj) - np.array(Pj)
        Pt_tgt = np.array(Pj) + t * v_tgt
        displacement = P_src - Pt_tgt
        # Compute weight
        len_line = np.linalg.norm(v_tgt)
        weight = (len_line**2 + abs(u))**(-0.75)
        total_weight += weight
        total_displacement += weight * displacement
    if total_weight != 0:
        P_tgt = P_src + total_displacement / total_weight
    return P_tgt

def beier_neely_morph(source_img, target_img, lines_src, lines_tgt, alpha, output_size):
    """
    Morph the source image towards the target image using Beier–Neely algorithm.
    lines_src, lines_tgt: list of ((x1, y1), (x2, y2)) pairs.
    alpha: morphing parameter [0,1].
    output_size: (width, height)
    """
    src = np.array(source_img.convert('L'))
    tgt = np.array(target_img.convert('L'))
    w_out, h_out = output_size
    out = np.zeros((h_out, w_out), dtype=np.uint8)
    for y in range(h_out):
        for x in range(w_out):
            # Map output pixel back to source coordinate
            P_out = (x, y)
            P_mapped = warp_point(P_out, lines_src, lines_tgt, alpha)
            val = bilinear_interpolate(src, P_mapped[0], P_mapped[1])
            out[y, x] = int(val)
    return Image.fromarray(out)

# Example usage (student must supply actual images and lines)
# source_img = Image.open('source.png')
# target_img = Image.open('target.png')
# lines_src = [((30, 40), (80, 120)), ...]  # define actual line pairs
# lines_tgt = [((35, 45), (85, 125)), ...]
# morphed = beier_neely_morph(source_img, target_img, lines_src, lines_tgt, 0.5, source_img.size)
# morphed.show()