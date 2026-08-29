# 0008 — Camera trust bootstrap

**Scope.** How a camera or its gateway proves identity at onboarding, across
radically heterogeneous vendor capability. Requirement IDs: `SEC-01`,
`SEC-02`, `SEC-05`, `VMS-06`, `VMS-07`; `CLAUDE.md`'s "assume adversarial
camera networks" constraint.

## Context

`SEC-01` requires no implicit trust extended from any camera network
segment, with all input authenticated and validated before use. `SEC-17`
names camera spoofing and registry poisoning as modelled threats. `VMS-06`
already acknowledges analog cameras with no IP interface, integrated at
DVR/NVR level. The fleet is explicitly heterogeneous by design of the
problem itself (kickoff §1.2 — the ~62,500 delta cameras are unregistered,
various vendors, "no registry, no standard interface, no known owner").

## Options considered

1. **Uniform cryptographic bootstrap for every camera** — no device
   certificate, no onboarding. The strongest possible reading of `SEC-01`,
   but flatly incompatible with `VMS-06`'s analog/legacy fleet and much of
   the delta fleet, which structurally cannot present a device certificate.
   Excludes exactly the under-instrumented cameras that are the project's
   actual problem — self-defeating.
2. **No per-camera cryptographic identity; trust by network segment only.**
   Works uniformly regardless of vendor capability, but directly violates
   `SEC-01` and makes registry poisoning (`SEC-17`) trivial — a compromised
   device on a trusted VLAN is indistinguishable from the real camera.
   Disqualified.
3. **Tiered trust, reusing `REG-04`'s provenance/confidence model.** Cameras
   that support a cryptographic identity mechanism (TLS client cert, ONVIF
   WS-Security, or any device the Connector SDK can provision a
   `SEC-05`-managed credential to) get full device-level authentication.
   Cameras that structurally cannot are onboarded at the Connector/DVR-NVR
   boundary instead — the Connector (an authenticated, `SEC-05`-credentialed
   principal) is what's actually trusted, and the individual camera behind it
   carries a permanent, visible "no device-level authentication" flag that
   narrows what that feed is eligible for (e.g., ineligible for `VMS-17`'s
   always-record high-security subset without a compensating control),
   visible on P6's oversight dashboard.

## Decision

Option 3. Tiered trust bootstrap: device-level authentication where the
camera supports it; Connector/gateway-level authentication with a visible
low-trust flag and narrowed eligibility where it doesn't.

## Consequences

- Reuses `REG-04`'s existing provenance/confidence mechanism applied to
  trust rather than only to metadata accuracy — not a new taxonomy.
- `SEC-01` stays honestly true at the boundary that can actually be
  authenticated (the Connector), rather than falsely claiming per-device
  authentication that doesn't exist for a large share of the fleet.
- The specific eligibility-narrowing policy (exactly what a low-trust feed
  cannot be used for) is real work, deferred to the WS-5 LLD and `SEC-06`'s
  flow-matrix, not invented here.

## Reversibility cost

Two-way door for which specific cameras land in which tier (that's data).
One-way-ish for the tiering concept itself once `VMS-17`'s always-record
eligibility rules are built against it — the concept should be locked before
that implementation, not after.

## Revisit trigger

The threat-model document (`CMP-15`, satisfying `SEC-17`) is drafted and
finds the low-trust tier's compensating control insufficient against
camera-spoofing or registry-poisoning specifically.

## What this does not cover

The exact eligibility-narrowing rule set — LLD (WS-5) and `SEC-06`'s
flow-matrix work.
