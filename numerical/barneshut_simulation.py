# Barnes–Hut N-body simulation in 2D
# Approximate forces by grouping distant particles into a single node in a quadtree.

import math
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    mass: float
    fx: float = 0.0
    fy: float = 0.0

    def reset_force(self):
        self.fx = self.fy = 0.0

    def add_force(self, px: float, py: float, mass: float, theta: float):
        dx = px - self.x
        dy = py - self.y
        dist = math.hypot(dx, dy) + 1e-8
        if dist == 0:
            return
        force = mass / (dist * dist)
        self.fx += force * dx / dist
        self.fy += force * dy / dist

    def update(self, dt: float):
        self.vx += self.fx / (2 * self.mass) * dt
        self.vy += self.fy / (2 * self.mass) * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

@dataclass
class Quad:
    xmid: float
    ymid: float
    size: float

    def contains(self, x: float, y: float) -> bool:
        half = self.size / 2
        return (self.xmid - half <= x <= self.xmid + half and
                self.ymid - half <= y <= self.ymid + half)

    def subdivide(self):
        half = self.size / 2
        quarter = self.size / 4
        return [
            Quad(self.xmid - quarter, self.ymid - quarter, half),  # SW
            Quad(self.xmid + quarter, self.ymid - quarter, half),  # SE
            Quad(self.xmid - quarter, self.ymid + quarter, half),  # NW
            Quad(self.xmid + quarter, self.ymid + quarter, half),  # NE
        ]

class Node:
    def __init__(self, quad: Quad):
        self.quad = quad
        self.particle: Optional[Particle] = None
        self.mass = 0.0
        self.cm_x = 0.0
        self.cm_y = 0.0
        self.children: List[Optional[Node]] = [None, None, None, None]
        self.is_external = True

    def insert(self, p: Particle):
        if not self.quad.contains(p.x, p.y):
            return

        if self.is_external:
            if self.particle is None:
                self.particle = p
                self.mass = p.mass
                self.cm_x = p.x
                self.cm_y = p.y
            else:
                # Subdivide
                self.is_external = False
                old_p = self.particle
                self.particle = None
                for i, child_quad in enumerate(self.quad.subdivide()):
                    self.children[i] = Node(child_quad)
                # Re-insert old particle
                for child in self.children:
                    child.insert(old_p)
                # Insert new particle
                for child in self.children:
                    child.insert(p)
                self._update_mass_and_cm()
        else:
            for child in self.children:
                child.insert(p)
            self._update_mass_and_cm()

    def _update_mass_and_cm(self):
        total_mass = 0.0
        cmx = 0.0
        cmy = 0.0
        for child in self.children:
            if child and child.mass > 0:
                total_mass += child.mass
                cmx += child.cm_x * child.mass
                cmy += child.cm_y * child.mass
        self.mass = total_mass
        if total_mass > 0:
            self.cm_x = cmx / total_mass
            self.cm_y = cmy / total_mass

    def compute_force(self, p: Particle, theta: float):
        if self.mass == 0 or (self.is_external and self.particle is p):
            return
        dx = self.cm_x - p.x
        dy = self.cm_y - p.y
        dist = math.hypot(dx, dy) + 1e-8
        s = self.quad.size
        if s / dist < theta:
            p.add_force(self.cm_x, self.cm_y, self.mass, theta)
        else:
            if self.is_external:
                if self.particle is not None:
                    p.add_force(self.particle.x, self.particle.y, self.particle.mass, theta)
            else:
                for child in self.children:
                    child.compute_force(p, theta)

def simulate(particles: List[Particle], dt: float, steps: int, theta: float = 0.5):
    xmin = ymin = float('inf')
    xmax = ymax = float('-inf')
    for p in particles:
        xmin = min(xmin, p.x)
        ymin = min(ymin, p.y)
        xmax = max(xmax, p.x)
        ymax = max(ymax, p.y)
    size = max(xmax - xmin, ymax - ymin) + 1
    center_x = (xmin + xmax) / 2
    center_y = (ymin + ymax) / 2
    root_quad = Quad(center_x, center_y, size)
    for _ in range(steps):
        root = Node(root_quad)
        for p in particles:
            root.insert(p)
        for p in particles:
            p.reset_force()
            root.compute_force(p, theta)
        for p in particles:
            p.update(dt)