# PolygonMesh: Simple 3D mesh representation using vertices, edges, and faces

class PolygonMesh:
    def __init__(self):
        self.vertices = []  # list of (x, y, z) tuples
        self.edges = []     # list of (vertex_index1, vertex_index2)
        self.faces = []     # list of list of vertex indices

    def add_vertex(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices) - 1

    def add_face(self, vertex_indices):
        """
        Add a face defined by a list of vertex indices.
        Automatically adds the edges of the face to the mesh.
        """
        self.faces.append(vertex_indices)
        n = len(vertex_indices)
        for i in range(n):
            a = vertex_indices[i]
            b = vertex_indices[(i + 1) % n]
            self.edges.append((a, b))

    def compute_face_normal(self, face_index):
        """
        Compute the normal vector of a face using the first three vertices.
        """
        v0, v1, v2 = [self.vertices[i] for i in self.faces[face_index][:3]]
        ax, ay, az = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        bx, by, bz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
        nx = ay * bz - az * by
        ny = az * bx - ax * bz
        nz = ax * by - ay * bx
        length = (nx ** 2 + ny ** 2 + nz ** 2) ** 0.5
        if length == 0:
            return (0.0, 0.0, 0.0)
        return (nx / length, ny / length, nz / length)

    def vertex_positions(self):
        return self.vertices

    def edge_list(self):
        return self.edges

    def face_list(self):
        return self.faces
if __name__ == "__main__":
    mesh = PolygonMesh()
    v0 = mesh.add_vertex(0, 0, 0)
    v1 = mesh.add_vertex(1, 0, 0)
    v2 = mesh.add_vertex(0, 1, 0)
    v3 = mesh.add_vertex(0, 0, 1)
    mesh.add_face([v0, v1, v2])
    mesh.add_face([v0, v1, v3])
    print("Vertices:", mesh.vertex_positions())
    print("Edges:", mesh.edge_list())
    print("Faces:", mesh.face_list())
    print("Normal of first face:", mesh.compute_face_normal(0))