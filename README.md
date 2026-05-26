# lead-finder

AI-assisted acquisition lead sourcing for local cash-flowing businesses.

Initial target scenario:

> Search Hocking County, Ohio. Find campground, RV park, and cabin resort businesses. Estimate how active each business is. Estimate current annual cashflow. Estimate how willing the owners are to sell. Return findings as a CSV table.

This repo is intentionally built as a deterministic data pipeline first, with LLM/agent behavior layered on top of structured evidence.

## Principles

- Every score must be evidence-backed.
- Outputs are estimates, not facts.
- Use ranges for revenue and cashflow.
- Prefer small, testable pipeline stages over one large autonomous agent.
- Store raw evidence and timestamps wherever possible.
- Avoid invasive personal profiling or unsupported claims about individuals.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_pipeline.py --fixture evals/fixtures/hocking_county_seed.json --output outputs/hocking_county_leads.csv
```

## Pipeline

1. **Discovery**: find matching businesses.
2. **Entity resolution**: normalize businesses, websites, addresses, owners, parcels.
3. **Activity analysis**: estimate whether the business is growing, stable, or shrinking.
4. **Income estimation**: estimate annual revenue and cashflow ranges.
5. **Transition analysis**: estimate openness to acquisition discussion.
6. **Reporting**: emit sortable CSV with scores, evidence, confidence, and narrative.

## Status

This is a rough skeleton. Connectors are stubs, scoring models are heuristic placeholders, and the fixture data is illustrative.

## Visible agentic demo

To demonstrate retrieval → raw storage → parsing → normalized storage → scoring → CSV export, run:

```bash
python scripts/run_agentic_demo.py
```

Outputs are written to:

```text
outputs/demo/lead_finder_demo.sqlite
outputs/demo/hocking_county_agentic_demo.csv
```

See `docs/agentic_demo.md` for the step-by-step explanation.
