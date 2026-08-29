# Requirements register

The authoritative list of requirement IDs for netra-setu. Every design
document, ADR, commit, ticket and test cites IDs from this file.

Related files:

- [CAPACITY.md](CAPACITY.md) — NFR target values and the 80,000-camera capacity model
- [COMPLIANCE.md](COMPLIANCE.md) — control matrix behind the `CMP-` requirements
- [SCOPE.md](SCOPE.md) — build classes, workstreams, technical risks, open questions
- [CHANGELOG.md](CHANGELOG.md) — ID lifecycle rules and the change log

## Conventions

**Prefixes**

| Prefix | Domain |
|---|---|
| `REG-` | Registry and GIS (Model 1) |
| `VMS-` | Federated video management and analytics (Model 4) |
| `BRG-` | Bridge between Model 1 and Model 4 |
| `NFR-` | Non-functional |
| `FOR-` | Forensics and evidentiary integrity |
| `SEC-` | Security |
| `CMP-` | Compliance |

**Priority** is MoSCoW: Must / Should / Could / Won't. Where the source
baseline stated no priority the cell reads `—` and the Notes column says so.

**Build class** appears in Notes:

| Class | Meaning |
|---|---|
| `LIVE` | Working code, demonstrated on real data |
| `SIM` | Working code, demonstrated on a synthetic or simulated fleet |
| `MODEL` | Analytical or design artefact only |

**Acceptance criteria** are populated only where the baseline states a
measurable threshold, a named deliverable artefact or an enumerated output.
`—` means the baseline gives no criterion and one still has to be written.

**Verification flag.** Notes marked *Requires external verification* carry a
verification flag from the source baseline. Do not treat them as settled.

IDs are permanent. See [CHANGELOG.md](CHANGELOG.md) before adding, changing or
retiring anything here.

---

## REG — Registry and GIS

### Identity and data model

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| REG-01 | Every camera record carries a globally unique, stable URN of the form `gj:cam:<district>:<dept>:<seq>`. Feed sessions, analytics events, evidence exports and audit records reference a camera only by this URN. | Must | No two camera records share a URN. Every camera reference in a feed session, analytics event, evidence export or audit record resolves to a registry URN. | Build: LIVE. Foundational — most other REG and all FOR/SEC traceability depends on it. |
| REG-02 | A camera's URN is unchanged by re-tendering, IP reassignment, firmware replacement or vendor change. Replacing hardware at the same position with the same coverage creates a new versioned `HardwareRecord` under the existing URN. Relocating a camera issues a new URN carrying a lineage link to the previous URN. | Must | Hardware swap at the same pole leaves the URN unchanged and adds a HardwareRecord version. Relocation produces a new URN whose lineage link resolves to the prior URN. | Build: LIVE. |
| REG-03 | The data model defines the entities `Owner`, `Site`, `Camera`, `HardwareRecord`, `Feed`, `Viewshed`, `HealthCheck`, `ComplianceRecord`, `AuditEvent`. | Must | All nine entities exist with defined relationships and cardinalities. | Build: LIVE. |
| REG-04 | Every metadata field records a provenance value from the set `declared` / `probed` / `field-verified`, and a confidence score. | Must | No metadata field is persisted without both a provenance value and a confidence score. | Build: LIVE. Rationale: source inventories contain coordinates set to the police station rather than the pole, placeholder names, missing bearings and duplicate records from overlapping tenders. Presenting that as authoritative would corrupt planning decisions. |
| REG-05 | The data model is published as a documented alignment with, or extension of, IUDX schema conventions. | Should | A field-level mapping between the netra-setu model and IUDX conventions is published, and every divergence is listed with a reason. | Build: LIVE. Baseline wording ("aligned to or extended from") is not directly testable; restated as the published mapping. Purpose is portability beyond Gujarat and avoidance of vendor lock-in. |

