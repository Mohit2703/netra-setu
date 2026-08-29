# netra-setu
Federated CCTV registry, GIS coverage analysis and video analytics for statewide policing. Purpose-bound access, forensic chain of custody, fully open source.

## Development

Architecture: [`docs/architecture/HLD.md`](docs/architecture/HLD.md), the
[ADRs](docs/architecture/adr/) and the per-workstream
[LLDs](docs/architecture/lld/). Requirements: [`docs/requirements/`](docs/requirements/).

```
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest
ruff check .
uvicorn netra_setu.app:app --reload
```

`src/netra_setu/` is one package per workstream (`registry`, `ingestion`,
`analytics`, `bridge`, `security`), plus `domain/` for the entities shared
across all of them. This is a scaffold, not a build-out — most requirement
IDs have a domain model but no implemented business logic yet; each
package's LLD is the source of truth for what it still needs.
