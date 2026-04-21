"""
BlackHole Simulation System - Unified Launcher
----------------------------------------------

This module acts as the main launcher of the repository.

Its purpose is to provide a single entry point for the most important actions
available in the project, without requiring the user to manually navigate the
full directory structure.

The launcher is intentionally positioned at repository root because it is meant
to coordinate the different layers of the system from one place.

Typical responsibilities include:
- starting the main Python simulation
- opening the web demonstration layer
- triggering C module build scripts
- generating project reports
- providing a compact control surface for the repository

This file should be understood as the operational entrypoint of the project,
not as part of the low-level simulation engine itself.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# PATH RESOLUTION
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
PYTHON_MAIN = ROOT_DIR / "src" / "python" / "simulations" / "main_simulation.py"
WEB_INDEX = ROOT_DIR / "web" / "index.html"
BUILD_SCRIPT = ROOT_DIR / "scripts" / "build_c.sh"
REPORT_SCRIPT = ROOT_DIR / "src" / "python" / "tools" / "generate_report.py"


# ---------------------------------------------------------------------------
# LOW-LEVEL HELPERS
# ---------------------------------------------------------------------------

def run_command(command: list[str], description: str) -> None:
    """
    Execute a subprocess command and report its intent.

    Parameters
    ----------
    command :
        Command and arguments to execute.
    description :
        Human-readable description printed before execution.

    Notes
    -----
    This helper keeps process execution consistent across all launcher actions.
    The subprocess is executed without forcing strict termination of the whole
    launcher in case of failure, because the launcher is intended as a user-
    facing utility rather than a hard pipeline.
    """
    print("=" * 72)
    print(description)
    print("=" * 72)
    subprocess.run(command, check=False)
    print()


def open_file_in_system(path: Path, description: str) -> None:
    """
    Open a file using the default system handler.

    Parameters
    ----------
    path :
        File to open.
    description :
        Human-readable action description.

    Notes
    -----
    This function keeps platform-specific open behavior isolated.
    """
    print("=" * 72)
    print(description)
    print("=" * 72)

    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    elif os.name == "nt":
        os.startfile(path)  # type: ignore[attr-defined]
    else:
        subprocess.run(["xdg-open", str(path)], check=False)

    print()


def path_exists_or_warn(path: Path, label: str) -> bool:
    """
    Check whether a required project path exists before attempting to use it.

    Parameters
    ----------
    path :
        Path to validate.
    label :
        Human-readable label used in warning output.

    Returns
    -------
    bool
        True if the path exists, False otherwise.
    """
    if path.exists():
        return True

    print("=" * 72)
    print(f"Missing resource: {label}")
    print("=" * 72)
    print(path)
    print()
    return False


# ---------------------------------------------------------------------------
# LAUNCH ACTIONS
# ---------------------------------------------------------------------------

def run_python_simulation() -> None:
    """
    Launch the main Python simulation entrypoint.

    This is the primary runtime path for the project.
    """
    if not path_exists_or_warn(PYTHON_MAIN, "Python simulation entrypoint"):
        return

    run_command(
        [sys.executable, str(PYTHON_MAIN)],
        "Running Python simulation",
    )


def open_web_demo() -> None:
    """
    Open the browser-based demonstration layer.

    This does not replace the Python simulation. It is intended as a visual
    and explanatory companion layer of the project.
    """
    if not path_exists_or_warn(WEB_INDEX, "Web interface"):
        return

    open_file_in_system(WEB_INDEX, "Opening web demo")


def build_c_modules() -> None:
    """
    Launch the helper script used to build the C layer.
    """
    if not path_exists_or_warn(BUILD_SCRIPT, "C build script"):
        return

    run_command(
        ["bash", str(BUILD_SCRIPT)],
        "Building C modules",
    )


def generate_report() -> None:
    """
    Generate a project report through the report utility.

    The generated report is written into the repository output directory.
    """
    if not path_exists_or_warn(REPORT_SCRIPT, "Report generator"):
        return

    run_command(
        [sys.executable, str(REPORT_SCRIPT)],
        "Generating project report",
    )


# ---------------------------------------------------------------------------
# MENU
# ---------------------------------------------------------------------------

def show_menu() -> None:
    """
    Print the main launcher menu.
    """
    print("=" * 72)
    print("                    BLACKHOLE SIMULATION SYSTEM                    ")
    print("=" * 72)
    print("1) Run Python simulation")
    print("2) Open web demo")
    print("3) Build C modules")
    print("4) Generate report")
    print("0) Exit")
    print()


def main() -> None:
    """
    Main launcher loop.

    The launcher is intentionally simple:
    - print menu
    - read user input
    - dispatch action
    - continue until explicit exit
    """
    while True:
        show_menu()
        choice = input("Select an option > ").strip()

        if choice == "1":
            run_python_simulation()

        elif choice == "2":
            open_web_demo()

        elif choice == "3":
            build_c_modules()

        elif choice == "4":
            generate_report()

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid option.")
            print()


if __name__ == "__main__":
    main()
