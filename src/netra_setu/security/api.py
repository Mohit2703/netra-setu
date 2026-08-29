"""Authorization/PDP API — SVC-013, SEC-07/SEC-08."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/authz", tags=["security"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# SEC-07/08 policy evaluation, SEC-09 break-glass: not implemented in this
# scaffold — see docs/architecture/lld/ws5-security-forensics-compliance.md.
