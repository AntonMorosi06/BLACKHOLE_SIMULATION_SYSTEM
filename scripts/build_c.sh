#!/bin/bash

# ============================================================================
# BlackHole Simulation System - C Build Helper
# ----------------------------------------------------------------------------
# This script builds the C modules located in src/c by invoking the local
# Makefile in that directory.
#
# Current responsibilities:
# - resolve the project root
# - move into the C source directory
# - run `make`
#
# The script intentionally remains simple because the C layer is currently a
# supporting subsystem of the overall project rather than a standalone build
# target with multiple profiles.
# ============================================================================

set -e

# Resolve the project root starting from this script location.
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
C_DIR="$ROOT_DIR/src/c"

echo "========================================="
echo " Building C modules"
echo "========================================="
echo "Project root: $ROOT_DIR"
echo "C source dir : $C_DIR"
echo

cd "$C_DIR" || exit 1
make

echo
echo "Build completed."