### Onboarding

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| REG-06 | Bulk import accepts CSV and XLSX, provides a schema-mapping UI, validates row by row, offers a dry-run preview before commit, and on commit writes valid rows while returning a row-level error report for rejected rows. | Must | A file containing both valid and invalid rows commits the valid rows only and returns an error report identifying each rejected row and its reason. Dry run writes nothing. | Build: LIVE. |
| REG-07 | Single-camera manual entry with map-based coordinate selection and the same validation rules as bulk import. | Must | — | Build: LIVE. |
| REG-08 | Authenticated REST API for programmatic camera onboarding, with a published OpenAPI specification. | Must | OpenAPI specification is published as a deliverable and matches the implemented endpoints. | Build: LIVE. The published spec is itself a challenge deliverable. |
| REG-09 | ONVIF discovery probes a specified subnet and populates make, model, firmware version, device capabilities and stream profiles for responding devices. | Should | — | Build: LIVE. |
| REG-10 | The system flags cameras whose stated coordinates are implausible relative to their stated ward, site or owning department's jurisdiction. | Must | — | Build: LIVE. No acceptance threshold stated; a plausibility rule and its tolerance still need defining. |
| REG-11 | Candidate duplicate records are detected by spatial clustering (DBSCAN over coordinates) combined with fuzzy matching on name and asset tag, and are placed in a merge queue for human adjudication. Records are never merged automatically. | Must | No merge occurs without a recorded human decision. | Build: LIVE. |
| REG-12 | A mobile field-verification flow captures a GPS fix, compass azimuth, mounting-height estimate and a reference frame at the camera position, upgrades the record's provenance from `declared` to `field-verified`, and retains the capture bundle. | Should | After a completed field verification the record's provenance is `field-verified` and the capture bundle is retrievable against that record. | Build: LIVE. Implementable as a responsive web form over the device geolocation and orientation APIs. |

### GIS and coverage

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| REG-13 | Interactive map with layers filterable by department, camera type, operational status, ANPR capability and compliance status. | Must | All five filter dimensions are available and compose. | Build: LIVE. |
| REG-14 | Each camera's coverage is stored as a wedge geometry in a spatial data store, derived from position, mounting height, azimuth, horizontal field of view and effective range, with building footprints subtracted where footprint data is available. | Must | Every camera with the required inputs has a stored viewshed geometry. | Build: LIVE. Coverage is modelled as geometry, not as point markers. Spatial store choice is an ADR decision, not a requirement. Handling of cameras missing an input — azimuth, height or FOV — is not specified in the baseline. |
| REG-15 | The coverage surface is the geometric union of camera viewsheds, computable per district, per ward and per road segment, and renderable as a heatmap. | Must | — | Build: LIVE. |
| REG-16 | Gap analysis differences the coverage surface against the OSM road network and against incident density per grid cell, and outputs a ranked list of uncovered high-incidence locations. | Must | Output is a ranked list with the ranking input values shown per row. | Build: LIVE. Sample gap-analysis report is a challenge deliverable. |
| REG-17 | ANPR cut-set analysis models the road network as a graph with ANPR-capable cameras as instrumented edges, determines whether a route exists from a given origin across a district boundary without traversing an instrumented edge, and outputs a ranked list of road segments to instrument in order to close such routes. | Should | For a given district, the analysis returns either a set of uninstrumented exit routes or a proof that none exists, plus the ranked segment list. | Build: LIVE. Structurally couples the registry to tracking: interception coverage is a min-cut problem on the road graph, not an area-coverage problem. Output is procurement guidance. |
| REG-18 | Report ranking cameras by hardware age, end-of-life status and failure history. | Must | — | Build: LIVE. |
| REG-19 | Search, filter and export (CSV and GeoJSON) scoped to the requesting user's role. Every export writes an audit record. | Must | No export path exists that does not write an audit record. | Build: LIVE. |

