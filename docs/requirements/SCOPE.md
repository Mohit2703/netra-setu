# Build scope, workstreams, risks and open questions

What is built as working code, what runs against a simulated fleet, and what
exists only as an analytical artefact. Requirement statements are in
[REGISTER.md](REGISTER.md).

**Build classes**

| Class | Meaning |
|---|---|
| `LIVE` | Working code, demonstrated on real data |
| `SIM` | Working code, demonstrated on a synthetic or simulated fleet |
| `MODEL` | Analytical or design artefact only |

Being explicit about the boundary is a requirement of the submission, not a
disclaimer attached to it. Nothing may be presented at a higher class than it
is listed here.

---

## 1. Build class per capability

| Capability | Class | Detail |
|---|---|---|
| Registry, PostGIS viewsheds, gap analysis, cut-set analysis | LIVE | Real, on a seeded fleet |
| Bulk / manual / API / ONVIF onboarding, validation, deduplication | LIVE | Real |
| Field verification flow | LIVE | Real, on a phone |
| Hardware compliance register and risk report | LIVE | Real schema; synthetic certification data pending Q-05 |
| Live ingestion and WebRTC view | LIVE | 20–50 real feeds — public streams plus own cameras |
| ANPR on Indian plates | LIVE | Real. Accuracy reported per condition with failure cases shown |
| Cross-camera tracking and route reconstruction | LIVE | 4–6 cameras, staged vehicle runs |
| Authorisation gate, audit, oversight dashboard | LIVE | Real, including a demonstrated refusal of an unauthorised request |
| Evidence package and chain of custody | LIVE | Real, verifiable by an independent tool |
| Face matching | LIVE, gated | Consented team-member gallery only; deliberately scope-limited |
| Fleet at scale | SIM | 500–2,000 synthetic cameras through the real connector stack |
| 80,000-camera scalability | MODEL | Measured node throughput plus the capacity model and load-test report — see [CAPACITY.md](CAPACITY.md) |
| Disaster recovery and redundancy design | MODEL | Design document with RPO/RTO (`NFR-06`) |
| VAHAN / SARTHI / CCTNS / AFIS integration | SIM | Adapter contracts plus mock services |
| GB/T 28181, analog DVR connectors | MODEL | Connector interface defined, implementation deferred |

Note: the source baseline lists `VMS-14`, `VMS-18` as `LIVE + MODEL` and
`NFR-04` as `LIVE + SIM` at requirement level, which the three-class table above
cannot express. Per-requirement build class is recorded in the Notes column of
[REGISTER.md](REGISTER.md) and is authoritative where the two differ.

---

## 2. Deliverable coverage

| Deliverable | Covered by |
|---|---|
| Working registry portal with GIS map view | `REG-01`–`REG-19` |
| Bulk and manual camera-onboarding demonstration | `REG-06`–`REG-08`, `REG-12` |
| Sample onboarded camera-metadata dataset | Seed dataset plus generator script |
| Registry API documentation | `REG-08` OpenAPI specification |
| Sample gap-analysis report | `REG-16`, `REG-17`, `REG-23` |
| Working centralised VMS prototype across multi-department feeds | `VMS-01`–`VMS-09`, multi-tenant owner model (`REG-03`) |
| ANPR and multi-location vehicle tracking demonstration | `VMS-10`, `VMS-22`, `BRG-01`–`BRG-04` |
| Scalability and load-test report for ~80,000 cameras | [CAPACITY.md](CAPACITY.md) §2, §3 |
| Disaster-recovery and redundancy design | `NFR-06`, `NFR-08` |
| Security architecture document | `CMP-15`, `SEC-17` |

The registry-portal row cites `REG-01`–`REG-19` and so omits `REG-20`–`REG-23`
(health monitoring and hardware compliance posture), which are registry portal
features. Treat the deliverable as covering `REG-01`–`REG-23`.

---

## 3. Workstreams

| WS | Scope | Requirement IDs |
|---|---|---|
| WS-1 Registry & GIS | Data model, onboarding, validation and deduplication, spatial viewsheds, gap and cut-set analysis, reports, hardware compliance & health aggregation | `REG-*` |
| WS-2 Ingestion & Streaming | Connector SDK, edge agent, store-and-forward, WebRTC delivery, tiered storage and retention | `VMS-01`–`VMS-09`, `VMS-16`–`VMS-20` |
| WS-3 Analytics | ANPR, vehicle attributes, specified-event detection, adaptive tiering, model cards, alert routing and disposition | `VMS-10`–`VMS-15`, `VMS-24`, `CMP-16` |
| WS-4 Bridge & Tracking | Road-graph binding, geometry-constrained candidate generation, route reconstruction, reverse gap feedback | `BRG-*`, `VMS-21`, `VMS-22` |
| WS-5 Security, Forensics & Compliance | Authorisation gate, audit, oversight dashboard, hashing, Merkle anchoring, evidence packaging, external system integration adapters, compliance artefacts | `SEC-*`, `FOR-*`, `CMP-01`–`CMP-15`, `VMS-23` |
| WS-6 Scale, Ops & Narrative | Simulated fleet, load tests, capacity model, disaster-recovery design | `NFR-*`, [CAPACITY.md](CAPACITY.md) §2–§3, §1 of this file |

