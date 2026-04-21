"""
Math tests for core vector utilities.

This test module validates the behavior of the shared mathematical helpers
defined in `src.python.core.vector_utils`.

The purpose of these tests is to ensure that the low-level numerical helpers
used across the simulation remain stable and predictable. Since these
functions are reused in multiple layers of the project, even small numerical
errors or edge-case inconsistencies could propagate into the simulation,
rendering, or auxiliary tools.

Covered functions:
- magnitude
- magnitude_squared
- normalize
- clamp
- lerp
- limit_vector
- map_range
"""

import math

from src.python.core.vector_utils import (
    magnitude,
    magnitude_squared,
    normalize,
    clamp,
    lerp,
    limit_vector,
    map_range,
)


# ═══════════════════════════════════════════════════════════
#  MAGNITUDE
# ═══════════════════════════════════════════════════════════

def test_magnitude_345():
    """
    The vector (3, 4) should have Euclidean magnitude 5.
    """
    assert round(magnitude(3, 4), 5) == 5.0


def test_magnitude_zero():
    """
    The zero vector should have zero magnitude.
    """
    assert magnitude(0, 0) == 0.0


def test_magnitude_negative():
    """
    Magnitude should be independent of sign direction.
    """
    assert round(magnitude(-3, -4), 5) == 5.0


def test_magnitude_large():
    """
    Magnitude should remain numerically stable for large values.
    """
    assert abs(magnitude(1e6, 1e6) - math.sqrt(2) * 1e6) < 1e-3


def test_magnitude_squared_basic():
    """
    Squared magnitude of (3, 4) should be 25.
    """
    assert magnitude_squared(3, 4) == 25.0


# ═══════════════════════════════════════════════════════════
#  NORMALIZE
# ═══════════════════════════════════════════════════════════

def test_normalize_x_axis():
    """
    A pure x-axis vector should normalize to (1, 0).
    """
    x, y = normalize(10, 0)
    assert (round(x, 5), round(y, 5)) == (1.0, 0.0)


def test_normalize_diagonal():
    """
    The vector (3, 4) should normalize to (3/5, 4/5).
    """
    x, y = normalize(3, 4)
    assert abs(x - 3 / 5) < 1e-6 and abs(y - 4 / 5) < 1e-6


def test_normalize_zero_vector():
    """
    The zero vector should normalize safely to (0, 0).
    """
    assert normalize(0, 0) == (0.0, 0.0)


def test_normalize_length_is_one():
    """
    A normalized non-zero vector should have magnitude 1.
    """
    x, y = normalize(5, -12)
    assert abs(math.hypot(x, y) - 1.0) < 1e-6


def test_normalize_then_magnitude():
    """
    Magnitude(normalize(v)) should be 1 for any non-zero vector.
    """
    x, y = normalize(7, 24)
    assert abs(magnitude(x, y) - 1.0) < 1e-6


# ═══════════════════════════════════════════════════════════
#  CLAMP
# ═══════════════════════════════════════════════════════════

def test_clamp_inside():
    """
    A value already inside the interval should remain unchanged.
    """
    assert clamp(5, 0, 10) == 5


def test_clamp_below():
    """
    A value below the minimum should be clamped to the minimum.
    """
    assert clamp(-5, 0, 10) == 0


def test_clamp_above():
    """
    A value above the maximum should be clamped to the maximum.
    """
    assert clamp(15, 0, 10) == 10


def test_clamp_edges():
    """
    Boundary values should be preserved exactly.
    """
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10


# ═══════════════════════════════════════════════════════════
#  LERP
# ═══════════════════════════════════════════════════════════

def test_lerp_boundaries():
    """
    Linear interpolation should reproduce endpoints when t is 0 or 1.
    """
    assert lerp(0, 10, 0) == 0
    assert lerp(0, 10, 1) == 10


def test_lerp_midpoint():
    """
    Linear interpolation at t=0.5 should return the midpoint.
    """
    assert lerp(0, 10, 0.5) == 5.0


# ═══════════════════════════════════════════════════════════
#  LIMIT VECTOR
# ═══════════════════════════════════════════════════════════

def test_limit_vector_no_change():
    """
    A vector already below the maximum norm should remain unchanged.
    """
    x, y = limit_vector(1, 0, 5)
    assert (x, y) == (1, 0)


def test_limit_vector_clamped():
    """
    A vector longer than the allowed maximum should be rescaled.
    """
    x, y = limit_vector(10, 0, 5)
    assert abs(x - 5.0) < 1e-6 and abs(y) < 1e-6


def test_limit_vector_diagonal():
    """
    Clamping should preserve direction while enforcing the max norm.
    """
    x, y = limit_vector(10, 10, 1)
    assert abs(math.hypot(x, y) - 1.0) < 1e-6


# ═══════════════════════════════════════════════════════════
#  MAP RANGE
# ═══════════════════════════════════════════════════════════

def test_map_range_basic():
    """
    A midpoint in the source interval should map to the midpoint
    of the target interval.
    """
    assert abs(map_range(5, 0, 10, 0, 100) - 50.0) < 1e-6


def test_map_range_zero_span():
    """
    If the input interval has zero span, the function should safely
    return the lower bound of the output interval.
    """
    assert map_range(5, 5, 5, 0, 100) == 0.0
