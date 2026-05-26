from __future__ import annotations

from agents.activity_agent import analyze_activity
from agents.discovery_agent import discover_from_fixture
from agents.income_agent import estimate_cashflow
from agents.report_agent import build_narrative
from agents.transition_agent import estimate_transition_likelihood
from models.business import LeadRecord


def run_from_fixture(records: list[dict]) -> list[LeadRecord]:
    candidates = discover_from_fixture(records)
    leads: list[LeadRecord] = []

    for candidate in candidates:
        activity = analyze_activity(candidate)
        cashflow = estimate_cashflow(candidate)
        transition = estimate_transition_likelihood(candidate)
        lead = LeadRecord(
            business=candidate,
            activity=activity,
            cashflow=cashflow,
            transition=transition,
            acquisition_narrative="",
            notes="Fixture-based placeholder analysis; verify before outreach.",
        )
        lead.acquisition_narrative = build_narrative(lead)
        leads.append(lead)

    return sorted(
        leads,
        key=lambda x: (x.transition.transition_score, x.activity.activity_score, x.cashflow.estimated_cashflow_high or 0),
        reverse=True,
    )
