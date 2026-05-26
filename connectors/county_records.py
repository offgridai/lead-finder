from __future__ import annotations


class CountyRecordsConnector:
    """Stub for assessor/recorder/GIS lookup.

    Intended outputs: parcels, owner names/entities, transfer history, tax status,
    liens, acreage, zoning, and source evidence.
    """

    def lookup_by_address(self, address: str) -> dict | None:
        return None
