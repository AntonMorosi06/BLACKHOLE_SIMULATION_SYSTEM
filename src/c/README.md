# C Modules

## Overview

This directory contains the low-level C components of the BlackHole Simulation System.

The C layer is not the main runtime entry point of the project. The primary simulation workflow currently runs through the Python layer. However, this directory plays an important architectural role because it provides a dedicated space for numerical and physics-oriented routines that can be isolated, tested, and expanded independently.

In the current state of the repository, the C layer should be understood as a supporting computational subsystem rather than as a standalone application.

---

## Purpose

The purpose of the C modules is to provide a lower-level implementation path for selected numerical tasks.

This has several advantages.

First, it separates small computational routines from the higher-level orchestration logic of the Python simulation.
Second, it creates a clear extension point for future optimization work.
Third, it reinforces the modular character of the repository by distinguishing between simulation control and raw computation.

The current C layer is therefore useful both as a technical experiment and as a structural foundation for future development.

---

## Current Files

The directory currently contains a small set of source files and build instructions.

| File              | Role                                          |
| ----------------- | --------------------------------------------- |
| `gravity_core.c`  | Core gravity-related numerical logic          |
| `orbit_solver.c`  | Orbit-related computation routines            |
| `schwarzschild.c` | Schwarzschild-related reference calculations  |
| `Makefile`        | Build instructions for the local C components |

These files are intentionally separated so that each one can focus on a narrow area of responsibility.

---

## Role in the Project

Within the global architecture of the BlackHole Simulation System, the C layer complements the Python layer.

| Layer  | Role                                                         |
| ------ | ------------------------------------------------------------ |
| Python | Main simulation environment, orchestration, rendering, tools |
| C      | Focused numerical and physics-oriented support routines      |

This means that the C components are not meant to replace the Python simulation. Instead, they provide a lower-level computational space that may become increasingly important as the project evolves.

---

## Build Process

The repository includes a helper script for building the C modules:

```bash id="cmd001"
bash scripts/build_c.sh
```

This script moves into the `src/c` directory and invokes the local `Makefile`.

If needed, the build can also be launched manually from inside this directory with:

```bash id="cmd002"
make
```

The helper script is preferred because it aligns with the structure of the repository and keeps build behavior consistent.

---

## Design Philosophy

The C modules are intentionally simple and focused.

They are not meant to reproduce the full complexity of the simulation layer. Instead, they serve as isolated computational units that can be inspected and extended without affecting the rest of the system.

This makes the C layer useful for:

* controlled experimentation
* low-level numerical study
* future performance-oriented refactoring
* separation of concerns within the repository

---

## Current Scope

At the current stage, the C layer should be considered:

* present
* meaningful
* technically relevant
* not yet central to the main execution path

This is an important distinction.

The project already benefits from the presence of the C layer as an architectural component, even if the Python layer remains the primary runtime environment.

---

## Future Direction

Possible future developments of the C layer include:

* expansion of numerical routines
* closer integration with the Python simulation
* performance-oriented reimplementation of selected components
* additional reference models for gravitational or orbital calculations

Any such extension should preserve the modular structure already present in the repository.

---

## Notes

Compiled outputs should not be committed to the repository. Only source files, the `Makefile`, and related documentation should be tracked.

The C layer is intentionally lightweight, and its value lies in its clarity and extensibility rather than in current complexity.

---

## Summary

This directory contains the low-level numerical support layer of the BlackHole Simulation System.

Its function is to provide a clean and extensible computational foundation that complements the Python simulation while keeping the overall architecture modular and well organized.
