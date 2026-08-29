"""Vendor connector port — ADR 0004. SVC-005, VMS-01 through VMS-06."""

from __future__ import annotations

from enum import StrEnum
from typing import Protocol, runtime_checkable


class ConnectorCapability(StrEnum):
    """ADR 0004's initial vocabulary — adding one is a two-way door,
    renaming one a shipped connector already declares is not."""

    STREAM = "stream"
    DEVICE_METADATA = "device-metadata"
    ANALYTICS_EVENTS = "analytics-events"
    PTZ_CONTROL = "ptz-control"
    HEALTH = "health"


@runtime_checkable
class Connector(Protocol):
    """Every vendor adapter, the ITMS/VISWAS bridge (SVC-007) and the
    simulated-fleet driver (ADR 0009) implement this same port — a connector
    declares what it offers, consumers never assume the full surface."""

    capabilities: frozenset[ConnectorCapability]

    def supports(self, capability: ConnectorCapability) -> bool: ...
