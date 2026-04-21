"""
Gravity Engine
--------------

This module contains the core gravitational utility functions used by the
BlackHole Simulation System.

Its responsibility is not to run the full simulation loop. Instead, it
provides the mathematical helpers required by multiple runtime layers,
including:

- distance and direction computation
- simplified gravitational force and acceleration
- speed clamping
- spatial region classification
- orbital and escape velocity estimates
- energy estimates
- accretion-zone intensity estimation
- tangential vector construction for orbital-like spawn behavior

The functions defined here are intentionally lightweight and reusable.
They are designed to support both the simulation engine and the rendering
layer without duplicating central-force logic across the codebase.
"""

import math
from typing import Tuple

from src.python.core.constants import (
    EPSILON,
    REGION_EVENT_HORIZON,
    REGION_ACCRETION_ZONE,
    REGION_OUTER_FIELD,
)
from src.python.core.vector_utils import clamp, normalize


# ═══════════════════════════════════════════════════════════
#  DISTANCE AND DIRECTION
# ═══════════════════════════════════════════════════════════

def compute_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Compute the Euclidean distance between two points.

    Parameters
    ----------
    x1, y1 :
        Coordinates of the first point.
    x2, y2 :
        Coordinates of the second point.

    Returns
    -------
    float
        Euclidean distance between the two points.
    """
    return math.hypot(x2 - x1, y2 - y1)


def compute_distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Compute the squared Euclidean distance between two points.

    Notes
    -----
    This helper avoids the square root operation and is useful when only
    relative distance comparison is required.
    """
    dx = x2 - x1
    dy = y2 - y1
    return dx * dx + dy * dy


def compute_direction_vector(
    x1: float, y1: float, x2: float, y2: float,
) -> Tuple[float, float]:
    """
    Compute the normalized direction vector from point (x1, y1) to point (x2, y2).

    Returns
    -------
    Tuple[float, float]
        Unit direction vector.

    Notes
    -----
    The actual normalization is delegated to core.vector_utils.normalize(...)
    so that near-zero behavior remains consistent across the project.
    """
    return normalize(x2 - x1, y2 - y1)


# ═══════════════════════════════════════════════════════════
#  FORCE AND ACCELERATION
# ═══════════════════════════════════════════════════════════

def compute_gravitational_force(
    distance: float,
    black_hole_mass: float,
    gravity_constant: float,
    softening: float,
) -> float:
    """
    Compute the scalar magnitude of the simplified gravitational force.

    Model
    -----
    F = G * M / (r² + softening)

    Notes
    -----
    This is a simulation-oriented central-force model, not a full physical
    black hole formulation. The softening term is used to avoid divergence
    when distance becomes very small.
    """
    return gravity_constant * black_hole_mass / (distance * distance + softening)


def compute_gravitational_acceleration(
    px: float, py: float,
    bx: float, by: float,
    black_hole_mass: float,
    gravity_constant: float,
    softening: float,
) -> Tuple[float, float]:
    """
    Compute the gravitational acceleration applied by the black hole to a particle.

    Parameters
    ----------
    px, py :
        Particle coordinates.
    bx, by :
        Black hole coordinates.
    black_hole_mass :
        Effective simulation mass of the black hole.
    gravity_constant :
        Scaled simulation gravitational constant.
    softening :
        Numerical softening factor used to stabilize force near the center.

    Returns
    -------
    Tuple[float, float]
        Acceleration components (ax, ay).
    """
    dx = bx - px
    dy = by - py
    dist_sq = dx * dx + dy * dy
    dist = math.sqrt(dist_sq)

    if dist < EPSILON:
        return 0.0, 0.0

    force = gravity_constant * black_hole_mass / (dist_sq + softening)
    inv_dist = 1.0 / dist
    return dx * inv_dist * force, dy * inv_dist * force


# ═══════════════════════════════════════════════════════════
#  SPEED CLAMPING
# ═══════════════════════════════════════════════════════════

def clamp_speed(vx: float, vy: float, max_speed: float) -> Tuple[float, float]:
    """
    Clamp a velocity vector to the configured maximum speed.

    Parameters
    ----------
    vx, vy :
        Velocity components.
    max_speed :
        Maximum allowed speed magnitude.

    Returns
    -------
    Tuple[float, float]
        Possibly rescaled velocity vector.

    Notes
    -----
    This helper preserves direction and only rescales magnitude when needed.
    """
    speed_sq = vx * vx + vy * vy
    if speed_sq <= max_speed * max_speed:
        return vx, vy

    speed = math.sqrt(speed_sq)
    if speed < EPSILON:
        return vx, vy

    scale = max_speed / speed
    return vx * scale, vy * scale


# ═══════════════════════════════════════════════════════════
#  REGION CLASSIFICATION
# ═══════════════════════════════════════════════════════════

def classify_region(
    px: float, py: float,
    bx: float, by: float,
    event_horizon_radius: float,
    accretion_radius: float,
) -> str:
    """
    Classify a particle position relative to the black hole.

    Returns one of:
    - REGION_EVENT_HORIZON
    - REGION_ACCRETION_ZONE
    - REGION_OUTER_FIELD

    Notes
    -----
    This function works directly from coordinates and is useful when the
    particle distance has not been computed yet.
    """
    dist_sq = compute_distance_squared(px, py, bx, by)

    if dist_sq <= event_horizon_radius * event_horizon_radius:
        return REGION_EVENT_HORIZON
    if dist_sq <= accretion_radius * accretion_radius:
        return REGION_ACCRETION_ZONE
    return REGION_OUTER_FIELD


