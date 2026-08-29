"""Registry & GIS domain entities — SVC-001/002/003, REG-01 through REG-23."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

_URN_PATTERN = re.compile(r"^gj:cam:[a-z0-9-]+:[a-z0-9-]+:\d+$")


class Provenance(StrEnum):
    DECLARED = "declared"
    PROBED = "probed"
    FIELD_VERIFIED = "field-verified"


class ProvenancedValue[T](BaseModel):
    """REG-04: no metadata field without a provenance value and a confidence score."""

    value: T
    provenance: Provenance
    confidence: float = Field(ge=0.0, le=1.0)


class Owner(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    jurisdiction: str


class Site(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    owner_id: UUID


class HardwareRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    make: str
    model: str
    firmware_version: str
    installed_at: datetime


class Viewshed(BaseModel):
    """ADR 0003: 2D wedge inputs only — the spatial-store product is a separate ADR."""

    azimuth_degrees: float | None = Field(default=None, ge=0.0, lt=360.0)
    horizontal_fov_degrees: float | None = Field(default=None, gt=0.0, le=360.0)
    mounting_height_m: float | None = Field(default=None, gt=0.0)
    effective_range_m: float | None = Field(default=None, gt=0.0)

    @property
    def is_computable(self) -> bool:
        """REG-14's own stated gap: missing any input leaves no viewshed."""
        return None not in (
            self.azimuth_degrees,
            self.horizontal_fov_degrees,
            self.mounting_height_m,
            self.effective_range_m,
        )


class Camera(BaseModel):
    """REG-01: identity is the URN. Never referenced by IP, vendor ID or database key."""

    urn: str
    owner_id: UUID
    site_id: UUID
    position: ProvenancedValue[tuple[float, float]]
    viewshed: Viewshed = Field(default_factory=Viewshed)
    hardware: HardwareRecord
    relocated_from_urn: str | None = None
    synthetic: bool = False  # OQ-010: field proposed, not signed off — do not rely on this

    @field_validator("urn")
    @classmethod
    def _validate_urn(cls, v: str) -> str:
        if not _URN_PATTERN.match(v):
            raise ValueError(f"{v!r} is not a valid REG-01 URN (gj:cam:<district>:<dept>:<seq>)")
        return v


class MergeQueueEntry(BaseModel):
    """REG-11: candidate duplicate. Resolution is always a human decision."""

    id: UUID = Field(default_factory=uuid4)
    candidate_urns: tuple[str, str]
    detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    resolved: bool = False
