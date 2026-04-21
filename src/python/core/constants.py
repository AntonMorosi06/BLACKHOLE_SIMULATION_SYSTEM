"""
Constants
---------

Centralized constant definitions for the BlackHole Simulation System.

This module collects the shared values used across the Python simulation
runtime, UI layer, and visualization helpers.

Its purpose is to keep global parameters in one place so that:

- the simulation remains easier to configure
- the rendering layer can reuse shared styling values
- runtime mode definitions remain consistent across modules
- the codebase avoids duplicated literals

Important note:
If this file already exists in your current repository with tuned values,
those values should be preserved. The main objective of this version is to
improve structure, naming clarity, and maintainability without changing the
logic of the system.
"""

# ---------------------------------------------------------------------------
# FRAME / TIMING
# ---------------------------------------------------------------------------

# Target frame rate used by the main simulation loop.
FPS = 60


# ---------------------------------------------------------------------------
# UI TEXT COLORS
# ---------------------------------------------------------------------------

# Primary text color used for standard HUD labels and generic information.
TEXT_COLOR = (235, 235, 245)

# Softer text color used for secondary information and less prominent labels.
TEXT_SOFT_COLOR = (170, 180, 205)

# Warning text color used for pause state, cautions, or highlighted status.
TEXT_WARNING_COLOR = (255, 200, 120)

# Accent color used for active mode information, titles, and key highlights.
TEXT_ACCENT_COLOR = (120, 190, 255)

# Success color used for positive notifications such as reset confirmation
# or screenshot success messages.
TEXT_SUCCESS_COLOR = (120, 230, 170)

# Error or alert color used where stronger emphasis is required.
TEXT_ERROR_COLOR = (255, 120, 120)


# ---------------------------------------------------------------------------
# SPAWN MODES
# ---------------------------------------------------------------------------

# Particle spawn mode identifiers.
#
# These constants are used to select the initialization pattern of particles
# when the simulation starts or resets.

SPAWN_EDGE = "edge"
SPAWN_DISK = "disk"
SPAWN_SPIRAL = "spiral"
SPAWN_CLUSTER = "cluster"
SPAWN_RAIN = "rain"

# Ordered list used by keyboard cycling and direct selection logic.
SPAWN_MODES = [
    SPAWN_EDGE,
    SPAWN_DISK,
    SPAWN_SPIRAL,
    SPAWN_CLUSTER,
    SPAWN_RAIN,
]

# Human-readable labels shown in the runtime interface.
SPAWN_MODE_LABELS = {
    SPAWN_EDGE: "Edge Inflow",
    SPAWN_DISK: "Accretion Disk",
    SPAWN_SPIRAL: "Spiral Arms",
    SPAWN_CLUSTER: "Cluster Collapse",
    SPAWN_RAIN: "Particle Rain",
}


# ---------------------------------------------------------------------------
# COLOR MODES
# ---------------------------------------------------------------------------

# Runtime color presentation modes used by the renderer.
#
# These values are treated as identifiers, not as direct RGB definitions.
# The actual interpretation happens in the rendering layer.

COLOR_MODES = [
    "classic",
    "speed",
    "radius",
    "temperature",
]

# Scalar used by animated color transitions or time-driven palette effects.
COLOR_SPEED = 0.015


# ---------------------------------------------------------------------------
# EFFECT COLORS
# ---------------------------------------------------------------------------

# Shockwave effect color used when particles are absorbed.
SHOCKWAVE_COLOR = (255, 160, 80)

# Stylized Hawking emission color.
HAWKING_COLOR = (180, 220, 255)

# Stylized jet emission color.
JET_COLOR = (120, 180, 255)


# ---------------------------------------------------------------------------
# NOTIFICATION PANEL STYLING
# ---------------------------------------------------------------------------

# Background color for on-screen notifications.
#
# The alpha component is intentionally included because notification rendering
# in the simulation uses semi-transparent surfaces.
NOTIF_BG = (12, 16, 28, 210)

# Border color for notification panels.
NOTIF_BORDER = (60, 90, 140, 180)


# ---------------------------------------------------------------------------
# OPTIONAL RENDER / VISUAL DEFAULTS
# ---------------------------------------------------------------------------

# These values are safe shared defaults for auxiliary modules.
# If your existing constants.py already defines additional runtime values,
# keep them as they are and leave this section only as shared UI support.

BG_SPACE = (4, 6, 12)
BG_SPACE_SOFT = (10, 12, 24)
STAR_COLOR = (220, 220, 255)
BLACK_HOLE_CORE_COLOR = (255, 140, 0)
EVENT_HORIZON_COLOR = (255, 90, 30)
ACCRETION_RING_COLOR = (255, 180, 90)


# ---------------------------------------------------------------------------
# MAINTENANCE NOTE
# ---------------------------------------------------------------------------

"""
Maintenance guidelines:

1. Keep this file limited to shared constants only.
   Do not place procedural logic here.

2. If values are tuned empirically for simulation stability or visual quality,
   document that in comments rather than duplicating magic numbers elsewhere.

3. If a constant is used only in one module and has no shared meaning,
   consider keeping it local to that module instead of moving it here.

4. Runtime modes imported by main_simulation.py should always remain stable,
   because they define part of the control contract of the application.
"""
