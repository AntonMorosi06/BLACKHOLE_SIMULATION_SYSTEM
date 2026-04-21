"""
Orbit-related tests for the BlackHole Simulation System.

This test module validates the behavior of the helper function
`orbital_velocity(...)` used by the orbit experiment layer.

The purpose of these tests is to ensure that the simplified orbital velocity
model behaves consistently with the mathematical relation expected by the
project:

    v = sqrt(G * M / r)

The tests do not attempt to validate a full physical orbital simulation.
They only verify that the scalar helper behaves correctly under the parameter
conditions currently used by the repository.
"""

import math

from src.python.simulations.orbit_experiment import orbital_velocity


# ═══════════════════════════════════════════════════════════
#  BASIC VALIDITY
# ═══════════════════════════════════════════════════════════

def test_orbital_velocity_positive():
    """
    Orbital velocity should be strictly positive when radius is greater than zero.
    """
    value = orbital_velocity(0.45, 9000.0, 180.0)
    assert value > 0.0


def test_orbital_velocity_zero_radius():
    """
    If the radius is zero, the function should safely return 0.0
    instead of raising an error or producing an invalid value.
    """
    value = orbital_velocity(0.45, 9000.0, 0.0)
    assert value == 0.0


def test_orbital_velocity_negative_radius():
    """
    If the radius is negative, the function should return 0.0
    to avoid non-physical results.
    """
    value = orbital_velocity(0.45, 9000.0, -10.0)
    assert value == 0.0


# ═══════════════════════════════════════════════════════════
#  FORMULA CONSISTENCY
# ═══════════════════════════════════════════════════════════

def test_orbital_velocity_matches_formula():
    """
    Explicitly verify the simplified formula:

        v = sqrt(G * M / r)
    """
    g = 0.45
    m = 9000.0
    r = 180.0

    expected = math.sqrt((g * m) / r)
    value = orbital_velocity(g, m, r)

    assert abs(value - expected) < 1e-9


def test_orbital_velocity_known_value():
    """
    Check a known numerical case against the expected analytical value.
    """
    value = orbital_velocity(0.45, 9000.0, 180.0)
    assert round(value, 6) == round(math.sqrt((0.45 * 9000.0) / 180.0), 6)


# ═══════════════════════════════════════════════════════════
#  MONOTONICITY PROPERTIES
# ═══════════════════════════════════════════════════════════

def test_orbital_velocity_decreases_with_radius():
    """
    For fixed G and M, increasing the orbital radius should reduce
    the orbital velocity.
    """
    g = 0.45
    m = 9000.0

    v1 = orbital_velocity(g, m, 100.0)
    v2 = orbital_velocity(g, m, 200.0)
    v3 = orbital_velocity(g, m, 400.0)

    assert v1 > v2 > v3


def test_orbital_velocity_increases_with_mass():
    """
    For fixed G and r, increasing the central mass should increase
    the orbital velocity.
    """
    g = 0.45
    r = 180.0

    v1 = orbital_velocity(g, 1000.0, r)
    v2 = orbital_velocity(g, 5000.0, r)
    v3 = orbital_velocity(g, 9000.0, r)

    assert v1 < v2 < v3


def test_orbital_velocity_increases_with_gravity_constant():
    """
    For fixed M and r, increasing the gravitational constant should increase
    the orbital velocity.
    """
    m = 9000.0
    r = 180.0

    v1 = orbital_velocity(0.10, m, r)
    v2 = orbital_velocity(0.30, m, r)
    v3 = orbital_velocity(0.45, m, r)

    assert v1 < v2 < v3
