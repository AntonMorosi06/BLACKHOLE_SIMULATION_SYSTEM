"""
Particle Model
--------------

This module defines the particle entity used throughout the simulation.

A particle represents the smallest active unit in the system. Each particle
is influenced by the central black hole and evolves over time according to
the simulation step logic implemented in the engine layer.

The particle model is intentionally lightweight, but it stores enough state
to support:

- motion in 2D space
- acceleration and velocity updates
- rendering
- trail visualization
- lifetime tracking
- absorption handling
- basic runtime statistics
"""

from dataclasses import dataclass, field
from typing import List, Tuple
import math


@dataclass
class Particle:
    """
    Simulation particle entity.

    Parameters
    ----------
    x, y :
        Current particle position in simulation coordinates.

    vx, vy :
        Current particle velocity components.

    ax, ay :
        Current particle acceleration components.
        These are updated by the simulation engine.

    mass :
        Simulation mass of the particle.
        In the current system this is mostly used as an internal property
        rather than as a driver of pairwise interactions.

    radius :
        Rendering radius used when drawing the particle.

    color :
        RGB color used for rendering.

    alive :
        Indicates whether the particle is still active in the simulation.
        Once absorbed or deactivated, the particle should no longer be updated.

    trail :
        Stores recent particle positions for rendering motion history.

    age :
        Counts how long the particle has existed in simulation steps.

    distance_traveled :
        Accumulates total path length traveled during the particle lifetime.

    min_approach :
        Stores the minimum distance reached relative to the black hole center.
        Useful for diagnostics and statistics.
    """

    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0
    ax: float = 0.0
    ay: float = 0.0
    mass: float = 1.0
    radius: int = 2
    color: Tuple[int, int, int] = (255, 255, 255)
    alive: bool = True
    trail: List[Tuple[float, float]] = field(default_factory=list)
    age: int = 0
    distance_traveled: float = 0.0
    min_approach: float = float("inf")

    def kill(self) -> None:
        """
        Mark the particle as inactive.

        This method is used when the particle is considered absorbed
        by the black hole or otherwise removed from the active simulation.

        The method does not delete the object. It only changes its runtime
        state so that higher-level systems can stop updating it while still
        retaining possible historical information.
        """
        self.alive = False

    def tick_age(self) -> None:
        """
        Advance the lifetime counter by one simulation step.

        This is used by the main simulation loop to keep track of how long
        a particle has survived inside the system.
        """
        self.age += 1

    def speed(self) -> float:
        """
        Return the current speed magnitude.

        This is a convenience method useful for debugging, metrics,
        and color or visualization logic.
        """
        return math.sqrt(self.vx * self.vx + self.vy * self.vy)

    def reset_acceleration(self) -> None:
        """
        Reset acceleration components to zero.

        This helper is useful if the engine or future extensions require
        an explicit force accumulation phase before computing a new update.
        """
        self.ax = 0.0
        self.ay = 0.0

    def as_tuple(self) -> Tuple[float, float]:
        """
        Return the current position as a tuple.

        This is mainly a convenience helper for rendering and trail logic.
        """
        return (self.x, self.y)
