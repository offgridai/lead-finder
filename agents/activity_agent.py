from __future__ import annotations

from models.business import ActivityAnalysis, BusinessCandidate
from models.evidence import EvidenceItem, EvidenceType


def analyze_activity(candidate: BusinessCandidate) -> ActivityAnalysis:
    """Heuristic placeholder for operational activity scoring.

    Future implementation should use review velocity, website freshness, social posting,
    booking activity, permit activity, and observed amenity changes.
    """
    drivers: list[str] = []
    score = 45.0
    confidence = 0.25

    text_blob = " ".join([e.text or "" for e in candidate.evidence]).lower()

    if "online booking" in text_blob or "book now" in text_blob:
        score += 12
        drivers.append("online_booking_present")
    if "new" in text_blob or "expanded" in text_blob or "renovated" in text_blob:
        score += 15
        drivers.append("recent_growth_or_upgrade_language")
    if "seasonal" in text_blob:
        score += 3
        drivers.append("seasonal_operation_confirmed")
    if "outdated" in text_blob or "stale" in text_blob or "last updated" in text_blob:
        score -= 12
        drivers.append("digital_staleness_signal")
    if "maintenance complaints" in text_blob or "declining reviews" in text_blob:
        score -= 18
        drivers.append("negative_review_trend_signal")

    if candidate.website:
        confidence += 0.15
    if candidate.evidence:
        confidence += min(0.35, 0.05 * len(candidate.evidence))

    if score >= 70:
        trend = "growing"
    elif score >= 40:
        trend = "stable"
    else:
        trend = "shrinking"

    return ActivityAnalysis(
        activity_score=max(0, min(100, score)),
        trend=trend,
        confidence=max(0, min(1, confidence)),
        drivers=drivers or ["insufficient_activity_evidence"],
        evidence=candidate.evidence,
    )
