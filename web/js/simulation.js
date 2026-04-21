/*
============================================================================
BlackHole Simulation System - Web Simulation Core
----------------------------------------------------------------------------
This module defines the browser-side simulation engine.

Responsibilities:
- manage particle collection
- update simulation state (internal or external)
- render particles and black hole
- optionally load external state from Python simulation

IMPORTANT:
This module supports two modes:
1) Internal simulation (pure browser)
2) External state mode (data from Python via JSON)
============================================================================
*/

class BlackHoleSimulation {
  constructor(canvas, config) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");

    this.config = config;

    this.particles = [];
    this.absorbed = 0;

    // Black hole parameters (default or external)
    this.blackHole = {
      x: canvas.width / 2,
      y: canvas.height / 2,
      radius: 20,
      accretionRadius: 120
    };

    // Flag: if true, ignore internal physics and use external data
    this.externalMode = true;
  }

  /*
  ============================================================================
  EXTERNAL STATE LOADING (STEP 3 CORE)
  ============================================================================
  */

  loadExternalState(state) {
    /*
      Load simulation state from Python JSON export.

      Expected structure:
      {
        particles: [{x, y}],
        absorbed: number,
        black_hole: {x, y, event_horizon_radius, accretion_radius}
      }
    */

    if (!state || !state.particles) return;

    // Replace particles completely (viewer mode)
    this.particles = state.particles.map(p => {
      return {
        x: p.x,
        y: p.y
      };
    });

    this.absorbed = state.absorbed || 0;

    // Update black hole if provided
    if (state.black_hole) {
      this.blackHole.x = state.black_hole.x;
      this.blackHole.y = state.black_hole.y;
      this.blackHole.radius = state.black_hole.event_horizon_radius || 20;
      this.blackHole.accretionRadius = state.black_hole.accretion_radius || 120;
    }
  }

  /*
  ============================================================================
  INTERNAL SIMULATION (fallback / optional)
  ============================================================================
  */

  spawnParticles(count = 100) {
    this.particles = [];

    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2
      });
    }
  }

  update() {
    // If external mode is active → DO NOTHING
    if (this.externalMode) return;

    // Otherwise fallback simulation
    for (let p of this.particles) {
      const dx = this.blackHole.x - p.x;
      const dy = this.blackHole.y - p.y;

      const dist = Math.sqrt(dx * dx + dy * dy) + 0.01;

      const force = 0.05;

      p.vx += (dx / dist) * force;
      p.vy += (dy / dist) * force;

      p.x += p.vx;
      p.y += p.vy;
    }
  }

  /*
  ============================================================================
  RENDERING
  ============================================================================
  */

  render() {
    const ctx = this.ctx;

    // Clear
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw accretion disk
    ctx.beginPath();
    ctx.arc(
      this.blackHole.x,
      this.blackHole.y,
      this.blackHole.accretionRadius,
      0,
      Math.PI * 2
    );
    ctx.strokeStyle = "rgba(255,150,50,0.2)";
    ctx.stroke();

    // Draw event horizon
    ctx.beginPath();
    ctx.arc(
      this.blackHole.x,
      this.blackHole.y,
      this.blackHole.radius,
      0,
      Math.PI * 2
    );
    ctx.fillStyle = "black";
    ctx.fill();

    // Draw particles
    ctx.fillStyle = "white";

    for (let p of this.particles) {
      ctx.fillRect(p.x, p.y, 2, 2);
    }
  }

  /*
  ============================================================================
  UTILITIES
  ============================================================================
  */

  getAliveCount() {
    return this.particles.length;
  }
}
