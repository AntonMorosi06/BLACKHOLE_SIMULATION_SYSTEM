# Project Overview

## Scope of the System

BlackHole Simulation System is a modular computational environment designed to simulate and visualize simplified gravitational dynamics around a central mass.

The system is not intended to reproduce full relativistic black hole physics. Its purpose is to provide a stable and extensible framework where numerical simulation, visualization, and structural organization are tightly connected.

The repository should be interpreted as a structured simulation system rather than a standalone application.

---

## Conceptual Structure

The system is built around a central idea: a particle field evolving under the influence of a dominant attractor.

This attractor represents a black hole in a simplified form. The behavior of the system emerges from the interaction between particles and this central entity, governed by a reduced force model.

The simulation evolves in discrete time steps. At each step:

* forces are computed
* velocities are updated
* positions are updated
* the system state is rendered

This loop defines the core dynamic of the system.

---

## Layered Architecture

The repository is organized into distinct layers, each responsible for a specific domain.

| Layer               | Responsibility                                            |
| ------------------- | --------------------------------------------------------- |
| Simulation (Python) | Execution of the simulation loop and system state updates |
| Numerical (C)       | Isolated low-level computation modules                    |
| Visualization (Web) | External representation and inspection of the system      |
| Documentation       | Conceptual and mathematical explanation                   |
| Infrastructure      | Setup, scripts, and execution support                     |

Each layer is designed to remain independent while contributing to the overall system.

---

## Simulation Pipeline

The simulation process follows a consistent pipeline.

1. Initialization
   Particles and central mass are created. Initial positions and velocities are assigned.

2. Force Computation
   For each particle, the distance from the center is calculated. A force value is derived from this distance.

3. Acceleration Update
   The direction toward the center is normalized and scaled by the computed force.

4. Velocity Update
   Velocity is updated using the computed acceleration and the simulation time step.

5. Position Update
   Particle positions are updated using the new velocities.

6. Rendering
   The current system state is visualized.

This pipeline repeats continuously during execution.

---

## Numerical Model

The system uses a simplified central-force model.

The force applied to each particle is proportional to the inverse square of the distance from the center, with an additional softening term to prevent instability at very small distances.

The purpose of this model is not physical accuracy, but:

* numerical stability
* visual coherence
* computational simplicity

This allows real-time simulation without divergence or instability.

---

## Data Flow

The internal data flow is minimal and direct.

* Constants define global parameters
* The simulation engine reads these parameters
* Particle states are updated at each step
* The renderer consumes the updated state

There is no complex data pipeline or external dependency chain. This keeps the system predictable and easy to extend.

---

## Modularity Principles

The system follows a set of structural principles:

* No duplication of core logic
* Centralized configuration through constants
* Separation between computation and rendering
* Isolation of experimental modules (C layer)
* Clear directory boundaries

These principles ensure that the system remains maintainable as it grows.

---

## Role of Each Directory

| Directory     | Role                            |
| ------------- | ------------------------------- |
| `src/python/` | Core simulation logic           |
| `src/c/`      | Low-level numerical experiments |
| `web/`        | Visual interface                |
| `docs/`       | System explanation              |
| `tests/`      | Validation and checks           |
| `scripts/`    | Execution and setup             |
| `data/`       | Configuration and outputs       |
| `logs/`       | Execution traces                |

Each directory has a clearly defined purpose and should not overlap with others.

---

## Execution Model

The system can be executed in two main ways:

* through the central launcher (`run_all.py`)
* by directly running the simulation module

The launcher provides a unified entry point, while direct execution allows focused testing and development.

---

## Current Limitations

The current implementation has known limitations.

* no relativistic physics
* simplified force model
* no collision handling between particles
* no full 3D simulation
* limited numerical precision control

These limitations are intentional and aligned with the current scope of the project.

---

## Extension Strategy

Future development should follow a controlled approach.

Changes should:

* preserve modular structure
* avoid breaking existing components
* introduce improvements incrementally
* maintain clarity of the system

The objective is to evolve the system without compromising its internal coherence.

---

## Summary

BlackHole Simulation System is a structured simulation framework based on a simplified gravitational model.

Its main value lies in:

* clarity of architecture
* consistency between modules
* extensibility
* real-time simulation capability

The system provides a stable base for further exploration in both computational and conceptual directions.
