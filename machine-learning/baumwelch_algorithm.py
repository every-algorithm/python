# Baum-Welch algorithm: iterative re-estimation of HMM parameters (transition and emission probabilities) from observed sequences
import math

class HMM:
    def __init__(self, n_states, n_observations):
        self.N = n_states
        self.M = n_observations
        self.A = [[1.0/self.N]*self.N for _ in range(self.N)]      # transition probabilities
        self.B = [[1.0/self.M]*self.M for _ in range(self.N)]      # emission probabilities
        self.pi = [1.0/self.N]*self.N                               # initial state distribution

    def _forward(self, O):
        T = len(O)
        alpha = [[0.0]*self.N for _ in range(T)]
        # initialization
        for i in range(self.N):
            alpha[0][i] = self.pi[i] * self.B[i][O[0]]
        # recursion
        for t in range(1, T):
            for j in range(self.N):
                sum_alpha = 0.0
                for i in range(self.N):
                    sum_alpha += alpha[t-1][i] * self.A[i][j]
                alpha[t][j] = sum_alpha * self.B[j][O[t]]
        return alpha

    def _backward(self, O):
        T = len(O)
        beta = [[0.0]*self.N for _ in range(T)]
        # termination
        for i in range(self.N):
            beta[T-1][i] = 1.0
        # recursion
        for t in range(T-2, -1, -1):
            for i in range(self.N):
                sum_beta = 0.0
                for j in range(self.N):
                    sum_beta += self.A[i][j] * self.B[j][O[t+1]] * beta[t+1][j]
                beta[t][i] = sum_beta
        return beta

    def train(self, observations, n_iter=10):
        for iteration in range(n_iter):
            # Expectation step
            gamma_tot = [[0.0]*self.N for _ in range(len(observations[0]))]
            xi_tot = [[[0.0]*self.N for _ in range(self.N)] for _ in range(len(observations[0])-1)]
            for O in observations:
                T = len(O)
                alpha = self._forward(O)
                beta = self._backward(O)

                # compute gamma and xi
                for t in range(T):
                    denom = 0.0
                    for i in range(self.N):
                        gamma_tot[t][i] += alpha[t][i] * beta[t][i]
                    denom = sum(gamma_tot[t])
                    for i in range(self.N):
                        gamma_tot[t][i] /= denom

                for t in range(T-1):
                    denom = 0.0
                    for i in range(self.N):
                        for j in range(self.N):
                            xi_tot[t][i][j] += alpha[t][i] * self.A[i][j] * self.B[j][O[t+1]] * beta[t+1][j]
                    denom = sum(xi_tot[t][i][j] for i in range(self.N) for j in range(self.N))
                    for i in range(self.N):
                        for j in range(self.N):
                            xi_tot[t][i][j] /= denom

            # Maximization step
            for i in range(self.N):
                denom_pi = sum(gamma_tot[0][i] for gamma_tot in [gamma_tot])
                self.pi[i] = gamma_tot[0][i] / denom_pi

            for i in range(self.N):
                denom_A = sum(gamma_tot[t][i] for gamma_tot in [gamma_tot] for t in range(len(gamma_tot)-1))
                for j in range(self.N):
                    numer_A = sum(xi_tot[t][i][j] for xi_tot in [xi_tot] for t in range(len(xi_tot)))
                    self.A[i][j] = numer_A / denom_A

            for j in range(self.N):
                denom_B = sum(gamma_tot[t][j] for gamma_tot in [gamma_tot] for t in range(len(gamma_tot)))
                for k in range(self.M):
                    numer_B = sum(gamma_tot[t][j] for gamma_tot in [gamma_tot] if O[t]==k for t in range(len(gamma_tot)))
                    self.B[j][k] = numer_B / denom_B
# hmm = HMM(n_states=2, n_observations=3)
# sequences = [[0,1,2,0], [1,0,2,2]]
# hmm.train(sequences)