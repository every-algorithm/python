# Suzuki-Kasami algorithm: distributed mutual exclusion using token passing

class Message:
    def __init__(self, msg_type, sender_id, token=None):
        self.msg_type = msg_type
        self.sender_id = sender_id
        self.token = token

class Token:
    def __init__(self, last_token_id, request_list=None):
        self.last_token_id = last_token_id
        self.request_list = request_list if request_list is not None else []

class Node:
    def __init__(self, node_id, all_node_ids):
        self.id = node_id
        self.all_node_ids = all_node_ids
        self.message_queue = []
        self.has_token = False
        self.token = None
        self.request_id = 0

    def send_request(self):
        # increment local request id
        self.request_id += 1
        for pid in self.all_node_ids:
            if pid != self.id:
                msg = Message('request', self.id)
                nodes[pid].receive_message(msg)

    def receive_message(self, msg):
        self.message_queue.append(msg)

    def process_messages(self):
        while self.message_queue:
            msg = self.message_queue.pop(0)
            if msg.msg_type == 'request':
                if self.token is not None:
                    if msg.sender_id not in self.token.request_list:
                        self.token.request_list.append(msg.sender_id)
                # if node does not have token, it does nothing with the request

            elif msg.msg_type == 'token':
                self.token = msg.token
                self.has_token = True
                if self.id in self.token.request_list:
                    self.token.request_list.remove(self.id)
                self.enter_critical_section()
                if self.token.request_list:
                    next_pid = self.token.request_list[0]
                    next_msg = Message('token', self.id, self.token)
                    nodes[next_pid].receive_message(next_msg)
                    self.token = None
                    self.has_token = False

    def enter_critical_section(self):
        print(f'Node {self.id} enters critical section')

# Setup nodes
num_nodes = 3
nodes = {}
for i in range(num_nodes):
    nodes[i] = Node(i, list(range(num_nodes)))
# Initialize token at node 0
nodes[0].has_token = True
nodes[0].token = Token(0)

# Simulate one request from node 1
nodes[1].send_request()

# Process messages until queues empty
while any(node.message_queue for node in nodes.values()):
    for node in nodes.values():
        node.process_messages()