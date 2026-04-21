/*
  ============================================================================
  BlackHole Simulation System - Web Particle Model
  ----------------------------------------------------------------------------
  This file defines the particle entity used by the browser-based simulation.

  The web layer particle model is intentionally minimal. Its purpose is to
  support real-time visual simulation in the browser without reproducing the
  full complexity of the Python runtime model.

  Current responsibilities:
  - store position
  - store velocity
  - track alive state
  - store recent trail points for rendering
  ============================================================================
*/

class Particle {
  constructor(x, y, vx, vy) {
    // Current position in canvas coordinates
    this.x = x;
    this.y = y;

    // Current velocity components
    this.vx = vx;
    this.vy = vy;

    // Indicates whether the particle is still active in the simulation
    this.alive = true;

    // Stores recent positions for visual trail rendering
    this.trail = [];
  }
}