### Health and hardware compliance posture

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| REG-20 | Continuous health monitoring per camera covering reachability, stream integrity, frame-rate deviation, focus/blur score, scene change (indicating the camera has moved) and tamper or obstruction. | Must | All six signals are collected and surfaced per camera. | Build: LIVE. Also claimed by WS-2; see [SCOPE.md](SCOPE.md). |
| REG-21 | Maintenance status workflow with an SLA clock per owning department and MTTR reporting. | Should | — | Build: LIVE. |
| REG-22 | Per camera the register records make, model, firmware version, BIS CRS registration status, MeitY ER-01 / STQC certification status, default-credential status, date of last credential rotation, and vendor end-of-support date. | Must | All nine fields are present per camera, each carrying REG-04 provenance and confidence. | Build: LIVE. Certification-status source data availability is an open question (see [SCOPE.md](SCOPE.md), Q-05). *Requires external verification* — certification deadlines have moved repeatedly. |
| REG-23 | Hardware risk report ranks the fleet by exposure — non-compliant, end-of-support, unpatched, default-credential — with rollups by district and department. | Must | Report produces a fleet ranking plus district and department rollups. | Build: LIVE. |

---

## VMS — Federated video management and analytics

### Ingestion and interoperability

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| VMS-01 | Camera connectors are plugins implementing a published interface. Adding a vendor or protocol requires no modification to core. | Must | A new connector is added and loaded without any change to core source. | Build: LIVE. |
| VMS-02 | ONVIF connectors for Profile S (streaming), Profile G (recording and replay), Profile T (H.264/H.265 plus analytics) and Profile M (analytics metadata). | Must | All four profiles have a working connector. | Build: LIVE. |
| VMS-03 | Connector for raw RTSP/RTP/RTCP, supporting the common authentication variants. | Must | — | Build: LIVE. |
| VMS-04 | Connectors for the Hikvision ISAPI, Axis VAPIX and Dahua vendor APIs. | Should | — | Build: SIM. |
| VMS-05 | Connector for GB/T 28181. Devices reachable only over GB/T 28181 are recorded as such in the hardware trust register (REG-22). | Could | — | Build: MODEL — interface defined, implementation deferred. |
| VMS-06 | Analog cameras are integrated at DVR/NVR level where the camera itself exposes no IP interface. | Should | — | Build: MODEL. |
| VMS-07 | Edge agents initiate all connections outbound over mTLS. No central component initiates a connection into a camera or edge network. The agent operates behind NAT/CGNAT with no static IP and no inbound port. | Must | With all inbound ports closed at the edge site, the agent connects and streams. | Build: LIVE. Driven by the fact that municipal sites typically sit behind NAT/CGNAT, which makes a central pull model unworkable. Restated as a security control in SEC-02. |
| VMS-08 | The edge buffers events and video locally while backhaul is unavailable and reconciles on reconnect with capture-time timestamps preserved. An outage within buffer capacity causes delay, not data loss. | Must | After a simulated backhaul outage of a stated duration, every buffered event appears centrally exactly once, with its original capture timestamp. | Build: LIVE. Buffer capacity in hours is not stated in the baseline and needs deriving. |
| VMS-09 | Live view is delivered to a browser over WebRTC, with HLS fallback where WebRTC is unavailable. | Must | Stream start time meets NFR-05. | Build: LIVE. |

