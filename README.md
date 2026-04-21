# BlackHole Simulation System

## Overview

BlackHole Simulation System is a modular project focused on the simulation and visualization of black hole related physical phenomena.

The repository combines numerical models, interactive Python simulations, low-level C components, documentation, tests, and a web-based visualization layer into a single structured system.

Its purpose is to provide both a conceptual and computational framework for exploring orbital behavior, gravitational effects, and simplified black hole models.

---

## Repository Structure

The project is organized into the following main modules:

| Module        | Purpose                                            |
| ------------- | -------------------------------------------------- |
| `src/python/` | Core Python simulation logic                       |
| `src/c/`      | Low-level numerical and physics-oriented C modules |
| `web/`        | Browser-based visual presentation                  |
| `docs/`       | Project description and mathematical notes         |
| `tests/`      | Validation of math and orbit logic                 |
| `scripts/`    | Environment setup and C build helpers              |
| `data/`       | Configuration and generated output                 |
| `assets/`     | Static resources                                   |
| `logs/`       | Runtime logs                                       |

---

## Core Components

### Python Simulation Layer

The Python side of the system provides the main simulation environment.

It includes:

* physical constants and configuration handling
* vector and math utilities
* black hole and particle models
* gravity engine and simulation step logic
* interactive simulation scripts
* report generation tools

### C Modules

The C layer contains low-level numerical components focused on:

* gravity core calculations
* orbit solving
* Schwarzschild-related computations

This allows the project to combine higher-level Python orchestration with lower-level computational modules.

### Web Module

The web layer provides a browser-based visual representation of the system.

It is intended as a lightweight presentation and interactive support layer rather than as the main computational engine.

---

## Main Features

The project currently includes:

* interactive Python simulation
* orbit experiment modules
* event horizon study module
* mathematical documentation
* low-level C components
* test suite
* web-based visualization support

---

## How to Run

### Install Python dependencies

```bash id="bh1a3k"
pip install -r requirements.txt
```

### Run the main launcher

```bash id="bhw73m"
python run_all.py
```

### Run the main Python simulation directly

```bash id="bho2kq"
python -m src.python.simulations.main_simulation
```

### Build C modules

```bash id="bh9wsm"
bash scripts/build_c.sh
```

---

## Documentation

The `docs/` directory contains the main written materials:

| File                       | Description                 |
| -------------------------- | --------------------------- |
| `00_project_overview.md`   | General structure and goals |
| `01_mathematical_model.md` | Mathematical basis          |
| `02_future_extensions.md`  | Planned evolution           |

---

## Current Scope

This project is an exploratory and modular simulation framework.

It is not intended as a complete astrophysical model, but as a structured prototype environment for studying simplified black hole related dynamics through code, visualization, and documentation.

---

## Future Direction

Possible future developments include:

* improved physical accuracy
* richer visualization
* stronger integration between Python and C modules
* enhanced reporting and data export
* more advanced web interaction
* extended experimental scenarios

---

## Author

Anton Morosi

---

## License

MIT License
