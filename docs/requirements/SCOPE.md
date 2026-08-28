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
| WS-1 Registry & GIS | Data model, onboarding, validation and deduplication, PostGIS viewsheds, gap and cut-set analysis, reports | `REG-*` |
| WS-2 Ingestion & Streaming | Connector SDK, edge agent, store-and-forward, WebRTC delivery, health monitoring | `VMS-01`–`VMS-09`, `REG-20` |
| WS-3 Analytics | ANPR, vehicle attributes, specified-event detection, adaptive tiering, model cards | `VMS-10`–`VMS-15`, `CMP-16` |
| WS-4 Bridge & Tracking | Road-graph binding, geometry-constrained candidate generation, route reconstruction, reverse gap feedback | `BRG-*`, `VMS-21`, `VMS-22` |
| WS-5 Security, Forensics & Compliance | Authorisation gate, audit, oversight dashboard, hashing, Merkle anchoring, evidence packaging, compliance artefacts | `SEC-*`, `FOR-*`, `CMP-*` |
| WS-6 Scale, Ops & Narrative | Simulated fleet, load tests, capacity model, disaster-recovery design | `NFR-*`, [CAPACITY.md](CAPACITY.md) §2–§3, §1 of this file |

### Coverage gaps in the workstream allocation

| Unassigned | Requirements |
|---|---|
| Storage and retention | `VMS-16`, `VMS-17`, `VMS-18`, `VMS-19`, `VMS-20` — no workstream claims these |
| External system integration | `VMS-23` — no workstream claims it |
| Alert routing and disposition | `VMS-24` — no workstream claims it |

`REG-20` is claimed twice: by WS-1 through the `REG-*` wildcard and by WS-2
explicitly. `REG-21` is claimed only by the WS-1 wildcard although it is
operationally adjacent to WS-2. Both need resolving before ownership means
anything.

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

## What this file does not cover

- Per-requirement build class. That is in the Notes column of
  [REGISTER.md](REGISTER.md).
- Capacity arithmetic and the load-test method. Those are in
  [CAPACITY.md](CAPACITY.md).
- Capabilities excluded from the product by decision rather than by build class.
  The operative constraints are carried as requirements (`VMS-12` named events
  only, `VMS-13` and `SEC-10` watchlist gating); the exclusion rationale is not
  recorded here.
- Schedule, staffing and ownership.
