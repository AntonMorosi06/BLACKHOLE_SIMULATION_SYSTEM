
**# Web Module

## Overview

This directory contains the browser-based visual and interactive layer of the BlackHole Simulation System.

The web module is designed as a lightweight demonstration environment that complements the main Python simulation. Its purpose is not to replace the core runtime of the project, but to provide an accessible and immediate way to inspect the system through a browser.

The current implementation combines:

* a static HTML interface
* a dedicated CSS presentation layer
* a small JavaScript simulation architecture
* interactive controls
* a simplified particle-based black hole visualization

This makes the module useful for presentation, inspection, and interactive demonstration.

---

## Role in the Project

Within the overall architecture of the repository, the web module acts as the visual and demonstrative layer.

| Layer  | Role                                    |
| ------ | --------------------------------------- |
| Python | Main simulation runtime                 |
| C      | Low-level numerical support             |
| Web    | Interactive browser-based demonstration |
| Docs   | Conceptual and mathematical explanation |
| Tests  | Targeted validation                     |

This means that the web module should be understood as a companion layer. It provides a readable and interactive representation of the system, but it does not attempt to reproduce the full depth of the Python simulation.

---

## Current Structure

The web layer is intentionally small and modular.

| File               | Role                              |
| ------------------ | --------------------------------- |
| `index.html`       | Main web interface                |
| `css/style.css`    | Visual presentation layer         |
| `js/config.js`     | Browser simulation configuration  |
| `js/particle.js`   | Particle entity for the web layer |
| `js/simulation.js` | Browser simulation core           |
| `js/main.js`       | Entry point and UI binding logic  |

This structure keeps configuration, model, simulation behavior, and startup logic separated.

---

## Functional Scope

The browser simulation currently supports:

* particle spawning around the simulation area
* central attraction toward a black hole core
* event horizon absorption
* accretion radius visualization
* short motion trails
* runtime particle counters
* play/pause interaction
* particle respawn through UI controls

These features are intentionally scoped to remain lightweight, fast, and readable inside a browser environment.

---

## Design Principles

The web module follows a small number of clear principles.

### Simplicity

The browser simulation is intentionally lighter than the Python runtime. It prioritizes responsiveness and readability over physical depth.

### Separation of Concerns

The module is split into distinct files so that each part has a narrow and understandable purpose:

* configuration
* particle model
* simulation logic
* entrypoint wiring
* styling

### Demonstrative Clarity

The interface is built to make the system understandable at a glance. The objective is visual explanation rather than full scientific completeness.

### Repository Consistency

Although simplified, the browser layer remains conceptually aligned with the rest of the project:

* black hole center
* event horizon
* accretion region
* central-force behavior
* particle absorption

---

## Relationship to the Python Simulation

The Python layer remains the main execution environment of the project.

The web module differs in several ways:

| Aspect     | Python Layer                 | Web Layer                        |
| ---------- | ---------------------------- | -------------------------------- |
| Purpose    | Primary simulation runtime   | Demonstration and presentation   |
| Complexity | Higher                       | Lower                            |
| Rendering  | Richer and more configurable | Lightweight and browser-oriented |
| Tooling    | Python-based                 | Native browser execution         |

This distinction is intentional. The browser module should be understood as a parallel visual layer, not as the authoritative simulation engine.

---

## Optional State Bridge

The repository can be extended so that the web module reads exported state from the Python simulation through a JSON file such as:

```text
data/output/state.json
```

In that configuration:

* the Python simulation exports particle positions and runtime values
* the web layer reads the exported state
* the browser interface acts as a live viewer of the Python system

This bridge is optional and does not change the role of the web module as a visual companion layer.

---

## Running the Web Module

The web interface can be opened directly in a browser through:

```bash id="wb1"
open web/index.html
```

or by starting a simple local server from the repository root:

```bash id="wb2"
python -m http.server 8000
```

and then opening the corresponding local address in a browser.

A local server is recommended if the browser becomes stricter about file access or if the module is extended further.

---

## Current Limitations

The current browser layer has clear and intentional limits.

| Area              | Limitation                                        |
| ----------------- | ------------------------------------------------- |
| Physical accuracy | Simplified                                        |
| Numerical depth   | Lower than Python layer                           |
| Feature scope     | Focused on visual demonstration                   |
| Synchronization   | No mandatory live integration with Python runtime |

These limitations are expected at the current stage of the project and reflect the demonstrative purpose of the web layer.

---

## Why This Module Matters

Even though it is lighter than the Python runtime, the web layer plays an important role in the project.

It provides:

* a fast visual entry point
* an accessible demonstration surface
* an interaction layer for non-Python environments
* a structured presentation of the core concepts

For collaborators, reviewers, or anyone exploring the repository for the first time, this module can be one of the easiest ways to understand the system.

---

## Future Extensions

Possible future developments of the web module include:

* richer parameter controls
* stronger dashboard elements
* improved visual effects
* synchronization with exported Python state
* additional explanatory overlays
* comparison between multiple simulation states

Any future extension should preserve the module’s current clarity and its role as a companion visual layer.

---

## Summary

The web module provides the browser-based demonstration environment of the BlackHole Simulation System.

Its value lies in making the system visible, explorable, and easier to interpret, while remaining structurally consistent with the broader repository.
**
