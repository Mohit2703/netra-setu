"""Security, forensics & compliance domain entities — SVC-013 through
SVC-017, SEC-*, FOR-*, CMP-01-15, VMS-23."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Purpose(StrEnum):
    """SEC-08: a controlled vocabulary, never free text."""

    INVESTIGATION = "investigation"
    COURT_ORDER = "court-order"
    OVERSIGHT_REVIEW = "oversight-review"
    MAINTENANCE = "maintenance"


class AuthorizationRequest(BaseModel):
    """SEC-07/SEC-08: rank + jurisdiction + purpose + time-box, jointly."""

    id: UUID = Field(default_factory=uuid4)
    requester_rank: int
    jurisdiction: str
    purpose: Purpose
    case_reference: str | None = None
    time_box_expires_at: datetime
    approved: bool | None = None  # None: not yet evaluated


class BreakGlassGrant(BaseModel):
    """SEC-09: two authorisers, expiring, mandatory review."""

    id: UUID = Field(default_factory=uuid4)
    first_authoriser_id: UUID
    second_authoriser_id: UUID | None = None
    granted_at: datetime | None = None
    expires_at: datetime | None = None
    review_task_open: bool = False


class WatchlistEntry(BaseModel):
    """SEC-10: irreversible embeddings, hard-capped gallery, mandatory expiry."""

    id: UUID = Field(default_factory=uuid4)
    embedding_ref: str  # opaque; the embedding itself never round-trips through this layer
    enrolled_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime


class AuditEvent(BaseModel):
    """SEC-11/FOR-08: append-only, independently verifiable."""

    id: UUID = Field(default_factory=uuid4)
    actor_id: UUID
    action: str
    subject: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ExternalCaseRef(BaseModel):
    """VMS-23. Build: SIM — validated against a mock eGujCop/CCTNS/ICJS."""

    case_number: str
    source_system: str


class ChainOfCustodyEntry(BaseModel):
    """FOR-08."""

    id: UUID = Field(default_factory=uuid4)
    segment_id: str
    action: str
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class EvidenceExport(BaseModel):
    """FOR-04: the only form in which video legitimately leaves custody."""

    id: UUID = Field(default_factory=uuid4)
    case_reference: str
    segment_ids: tuple[str, ...]
    hash_manifest: dict[str, str]
    custody_log: tuple[ChainOfCustodyEntry, ...]
    exported_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
