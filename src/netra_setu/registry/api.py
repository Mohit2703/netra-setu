"""Registry Portal API — SVC-004/001, REG-08 (published spec is itself a deliverable)."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/registry", tags=["registry"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# REG-06/07/08 onboarding, REG-13 map/filter, REG-19 search/export: not
# implemented in this scaffold — see docs/architecture/lld/ws1-registry-gis.md.
