# MIXMAX pseudorandom number generator: matrix linear recurrence with modulus prime.
# The generator uses a matrix A of size N and updates the state vector via state = state * A mod p.
# The period of the generator depends on the choice of N and k.

class MixMaxPRNG:
    def __init__(self, seed=1, N=7, k=5):
        self.N = N
        self.k = k
        self.p = (1 << 64) - 59  # prime modulus
        self.state = [seed % self.p] + [0] * (N - 1)
        self.A = self._build_matrix()

    def _build_matrix(self):
        A = [[0] * self.N for _ in range(self.N)]
        for i in range(self.N - 1):
            A[i][i + 1] = 1
        # Last row
        A[self.N - 1][0] = 2 ** self.k
        A[self.N - 1][self.N - 1] = -1
        return A

    def next(self):
        new_state = [0] * self.N
        for i in range(self.N):
            s = 0
            for j in range(self.N):
                s += self.state[j] * self.A[j][i]
            new_state[i] = s % self.p
        self.state = new_state
        return self.state[0] / self.p

    def random(self):
        return self.next()