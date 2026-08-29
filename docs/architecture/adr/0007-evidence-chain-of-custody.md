# 0007 — Evidence chain of custody

**Scope.** How segment hashes are anchored for tamper-evidence and legal
admissibility. Requirement IDs: `FOR-01`, `FOR-02`, `FOR-04`, `FOR-05`,
`FOR-08`, `CMP-04`.

## Context

`FOR-02` explicitly leaves the anchor mechanism open in its own text
("anchored to an append-only transparency log, to an RFC 3161 trusted
timestamp, or to both"). `FOR-08` requires verification "by a party that does
not trust the platform operator... using only the export and public anchors,
with no platform-held secret" — a strong bar, given the platform's own
operator is a state police force whose impartiality regarding its own
evidence is exactly what might be questioned. `FOR-05`/`CMP-04` require an
auto-generated certificate supporting admissibility under Bharatiya Sakshya
Adhiniyam 2023 s.63 — both already carry a `COMPLIANCE.md`-level "requires
external verification, not reviewed by anyone qualified" caveat that this
decision does not resolve or need to resolve.

## Options considered

1. **RFC 3161 trusted timestamp only.** Simple, standard, easy to verify
   with off-the-shelf tooling — boring technology in the purest sense. But
   the Time Stamping Authority is itself a single trusted third party; if
   compromised, unavailable, or (for a state-operated system) perceived as
   not independent of the operator, `FOR-08`'s "doesn't trust the operator"
   property partially collapses. No continuously public, third-party-
   mirrorable record.
2. **Append-only public transparency log only** (Certificate-Transparency-
   style, independently mirrorable, tamper-evident even under later
   log-operator compromise). The strongest available answer to `FOR-08`, but
   no widely-recognised precedent in an Indian court context comparable to a
   timestamp authority — a defence expert could plausibly (and validly,
   independent of cryptographic soundness) challenge it as unfamiliar.
3. **Both**, exactly as `FOR-02`'s text already allows. The transparency log
   delivers `FOR-08`'s operator-independence guarantee; the RFC 3161 token
   gives `FOR-05`'s certificate a familiar, court-recognisable artefact to
   cite. Genuinely more moving parts — two anchoring mechanisms, two
   verification procedures — and the transparency log itself is
   infrastructure netra-setu would have to operate (no ready-made
   India-hosted open-source transparency-log service is named anywhere in
   this repo; a separate, smaller open question, not this decision).

## Decision

Option 3. Anchor every daily per-camera Merkle root (`FOR-02`) to both an
append-only transparency log and an RFC 3161 timestamp.

## Consequences

- SVC-016 (Forensic Integrity Service) must operate or integrate two anchor
  mechanisms, not one — real added implementation and documentation cost,
  deliberately accepted given how directly `FOR-08` and `FOR-05` pull in
  different directions and how central forensic credibility is to this
  project's stated NFSU-facing opportunity (kickoff §1.1, §9).
- `FOR-04`'s evidence export package includes both anchor proofs; `FOR-05`'s
  certificate can reference the timestamp specifically, while the
  transparency-log proof supports independent verification regardless of
  certificate sufficiency.
- One of the few places in this document where the "prefer boring
  technology, single mechanism" default is deliberately not taken — flagged
  explicitly so it isn't mistaken for scope creep at LLD/review time.

## Reversibility cost

One-way-ish once evidence has been exported and handed to a court
referencing a specific anchoring scheme — past exports aren't invalidated by
a later change, but two eras of evidence would verify differently, a real
operational and legal-narrative cost.

## Revisit trigger

A qualified legal reviewer (per `COMPLIANCE.md`'s standing caveat, not yet
obtained) finds the transparency-log half adds no admissibility value a
court will recognise, or finds it actively confuses the certificate story.

## What this does not cover

Which specific transparency-log implementation/hosting to use — no candidate
is named anywhere in this repo; a separate, smaller decision once this ADR's
mechanism choice is accepted. Whether `FOR-05`'s certificate actually
satisfies BSA 2023 s.63 — an unresolved legal question this ADR does not and
cannot answer.
