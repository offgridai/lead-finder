from __future__ import annotations

from models.business import BusinessCandidate, TransitionAnalysis


def estimate_transition_likelihood(candidate: BusinessCandidate) -> TransitionAnalysis:
    """Estimate openness to acquisition discussion from public/business signals.

    This is deliberately framed as transition likelihood, not distress or vulnerability.
    """
    score = 35.0
    confidence = 0.2
    drivers: list[str] = []
    text_blob = " ".join([e.text or "" for e in candidate.evidence]).lower()

    if "family owned" in text_blob or "family-operated" in text_blob:
        score += 10
        drivers.append("family_operated_business")
    if "since 19" in text_blob or "owned for" in text_blob or "long-term owner" in text_blob:
        score += 18
        drivers.append("long_term_ownership_signal")
    if "retire" in text_blob or "retirement" in text_blob:
        score += 25
        drivers.append("retirement_language")
    if "stale" in text_blob or "outdated" in text_blob or "no recent updates" in text_blob:
        score += 10
        drivers.append("digital_staleness")
    if "expanded" in text_blob or "new cabins" in text_blob or "new rv sites" in text_blob:
        score -= 10
        drivers.append("recent_reinvestment_reduces_sale_likelihood")
    if "second generation" in text_blob or "next generation" in text_blob:
        score -= 8
        drivers.append("succession_or_continuity_signal")

    if candidate.evidence:
        confidence += min(0.45, 0.06 * len(candidate.evidence))

    score = max(0, min(100, score))
    if score >= 70:
        likelihood = "high"
    elif score >= 45:
        likelihood = "moderate"
    else:
        likelihood = "low"

    driver = drivers[0] if drivers else "insufficient_transition_evidence"
    return TransitionAnalysis(
        transition_score=score,
        transition_likelihood=likelihood,
        likely_transition_driver=driver,
        confidence=max(0, min(1, confidence)),
        drivers=drivers or [driver],
        evidence=candidate.evidence,
    )
