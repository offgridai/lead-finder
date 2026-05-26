from __future__ import annotations

from abc import ABC, abstractmethod

from models.business import BusinessCandidate


class BusinessDiscoveryConnector(ABC):
    """Interface for business discovery sources."""

    @abstractmethod
    def search(self, county: str, state: str, business_types: list[str]) -> list[BusinessCandidate]:
        raise NotImplementedError
