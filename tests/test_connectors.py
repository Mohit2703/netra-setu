from netra_setu.ingestion.connectors.base import ConnectorCapability


class _FakeBridgeConnector:
    """Stands in for SVC-007 — declares analytics-events, never stream (OQ-003)."""

    capabilities = frozenset(
        {ConnectorCapability.ANALYTICS_EVENTS, ConnectorCapability.DEVICE_METADATA}
    )

    def supports(self, capability: ConnectorCapability) -> bool:
        return capability in self.capabilities


def test_bridge_connector_declares_no_stream_capability() -> None:
    bridge = _FakeBridgeConnector()
    assert bridge.supports(ConnectorCapability.ANALYTICS_EVENTS) is True
    assert bridge.supports(ConnectorCapability.STREAM) is False
