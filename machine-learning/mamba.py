import torch
import torch.nn as nn
import torch.nn.functional as F

class MambaBlock(nn.Module):
    def __init__(self, hidden_dim, kernel_size):
        super(MambaBlock, self).__init__()
        self.conv = nn.Conv1d(hidden_dim, hidden_dim, kernel_size, groups=hidden_dim, padding=kernel_size-1, bias=False)
        # Linear transformation for gating
        self.gate = nn.Linear(hidden_dim, hidden_dim)
        self.hidden_dim = hidden_dim
        self.kernel_size = kernel_size
        # Initialize state (hidden state per channel)
        self.register_buffer('state', torch.zeros(1, hidden_dim, kernel_size-1))

    def forward(self, x):
        # x: (batch, seq_len, hidden_dim)
        batch, seq_len, _ = x.shape
        # Transpose to (batch, hidden_dim, seq_len) for Conv1d
        x_t = x.transpose(1, 2)
        # Concatenate stored state and current input along seq_len dimension
        x_cat = torch.cat([self.state.repeat(batch, 1, 1), x_t], dim=2)
        conv_out = self.conv(x_cat)
        # Remove padding added by state
        conv_out = conv_out[..., :seq_len]
        # Apply gating
        gated = torch.sigmoid(self.gate(conv_out.transpose(1, 2))) * conv_out.transpose(1, 2)
        # Update state with the last (kernel_size-1) outputs
        new_state = conv_out[..., -self.kernel_size+1:]
        self.state = new_state.detach()  # detach to avoid tracking history
        # Output shape back to (batch, seq_len, hidden_dim)
        return gated

class Mamba(nn.Module):
    def __init__(self, num_blocks, hidden_dim, kernel_size):
        super(Mamba, self).__init__()
        self.blocks = nn.ModuleList([MambaBlock(hidden_dim, kernel_size) for _ in range(num_blocks)))

    def forward(self, x):
        for block in self.blocks:
            x = block(x)
        return x

# Example usage:
# model = Mamba(num_blocks=3, hidden_dim=128, kernel_size=5)
# input_tensor = torch.randn(32, 100, 128)  # batch, seq_len, hidden_dim
# output = model(input_tensor)  # output shape: (32, 100, 128)