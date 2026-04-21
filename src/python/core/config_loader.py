"""
Configuration Loader
--------------------

This module provides the configuration loading utility used by the Python
simulation layer.

Its role is intentionally simple:

- locate the simulation configuration file
- load the JSON configuration into memory
- return a dictionary usable by the runtime

The loader is kept separate from the simulation logic so that configuration
management remains centralized and easier to maintain.

The configuration file is expected to define the numerical and visual runtime
parameters required by the simulation.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_config() -> dict:
    """
    Load the simulation configuration file.

    Returns
    -------
    dict
        A dictionary containing the simulation parameters required by the
        Python runtime.

    Notes
    -----
    The configuration file is expected at:

        data/config/simulation_config.json

    relative to the project root.

    This function intentionally returns a plain dictionary rather than a custom
    configuration object in order to keep the current project structure simple
    and compatible with the rest of the codebase.
    """

    # Resolve project root starting from this file:
    #
    # src/python/core/config_loader.py
    # -> parent(core)
    # -> parent(python)
    # -> parent(src)
    # -> parent(project root)
    root_dir = Path(__file__).resolve().parents[3]

    config_path = root_dir / "data" / "config" / "simulation_config.json"

    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)

    return config
