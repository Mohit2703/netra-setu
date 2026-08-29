# 0003 — Viewshed representation

**Scope.** How a camera's field-of-view coverage is represented and computed.
Requirement IDs: `REG-14`, `REG-15`, `REG-16`, `REG-17`.

## Context

`REG-14` (as corrected — see `REGISTER.md`, wording fix 2026-08-29) requires
coverage stored as a wedge geometry derived from position, mounting height,
azimuth, horizontal FOV and effective range, with building footprints
subtracted *where footprint data is available* — the requirement itself
already concedes footprint data may not exist. `REG-15` requires the coverage
surface computable as a union per district/ward/road segment and renderable
as a heatmap. `REG-16` differences that surface against the OSM road network
and incident density. `REG-17` needs only a road-segment-inside-or-outside-
wedge test for cut-set analysis. Nothing in this repo states 3D building or
terrain data is available at state scale.

## Options considered

1. **Full 3D volumetric ray-casting** against building/terrain models. Most
   physically accurate, but no 3D data source is named anywhere in the
   register or capacity model, and ray-casting at 80,000 cameras is an
   unbudgeted compute cost `CAPACITY.md` doesn't account for. Over-engineered
   relative to what `REG-14` literally specifies.
2. **2D polygon wedge** — a pie-slice sector from position/azimuth/FOV/range,
   2D footprint polygons subtracted where available via standard
   polygon-difference. Matches `REG-14`'s text exactly; boring, cheap,
   well-supported GIS operation. `REG-15`'s union and `REG-16`'s road-network
   diff are natural 2D operations on this representation.
3. **2D default with an optional 3D refinement pass** for a small flagged
   high-value subset (e.g., border/highway ANPR cameras). No requirement asks
   for tiered fidelity; two code paths for one computation is premature
   generality dressed as a hedge.

## Decision

Option 2. 2D wedge polygon as the sole viewshed representation, footprint
subtraction applied where footprint data exists, unmodelled elsewhere
(matching `REG-14`'s own stated gap).

## Consequences

- SVC-002 (GIS & Coverage Engine) needs only 2D polygon operations (union,
  difference, point/line-in-polygon) — no 3D geometry library, no terrain
  data pipeline. Any 2D spatial store with polygon support satisfies this;
  the specific product is a smaller, separate ADR, deliberately not made here
  — `REG-14`'s wording fix moved it out of the requirement text for exactly
  this reason.
- `REG-14`'s own unresolved gap (what happens to a camera missing azimuth,
  height, or FOV) is unaffected by this decision and remains open in
  `REGISTER.md`'s Notes column.
- No ground-truth occlusion beyond the footprint layer: a wedge that
  geometrically overlaps a building it can't actually see through still
  counts as covered wherever footprint data is missing. Known, accepted
  limitation, not a defect of this decision.

## Reversibility cost

Two-way door for the fidelity choice itself — a 2D wedge column can gain a
3D-refinement side-table later without migrating the primary representation.
Keep a thin geometry-access port between SVC-002 and its consumers (SVC-012's
cut-set analysis, the gap-analysis report) so a future product/fidelity
change doesn't ripple into every consumer directly.

## Revisit trigger

A specific border/highway corridor's false-coverage rate (wedge says covered,
operator reports it isn't) is measured and shown material during Stage 2
live-demo preparation.

## What this does not cover

The specific spatial-store product (the technology choice `REG-14`'s wording
fix deferred) — a smaller, separate ADR once storage-layer choices are made
across the platform, not scoped here.