### Analytics

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| VMS-10 | ANPR reads Indian plates, handling two-line plates, HSRP and legacy plates, decorative and non-standard fonts, the IND hologram, the full state-code range, night-time IR washout, and motorcycle plate geometry. Accuracy is measured and reported per condition. | Must | Measured accuracy is published broken down by plate condition, with failure cases shown. A single headline accuracy figure does not satisfy this. | Build: LIVE. Highest technical risk in the programme (R-01). Dataset availability is Q-07. |
| VMS-11 | Vehicle attribute extraction — class, colour, coarse make — is available as a re-identification aid where the plate read fails. The class taxonomy covers Indian road classes including auto-rickshaw, tempo traveller, LCV and MUV. | Should | Taxonomy is not a generic COCO class set and includes the named Indian classes. | Build: LIVE. |
| VMS-12 | Detection of the named events: unattended object, crowd density threshold breach, wrong-way movement, loitering in a defined zone, camera tamper. No scoring or inference of intent, suspicion or demeanour. | Should | Only the enumerated event types are emitted. No output expresses a suspicion or intent score. | Build: LIVE. The exclusion is a scope decision, not a capability limit; see [SCOPE.md](SCOPE.md). |
| VMS-13 | Face matching runs only against an authorised, time-boxed watchlist. Embeddings are irreversible, gallery size is hard-capped, and every entry carries a mandatory expiry. | Could | No match executes against an entry past its expiry or against a gallery exceeding the cap. | Build: LIVE (gated). Prototype gallery is consented team members only. Constraints enumerated in SEC-10. |
| VMS-14 | Analytics run in three tiers: continuous full-rate inference on border, highway and strategic cameras; reduced-frame-rate sampling on urban junction cameras; event-triggered inference elsewhere. Tier is per-camera configuration. | Must | Each camera has an assigned tier and the running inference rate matches it. | Build: LIVE + MODEL. Tier populations and the GPU budget they imply are in [CAPACITY.md](CAPACITY.md). |
| VMS-15 | Every analytics output persists model name, model version, model artefact hash, input frame reference and confidence. Outputs are presented in the UI as leads requiring human confirmation, not as conclusions. | Must | No analytics record exists without all five provenance fields. Every UI surface presenting an analytics output displays the human-confirmation qualifier. | Build: LIVE. Precondition for FOR-07 reproducibility and for contestability of any AI-derived claim in an evidence package. |

### Storage and retention

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| VMS-16 | Structured events are transported to the state tier. Raw video remains at the edge unless retrieval is explicitly triggered. | Must | No raw video path from edge to state tier exists other than the VMS-17 triggers. | Build: LIVE. Justified by the storage and bandwidth arithmetic in [CAPACITY.md](CAPACITY.md). |
| VMS-17 | Central video retrieval occurs only on one of: an alert, a case-linked investigation request, or membership of a configured always-record subset (inter-state entry-exit points, high-security sites). | Must | Every central video retrieval record names one of the three triggers. | Build: LIVE. |
| VMS-18 | Three storage tiers: hot NVMe at the edge holding 24–72 hours, warm erasure-coded object store holding approximately 30 days, cold archive holding evidence-flagged material only. | Must | Tier residency matches the stated windows; nothing not evidence-flagged reaches cold archive. | Build: LIVE + MODEL. Erasure-coding overhead assumption is in [CAPACITY.md](CAPACITY.md). |
| VMS-19 | The retention clock is a function of case status, not of camera. Footage not flagged to a case expires on schedule, and each expiry is logged. | Must | Two cameras with identical configuration but different case flags retain for different periods. Every expiry produces a log entry. | Build: LIVE. |
| VMS-20 | At end of retention, data is irreversibly deleted by an automated process that logs the deletion and retains a deletion certificate. | Must | Deletion is not reversible from platform-held state, and a retrievable deletion certificate exists per deletion event. | Build: LIVE. |

### Search, tracking and integration

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| VMS-21 | Plate search across the event store with time and geography filters. | Must | p95 under 5 s over a 90-day event window (NFR-04). | Build: LIVE. Test-corpus cardinality relative to the modelled fleet is an unresolved inconsistency; see [CAPACITY.md](CAPACITY.md). |
| VMS-22 | Cross-camera vehicle tracking produces a reconstructed route rendered on the map with a confidence value per hop. | Must | Every hop in a rendered route carries its own confidence value. | Build: LIVE. |
| VMS-23 | Adapter interfaces with defined contracts and mock implementations for VAHAN (registration lookup), SARTHI (licence), eGujCop / CCTNS / ICJS (case and FIR linkage), and AFIS/NAFIS. | Must | A published contract plus a running mock exists for each of the four. | Build: SIM. Availability of real or sandbox endpoints is Q-03. |
| VMS-24 | Alerts route to the Netram district node holding jurisdiction. Operators acknowledge, escalate or dismiss, and record a disposition (true positive / false positive) that feeds model evaluation. | Must | Every alert reaches exactly one jurisdictionally correct node. Disposition data is retrievable for model evaluation. | Build: LIVE. Mitigation for operator false-positive load (R-07). |

---

