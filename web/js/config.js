/*
  ============================================================================
  BlackHole Simulation System - Web Configuration
  ----------------------------------------------------------------------------
  This file defines the runtime configuration used by the browser-based
  simulation layer.

  Its purpose is intentionally narrow:
  - provide a single shared configuration object
  - keep the main simulation script cleaner
  - make the web demo easier to tune and inspect

  Notes:
  - This configuration belongs to the web layer only.
  - It does not replace the Python simulation configuration.
  - Values here are tuned for interactive browser rendering and visual clarity.
  ============================================================================
*/

const SIM_CONFIG = {
  // Canvas dimensions
  width: 1200,
  height: 650,

  // Particle system
  particleCount: 220,

  // Central force parameters
  gravity: 0.42,
  blackHoleMass: 8000,
  softening: 20,

  // Black hole structure
  eventHorizonRadius: 32,
  accretionRadius: 120,

  // Runtime state
  running: true
};
