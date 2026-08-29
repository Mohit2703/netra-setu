# Open questions

Append as you go. Resolve in place with the answer and the date.
Never delete an entry.

---

## OQ-001 — Requirements register predates its own cited source

**Status:** OPEN — accepted as a permanent limitation, 2026-08-29
**Raised:** 2026-08-29

`docs/requirements/REGISTER.md`, `CAPACITY.md`, `COMPLIANCE.md` and `SCOPE.md`
were committed 2026-08-28 17:04 (`3bae7fc`) — **~21 hours before**
`_context/inputs/ProblemStatementGPIC2026.pdf` entered the repo (`1c1ba22`,
2026-08-29 14:07). The PDF is 12 pages and covers only §1–4 (context, problem
restatement, scope, personas); it explicitly forward-references §8
(compliance), §9 (forensic/NFSU) and §14 (organiser questions) as sections it
does not yet contain. `3bae7fc`'s own commit message says the 101 requirements
were "extracted from private source" — not this PDF.

Everything the PDF's §1–4 *does* state checks out against the register: the
capability table (A–M), the four stated exclusions, the P1–P6 personas, and the
VISWAS/Netram/TRINETRA figures all match `SCOPE.md`/`REGISTER.md`. Everything
beyond that — individual acceptance criteria, named algorithms, and the NFR
numbers (`OQ-002`) — has no independently checkable source anywhere in this
repo.

**2026-08-29 — resolution:** spot-check rather than re-derive. Proceeding on
`REGISTER.md` as authoritative. This entry stays open as a standing, accepted
limitation rather than a blocker. If a fuller version of the private source
ever turns up, re-run this diff before trusting further design work on the
rows it would newly cover.

## OQ-002 — NFR target provenance

**Status:** RESOLVED 2026-08-29 — source: user confirmation
**Raised:** 2026-08-29

`NFR-01`–`NFR-06`'s specific numbers (99.9%/99.5% availability, p95<3s alert
latency, p95<5s plate query, <2s stream start, RPO 5 min/RTO 30 min) appear
nowhere in the baseline PDF and have no stated derivation in `CAPACITY.md`
beyond "ASSUMED." The one NFR number independently confirmed against the PDF
is `NFR-07`'s 30% feed-loss figure — the PDF's own text says "the system that
stays usable at 30% feed loss wins" almost verbatim. `NFR-08` carries no
number to check.

HLD's latency-budget arithmetic (kickoff prompt §8: "latency budget hops sum
to ≤ the stated target") will cite whichever of these numbers survive, and
`.claude/rules/architecture-docs.md` requires every one be labelled GIVEN or
ASSUMED. Asking whether NFR-01–06 come from the private source (→ GIVEN,
citable as-is) or were the prior session's placeholder estimates (→ ASSUMED,
needs a validation plan before HLD leans on them) before drafting that
section.

**2026-08-29 — resolution:** confirmed real, from the private source. `HLD.md`
cites `NFR-01`–`NFR-06` as GIVEN (traceable to `REGISTER.md`/`CAPACITY.md`)
without further hedging. The per-hop latency *breakdowns* HLD adds on top —
how a 3s or 2s budget splits across capture/inference/network/render — are
still ASSUMED; the target is sourced, the arithmetic decomposing it is new and
needs the `CAPACITY.md` §3 load test to confirm.

## OQ-003 — VISWAS/ITMS overlap: bridge, don't duplicate

**Status:** RESOLVED 2026-08-29 — source: user decision
**Raised:** 2026-08-29