### Workstream ownership — resolved 2026-08-29

Previously unassigned (`VMS-16`–`VMS-20`, `VMS-23`, `VMS-24`) and
double-claimed (`REG-20`, `REG-21`) requirements, resolved while drafting the
LLDs (`docs/architecture/lld/`), per
[`OPEN-QUESTIONS.md`](../architecture/OPEN-QUESTIONS.md) OQ-004:

- **Storage and retention** (`VMS-16`–`VMS-20`) → WS-2. The storage tiers
  (hot at the edge, warm/cold central) are the direct continuation of the
  ingestion pipeline WS-2 already owns, not a separate concern.
- **External system integration** (`VMS-23`: VAHAN/SARTHI/eGujCop-CCTNS-ICJS/
  AFIS-NAFIS) → WS-5. These adapters are used primarily to validate a case
  reference (`SEC-08`) and for forensic identification (AFIS/NAFIS) — closer
  to WS-5's authorisation/forensics concerns than to ingestion.
- **Alert routing and disposition** (`VMS-24`) → WS-3. Alerts are analytics
  output; disposition capture directly feeds model evaluation and per-camera
  threshold tuning (`R-07`'s mitigation), an analytics-quality concern.
- **`REG-20`** (health monitoring) → WS-1 owns the requirement — aggregation
  and presentation, `SVC-003` in `HLD.md`. WS-2's Edge Agent is the raw
  *signal source* it depends on, not a second owner. Resolves the
  double-claim: one requirement, one owner, one documented dependency.
- **`REG-21`** (maintenance workflow, SLA clock, MTTR) → stays WS-1. It
  consumes WS-1's own `REG-20` aggregation, not WS-2 directly —
  "operationally adjacent to WS-2" doesn't require reassignment.

All 101 requirement IDs now have exactly one owning workstream. No orphans,
no double-claims.

---

## 4. Technical risks

Scoped to risks to the system. Programme, team and presentation risks are
tracked elsewhere and are deliberately not in this repo.

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Indian-plate ANPR underperforms. Two-line plates, decorative fonts, HSRP variation and IR washout defeat generic models. | High | High | Start ANPR first, not last. Self-collect a validation set early. Report measured accuracy per condition with failure cases rather than a headline figure (`VMS-10`, `CMP-16`). |
| R-03 | Degraded or hostile network conditions in the deployment environment break ingestion and live view. | Medium | High | `NFR-07` graceful degradation and `VMS-08` store-and-forward. Test under deliberate packet loss and feed kills, not only on a clean network. |
| R-07 | False-positive load makes the operator experience unusable at fleet scale. | Medium | High | Disposition capture feeding model evaluation (`VMS-24`), per-camera threshold tuning driven by `BRG-05` quality warnings, alert deduplication. |
| R-09 | Model 1 and Model 4 are delivered as two systems that share a login rather than one integrated system. | Medium | High | The bridge is a named workstream (WS-4) with its own requirement set (`BRG-*`), not integration glue added at the end. |

Risks R-02, R-04, R-05, R-06, R-08 and R-10 in the source baseline concern
programme management, legal exposure or presentation. They are out of scope for
this repo.

---

## 5. Technical open questions

Answers here change scope materially. Directed at the challenge organisers.

| ID | Question | Affects |
|---|---|---|
| Q-01 | Will sample multi-department feeds be provided, and over what protocols — RTSP endpoints, recorded files, or live ONVIF devices? | `VMS-02`–`VMS-06`, the whole ingestion plan |
| Q-02 | For the live evaluation environment: what network, what feed count, and is GPU compute provided or brought? | [CAPACITY.md](CAPACITY.md) §3, `NFR-07` |
| Q-03 | Are sandbox or mock endpoints available for VAHAN, SARTHI, eGujCop/CCTNS and AFIS/NAFIS? | `VMS-23` — determines mock versus real |
| Q-04 | Is any existing camera inventory available, even partial or poor quality? Real inventory data with real defects is more useful than clean synthetic data. | `REG-04`, `REG-10`, `REG-11`, seed dataset |
| Q-05 | Is ER-01 / BIS CRS certification status per camera model available in any machine-readable form? | `REG-22`, `REG-23`, `CMP-03` |
| Q-07 | Is a real, even anonymised, Indian-plate ANPR dataset available, or is self-collection required? | `VMS-10` — the largest schedule risk in the ML work (R-01) |
| Q-08 | What relationship to the existing statewide CCTV estate is expected — federate over it, extend it, or replace it? | Core architectural framing; affects every `BRG-` and `VMS-` interface assumption |
| Q-10 | Are there constraints on demonstrating face matching, given the intended scope limitation? | `VMS-13`, `SEC-10` |

Q-06 and Q-09 from the source baseline concern evaluation weighting and entry
category. They are not technical and are not tracked here.

Architecture-level open questions raised during design work belong in
[../architecture/OPEN-QUESTIONS.md](../architecture/OPEN-QUESTIONS.md), not
here. This section holds only questions whose answers come from the organisers.

---

## 6. Dataset references

Candidate training and validation data for `VMS-10` and `VMS-11`. Both are drawn
from operational Indian city CCTV and use India-specific vehicle taxonomies.

| Dataset | Description | Licence | Reference |
|---|---|---|---|
| UVH-26 | Annotated Indian traffic-camera dataset; 26,646 images from approximately 2,800 Bengaluru Safe-City cameras; 14 India-specific vehicle classes | **Not stated in the source baseline. Must be confirmed before any use.** | https://arxiv.org/pdf/2511.02563 |
| BMD-45 | Large-scale CCTV vehicle-detection dataset for urban traffic in developing cities | **Not stated in the source baseline. Must be confirmed before any use.** | https://arxiv.org/pdf/2604.24419 |

Neither licence has been checked. The project is open-source only, so a dataset
whose terms are unclear or non-commercial-restricted cannot be used, and the
licence must be resolved before either is pulled into a training pipeline. Any
model trained on either dataset must record its provenance under `CMP-16`.

---

## 7. Roadmap — Stage 1 and Stage 2 milestones

Relative sequence, not calendar dates — [`OPEN-QUESTIONS.md`](../architecture/OPEN-QUESTIONS.md)
OQ-011 (real Stage 1/2 dates, team size/parallelism) is still open. Ordered
by dependency, not by workstream number: `M0`/`M1` (WS-1) must precede
`M2` (WS-2) per the "Model 1 first, ships cleanly, admits Model 4 without a
rewrite" constraint (`CLAUDE.md`; kickoff §2); everything from `M3` onward
can run in parallel across workstream owners if the team supports it
(OQ-011), or sequentially if it doesn't — the milestones themselves don't
change either way, only their calendar spacing.

| Milestone | Scope | Workstream | Satisfies (deliverable, `SCOPE.md` §2) |
|---|---|---|---|
| `M0` | Registry MVP: identity, bulk/manual/API onboarding, basic dedup | WS-1 | Sample onboarded camera-metadata dataset |
| `M1` | Registry complete: GIS/viewshed, gap + cut-set analysis, hardware compliance | WS-1 | Working registry portal with GIS map view; sample gap-analysis report; registry API docs |
| `M2` | VMS ingestion foundation: connector SDK, edge agent, 20–50 real feeds live, WebRTC view, simulated-fleet driver online | WS-2 | Working centralised VMS prototype across multi-department feeds |
| `M3` | Analytics online: ANPR + specified-event detection on real+simulated feeds, alert routing | WS-3 | ANPR demonstration |
| `M4` | Bridge & tracking: road-graph binding, candidate-set generation, staged multi-camera vehicle run | WS-4 | Multi-location vehicle-tracking demonstration |
| `M5` | Security/forensics: authorisation gate, audit, evidence export, chain of custody, demonstrated refusal | WS-5 | Security architecture document; a demonstrated unauthorised-request refusal |
| `M6` | Scale & DR: 500–2,000-camera load test, capacity/DR docs finalised | WS-6 | Scalability/load-test report; disaster-recovery design |
| `M7` | Live-demo hardening: graceful degradation under induced packet loss/feed kills, false-positive tuning, gated face-match demo, full P3-scenario and P1-gap-to-tender walkthroughs | All | Stage 2 readiness |

`M0`–`M1` is Stage 1's likely centre of gravity given "Model 1 first"; `M2`–`M6`
scale with however much of Stage 1's window remains. `M7` is squarely Stage
2 — it exists only to rehearse the two end-to-end scenarios `HLD.md` already
walks on paper (§5.4's P3 route-reconstruction flow; `REG-16`'s gap report
feeding a P1 tender decision) against a live, degrading network, per the
kickoff's own framing: "the finale is live, not slides."

---

## What this file does not cover

- Per-requirement build class. That is in the Notes column of
  [REGISTER.md](REGISTER.md).
- Capacity arithmetic and the load-test method. Those are in
  [CAPACITY.md](CAPACITY.md).
- Capabilities excluded from the product by decision rather than by build class.
  The operative constraints are carried as requirements (`VMS-12` named events
  only, `VMS-13` and `SEC-10` watchlist gating); the exclusion rationale is not
  recorded here.
- Calendar dates, staffing and per-workstream ownership for §7's roadmap —
  pending [`OPEN-QUESTIONS.md`](../architecture/OPEN-QUESTIONS.md) OQ-011.
