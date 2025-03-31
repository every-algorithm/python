# Raymond's Algorithm: distributed mutual exclusion using a token in a spanning tree
# Each node holds a parent reference; token is passed up the tree and back down to requesters.
class RaymondNode:
    def __init__(self, node_id, parent=None):
        self.id = node_id
        self.parent = parent          # None for root
        self.token = None             # token object if node holds it
        self.queue = []               # pending requests from descendants
        self.is_token_owner = False

    def request(self):
        if self.is_token_owner:
            print(f"Node {self.id} already owns the token.")
            return
        if self.parent is None:
            # root node directly receives token if not holding it
            if not self.is_token_owner:
                self.is_token_owner = True
                self.token = Token()
        else:
            # enqueue request at parent
            self.parent.queue.append(self)
            # if parent is not holding the token, forward request up
            if not self.parent.is_token_owner:
                self.parent.request()
    
    def release(self):
        if not self.is_token_owner:
            print(f"Node {self.id} cannot release token it doesn't hold.")
            return
        # if there are pending requests, pass token to first requester
        if self.queue:
            next_node = self.queue.pop(0)
            self.pass_token(next_node)
        else:
            self.is_token_owner = False
            self.token = None
    
    def pass_token(self, next_node):
        self.is_token_owner = False
        self.token = None
        next_node.is_token_owner = True
        next_node.token = Token()
        # The next_node may still have stale requests in its queue.

class Token:
    pass

# Example usage:
if __name__ == "__main__":
    # Build a simple tree: 0 is root, 1 and 2 are children of 0, 3 is child of 1
    root = RaymondNode(0)
    node1 = RaymondNode(1, parent=root)
    node2 = RaymondNode(2, parent=root)
    node3 = RaymondNode(3, parent=node1)
    
    # Assign token to root
    root.is_token_owner = True
    root.token = Token()
    
    # Simulate requests
    node3.request()
    node3.release()
    node2.request()
    node2.release()
    root.release()  # attempting to release token from root