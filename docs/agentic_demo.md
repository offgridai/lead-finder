# Visible Agentic Demo

This repo intentionally includes a small deterministic demo that proves the mechanics of the agent pipeline before any live integrations are added.

Run:

```bash
python scripts/run_agentic_demo.py
```

It demonstrates:

1. **Retrieval** — `DemoSourceConnector` reads local HTML source pages as stand-ins for Google Maps, county records, tourism directories, etc.
2. **Raw storage** — raw retrieved documents are saved into SQLite in `raw_documents`.
3. **Parsing** — `parse_demo_business_page` extracts normalized `BusinessCandidate` records from raw HTML.
4. **Normalized storage** — parsed candidates are saved into SQLite in `candidates`.
5. **Agent steps** — activity, cashflow, and transition agents each run independently.
6. **Lead storage** — final lead records are saved into SQLite in `leads`.
7. **CSV export** — the final sortable table is written to `outputs/demo/hocking_county_agentic_demo.csv`.

The goal is not to produce real acquisition leads yet. The goal is to make every stage inspectable so the project can be expanded safely.

## Next connectors to implement

Replace or supplement the demo connector with:

- Google Places / Maps API or licensed equivalent
- Hocking County auditor / recorder data
- Ohio Secretary of State business search
- campground directories
- review platforms where access is permitted
- business websites and booking calendars where terms allow

Each connector should emit `RetrievedDocument` or a similarly raw source object before parsing. Do not skip raw storage.
