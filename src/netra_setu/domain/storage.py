"""Storage & retention domain entities — SVC-011, VMS-16 through VMS-20."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class StorageTier(StrEnum):
    """VMS-18. Hot and warm are edge-resident; only cold is centrally
    replicated — VMS-16 keeps raw video off GSWAN by default (HLD.md §3)."""

    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


class CaseLink(BaseModel):
    """VMS-19: the retention clock is a function of case status, not camera."""

    segment_id: str
    case_reference: str | None = None


class DeletionCertificate(BaseModel):
    """VMS-20."""

    segment_id: str
    deleted_at: datetime
    certificate_id: str
