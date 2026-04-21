"""
Black Hole Simulation — Main Simulation Loop (v0.5)

This module contains the main interactive simulation entry point of the
BlackHole Simulation System.

It is the highest-level runtime module of the Python layer and is responsible
for coordinating:

- simulation initialization
- particle spawning
- runtime controls
- event handling
- particle updates
- advanced visual effects
- runtime statistics
- rendering orchestration

The current implementation includes multiple active systems layered on top of
the core gravity simulation:

    1-5         spawn mode selection (Edge / Disk / Spiral / Cluster / Rain)
    C           color mode cycling
    F11         fullscreen toggle
    F12         screenshot
    SPACE       pause
    R           reset
    D / H / T   debug / HUD / trail toggle
    +/-         particle count adjustment
    UP / DOWN   time scale control
    Scroll      black hole mass adjustment
    LMB / RMB   attract / repel local mouse force

Active runtime systems:
    - absorption shockwaves
    - Hawking radiation style spontaneous emission
    - polar jet emission
    - milestone notifications
    - absorption sparkline
"""

import math
import random
import os
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple
from collections import deque

import pygame

from src.python.core.constants import (
    FPS, TEXT_COLOR, TEXT_SOFT_COLOR, TEXT_WARNING_COLOR, TEXT_ACCENT_COLOR,
    TEXT_SUCCESS_COLOR, TEXT_ERROR_COLOR,
    SPAWN_MODES, SPAWN_MODE_LABELS, SPAWN_EDGE, SPAWN_DISK, SPAWN_SPIRAL,
    SPAWN_CLUSTER, SPAWN_RAIN,
    COLOR_MODES, COLOR_SPEED,
    SHOCKWAVE_COLOR, HAWKING_COLOR, JET_COLOR,
    NOTIF_BG, NOTIF_BORDER,
)
from src.python.core.config_loader import load_config
from src.python.models.particle import Particle
from src.python.models.black_hole import BlackHole
from src.python.engine.simulation_step import update_particle
from src.python.render.draw import draw_scene, invalidate_starfield_cache

# Discrete runtime multipliers used to scale the effective simulation step.
TIME_SCALES = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0]


# ═══════════════════════════════════════════════════════════
#  EXTERNAL STATE EXPORT (STEP 2)
# ═══════════════════════════════════════════════════════════

OUTPUT_PATH = Path("data/output/state.json")


def export_state(particles, absorbed, black_hole=None):
    """
    Export the current simulation state to a JSON file.

    This file is intended to be consumed by the browser-based web layer,
    allowing the web interface to visualize the live state of the Python
    simulation without directly embedding the Python runtime.

    Exported fields:
    - active particle positions
    - absorbed particle count
    - black hole position and radii (if provided)
    - timestamp
    """
    data = {
        "particles": [
            {"x": p.x, "y": p.y}
            for p in particles if getattr(p, "alive", True)
        ],
        "absorbed": absorbed,
        "timestamp": time.time(),
    }

    if black_hole is not None:
        data["black_hole"] = {
            "x": black_hole.x,
            "y": black_hole.y,
            "mass": black_hole.mass,
            "event_horizon_radius": black_hole.event_horizon_radius,
            "accretion_radius": black_hole.accretion_radius,
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f)


# ═══════════════════════════════════════════════════════════
#  DATA STRUCTURES
# ═══════════════════════════════════════════════════════════

@dataclass
class SimulationStats:
    """
    Runtime statistics container.

    Tracks the global state of the simulation over time, including:
    - frame count
    - total absorbed particles
    - total respawned particles
    - Hawking emission count
    - jet emission count
    - peak alive particles
    - simulation time
    - a rolling absorption history used for the sparkline
    """

    frame_count: int = 0
    absorbed_total: int = 0
    respawned_total: int = 0
    hawking_emitted: int = 0
    jet_emitted: int = 0
    initial_count: int = 0
    peak_alive: int = 0
    sim_time: float = 0.0
    absorption_history: deque = field(default_factory=lambda: deque(maxlen=120))
    _abs_this_sec: int = 0
    _sec_timer: float = 0.0

    def tick(self, alive_count, dt, absorbed_frame=0):
        """
        Advance statistics by one frame.

        Updates:
        - frame count
        - simulation time
        - peak alive count
        - rolling absorption history
        """
        self.frame_count += 1
        self.sim_time += dt
        self.peak_alive = max(self.peak_alive, alive_count)
        self._abs_this_sec += absorbed_frame
        self._sec_timer += dt
        if self._sec_timer >= 0.5:
            self.absorption_history.append(self._abs_this_sec)
            self._abs_this_sec = 0
            self._sec_timer = 0.0

    def register_absorbed(self, count):
        """Register absorbed particles."""
        self.absorbed_total += count

    def register_respawn(self, count):
        """Register respawned particles."""
        self.respawned_total += count


