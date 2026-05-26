from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class RetrievedDocument:
    source_name: str
    source_url: str
    content_type: str
    retrieved_at: str
    raw_text: str


class DemoSourceConnector:
    """Retrieves local demo pages as if they came from external sources.

    This is intentionally boring and deterministic. It proves the agentic pipeline shape
    before you plug in Google Places, county records, Ohio SOS, TripAdvisor, etc.
    """

    def __init__(self, fixture_dir: Path):
        self.fixture_dir = fixture_dir

    def retrieve(self, county: str, state: str, business_types: list[str]) -> list[RetrievedDocument]:
        docs: list[RetrievedDocument] = []
        now = datetime.now(timezone.utc).isoformat()
        for path in sorted(self.fixture_dir.glob("*.html")):
            docs.append(
                RetrievedDocument(
                    source_name="demo_local_html",
                    source_url=f"file://{path}",
                    content_type="text/html",
                    retrieved_at=now,
                    raw_text=path.read_text(encoding="utf-8"),
                )
            )
        return docs
