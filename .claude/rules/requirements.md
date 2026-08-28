---
paths:
  - "docs/requirements/**/*.md"
---

# Requirements register rules

This directory is the contract every design document is written against.
Treat edits here as breaking changes.

- IDs are permanent. Never renumber, never reuse a retired ID.
- To retire a requirement, mark it SUPERSEDED with a pointer to its
  replacement. Do not delete the row.
- Any change to a requirement's meaning needs a CHANGELOG.md entry in the same
  commit: date, ID, what changed, why.
- Before changing a requirement, grep `docs/architecture/` for the ID and report
  which documents cite it. Changing a cited requirement without saying so
  silently invalidates design work.
- Requirements state verifiable behaviour, not implementation. If you find
  yourself naming a technology, it belongs in an ADR instead.
- Everything here becomes public at submission. No internal commentary, no
  legal argument, no strategy.