@dataclass
class Shockwave:
    """
    Visual effect emitted when a particle is absorbed.

    The shockwave expands and fades until it becomes inactive.
    """

    x: float
    y: float
    radius: float = 0.0
    max_radius: float = 120.0
    alpha: float = 255.0
    speed: float = 4.0
    alive: bool = True

    def update(self):
        """Advance the shockwave animation."""
        self.radius += self.speed
        self.alpha -= 4.0
        if self.alpha <= 0 or self.radius > self.max_radius:
            self.alive = False


@dataclass
class Notification:
    """
    Lightweight UI notification message.

    Used for:
    - mode changes
    - screenshots
    - milestone events
    - reset feedback
    """

    text: str
    color: Tuple[int, int, int] = (200, 220, 255)
    timer: float = 3.0
    y_offset: float = 0.0
    alive: bool = True

    def update(self, dt):
        """Decrease visibility lifetime."""
        self.timer -= dt
        if self.timer <= 0:
            self.alive = False


# ═══════════════════════════════════════════════════════════
#  SPAWN MODES
# ═══════════════════════════════════════════════════════════

def spawn_edge(count, w, h, margin, smin, smax, bx, by):
    """
    Spawn particles around the outer boundaries of the simulation area.

    Particles are initialized outside or near the visible frame and given
    an inward-biased motion with a small tangential component.
    """
    particles = []
    for _ in range(count):
        side = random.randint(0, 3)
        if side == 0:
            x, y = random.uniform(-margin, w + margin), random.uniform(-margin, 0)
        elif side == 1:
            x, y = random.uniform(-margin, w + margin), random.uniform(h, h + margin)
        elif side == 2:
            x, y = random.uniform(-margin, 0), random.uniform(-margin, h + margin)
        else:
            x, y = random.uniform(w, w + margin), random.uniform(-margin, h + margin)

        vx, vy = random.uniform(smin, smax), random.uniform(smin, smax)
        dx, dy = bx - x, by - y
        d = math.hypot(dx, dy) + 1e-6
        s = random.uniform(0.3, 1.4)

        # Add a slight tangential component so motion is not purely radial.
        vx += (-dy / d) * s
        vy += (dx / d) * s

        particles.append(Particle(x=x, y=y, vx=vx, vy=vy))
    return particles


def spawn_disk(count, w, h, margin, smin, smax, bx, by):
    """
    Spawn particles inside an accretion-disk-like structure.

    Particles are placed around the black hole using radial and angular
    coordinates and given approximate tangential orbital velocity.
    """
    particles = []
    for _ in range(count):
        r = random.uniform(80, 280)
        a = random.uniform(0, 2 * math.pi)
        x, y = bx + math.cos(a) * r, by + math.sin(a) * r

        # Approximate tangential orbital speed.
        v_orb = math.sqrt(0.48 * 10000 / max(r, 1)) * random.uniform(0.7, 1.1)
        vx, vy = -math.sin(a) * v_orb, math.cos(a) * v_orb

        # Small perturbation prevents an overly rigid distribution.
        vx += random.uniform(-0.3, 0.3)
        vy += random.uniform(-0.3, 0.3)

        particles.append(Particle(x=x, y=y, vx=vx, vy=vy))
    return particles


