# 0009 — Simulated-fleet architecture

**Scope.** How the 80,000-camera scale story is demonstrated without 80,000
real cameras. Requirement IDs: build-class discipline (LIVE/SIM/MODEL,
`SCOPE.md`). Depends on ADR 0004's connector port.

## Context

The kickoff constraint is explicit and named: "one code path serves a
handful of real cameras and a simulated 80,000-camera fleet — the synthetic
fleet is a driver behind the same port as a real ONVIF camera, not a
parallel mock stack." `CAPACITY.md` §3's load-test plan already
half-specifies this: "500–2,000 synthetic cameras, produced by FFmpeg
looping recorded files against the real connector stack," and warns
explicitly against presenting "a modelled number as a measured one."

## Options considered

1. **Parallel mock stack** — a distinct simulation-mode code path used only
   for load testing/demos. Fastest to build, but directly contradicts the
   named constraint: a parallel path means the scale story (a named Stage 2
   deliverable) never actually exercises the real ingestion/analytics code —
   exactly the failure mode `CAPACITY.md` §3 warns against.
2. **Synthetic driver behind the real connector port** — a
   `SimulatedCameraDriver` implementing ADR 0004's capability-negotiated port
   exactly as a real vendor adapter would (declaring `stream` +
   `device-metadata`, streaming FFmpeg-looped recorded video per
   `CAPACITY.md` §3), registered via `REG-08`'s real onboarding API with real
   `REG-01` URNs, invisible to every downstream consumer.
3. **Synthetic driver behind the port, registered in a separate
   shadow-registry namespace** rather than the same URN space. Structurally
   impossible to confuse with real data, but stops exercising the actual
   Registry onboarding/dedup path — a weaker version of option 2's own goal,
   and closer to option 1's parallel-stack problem, just moved one layer up
   the stack.

## Decision

Option 2. Synthetic cameras are real connector-port clients and real
registry entrants, distinguished only by an explicit synthetic flag.

## Consequences

- Every consumer downstream of SVC-005 (Analytics Runtime, Event Bus,
  Storage Tier Manager, Alert Routing, Registry) is genuinely tested at
  whatever scale a load-test run reaches — a 500–2,000-camera test exercises
  the same code a real 20–50-feed demo does.
- A synthetic camera is otherwise indistinguishable from a real one in the
  registry, which is exactly the point but also the risk: a new, explicit
  `synthetic` field (distinct from `REG-04`'s provenance values, which
  describe metadata accuracy, not whether the camera itself is real) is
  needed so P1's coverage/gap-analysis reports and P6's oversight dashboard
  never silently conflate load-test data with the real fleet. **Not invented
  unilaterally here** — per the register's own rule, proposed for the user's
  sign-off in [`OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) OQ-010.
- Directly depends on ADR 0004's capability-negotiated port; if that port's
  capability vocabulary changes, the simulated driver must track it.

## Reversibility cost

Two-way door. The synthetic flag is additive — a new field, not a change to
`REG-01`'s URN scheme or `REG-11`'s dedup logic.

## Revisit trigger

A load-test run at 2,000+ synthetic cameras shows the synthetic flag is
insufficient isolation in practice (e.g., synthetic records leaking into a
real gap-analysis report shown to P1) — escalate to option 3's namespace
separation only if option 2 demonstrably fails.

## What this does not cover

The actual creation of the synthetic-flag field/requirement ID — pending
user sign-off, tracked in `OPEN-QUESTIONS.md` (OQ-010).
