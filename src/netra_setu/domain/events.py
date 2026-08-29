"""Analytics domain entities — SVC-008/018, VMS-10 through VMS-15, VMS-24."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class InferenceTier(StrEnum):
    """VMS-14."""

    FULL_RATE = "full-rate"
    SAMPLED = "sampled"
    EVENT_TRIGGERED = "event-triggered"


class SpecifiedEvent(StrEnum):
    """VMS-12: the enumerated set only — no suspicion or intent scoring."""

    UNATTENDED_OBJECT = "unattended-object"
    CROWD_DENSITY = "crowd-density"
    WRONG_WAY = "wrong-way"
    LOITERING = "loitering"
    CAMERA_TAMPER = "camera-tamper"


class ModelProvenance(BaseModel):
    """VMS-15: every analytics output persists these five fields, no exceptions."""

    model_name: str
    model_version: str
    model_artefact_hash: str
    input_frame_ref: str
    confidence: float = Field(ge=0.0, le=1.0)


class DetectionRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    camera_urn: str
    captured_at: datetime
    provenance: ModelProvenance


class Alert(BaseModel):
    """VMS-24."""

    id: UUID = Field(default_factory=uuid4)
    camera_urn: str
    jurisdiction: str
    raised_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Disposition(StrEnum):
    TRUE_POSITIVE = "true-positive"
    FALSE_POSITIVE = "false-positive"


class AlertDisposition(BaseModel):
    alert_id: UUID
    disposition: Disposition
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
