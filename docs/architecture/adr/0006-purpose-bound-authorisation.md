# 0006 — Purpose-bound authorisation

**Scope.** Where the authorisation policy decision point lives. Requirement
IDs: `SEC-07`, `SEC-08`, `SEC-09`, `SEC-11`, `SEC-12`, `SEC-14`, `SEC-17`.

## Context

`SEC-07` requires rank+jurisdiction+purpose+time-box jointly, never any one
alone. `SEC-08` requires every high-intrusion operation (face search,
retrospective tracking, watchlist enrolment, bulk export) to be refused and
logged if any of case-reference/purpose/time-box/approver-rank is missing.
`SEC-11` requires the audit log be independently verifiable. `SEC-17` names
insider misuse as the largest modelled threat, with `SEC-08`/`11`/`12`/`14`
existing primarily to mitigate it.

## Options considered

1. **Centralised PDP** — one Authorization/PDP service (SVC-013) that every
   gated resource server calls synchronously. Uniform, auditable from a
   single chokepoint; every gated operation hard-depends on SVC-013's
   availability, a deliberate, stated consequence rather than an accident.
2. **Distributed/embedded PDP** — each resource server embeds its own policy
   evaluation. No single point of failure, but N independent copies of
   enforcement logic directly undermine `SEC-11`'s independent-audit
   property and multiply the surface for a subtle under-enforcement bug —
   disqualified against `SEC-17`'s own stated insider-misuse threat model.
3. **Centralised decision with a short-TTL, fail-closed local cache** at each
   resource server, for resilience against brief central unavailability.
   Keeps option 1's single-logic-surface property while surviving transient
   GSWAN blips; genuine added complexity (cache invalidation, staleness
   bounds) that may be premature before SVC-013's own availability is
   measured.

## Decision

Option 1 for the Stage 1/Stage 2 build; option 3 is the documented upgrade
path if SVC-013 availability or GSWAN partition frequency proves to be a real
operational problem.

## Consequences

- SVC-013 is a hard dependency for every gated operation (face search,
  retrospective tracking, watchlist enrolment, bulk export, high-value video
  retrieval). At a partitioned Netram node, these operations fail closed —
  correct per `SEC-08`'s stakes, but worth stating as designed behaviour, not
  an outage.
- `SEC-12`'s rate-limiting/anomaly detection and `SEC-14`'s oversight
  dashboard both read from one chokepoint, simplifying both.
- Option 2 (distributed PDP) is not merely deprioritised but actively
  rejected — noted so it isn't quietly reconsidered at LLD time without
  revisiting this reasoning.

## Reversibility cost

Two-way door. SVC-013 already exists as a distinct container in `HLD.md` §3;
adding a resilience cache (option 3) later is additive, not a rearchitecture.

## Revisit trigger

Live-demo network testing under deliberate packet loss (kickoff's R-03
mitigation) shows gated operations failing closed often enough to be a
demo-killing UX problem.

## What this does not cover

The actual policy language/engine (e.g., a specific policy-as-code
framework) — a smaller, separate ADR at LLD time.
