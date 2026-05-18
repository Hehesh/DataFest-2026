from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.generate_figures import generate_figures
from scripts.generate_synthetic_data import main as generate_synthetic_data
from scripts.run_processing import run_processing


def main() -> None:
    print("1/3 Generating synthetic public demo data...")
    generate_synthetic_data()

    print("2/3 Running county-panel and scoring pipeline...")
    run_processing()

    print("3/3 Generating public-facing figures and demo PDF...")
    generate_figures()

    print("Demo pipeline complete.")


if __name__ == "__main__":
    main()
