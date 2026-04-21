"""
Gravity Engine
--------------

This module implements the core physics logic of the simulation.

It is responsible for computing the interaction between each particle
and the central mass (black hole), and updating particle acceleration,
velocity, and position accordingly.

The model used is a simplified central-force system based on an
inverse-square law with a softening factor to ensure numerical stability.
"""

import math

# Import constants from centralized configuration
from src.python.core.constants import G, BLACK_HOLE_MASS, SOFTENING, DELTA_TIME


class GravityEngine:
    """
    Core simulation engine for particle dynamics.

    This class encapsulates the logic required to:
    - compute forces acting on particles
    - update acceleration
    - update velocity
    - update position

    The system assumes:
    - a single central mass
    - no particle-particle interaction
    - 2D space
    """

    def __init__(self, center_x, center_y):
        """
        Initialize the gravity engine.

        Parameters:
        - center_x: x coordinate of the central mass
        - center_y: y coordinate of the central mass
        """
        self.cx = center_x
        self.cy = center_y

    # -----------------------------------------------------------------------
    # FORCE COMPUTATION
    # -----------------------------------------------------------------------

    def compute_force(self, particle):
        """
        Compute acceleration for a single particle.

        This function calculates:
        - displacement from center
        - distance
        - normalized direction
        - force magnitude (with softening)
        - acceleration components

        The result is stored directly in the particle.
        """

        # Displacement from center
        dx = self.cx - particle.x
        dy = self.cy - particle.y

        # Distance from center
        dist_sq = dx * dx + dy * dy
        dist = math.sqrt(dist_sq)

        # Avoid division by zero
        if dist == 0:
            return

        # Normalize direction vector
        nx = dx / dist
        ny = dy / dist

        # Compute force with softening term
        force = G * BLACK_HOLE_MASS / (dist_sq + SOFTENING)

        # Apply acceleration
        particle.ax = nx * force
        particle.ay = ny * force

    # -----------------------------------------------------------------------
    # STATE UPDATE
    # -----------------------------------------------------------------------

    def update_particle(self, particle):
        """
        Update velocity and position of a particle.

        Uses explicit time integration:
        v = v + a * dt
        x = x + v * dt
        """

        # Update velocity
        particle.vx += particle.ax * DELTA_TIME
        particle.vy += particle.ay * DELTA_TIME

        # Update position
        particle.x += particle.vx * DELTA_TIME
        particle.y += particle.vy * DELTA_TIME

    # -----------------------------------------------------------------------
    # MAIN UPDATE LOOP
    # -----------------------------------------------------------------------

    def update(self, particles):
        """
        Update all particles in the system.

        The update is performed in two steps:
        1. Compute forces
        2. Update state

        This separation ensures clarity and avoids mixing logic.
        """

        # Step 1: compute forces
        for particle in particles:
            self.compute_force(particle)

        # Step 2: update positions
        for particle in particles:
            self.update_particle(particle)
