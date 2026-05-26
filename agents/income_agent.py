from __future__ import annotations

from models.business import BusinessCandidate, CashflowEstimate


def estimate_cashflow(candidate: BusinessCandidate) -> CashflowEstimate:
    """Estimate revenue/cashflow using rough capacity heuristics.

    This placeholder reads simple manually supplied observed_value fields:
    - rv_sites
    - cabins
    - campsites

    Future implementation should estimate capacity from websites, booking engines,
    maps, directories, and photos.
    """
    rv_sites = 0
    cabins = 0
    campsites = 0
    assumptions: list[str] = []

    for item in candidate.evidence:
        if isinstance(item.observed_value, dict):
            rv_sites = max(rv_sites, int(item.observed_value.get("rv_sites", 0) or 0))
            cabins = max(cabins, int(item.observed_value.get("cabins", 0) or 0))
            campsites = max(campsites, int(item.observed_value.get("campsites", 0) or 0))

    # Conservative rough Hocking Hills-style seasonal assumptions.
    # These are placeholders and should be calibrated with real operator data.
    rv_revenue_low = rv_sites * 65 * 105
    rv_revenue_high = rv_sites * 95 * 150
    cabin_revenue_low = cabins * 175 * 100
    cabin_revenue_high = cabins * 325 * 180
    campsite_revenue_low = campsites * 35 * 75
    campsite_revenue_high = campsites * 60 * 120

    revenue_low = rv_revenue_low + cabin_revenue_low + campsite_revenue_low
    revenue_high = rv_revenue_high + cabin_revenue_high + campsite_revenue_high

    if revenue_high == 0:
        return CashflowEstimate(
            confidence=0.05,
            assumptions=["No capacity evidence found; cannot estimate cashflow yet."],
            evidence=candidate.evidence,
        )

    assumptions.extend([
        f"rv_sites={rv_sites}, cabins={cabins}, campsites={campsites}",
        "Seasonal revenue model: unit_count × nightly_rate × occupied_nights.",
        "Cashflow estimated at 25%-45% of gross revenue before debt service.",
    ])

    return CashflowEstimate(
        estimated_revenue_low=round(revenue_low),
        estimated_revenue_high=round(revenue_high),
        estimated_cashflow_low=round(revenue_low * 0.25),
        estimated_cashflow_high=round(revenue_high * 0.45),
        confidence=0.35 if (rv_sites + cabins + campsites) > 0 else 0.1,
        assumptions=assumptions,
        evidence=candidate.evidence,
    )
