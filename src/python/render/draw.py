"""
Rendering 2D avanzato — v0.4.0

This module contains the full 2D rendering layer of the
BlackHole Simulation System.

It is responsible for drawing the visible state of the simulation and all
secondary visual systems currently active in the project.

Main rendering responsibilities:
- background and starfield
- black hole visual structure
- accretion disk layers
- particle rendering
- trails and color modes
- HUD and metrics
- minimap
- bottom control bar
- mouse interaction feedback
- warning overlays

The file is intentionally large because it acts as the main visual assembly
layer of the project. Its logic is grouped into sections to keep responsibilities
clear and to avoid mixing low-level drawing helpers with scene orchestration.
"""

import math
import pygame
from typing import Optional

from src.python.core.constants import (
    COLOR_SPEED, COLOR_ENERGY, COLOR_DISTANCE, COLOR_AGE, COLOR_REGION,
    PARTICLE_DISTANCE_COLORS, PARTICLE_AGE_COLORS, PARTICLE_ENERGY_COLORS,
    EPSILON, REGION_EVENT_HORIZON, REGION_ACCRETION_ZONE,
    BACKGROUND_COLOR, EVENT_HORIZON_COLOR, PHOTON_RING_COLOR,
    ACCRETION_INNER_COLOR, ACCRETION_MID_COLOR, ACCRETION_OUTER_COLOR,
    ACCRETION_EDGE_COLOR, ACCRETION_BASE_COLOR,
    GLOW_INNER_COLOR, GLOW_OUTER_COLOR, LENSING_COLOR,
    PARTICLE_SPEED_COLORS, PARTICLE_OUTER_COLOR,
    PARTICLE_ACCRETION_COLOR, PARTICLE_EVENT_COLOR,
    TRAIL_OUTER_COLOR, TRAIL_ACCRETION_COLOR, TRAIL_EVENT_COLOR,
    STAR_COLOR_DIM, STAR_COLOR_BRIGHT, STAR_COLOR_WARM, STAR_COLOR_BLUE,
    TEXT_SOFT_COLOR, TEXT_WARNING_COLOR, TEXT_ACCENT_COLOR,
    TEXT_SUCCESS_COLOR, TEXT_COLOR, TEXT_ERROR_COLOR,
    HUD_BG_COLOR, HUD_BORDER_COLOR, HUD_BAR_BG, HUD_BAR_FILL,
    HUD_BAR_WARN, HUD_BAR_CRIT, DEBUG_LINE_COLOR,
)
from src.python.core.vector_utils import clamp, lerp
from src.python.engine.gravity_engine import classify_region_from_distance


# ═══════════════════════════════════════════════════════════
#  COLOR HELPERS
# ═══════════════════════════════════════════════════════════

def mix_color(a, b, t):
    """
    Linearly interpolate between two RGB colors.

    Parameters
    ----------
    a, b :
        RGB tuples.
    t :
        Blend factor in [0, 1].

    Returns
    -------
    tuple
        Mixed RGB color.
    """
    t = clamp(t, 0.0, 1.0)
    return (
        int(lerp(a[0], b[0], t)),
        int(lerp(a[1], b[1], t)),
        int(lerp(a[2], b[2], t)),
    )


def speed_to_color(speed, max_speed):
    """
    Map particle speed to the configured speed palette.

    This helper is used by the default speed-based color mode and also by
    several secondary render systems that need a speed-aware color estimate.
    """
    t = clamp(speed / max(max_speed, 0.01), 0.0, 1.0)
    idx = t * (len(PARTICLE_SPEED_COLORS) - 1)
    i = int(idx)
    f = idx - i
    if i >= len(PARTICLE_SPEED_COLORS) - 1:
        return PARTICLE_SPEED_COLORS[-1]
    return mix_color(PARTICLE_SPEED_COLORS[i], PARTICLE_SPEED_COLORS[i + 1], f)


def gradient_color(t, palette):
    """
    Map a normalized scalar t in [0, 1] onto a color palette.
    """
    t = clamp(t, 0.0, 1.0)
    idx = t * (len(palette) - 1)
    i = int(idx)
    f = idx - i
    if i >= len(palette) - 1:
        return palette[-1]
    return mix_color(palette[i], palette[i + 1], f)


