from __future__ import annotations

from pydantic import BaseModel, Field

from .evidence import EvidenceItem


class OwnerProfile(BaseModel):
    owner_name: str | None = None
    owner_entity: str | None = None
    mailing_address: str | None = None
    ownership_start_year: int | None = None
    related_entities: list[str] = Field(default_factory=list)
    parcels: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)

    @property
    def ownership_duration_years(self) -> int | None:
        if self.ownership_start_year is None:
            return None
        # Keep deterministic; updated by callers if exact current year matters.
        return 2026 - self.ownership_start_year
