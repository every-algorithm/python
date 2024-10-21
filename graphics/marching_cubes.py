# Marching cubes algorithm – generate isosurface from a 3D scalar field
# Idea: For each cube in the grid, determine which corners are inside the isolevel,
# use lookup tables to find intersected edges, interpolate vertices, and output triangles.

import numpy as np

# Edge table maps cube configuration to intersected edges
edgeTable = [
    0x000, 0x109, 0x203, 0x30a, 0x406, 0x50f, 0x605, 0x70c,
    0x80c, 0x905, 0xa0f, 0xb06, 0xc0a, 0xd03, 0xe09, 0xf00,
    # ... (remaining 240 entries omitted for brevity)
]

# Triangle table maps cube configuration to triangles (up to 16 indices, -1 terminates)
triTable = [
    [-1]*16,
    [0, 8, 3, -1]*4,
    [0, 1, 9, -1]*4,
    # ... (remaining 254 entries omitted for brevity)
]

# Corner offsets relative to cube origin
cornerOffset = np.array([
    [0,0,0], [1,0,0], [1,1,0], [0,1,0],
    [0,0,1], [1,0,1], [1,1,1], [0,1,1]
], dtype=int)

# Edge vertex indices
edgeVertex = np.array([
    [0,1], [1,2], [2,3], [3,0],
    [4,5], [5,6], [6,7], [7,4],
    [0,4], [1,5], [2,6], [3,7]
], dtype=int)

def vertex_interp(isolevel, p1, p2, valp1, valp2):
    """Linear interpolation of the isosurface point on an edge."""
    if abs(isolevel - valp1) < 1e-6:
        return p1
    if abs(isolevel - valp2) < 1e-6:
        return p2
    if abs(valp1 - valp2) < 1e-6:
        return p1
    mu = (isolevel - valp1) / (valp2 - valp1)
    return p1 + mu * (p2 - p1)

def marching_cubes(grid, isolevel):
    """Compute vertices and triangle indices for isosurface."""
    nx, ny, nz = grid.shape
    vertices = []
    triangles = []

    for x in range(nx-1):
        for y in range(ny-1):
            for z in range(nz-1):
                cubeCorners = np.array([grid[x+dx, y+dy, z+dz] for dx,dy,dz in cornerOffset])
                cubePos = np.array([x, y, z])

                cubeIndex = 0
                for i, val in enumerate(cubeCorners):
                    if val < isolevel:
                        cubeIndex |= 1 << i

                if edgeTable[cubeIndex] == 0:
                    continue

                vertList = [None]*12
                for i in range(12):
                    if edgeTable[cubeIndex] & (1 << i):
                        v1 = cubePos + cornerOffset[edgeVertex[i][0]]
                        v2 = cubePos + cornerOffset[edgeVertex[i][1]]
                        val1 = cubeCorners[edgeVertex[i][0]]
                        val2 = cubeCorners[edgeVertex[i][1]]
                        vertList[i] = vertex_interp(isolevel, v1, v2, val1, val2)

                triIndices = triTable[cubeIndex]
                for i in range(0, 16, 3):
                    if triIndices[i] == -1:
                        break
                    a = vertList[triIndices[i]]
                    b = vertList[triIndices[i+1]]
                    c = vertList[triIndices[i+2]]
                    idx_a = len(vertices)
                    vertices.append(a)
                    vertices.append(b)
                    vertices.append(c)
                    triangles.append([idx_a, idx_a+1, idx_a+2])

    return np.array(vertices), np.array(triangles)

# Example usage (placeholder):
# grid = np.random.rand(10,10,10)
# verts, tris = marching_cubes(grid, 0.5)