def spawn_spiral(count, w, h, margin, smin, smax, bx, by):
    """
    Spawn particles in a two-arm spiral pattern.

    This is a visual-structural spawn mode intended to generate a more
    organized large-scale shape at initialization.
    """
    particles = []
    for i in range(count):
        arm = i % 2
        t = (i / count) * 4 * math.pi
        r = 60 + t * 20 + random.uniform(-15, 15)
        a = t + arm * math.pi + random.uniform(-0.2, 0.2)
        x, y = bx + math.cos(a) * r, by + math.sin(a) * r

        v_orb = math.sqrt(0.48 * 10000 / max(r, 1)) * random.uniform(0.6, 1.0)
        vx, vy = -math.sin(a) * v_orb, math.cos(a) * v_orb
        particles.append(Particle(x=x, y=y, vx=vx, vy=vy))
    return particles


def spawn_cluster(count, w, h, margin, smin, smax, bx, by):
    """
    Spawn particles in four dense clusters directed toward the center.

    This mode creates localized structures that then collapse inward.
    """
    particles = []
    centers = [
        (bx - 250, by - 200),
        (bx + 250, by - 200),
        (bx - 250, by + 200),
        (bx + 250, by + 200),
    ]

    for i in range(count):
        cx, cy = centers[i % 4]
        x = cx + random.gauss(0, 30)
        y = cy + random.gauss(0, 30)

        dx, dy = bx - x, by - y
        d = math.hypot(dx, dy) + 1e-6
        s = random.uniform(0.5, 1.5)

        vx = (dx / d) * s * 0.5 + (-dy / d) * s * 0.3 + random.uniform(-0.3, 0.3)
        vy = (dy / d) * s * 0.5 + (dx / d) * s * 0.3 + random.uniform(-0.3, 0.3)

        particles.append(Particle(x=x, y=y, vx=vx, vy=vy))
    return particles


def spawn_rain(count, w, h, margin, smin, smax, bx, by):
    """
    Spawn particles as a downward rain from above the simulation window.

    This mode is primarily visual and produces a strong inflow pattern.
    """
    particles = []
    for _ in range(count):
        x = random.uniform(0, w)
        y = random.uniform(-margin, -10)
        vx = random.uniform(-0.5, 0.5)
        vy = random.uniform(1.0, 3.0)
        particles.append(Particle(x=x, y=y, vx=vx, vy=vy))
    return particles


# Mapping between spawn mode identifiers and their corresponding generators.
SPAWN_FUNCS = {
    SPAWN_EDGE: spawn_edge,
    SPAWN_DISK: spawn_disk,
    SPAWN_SPIRAL: spawn_spiral,
    SPAWN_CLUSTER: spawn_cluster,
    SPAWN_RAIN: spawn_rain,
}


def spawn_particles(count, w, h, margin, smin, smax, bx, by, mode=SPAWN_EDGE):
    """
    Dispatch particle creation using the selected spawn mode.
    """
    return SPAWN_FUNCS.get(mode, spawn_edge)(count, w, h, margin, smin, smax, bx, by)


# ═══════════════════════════════════════════════════════════
#  SECONDARY EMISSION SYSTEMS
# ═══════════════════════════════════════════════════════════

def emit_hawking(bh, count=2):
    """
    Emit small particles around the event-horizon region.

    This is a stylized visual approximation inspired by Hawking radiation.
    It is not intended as a physical implementation of the phenomenon.
    """
    particles = []
    for _ in range(count):
        a = random.uniform(0, 2 * math.pi)
        r = bh.event_horizon_radius * random.uniform(1.1, 1.6)
        x, y = bh.x + math.cos(a) * r, bh.y + math.sin(a) * r
        spd = random.uniform(3.0, 8.0)
        vx, vy = math.cos(a) * spd, math.sin(a) * spd
        p = Particle(x=x, y=y, vx=vx, vy=vy, mass=0.3, radius=1,
                     color=(180, 220, 255))
        particles.append(p)
    return particles


def emit_jet(bh, count=3):
    """
    Emit high-speed particles along the vertical axis.

    This system creates a stylized polar jet effect and is primarily intended
    as a visual and conceptual extension of the simulation.
    """
    particles = []
    for _ in range(count):
        direction = random.choice([-1, 1])  # upward or downward
        x = bh.x + random.uniform(-8, 8)
        y = bh.y + direction * bh.event_horizon_radius * 1.2
        vx = random.uniform(-0.5, 0.5)
        vy = direction * random.uniform(8.0, 14.0)
        p = Particle(x=x, y=y, vx=vx, vy=vy, mass=0.2, radius=1,
                     color=(120, 180, 255))
        particles.append(p)
    return particles


