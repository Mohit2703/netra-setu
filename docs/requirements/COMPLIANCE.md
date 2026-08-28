# Compliance control matrix

One row per control, `CMP-01`–`CMP-16`. Requirement statements are in
[REGISTER.md](REGISTER.md).

**Read this first.** The obligations below are restatements of published
instruments made by engineers, not lawyers. None has been reviewed by qualified
counsel, and the regulatory dates cited have moved more than once. Treat every
row as unverified until someone qualified has checked it. Nothing here should be
presented as a legal conclusion.

**Control type**

| Type | Meaning |
|---|---|
| Architectural | Enforced by a code path or an infrastructure constraint. Testable. |
| Policy | Delivered as a written artefact or an organisational process. |
| Both | Has an enforced half and a documented half; both are required. |

---

## Statutory and regulatory controls

| ID | Obligation | Source instrument | Satisfying requirements | Type |
|---|---|---|---|---|
| CMP-01 | Purpose limitation, retention discipline, security safeguards, data-subject rights handling and breach response for personal data. | DPDP Act 2023 and DPDP Rules 2025. Rules notified 13 Nov 2025; Data Protection Board operational immediately; penalties and Consent Manager registration from 13 Nov 2026; full compliance by 13 May 2027. Dates unverified. | `SEC-07`, `SEC-08`, `SEC-11`, `VMS-19`, `VMS-20`, `SEC-03`–`SEC-06`, `SEC-10`, `CMP-12` | Both |
| CMP-02 | Cyber-incident reporting within 6 hours of detection; log retention of 180 days within India; system clock synchronisation to NIC/NPL sources. | CERT-In Directions, April 2022 | `FOR-06` (clock sync); log-retention configuration; incident-response runbook | Both |
| CMP-03 | Camera hardware must be certification-tracked; non-compliant devices identified and remediated. Essential Requirements notified 9 Apr 2024; BIS CRS implementation guidelines 22 Oct 2024; stock-clearance relaxation withdrawn, non-ER-compliant cameras not saleable from 1 Apr 2026. Dates unverified. | MeitY ER-01 / BIS CRS / STQC | `REG-22`, `REG-23` | Architectural |
| CMP-04 | Electronic records require an accompanying certification to be admissible. | Bharatiya Sakshya Adhiniyam 2023, s. 63 | `FOR-04`, `FOR-05` | Architectural |
| CMP-05 | Audio-video recording of search and seizure. | BNSS 2023, s. 105 | **None.** The platform provides hash-anchored admissible-package infrastructure via `FOR-01`–`FOR-05`, but no requirement ID is written against this obligation. | Architectural |
| CMP-06 | Directions on CCTV in police stations: coverage, audio, night vision, retention periods and oversight committees. | *Paramvir Singh Saini v. Baljit Singh* (2020) | Conditional. If police-station cameras are in registry scope: `REG-13`, `REG-14`, `VMS-18`, `VMS-19`, `SEC-14`. Scope decision not yet made. | Both |
| CMP-07 | Reasonable security practices; confidentiality obligations on persons with lawful access. | IT Act 2000, ss. 43A, 72, 72A | `SEC-*` for the technical half; a written personnel access policy for the other half | Both |
| CMP-08 | No raw video egress to public cloud or offshore infrastructure. Hosting on state data-centre infrastructure, transport over the state network. | Data-localisation position for state infrastructure (GSDC / MeghRaj hosting, GSWAN transport) | Architectural constraint, recorded explicitly in `CMP-15` | Architectural |
| CMP-09 | Accessibility and usability standards for a government-facing portal. | GIGW 3.0 | Frontend conformance pass against GIGW 3.0 | Architectural |
| CMP-10 | Alignment of information-security and privacy management controls. | ISO/IEC 27001 and ISO/IEC 27701 | Control mapping table. **Design artefact, not a certification** — must never be described as certified. | Policy |
| CMP-11 | Protected-system considerations for critical information infrastructure; the design should not preclude designation. | NCIIPC | None identified. Recorded as a design constraint only. | Policy |

## Artefacts

| ID | Obligation | Source instrument | Satisfying requirements | Type |
|---|---|---|---|---|
| CMP-12 | Data Protection Impact Assessment per capability: intrusion rating, necessity justification, mitigations. Face matching covered explicitly, with its scope limitation recorded as the mitigation. | Referenced by `CMP-01` | Assesses `VMS-13`, `VMS-22`, `SEC-08`, `SEC-10`, `REG-19` among others | Policy |
| CMP-13 | Retention schedule by data class — raw video, event metadata, thumbnails, embeddings, audit logs, evidence packages — each with its basis and its deletion mechanism. | Referenced by `CMP-01` | Implemented by `VMS-18`, `VMS-19`, `VMS-20`, `SEC-10` | Both |
| CMP-14 | Standard operating procedure for authorisation, break-glass and oversight review. | Operational requirement | Documents the operation of `SEC-08`, `SEC-09`, `SEC-14` | Policy |
| CMP-15 | Security architecture document: threat model, segmentation, key management, disaster recovery. | Named challenge deliverable | Contains `SEC-17` (threat model), `SEC-06` (segmentation), `SEC-05` (key management), `NFR-06` (DR) | Policy |
| CMP-16 | Model card per analytics model: training-data provenance, known failure modes, measured accuracy, measured differential performance across conditions, recommended confidence thresholds, prohibited uses. | Research-practice requirement | Applies to the models behind `VMS-10`, `VMS-11`, `VMS-12`, `VMS-13`. Complements `VMS-15` provenance and `FOR-07` reproducibility. | Policy |

---

## Traceability gaps

| Gap | Detail |
|---|---|
| `CMP-05` has no satisfying requirement ID | The obligation is asserted to be met by the evidence-package capability, but no `FOR-` or `VMS-` requirement is written against it. Either add one or record that the obligation is out of platform scope. |
| `CMP-06` is conditional | Applicability depends on whether police-station cameras fall in registry scope. Until that is decided the row cannot be tested. |
| `CMP-11` is untestable as written | "Should not preclude designation" is not a verifiable property. Needs restating as concrete design constraints, or demoting to a note. |
| Log-retention and incident-response under `CMP-02` have no requirement IDs | Only the clock-synchronisation half maps to a requirement (`FOR-06`). The 180-day in-India retention and the 6-hour reporting path do not. |
| `CMP-07` personnel access policy has no requirement ID | The technical half maps to `SEC-*`; the policy half is unowned. |

---

## What this file does not cover

- Whether any of these instruments applies to this platform, to its operator, or
  to the data it holds. That is a legal determination and it is not made here.
- Exemptions, carve-outs and their scope.
- Certification, audit or attestation against any of the named standards.
- Currency of the cited dates. Verify before relying on any of them.
