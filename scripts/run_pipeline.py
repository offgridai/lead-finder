from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.report_agent import write_csv
from pipelines.hocking_county_campgrounds import run_from_fixture


def main() -> None:
    parser = argparse.ArgumentParser(description="Run lead-finder pipeline from fixture data.")
    parser.add_argument("--fixture", required=True, help="Path to fixture JSON file.")
    parser.add_argument("--output", required=True, help="Output CSV path.")
    args = parser.parse_args()

    fixture_path = Path(args.fixture)
    records = json.loads(fixture_path.read_text(encoding="utf-8"))
    leads = run_from_fixture(records)
    write_csv(leads, args.output)
    print(f"Wrote {len(leads)} leads to {args.output}")


if __name__ == "__main__":
    main()
