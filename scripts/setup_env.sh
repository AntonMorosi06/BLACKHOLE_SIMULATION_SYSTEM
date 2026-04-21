
#!/bin/bash

# ============================================================================
# BlackHole Simulation System - Environment Setup Helper
# ----------------------------------------------------------------------------
# This script prepares the local Python environment for the project.
#
# Current responsibilities:
# - create a virtual environment in .venv
# - activate the environment
# - upgrade pip
# - install project dependencies from requirements.txt
#
# The script is intentionally simple because the repository currently uses
# a lightweight local setup strategy and does not depend on more complex
# environment managers.
# ============================================================================

set -e

# Resolve the project root starting from this script location.
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
REQ_FILE="$ROOT_DIR/requirements.txt"

echo "========================================="
echo " Setting up Python environment"
echo "========================================="
echo "Project root : $ROOT_DIR"
echo "Venv path    : $VENV_DIR"
echo "Requirements : $REQ_FILE"
echo

# Create the virtual environment.
python3 -m venv "$VENV_DIR"

# Activate the virtual environment.
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

# Upgrade pip and install dependencies.
pip install --upgrade pip
pip install -r "$REQ_FILE"

echo
echo "Environment ready."
echo "Activate it later with:"
echo "source .venv/bin/activate"
