# Tests Module

## Overview

This directory contains a small set of verification scripts used to validate selected components of the BlackHole Simulation System.

The tests included in this module are not meant to provide full coverage of the entire project. Instead, they focus on validating core numerical behaviors and ensuring that key physical relationships remain stable during development.

At the current stage of the project, the testing layer is intentionally lightweight and targeted.

---

## Scope of the Tests

The tests included in this directory focus on two main areas:

| Area                    | Description                                         |
| ----------------------- | --------------------------------------------------- |
| Mathematical validation | Verification of core numerical computations         |
| Orbital behavior        | Basic validation of motion under central attraction |

These tests are designed to check correctness of core building blocks rather than full system integration.

---

## Current Files

| File            | Purpose                                                             |
| --------------- | ------------------------------------------------------------------- |
| `test_math.py`  | Verifies fundamental numerical relationships used in the simulation |
| `test_orbit.py` | Tests basic orbital dynamics under central force                    |

Each test file targets a specific aspect of the system to keep the testing layer modular and easy to extend.

---

## Testing Philosophy

The project follows a pragmatic testing approach.

### Targeted Validation

Instead of attempting to test every component, the current tests focus on critical numerical behaviors. These are the parts of the system where correctness matters most.

### Stability Over Coverage

The goal is not to maximize test coverage, but to ensure that key computations remain stable and predictable over time.

### Simplicity

The tests are intentionally simple and readable. They are designed to be understood quickly without requiring complex setup or tooling.

---

## How to Run the Tests

Tests can be executed directly from the repository root using Python.

Example:

```bash id="tst1"
python tests/test_math.py
```

```bash id="tst2"
python tests/test_orbit.py
```

If a virtual environment is used, make sure it is activated before running the tests.

---

## What the Tests Check

### Mathematical Consistency

The mathematical tests ensure that core formulas used in the simulation behave as expected. This includes:

* force computation consistency
* stable numerical outputs
* absence of obvious anomalies

### Orbital Behavior

The orbit tests validate:

* motion under central attraction
* general stability of trajectories
* expected qualitative behavior of particles

These are not full physics validations, but sanity checks aligned with the simplified model used in the project.

---

## Limitations

The current testing module has known limitations.

| Area          | Limitation           |
| ------------- | -------------------- |
| Coverage      | Only partial         |
| Integration   | No full system tests |
| Performance   | Not evaluated        |
| Visualization | Not tested           |

These limitations are expected at the current stage of development and reflect the incremental approach of the project.

---

## Role in the Repository

Within the overall system, the tests module acts as a verification layer for selected components.

| Layer  | Role                   |
| ------ | ---------------------- |
| Python | Simulation runtime     |
| C      | Numerical support      |
| Web    | Visualization          |
| Tests  | Targeted validation    |
| Docs   | Conceptual explanation |

The tests help ensure that the core numerical behavior of the system remains consistent as the project evolves.

---

## Future Extensions

Potential improvements for this module include:

* additional numerical validation tests
* structured test suites
* integration-level checks
* automated execution pipelines

Any extension should preserve the current clarity and avoid unnecessary complexity.

---

## Summary

The tests module provides a focused and lightweight verification layer for the BlackHole Simulation System.

Its purpose is to ensure that essential numerical behaviors remain correct and stable, without introducing unnecessary complexity into the development workflow.
