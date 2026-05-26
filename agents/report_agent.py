from __future__ import annotations

import csv
from pathlib import Path

from models.business import LeadRecord


def build_narrative(lead: LeadRecord) -> str:
    b = lead.business
    return (
        f"{b.name} appears to be a {b.business_type.value.replace('_', ' ')} with "
        f"activity trend '{lead.activity.trend}' and {lead.transition.transition_likelihood} "
        f"estimated openness to acquisition discussion. Key drivers: "
        f"activity={', '.join(lead.activity.drivers[:3])}; "
        f"transition={', '.join(lead.transition.drivers[:3])}."
    )


def write_csv(leads: list[LeadRecord], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "business_name",
        "business_type",
        "address",
        "website",
        "county",
        "state",
        "activity_score",
        "activity_trend",
        "activity_confidence",
        "estimated_revenue_low",
        "estimated_revenue_high",
        "estimated_cashflow_low",
        "estimated_cashflow_high",
        "cashflow_confidence",
        "transition_likelihood",
        "transition_score",
        "likely_transition_driver",
        "transition_confidence",
        "acquisition_narrative",
        "evidence_urls",
        "notes",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            evidence_urls = sorted({str(e.url) for e in lead.business.evidence if e.url})
            writer.writerow({
                "business_name": lead.business.name,
                "business_type": lead.business.business_type.value,
                "address": lead.business.address,
                "website": str(lead.business.website) if lead.business.website else "",
                "county": lead.business.county,
                "state": lead.business.state,
                "activity_score": round(lead.activity.activity_score, 1),
                "activity_trend": lead.activity.trend,
                "activity_confidence": round(lead.activity.confidence, 2),
                "estimated_revenue_low": lead.cashflow.estimated_revenue_low,
                "estimated_revenue_high": lead.cashflow.estimated_revenue_high,
                "estimated_cashflow_low": lead.cashflow.estimated_cashflow_low,
                "estimated_cashflow_high": lead.cashflow.estimated_cashflow_high,
                "cashflow_confidence": round(lead.cashflow.confidence, 2),
                "transition_likelihood": lead.transition.transition_likelihood,
                "transition_score": round(lead.transition.transition_score, 1),
                "likely_transition_driver": lead.transition.likely_transition_driver,
                "transition_confidence": round(lead.transition.confidence, 2),
                "acquisition_narrative": lead.acquisition_narrative,
                "evidence_urls": " | ".join(evidence_urls),
                "notes": lead.notes or "",
            })


def lead_to_csv_row(lead: LeadRecord) -> dict[str, object]:
    evidence_urls = sorted({str(e.url) for e in lead.business.evidence if e.url})
    return {
        "business_name": lead.business.name,
        "business_type": lead.business.business_type.value,
        "address": lead.business.address,
        "website": str(lead.business.website) if lead.business.website else "",
        "county": lead.business.county,
        "state": lead.business.state,
        "activity_score": round(lead.activity.activity_score, 1),
        "activity_trend": lead.activity.trend,
        "activity_confidence": round(lead.activity.confidence, 2),
        "estimated_revenue_low": lead.cashflow.estimated_revenue_low,
        "estimated_revenue_high": lead.cashflow.estimated_revenue_high,
        "estimated_cashflow_low": lead.cashflow.estimated_cashflow_low,
        "estimated_cashflow_high": lead.cashflow.estimated_cashflow_high,
        "cashflow_confidence": round(lead.cashflow.confidence, 2),
        "transition_likelihood": lead.transition.transition_likelihood,
        "transition_score": round(lead.transition.transition_score, 1),
        "likely_transition_driver": lead.transition.likely_transition_driver,
        "transition_confidence": round(lead.transition.confidence, 2),
        "acquisition_narrative": lead.acquisition_narrative,
        "evidence_urls": " | ".join(evidence_urls),
        "notes": lead.notes or "",
    }
