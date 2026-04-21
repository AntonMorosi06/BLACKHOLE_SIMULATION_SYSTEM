/*
  ============================================================================
  BlackHole Simulation System - Web Simulation Core
  ----------------------------------------------------------------------------
  This file contains the browser-based simulation engine used by the web layer.

  The simulation implemented here is intentionally lightweight compared to the
  Python runtime. Its role is to provide an interactive visual demonstration
  of the system inside the browser.

  Main responsibilities:
  - initialize simulation state
  - spawn particles
  - update particle motion under central attraction
  - detect absorption inside the event horizon
  - render background, black hole, and particles
  - expose compact runtime counters for the UI layer

  This module is not intended to replace the Python simulation.
  It is a browser-oriented companion layer focused on readability,
  responsiveness, and demonstrative clarity.
  ============================================================================
*/

class BlackHoleSimulation {
  constructor(canvas, config) {
    // Rendering surface
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");

    // Shared runtime configuration
    this.config = config;

    // Fixed center of the black hole in canvas coordinates
    this.centerX = canvas.width / 2;
    this.centerY = canvas.height / 2;

    // Particle state
    this.particles = [];

    // Runtime counter of absorbed particles
    this.absorbed = 0;

    // Initial particle creation
    this.spawnParticles();
  }

  spawnParticles() {
    /*
      Reset and repopulate the simulation.

      Particles are spawned around the outer boundaries of the canvas and then
      attracted inward by the central mass.
    */
    this.particles = [];
    this.absorbed = 0;

    for (let i = 0; i < this.config.particleCount; i++) {
      const side = Math.floor(Math.random() * 4);
      let x, y;

      // Spawn particles slightly outside the visible canvas bounds.
      if (side === 0) {
        x = Math.random() * this.canvas.width;
        y = -40;
      } else if (side === 1) {
        x = Math.random() * this.canvas.width;
        y = this.canvas.height + 40;
      } else if (side === 2) {
        x = -40;
        y = Math.random() * this.canvas.height;
      } else {
        x = this.canvas.width + 40;
        y = Math.random() * this.canvas.height;
      }

      // Small randomized initial velocity.
      const vx = (Math.random() - 0.5) * 2.4;
      const vy = (Math.random() - 0.5) * 2.4;

      this.particles.push(new Particle(x, y, vx, vy));
    }
  }

  update() {
    /*
      Advance the simulation by one frame.

      For each active particle:
      - compute distance from center
      - check event horizon absorption
      - compute central attraction
      - update velocity and position
      - store trail points for rendering
    */
    if (!this.config.running) return;

    for (const p of this.particles) {
      if (!p.alive) continue;

      const dx = this.centerX - p.x;
      const dy = this.centerY - p.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      // Absorption threshold: particles crossing the event horizon are removed.
      if (dist <= this.config.eventHorizonRadius) {
        p.alive = false;
        this.absorbed++;
        continue;
      }

      // Normalized direction toward the center.
      const nx = dx / (dist || 1);
      const ny = dy / (dist || 1);

      // Simplified central-force model with softening.
      const force =
        this.config.gravity *
        this.config.blackHoleMass /
        ((dist * dist) + this.config.softening);

      // Velocity and position update.
      p.vx += nx * force;
      p.vy += ny * force;
      p.x += p.vx;
      p.y += p.vy;

      // Maintain a short motion trail for visual readability.
      p.trail.push({ x: p.x, y: p.y });
      if (p.trail.length > 18) {
        p.trail.shift();
      }
    }
  }

  drawBackground() {
    /*
      Draw the radial background glow centered on the black hole.

      This provides depth and visual focus to the canvas without requiring a
      separate static background asset.
    */
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    const grad = ctx.createRadialGradient(
      this.centerX, this.centerY, 10,
      this.centerX, this.centerY, this.canvas.width * 0.55
    );

    grad.addColorStop(0, "rgba(255,140,50,0.08)");
    grad.addColorStop(0.25, "rgba(255,120,40,0.05)");
    grad.addColorStop(0.6, "rgba(10,12,20,0.2)");
    grad.addColorStop(1, "rgba(2,3,5,1)");

    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  drawBlackHole() {
    /*
      Draw the simplified visual structure of the black hole:
      - outer accretion boundary
      - central event horizon region
    */
    const ctx = this.ctx;

    // Accretion radius
    ctx.beginPath();
    ctx.strokeStyle = "rgba(255,140,60,0.85)";
    ctx.lineWidth = 2;
    ctx.arc(this.centerX, this.centerY, this.config.accretionRadius, 0, Math.PI * 2);
    ctx.stroke();

    // Event horizon
    ctx.beginPath();
    ctx.fillStyle = "#040404";
    ctx.arc(this.centerX, this.centerY, this.config.eventHorizonRadius, 0, Math.PI * 2);
    ctx.fill();
  }

  drawParticles() {
    /*
      Draw all active particles and their short trails.

      Trail rendering is intentionally lightweight so that the browser demo
      remains responsive while still conveying motion history.
    */
    const ctx = this.ctx;

    for (const p of this.particles) {
      if (!p.alive) continue;

      if (p.trail.length > 1) {
        ctx.beginPath();
        ctx.strokeStyle = "rgba(255,140,70,0.25)";
        ctx.lineWidth = 1;
        ctx.moveTo(p.trail[0].x, p.trail[0].y);

        for (const t of p.trail) {
          ctx.lineTo(t.x, t.y);
        }

        ctx.stroke();
      }

      ctx.beginPath();
      ctx.fillStyle = "#ffd29c";
      ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  render() {
    /*
      Render a complete frame of the browser simulation.
    */
    this.drawBackground();
    this.drawBlackHole();
    this.drawParticles();
  }

  getAliveCount() {
    /*
      Return the number of currently active particles.

      This is useful for dashboard labels or compact status counters in the UI.
    */
    return this.particles.filter(p => p.alive).length;
  }
}