## BRG — Bridge between registry and VMS

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| BRG-01 | Every camera in the registry is bound to a road-network segment (OSM edge) with a direction of view. | Must | Every ANPR-capable camera has a segment binding and a direction. Unbound cameras are reported as unbound. | Build: LIVE. |
| BRG-02 | Given an ANPR hit at camera A at time *t*, the system derives from the registry road graph the set of cameras physically reachable within a travel-time window bounded by a configured plausible speed, and restricts re-identification to that candidate set. | Must | Re-identification queries touch only the derived candidate set. | Build: LIVE. |
| BRG-03 | Route reconstruction is a constrained graph search over the BRG-02 candidate set rather than a fleet-wide match. The UI reports candidate cameras considered against fleet size. | Must | The reported candidate count matches the set actually searched. | Build: LIVE. Two effects: query latency proportional to candidates rather than fleet size, and removal of physically implausible matches. |
| BRG-04 | A tracking discontinuity — a vehicle unmatched between two cameras for longer than a threshold — automatically files a gap-analysis finding against the intervening road segment, which appears in the REG-16 gap report. | Should | A synthetic discontinuity produces a finding attached to the correct road segment and visible in the gap report. | Build: LIVE. Closes the loop: registry geometry makes tracking tractable, tracking failures improve the registry. Threshold value not stated in the baseline. |
| BRG-05 | Viewshed geometry configures analytics: zone definitions, expected direction of travel (enabling wrong-way detection without manual setup), and expected plate size in pixels (raising an automatic quality warning where ANPR cannot work). | Should | Wrong-way detection zones and plate-size quality warnings are derived from viewshed geometry with no per-camera manual configuration. | Build: LIVE. Feeds per-camera threshold tuning (R-07). |

---

## NFR — Non-functional

Target values and their derivation are in [CAPACITY.md](CAPACITY.md).

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| NFR-01 | The registry portal is available to authorised users. | — | 99.9% availability. | Build: MODEL. Priority not stated in the source baseline. Measurement window and exclusions not defined. |
| NFR-02 | A live feed is viewable, excluding faults in the camera or the network beyond the platform boundary. | — | 99.5% availability per feed. | Build: MODEL. Priority not stated in the source baseline. |
| NFR-03 | Elapsed time from frame capture to the alert appearing to an operator. | — | p95 under 3 s. | Build: LIVE. Priority not stated in the source baseline. |
| NFR-04 | Elapsed time for a plate query across a 90-day event window. | — | p95 under 5 s. | Build: LIVE + SIM. Priority not stated in the source baseline. Realised by VMS-21. |
| NFR-05 | Elapsed time from live-view request to first frame rendered. | — | Under 2 s. | Build: LIVE. Priority not stated in the source baseline. Percentile not stated. |
| NFR-06 | The metadata tier is recoverable after loss of its primary site. | — | RPO 5 minutes, RTO 30 minutes. | Build: MODEL. Priority not stated in the source baseline. Disaster-recovery design is a challenge deliverable. |
| NFR-07 | The system remains operable with 30% of feeds unavailable. Each unavailable feed is attributed in the UI to camera fault, network fault or platform fault. No feed is rendered as an unexplained black tile. | Must | With 30% of feeds killed, all remaining functions remain usable and every unavailable feed displays an attributed cause. | Build: LIVE. No target value given in the source baseline — the third column of the source table held a priority for this row. Graceful degradation is treated as a requirement, not as polish. |
| NFR-08 | Ingestion and inference capacity scales out by adding nodes. A new Netram node joins by registration, with no reconfiguration of central components. | Must | Adding a node requires no change to central configuration. | Build: MODEL. No target value given in the source baseline — the third column of the source table held a priority for this row. |

---

