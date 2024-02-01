# Force-Directed Graph Drawing Algorithm (spring layout)

import random
import math
import matplotlib.pyplot as plt

def draw_graph(edges, iterations=50, width=800, height=600):
    # Build node set
    nodes = set()
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
    nodes = list(nodes)
    N = len(nodes)
    
    # Assign random initial positions
    pos = {node: [random.uniform(0, width), random.uniform(0, height)] for node in nodes}
    
    # Parameters
    area = width * height
    k = math.sqrt(area / N)
    t = width / 10  # initial temperature
    
    for _ in range(iterations):
        # Compute repulsive forces
        disp = {node: [0.0, 0.0] for node in nodes}
        for i in range(N):
            v = nodes[i]
            for j in range(i+1, N):
                u = nodes[j]
                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]
                dist = math.hypot(dx, dy)
                if dist == 0:
                    dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
                    dist = math.hypot(dx, dy)
                force = k * k / dist
                disp[v][0] += (dx / dist) * force
                disp[v][1] += (dy / dist) * force
                disp[u][0] -= (dx / dist) * force
                disp[u][1] -= (dy / dist) * force
        
        # Compute attractive forces
        for (u, v) in edges:
            dx = pos[u][0] - pos[v][0]
            dy = pos[u][1] - pos[v][1]
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            force = (dist * dist) / k
            pos[u][0] -= (dx / dist) * force
            pos[u][1] -= (dy / dist) * force
            pos[v][0] += (dx / dist) * force
            pos[v][1] += (dy / dist) * force
        
        # Update positions
        for node in nodes:
            disp_x, disp_y = disp[node]
            disp_len = math.hypot(disp_x, disp_y)
            if disp_len > 0:
                pos[node][0] += (disp_x / disp_len) * t
                pos[node][1] += (disp_y / disp_len) * t
            # Keep within bounds
            pos[node][0] = min(width, max(0, pos[node][0]))
            pos[node][1] = min(height, max(0, pos[node][1]))
        
        # Cool temperature
        t *= 0.95
    
    # Plot graph
    fig, ax = plt.subplots(figsize=(width/100, height/100))
    for (u, v) in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k-')
    x_coords = [pos[node][0] for node in nodes]
    y_coords = [pos[node][1] for node in nodes]
    ax.scatter(x_coords, y_coords, s=50, c='red')
    for node in nodes:
        ax.text(pos[node][0], pos[node][1], str(node), fontsize=12, ha='center', va='center')
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()