def classify_region_from_distance(
    distance: float,
    event_horizon_radius: float,
    accretion_radius: float,
) -> str:
    """
    Classify a particle region using a precomputed distance.

    Notes
    -----
    This helper avoids recomputing geometry when the scalar distance is already
    available, which is useful in both simulation and rendering paths.
    """
    if distance <= event_horizon_radius:
        return REGION_EVENT_HORIZON
    if distance <= accretion_radius:
        return REGION_ACCRETION_ZONE
    return REGION_OUTER_FIELD


# ═══════════════════════════════════════════════════════════
#  ORBITAL AND ESCAPE VELOCITIES
# ═══════════════════════════════════════════════════════════

def estimate_orbital_velocity(
    distance: float, gravity_constant: float, black_hole_mass: float,
) -> float:
    """
    Estimate the circular orbital velocity.

    Model
    -----
    v = sqrt(G * M / r)

    Notes
    -----
    This is used as a simulation-oriented estimate and is especially useful
    for controlled spawning of particles in orbit-like configurations.
    """
    if distance <= EPSILON:
        return 0.0
    return math.sqrt(gravity_constant * black_hole_mass / distance)


def compute_escape_velocity(
    distance: float, gravity_constant: float, black_hole_mass: float,
) -> float:
    """
    Estimate the escape velocity.

    Model
    -----
    v = sqrt(2 * G * M / r)

    Notes
    -----
    This is a simplified scalar estimate, suitable for diagnostics and spawn
    logic rather than full physical interpretation.
    """
    if distance <= EPSILON:
        return 0.0
    return math.sqrt(2.0 * gravity_constant * black_hole_mass / distance)


# ═══════════════════════════════════════════════════════════
#  ENERGY ESTIMATES
# ═══════════════════════════════════════════════════════════

def compute_kinetic_energy(mass: float, vx: float, vy: float) -> float:
    """
    Compute the classical kinetic energy of a particle.

    Model
    -----
    K = 1/2 * m * v²
    """
    return 0.5 * mass * (vx * vx + vy * vy)


def compute_potential(
    distance: float, gravity_constant: float, black_hole_mass: float,
) -> float:
    """
    Compute the simplified gravitational potential term.

    Model
    -----
    U = -G * M / r

    Notes
    -----
    The distance is clamped from below using EPSILON to avoid division by zero.
    """
    distance = max(distance, EPSILON)
    return -gravity_constant * black_hole_mass / distance


def compute_total_energy(
    particle_mass: float, distance: float,
    gravity_constant: float, black_hole_mass: float,
    vx: float, vy: float,
) -> float:
    """
    Compute the total simplified mechanical energy of a particle.

    Returns
    -------
    float
        Total energy = kinetic + potential contribution.
    """
    kinetic = compute_kinetic_energy(particle_mass, vx, vy)
    potential = particle_mass * compute_potential(distance, gravity_constant, black_hole_mass)
    return kinetic + potential


# ═══════════════════════════════════════════════════════════
#  VISUAL / ACCRETION HELPERS
# ═══════════════════════════════════════════════════════════

def compute_accretion_intensity(
    distance: float,
    event_horizon_radius: float,
    accretion_radius: float,
) -> float:
    """
    Compute a normalized intensity value inside the accretion region.

    Returns
    -------
    float
        Value in [0.0, 1.0], where:
        - 0.0 means outside the accretion zone
        - 1.0 means at or inside the event horizon boundary

    Notes
    -----
    This helper is primarily used as a visual modulation factor rather than
    as a physical quantity.
    """
    if distance <= event_horizon_radius:
        return 1.0
    if distance > accretion_radius:
        return 0.0

    span = max(accretion_radius - event_horizon_radius, EPSILON)
    return clamp(1.0 - (distance - event_horizon_radius) / span, 0.0, 1.0)


# ═══════════════════════════════════════════════════════════
#  TANGENTIAL HELPERS
# ═══════════════════════════════════════════════════════════

def compute_tangential_vector(
    px: float, py: float, bx: float, by: float,
    clockwise: bool = True,
) -> Tuple[float, float]:
    """
    Compute a unit tangential vector around the black hole center.

    Parameters
    ----------
    px, py :
        Particle or point coordinates.
    bx, by :
        Black hole center coordinates.
    clockwise :
        If True, return clockwise tangential direction.
        Otherwise return counterclockwise tangential direction.

    Returns
    -------
    Tuple[float, float]
        Tangential unit vector.

    Notes
    -----
    This helper is especially useful for orbital spawn initialization and
    other visual or motion setups requiring a perpendicular direction.
    """
    nx, ny = normalize(bx - px, by - py)

    if abs(nx) < EPSILON and abs(ny) < EPSILON:
        return 0.0, 0.0

    if clockwise:
        return -ny, nx
    return ny, -nx
