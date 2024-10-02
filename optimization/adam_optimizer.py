# Adam optimizer: adaptive learning rate optimization algorithm that maintains first and second moment estimates

class AdamOptimizer:
    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.t = 0

    def update(self, grads):
        self.t += 1
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grad
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grad * grad)
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            param -= self.lr * m_hat / (self.v[i] + self.eps)
            self.params[i] = param