## FOR — Forensics and evidentiary integrity

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| FOR-01 | Video segments are stored content-addressed, with SHA-256 computed at the edge at the point of capture. | Must | Every stored segment's identifier is the hash of its content, computed before the segment leaves the capturing node. | Build: LIVE. |
| FOR-02 | A Merkle tree is built per camera per day over segment hashes. The daily root is anchored to an append-only transparency log, to an RFC 3161 trusted timestamp, or to both. | Must | For any segment, an inclusion proof to an anchored daily root can be produced. | Build: LIVE. Choice between transparency log and RFC 3161 is not settled in the baseline. |
| FOR-03 | Any recording interruption — camera offline, network loss, storage fault — produces a signed record stating the cause. | Must | An induced interruption produces a signed gap record with a populated cause. | Build: LIVE. Makes continuity provable from the record set and makes selective deletion detectable. Whether gap records are anchored into the FOR-02 Merkle tree is not stated in the baseline and needs deciding. |
| FOR-04 | An evidence export is a signed package containing: video segments, hash manifest, Merkle inclusion proofs, the full chain-of-custody log, the camera registry snapshot at time of capture (position, field of view, firmware), and analytics provenance for every AI-derived claim in the package. | Must | All six components are present in an export and the package signature verifies. | Build: LIVE. Depends on REG-14, VMS-15, FOR-01, FOR-02, FOR-08. |
| FOR-05 | Each evidence export is accompanied by an auto-generated certificate structured to support admissibility of electronic records under Bharatiya Sakshya Adhiniyam 2023, s. 63. | Must | A certificate is generated for every export without manual authoring. | Build: LIVE. *Requires external verification* — certificate format and sufficiency have not been checked by anyone qualified. Do not assert admissibility until that has happened. |
| FOR-06 | All nodes are NTP-synchronised to NIC or NPL sources. Clock drift is recorded, and drift events are flagged on any export covering the affected interval. | Must | Drift beyond a configured threshold appears as a flag on affected exports. | Build: LIVE. Also satisfies part of CMP-02. Threshold value not stated in the baseline. |
| FOR-07 | Given an evidence export, a reviewer can re-run the recorded model version against the recorded input frame and obtain the recorded output. | Should | An independent reviewer reproduces the recorded output byte-for-byte or within a stated tolerance. | Build: LIVE. Requires model artefacts to be retained and addressable by the hash recorded in VMS-15. |
| FOR-08 | Chain-of-custody log entries are append-only and verifiable by a party that does not trust the platform operator. | Must | Verification succeeds using only the export and public anchors, with no platform-held secret. | Build: LIVE. |

---

