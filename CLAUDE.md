# netra-setu

Federated CCTV registry, GIS coverage analysis and video analytics for
statewide policing. Purpose-bound access, forensic chain of custody,
fully open source.

The thesis: cameras stay where they are, owned by whoever owns them. This
system adds a registry, a coverage model, an authorisation gate and an
evidence pipeline on top of infrastructure that already exists.

## Status

Pre-implementation. There is no application code and none should be written
yet. Current work is architecture: HLD, then ADRs, then LLD per workstream.

Do not scaffold. Do not create package manifests, Dockerfiles, migrations or
CI config. If a task appears to need them, stop and ask.

## Layout

- `docs/architecture/HLD.md` — high-level design
- `docs/architecture/adr/` — one file per load-bearing decision
- `docs/architecture/lld/` — one file per workstream
- `docs/architecture/OPEN-QUESTIONS.md` — running list, never allowed to be empty

Application code will live under `src/` once the architecture settles.

Conventions for design documents are in `.claude/rules/architecture-docs.md`.
They load automatically when working under `docs/architecture/`.

## Requirements

`docs/requirements/REGISTER.md` is the single source of truth for requirements.
Read it on demand. Do not import it.

- `docs/requirements/REGISTER.md` — every requirement ID and statement
- `docs/requirements/CAPACITY.md` — NFR targets and the capacity model
- `docs/requirements/COMPLIANCE.md` — control matrix
- `docs/requirements/SCOPE.md` — demo scope and workstreams
- `docs/requirements/CHANGELOG.md` — append-only history of ID changes

Prefixes: REG- registry, VMS- video management, BRG- Model 1 / Model 4 bridge,
NFR- non-functional, FOR- forensics, SEC- security, CMP- compliance.

Rules:
- Cite requirement IDs in every design decision.
- Never invent an ID. If a design needs a requirement that does not exist, add
  it to `docs/architecture/OPEN-QUESTIONS.md` and ask before creating one.
- Never renumber or reuse an ID.
- Changing a requirement's meaning means an entry in CHANGELOG.md in the same
  commit, and checking which design docs cite that ID.

## Constraints

- Open source only. Flag any dependency whose licence is unclear.
- Assume adversarial camera networks. Authentication and transport security
  are architectural concerns, not deployment configuration.
- Prefer boring technology. Novel choices need a justification against a
  boring baseline.

## Working agreements

- Plan before code.
- Write open questions down rather than deciding silently.
- This file is shared via source control. Keep personal context, credentials,
  local paths and scratch notes out of it — use `CLAUDE.local.md`, which is
  gitignored.