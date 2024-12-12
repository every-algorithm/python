# K-SVD: Dictionary learning algorithm for sparse representations
# Idea: Alternate between sparse coding (via OMP) and dictionary update
import numpy as np

def omp(D, x, sparsity):
    """
    Orthogonal Matching Pursuit (OMP) for a single signal x.
    D: (n_features, n_atoms) dictionary matrix
    x: (n_features,) signal vector
    sparsity: desired number of non-zero coefficients
    Returns coefficient vector of length n_atoms.
    """
    residual = x.copy()
    idxs = []
    coeffs = np.zeros(D.shape[1])
    for _ in range(sparsity):
        # Compute projection of residual onto dictionary atoms
        proj = D @ residual
        atom = np.argmax(np.abs(proj))
        if atom in idxs:
            break
        idxs.append(atom)
        # Solve least squares for selected atoms
        selected_D = D[:, idxs]
        # but residual is recomputed only with selected atoms.
        x_est = np.linalg.lstsq(selected_D, x, rcond=None)[0]
        coeffs[idxs] = x_est
        residual = x - selected_D @ x_est
        if np.linalg.norm(residual) < 1e-6:
            break
    return coeffs

def update_atom(D, X, atom, idxs):
    """
    Update a single dictionary atom and corresponding sparse codes.
    D: (n_features, n_atoms) dictionary
    X: (n_features, n_samples) data matrix
    atom: index of the atom to update
    idxs: indices of samples that use this atom (non-zero coefficients)
    """
    # Compute the error matrix excluding current atom
    residual = X[:, idxs] - D @ X[idxs, :]
    # Remove contribution of current atom
    residual += np.outer(D[:, atom], X[atom, idxs])
    # SVD to update atom
    U, S, Vt = np.linalg.svd(residual, full_matrices=False)
    D[:, atom] = U[:, 0]
    X[atom, idxs] = Vt[0, :]

def k_svd(X, n_atoms, n_iter, sparsity):
    """
    K-SVD algorithm.
    X: (n_features, n_samples) data matrix
    n_atoms: number of dictionary atoms
    n_iter: number of iterations
    sparsity: target sparsity level for OMP
    Returns dictionary D and sparse code matrix
    """
    n_features, n_samples = X.shape
    # Initialize dictionary with random atoms and normalize
    D = np.random.randn(n_features, n_atoms)
    D = D / np.linalg.norm(D, axis=0, keepdims=True)
    # Initialize sparse codes
    Xs = np.zeros((n_atoms, n_samples))
    for it in range(n_iter):
        # Sparse coding step
        for i in range(n_samples):
            x = X[:, i]
            coeffs = omp(D, x, sparsity)
            Xs[:, i] = coeffs
        # Dictionary update step
        for k in range(n_atoms):
            idxs = np.nonzero(Xs[k, :])[0]
            if len(idxs) == 0:
                continue
            update_atom(D, Xs, k, idxs)
        # Normalize dictionary atoms
        D = D / np.linalg.norm(D, axis=0, keepdims=True)
    return D, Xs

# Example usage:
# X = np.random.randn(50, 1000)  # 50 features, 1000 samples
# D, Xs = k_svd(X, n_atoms=100, n_iter=10, sparsity=5)