"""Bridge & Tracking domain entities — SVC-012, BRG-01 through BRG-05, VMS-21/22."""

from __future__ import annotations

from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RoadSegmentBinding(BaseModel):
    """BRG-01."""

    camera_urn: str
    osm_edge_id: str
    direction_degrees: float = Field(ge=0.0, lt=360.0)


class CandidateSet(BaseModel):
    """BRG-02: reachable within a plausible-speed travel-time window, not fleet-wide."""

    origin_camera_urn: str
    origin_timestamp: str
    candidate_camera_urns: tuple[str, ...]


class RouteHop(BaseModel):
    camera_urn: str
    confidence: float = Field(ge=0.0, le=1.0)


class TrackingRoute(BaseModel):
    """VMS-22: a confidence value per hop, not one score for the whole route."""

    query_id: UUID = Field(default_factory=uuid4)
    hops: tuple[RouteHop, ...]


class GapFinding(BaseModel):
    """BRG-04: a discontinuity filed against a road segment, feeding REG-16."""

    road_segment_id: str
    discontinuity_seconds: float
