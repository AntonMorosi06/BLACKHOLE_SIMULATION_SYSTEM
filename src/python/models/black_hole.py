"""
Black Hole Model
----------------

This module defines the central black hole entity used by the simulation.

In the current system, the black hole is modeled as a static central object
that influences particles through a simplified gravitational field.

The class is intentionally minimal. Its role is to provide a structured
container for the properties required by the simulation engine and rendering
layer, without introducing unnecessary physical complexity.

Current responsibilities:
- define the position of the central attractor
- store the black hole mass used in force computation
- define the event horizon radius
- define the accretion radius used for visual and behavioral context
"""

from dataclasses import dataclass


@dataclass
class BlackHole:
    """
    Central black hole entity.

    Parameters
    ----------
    x, y :
        Coordinates of the black hole center in the simulation space.

    mass :
        Effective simulation mass used by the gravity engine.
        This is a scaled quantity and does not correspond directly to
        real-world astrophysical mass units.

    event_horizon_radius :
        Radius used as the absorption threshold.
        When a particle crosses this boundary, it is considered absorbed.

    accretion_radius :
        Outer radius used for conceptual and visual purposes.
        This does not necessarily imply physical accretion modeling, but
        provides a secondary boundary useful for rendering and interpretation.
    """

    x: float
    y: float
    mass: float
    event_horizon_radius: float
    accretion_radius: float

    def position(self) -> tuple[float, float]:
        """
        Return the current black hole position as a tuple.

        This is a convenience helper primarily useful for rendering,
        diagnostics, and future extension.
        """
        return (self.x, self.y)

    def set_mass(self, new_mass: float) -> None:
        """
        Update the black hole mass.

        This helper keeps the update explicit and makes runtime mass changes
        easier to manage from external control logic.

        No additional validation is enforced here because the current
        simulation already controls mass bounds at a higher level.
        """
        self.mass = new_mass

    def contains(self, px: float, py: float) -> bool:
        """
        Check whether a point lies inside the event horizon radius.

        This helper does not replace the simulation step logic, but it provides
        a clean geometric test that may be useful for diagnostics or future
        rendering-related checks.
        """
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) <= (self.event_horizon_radius * self.event_horizon_radius)

    def inside_accretion_zone(self, px: float, py: float) -> bool:
        """
        Check whether a point lies inside the accretion radius.

        This is primarily a semantic helper for code clarity. In the current
        repository, the accretion radius is mostly a conceptual and visual
        quantity rather than a full physical subsystem.
        """
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) <= (self.accretion_radius * self.accretion_radius)
