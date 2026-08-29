# 0001 — Registry as system of record vs. projection over departmental sources

**Scope.** How camera-metadata truth is owned between netra-setu's registry
and the departments who actually hold the cameras. Requirement IDs:
`REG-01`–`REG-12`, especially `REG-04`.

## Context

`REG-04` requires every metadata field to carry a provenance value
(`declared`/`probed`/`field-verified`) and a confidence score — truth here is
already graded, not absolute, by requirement. `REG-11` requires
human-adjudicated deduplication; merges are never automatic. P4 (Department
Nodal Officer)'s stated need is "onboard my cameras without losing control."
The federation thesis (`CLAUDE.md`; kickoff §1.2) tests every decision against
"does this require the incumbent to give something up?" Most of the ~62,500
delta cameras have no existing systematic inventory at all — they are *delta*
precisely because no registry currently exists for them.

## Options considered

1. **Full system of record.** netra-setu's copy becomes authoritative the
   moment a camera is onboarded; any departmental system becomes secondary.
   Simplest consistency model, but forces a department with its own asset
   system to treat it as downstream of ours — conflicts with the federation
   thesis and P4's stated need directly.
2. **Live projection over departmental sources.** netra-setu holds no
   independent truth, only a continuously-synced reflection of each
   department's own system of record. Politically ideal, but most delta
   departments have nothing to project *from* — solves a problem (existing
   departmental systems of record) that mostly doesn't exist yet, while adding
   real reconciliation complexity for the minority that do have one.
3. **Split ownership by field type.** netra-setu is system of record only for
   what only it can define — URN identity (`REG-01`), coverage geometry
   (`REG-14`), cross-department confidence/provenance (`REG-04`). Each `Owner`
   remains the upstream source for declared facts about their own physical
   asset, pushed in via `REG-08`'s API or `REG-06`/`REG-07`'s onboarding paths
   — netra-setu never reaches out to pull from a departmental system.

## Decision

Option 3. Registry is system of record for registry-derived facts (identity,
coverage, provenance/confidence); owners remain the source for declared facts
about their own assets, submitted through the existing onboarding channels
rather than a bespoke per-department sync integration.

## Consequences

- `REG-04`'s provenance/confidence model is the reconciliation mechanism — no
  new mechanism invented. A later owner-submitted update to a
  `field-verified` record is a confidence *event*, not a silent overwrite; the
  exact reconciliation policy (does a new `declared` update ever downgrade a
  `field-verified` record, or sit alongside it pending re-verification) is
  LLD-level work (WS-1), not decided here.
- SVC-001 (Registry Core) is the only writer of `Camera.urn`,
  `Camera.viewshed`, `Camera.provenance`. No other container writes these
  fields.
- P4's "own my cameras" need is satisfied procedurally (their submissions are
  authoritative for their own declared facts), not architecturally (they don't
  run a competing system of record) — deliberate, to keep the architecture
  simple. A department insisting on live-sync integration later is a new
  connector-shaped problem (ADR 0004's port), not a registry-ownership one.

## Reversibility cost

Two-way door. A policy and API-contract choice on top of `REG-04`'s existing
schema, not a schema-destroying one. Becomes expensive only after a specific
department has built a real integration against a specific reconciliation
contract.

## Revisit trigger

A department with an existing, authoritative asset-management system asks to
integrate it directly rather than push updates through `REG-08`'s API.

## What this does not cover

The exact reconciliation/confidence-decay policy when a declared update
conflicts with a field-verified record — WS-1 LLD work.
