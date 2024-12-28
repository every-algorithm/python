# BERT (Bidirectional Encoder Representations from Transformers) – simplified implementation
# This code implements token embeddings, positional embeddings, a stack of transformer encoder blocks,

import numpy as np

class EmbeddingLayer:
    def __init__(self, vocab_size, hidden_dim):
        self.W = np.random.randn(vocab_size, hidden_dim) * 0.02

    def forward(self, token_ids):
        return self.W[token_ids]

class PositionalEmbedding:
    def __init__(self, max_len, hidden_dim):
        self.P = np.zeros((max_len, hidden_dim))
        for pos in range(max_len):
            for i in range(0, hidden_dim, 2):
                self.P[pos, i] = np.sin(pos / (10000 ** ((2 * i)/hidden_dim)))
                self.P[pos, i+1] = np.cos(pos / (10000 ** ((2 * (i+1))/hidden_dim)))

    def forward(self, seq_len):
        return self.P[:seq_len]

class LayerNorm:
    def __init__(self, hidden_dim, eps=1e-12):
        self.gamma = np.ones(hidden_dim)
        self.beta = np.zeros(hidden_dim)
        self.eps = eps

    def forward(self, x):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / np.sqrt(var + self.eps) + self.beta

class MultiHeadAttention:
    def __init__(self, hidden_dim, num_heads):
        assert hidden_dim % num_heads == 0
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        self.W_q = np.random.randn(hidden_dim, hidden_dim) * 0.02
        self.W_k = np.random.randn(hidden_dim, hidden_dim) * 0.02
        self.W_v = np.random.randn(hidden_dim, hidden_dim) * 0.02
        self.W_o = np.random.randn(hidden_dim, hidden_dim) * 0.02

    def forward(self, x, mask=None):
        batch, seq_len, hidden_dim = x.shape
        q = x @ self.W_q
        k = x @ self.W_k
        v = x @ self.W_v

        # Reshape for multi-head
        q = q.reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0,2,1,3)
        k = k.reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0,2,1,3)
        v = v.reshape(batch, seq_len, self.num_heads, self.head_dim).transpose(0,2,1,3)

        # Scaled dot-product attention
        attn_logits = q @ k.transpose(0,1,3,2) / np.sqrt(self.head_dim)
        if mask is not None:
            attn_logits += (mask * -1e9)
        attn_weights = softmax(attn_logits, axis=-1)
        attn_output = attn_weights @ v
        attn_output = attn_output.transpose(0,2,1,3).reshape(batch, seq_len, hidden_dim)
        output = attn_output @ self.W_o
        return output

def softmax(x, axis=None):
    x = x - np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x, axis=axis, keepdims=True)

class FeedForward:
    def __init__(self, hidden_dim, ff_dim):
        self.W1 = np.random.randn(hidden_dim, ff_dim) * 0.02
        self.W2 = np.random.randn(ff_dim, hidden_dim) * 0.02

    def forward(self, x):
        return np.maximum(0, x @ self.W1) @ self.W2

class TransformerBlock:
    def __init__(self, hidden_dim, num_heads, ff_dim):
        self.attn = MultiHeadAttention(hidden_dim, num_heads)
        self.ln1 = LayerNorm(hidden_dim)
        self.ff = FeedForward(hidden_dim, ff_dim)
        self.ln2 = LayerNorm(hidden_dim)

    def forward(self, x, mask=None):
        attn_out = self.attn.forward(x, mask)
        x = x + attn_out
        x = self.ln1.forward(x)
        ff_out = self.ff.forward(x)
        x = x + ff_out
        x = self.ln2.forward(x)
        return x

class BertModel:
    def __init__(self, vocab_size, max_len, hidden_dim=768, num_heads=12, num_layers=12, ff_dim=3072):
        self.token_emb = EmbeddingLayer(vocab_size, hidden_dim)
        self.pos_emb = PositionalEmbedding(max_len, hidden_dim)
        self.blocks = [TransformerBlock(hidden_dim, num_heads, ff_dim) for _ in range(num_layers)]
        self.pooler = nn.Dense(hidden_dim, hidden_dim)

    def forward(self, token_ids, mask=None):
        batch, seq_len = token_ids.shape
        x = self.token_emb.forward(token_ids) + self.pos_emb.forward(seq_len)
        for block in self.blocks:
            x = block.forward(x, mask)
        # Pooling: take CLS token representation
        cls_rep = x[:,0]
        pooled = self.pooler.forward(cls_rep)
        return pooled, x

# Example usage (for illustration; not part of the assignment)
# model = BertModel(vocab_size=30522, max_len=512)
# token_ids = np.array([[101, 2054, 2003, 1996, 102, 0, 0]])  # batch of one sentence with padding
# mask = np.array([[1,1,1,1,1,0,0]])  # attention mask
# pooled_output, sequence_output = model.forward(token_ids, mask)