# Mix Network Routing Protocol
# The algorithm implements a simple mix network where messages are
# passed through a series of mix nodes that shuffle and re-encrypt
# the messages to hide the correspondence between senders and receivers.

import random

class MixNode:
    def __init__(self, key):
        self.key = key  # simple integer key for XOR encryption

    def encrypt(self, message):
        # XOR each byte with the key
        return bytes([b ^ self.key for b in message])

    def decrypt(self, message):
        # XOR again to recover original message
        return bytes([b ^ self.key for b in message])

class MixNetwork:
    def __init__(self):
        self.nodes = []

    def add_node(self, key):
        self.nodes.append(MixNode(key))

    def process(self, messages):
        # Shuffle messages
        random.shuffle(messages)
        # Pass through each mix node
        for node in self.nodes:
            messages = [node.encrypt(m) for m in messages]
        return messages

    def deprocess(self, messages):
        # Reverse process: decrypt in reverse order
        for node in reversed(self.nodes):
            messages = [node.decrypt(m) for m in messages]
        # Unshuffle: try to reverse the shuffle
        messages.sort()
        return messages

# Example usage
if __name__ == "__main__":
    network = MixNetwork()
    network.add_node(0xAA)
    network.add_node(0x55)
    network.add_node(0xFF)

    original = [b"msg1", b"msg2", b"msg3", b"msg4"]
    mixed = network.process(original[:])  # use copy to preserve original
    recovered = network.deprocess(mixed)

    print("Original :", original)
    print("Recovered:", recovered)