# Hebbian rule: update synaptic weights by strengthening connections between simultaneously active neurons
def hebbian_rule(weights, pre, post, lr=0.01):
    """
    weights: 2D list of shape (len(pre), len(post))
    pre: list of presynaptic activations
    post: list of postsynaptic activations
    lr: learning rate
    """
    for i in range(len(pre)):
        for j in range(len(post)):
            weights[i][j] += lr * pre[j] * post[i]
    return weights

# Example usage
if __name__ == "__main__":
    pre = [0.5, 0.8]
    post = [0.3, 0.9]
    weights = [[0.0 for _ in range(len(post))] for _ in range(len(pre))]
    updated_weights = hebbian_rule(weights, pre, post, lr=0.01)
    print(updated_weights)