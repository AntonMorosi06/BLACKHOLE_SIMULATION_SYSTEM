# Mathematical Model

## Purpose

This document defines the mathematical basis used in the BlackHole Simulation System.

The goal of the model is not to reproduce a fully accurate physical representation of black holes. Instead, it provides a consistent and computationally stable framework for simulating particle motion under a central attractive force.

The mathematical structure is intentionally simplified, but designed to remain coherent, extensible, and directly translatable into code.

---

## Modeling Approach

The system adopts a central-force approximation.

A single dominant mass is placed at the center of the system. All particles evolve under the influence of this central attractor.

The model assumes:

* no interaction between particles
* a static central mass
* a two-dimensional simulation space
* discrete time evolution

This allows the system to remain computationally efficient and visually interpretable.

---

## Core Quantities

The simulation is defined through a small set of quantities:

| Symbol | Meaning                         |
| ------ | ------------------------------- |
| G      | Gravitational constant (scaled) |
| M      | Central mass                    |
| r      | Distance from the center        |
| a      | Acceleration                    |
| v      | Velocity                        |
| x, y   | Position coordinates            |

All quantities are expressed in simulation units rather than real-world units.

---

## Distance Computation

For each particle, the distance from the center is computed as:

r = sqrt((cx - x)^2 + (cy - y)^2)

where:

* (cx, cy) is the position of the central mass
* (x, y) is the particle position

This distance is used to determine both direction and magnitude of the force.

---

## Direction Vector

The direction toward the center is obtained by normalizing the displacement:

dx = cx - x
dy = cy - y

nx = dx / r
ny = dy / r

This produces a unit vector pointing toward the attractor.

---

## Force Model

The system uses a simplified inverse-square law:

F = G * M / (r^2 + s)

where:

* s is a softening term

The softening term is critical. It prevents the force from becoming numerically unstable when r approaches zero.

Without this term, the system would diverge near the center.

---

## Acceleration

Acceleration is derived directly from the force:

ax = nx * F
ay = ny * F

This ensures that the particle is always accelerated toward the center.

---

## Time Integration

The simulation uses a simple explicit integration scheme.

Velocity is updated as:

v = v + a * dt

Position is updated as:

x = x + v * dt

where dt is the time step of the simulation.

This method is computationally efficient but introduces approximation error. The system compensates by keeping dt small and using a stable force formulation.

---

## Numerical Stability

Several design choices ensure stability:

* softening term in the force equation
* bounded time step
* limited force magnitude near the center
* absence of particle-particle interactions

These constraints prevent divergence and allow continuous real-time execution.

---

## Event Horizon Representation

The system does not implement a true relativistic event horizon.

Instead, a conceptual boundary may be defined using a radius threshold. Inside this region, particles may:

* accelerate rapidly
* become visually trapped
* be removed from the simulation

This is a visual and behavioral approximation rather than a physical model.

---

## Model Limitations

The current model has several limitations:

| Area         | Limitation                  |
| ------------ | --------------------------- |
| Relativity   | Not implemented             |
| Space        | Two-dimensional only        |
| Interactions | No particle-particle forces |
| Accuracy     | Approximate integration     |
| Units        | Not physically scaled       |

These limitations are intentional and aligned with the goal of maintaining simplicity and stability.

---

## Extension Potential

The mathematical model can be extended in several directions:

* introduction of tangential velocity for stable orbits
* improved integration methods (e.g. semi-implicit schemes)
* three-dimensional extension
* relativistic corrections
* multi-body interaction systems

All extensions should preserve numerical stability and structural clarity.

---

## Summary

The mathematical model of the system is based on a simplified central-force formulation with explicit time integration.

Its primary strengths are:

* computational simplicity
* numerical stability
* direct mapping to code
* extensibility

This makes it suitable as a foundation for both experimentation and progressive refinement.
