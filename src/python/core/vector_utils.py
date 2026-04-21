"""
Vector Utilities
----------------

Centralized vector and scalar utility functions used across the
BlackHole Simulation System.

This module exists to avoid duplication of small mathematical operations
inside the simulation, rendering, and engine layers.

The functions defined here are intentionally minimal. Their purpose is not
to replace a numerical library, but to provide a clear and reusable set of
helpers for the specific needs of this project.

Current responsibilities:
- 2D vector magnitude operations
- normalization
- vector limiting
- perpendicular vector computation
- scalar clamping and interpolation
- value remapping between ranges
"""

import math
from typing import Tuple

from src.python.core.constants import EPSILON


# ═══════════════════════════════════════════════════════════
#  VECTOR OPERATIONS
# ═══════════════════════════════════════════════════════════

def magnitude(x: float, y: float) -> float:
    """
    Return the Euclidean magnitude of a 2D vector.

    Parameters
    ----------
    x, y :
        Vector components.

    Returns
    -------
    float
        Euclidean norm of the vector.

    Notes
    -----
    This is equivalent to sqrt(x^2 + y^2), but uses math.hypot for clarity
    and numerical robustness.
    """
    return math.hypot(x, y)


def magnitude_squared(x: float, y: float) -> float:
    """
    Return the squared magnitude of a 2D vector.

    Parameters
    ----------
    x, y :
        Vector components.

    Returns
    -------
    float
        Squared Euclidean norm.

    Notes
    -----
    This avoids the square root operation and is useful in cases where only
    relative comparison of lengths is needed.
    """
    return x * x + y * y


def normalize(x: float, y: float) -> Tuple[float, float]:
    """
    Normalize a 2D vector.

    Parameters
    ----------
    x, y :
        Vector components.

    Returns
    -------
    Tuple[float, float]
        Normalized vector components.

    Notes
    -----
    If the vector magnitude is smaller than EPSILON, the function returns
    (0.0, 0.0) to avoid unstable division by near-zero values.
    """
    mag = math.hypot(x, y)
    if mag < EPSILON:
        return 0.0, 0.0
    return x / mag, y / mag


def limit_vector(x: float, y: float, max_value: float) -> Tuple[float, float]:
    """
    Limit the magnitude of a 2D vector to a maximum value.

    Parameters
    ----------
    x, y :
        Vector components.
    max_value :
        Maximum allowed vector magnitude.

    Returns
    -------
    Tuple[float, float]
        Possibly rescaled vector.

    Notes
    -----
    If the vector is already shorter than max_value, it is returned unchanged.
    This helper is useful for speed clamping and general vector stabilization.
    """
    mag = math.hypot(x, y)
    if mag > max_value and mag > EPSILON:
        scale = max_value / mag
        return x * scale, y * scale
    return x, y


def perpendicular(x: float, y: float) -> Tuple[float, float]:
    """
    Return the perpendicular vector obtained by a 90-degree counterclockwise
    rotation.

    Parameters
    ----------
    x, y :
        Vector components.

    Returns
    -------
    Tuple[float, float]
        Perpendicular vector (-y, x).

    Notes
    -----
    This helper is useful for generating tangential motion or orthogonal
    directional components in 2D space.
    """
    return -y, x


# ═══════════════════════════════════════════════════════════
#  SCALAR OPERATIONS
# ═══════════════════════════════════════════════════════════

def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    Clamp a scalar value between a minimum and a maximum.

    Parameters
    ----------
    value :
        Input scalar.
    minimum :
        Lower allowed bound.
    maximum :
        Upper allowed bound.

    Returns
    -------
    float
        Clamped scalar value.
    """
    return max(minimum, min(maximum, value))


def lerp(a: float, b: float, t: float) -> float:
    """
    Perform linear interpolation between two values.

    Parameters
    ----------
    a :
        Start value.
    b :
        End value.
    t :
        Interpolation factor.

    Returns
    -------
    float
        Interpolated scalar value.

    Notes
    -----
    No automatic clamping is applied to t. This means the function can also
    be used for extrapolation if t is outside the [0, 1] interval.
    """
    return a + (b - a) * t


def map_range(
    value: float,
    in_min: float, in_max: float,
    out_min: float, out_max: float,
) -> float:
    """
    Remap a value from one interval to another.

    Parameters
    ----------
    value :
        Input value in the source range.
    in_min, in_max :
        Source range bounds.
    out_min, out_max :
        Target range bounds.

    Returns
    -------
    float
        Remapped value in the output range.

    Notes
    -----
    If the source interval is too small (below EPSILON), the function returns
    out_min to avoid division by near-zero spans.
    """
    span = in_max - in_min
    if abs(span) < EPSILON:
        return out_min
    t = (value - in_min) / span
    return lerp(out_min, out_max, t)
