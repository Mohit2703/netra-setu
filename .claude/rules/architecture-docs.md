---
paths:
  - "docs/architecture/**/*.md"
---

# Architecture document rules

## Structure
- Open every document with purpose, scope, and the requirement IDs it covers.
- Mermaid for all diagrams, inline. No binary diagram files.
- Label C4 levels explicitly: Context, Container, Component.
- Use tables for anything enumerable: components, failure modes, NFR budgets.

## Rigour
- Label every line GIVEN (traceable to the requirements register) or ASSUMED.
- Every ASSUMED needs a validation plan, or it moves to OPEN-QUESTIONS.md.
- Numbers carry their derivation. An unsourced figure is a defect.
- No component without a requirement ID justifying it.

## Decisions
- ADR filename: `adr/NNNN-kebab-case-slug.md`, NNNN zero-padded.
- ADR sections: Context / Options considered / Decision / Consequences /
  Reversibility cost / Revisit trigger.
- Minimum three options, including one rejected and the reason.
- Mark each decision a one-way or two-way door.

## Honesty
- End every document with "What this does not cover".
- Append to OPEN-QUESTIONS.md as you go. Resolve entries in place with the
  answer and the date. Never delete one.