def particle_color_by_mode(p_data, mode, max_speed, max_age=600):
    """
    Compute particle color according to the currently selected color mode.

    Supported modes include:
    - speed
    - energy
    - distance
    - age
    - region

    The input p_data is the precomputed particle rendering dictionary returned
    by _pdata(...), which avoids repeating the same computations across
    multiple draw stages.
    """
    if mode == COLOR_SPEED:
        return speed_to_color(p_data["spd"], max_speed)

    elif mode == COLOR_ENERGY:
        # Normalized kinetic energy approximation.
        ke = 0.5 * p_data["spd"] ** 2
        max_ke = 0.5 * max_speed ** 2
        return gradient_color(ke / max(max_ke, 0.01), PARTICLE_ENERGY_COLORS)

    elif mode == COLOR_DISTANCE:
        # Normalized distance from the center.
        t = clamp(p_data["dist"] / 500.0, 0, 1)
        return gradient_color(1.0 - t, PARTICLE_DISTANCE_COLORS)

    elif mode == COLOR_AGE:
        age = p_data.get("age", 0)
        return gradient_color(clamp(age / max_age, 0, 1), PARTICLE_AGE_COLORS)

    elif mode == COLOR_REGION:
        r = p_data["region"]
        if r == REGION_EVENT_HORIZON:
            return PARTICLE_EVENT_COLOR
        elif r == REGION_ACCRETION_ZONE:
            return PARTICLE_ACCRETION_COLOR
        else:
            return PARTICLE_OUTER_COLOR

    return speed_to_color(p_data["spd"], max_speed)


# ═══════════════════════════════════════════════════════════
#  BACKGROUND CACHE
# ═══════════════════════════════════════════════════════════

_bg_cache = None
_bg_size = (0, 0)


def draw_background(screen):
    """
    Draw the cached radial background.

    The background is regenerated only when the screen size changes.
    This avoids rebuilding the same layered glow each frame.
    """
    global _bg_cache, _bg_size
    w, h = screen.get_size()

    if _bg_cache is None or _bg_size != (w, h):
        _bg_cache = pygame.Surface((w, h))
        _bg_cache.fill(BACKGROUND_COLOR)

        cx, cy = w // 2, h // 2
        mr = max(w, h) // 2 + 80
        temp = pygame.Surface((mr * 2, mr * 2), pygame.SRCALPHA)

        for i in range(18, 0, -1):
            t = i / 18
            r = int(mr * t)
            pygame.draw.circle(
                temp,
                (
                    int(16 * t + 3 * (1 - t)),
                    int(18 * t + 4 * (1 - t)),
                    int(35 * t + 8 * (1 - t)),
                    int(50 * t),
                ),
                (mr, mr),
                r,
            )

        _bg_cache.blit(temp, (cx - mr, cy - mr))
        _bg_size = (w, h)

    screen.blit(_bg_cache, (0, 0))


# ═══════════════════════════════════════════════════════════
#  STARFIELD CACHE
# ═══════════════════════════════════════════════════════════

_star_cache = None
_star_size = (0, 0)


def draw_starfield(screen, stars=None, count=220):
    """
    Draw the cached starfield.

    If a procedural or precomputed star list is provided, it is used to build
    the cache. Otherwise a fallback deterministic pattern is generated.
    """
    global _star_cache, _star_size
    w, h = screen.get_size()

    if _star_cache is None or _star_size != (w, h):
        _star_cache = pygame.Surface((w, h), pygame.SRCALPHA)
        _star_size = (w, h)

        if stars:
            for s in stars:
                x, y = int(s.get("x", 0)), int(s.get("y", 0))
                r = max(1, int(s.get("radius", 1)))
                a = int(s.get("alpha", 120))
                k = s.get("kind", 0)
                c = (
                    STAR_COLOR_WARM if k == 1
                    else STAR_COLOR_BLUE if k == 2
                    else STAR_COLOR_BRIGHT if s.get("bright")
                    else STAR_COLOR_DIM
                )
                pygame.draw.circle(_star_cache, (*c, a), (x, y), r)
        else:
            for i in range(count):
                x, y = (i * 73) % w, (i * 131) % h
                r = 1 if i % 7 else 2
                a = 50 + (i * 37) % 170
                c = (
                    STAR_COLOR_WARM if i % 17 == 0
                    else STAR_COLOR_BLUE if i % 13 == 0
                    else STAR_COLOR_BRIGHT if i % 11 == 0
                    else STAR_COLOR_DIM
                )
                pygame.draw.circle(_star_cache, (*c, a), (x, y), r)

    screen.blit(_star_cache, (0, 0))


