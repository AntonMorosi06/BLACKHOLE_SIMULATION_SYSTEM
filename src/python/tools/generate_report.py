"""
Generate Report
---------------

This module generates a structured textual report describing the current state
of the BlackHole Simulation System.

The report is intended as an internal diagnostic and documentation support tool.
It does not analyze runtime particle trajectories directly. Instead, it builds
a synthetic project report by combining:

- project metadata
- active JSON configuration
- derived metrics
- qualitative parameter interpretation
- structural project inventory
- runtime feature summary
- current development status
- architectural notes
- future work directions

The generated output is saved inside the project's data/output directory in
multiple formats.

This tool is especially useful for:
- repository inspection
- project snapshots
- documentation support
- configuration sanity review
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

from src.python.core.config_loader import load_config
from src.python.core.constants import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_AUTHOR,
)


LINE_WIDTH = 88


# ═══════════════════════════════════════════════════════════
#  BASIC HELPERS
# ═══════════════════════════════════════════════════════════

def hr(char: str = "=") -> str:
    """
    Return a horizontal separator line.

    Parameters
    ----------
    char :
        Character used to build the separator.

    Returns
    -------
    str
        Repeated separator string.
    """
    return char * LINE_WIDTH


def get_project_root() -> Path:
    """
    Return the root directory of the project.

    The path is resolved starting from this file:
    src/python/tools/generate_report.py
    """
    return Path(__file__).resolve().parents[3]


def get_output_dir() -> Path:
    """
    Return the report output directory.

    The directory is created automatically if it does not exist.
    """
    output_dir = get_project_root() / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_src_root() -> Path:
    """
    Return the root directory of the Python source layer.
    """
    return get_project_root() / "src" / "python"


def safe_get(config: dict, key: str, default=None):
    """
    Safely read a key from the configuration dictionary.

    This helper keeps the rest of the report code compact and avoids repeated
    config.get(...) calls with fallback values.
    """
    return config.get(key, default)


def format_kv(key: str, value) -> str:
    """
    Return a consistently aligned 'key : value' string.
    """
    return f"{key:<32}: {value}"


def bool_to_label(value: bool) -> str:
    """
    Convert a boolean flag into a human-readable label.
    """
    return "enabled" if value else "disabled"


# ═══════════════════════════════════════════════════════════
#  HEADER AND GENERAL SUMMARY
# ═══════════════════════════════════════════════════════════

def build_header() -> str:
    """
    Build the report header.

    Includes:
    - project name
    - version
    - author
    - generation timestamp
    - project root path
    """
    now = datetime.now()

    lines = [
        hr("="),
        f"{PROJECT_NAME}",
        f"Version: {PROJECT_VERSION}",
        f"Author: {PROJECT_AUTHOR}",
        f"Generated at: {now.isoformat()}",
        f"Project root: {get_project_root()}",
        hr("="),
        ""
    ]
    return "\n".join(lines)


def build_project_summary() -> str:
    """
    Build the high-level descriptive summary of the project.

    This section is intentionally narrative: it gives a compact conceptual
    description of the repository and its purpose.
    """
    lines = [
        "PROJECT SUMMARY",
        hr("-"),
        "BLACKHOLE SIMULATION SYSTEM è un ambiente modulare dedicato alla",
        "simulazione di un buco nero in forma semplificata, con particolare",
        "attenzione alla separazione tra motore fisico, rendering grafico,",
        "configurazione parametrica, moduli numerici in C e interfaccia futura.",
        "",
        "Il sistema è pensato come base estendibile per lo studio del moto di",
        "particelle soggette a un attrattore centrale, dell'assorbimento entro",
        "l'orizzonte degli eventi, della zona di accrescimento e di possibili",
        "evoluzioni verso modelli più sofisticati sia sul piano fisico sia",
        "sul piano della rappresentazione visiva.",
        "",
        "L'architettura privilegia modularità, leggibilità, configurabilità e",
        "possibilità di integrazione tra componenti Python, moduli C e layer",
        "grafici o dashboard esterne.",
        ""
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
#  CONFIGURATION SECTIONS
# ═══════════════════════════════════════════════════════════

def build_config_section(config: dict) -> str:
    """
    Build the section listing the currently active configuration values.

    All configuration keys are sorted alphabetically for readability.
    """
    lines = [
        "ACTIVE CONFIGURATION",
        hr("-")
    ]

    for key in sorted(config.keys()):
        lines.append(format_kv(key, config[key]))

    lines.append("")
    return "\n".join(lines)


def derive_config_metrics(config: dict) -> Dict[str, float]:
    """
    Derive synthetic metrics from the active configuration.

    These values do not represent measured runtime data. They are
    configuration-derived indicators useful for quick qualitative inspection.
    """
    width = safe_get(config, "window_width", 0)
    height = safe_get(config, "window_height", 0)
    particle_count = safe_get(config, "particle_count", 0)
    event_horizon = safe_get(config, "event_horizon_radius", 0.0)
    accretion = safe_get(config, "accretion_radius", 0.0)
    gravity = safe_get(config, "gravity_constant", 0.0)
    mass = safe_get(config, "black_hole_mass", 0.0)
    damping = safe_get(config, "damping", 0.999)
    max_speed = safe_get(config, "max_speed", 0.0)
    dt = safe_get(config, "dt", 1.0)

    world_area = width * height
    density = (particle_count / world_area) if world_area > 0 else 0.0
    accretion_to_horizon_ratio = (accretion / event_horizon) if event_horizon > 0 else 0.0
    attraction_index = gravity * mass
    kinematic_index = max_speed * dt
    damping_loss = 1.0 - damping

    return {
        "world_area": world_area,
        "particle_density": density,
        "accretion_to_horizon_ratio": accretion_to_horizon_ratio,
        "attraction_index": attraction_index,
        "kinematic_index": kinematic_index,
        "damping_loss_per_step": damping_loss,
    }


def build_derived_metrics_section(config: dict) -> str:
    """
    Build the section containing derived configuration metrics.
    """
    metrics = derive_config_metrics(config)

    lines = [
        "DERIVED METRICS",
        hr("-"),
        format_kv("world_area", metrics["world_area"]),
        format_kv("particle_density", f"{metrics['particle_density']:.8f}"),
        format_kv("accretion_to_horizon_ratio", f"{metrics['accretion_to_horizon_ratio']:.4f}"),
        format_kv("attraction_index (G*M)", f"{metrics['attraction_index']:.6f}"),
        format_kv("kinematic_index (max_speed*dt)", f"{metrics['kinematic_index']:.6f}"),
        format_kv("damping_loss_per_step", f"{metrics['damping_loss_per_step']:.8f}"),
        ""
    ]
    return "\n".join(lines)


def build_interpretation_section(config: dict) -> str:
    """
    Build a qualitative interpretation of the current configuration.

    This section translates raw parameter values into readable project-level
    observations.
    """
    particle_count = config.get("particle_count", 0)
    mass = config.get("black_hole_mass", 0.0)
    gravity = config.get("gravity_constant", 0.0)
    event_horizon = config.get("event_horizon_radius", 0.0)
    accretion = config.get("accretion_radius", 0.0)
    damping = config.get("damping", 0.999)
    max_speed = config.get("max_speed", 12.0)
    dt = config.get("dt", 1.0)

    lines = [
        "PARAMETER INTERPRETATION",
        hr("-"),
        f"- Il sistema genera inizialmente {particle_count} particelle.",
        f"- La massa simbolica del buco nero è impostata a {mass}.",
        f"- La costante gravitazionale di simulazione è {gravity}.",
        f"- Il raggio dell'orizzonte degli eventi è {event_horizon}.",
        f"- Il raggio della zona di accrescimento è {accretion}.",
        f"- Il damping cinematico è {damping}.",
        f"- La velocità massima ammessa è {max_speed}.",
        f"- Il passo temporale nominale della simulazione è {dt}.",
        "",
        "Interpretazione generale:",
        "Un aumento della massa o della costante gravitazionale rende",
        "l'attrazione centrale più intensa. Un aumento del raggio",
        "dell'orizzonte degli eventi amplia la regione di assorbimento.",
        "Un aumento del raggio di accrescimento rende la struttura visiva",
        "del sistema più estesa e percepibile anche nelle regioni esterne.",
        "",
        "Un damping molto vicino a 1 conserva maggiormente il moto, mentre",
        "valori più bassi dissipano energia più rapidamente. Un max_speed",
        "più alto consente traiettorie più aggressive ma può aumentare il",
        "rischio di instabilità numerica se non bilanciato con dt e softening.",
        ""
    ]
    return "\n".join(lines)


def evaluate_config_health(config: dict) -> List[str]:
    """
    Produce qualitative health notes for the active configuration.

    The output is intentionally heuristic. It does not claim formal numerical
    validation, but helps highlight potentially problematic parameter ranges.
    """
    notes = []

    width = safe_get(config, "window_width", 0)
    height = safe_get(config, "window_height", 0)
    particle_count = safe_get(config, "particle_count", 0)
    event_horizon = safe_get(config, "event_horizon_radius", 0.0)
    accretion = safe_get(config, "accretion_radius", 0.0)
    softening = safe_get(config, "softening", 0.0)
    damping = safe_get(config, "damping", 0.999)
    max_speed = safe_get(config, "max_speed", 12.0)
    dt = safe_get(config, "dt", 1.0)

    if width < 640 or height < 480:
        notes.append("La finestra di simulazione è relativamente piccola e può ridurre la leggibilità visiva.")
    if particle_count < 50:
        notes.append("Il numero di particelle è basso: la scena potrebbe apparire troppo vuota.")
    if particle_count > 5000:
        notes.append("Il numero di particelle è molto alto: possibile impatto rilevante sulle performance.")
    if event_horizon == 0:
        notes.append("Il raggio dell'orizzonte è nullo: l'assorbimento potrebbe non essere visivamente evidente.")
    if accretion <= event_horizon:
        notes.append("La zona di accrescimento è troppo vicina o uguale all'orizzonte: contrasto visivo ridotto.")
    if softening < 1e-6:
        notes.append("Il softening è molto basso: rischio di accelerazioni eccessive vicino al centro.")
    if damping < 0.95:
        notes.append("Il damping è piuttosto aggressivo: il moto potrebbe apparire troppo dissipativo.")
    if max_speed > 50:
        notes.append("Il max_speed è elevato: possono emergere comportamenti numerici difficili da controllare.")
    if dt > 2.0:
        notes.append("Il passo temporale è alto: attenzione a possibili errori di integrazione visibili.")

    if not notes:
        notes.append("La configurazione attiva appare internamente coerente per una simulazione semplificata.")

    return notes


def build_config_health_section(config: dict) -> str:
    """
    Build the qualitative configuration health section.
    """
    notes = evaluate_config_health(config)

    lines = [
        "CONFIG HEALTH CHECK",
        hr("-")
    ]

    for note in notes:
        lines.append(f"- {note}")

    lines.append("")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
#  PROJECT STRUCTURE AND INVENTORY
# ═══════════════════════════════════════════════════════════

def scan_project_tree() -> List[Tuple[str, bool]]:
    """
    Collect a small inventory of important project paths and their existence.

    This is not intended to be a full recursive project scan. It is a focused
    structural sanity check over the key directories expected by the system.
    """
    root = get_project_root()

    important_paths = [
        root / "src",
        root / "src" / "python",
        root / "src" / "python" / "core",
        root / "src" / "python" / "engine",
        root / "src" / "python" / "models",
        root / "src" / "python" / "render",
        root / "src" / "python" / "simulations",
        root / "src" / "python" / "tools",
        root / "data",
        root / "data" / "config",
        root / "data" / "output",
    ]

    return [(str(path.relative_to(root)), path.exists()) for path in important_paths]


def build_project_structure_section() -> str:
    """
    Build the project structure overview section.
    """
    scanned = scan_project_tree()

    lines = [
        "PROJECT STRUCTURE OVERVIEW",
        hr("-")
    ]

    for rel_path, exists in scanned:
        status = "[x]" if exists else "[ ]"
        lines.append(f"{status} {rel_path}")

    lines.append("")
    return "\n".join(lines)


def count_python_files() -> int:
    """
    Count Python source files inside src/python.
    """
    src_root = get_src_root()
    if not src_root.exists():
        return 0
    return len(list(src_root.rglob("*.py")))


def count_c_files() -> int:
    """
    Count C source files inside the project root.
    """
    root = get_project_root()
    return len(list(root.rglob("*.c")))


def build_code_inventory_section() -> str:
    """
    Build the code inventory section.
    """
    py_count = count_python_files()
    c_count = count_c_files()

    lines = [
        "CODE INVENTORY",
        hr("-"),
        format_kv("python_files", py_count),
        format_kv("c_files", c_count),
        ""
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
#  RUNTIME FEATURES AND STATUS
# ═══════════════════════════════════════════════════════════

def build_runtime_features_section(config: dict) -> str:
    """
    Build the runtime feature summary section.

    These values are read from configuration and describe optional or
    tunable simulation features.
    """
    lines = [
        "RUNTIME FEATURES",
        hr("-"),
        format_kv("show_debug_overlay", bool_to_label(safe_get(config, "show_debug_overlay", False))),
        format_kv("show_trails", bool_to_label(safe_get(config, "show_trails", True))),
        format_kv("show_starfield", bool_to_label(safe_get(config, "show_starfield", True))),
        format_kv("trail_length", safe_get(config, "trail_length", 30)),
        format_kv("starfield_count", safe_get(config, "starfield_count", 180)),
        format_kv("ring_count", safe_get(config, "ring_count", 6)),
        format_kv("respawn_threshold", safe_get(config, "respawn_threshold", 25)),
        format_kv("respawn_batch_size", safe_get(config, "respawn_batch_size", 80)),
        ""
    ]
    return "\n".join(lines)


def build_status_section() -> str:
    """
    Build the current development status section.

    This section acts as a compact human-readable project checklist.
    """
    lines = [
        "CURRENT DEVELOPMENT STATUS",
        hr("-"),
        "[x] Struttura base del progetto definita",
        "[x] Moduli Python principali impostati",
        "[x] Motore gravitazionale semplificato definito",
        "[x] Entità Particle e BlackHole implementate",
        "[x] Rendering 2D della scena disponibile",
        "[x] Configurazione JSON centralizzata",
        "[x] Launcher o entrypoint principale disponibile",
        "[x] Strumenti di report automatico introdotti",
        "[x] Moduli C introduttivi predisposti",
        "[ ] Esportazione dati di simulazione avanzata",
        "[ ] Analisi temporale dettagliata delle particelle",
        "[ ] Dashboard web sincronizzata con output Python",
        "[ ] Simulazione 3D o pseudo-3D avanzata",
        "[ ] Modellazione più avanzata del disco di accrescimento",
        "[ ] Supporto a benchmark e profiling automatico",
        ""
    ]
    return "\n".join(lines)


def build_design_notes_section() -> str:
    """
    Build the architectural notes section.

    This section summarizes the separation of responsibilities across the
    Python project layout.
    """
    lines = [
        "ARCHITECTURAL NOTES",
        hr("-"),
        "Il progetto adotta una separazione tra:",
        "- core: costanti, configurazione, fondamenta condivise",
        "- models: entità dati del dominio (Particle, BlackHole, ecc.)",
        "- engine: logica fisica, aggiornamento dello stato, simulazione",
        "- render: visualizzazione 2D, overlay e resa della scena",
        "- simulations: scenari eseguibili e entrypoint applicativi",
        "- tools: strumenti ausiliari per analisi, report e supporto",
        "",
        "Questa separazione facilita manutenzione, testing, estensione",
        "futura e integrazione con moduli a maggiore intensità numerica.",
        ""
    ]
    return "\n".join(lines)


def build_future_work_section() -> str:
    """
    Build the future work section.

    The items included here are intentionally broad and strategic rather than
    tied to one single file or subsystem.
    """
    lines = [
        "FUTURE WORK",
        hr("-"),
        "1. Introduzione di velocità tangenziali più controllate per simulare",
        "   orbite pseudo-stabili e configurazioni iniziali più fisicamente",
        "   interpretabili.",
        "2. Salvataggio delle traiettorie delle particelle in file CSV o JSON",
        "   per analisi offline e visualizzazione esterna.",
        "3. Integrazione tra modulo Python e modulo C per accelerare i calcoli",
        "   e testare versioni numericamente più spinte.",
        "4. Costruzione di una dashboard web con statistiche in tempo reale e",
        "   controlli parametrici dinamici.",
        "5. Studio di effetti visuali ispirati alla lente gravitazionale e",
        "   alla distorsione dello spazio-tempo.",
        "6. Possibile estensione verso rappresentazioni tridimensionali o",
        "   pseudo-tridimensionali con camera orbitale.",
        "7. Introduzione di benchmark, profiling automatico e confronto tra",
        "   configurazioni diverse.",
        "8. Arricchimento della componente teorica per collegare il progetto",
        "   a sezioni documentali più scientifiche o divulgative.",
        ""
    ]
    return "\n".join(lines)


def build_footer() -> str:
    """
    Build the closing section of the report.
    """
    lines = [
        hr("="),
        "End of report",
        hr("="),
        ""
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
#  REPORT ASSEMBLY
# ═══════════════════════════════════════════════════════════

def generate_report_text() -> str:
    """
    Generate the full report text by assembling all sections in order.
    """
    config = load_config()

    sections = [
        build_header(),
        build_project_summary(),
        build_project_structure_section(),
        build_code_inventory_section(),
        build_config_section(config),
        build_derived_metrics_section(config),
        build_runtime_features_section(config),
        build_interpretation_section(config),
        build_config_health_section(config),
        build_status_section(),
        build_design_notes_section(),
        build_future_work_section(),
        build_footer()
    ]

    return "\n".join(sections)


# ═══════════════════════════════════════════════════════════
#  FILE OUTPUT
# ═══════════════════════════════════════════════════════════

def save_latest_report(report_text: str) -> Path:
    """
    Save the report under a fixed latest_report.txt filename.
    """
    output_path = get_output_dir() / "latest_report.txt"
    output_path.write_text(report_text, encoding="utf-8")
    return output_path


def save_timestamped_report(report_text: str) -> Path:
    """
    Save the report with a timestamped TXT filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = get_output_dir() / f"report_{timestamp}.txt"
    output_path.write_text(report_text, encoding="utf-8")
    return output_path


def save_markdown_report(report_text: str) -> Path:
    """
    Save a timestamped Markdown copy of the report.

    The content remains plain text oriented, but the .md extension allows
    easier inspection in repository tooling and editors.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = get_output_dir() / f"report_{timestamp}.md"
    output_path.write_text(report_text, encoding="utf-8")
    return output_path


# ═══════════════════════════════════════════════════════════
#  ENTRYPOINT
# ═══════════════════════════════════════════════════════════

def generate():
    """
    Generate and save the report in all supported output formats.

    Output files currently include:
    - latest_report.txt
    - timestamped .txt report
    - timestamped .md report
    """
    report_text = generate_report_text()

    latest_path = save_latest_report(report_text)
    timestamped_path = save_timestamped_report(report_text)
    markdown_path = save_markdown_report(report_text)

    print(hr("="))
    print("REPORT GENERATO CON SUCCESSO")
    print(hr("="))
    print(f"Latest report     : {latest_path}")
    print(f"Timestamped report: {timestamped_path}")
    print(f"Markdown report   : {markdown_path}")
    print(hr("="))


if __name__ == "__main__":
    generate()
