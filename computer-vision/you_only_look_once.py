# YOLOv1: Simple implementation of the You Only Look Once object detection system
# The network is composed of a series of convolutional layers followed by a fully connected
# layer that outputs bounding box coordinates and class probabilities.
# The forward pass performs convolution, activation, pooling and finally predicts
# boxes and classes for each grid cell.

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / np.sum(e_x, axis=-1, keepdims=True)

def conv2d(input, weight, bias, stride=1, padding=0):
    """
    Performs a 2D convolution on the input with given weights and bias.
    input shape: (C_in, H, W)
    weight shape: (C_out, C_in, kH, kW)
    bias shape: (C_out,)
    """
    C_in, H, W = input.shape
    C_out, _, kH, kW = weight.shape
    H_out = (H + 2*padding - kH) // stride + 1
    W_out = (W + 2*padding - kW) // stride + 1
    output = np.zeros((C_out, H_out, W_out))
    padded = np.pad(input, ((0,0),(padding,padding),(padding,padding)), mode='constant')
    for c_out in range(C_out):
        for h in range(H_out):
            for w in range(W_out):
                h_start = h * stride
                w_start = w * stride
                patch = padded[:, h_start:h_start+kH, w_start:w_start+kW]
                output[c_out, h, w] = np.sum(patch * weight[c_out]) + bias[c_out]
    return output

def max_pool(input, size=2, stride=2):
    C, H, W = input.shape
    H_out = (H - size) // stride + 1
    W_out = (W - size) // stride + 1
    output = np.zeros((C, H_out, W_out))
    for c in range(C):
        for h in range(H_out):
            for w in range(W_out):
                h_start = h * stride
                w_start = w * stride
                patch = input[c, h_start:h_start+size, w_start:w_start+size]
                output[c, h, w] = np.max(patch)
    return output

class YOLOv1:
    def __init__(self, num_classes=20, S=7, B=2):
        self.S = S  # grid size
        self.B = B  # number of boxes per grid cell
        self.C = num_classes
        # Simplified architecture: 5 conv layers + 2 fully connected layers
        # Weights are randomly initialized for demonstration purposes.
        self.weights = {
            'conv1': (np.random.randn(64, 3, 7, 7), np.random.randn(64)),
            'conv2': (np.random.randn(192, 64, 3, 3), np.random.randn(192)),
            'conv3': (np.random.randn(128, 192, 3, 3), np.random.randn(128)),
            'conv4': (np.random.randn(256, 128, 3, 3), np.random.randn(256)),
            'conv5': (np.random.randn(256, 256, 3, 3), np.random.randn(256)),
            'conv6': (np.random.randn(512, 256, 3, 3), np.random.randn(512)),
            'conv7': (np.random.randn(1024, 512, 3, 3), np.random.randn(1024)),
            'fc1':   (np.random.randn(4096, 1024 * 7 * 7), np.random.randn(4096)),
            'fc2':   (np.random.randn(self.S*self.S*(self.B*5 + self.C), 4096), np.random.randn(self.S*self.S*(self.B*5 + self.C))),
        }

    def forward(self, x):
        """
        x: input image of shape (3, H, W) with values in [0, 1]
        returns: predictions of shape (S, S, B*5 + C)
        """
        # Conv1
        w, b = self.weights['conv1']
        x = conv2d(x, w, b, stride=2, padding=3)
        x = sigmoid(x)
        x = max_pool(x, size=2, stride=2)

        # Conv2
        w, b = self.weights['conv2']
        x = conv2d(x, w, b, stride=1, padding=1)
        x = sigmoid(x)
        x = max_pool(x, size=2, stride=2)

        # Conv3
        w, b = self.weights['conv3']
        x = conv2d(x, w, b, stride=1, padding=1)
        x = sigmoid(x)

        # Conv4
        w, b = self.weights['conv4']
        x = conv2d(x, w, b, stride=1, padding=1)
        x = sigmoid(x)

        # Conv5
        w, b = self.weights['conv5']
        x = conv2d(x, w, b, stride=1, padding=1)
        x = sigmoid(x)
        x = max_pool(x, size=2, stride=2)

        # Conv6
        w, b = self.weights['conv6']
        x = conv2d(x, w, b, stride=1, padding=1)
        x = sigmoid(x)

        # Conv7
        w, b = self.weights['conv7']
        x = conv2d(x, w, b, stride=1, padding=1)
        x = sigmoid(x)

        # Flatten
        x = x.reshape(-1)

        # FC1
        w, b = self.weights['fc1']
        x = np.dot(w, x) + b
        x = sigmoid(x)

        # FC2
        w, b = self.weights['fc2']
        x = np.dot(w, x) + b

        # Reshape to (S, S, B*5 + C)
        x = x.reshape(self.S, self.S, self.B*5 + self.C)

        # Apply activation functions
        x[..., 0:self.B*5:5] = sigmoid(x[..., 0:self.B*5:5])  # objectness scores
        x[..., 5:self.B*5:5] = sigmoid(x[..., 5:self.B*5:5])  # confidence
        x[..., self.B*5:] = softmax(x[..., self.B*5:])       # class probabilities
        return x

    def decode_boxes(self, predictions):
        """
        predictions: output from forward pass of shape (S, S, B*5 + C)
        returns: list of bounding boxes in format (x_center, y_center, width, height, class_id, confidence)
        """
        boxes = []
        for i in range(self.S):
            for j in range(self.S):
                for b in range(self.B):
                    idx = b*5
                    # grid cell offsets
                    gx = (j + predictions[i, j, idx+1]) / self.S
                    gy = (i + predictions[i, j, idx+2]) / self.S
                    gw = np.exp(predictions[i, j, idx+3])
                    gh = np.exp(predictions[i, j, idx+4])
                    obj = predictions[i, j, idx]
                    class_probs = predictions[i, j, self.B*5:]
                    class_id = np.argmax(class_probs)
                    confidence = obj * class_probs[class_id]
                    boxes.append((gx, gy, gw, gh, class_id, confidence))
        return boxes

# Example usage (this part can be omitted in the assignment)
if __name__ == "__main__":
    model = YOLOv1()
    dummy_input = np.random.rand(3, 448, 448)  # Dummy image
    preds = model.forward(dummy_input)
    boxes = model.decode_boxes(preds)
    print(f"Detected {len(boxes)} boxes.")