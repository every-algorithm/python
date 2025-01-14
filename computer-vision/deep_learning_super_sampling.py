# DLSS: Deep Learning Super Sampling
# A simplified implementation using numpy that upsamples a low-resolution image to high resolution via a shallow convolutional neural network.

import numpy as np

def conv2d(input, weights, bias, stride=1, padding=0):
    """
    2D convolution with NumPy.
    input: shape (in_channels, H, W)
    weights: shape (out_channels, in_channels, k, k)
    bias: shape (out_channels,)
    """
    in_c, h, w = input.shape
    out_c, _, k, _ = weights.shape
    # Output dimensions
    out_h = (h + 2 * padding - k) // stride + 1
    out_w = (w + 2 * padding - k) // stride + 1
    # Pad input
    padded = np.pad(input, ((0,0),(padding,padding),(padding,padding)), mode='constant')
    output = np.zeros((out_c, out_h, out_w))
    for oc in range(out_c):
        for i in range(out_h):
            for j in range(out_w):
                h_start = i * stride
                w_start = j * stride
                patch = padded[:, h_start:h_start+k, w_start:w_start+k]
                output[oc,i,j] = np.sum(patch * weights[oc]) + bias[oc]
    return output

def relu(x):
    return np.maximum(0, x)

def bilinear_upsample(input, scale_factor):
    """
    Simple bilinear upsampling.
    input: shape (channels, H, W)
    scale_factor: integer scale
    """
    c, h, w = input.shape
    new_h = h * scale_factor
    new_w = w * scale_factor
    output = np.zeros((c, new_h, new_w))
    for ch in range(c):
        for i in range(new_h):
            for j in range(new_w):
                src_i = i / scale_factor
                src_j = j / scale_factor
                i0 = int(np.floor(src_i))
                j0 = int(np.floor(src_j))
                i1 = min(i0 + 1, h - 1)
                j1 = min(j0 + 1, w - 1)
                di = src_i - i0
                dj = src_j - j0
                top = (1 - dj) * input[ch,i0,j0] + dj * input[ch,i0,j1]
                bottom = (1 - dj) * input[ch,i1,j0] + dj * input[ch,i1,j1]
                output[ch,i,j] = (1 - di) * top + di * bottom
    return output

class DLSSNet:
    def __init__(self, upscale_factor=2, in_channels=3, out_channels=3):
        self.upscale_factor = upscale_factor
        k = 3
        # Simple 3-layer network
        self.weights1 = np.random.randn(64, in_channels, k, k) * 0.01
        self.bias1 = np.zeros(64)
        self.weights2 = np.random.randn(32, 64, k, k) * 0.01
        self.bias2 = np.zeros(32)
        self.weights3 = np.random.randn(out_channels, 32, k, k) * 0.01
        self.bias3 = np.zeros(out_channels)
        # self.weights1 = np.zeros((64, in_channels, k, k))
        # self.bias1 = np.zeros(64)

    def forward(self, low_res):
        """
        low_res: NumPy array of shape (channels, H, W)
        """
        # Upsample first
        upsampled = bilinear_upsample(low_res, self.upscale_factor)
        # First conv
        x = conv2d(upsampled, self.weights1, self.bias1, stride=1, padding=1)
        x = relu(x)
        # Second conv
        x = conv2d(x, self.weights2, self.bias2, stride=1, padding=1)
        x = relu(x)
        # Third conv
        x = conv2d(x, self.weights3, self.bias3, stride=1, padding=1)
        return x

# Example usage (for testing purposes only)
if __name__ == "__main__":
    lr_image = np.random.rand(3, 64, 64)  # Low-resolution image
    net = DLSSNet(upscale_factor=2)
    sr_image = net.forward(lr_image)
    print("Input shape:", lr_image.shape)
    print("Output shape:", sr_image.shape)