# BlackHole Simulation System

## Overview

BlackHole Simulation System is a modular project designed to simulate, visualize, and analyze the behavior of particles under the influence of a central massive attractor.

The system is built as a multi-layer architecture combining:

* a Python-based simulation engine
* a lightweight C numerical layer
* a browser-based interactive visualization
* structured documentation and validation tests

The goal of the project is not to replicate a full relativistic model, but to create a clear, controllable, and extensible environment for exploring central-force systems and their emergent behavior.

---

## System Architecture

The repository is structured as a set of coordinated layers, each with a specific responsibility.

| Layer   | Role                                    |
| ------- | --------------------------------------- |
| Python  | Core simulation runtime                 |
| C       | Low-level numerical utilities           |
| Web     | Interactive visualization layer         |
| Docs    | Conceptual and structural documentation |
| Tests   | Targeted validation of key components   |
| Scripts | Environment setup and utilities         |

This separation allows the system to remain modular, readable, and extensible.

---

## Key Features

The system currently supports:

* particle-based simulation under central attraction
* configurable black hole mass and gravitational strength
* event horizon absorption logic
* accretion radius visualization
* real-time particle motion and trail rendering
* browser-based interactive controls
* modular simulation structure
* targeted validation tests

These features are implemented with a focus on clarity, stability, and incremental development.

---

## Repository Structure

The project is organized as follows:

```
blackhole-simulation-system/
│
├── src/
│   ├── python/           # Main simulation engine
│   └── c/                # Numerical support modules
│
├── web/                  # Browser-based visualization
│   ├── index.html
│   ├── css/
│   └── js/
│
├── data/
│   └── config/           # Simulation configuration
│
├── tests/                # Validation scripts
│
├── scripts/              # Setup and build utilities
│
├── docs/                 # Project documentation
│
└── run_all.py            # Unified launcher
```

Each directory is intentionally scoped to a specific part of the system.

---

## Running the Project

### Python Simulation

Run the main simulation directly:

```bash id="r1"
python src/python/simulations/main_simulation.py
```

---

### Web Interface

Open the browser-based simulation:

```bash id="r2"
open web/index.html
```

Or run a local server:

```bash id="r3"
python -m http.server 8000
```

---

### Launcher

Use the unified launcher to access core features:

```bash id="r4"
python run_all.py
```

---

### Tests

Run validation scripts:

```bash id="r5"
python tests/test_math.py
```

```bash id="r6"
python tests/test_orbit.py
```

---

## Design Principles

The system is built around a small number of core principles.

### Modularity

Each layer is separated and independently understandable.
This allows the system to evolve without breaking internal structure.

### Clarity

The project prioritizes readability over unnecessary complexity.
Every component is designed to be inspectable and understandable.

### Incremental Development

The system is intentionally built in stages, allowing controlled expansion over time.

### Demonstrative Value

The web layer and visual outputs are designed to make the system observable and explainable.

---

## Relationship Between Layers

The different layers of the system are connected conceptually but remain technically independent.

* The Python layer provides the main simulation logic
* The C layer supports numerical computation where needed
* The web layer offers a simplified interactive representation
* The tests validate selected behaviors
* The documentation explains structure and intent

This separation ensures that each part of the system can evolve without introducing unnecessary coupling.

---

## Limitations

The current system has known and intentional limitations:

* simplified physics model
* no full relativistic simulation
* partial test coverage
* no real-time synchronization between Python and web layers

These constraints reflect the current development stage and the chosen design approach.

---

## Future Directions

Potential future developments include:

* deeper integration between Python and web layers
* improved numerical models
* extended visualization capabilities
* richer control systems and dashboards
* additional validation tests

All future extensions are expected to preserve the current modular structure.

---

## Why This Project Matters

This project is designed as a structured environment for exploring:

* central-force systems
* emergent particle behavior
* simulation architecture design
* multi-layer system organization

It serves both as a technical foundation and as a demonstrative system that can be extended over time.

---

## Summary

BlackHole Simulation System is a modular, multi-layer simulation environment that combines computation, visualization, and structure into a coherent and extensible project.

The repository is designed to remain readable, adaptable, and progressively expandable.
