from __future__ import annotations

import re

from bs4 import BeautifulSoup

from connectors.demo_sources import RetrievedDocument
from models.business import BusinessCandidate, BusinessType
from models.evidence import EvidenceItem, EvidenceType


def _business_type(value: str) -> BusinessType:
    normalized = value.strip().lower().replace(" ", "_")
    try:
        return BusinessType(normalized)
    except ValueError:
        return BusinessType.UNKNOWN


def parse_demo_business_page(doc: RetrievedDocument) -> BusinessCandidate:
    soup = BeautifulSoup(doc.raw_text, "html.parser")
    root = soup.select_one("[data-business]")
    if root is None:
        raise ValueError(f"No [data-business] block found in {doc.source_url}")

    def field(name: str) -> str | None:
        node = root.select_one(f"[data-field='{name}']")
        return node.get_text(" ", strip=True) if node else None

    name = field("name") or "Unknown Business"
    page_text = root.get_text(" ", strip=True)

    def first_int(pattern: str) -> int:
        match = re.search(pattern, page_text, re.IGNORECASE)
        return int(match.group(1)) if match else 0

    observed = {
        "source_url": doc.source_url,
        "rv_sites": first_int(r"(\d+)\s+(?:full-hookup\s+)?(?:rv\s+)?sites"),
        "cabins": first_int(r"(\d+)\s+cabins"),
        "campsites": first_int(r"(\d+)\s+(?:campsites|camping sites)"),
    }

    candidate = BusinessCandidate(
        business_id=(name.lower().replace(" ", "-").replace("'", "")),
        name=name,
        business_type=_business_type(field("type") or "unknown"),
        address=field("address"),
        county=field("county"),
        state=field("state"),
        website=field("website"),
        phone=field("phone"),
        source_urls=[],
        evidence=[
            EvidenceItem(
                type=EvidenceType.DIRECTORY,
                source_name="demo_local_html",
                title="business_discovery",
                text=page_text,
                observed_value=observed,
                confidence=0.95,
            )
        ],
    )
    return candidate
