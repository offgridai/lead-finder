from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from .evidence import EvidenceItem


class BusinessType(str, Enum):
    CAMPGROUND = "campground"
    RV_PARK = "rv_park"
    CABIN_RESORT = "cabin_resort"
    GLAMPING = "glamping"
    MIXED_OUTDOOR_LODGING = "mixed_outdoor_lodging"
    UNKNOWN = "unknown"


class BusinessCandidate(BaseModel):
    business_id: str
    name: str
    business_type: BusinessType = BusinessType.UNKNOWN
    address: str | None = None
    county: str | None = None
    state: str | None = None
    website: HttpUrl | None = None
    phone: str | None = None
    source_urls: list[HttpUrl] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)


class ActivityAnalysis(BaseModel):
    activity_score: float = Field(ge=0.0, le=100.0)
    trend: Literal["growing", "stable", "shrinking", "unknown"]
    confidence: float = Field(ge=0.0, le=1.0)
    drivers: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)


class CashflowEstimate(BaseModel):
    estimated_revenue_low: int | None = None
    estimated_revenue_high: int | None = None
    estimated_cashflow_low: int | None = None
    estimated_cashflow_high: int | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    assumptions: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)


class TransitionAnalysis(BaseModel):
    transition_score: float = Field(ge=0.0, le=100.0)
    transition_likelihood: Literal["low", "moderate", "high", "unknown"]
    likely_transition_driver: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    drivers: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)


class LeadRecord(BaseModel):
    business: BusinessCandidate
    activity: ActivityAnalysis
    cashflow: CashflowEstimate
    transition: TransitionAnalysis
    acquisition_narrative: str
    notes: str | None = None
