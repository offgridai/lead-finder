from __future__ import annotations

from models.business import BusinessCandidate
from .base import BusinessDiscoveryConnector


class GooglePlacesConnector(BusinessDiscoveryConnector):
    """Stub connector.

    Future implementation should use an approved API or licensed data source.
    Do not scrape Google pages directly.
    """

    def search(self, county: str, state: str, business_types: list[str]) -> list[BusinessCandidate]:
        return []