Related to `SCOPE.md` §5 Q-08 (organiser-directed: "what relationship to the
existing statewide CCTV estate is expected"), but distinct — Q-08 asks the
organisers about expectations at the framing level, already effectively
answered by the PDF's own thesis ("federation... not a replacement"). This
entry is the internal follow-on: *given* federation, how does netra-setu's own
analytics stack relate to the ITMS analytics ITMS already runs on the ~17,500
VISWAS cameras (ANPR, red-light, stolen-vehicle, crowd, tamper)?

**Decision:** bridge-only. netra-setu never runs its own inference on VISWAS
video — it ingests ITMS's existing outputs as external events through a
connector. Our own edge analytics (`VMS-10`–`VMS-15`) run only on the ~62,500
delta cameras with no analytics today. Rejected alternative: capability-
negotiated connectors that could run our analytics on any camera, preferring
ITMS output when present — more flexible, more moving parts, and in tension
with "federation, not replacement" (test: "does this require the incumbent to
give something up?" — capability negotiation implicitly assumes ours might
replace theirs on their own cameras).

**Consequence:** narrows (does not replace) §6 decisions 4 (vendor connector
port — must accept pre-computed analytics events as a first-class input type)
and 5 (edge/central split — the edge agent normalises ITMS output for VISWAS
cameras rather than running models). Both still get written up as full ADRs
with the rejected option stated, per `architecture-docs.md`.

## OQ-004 — LLD file grouping: 6 files (WS-1..WS-6), not the kickoff prompt's 8

**Status:** RESOLVED 2026-08-29 — following the repo over the kickoff prompt
**Raised:** 2026-08-29

`_context/prompts/01-architecture-kickoff.md` §3 suggests roughly 8 LLD files,
but hedges: "propose the actual split before writing." `CLAUDE.md` says
`docs/architecture/lld/` is one file per *workstream*, and `SCOPE.md` §3
already defines workstream concretely: WS-1..WS-6, each with requirement IDs
assigned. Per "follow the repo, don't silently reconcile": LLDs will be one
file per WS-1..WS-6.

This requires fixing `SCOPE.md`'s own documented ownership gaps as part of
that work: `VMS-16`–`VMS-20` (storage/retention), `VMS-23` (integrations) and
`VMS-24` (alert routing) are currently unassigned to any workstream; `REG-20`
is double-claimed by WS-1 and WS-2; `REG-21` sits only under WS-1's wildcard
despite being operationally WS-2's concern. Deferred to the LLD-authoring
phase, not fixed yet.

## OQ-005 — Traceability table location

**Status:** ASSUMED 2026-08-29 — two-way door, easily revisited
**Raised:** 2026-08-29

Kickoff prompt §4 wants a requirement→component traceability table; neither
`CLAUDE.md` nor `architecture-docs.md` says where it lives. Defaulting to a new
`docs/architecture/TRACEABILITY.md` (columns: requirement ID → design doc
section → `SVC-###` → planned module path → planned test → shaping ADRs →
build class). Cheap to move into `HLD.md` or split per-LLD later if that
proves wrong — flag if you'd rather decide now.

## OQ-006 — No requirement ID for "prototype uses only synthetic/consented data"

**Status:** OPEN — proposed, not created
**Raised:** 2026-08-29

The baseline's exclusion "prototype runs on synthetic and consented data only
— no real FIR data, no real watchlists, no scraped faces" doesn't map to any
`REG-`/`VMS-`/`SEC-`/`CMP-` ID. Same shape as the `CMP-05` gap `COMPLIANCE.md`
already flags (an obligation with no satisfying requirement). Not inventing an
ID per `.claude/rules/requirements.md` ("never invent an ID... add it to
OPEN-QUESTIONS.md and ask before creating one"). Candidate next ID if the user
wants one: `CMP-17` (a policy-type compliance control) or a new `SEC-` row (an
architectural constraint on data sources) — needs the user's call on which,
then it gets created there, not here.

## OQ-007 — UVH-26 / BMD-45 dataset licences unconfirmed

**Status:** OPEN — standing item, non-blocking
**Raised:** 2026-08-29

`SCOPE.md` §6 already flags both candidate ANPR datasets as licence-unconfirmed
("Not stated in the source baseline. Must be confirmed before any use.").
Doesn't block HLD/ADR work (no architecture decision here depends on which
dataset gets used); revisit before `VMS-10`/`VMS-11` implementation planning or
`CMP-16` model-card work starts.

## OQ-008 — "Sentinel Gujarat" portal

**Status:** RESOLVED 2026-08-29 — source: user decision
**Raised:** 2026-08-29

PDF §1.1 names "Sentinel Gujarat / official Gujarat Police portal" as "the
portal" in a table describing the challenge's own stage structure (prize pool,
start date, technology/knowledge partners, portal) — not in any capability,
requirement or persona section. **Decision:** the challenge's submission site,
unrelated to netra-setu's own architecture. Not modelled as an external system
in the HLD L1 context diagram.

## OQ-009 — VISWAS-vs-delta partition and VMS-14's tier partition are unreconciled

**Status:** OPEN — surfaced while drafting HLD.md
**Raised:** 2026-08-29

`CAPACITY.md` §2.1/§2.4 partitions the 80,000-camera fleet by **inference
tier** (8,000 full-rate ANPR-capable / 30,000 sampled / 42,000 event-triggered)
and sizes the ~838-GPU budget assuming *netra-setu's own* analytics run that
whole tiering. `OQ-003` partitions the same fleet by **ownership/bridging**
(~17,500 already-instrumented VISWAS cameras bridged from ITMS, no inference
of ours / ~62,500 delta cameras, ours to run). These are two different axes
over the same 80,000 cameras and nothing in this repo states how they overlap
— e.g., whether the 8,000 full-rate ANPR tier is mostly-VISWAS,
mostly-delta, or a mix.

If a material share of the full-rate/sampled tiers are VISWAS cameras (whose
analytics are bridged per `OQ-003`, not run by us), the real GPU budget for
*our* analytics is smaller than 838 — `CAPACITY.md` §2.4 would be
double-budgeting compute for cameras we don't run inference on. Likely related
to `SCOPE.md` Q-01/Q-04 (feed protocols, existing inventory). Needs either an
organiser answer (how many VISWAS cameras fall in each `VMS-14` tier) or an
explicit ASSUMED split with a validation plan, before `CAPACITY.md`'s GPU
arithmetic is revised in the LLD/capacity-extension phase. Not resolved here —
flagged in `HLD.md` at the point it would otherwise silently contradict
`CAPACITY.md`.

## OQ-010 — No field distinguishes a synthetic camera from a real one

**Status:** OPEN — proposed, not created
**Raised:** 2026-08-29

ADR 0009 (simulated-fleet architecture) registers synthetic cameras through
the real `REG-08` onboarding API with real `REG-01` URNs, deliberately
indistinguishable from real cameras to every downstream consumer — that's the
point (it's what actually exercises the production code path at scale). But
nothing today stops a synthetic load-test fleet from silently appearing in a
real gap-analysis report shown to P1, or in P6's oversight dashboard. Needs an
explicit `synthetic` field on `Camera`, distinct from `REG-04`'s provenance
values (which describe metadata *accuracy*, not whether the camera is real).
Not inventing a requirement ID or schema field per
`.claude/rules/requirements.md` — candidate: an amendment to `REG-03`'s
data-model requirement, or a new `REG-` row. Needs the user's call before
it's created.
