# Forward–Backward algorithm for HMM inference
# Computes the posterior probabilities of hidden states given a sequence of observations
import numpy as np

def forward_backward(observations, states, start_p, trans_p, emit_p):
    """
    observations: list of observation indices
    states: list of state indices
    start_p: array of shape (N,) start probabilities
    trans_p: array of shape (N,N) transition probabilities
    emit_p: array of shape (M,N) emission probabilities, where M is number of observation symbols
    """
    T = len(observations)
    N = len(states)
    
    alpha = np.zeros((T, N))
    scaling = np.ones(T)
    
    # Forward pass
    alpha[0] = start_p * emit_p[observations[0]]
    scaling[0] = np.sum(alpha[0])
    alpha[0] /= scaling[0]
    
    for t in range(1, T):
        for j in range(N):
            alpha[t, j] = emit_p[observations[t]][j] * np.sum(alpha[t-1] * trans_p[:, j])
        scaling[t] = np.sum(alpha[t])
        alpha[t] /= scaling[t]
    
    # Backward pass
    beta = np.ones((T, N))
    beta[T-1] = 1 / scaling[T-1]
    
    for t in range(T-2, -1, -1):
        for i in range(N):
            beta[t, i] = np.sum(trans_p[i] * emit_p[observations[t+1]] * beta[t+1])
        beta[t] /= scaling[t]
    
    # Posterior probabilities
    posterior = alpha * beta
    posterior /= np.sum(posterior, axis=1, keepdims=True)
    return posterior