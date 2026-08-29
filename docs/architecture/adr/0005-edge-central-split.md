# 0005 — Edge/central split

**Scope.** What runs on a Netram node vs. centrally at Gandhinagar, and what
crosses GSWAN. Requirement IDs: `VMS-14`, `VMS-16`–`VMS-18`, `NFR-03`,
`NFR-08`. Shaped by [`OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) OQ-003;
flagged against OQ-009.

## Context

The 34 Netram district Command & Control Centres are given as the edge
compute tier (kickoff §1.2 — already operational, already networked to
Gandhinagar). `VMS-16` requires raw video to remain at the edge unless
explicitly retrieved. `CAPACITY.md` §2.2 already computes and rejects a fully
centralised alternative (160 Gbps sustained ingress, 71 PB storage) in favour
of the federated design; §2.4 sizes a ~838-GPU budget assuming netra-setu's
own inference runs the full `VMS-14` tiering (full-rate/sampled/
event-triggered) at the edge. OQ-009 (open) notes this GPU figure may be
overstated once OQ-003's VISWAS-bridging is accounted for, since some
full-rate/sampled-tier cameras are likely already-instrumented VISWAS cameras
whose analytics are bridged, not run by us.

## Options considered

1. **All inference at the edge.** Matches `VMS-16` and the capacity model
   already on record; keeps GSWAN load at the metadata-only ~11 Gbps figure
   (`CAPACITY.md` §2.5) instead of 160 Gbps. Real consequence: GPU hardware
   (up to ~25/node pending OQ-009) must be procured and racked at 34 sites —
   a genuine logistics dependency outside this platform's software scope.
2. **Centralised inference.** The option `CAPACITY.md` §2.2 already rejects
   with derived numbers; reopening it without new information contradicts a
   standing derivation and violates `VMS-16` (Must).
3. **Split by tier — event-triggered cameras inferred centrally on-demand.**
   Would reduce the per-node GPU footprint, but adds a new GSWAN round-trip
   to the alert path for that tier, which plausibly breaks `NFR-03`'s
   p95<3s alert-latency target (see `HLD.md` §6's arithmetic) — an apparent
   hardware saving that doesn't survive the latency budget, and isn't
   requested by any requirement.

## Decision

Option 1. All analytics inference runs at the edge (Netram nodes); only
metadata, events, alerts and on-demand video (`VMS-17` triggers only) cross
GSWAN.

## Consequences

- Largely already implied by `VMS-16` and `CAPACITY.md`'s existing
  arithmetic — this ADR documents and formalises it rather than discovering
  it fresh.
- The GPU procurement burden is real and unresolved by software architecture;
  `SCOPE.md`'s existing exclusion ("physical camera procurement/installation
  advice is out of software scope") extends naturally to GPU hardware — the
  registry/capacity model reports the need, procurement acts on it.
- OQ-009 remains open and now has a concrete consumer: if the true
  post-bridging GPU count is still not procurable at 34 sites, this decision
  (not just the number) needs revisiting.

## Reversibility cost

One-way-ish. Once WS-2's edge-agent/connector LLD and code exist assuming
edge-resident inference, moving inference tiers between edge and central
means re-plumbing the event bus's trust boundary and the GSWAN bandwidth
budget.

## Revisit trigger

OQ-009 resolves in a way that shows the true edge GPU count (after
subtracting bridged-VISWAS cameras) still isn't procurable at 34 sites even
after the subtraction.

## What this does not cover

The actual resolution of OQ-009's VISWAS/tier overlap — needs an organiser
or user answer before `CAPACITY.md`'s GPU arithmetic is revised.
