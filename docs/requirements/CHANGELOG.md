# Requirements changelog

Every change to the meaning of a requirement is recorded here. Newest entry
first.

## Rules

- **IDs are permanent.** Never renumber a requirement and never reuse a retired
  ID for anything else.
- **To retire a requirement, mark it `SUPERSEDED` in the Notes column of
  [REGISTER.md](REGISTER.md)** with a pointer to the replacement ID. Do not
  delete the row. The row stays in place so that older documents, commits and
  tickets citing the ID still resolve.
- **Every change to a requirement's meaning gets an entry here**: date, ID, what
  changed, why. Fixing a typo does not. Changing what would make the requirement
  pass or fail does.
- **Adding a requirement means appending the next ID in its prefix.** Never
  insert into a sequence and never fill a gap left by a retirement.

---

## 2026-08-28 — Initial extraction

Requirements register established in this repo. 101 requirement IDs extracted
from the project's problem-statement baseline into
[REGISTER.md](REGISTER.md), [CAPACITY.md](CAPACITY.md),
[COMPLIANCE.md](COMPLIANCE.md) and [SCOPE.md](SCOPE.md).

| Prefix | IDs | Count |
|---|---|---|
| `REG-` | REG-01 – REG-23 | 23 |
| `VMS-` | VMS-01 – VMS-24 | 24 |
| `BRG-` | BRG-01 – BRG-05 | 5 |
| `NFR-` | NFR-01 – NFR-08 | 8 |
| `FOR-` | FOR-01 – FOR-08 | 8 |
| `SEC-` | SEC-01 – SEC-17 | 17 |
| `CMP-` | CMP-01 – CMP-16 | 16 |
| **Total** | | **101** |

All seven sequences are contiguous with no duplicates and no gaps.

No requirement meaning was changed by the extraction. Statements were rewritten
into plain, testable language; every rewrite preserves the original meaning.
Where a source statement was not testable as written, the ID and intent were
kept and the testable restatement is noted in that row's Notes column.

Acceptance criteria were populated only where the source baseline stated a
measurable threshold, a named deliverable artefact or an enumerated output. Rows
reading `—` have no acceptance criteria yet and need them written.
