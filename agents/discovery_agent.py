from __future__ import annotations

from models.business import BusinessCandidate


def discover_from_fixture(records: list[dict]) -> list[BusinessCandidate]:
    """Load seed candidates from fixture JSON.

    Real discovery connectors should normalize their results into this same schema.
    """
    return [BusinessCandidate.model_validate(record) for record in records]
