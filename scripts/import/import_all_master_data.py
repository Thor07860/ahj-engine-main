#!/usr/bin/env python
"""
Master Data Import Runner

Runs full database schema + master-data import in order:
1) Alembic migrations to head
2) Regulatory data import (countries, states, AHJs, utilities)
3) Codes import
4) Equipment/categories import
5) Labels import

Usage:
    python scripts/import/import_all_master_data.py
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_step(name: str, command: list[str]) -> bool:
    print("\n" + "=" * 70)
    print(f"{name}")
    print("=" * 70)
    print("Running:", " ".join(command))

    result = subprocess.run(command, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        print(f"\nFAILED: {name} (exit code {result.returncode})")
        return False

    print(f"\nSUCCESS: {name}")
    return True


def main() -> int:
    python_exe = sys.executable

    steps = [
        ("Apply Alembic Migrations", [python_exe, "-m", "alembic", "upgrade", "head"]),
        (
            "Import Regulatory Data",
            [python_exe, "scripts/import/import_regulatory_data.py"],
        ),
        (
            "Import Codes",
            [python_exe, "scripts/import/import_codes.py"],
        ),
        (
            "Import Equipment & Categories",
            [python_exe, "scripts/import/import_equipment_categories.py"],
        ),
        (
            "Import Labels",
            [python_exe, "scripts/import/import_labels_new.py"],
        ),
    ]

    print("\n" + "=" * 70)
    print("MASTER DATA IMPORT STARTED")
    print(f"Project Root: {PROJECT_ROOT}")
    print("=" * 70)

    for step_name, command in steps:
        if not run_step(step_name, command):
            print("\nMaster import stopped due to failure.")
            return 1

    print("\n" + "=" * 70)
    print("MASTER DATA IMPORT COMPLETED")
    print("All schema updates and imports finished successfully.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
