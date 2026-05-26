from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class EvidenceType(str, Enum):
    WEBSITE = "website"
    REVIEW = "review"
    DIRECTORY = "directory"
    PUBLIC_RECORD = "public_record"
    BUSINESS_REGISTRY = "business_registry"
    PERMIT = "permit"
    SOCIAL = "social"
    BOOKING = "booking"
    MANUAL_NOTE = "manual_note"


class EvidenceItem(BaseModel):
    type: EvidenceType
    source_name: str
    url: HttpUrl | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: str | None = None
    text: str | None = None
    observed_value: Any | None = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
