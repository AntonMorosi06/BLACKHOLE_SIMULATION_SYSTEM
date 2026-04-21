/*
  ============================================================================
  BlackHole Simulation System - Web Entry Point
  ----------------------------------------------------------------------------
  This file is the main browser entrypoint for the web simulation layer.

  Its responsibilities are intentionally minimal:
  - read the required DOM references
  - create the browser simulation instance
  - keep the small runtime dashboard updated
  - bind the main control buttons
  - start the animation loop

  The simulation logic itself is not implemented here.
  It is delegated to:
  - config.js       -> runtime parameters
  - particle.js     -> particle entity
  - simulation.js   -> browser simulation core

  This file exists to connect those parts into a running web demo.
  ============================================================================
*/


/* ============================================================================
   DOM REFERENCES
   ============================================================================ */

const canvas = document.getElementById("blackholeCanvas");
const spawnBtn = document.getElementById("spawnBtn");
const toggleMotionBtn = document.getElementById("toggleMotionBtn");

const particleCountEl = document.getElementById("particleCount");
const absorbedCountEl = document.getElementById("absorbedCount");
const simStatusEl = document.getElementById("simStatus");


/* ============================================================================
   SIMULATION INSTANCE
   ============================================================================ */

const simulation = new BlackHoleSimulation(canvas, SIM_CONFIG);


/* ============================================================================
   UI STATE UPDATES
   ============================================================================ */

function updateStats() {
  /*
    Refresh the compact dashboard values displayed in the page.

    Current metrics:
    - alive particle count
    - absorbed particle count
    - simulation running / paused state
  */
  particleCountEl.textContent = simulation.getAliveCount();
  absorbedCountEl.textContent = simulation.absorbed;
  simStatusEl.textContent = SIM_CONFIG.running ? "running" : "paused";
}


/* ============================================================================
   MAIN LOOP
   ============================================================================ */

function loop() {
  /*
    Main browser animation loop.

    For each frame:
    1. update simulation state
    2. render the scene
    3. refresh visible UI metrics
    4. request the next animation frame
  */
  simulation.update();
  simulation.render();
  updateStats();

  requestAnimationFrame(loop);
}


/* ============================================================================
   UI EVENT BINDINGS
   ============================================================================ */

spawnBtn.addEventListener("click", () => {
  /*
    Repopulate the simulation with a fresh particle set.
  */
  simulation.spawnParticles();
});

toggleMotionBtn.addEventListener("click", () => {
  /*
    Toggle the global running state of the browser simulation.
  */
  SIM_CONFIG.running = !SIM_CONFIG.running;
});


/* ============================================================================
   STARTUP
   ============================================================================ */

loop();