## SEC — Security

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| SEC-01 | Camera network segments are treated as untrusted. No implicit trust is extended from a camera network into any other tier, and all input originating from a camera network is authenticated and validated before use. | Must | No component accepts unauthenticated input from a camera network segment. | Build: LIVE. The source states this as a principle; restated here as a testable constraint. Rationale: camera VLANs are among the most frequently compromised segments of municipal networks. |
| SEC-02 | Edge connectivity is outbound-only. The centre never dials into a camera network. | Must | No inbound connection from a central component to an edge or camera network exists in any allowed flow. | Build: LIVE. Restates VMS-07 as a security control; the same behaviour therefore carries two IDs by design. |
| SEC-03 | Every internal service-to-service hop uses mTLS. No internal endpoint accepts unauthenticated requests. | Must | A scan of internal endpoints finds none reachable without a client certificate. | Build: LIVE. |
| SEC-04 | Services authenticate as workloads using SPIFFE/SPIRE identities rather than shared secrets. | Should | No service-to-service authentication uses a long-lived shared secret. | Build: LIVE. |
| SEC-05 | Per-camera credentials are held in a secrets manager, rotated automatically, with rotation age reported into the REG-22 register. | Must | No camera credential exists outside the secrets manager. Rotation age is queryable per camera. | Build: LIVE. Secrets-manager product choice is an ADR decision, not a requirement. |
| SEC-06 | Network segmentation separates camera VLANs, edge tier, analytics tier and state tier, with allowed flows explicitly enumerated. | Must | A published flow matrix enumerates every permitted flow; anything absent is denied. | Build: MODEL. |
| SEC-07 | An authorisation decision is a function of rank, jurisdiction, declared purpose and time-box together. Rank alone is insufficient; jurisdiction alone is insufficient. | Must | A request satisfying only rank, or only jurisdiction, is denied. | Build: LIVE. RBAC combined with ABAC. |
| SEC-08 | Every high-intrusion operation — face search, retrospective cross-camera tracking, watchlist enrolment, bulk export — requires a case reference (FIR / CCTNS number or written authorisation ID), a purpose selected from a controlled vocabulary, an explicit time-box, and an approver at or above a configured minimum rank. A request missing any of these is refused, and the refusal is logged. | Must | A high-intrusion request with no case reference is refused, the refusal is written to the audit log, and it appears on the SEC-14 dashboard. Free-text purposes are rejected. | Build: LIVE. Central control for the insider-misuse threat named in SEC-17. |
| SEC-09 | Break-glass access requires two authorisers, expires after a configured interval, and creates a mandatory post-hoc review task assigned to a named reviewer. | Must | Single-authoriser break-glass is impossible. Every break-glass grant produces an open review task. | Build: LIVE. |
| SEC-10 | Watchlist entries hold encrypted irreversible embeddings, are subject to a configurable hard cap on gallery size, and carry a mandatory per-entry expiry. No enrolment path exists from a general-population source. | Must | Enrolment beyond the cap fails. Entries past expiry are not matchable. No bulk-enrolment interface exists. | Build: LIVE. |
| SEC-11 | An append-only audit log records who searched for whom, when, and under what authority, and is independently verifiable. | Must | Log entries cannot be altered or deleted through any platform interface, and verification succeeds under FOR-08. | Build: LIVE. Verifiability mechanism is FOR-08; the same property therefore carries two IDs. |
| SEC-12 | Per-user and per-role query rate limits are enforced. Anomaly detection flags volume spikes, off-jurisdiction targets, and repeated searches against the same subject without case progression. | Should | Exceeding a rate limit blocks the query and logs it. Each of the three named anomaly patterns raises a flag. | Build: LIVE. |
| SEC-13 | Honeytoken records exist in the registry and in watchlists. Access to one raises an alert. | Could | Accessing a honeytoken record raises an alert. | Build: LIVE. |
| SEC-14 | A read-only oversight dashboard reports search volumes by type and district, face-search counts, denial counts with reasons, and flagged anomalies. | Should | All four report classes are present and the view has no write capability. | Build: LIVE. Serves the oversight-reviewer role, which has no operational access. |
| SEC-15 | Each owning department can see which of its cameras were accessed, by whom, and under which authorisation. | Should | A department user sees access records for its own cameras and for no others. | Build: LIVE. Precondition for federation: owners retain visibility without owning the platform. |
| SEC-16 | A CycloneDX SBOM is produced for all components, container images are cryptographically signed, and base images are pinned by digest. | Should | SBOM exists for every shipped component; every image signature verifies; no image reference is by mutable tag. | Build: LIVE. Signing-tool choice is an ADR decision, not a requirement. |
| SEC-17 | A documented threat model covers at minimum: RTSP injection and stream replay, camera spoofing, credential stuffing on the portal, insider misuse, ingestion-path DDoS, adversarial evasion (obscured or modified plates, masks), and registry poisoning — the injection of false camera records to manufacture blind spots in gap analysis. | Must | All seven threat classes are covered with an entry stating attack, impact and mitigating requirement IDs. | Build: MODEL. Delivered as part of CMP-15. Insider misuse is treated as the largest modelled risk; SEC-08, SEC-11, SEC-12 and SEC-14 exist primarily for it. |

---

## CMP — Compliance

Obligation sources, control types and cross-references are in
[COMPLIANCE.md](COMPLIANCE.md). None of these rows carried a MoSCoW priority in
the source baseline.