# ═══════════════════════════════════════════════════════════
#  SIMULATION SETUP HELPERS
# ═══════════════════════════════════════════════════════════

def create_starfield(w, h, count=220):
    """
    Create a cached procedural starfield used as background decoration.
    """
    return [{"x": random.randint(0, w), "y": random.randint(0, h),
             "radius": random.choice([1, 1, 1, 2]), "alpha": random.randint(60, 220),
             "bright": random.random() < 0.15, "kind": random.choice([0, 0, 0, 0, 0, 1, 2])}
            for _ in range(count)]


def create_black_hole(config):
    """
    Build the central black hole instance from loaded configuration.
    """
    return BlackHole(
        x=config["window_width"] / 2,
        y=config["window_height"] / 2,
        mass=config["black_hole_mass"],
        event_horizon_radius=config["event_horizon_radius"],
        accretion_radius=config["accretion_radius"],
    )


def reset_simulation(config, spawn_mode=SPAWN_EDGE):
    """
    Reset the simulation to a clean state.

    Recreates:
    - the black hole
    - the particle set
    - runtime statistics
    - background starfield
    """
    bh = create_black_hole(config)
    parts = spawn_particles(config["particle_count"], config["window_width"],
        config["window_height"], config["particle_spawn_margin"],
        config["initial_speed_min"], config["initial_speed_max"], bh.x, bh.y, spawn_mode)
    stats = SimulationStats(initial_count=len(parts), peak_alive=len(parts))
    stars = create_starfield(config["window_width"], config["window_height"],
                             config.get("starfield_count", 220))
    invalidate_starfield_cache()
    return bh, parts, stats, stars


def apply_mouse_force(particles, mx, my, attract=True, strength=600.0):
    """
    Apply an external local mouse-based force to nearby particles.

    Left mouse button:
        attraction

    Right mouse button:
        repulsion

    The force decays with distance and affects only particles inside a local
    influence region.
    """
    for p in particles:
        if not p.alive:
            continue
        dx, dy = mx - p.x, my - p.y
        d2 = dx * dx + dy * dy
        if d2 > 200000:
            continue
        d = math.sqrt(d2) if d2 > 1 else 1.0
        f = strength / (d2 + 100)
        if not attract:
            f = -f
        p.vx += (dx / d) * f
        p.vy += (dy / d) * f


def respawn_if_needed(particles, config, bx, by, mode=SPAWN_EDGE):
    """
    Maintain a minimum population of alive particles.

    If the alive population drops below the configured threshold, a new batch
    is spawned using the currently selected spawn mode.
    """
    alive = [p for p in particles if p.alive]
    if len(alive) >= config.get("respawn_threshold", 30):
        return alive, 0

    batch = config.get("respawn_batch_size", 100)
    new = spawn_particles(batch, config["window_width"], config["window_height"],
        config["particle_spawn_margin"], config["initial_speed_min"],
        config["initial_speed_max"], bx, by, mode)
    alive.extend(new)
    return alive, len(new)


# ═══════════════════════════════════════════════════════════
#  RENDERING HELPERS
# ═══════════════════════════════════════════════════════════

