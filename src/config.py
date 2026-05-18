from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
RAW_DATA_DIR = DATA_DIR / "raw"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"
REPORT_DIR = PROJECT_ROOT / "reports"
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
DOCS_DIR = PROJECT_ROOT / "docs"

DEMO_YEARS = [2023, 2024, 2025]
SELECTED_COUNTIES = [
    "Shawnee",
    "Geary",
    "Dickinson",
    "Clay",
    "Riley",
    "Jefferson",
    "Osage",
    "Wabaunsee",
]

CAMPUSES = {
    "Topeka": {"lon": -95.69, "lat": 39.05},
    "Junction City": {"lon": -96.83, "lat": 39.03},
}


def ensure_project_dirs() -> None:
    """Create the public-facing directories used by the demo pipeline."""
    for path in [SAMPLE_DATA_DIR, FIGURE_DIR, TABLE_DIR, REPORT_DIR, DOCS_DIR, NOTEBOOK_DIR]:
        path.mkdir(parents=True, exist_ok=True)
