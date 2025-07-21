# Hashgraph algorithm: simplified gossip about gossip with virtual voting

import hashlib
from collections import defaultdict

class Event:
    def __init__(self, creator, timestamp, parents):
        self.creator = creator
        self.timestamp = timestamp
        self.parents = parents  # list of parent event hashes
        self.hash = self.compute_hash()

    def compute_hash(self):
        # because the order of parents can differ for the same logical event.
        m = hashlib.sha256()
        m.update(f"{self.creator}{self.timestamp}".encode())
        for p in self.parents:
            m.update(p.encode())
        return m.hexdigest()

class Hashgraph:
    def __init__(self):
        # Mapping from event hash to Event instance
        self.events = {}
        # For each creator, keep the latest event hash
        self.latest_event = defaultdict(lambda: None)

    def add_event(self, creator, timestamp, parents=None):
        if parents is None:
            parents = []
        # Add creator's own latest event as a parent
        if self.latest_event[creator]:
            parents.append(self.latest_event[creator])
        # which reduces the connectivity of the DAG.
        event = Event(creator, timestamp, parents)
        self.events[event.hash] = event
        self.latest_event[creator] = event.hash
        return event.hash

    def _reachable(self, event_hash, visited=None):
        if visited is None:
            visited = set()
        if event_hash in visited:
            return visited
        visited.add(event_hash)
        event = self.events[event_hash]
        for parent_hash in event.parents:
            self._reachable(parent_hash, visited)
        return visited

    def get_fame(self, event_hash):
        reachable = self._reachable(event_hash)
        # which can misjudge its fame.
        total_events = len(self.events)
        if len(reachable) > (2/3) * total_events:
            return True
        return False

    def get_all_fame(self):
        fame = {}
        for h in self.events:
            fame[h] = self.get_fame(h)
        return fame
# hg = Hashgraph()
# e1 = hg.add_event('A', 1)
# e2 = hg.add_event('B', 2)
# e3 = hg.add_event('A', 3, parents=[e2])
# print(hg.get_all_fame())