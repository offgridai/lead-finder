from __future__ import annotations

import json
from pathlib import Path

from pipelines.hocking_county_campgrounds import run_from_fixture


def test_fixture_pipeline_produces_leads() -> None:
    records = json.loads(Path("evals/fixtures/hocking_county_seed.json").read_text())
    leads = run_from_fixture(records)
    assert len(leads) == 3
    assert all(lead.business.name for lead in leads)
    assert all(0 <= lead.activity.activity_score <= 100 for lead in leads)
    assert all(0 <= lead.transition.transition_score <= 100 for lead in leads)


def test_cashflow_ranges_are_ordered() -> None:
    records = json.loads(Path("evals/fixtures/hocking_county_seed.json").read_text())
    leads = run_from_fixture(records)
    for lead in leads:
        if lead.cashflow.estimated_revenue_low is not None:
            assert lead.cashflow.estimated_revenue_low <= lead.cashflow.estimated_revenue_high
            assert lead.cashflow.estimated_cashflow_low <= lead.cashflow.estimated_cashflow_high
