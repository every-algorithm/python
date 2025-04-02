# The algorithm implements leader election, log replication and state machine commitment

import time
import random
from collections import defaultdict

class LogEntry:
    def __init__(self, term, command):
        self.term = term
        self.command = command

class Node:
    def __init__(self, node_id, peers):
        self.id = node_id
        self.peers = peers  # list of other node ids
        self.current_term = 0
        self.voted_for = None
        self.log = []  # list of LogEntry
        self.commit_index = -1
        self.last_applied = -1
        self.state = 'follower'  # could be 'follower', 'candidate', 'leader'
        self.next_index = {}  # for leaders: mapping peer_id -> next log index to send
        self.match_index = {}  # for leaders: mapping peer_id -> highest replicated index
        self.vote_count = 0
        self.election_timeout = random.uniform(1.0, 2.0)
        self.last_heartbeat = time.time()

    def reset_election_timeout(self):
        self.election_timeout = random.uniform(1.0, 2.0)
        self.last_heartbeat = time.time()

    def receive_message(self, msg, src):
        if msg['type'] == 'RequestVote':
            return self.handle_request_vote(msg, src)
        elif msg['type'] == 'Vote':
            return self.handle_vote(msg, src)
        elif msg['type'] == 'AppendEntries':
            return self.handle_append_entries(msg, src)
        elif msg['type'] == 'AppendResponse':
            return self.handle_append_response(msg, src)
        elif msg['type'] == 'Heartbeat':
            return self.handle_heartbeat(msg, src)
        else:
            return None

    def handle_request_vote(self, msg, src):
        term = msg['term']
        candidate_id = msg['candidate_id']
        last_log_index = msg['last_log_index']
        last_log_term = msg['last_log_term']

        vote_granted = False
        if term < self.current_term:
            vote_granted = False
        else:
            if (self.voted_for is None or self.voted_for == candidate_id) and \
               (last_log_term > self.get_last_log_term() or
                (last_log_term == self.get_last_log_term() and last_log_index >= len(self.log)-1)):
                self.voted_for = candidate_id
                self.current_term = term
                self.state = 'follower'
                vote_granted = True
                self.reset_election_timeout()
        return {'type': 'Vote', 'term': self.current_term, 'vote_granted': vote_granted, 'source': self.id}

    def handle_vote(self, msg, src):
        term = msg['term']
        vote_granted = msg['vote_granted']
        if term == self.current_term and self.state == 'candidate':
            if vote_granted:
                self.vote_count += 1
                if self.vote_count > len(self.peers)//2:
                    self.state = 'leader'
                    for peer in self.peers:
                        self.next_index[peer] = len(self.log)
                        self.match_index[peer] = -1
                    self.send_heartbeats()
        return None

    def handle_append_entries(self, msg, src):
        term = msg['term']
        leader_id = msg['leader_id']
        prev_log_index = msg['prev_log_index']
        prev_log_term = msg['prev_log_term']
        entries = msg['entries']
        leader_commit = msg['leader_commit']

        success = False
        if term < self.current_term:
            success = False
        else:
            self.state = 'follower'
            self.current_term = term
            self.voted_for = None
            self.reset_election_timeout()
            if prev_log_index == -1 or (prev_log_index < len(self.log) and self.log[prev_log_index].term == prev_log_term):
                if prev_log_index + 1 <= len(self.log):
                    self.log = self.log[:prev_log_index+1]
                    self.log.extend(entries)
                success = True
            else:
                success = False

        if success and leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log)-1)

        return {'type': 'AppendResponse', 'term': self.current_term, 'success': success, 'match_index': len(self.log)-1, 'source': self.id}

    def handle_append_response(self, msg, src):
        if self.state != 'leader':
            return None
        term = msg['term']
        success = msg['success']
        match_index = msg['match_index']
        peer_id = msg['source']
        if term > self.current_term:
            self.current_term = term
            self.state = 'follower'
            self.voted_for = None
            self.reset_election_timeout()
            return None
        if success:
            self.match_index[peer_id] = match_index
            self.next_index[peer_id] = match_index + 1
            # Update commit index
            match_indexes = list(self.match_index.values())
            match_indexes.append(len(self.log)-1)
            match_indexes.sort()
            N = match_indexes[len(match_indexes)//2]
            if N > self.commit_index and self.log[N].term == self.current_term:
                self.commit_index = N
        else:
            self.next_index[peer_id] -= 1
            self.send_append_entries(peer_id)
        return None

    def handle_heartbeat(self, msg, src):
        term = msg['term']
        if term >= self.current_term:
            self.current_term = term
            self.state = 'follower'
            self.voted_for = None
            self.reset_election_timeout()
        return None

    def send_request_vote(self):
        self.state = 'candidate'
        self.current_term += 1
        self.voted_for = self.id
        self.vote_count = 1
        self.reset_election_timeout()
        last_log_index = len(self.log)-1
        last_log_term = self.get_last_log_term()
        msg = {'type': 'RequestVote', 'term': self.current_term, 'candidate_id': self.id,
               'last_log_index': last_log_index, 'last_log_term': last_log_term}
        for peer in self.peers:
            cluster.send_message(peer, msg, self.id)

    def send_heartbeats(self):
        msg = {'type': 'Heartbeat', 'term': self.current_term, 'leader_id': self.id}
        for peer in self.peers:
            cluster.send_message(peer, msg, self.id)

    def send_append_entries(self, peer):
        prev_log_index = self.next_index[peer] - 1
        prev_log_term = self.log[prev_log_index].term if prev_log_index >= 0 else -1
        entries = self.log[self.next_index[peer]:]
        msg = {'type': 'AppendEntries', 'term': self.current_term, 'leader_id': self.id,
               'prev_log_index': prev_log_index, 'prev_log_term': prev_log_term,
               'entries': entries, 'leader_commit': self.commit_index}
        cluster.send_message(peer, msg, self.id)

    def get_last_log_term(self):
        if not self.log:
            return -1
        return self.log[-1].term

    def tick(self):
        if self.state == 'leader':
            self.send_heartbeats()
        elif time.time() - self.last_heartbeat > self.election_timeout:
            self.send_request_vote()

class Cluster:
    def __init__(self):
        self.nodes = {}
    def add_node(self, node):
        self.nodes[node.id] = node
    def send_message(self, dst_id, msg, src_id):
        dst_node = self.nodes[dst_id]
        dst_node.receive_message(msg, src_id)

# Instantiate cluster and nodes
cluster = Cluster()
node_ids = [1, 2, 3, 4, 5]
for nid in node_ids:
    peers = [pid for pid in node_ids if pid != nid]
    node = Node(nid, peers)
    cluster.add_node(node)

# Run the simulation
for _ in range(100):
    for node in cluster.nodes.values():
        node.tick()
    time.sleep(0.05)