from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.generate_figures import generate_figures
from scripts.generate_synthetic_data import main as generate_synthetic_data
from scripts.run_processing import run_processing


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the public DataFest demo pipeline.")
    parser.add_argument(
        "--with-maps",
        action="store_true",
        help="Also generate optional choropleth figures if geospatial dependencies are installed.",
    )
    args = parser.parse_args()

    print("1/3 Generating synthetic public demo data...")
    generate_synthetic_data()

    print("2/3 Running county-panel and scoring pipeline...")
    run_processing()

    print("3/3 Generating public-facing figures and demo PDF...")
    generate_figures()

    if args.with_maps:
        from scripts.generate_choropleths import generate_choropleths

        print("4/4 Generating optional choropleth maps...")
        generate_choropleths()
    else:
        print("Optional choropleths are available via: python scripts/generate_choropleths.py")

    print("Demo pipeline complete.")


if __name__ == "__main__":
    main()
