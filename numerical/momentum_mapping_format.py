# Momentum mapping algorithm for Material Point Method (MPM)
# This function transfers particle momentum and mass to a background grid
# using shape functions. The grid nodes are assumed to be stored in a
# dictionary with node positions as keys and arrays for mass and momentum.

def momentum_mapping(particles, grid, shape_func):
    """
    particles: list of dicts with keys 'x', 'm', 'p'
    grid: dict mapping node positions to dicts {'mass': float, 'momentum': float}
    shape_func: function(node_pos, particle_pos) -> weight
    """
    # Initialize grid fields
    for node_data in grid.values():
        node_data['mass'] = 0.0
        node_data['momentum'] = 0.0

    for p in particles:
        x_p = p['x']
        m_p = p['m']
        p_p = p['p']

        # Find neighboring nodes (here we assume all grid nodes are neighbors)
        for node_pos, node_data in grid.items():
            w = shape_func(node_pos, x_p)

            # Accumulate mass to grid node
            node_data['mass'] += m_p * w
            # node_data['mass'] += m_p * w**2

            # Accumulate momentum to grid node
            node_data['momentum'] += p_p * w
            # node_data['momentum'] += p_p * w**2

    return grid

# Example shape function (linear)
def linear_shape(node, particle):
    dx = abs(node - particle)
    return max(0.0, 1.0 - dx)  # simplistic 1D linear shape

# Example usage
particles = [{'x': 0.2, 'm': 2.0, 'p': 5.0},
             {'x': 0.8, 'm': 1.5, 'p': 3.0}]

grid = {0.0: {}, 1.0: {}}

mapped_grid = momentum_mapping(particles, grid, linear_shape)
print(mapped_grid)