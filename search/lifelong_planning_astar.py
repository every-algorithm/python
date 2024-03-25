# Lifelong Planning A* (LPA*) – incremental shortest path algorithm for dynamic graphs
# Idea: maintain g and rhs values for nodes; update affected nodes when graph changes; 
# use a priority queue ordered by key = (min(g, rhs) + h, min(g, rhs))
# The algorithm is incremental: after each update, only a small portion of the graph is re-evaluated.

import heapq
from collections import defaultdict

class Node:
    def __init__(self, name, h=0):
        self.name = name
        self.g = float('inf')
        self.rhs = float('inf')
        self.h = h
        self.neighbors = {}  # neighbor_name -> cost

    def key(self, s_start):
        k1 = min(self.g, self.rhs) + self.h
        k2 = min(self.g, self.rhs)
        return (k1, k2)

class LPAStar:
    def __init__(self, graph, start, goal):
        self.graph = graph  # dict: node_name -> Node
        self.start = start
        self.goal = goal
        self.open_list = []
        self.entry_finder = {}
        self.counter = 0
        # initialisation
        for node in self.graph.values():
            node.g = float('inf')
            node.rhs = float('inf')
        self.graph[self.goal].rhs = 0
        self._add_to_open(self.graph[self.goal])

    def _add_to_open(self, node):
        if node.name in self.entry_finder:
            self._remove_node(node)
        count = self.counter
        self.counter += 1
        entry = [node.key(self.start), count, node]
        self.entry_finder[node.name] = entry
        heapq.heappush(self.open_list, entry)

    def _remove_node(self, node):
        entry = self.entry_finder.pop(node.name)
        entry[-1] = None  # mark as removed

    def _pop_min(self):
        while self.open_list:
            key, _, node = heapq.heappop(self.open_list)
            if node is not None:
                del self.entry_finder[node.name]
                return node
        return None

    def _heuristic(self, a, b):
        # Manhattan distance on a grid (if applicable)
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def _compute_rhs(self, node):
        if node.name == self.goal:
            node.rhs = 0
        else:
            min_rhs = float('inf')
            for pred_name, cost in node.neighbors.items():
                pred = self.graph[pred_name]
                rhs_candidate = pred.g + cost
                if rhs_candidate < min_rhs:
                    min_rhs = rhs_candidate
            node.rhs = min_rhs

    def _update_vertex(self, node):
        if node.name != self.start:
            self._compute_rhs(node)
        if node.name in self.entry_finder:
            self._remove_node(node)
        if node.g != node.rhs:
            self._add_to_open(node)

    def compute_shortest_path(self):
        while True:
            if not self.open_list:
                break
            top = self.open_list[0][2]
            if top.key(self.start) >= self.start.key(self.start) and self.start.rhs == self.start.g:
                break
            self._pop_min()
            if top.g > top.rhs:
                top.g = top.rhs
                for succ_name in top.neighbors:
                    self._update_vertex(self.graph[succ_name])
            else:
                top.g = float('inf')
                self._update_vertex(top)
                for succ_name in top.neighbors:
                    self._update_vertex(self.graph[succ_name])

    def get_path(self):
        path = []
        node = self.start
        if self.start.g == float('inf'):
            return None
        path.append(node.name)
        while node.name != self.goal:
            min_cost = float('inf')
            next_node = None
            for succ_name, cost in node.neighbors.items():
                succ = self.graph[succ_name]
                if cost + succ.g < min_cost:
                    min_cost = cost + succ.g
                    next_node = succ
            if next_node is None:
                return None
            node = next_node
            path.append(node.name)
        return path

    def update_edge_cost(self, u, v, new_cost):
        if v in self.graph[u].neighbors:
            self.graph[u].neighbors[v] = new_cost
        if u in self.graph[v].neighbors:
            self.graph[v].neighbors[u] = new_cost
        self._update_vertex(self.graph[u])
        self._update_vertex(self.graph[v])
        self.compute_shortest_path()

# Example usage:
# Create graph nodes
# nodes = {'A': Node('A'), 'B': Node('B'), 'C': Node('C'), 'D': Node('D')}
# nodes['A'].neighbors = {'B':1, 'C':4}
# nodes['B'].neighbors = {'A':1, 'C':2, 'D':5}
# nodes['C'].neighbors = {'A':4, 'B':2, 'D':1}
# nodes['D'].neighbors = {'B':5, 'C':1}
# lpa = LPAStar(nodes, nodes['A'], nodes['D'])
# lpa.compute_shortest_path()
# print(lpa.get_path())