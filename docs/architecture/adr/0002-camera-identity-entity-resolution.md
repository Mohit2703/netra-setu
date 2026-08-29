# 0002 — Camera identity and entity resolution

**Scope.** How camera identity is issued and deduplicated across four
onboarding paths (bulk, manual, API, ONVIF) plus field verification.
Requirement IDs: `REG-01`, `REG-06`–`REG-12`.

## Context

`REG-11` specifies dedup via DBSCAN spatial clustering combined with fuzzy
name/asset-tag matching, feeding a merge queue for mandatory human
adjudication — never automatic merge. `REG-06` requires bulk import
(potentially thousands of rows) to support a dry-run preview and commit valid
rows while rejecting only invalid ones. DBSCAN is not naturally an
incremental/online algorithm.

## Options considered

1. **Optimistic issuance, dedup after.** URNs assigned at first sighting on
   any path; `REG-11`'s batch dedup runs after the fact. Never blocks
   onboarding and matches `REG-11`'s "merge queue" framing (duplicates are
   expected, not prevented) — but leaves a window where transient duplicate
   URNs exist and must be handled explicitly by every consumer until
   adjudicated.
2. **Pessimistic, synchronous dedup before issuance.** No URN issued until a
   full spatial+fuzzy check clears. No transient duplicates ever exist, but
   requires either a full-fleet re-clustering per row (doesn't scale to bulk
   import) or a weaker point check that isn't actually `REG-11`'s specified
   algorithm.
3. **Hybrid.** A cheap, synchronous exact/near-exact coincidence check
   (spatial-index proximity, no fuzzy name matching) blocks only the
   highest-confidence duplicate case at write time; the full `REG-11`
   DBSCAN+fuzzy-match pass runs asynchronously per onboarding batch,
   populating the merge queue.

## Decision

Option 3. Synchronous cheap check for exact-coincidence duplicates; async
batch DBSCAN+fuzzy match exactly as `REG-11` specifies, feeding the human
merge queue.

## Consequences

- Records pending adjudication need an explicit, stated policy for GIS/
  coverage reads in the meantime: both candidate records participate
  independently in the coverage union until adjudicated — undercounting
  coverage is judged worse than a small window of possible overcounting.
  Stated here so it isn't left implicit; full mechanics are WS-1 LLD work.
- `REG-06`'s dry-run/commit-valid-rows-only behaviour is unaffected — the
  async dedup pass runs after commit, not as a precondition of it.
- Bulk-import throughput is bounded only by the cheap synchronous check (a
  spatial-index lookup), not by full-fleet clustering — scales to
  80,000-camera bulk loads.

## Reversibility cost

Two-way door. The sync/async split is an implementation detail behind
`REG-11`'s stable external contract (records enter a merge queue for human
adjudication); it can be retuned without touching the URN scheme or the audit
model.

## Revisit trigger

Bulk-import load testing (WS-6) shows the async batch job can't keep the merge
queue's staleness window inside an acceptable bound at fleet scale.

## What this does not cover

The exact coverage-math policy for pending-merge records — stated as a
consequence above, detailed in the WS-1 LLD.
