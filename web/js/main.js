/*
============================================================================
BlackHole Simulation System - Web Main Entry Point
----------------------------------------------------------------------------
This module initializes the browser-side viewer and keeps it synchronized
with the Python simulation state exported as JSON.

Responsibilities:
- initialize canvas and simulation
- fetch external state from Python export
- pass external state into the browser simulation
- update runtime UI counters
- maintain the animation loop
============================================================================
*/


/*
============================================================================
DOM REFERENCES
============================================================================
*/

const canvas = document.getElementById("blackholeCanvas");
const particleCountEl = document.getElementById("particleCount");
const absorbedCountEl = document.getElementById("absorbedCount");
const simStatusEl = document.getElementById("simStatus");
const spawnBtn = document.getElementById("spawnBtn");
const toggleMotionBtn = document.getElementById("toggleMotionBtn");


/*
============================================================================
SIMULATION INSTANCE
============================================================================
*/

const simulation = new BlackHoleSimulation(canvas, SIM_CONFIG);


/*
============================================================================
EXTERNAL STATE FETCH (STEP 4 CORE)
============================================================================
*/

async function fetchState() {
  /*
    Fetch exported state from the Python simulation.

    Expected file:
    ../data/output/state.json

    Returns:
    - parsed JSON object on success
    - null on failure
  */
  try {
    const response = await fetch("../data/output/state.json?ts=" + Date.now());

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.warn("Unable to fetch external simulation state:", error);
    return null;
  }
}


/*
============================================================================
UI UPDATES
============================================================================
*/

function updateStats() {
  /*
    Refresh compact runtime stats shown in the web UI.
  */
  if (particleCountEl) {
    particleCountEl.textContent = simulation.getAliveCount();
  }

  if (absorbedCountEl) {
    absorbedCountEl.textContent = simulation.absorbed;
  }

  if (simStatusEl) {
    simStatusEl.textContent = SIM_CONFIG.running ? "running" : "paused";
  }
}


/*
============================================================================
BUTTON BINDINGS
============================================================================
*/

if (spawnBtn) {
  spawnBtn.addEventListener("click", () => {
    /*
      In external mode this mainly acts as a local fallback trigger.
      If external state is active, the Python simulation remains authoritative.
    */
    if (!simulation.externalMode) {
      simulation.spawnParticles(SIM_CONFIG.particleCount);
    }
  });
}

if (toggleMotionBtn) {
  toggleMotionBtn.addEventListener("click", () => {
    /*
      Toggle browser-side update state.

      In external mode this mainly affects UI state. The Python simulation
      remains the authoritative producer of state.json.
    */
    SIM_CONFIG.running = !SIM_CONFIG.running;
  });
}


/*
============================================================================
MAIN LOOP
============================================================================
*/

async function loop() {
  /*
    Main browser loop.

    Sequence:
    1. fetch external state
    2. load it into the simulation if available
    3. update local fallback simulation if external mode is off
    4. render scene
    5. refresh UI
    6. request next frame
  */

  if (SIM_CONFIG.running) {
    const state = await fetchState();

    if (state) {
      simulation.loadExternalState(state);
    } else {
      simulation.update();
    }
  }

  simulation.render();
  updateStats();

  requestAnimationFrame(loop);
}


/*
============================================================================
STARTUP
============================================================================
*/

updateStats();
loop();
