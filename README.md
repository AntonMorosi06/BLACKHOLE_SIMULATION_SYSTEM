# BlackHole Simulation System

## Introduction

BlackHole Simulation System is a modular computational project designed to simulate and visualize simplified black hole related dynamics.

The system integrates multiple layers — numerical computation, real-time simulation, low-level modules, and visual representation — into a single structured environment. The objective is not to reproduce a complete astrophysical model, but to build a coherent framework where physical intuition, simulation logic, and software architecture evolve together.

This repository should be understood as a controlled simulation system rather than a scientific engine. Its strength lies in the clarity of its structure and the consistency between its components.

---

## System Purpose

The project is built around a clear set of objectives.

The first objective is to simulate particle behavior under the influence of a central mass, using simplified gravitational dynamics that remain numerically stable and visually interpretable.

The second objective is to provide a real-time simulation environment where motion, interaction, and system evolution can be observed directly.

The third objective is to maintain a modular architecture where different computational layers can evolve independently without breaking the system as a whole.

The fourth objective is to connect simulation, documentation, and visualization into a single repository that can be inspected, extended, and understood as a complete system.

---

## Architectural Structure

The repository is organized into independent but connected modules.

| Module        | Description                                             |
| ------------- | ------------------------------------------------------- |
| `src/python/` | Main simulation engine and execution logic              |
| `src/c/`      | Low-level numerical modules for isolated computations   |
| `web/`        | Browser-based visualization and demonstrative interface |
| `docs/`       | Conceptual, structural, and mathematical documentation  |
| `tests/`      | Validation of selected components                       |
| `scripts/`    | Environment setup and build automation                  |
| `data/`       | Configuration files and generated outputs               |
| `assets/`     | Static resources                                        |
| `logs/`       | Runtime logs                                            |

This structure allows each part of the system to remain isolated while still contributing to a unified workflow.

---

## Simulation Model

The simulation is based on a simplified central-force model.

Particles are influenced by a central mass representing a black hole. The force applied is derived from a reduced gravitational formulation, adapted to ensure numerical stability and real-time performance.

The system does not implement full relativistic physics. Instead, it uses controlled approximations that allow consistent behavior within a discrete-time simulation loop.

A softening factor is introduced to prevent instability when particles approach the center. This avoids singularities and ensures that the system remains stable under all conditions.

The model is intentionally minimal, but structured in a way that allows progressive extension.

---

## Python Layer

The Python layer is the core of the system.

It includes:

* constants and configuration management
* vector and utility functions
* particle and black hole models
* gravity engine logic
* simulation loop execution
* rendering
* report generation tools

This layer is responsible for running the simulation and producing the observable behavior of the system.

---

## C Layer

The C layer provides a lower-level computational perspective.

Its purpose is to isolate selected numerical routines and offer a more explicit implementation of certain physical computations. It is not required for running the main simulation, but acts as a complementary layer for experimentation and future optimization.

---

## Web Layer

The web module provides a visual and explanatory interface.

It is not a replacement for the simulation engine. Instead, it serves as a way to present the system in a more accessible format, allowing inspection of concepts, structure, and behavior through a browser.

---

## Running the System

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the launcher

```bash
python run_all.py
```

### Run the simulation directly

```bash
python -m src.python.simulations.main_simulation
```

### Open the web interface

Open the file:

```bash
web/index.html
```

### Build C modules

```bash
bash scripts/build_c.sh
```

---

## Documentation

The `docs/` directory contains the written structure of the system.

| File                       | Description                   |
| -------------------------- | ----------------------------- |
| `00_project_overview.md`   | General structure and purpose |
| `01_mathematical_model.md` | Mathematical foundation       |
| `02_future_extensions.md`  | Future development directions |

These documents provide the conceptual layer that complements the code.

---

## Current Scope

The repository currently provides:

* a modular simulation framework
* a controllable particle system
* a central gravitational model
* a real-time visualization layer
* low-level numerical modules
* structured documentation
* a unified launcher system

The system is complete as a prototype, but intentionally open for extension.

---

## Future Direction

The system is designed to evolve in a controlled way.

Future work may include:

* more accurate orbital dynamics
* enhanced visualization techniques
* stronger numerical methods
* deeper integration between Python and C modules
* additional simulation scenarios

All future development should preserve the modular structure of the repository.

---

## Author

Anton Morosi

---

## License

MIT License