def draw_shockwaves(screen, shockwaves):
    """
    Draw all active shockwave effects on a transparent overlay.
    """
    if not shockwaves:
        return

    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for sw in shockwaves:
        if not sw.alive:
            continue
        a = max(0, int(sw.alpha))
        col = (*SHOCKWAVE_COLOR, a)
        pygame.draw.circle(s, col, (int(sw.x), int(sw.y)), int(sw.radius), 2)
        if sw.radius > 10:
            col2 = (*SHOCKWAVE_COLOR, a // 3)
            pygame.draw.circle(s, col2, (int(sw.x), int(sw.y)), int(sw.radius * 0.6), 1)
    screen.blit(s, (0, 0))


def draw_notifications(screen, notifications, font):
    """
    Draw stacked notifications in the upper-right area of the screen.
    """
    if not notifications:
        return

    w = screen.get_width()
    y = 80
    for n in notifications:
        if not n.alive:
            continue
        fade = min(1.0, n.timer / 0.5) if n.timer < 0.5 else 1.0
        alpha = int(220 * fade)
        txt = font.render(n.text, True, (*n.color,))
        tw = txt.get_width() + 24
        panel = pygame.Surface((tw, 28), pygame.SRCALPHA)
        panel.fill((*NOTIF_BG[:3], int(NOTIF_BG[3] * fade)))
        pygame.draw.rect(panel, (*NOTIF_BORDER[:3], int(NOTIF_BORDER[3] * fade)), (0, 0, tw, 28), 1)
        panel.blit(txt, (12, 4))
        panel.set_alpha(alpha)
        screen.blit(panel, (w - tw - 28, y))
        y += 34


def draw_title(screen, tf, sf, w, spawn_mode, color_mode, time_scale):
    """
    Draw the simulation title and compact runtime context information.
    """
    t = tf.render("BLACK HOLE SIMULATION", True, (235, 235, 245))
    screen.blit(t, (w - t.get_width() - 28, 14))

    mode_info = f"Spawn: {SPAWN_MODE_LABELS.get(spawn_mode, spawn_mode)}  Color: {color_mode.title()}  Time: {time_scale:.2f}x"
    s = sf.render(mode_info, True, TEXT_ACCENT_COLOR)
    screen.blit(s, (w - s.get_width() - 28, 44))

    keys = sf.render("1-5 spawn · C color · F11 fullscreen · F12 screenshot", True, TEXT_SOFT_COLOR)
    screen.blit(keys, (w - keys.get_width() - 28, 62))


def draw_sparkline(screen, data, x, y, w, h, color=(255, 160, 80)):
    """
    Draw a compact sparkline showing recent absorption activity.
    """
    if len(data) < 2:
        return

    s = pygame.Surface((w, h), pygame.SRCALPHA)
    s.fill((10, 12, 24, 160))
    pygame.draw.rect(s, (40, 50, 80, 80), (0, 0, w, h), 1)

    mx = max(data) if max(data) > 0 else 1
    points = []
    for i, v in enumerate(data):
        px = int(i / (len(data) - 1) * (w - 4)) + 2
        py = h - 2 - int((v / mx) * (h - 4))
        points.append((px, py))

    if len(points) >= 2:
        pygame.draw.lines(s, color, False, points, 1)

        # Fill area below the line for stronger readability.
        fill_points = points + [(points[-1][0], h - 2), (points[0][0], h - 2)]
        pygame.draw.polygon(s, (*color, 30), fill_points)

    screen.blit(s, (x, y))
    f = pygame.font.SysFont("consolas", 10)
    screen.blit(f.render("Absorption Rate", True, TEXT_SOFT_COLOR), (x, y - 14))


# ═══════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════

def main():
    """
    Run the main interactive simulation loop.

    This function is responsible for:
    - loading configuration
    - initializing pygame
    - handling user interaction
    - updating simulation state
    - triggering secondary systems
    - rendering the final frame
    """
    config = load_config()
    pygame.init()
    pygame.display.set_caption("Black Hole Simulation — v0.5")

    fullscreen = False
    screen = pygame.display.set_mode((config["window_width"], config["window_height"]))
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Consolas", 13)
    title_font = pygame.font.SysFont("Consolas", 20, bold=True)
    notif_font = pygame.font.SysFont("Consolas", 13)

    # Default indices for spawn and color behavior.
    spawn_mode_idx = 0
    color_mode_idx = 0

    bh, particles, stats, stars = reset_simulation(config, SPAWN_MODES[spawn_mode_idx])

    paused = False
    show_debug = False
    show_hud = True
    show_trails = config.get("show_trails", True)
    running = True
    frame = 0

    # Cached runtime configuration values.
    gravity = config["gravity_constant"]
    softening = config["softening"]
    damping = config.get("damping", 0.999)
    max_speed = config.get("max_speed", 14.0)
    sim_dt = config.get("dt", 1.0)
    trail_length = config.get("trail_length", 35)
    show_starfield = config.get("show_starfield", True)
    ring_count = config.get("ring_count", 8)

    # Mouse interaction state.
    mouse_active = False
    mouse_mode = "attract"

    # Start at 1.0x simulation speed.
    time_scale_idx = 3

    # Runtime visual and notification systems.
    shockwaves: List[Shockwave] = []
    notifications: List[Notification] = []
    hawking_timer = 0.0
    jet_timer = 0.0

    # Absorption milestones used for on-screen notifications.
    absorption_milestones = {50, 100, 200, 500, 1000, 2000, 5000}
    triggered_milestones = set()

    while running:
        dt = clock.tick(FPS) / 1000.0
        fps = clock.get_fps()
        frame += 1
        time_scale = TIME_SCALES[time_scale_idx]
        spawn_mode = SPAWN_MODES[spawn_mode_idx]
        color_mode = COLOR_MODES[color_mode_idx]

        # ─── EVENT HANDLING ────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_r:
                    bh, particles, stats, stars = reset_simulation(config, spawn_mode)
                    shockwaves.clear()
                    notifications.clear()
                    triggered_milestones.clear()
                    paused = False
                    notifications.append(
                        Notification(f"Reset — {SPAWN_MODE_LABELS[spawn_mode]}", TEXT_SUCCESS_COLOR)
                    )

                elif event.key == pygame.K_d:
                    show_debug = not show_debug

                elif event.key == pygame.K_h:
                    show_hud = not show_hud

                elif event.key == pygame.K_t:
                    show_trails = not show_trails

                elif event.key == pygame.K_c:
                    color_mode_idx = (color_mode_idx + 1) % len(COLOR_MODES)
                    notifications.append(
                        Notification(f"Color: {COLOR_MODES[color_mode_idx].title()}", TEXT_ACCENT_COLOR)
                    )

                elif event.key == pygame.K_UP:
                    time_scale_idx = min(time_scale_idx + 1, len(TIME_SCALES) - 1)

                elif event.key == pygame.K_DOWN:
                    time_scale_idx = max(time_scale_idx - 1, 0)

                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    idx = event.key - pygame.K_1
                    if 0 <= idx < len(SPAWN_MODES):
                        spawn_mode_idx = idx
                        bh, particles, stats, stars = reset_simulation(config, SPAWN_MODES[idx])
                        shockwaves.clear()
                        triggered_milestones.clear()
                        notifications.append(
                            Notification(f"Spawn: {SPAWN_MODE_LABELS[SPAWN_MODES[idx]]}", TEXT_ACCENT_COLOR)
                        )

                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    new = spawn_particles(
                        80,
                        config["window_width"],
                        config["window_height"],
                        config["particle_spawn_margin"],
                        config["initial_speed_min"],
                        config["initial_speed_max"],
                        bh.x,
                        bh.y,
                        spawn_mode,
                    )
                    particles.extend(new)
                    stats.register_respawn(len(new))

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    alive = [p for p in particles if p.alive]
                    for p in alive[-80:]:
                        p.kill()

                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((config["window_width"], config["window_height"]))
                    invalidate_starfield_cache()

                elif event.key == pygame.K_F12:
                    # Save a screenshot in the output directory.
                    sdir = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "..", "data", "output"
                    )
                    os.makedirs(sdir, exist_ok=True)
                    spath = os.path.join(sdir, f"screenshot_{frame}.png")
                    pygame.image.save(screen, spath)
                    notifications.append(
                        Notification(f"Screenshot saved: {os.path.basename(spath)}", TEXT_SUCCESS_COLOR)
                    )

            elif event.type == pygame.MOUSEWHEEL:
                # Scroll modifies black hole mass in real time.
                bh.mass = max(1000, bh.mass + event.y * 500)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_active = True
                    mouse_mode = "attract"
                elif event.button == 3:
                    mouse_active = True
                    mouse_mode = "repel"

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    mouse_active = False

        # ─── MOUSE FORCE APPLICATION ──────────────────────────────────────
        if mouse_active and not paused:
            mx, my = pygame.mouse.get_pos()
            apply_mouse_force(particles, mx, my, attract=(mouse_mode == "attract"))

        # ─── SIMULATION UPDATE ────────────────────────────────────────────
        if not paused:
            effective_dt = sim_dt * time_scale
            sub_steps = max(1, int(time_scale))
            step_dt = effective_dt / sub_steps

            absorbed_frame = 0

            for _ in range(sub_steps):
                for p in particles:
                    if not p.alive:
                        continue

                    old_x, old_y = p.x, p.y
                    result = update_particle(
                        p, bh, gravity, softening, damping, max_speed, step_dt, trail_length
                    )

                    # Track particle lifetime information only if still alive.
                    if p.alive:
                        p.tick_age()
                        p.distance_traveled += math.hypot(p.x - old_x, p.y - old_y)
                        if result["distance"] is not None:
                            p.min_approach = min(p.min_approach, result["distance"])

                    if result["absorbed"]:
                        absorbed_frame += 1
                        shockwaves.append(Shockwave(x=p.x, y=p.y))

            if absorbed_frame > 0:
                stats.register_absorbed(absorbed_frame)

            # Trigger milestone notifications once.
            for m in absorption_milestones:
                if stats.absorbed_total >= m and m not in triggered_milestones:
                    triggered_milestones.add(m)
                    notifications.append(Notification(f"🌀 {m} particles absorbed!", (255, 200, 80)))

            # Periodic Hawking-style emission.
            hawking_timer += dt * time_scale
            if hawking_timer > 2.0:
                hawking_timer = 0.0
                hp = emit_hawking(bh, count=random.randint(1, 3))
                particles.extend(hp)
                stats.hawking_emitted += len(hp)

            # Periodic jet emission.
            jet_timer += dt * time_scale
            if jet_timer > 5.0:
                jet_timer = 0.0
                jp = emit_jet(bh, count=random.randint(2, 5))
                particles.extend(jp)
                stats.jet_emitted += len(jp)

            # Respawn particles if population drops below threshold.
            particles, respawned = respawn_if_needed(particles, config, bh.x, bh.y, spawn_mode)
            if respawned > 0:
                stats.register_respawn(respawned)

            alive_count = sum(1 for p in particles if p.alive)
            stats.tick(alive_count, dt * time_scale, absorbed_frame)

            # ─── STATE EXPORT FOR WEB LAYER (STEP 2) ──────────────────────
            # Export every 3 frames to avoid unnecessary file writes at full FPS.
            if frame % 3 == 0:
                export_state(particles, stats.absorbed_total, bh)

        # ─── VISUAL EFFECT UPDATES ────────────────────────────────────────
        for sw in shockwaves:
            sw.update()
        shockwaves = [sw for sw in shockwaves if sw.alive]

        for n in notifications:
            n.update(dt)
        notifications = [n for n in notifications if n.alive]

        # ─── RENDERING ────────────────────────────────────────────────────
        mouse_pos = pygame.mouse.get_pos() if mouse_active else None

        draw_scene(
            screen, bh, particles,
            debug=show_debug, show_hud=show_hud,
            show_starfield=show_starfield, show_trails=show_trails,
            stars=stars, ring_count=ring_count, max_speed=max_speed,
            frame=frame, stats=stats, config=config, fps=fps,
            mouse_active=mouse_active, mouse_pos=mouse_pos, mouse_mode=mouse_mode,
            paused=paused, time_scale=time_scale, color_mode=color_mode,
        )

        draw_shockwaves(screen, shockwaves)
        draw_title(screen, title_font, font, screen.get_width(), spawn_mode, color_mode, time_scale)
        draw_notifications(screen, notifications, notif_font)

        # Draw the absorption-rate sparkline when HUD is enabled.
        if show_hud and len(stats.absorption_history) > 2:
            draw_sparkline(
                screen,
                list(stats.absorption_history),
                14,
                screen.get_height() - 120,
                180,
                50,
            )

        if paused:
            lbl = title_font.render("⏸ PAUSED", True, TEXT_WARNING_COLOR)
            screen.blit(lbl, (screen.get_width() // 2 - lbl.get_width() // 2, screen.get_height() // 2 - 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