def invalidate_starfield_cache():
    """
    Invalidate both background and starfield caches.

    This is typically required after a resize, fullscreen switch, or any
    change that invalidates cached screen-size-dependent surfaces.
    """
    global _star_cache, _bg_cache
    _star_cache = None
    _bg_cache = None


# ═══════════════════════════════════════════════════════════
#  BLACK HOLE AND ACCRETION VISUALS
# ═══════════════════════════════════════════════════════════

def draw_accretion_disk(screen, bh, frame=0):
    """
    Draw the accretion-disk region around the black hole.

    This includes:
    - diffuse nebula glow
    - concentric multi-band disk
    - rotating disk particles / dots
    - disk boundary outlines
    """
    cx, cy = int(bh.x), int(bh.y)
    ar = int(bh.accretion_radius)

    # Diffuse nebula glow in the accretion zone.
    neb_r = int(ar * 1.3)
    neb_s = neb_r * 2 + 4
    neb = pygame.Surface((neb_s, neb_s), pygame.SRCALPHA)
    nc = neb_s // 2
    for i in range(10, 0, -1):
        t = i / 10
        pygame.draw.circle(neb, (255, 120, 50, int(8 * t)), (nc, nc), int(neb_r * t))
    screen.blit(neb, (cx - nc, cy - nc))

    # Multi-band accretion structure.
    size = ar * 2 + 30
    temp = pygame.Surface((size, size), pygame.SRCALPHA)
    c = size // 2
    bands = [
        (1.0, ACCRETION_EDGE_COLOR, 28, 10),
        (0.88, ACCRETION_OUTER_COLOR, 34, 7),
        (0.75, ACCRETION_MID_COLOR, 38, 5),
        (0.62, ACCRETION_INNER_COLOR, 30, 4),
        (0.50, (255, 80, 25), 20, 3),
    ]
    for factor, color, alpha, width in bands:
        r = int(ar * factor)
        pygame.draw.circle(temp, (*color, alpha), (c, c), r, width)
    screen.blit(temp, (cx - c, cy - c))

    # Rotating accretion dots for visual motion.
    dot_count = 24
    time_angle = frame * 0.008
    dot_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for i in range(dot_count):
        orbit_r = ar * (0.55 + 0.4 * ((i % 5) / 5))
        speed_factor = 1.0 / max(0.5, orbit_r / ar)
        a = time_angle * speed_factor * 3 + (i * 2 * math.pi / dot_count)
        dx = int(math.cos(a) * orbit_r)
        dy = int(math.sin(a) * orbit_r)
        dot_alpha = int(40 + 30 * math.sin(frame * 0.02 + i))
        dot_r = 2 if i % 3 else 1
        color_t = (orbit_r - ar * 0.5) / max(1, ar * 0.5)
        dot_color = mix_color(ACCRETION_INNER_COLOR, ACCRETION_EDGE_COLOR, color_t)
        pygame.draw.circle(dot_surf, (*dot_color, dot_alpha), (c + dx, c + dy), dot_r)
    screen.blit(dot_surf, (cx - c, cy - c))

    pygame.draw.circle(screen, ACCRETION_OUTER_COLOR, (cx, cy), ar, 1)
    pygame.draw.circle(screen, ACCRETION_BASE_COLOR, (cx, cy), int(ar * 0.5), 1)


