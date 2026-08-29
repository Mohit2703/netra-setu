from datetime import UTC, datetime
from uuid import uuid4

import pytest

from netra_setu.domain.camera import (
    Camera,
    HardwareRecord,
    Provenance,
    ProvenancedValue,
    Viewshed,
)


def _hardware() -> HardwareRecord:
    return HardwareRecord(
        make="x", model="y", firmware_version="1.0", installed_at=datetime.now(UTC)
    )


def _position() -> ProvenancedValue[tuple[float, float]]:
    return ProvenancedValue(value=(23.02, 72.57), provenance=Provenance.DECLARED, confidence=0.5)


def test_camera_urn_must_match_reg_01_scheme() -> None:
    with pytest.raises(ValueError, match="REG-01"):
        Camera(
            urn="not-a-valid-urn",
            owner_id=uuid4(),
            site_id=uuid4(),
            position=_position(),
            hardware=_hardware(),
        )


def test_valid_urn_constructs_and_defaults_non_synthetic() -> None:
    camera = Camera(
        urn="gj:cam:ahmedabad:police:1",
        owner_id=uuid4(),
        site_id=uuid4(),
        position=_position(),
        hardware=_hardware(),
    )
    assert camera.synthetic is False


def test_viewshed_not_computable_without_all_four_inputs() -> None:
    assert Viewshed(azimuth_degrees=90.0).is_computable is False
    assert (
        Viewshed(
            azimuth_degrees=90.0,
            horizontal_fov_degrees=60.0,
            mounting_height_m=5.0,
            effective_range_m=30.0,
        ).is_computable
        is True
    )
