# 0004 — Vendor connector port

**Scope.** The interface every camera/feed source integrates through —
vendor adapters, the ITMS/VISWAS bridge, and the simulated-fleet driver
alike. Requirement IDs: `VMS-01`–`VMS-06`. Shaped by
[`OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) OQ-003 (bridge-only for VISWAS);
feeds ADR 0009.

## Context

`VMS-01` requires that adding a vendor or protocol requires no core
modification. `VMS-02`–`04` assume a real video/device stream; `VMS-05`
(GB/T 28181) and `VMS-06` (analog/DVR) are already marked `Build: MODEL`,
"interface defined, implementation deferred" — the register itself already
anticipates connectors that don't offer the full surface a naive stream-only
port would assume. OQ-003 (resolved 2026-08-29) requires the port to also
accept SVC-007, the ITMS/VISWAS bridge, which offers pre-computed analytics
*events*, never raw video, as a first-class input — not a special case.

## Options considered

1. **Stream-first port**, with analytics-event ingestion bolted on outside
   the main interface. Matches most connectors' literal shape, but forces
   SVC-007 to fake a video stream it structurally does not have just to
   satisfy a port it doesn't fit — undoing the anti-corruption-layer purpose
   SVC-007 exists for. Also awkward for `VMS-06`, where sometimes only an
   alarm/contact-closure signal is available.
2. **Capability-negotiated port.** Every connector declares which
   capabilities it offers from a fixed set (`stream`, `device-metadata`,
   `analytics-events`, `ptz-control`, `health`); the port's required surface
   is minimal (identity + ≥1 capability); consumers query capabilities
   before use rather than assuming full surface. This *is* what `VMS-01`
   already asks for, and is exactly how `VMS-05`/`06`'s already-deferred,
   weaker-than-full connectors are meant to fit without special-casing every
   consumer.
3. **Typed interface hierarchy** (`StreamingConnector` /
   `EventBridgeConnector` / `HybridConnector`). Type-safe at wiring time, but
   any future connector offering both stream and analytics-events (plausible
   for a modern vendor VMS API) forces a hybrid type duplicating both
   interfaces' methods — converges back to option 2's shape with more
   ceremony.

## Decision

Option 2. Capability-negotiated connector port; the initial capability
vocabulary is `stream`, `device-metadata`, `analytics-events`, `ptz-control`,
`health`.

## Consequences

- SVC-005 (Connector SDK) defines the port; SVC-007 (ITMS/VISWAS Bridge)
  declares `analytics-events` + `device-metadata` only, no `stream` — a
  first-class connector, not a workaround.
- SVC-008 (Analytics Runtime) and SVC-009 (Live View Gateway) must both
  handle "capability absent" as a normal, expected case — arguably free,
  given `NFR-07`'s graceful-degradation posture already requires equivalent
  handling elsewhere.
- Directly sets up ADR 0009 (simulated fleet): the synthetic driver declares
  the same capabilities a real connector would and is indistinguishable to
  any consumer.

## Reversibility cost

Two-way door in principle (capability sets can grow), but functions as a de
facto one-way door once several connectors and consumers are written against
a specific vocabulary. Getting the *initial* capability set right matters
more than for most decisions in this document.

## Revisit trigger

A real vendor connector (`VMS-04`: Hikvision/Axis/Dahua) is implemented and
needs a capability the initial set didn't anticipate.

## What this does not cover

The wire-level shape of each capability's data (e.g., the exact
`analytics-events` payload schema) — WS-2/WS-3 LLD work.