| ID | Requirement | Priority | Acceptance criteria | Notes |
|---|---|---|---|---|
| CMP-01 | Personal-data handling implements purpose limitation (SEC-07, SEC-08), retention and deletion discipline (VMS-19, VMS-20), security safeguards (SEC-03–SEC-06, SEC-10), audit (SEC-11) and a data protection impact assessment (CMP-12), under the DPDP Act 2023 and DPDP Rules 2025. | — | Each named control is implemented and traceable to this row. | *Requires external verification.* Applicability analysis for state instrumentalities is outside this repo. |
| CMP-02 | Cyber incidents are reportable within 6 hours of detection, logs are retained for 180 days within India, and system clocks are synchronised to NIC/NPL sources. | — | Log retention configuration is 180 days minimum with in-India storage. Clock sync satisfies FOR-06. An incident-response runbook defines the 6-hour path. | *Requires external verification.* Clock synchronisation delivered by FOR-06. |
| CMP-03 | Fleet hardware certification status is tracked per device and non-compliant devices are identified for remediation. | — | Satisfied by REG-22 and REG-23. | *Requires external verification* — certification deadlines have moved repeatedly. |
| CMP-04 | Electronic records exported as evidence are accompanied by the certification required for admissibility. | — | Satisfied by FOR-04 and FOR-05. | *Requires external verification.* |
| CMP-05 | The platform provides infrastructure for hash-anchored, admissible audio-video packages of the kind required for recorded search and seizure. | — | — | *Requires external verification.* No dedicated requirement ID satisfies this row; it rests on the FOR-01–FOR-05 package capability. Flagged as a traceability gap. |
| CMP-06 | Where police-station cameras fall within registry scope, their coverage, audio, night-vision, retention-period and oversight-committee attributes are modelled and reported. | — | — | *Requires external verification.* Conditional on a scope decision not yet made — whether police-station cameras are in registry scope. Untestable until that is settled. |
| CMP-07 | Reasonable security practices are implemented, and confidentiality obligations on persons with lawful access are defined in a personnel access policy. | — | Technical half satisfied by the SEC- set; policy half by a written personnel access policy. | *Requires external verification.* Part architectural, part policy. |
| CMP-08 | No raw video egresses to public cloud or offshore infrastructure. Hosting is on state data-centre infrastructure and transport is over the state network. | — | No data-flow path in the architecture sends raw video outside the stated boundary. | Architectural constraint; stated explicitly in the security architecture document (CMP-15). |
| CMP-09 | The government-facing portal conforms to GIGW 3.0 accessibility and usability standards. | — | A documented conformance pass against GIGW 3.0 with findings closed or listed. | Low cost, commonly omitted. |
| CMP-10 | A control mapping table aligns the platform's controls to ISO/IEC 27001 and ISO/IEC 27701. | — | Mapping table exists covering both standards. | Design artefact. Not a certification and must not be described as one. |
| CMP-11 | The design does not preclude designation of the platform as critical information infrastructure. | — | — | Untestable as written. Needs restating as a list of concrete design constraints, or downgrading to a note. Flagged. |
| CMP-12 | A data protection impact assessment is produced per capability, giving intrusion rating, necessity justification and mitigations, and covering face matching explicitly with its scope limitation recorded as the mitigation. | — | One assessed entry per capability, face matching included. | Artefact. Referenced by CMP-01. |
| CMP-13 | A retention schedule is published by data class — raw video, event metadata, thumbnails, embeddings, audit logs, evidence packages — each with its basis and its deletion mechanism. | — | All six data classes present, each with a basis and a named deletion mechanism. | Artefact. Implemented by VMS-19 and VMS-20. |
| CMP-14 | A standard operating procedure covers authorisation, break-glass and oversight review. | — | Procedure covers all three and is usable by an operating organisation without reference to the build team. | Artefact. Corresponds to SEC-08, SEC-09, SEC-14. |
| CMP-15 | A security architecture document covers threat model, segmentation, key management and disaster recovery. | — | All four sections present. Threat model satisfies SEC-17. | Artefact. Named challenge deliverable. |
| CMP-16 | A model card is published per analytics model covering training-data provenance, known failure modes, measured accuracy, measured differential performance across conditions, recommended confidence thresholds and prohibited uses. | — | All six sections present per model. A single headline accuracy figure does not satisfy this. | Artefact. Applies to every model behind VMS-10, VMS-11, VMS-12, VMS-13. |
