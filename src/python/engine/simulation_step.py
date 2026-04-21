"""
Simulation Step
---------------

This module contains the per-particle update logic used by the main simulation.

Its role is intentionally narrow and well-defined:

- compute the force acting on a particle from the central black hole
- update acceleration
- update velocity
- apply damping and speed limits
- update position
- maintain visual trail history
- detect whether the particle has been absorbed

The purpose of keeping this logic isolated in a dedicated module is to ensure
that the main simulation loop remains readable while the physical update
pipeline stays centralized and reusable.
"""

import math


def update_particle(particle, black_hole, gravity_constant, softening, damping, max_speed, dt, trail_length):
    """
    Update a single particle for one simulation step.

    Parameters
    ----------
    particle :
        The particle instance to update.
    black_hole :
        The central black hole object. Expected to provide position and
        characteristic radii such as the event horizon.
    gravity_constant :
        Scaled gravitational constant used by the simulation.
    softening :
        Numerical softening term used to avoid instability near the center.
    damping :
        Multiplicative damping factor applied to velocity after force update.
    max_speed :
        Maximum allowed particle speed.
    dt :
        Time step used for this simulation update.
    trail_length :
        Maximum number of trail points stored for visual rendering.

    Returns
    -------
    dict
        A dictionary describing the result of the update. The expected keys are:
        - "absorbed": boolean flag indicating whether the particle crossed
          the absorption threshold
        - "distance": last computed distance from the black hole center

    Notes
    -----
    This function is intentionally simple and focused. It does not manage:
    - particle spawning
    - rendering
    - notifications
    - statistics aggregation

    Those concerns remain in higher-level modules.
    """

    # Skip all computations if the particle is already inactive.
    if not particle.alive:
        return {
            "absorbed": False,
            "distance": None,
        }

    # -----------------------------------------------------------------------
    # DISPLACEMENT AND DISTANCE
    # -----------------------------------------------------------------------

    # Compute displacement from particle to black hole center.
    dx = black_hole.x - particle.x
    dy = black_hole.y - particle.y

    # Euclidean distance from the center.
    distance_sq = dx * dx + dy * dy
    distance = math.sqrt(distance_sq)

    # -----------------------------------------------------------------------
    # ABSORPTION CHECK
    # -----------------------------------------------------------------------

    # If the particle has entered the event horizon region, it is considered
    # absorbed and removed from the active simulation.
    #
    # This is a simulation-level approximation and not a relativistic model.
    if distance <= black_hole.event_horizon_radius:
        particle.kill()
        return {
            "absorbed": True,
            "distance": distance,
        }

    # -----------------------------------------------------------------------
    # DIRECTION NORMALIZATION
    # -----------------------------------------------------------------------

    # Avoid undefined normalization at zero distance.
    if distance == 0:
        return {
            "absorbed": False,
            "distance": distance,
        }

    nx = dx / distance
    ny = dy / distance

    # -----------------------------------------------------------------------
    # FORCE AND ACCELERATION
    # -----------------------------------------------------------------------

    # Central-force model with softening:
    #
    #     F = G * M / (r^2 + softening)
    #
    # The softening term prevents numerical divergence near the center.
    force = gravity_constant * black_hole.mass / (distance_sq + softening)

    # Acceleration points toward the center.
    particle.ax = nx * force
    particle.ay = ny * force

    # -----------------------------------------------------------------------
    # VELOCITY UPDATE
    # -----------------------------------------------------------------------

    # Explicit integration of acceleration into velocity.
    particle.vx += particle.ax * dt
    particle.vy += particle.ay * dt

    # Apply damping to reduce long-term runaway energy growth and keep
    # particle motion visually controlled.
    particle.vx *= damping
    particle.vy *= damping

    # -----------------------------------------------------------------------
    # SPEED LIMIT
    # -----------------------------------------------------------------------

    # Clamp velocity magnitude to the configured maximum.
    speed_sq = particle.vx * particle.vx + particle.vy * particle.vy
    if speed_sq > max_speed * max_speed:
        speed = math.sqrt(speed_sq)
        if speed > 0:
            scale = max_speed / speed
            particle.vx *= scale
            particle.vy *= scale

    # -----------------------------------------------------------------------
    # POSITION UPDATE
    # -----------------------------------------------------------------------

    # Update spatial position using the current velocity.
    particle.x += particle.vx * dt
    particle.y += particle.vy * dt

    # -----------------------------------------------------------------------
    # TRAIL MANAGEMENT
    # -----------------------------------------------------------------------

    # Append the current position to the particle trail so that the renderer
    # can visualize recent motion history.
    if hasattr(particle, "trail"):
        particle.trail.append((particle.x, particle.y))

        # Keep only the most recent trail points.
        if len(particle.trail) > trail_length:
            particle.trail = particle.trail[-trail_length:]

    # -----------------------------------------------------------------------
    # RESULT
    # -----------------------------------------------------------------------

    return {
        "absorbed": False,
        "distance": distance,
    }
