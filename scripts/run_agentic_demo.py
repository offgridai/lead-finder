from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.activity_agent import analyze_activity
from agents.income_agent import estimate_cashflow
from agents.report_agent import build_narrative, lead_to_csv_row
from agents.transition_agent import estimate_transition_likelihood
from connectors.demo_sources import DemoSourceConnector
from models.business import LeadRecord
from parsers.demo_business_parser import parse_demo_business_page
from storage.sqlite_store import LeadFinderStore


def run_demo(project_root: Path, output_dir: Path) -> dict[str, int | str]:
    fixture_dir = project_root / "evals" / "fixtures" / "demo_web_pages"
    output_dir.mkdir(parents=True, exist_ok=True)

    store = LeadFinderStore(output_dir / "lead_finder_demo.sqlite")

    # Step 1A: retrieve raw source documents.
    connector = DemoSourceConnector(fixture_dir)
    raw_docs = connector.retrieve(
        county="Hocking County",
        state="Ohio",
        business_types=["campground", "rv_park", "cabin_resort"],
    )
    store.save_raw_documents(raw_docs)

    # Step 1B: parse raw documents into normalized business candidates.
    candidates = [parse_demo_business_page(doc) for doc in raw_docs]
    store.save_candidates(candidates)

    # Steps 2-4: run separate analysis agents over normalized candidates.
    leads: list[LeadRecord] = []
    for candidate in candidates:
        lead = LeadRecord(
            business=candidate,
            activity=analyze_activity(candidate),
            cashflow=estimate_cashflow(candidate),
            transition=estimate_transition_likelihood(candidate),
            acquisition_narrative="",
            notes="Demo evidence only. Replace demo connector with live source connectors before using commercially.",
        )
        lead.acquisition_narrative = build_narrative(lead)
        leads.append(lead)

    leads.sort(
        key=lambda lead: (
            lead.cashflow.estimated_cashflow_high or 0,
            lead.transition.transition_score,
            lead.activity.activity_score,
        ),
        reverse=True,
    )
    store.save_leads(leads)

    # Step 5: produce a sortable CSV table.
    csv_path = output_dir / "hocking_county_agentic_demo.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(lead_to_csv_row(leads[0]).keys()))
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead_to_csv_row(lead))

    counts = store.counts()
    return {
        "raw_documents": counts["raw_documents"],
        "candidates": counts["candidates"],
        "leads": counts["leads"],
        "csv_path": str(csv_path),
        "sqlite_path": str(output_dir / "lead_finder_demo.sqlite"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the visible agentic demo pipeline.")
    parser.add_argument("--output-dir", default="outputs/demo", help="Where CSV + SQLite artifacts are written")
    args = parser.parse_args()

    result = run_demo(PROJECT_ROOT, PROJECT_ROOT / args.output_dir)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