def draw_black_hole_core(screen, bh, frame=0):
    """
    Draw the core black hole visual structure.

    This includes:
    - lensing rings
    - outer glow
    - pulsating photon ring
    - event horizon core
    """
    cx, cy = int(bh.x), int(bh.y)
    ehr = int(bh.event_horizon_radius)

    lr = int(ehr * 4.5)
    ls = lr * 2 + 4
    lens = pygame.Surface((ls, ls), pygame.SRCALPHA)
    lc = ls // 2
    for i in range(6):
        r = int(ehr * 2.5 + i * ehr * 0.35)
        col = (*LENSING_COLOR, max(4, 18 - i * 3))
        pygame.draw.circle(lens, col, (lc, lc), r, 1)
    screen.blit(lens, (cx - lc, cy - lc))

    gr = int(ehr * 3.5)
    gs = gr * 2 + 4
    glow = pygame.Surface((gs, gs), pygame.SRCALPHA)
    gc = gs // 2
    for i in range(24, 0, -1):
        t = i / 24
        r = int(gr * t)
        c = mix_color(GLOW_INNER_COLOR, GLOW_OUTER_COLOR, 1.0 - t)
        pygame.draw.circle(glow, (*c, int(28 * t)), (gc, gc), r)
    screen.blit(glow, (cx - gc, cy - gc))

    pr_r = int(ehr * 1.5)
    pr_alpha = int(40 + 15 * math.sin(frame * 0.03))
    ps = pr_r * 2 + 6
    pc = ps // 2
    pr = pygame.Surface((ps, ps), pygame.SRCALPHA)
    pygame.draw.circle(pr, (*PHOTON_RING_COLOR, pr_alpha), (pc, pc), pr_r, 2)
    pygame.draw.circle(pr, (*PHOTON_RING_COLOR, pr_alpha // 2), (pc, pc), pr_r + 2, 1)
    screen.blit(pr, (cx - pc, cy - pc))

    pygame.draw.circle(screen, EVENT_HORIZON_COLOR, (cx, cy), ehr)
    pygame.draw.circle(screen, (2, 2, 4), (cx, cy), max(1, ehr - 4))


def draw_spacetime_rings(screen, bh, ring_count=8):
    """
    Draw concentric spacetime-inspired rings around the black hole.
    """
    cx, cy = int(bh.x), int(bh.y)
    base = bh.accretion_radius + 25
    mr = int(base + ring_count * 30) + 4
    s = mr * 2 + 4
    temp = pygame.Surface((s, s), pygame.SRCALPHA)
    c = s // 2
    for i in range(ring_count):
        r = int(base + i * 30)
        col = (
            (*LENSING_COLOR, max(5, 20 - i * 2))
            if i % 2 == 0
            else (100, 140, 220, max(5, 16 - i * 2))
        )
        pygame.draw.circle(temp, col, (c, c), r, 1)
    screen.blit(temp, (cx - c, cy - c))


# ═══════════════════════════════════════════════════════════
#  PARTICLE RENDERING
# ═══════════════════════════════════════════════════════════

def _pdata(p, bh, ms=14.0):
    """
    Precompute particle rendering data.

    This helper centralizes:
    - distance from center
    - speed
    - region classification
    - speed-based color
    - glow and trail color selection
    - effective visual radius

    Returning a compact dictionary avoids recomputing these values across
    multiple render passes.
    """
    if not p.alive:
        return None

    dx, dy = bh.x - p.x, bh.y - p.y
    dist = math.sqrt(dx * dx + dy * dy)
    spd = math.hypot(p.vx, p.vy)
    region = classify_region_from_distance(dist, bh.event_horizon_radius, bh.accretion_radius)
    sc = speed_to_color(spd, ms)

    ehr, ar = bh.event_horizon_radius, bh.accretion_radius
    t = clamp(1.0 - (dist - ehr) / max(1.0, ar - ehr), 0.0, 1.0) if ar > ehr else 0.0

    if region == REGION_EVENT_HORIZON:
        gc = (255, 60, 30, 70)
        tc = TRAIL_EVENT_COLOR
        bc = PARTICLE_EVENT_COLOR
    elif region == REGION_ACCRETION_ZONE:
        bc = mix_color(sc, PARTICLE_ACCRETION_COLOR, t * 0.5)
        gc = (255, 150, 60, int(25 + 50 * t))
        tc = mix_color(TRAIL_OUTER_COLOR, TRAIL_ACCRETION_COLOR, t)
    else:
        bc = sc
        gc = (sc[0], sc[1], sc[2], 20)
        tc = TRAIL_OUTER_COLOR

    spd_factor = clamp(spd / max(ms, 1), 0, 1)
    vis_r = max(2, p.radius + int(t * 2) + int(spd_factor * 1.5))

    return {
        "px": int(p.x),
        "py": int(p.y),
        "r": vis_r,
        "bc": bc,
        "gc": gc,
        "tc": tc,
        "trail": p.trail,
        "spd": spd,
        "dist": dist,
        "region": region,
        "spd_f": spd_factor,
        "age": getattr(p, "age", 0),
        "peak_speed": getattr(p, "peak_speed", 0),
    }


def draw_particles(screen, particles, bh, show_trails=True, max_speed=14.0, color_mode='speed'):
    """
    Draw all active particles and, optionally, their trails.

    Rendering is performed in multiple passes:
    1. trail pass
    2. outer glow pass
    3. solid particle pass

    This improves readability and gives particles more visual depth.
    """
    w, h = screen.get_size()
    rd = [d for d in (_pdata(p, bh, max_speed) for p in particles) if d]
    if not rd:
        return

    alpha = pygame.Surface((w, h), pygame.SRCALPHA)

    if show_trails:
        for d in rd:
            trail = d["trail"]
            if len(trail) < 2:
                continue
            tc, sc = d["tc"], d["bc"]
            n = len(trail)
            for i in range(1, n):
                prog = i / n
                a = int(255 * prog * 0.38)
                c = mix_color(tc, sc, prog * 0.4)
                lw = max(1, int(1 + d["spd_f"] * 1.5 * prog))
                pygame.draw.line(
                    alpha,
                    (c[0], c[1], c[2], a),
                    (int(trail[i - 1][0]), int(trail[i - 1][1])),
                    (int(trail[i][0]), int(trail[i][1])),
                    lw
                )

    for d in rd:
        pygame.draw.circle(alpha, d["gc"], (d["px"], d["py"]), d["r"] + 4)

    screen.blit(alpha, (0, 0))

    for d in rd:
        final_color = particle_color_by_mode(d, color_mode, max_speed)

        # Slight blend toward accretion color inside the accretion zone.
        if d["region"] == REGION_ACCRETION_ZONE and color_mode != COLOR_REGION:
            final_color = mix_color(final_color, PARTICLE_ACCRETION_COLOR, 0.2)

        pygame.draw.circle(screen, final_color, (d["px"], d["py"]), d["r"])


# ═══════════════════════════════════════════════════════════
#  SECONDARY DETAIL PASSES
# ═══════════════════════════════════════════════════════════

def draw_center_highlight(screen, bh):
    """
    Draw a subtle highlight at the black hole center.
    """
    cx, cy = int(bh.x), int(bh.y)
    r = max(3, int(bh.event_horizon_radius * 0.3))
    s = r * 2 + 6
    c = s // 2
    t = pygame.Surface((s, s), pygame.SRCALPHA)
    pygame.draw.circle(t, (255, 220, 160, 14), (c, c), r)
    screen.blit(t, (cx - c, cy - c))


def draw_debug_guides(screen, bh, enabled=False):
    """
    Draw debug guides such as axes, radii, and reference rings.
    """
    if not enabled:
        return

    w, h = screen.get_size()
    cx, cy = int(bh.x), int(bh.y)
    t = pygame.Surface((w, h), pygame.SRCALPHA)

    pygame.draw.line(t, DEBUG_LINE_COLOR, (0, cy), (w, cy), 1)
    pygame.draw.line(t, DEBUG_LINE_COLOR, (cx, 0), (cx, h), 1)
    pygame.draw.circle(t, (255, 100, 60, 60), (cx, cy), int(bh.event_horizon_radius), 1)
    pygame.draw.circle(t, (255, 180, 80, 40), (cx, cy), int(bh.accretion_radius), 1)

    for d in range(100, max(w, h), 100):
        pygame.draw.circle(t, (50, 60, 90, 18), (cx, cy), d, 1)

    screen.blit(t, (0, 0))


# ═══════════════════════════════════════════════════════════
#  HUD
# ═══════════════════════════════════════════════════════════

def _draw_bar(surf, x, y, w, h, val, mx, col, bg=HUD_BAR_BG):
    """
    Draw a compact horizontal progress bar.
    """
    pygame.draw.rect(surf, bg, (x, y, w, h))
    fw = int(w * clamp(val / max(mx, 1), 0, 1))
    if fw > 0:
        pygame.draw.rect(surf, col, (x, y, fw, h))


def draw_hud(screen, particles, bh, font=None, stats=None, config=None, fps=0, time_scale=1.0):
    """
    Draw the main simulation HUD.

    The HUD includes:
    - frame and time info
    - alive particle counts
    - region occupancy
    - speed bars
    - black hole parameters
    - optional runtime statistics
    - speed histogram
    """
    if font is None:
        font = pygame.font.SysFont("consolas", 13)

    total = len(particles)
    alive = sum(1 for p in particles if p.alive)
    speeds = [math.hypot(p.vx, p.vy) for p in particles if p.alive]
    avg_spd = sum(speeds) / len(speeds) if speeds else 0.0
    max_spd_obs = max(speeds) if speeds else 0.0
    ms = config.get("max_speed", 14.0) if config else 14.0

    rc = {"outer": 0, "accretion": 0, "event": 0}
    for p in particles:
        if not p.alive:
            continue
        d = math.hypot(bh.x - p.x, bh.y - p.y)
        r = classify_region_from_distance(d, bh.event_horizon_radius, bh.accretion_radius)
        if r == REGION_EVENT_HORIZON:
            rc["event"] += 1
        elif r == REGION_ACCRETION_ZONE:
            rc["accretion"] += 1
        else:
            rc["outer"] += 1

    pw, ph = 310, 390
    panel = pygame.Surface((pw, ph), pygame.SRCALPHA)
    panel.fill(HUD_BG_COLOR)
    pygame.draw.rect(panel, HUD_BORDER_COLOR, (0, 0, pw, ph), 1)

    x, y = 12, 8
    lh = 17
    bh_ = 7

    def txt(label, color=TEXT_SOFT_COLOR):
        nonlocal y
        panel.blit(font.render(label, True, color), (x, y))
        y += lh

    panel.blit(font.render("─ SIMULATION HUD ─", True, TEXT_ACCENT_COLOR), (x, y))
    y += lh + 2

    ts_label = f"×{time_scale:.1f}" if time_scale != 1.0 else "×1.0"
    ts_color = (
        TEXT_SUCCESS_COLOR if time_scale == 1.0
        else (255, 200, 80) if time_scale > 1
        else (100, 180, 255)
    )
    txt(f"FPS: {fps:.0f}  Time: {ts_label}", ts_color if fps >= 50 else TEXT_WARNING_COLOR)

    txt(f"Particles: {alive} / {total}")
    bc = HUD_BAR_FILL if alive > total * 0.3 else HUD_BAR_WARN if alive > total * 0.1 else HUD_BAR_CRIT
    _draw_bar(panel, x, y, pw - 24, bh_, alive, max(total, 1), bc)
    y += bh_ + 5

    txt(f"  Outer:     {rc['outer']}", PARTICLE_OUTER_COLOR)
    txt(f"  Accretion: {rc['accretion']}", PARTICLE_ACCRETION_COLOR)
    txt(f"  Event H.:  {rc['event']}", PARTICLE_EVENT_COLOR)
    y += 3

    txt(f"Avg Speed: {avg_spd:.2f}")
    _draw_bar(panel, x, y, pw - 24, bh_, avg_spd, ms, speed_to_color(avg_spd, ms))
    y += bh_ + 4

    txt(f"Max Speed: {max_spd_obs:.2f}")
    _draw_bar(panel, x, y, pw - 24, bh_, max_spd_obs, ms, speed_to_color(max_spd_obs, ms))
    y += bh_ + 4

    txt(f"Mass: {bh.mass:.0f}  G: {config.get('gravity_constant', 0.45):.2f}" if config else f"Mass: {bh.mass:.0f}")
    txt(f"EH: {bh.event_horizon_radius:.0f}  AR: {bh.accretion_radius:.0f}")

    if stats:
        y += 3
        txt(f"Absorbed: {stats.absorbed_total}  Respawned: {stats.respawned_total}")
        txt(f"Time: {stats.sim_time:.1f}s  Frames: {stats.frame_count}")

    y += 6
    panel.blit(font.render("Speed Distribution:", True, TEXT_ACCENT_COLOR), (x, y))
    y += lh

    hist_bins = 12
    hist_h = 35
    hist_w = pw - 24
    bin_w = hist_w // hist_bins
    bins = [0] * hist_bins

    for s in speeds:
        bi = min(int(s / max(ms, 0.01) * hist_bins), hist_bins - 1)
        bins[bi] += 1

    max_bin = max(bins) if bins else 1
    for i in range(hist_bins):
        bh_val = int(hist_h * bins[i] / max(max_bin, 1))
        col = speed_to_color(ms * (i + 0.5) / hist_bins, ms)
        pygame.draw.rect(panel, (*col,), (x + i * bin_w, y + hist_h - bh_val, bin_w - 1, bh_val))
        pygame.draw.rect(panel, (30, 35, 50), (x + i * bin_w, y, bin_w - 1, hist_h - bh_val))

    y += hist_h + 4

    panel.blit(font.render("Slow", True, PARTICLE_SPEED_COLORS[0]), (x, y))
    panel.blit(font.render("Fast", True, PARTICLE_SPEED_COLORS[-1]), (x + pw - 60, y))

    lx = x + 36
    lw = (pw - 24 - 72) // len(PARTICLE_SPEED_COLORS)
    for i, c in enumerate(PARTICLE_SPEED_COLORS):
        pygame.draw.rect(panel, c, (lx + i * lw, y + 2, lw, 10))

    screen.blit(panel, (14, 14))


# ═══════════════════════════════════════════════════════════
#  MINIMAP
# ═══════════════════════════════════════════════════════════

def draw_minimap(screen, particles, bh, w=160, h=100):
    """
    Draw a compact minimap in the lower-right area of the screen.
    """
    sw, sh = screen.get_size()
    mx, my = sw - w - 14, sh - h - 46

    mini = pygame.Surface((w, h), pygame.SRCALPHA)
    mini.fill((6, 8, 16, 180))
    pygame.draw.rect(mini, (40, 50, 80, 100), (0, 0, w, h), 1)

    sx = w / sw
    sy = h / sh
    bcx, bcy = int(bh.x * sx), int(bh.y * sy)

    ar = max(2, int(bh.accretion_radius * sx))
    pygame.draw.circle(mini, (255, 120, 50, 20), (bcx, bcy), ar)

    er = max(1, int(bh.event_horizon_radius * sx))
    pygame.draw.circle(mini, (20, 20, 30), (bcx, bcy), er)

    for p in particles:
        if not p.alive:
            continue
        px, py = int(p.x * sx), int(p.y * sy)
        if 0 <= px < w and 0 <= py < h:
            spd = math.hypot(p.vx, p.vy)
            c = speed_to_color(spd, 14.0)
            mini.set_at((px, py), (*c, 200))

    screen.blit(mini, (mx, my))
    f = pygame.font.SysFont("consolas", 10)
    screen.blit(f.render("MINIMAP", True, (80, 100, 140)), (mx + 4, my + 2))


# ═══════════════════════════════════════════════════════════
#  BOTTOM BAR
# ═══════════════════════════════════════════════════════════

def draw_bottom_bar(screen, font=None, paused=False, time_scale=1.0, show_trails=True):
    """
    Draw the bottom control reference bar.
    """
    if font is None:
        font = pygame.font.SysFont("consolas", 12)

    w, h = screen.get_size()
    bar_h = 32
    bar = pygame.Surface((w, bar_h), pygame.SRCALPHA)
    bar.fill((6, 8, 16, 200))
    pygame.draw.line(bar, (40, 50, 80, 100), (0, 0), (w, 0), 1)

    controls = [
        ("SPACE", "Pause" if not paused else "Play", TEXT_ACCENT_COLOR if paused else TEXT_SOFT_COLOR),
        ("R", "Reset", TEXT_SOFT_COLOR),
        ("T", f"Trails {'ON' if show_trails else 'OFF'}", TEXT_SUCCESS_COLOR if show_trails else TEXT_ERROR_COLOR),
        ("D", "Debug", TEXT_SOFT_COLOR),
        ("H", "HUD", TEXT_SOFT_COLOR),
        ("↑↓", f"Speed {time_scale:.1f}x", (255, 200, 80) if time_scale != 1.0 else TEXT_SOFT_COLOR),
        ("+/-", "Particles", TEXT_SOFT_COLOR),
        ("Scroll", "Mass", TEXT_SOFT_COLOR),
        ("LMB", "Attract", (100, 200, 255)),
        ("RMB", "Repel", (255, 100, 100)),
    ]

    x = 16
    y = 8
    for key, label, color in controls:
        key_surf = font.render(f"[{key}]", True, (180, 190, 220))
        bar.blit(key_surf, (x, y))
        x += key_surf.get_width() + 4

        lbl_surf = font.render(label, True, color)
        bar.blit(lbl_surf, (x, y))
        x += lbl_surf.get_width() + 16

    screen.blit(bar, (0, h - bar_h))


# ═══════════════════════════════════════════════════════════
#  MOUSE / WARNING OVERLAYS
# ═══════════════════════════════════════════════════════════

def draw_mouse_indicator(screen, mx, my, mode="attract", font=None):
    """
    Draw a visual indicator showing the active mouse interaction region.
    """
    if font is None:
        font = pygame.font.SysFont("consolas", 11)

    color = (100, 200, 255, 80) if mode == "attract" else (255, 100, 100, 80)
    label = "ATTRACT" if mode == "attract" else "REPEL"

    t = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pygame.draw.circle(t, color, (mx, my), 30, 2)
    pygame.draw.circle(t, (*color[:3], 15), (mx, my), 55, 1)
    screen.blit(t, (0, 0))

    txt = font.render(label, True, color[:3])
    screen.blit(txt, (mx - txt.get_width() // 2, my - 46))


def draw_warning_overlay(screen, text, font=None):
    """
    Draw a compact warning message near the bottom of the screen.
    """
    if font is None:
        font = pygame.font.SysFont("consolas", 18, bold=True)
    screen.blit(font.render(text, True, TEXT_WARNING_COLOR), (20, screen.get_height() - 70))


# ═══════════════════════════════════════════════════════════
#  COMPOSITE SCENE
# ═══════════════════════════════════════════════════════════

def draw_scene(
    screen,
    black_hole,
    particles,
    debug=False,
    show_hud=True,
    show_starfield=True,
    show_trails=True,
    stars=None,
    ring_count=8,
    max_speed=14.0,
    frame=0,
    stats=None,
    config=None,
    fps=0,
    mouse_active=False,
    mouse_pos=None,
    mouse_mode="attract",
    paused=False,
    time_scale=1.0,
    color_mode='speed'
):
    """
    Draw the complete simulation frame.

    This function is the top-level visual compositor of the Python simulation.
    It assembles the full frame in layered order:

    1. background
    2. starfield
    3. spacetime rings
    4. accretion disk
    5. black hole core
    6. particles
    7. center highlight
    8. debug guides
    9. mouse indicator
    10. HUD
    11. minimap
    12. bottom bar
    13. warnings
    """
    draw_background(screen)

    if show_starfield:
        draw_starfield(screen, stars=stars)

    draw_spacetime_rings(screen, black_hole, ring_count=ring_count)
    draw_accretion_disk(screen, black_hole, frame=frame)
    draw_black_hole_core(screen, black_hole, frame=frame)
    draw_particles(screen, particles, black_hole, show_trails=show_trails, max_speed=max_speed, color_mode=color_mode)
    draw_center_highlight(screen, black_hole)
    draw_debug_guides(screen, black_hole, enabled=debug)

    if mouse_active and mouse_pos:
        draw_mouse_indicator(screen, mouse_pos[0], mouse_pos[1], mode=mouse_mode)

    if show_hud:
        draw_hud(screen, particles, black_hole, stats=stats, config=config, fps=fps, time_scale=time_scale)

    draw_minimap(screen, particles, black_hole)
    draw_bottom_bar(screen, paused=paused, time_scale=time_scale, show_trails=show_trails)

    alive = sum(1 for p in particles if p.alive)
    if alive < max(1, len(particles) // 8):
        draw_warning_overlay(screen, "LOW PARTICLE COUNT")
