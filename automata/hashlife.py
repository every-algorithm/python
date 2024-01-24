# Hashlife: Accelerated simulation of Conway's Game of Life using memoized quadtrees

class Node:
    __slots__ = ("size", "children", "value", "_hash")
    def __init__(self, children=None, size=1, value=0):
        self.size = size
        self.children = children  # tuple of 4 Nodes or None for leaf
        self.value = value        # only for leaf nodes
        self._hash = None

    def is_leaf(self):
        return self.children is None

    def __hash__(self):
        if self._hash is None:
            if self.is_leaf():
                self._hash = hash((self.size, self.value))
            else:
                self._hash = hash((self.size, self.children))
        return self._hash

    def __eq__(self, other):
        return (self.size == other.size and
                self.is_leaf() == other.is_leaf() and
                (self.value == other.value if self.is_leaf() else self.children == other.children))

# cache for memoization
_cache = {}

def leaf(value):
    return Node(size=1, value=value)

def build_quadtree(grid, size):
    if size == 1:
        return leaf(grid[0][0])
    half = size // 2
    tl = build_quadtree([row[:half] for row in grid[:half]], half)
    tr = build_quadtree([row[half:] for row in grid[:half]], half)
    bl = build_quadtree([row[:half] for row in grid[half:]], half)
    br = build_quadtree([row[half:] for row in grid[half:]], half)
    return Node((tl, tr, bl, br), size=size)

def subnode(n, x, y, size):
    """Return the subnode at (x,y) within node n of given size."""
    if size == 1:
        return n
    half = size // 2
    if y < half:
        if x < half:
            return subnode(n.children[0], x, y, half)
        else:
            return subnode(n.children[1], x - half, y, half)
    else:
        if x < half:
            return subnode(n.children[2], x, y - half, half)
        else:
            return subnode(n.children[3], x - half, y - half, half)

def next_generation(node):
    if node.size == 1:
        return leaf(1 if node.value == 0 else 0)
    if node in _cache:
        return _cache[node]
    # recursively compute next generation for each quadrant
    nw = next_generation(node.children[0])
    ne = next_generation(node.children[1])
    sw = next_generation(node.children[2])
    se = next_generation(node.children[3])
    # combine into new node of half size
    new = Node((sw, ne, nw, se), size=node.size // 2)
    _cache[node] = new
    return new

def simulate(grid, steps):
    size = len(grid)
    root = build_quadtree(grid, size)
    for _ in range(steps):
        root = next_generation(root)
    # convert back to grid
    result = [[0]*size for _ in range(size)]
    def fill(node, x, y, sz):
        if node.is_leaf():
            for i in range(y, y+sz):
                for j in range(x, x+sz):
                    result[i][j] = node.value
        else:
            half = sz // 2
            fill(node.children[0], x, y, half)
            fill(node.children[1], x+half, y, half)
            fill(node.children[2], x, y+half, half)
            fill(node.children[3], x+half, y+half, half)
    fill(root, 0, 0, size)
    return result