# Non-functional targets and capacity model

Covers `NFR-01`–`NFR-08` and the sizing arithmetic behind `VMS-14`, `VMS-16`
and `VMS-18`. Requirement statements live in [REGISTER.md](REGISTER.md); this
file holds the numbers and their derivations.

Every input is labelled. `ASSUMED` values are estimates that have not been
measured and are expected to be challenged — they are stated in one place so
that changing one changes every downstream figure. `GIVEN` values come from the
requirements baseline or from published infrastructure facts.

---

## 1. Non-functional targets

| ID | Property | Target | SLI / measurement method | Build class | Priority |
|---|---|---|---|---|---|
| NFR-01 | Registry portal availability | 99.9% | Successful-request ratio over a rolling window (window TBD, see gap below) | MODEL | not stated |
| NFR-02 | Live-view availability per feed, excluding camera and network faults | 99.5% | Per-feed stream-active ratio, faults attributed per `NFR-07`, from `REG-20` health signals | MODEL | not stated |
| NFR-03 | Frame capture → operator alert | p95 < 3 s | Alert-event timestamp minus capture timestamp, p95; arithmetic in `HLD.md` §6, measured via §3's load test | LIVE | not stated |
| NFR-04 | Plate query across 90 days of events | p95 < 5 s | Query response time, p95; §3's load test (corpus-cardinality caveat below applies) | LIVE + SIM | not stated |
| NFR-05 | Live-view stream start | < 2 s | Time from stream request to first rendered frame; instrumented at the Live View Gateway (WS-2 LLD) | LIVE | not stated |
| NFR-06 | Metadata tier disaster recovery | RPO 5 min / RTO 30 min | Replication lag (RPO proxy) + measured failover duration (RTO); design in WS-6 LLD §2–§3 | MODEL | not stated |
| NFR-07 | Graceful degradation | Operable at 30% feed loss, with cause attribution per unavailable feed | Core-function pass/fail under a synthetic 30%-feed-kill test, plus attribution-correctness rate; test named in `SCOPE.md` risk `R-03`, not yet run | LIVE | Must |
| NFR-08 | Horizontal scale-out | New node joins by registration, no central reconfiguration | Central-config diff is empty after a registration event (binary, per-registration); sequence in WS-6 LLD §3.1 | MODEL | Must |

Gaps in the target definitions, carried forward as work to do:

- NFR-01, NFR-02: no measurement window and no exclusion list.
- NFR-05: no percentile stated, unlike NFR-03 and NFR-04.
- NFR-07, NFR-08: no measurable target value — the source table's third column
  held a MoSCoW priority for these two rows rather than a target.

---

## 2. Capacity model — 80,000 cameras

### 2.1 Inputs

| Parameter | Value | Label | Source or basis |
|---|---|---|---|
| Camera count | 80,000 | GIVEN | Challenge target fleet size |
| Blended average bitrate | 2 Mbps | ASSUMED | Mix of 1080p H.265, 4 MP and legacy SD |
| ANPR-capable cameras | 8,000 | ASSUMED | Borders, highways, strategic sites |
| Sampled urban junction cameras | 30,000 | ASSUMED | VMS-14 middle tier |
| Event-triggered remainder | 42,000 | ASSUMED | Balance of the fleet; 8,000 + 30,000 + 42,000 = 80,000 |
| Vehicle events per ANPR camera per day | 25,920 | ASSUMED | 0.3 events/s averaged over 24 h; 0.3 × 86,400 = 25,920 |
| Event record size (JSON) | ~500 B | ASSUMED | — |
| Event thumbnail crop | ~8 KB | ASSUMED | — |
| Streams per L4-class GPU, full-rate detection + OCR | ~20 | ASSUMED | TensorRT INT8 |
| Streams per L4-class GPU at ~2 fps | ~90 | ASSUMED | Not in the source assumption table; used in the GPU arithmetic. Implies ~4.5× throughput over full rate, which is itself unvalidated. |
| Concurrency of the event-triggered tier | 5% | ASSUMED | Not in the source assumption table; used in the GPU arithmetic |
| Peak-to-average event factor | 4× | ASSUMED | Not in the source assumption table; used in the event-rate arithmetic |
| Raw-video retention window for the rejection case | 30 days | ASSUMED | Used only to size the option being rejected |
| Erasure-coding scheme | 8+3 | ASSUMED | Overhead factor 11/8 = 1.375 |
| Edge node count | 34 | GIVEN | Existing district command-and-control centres |
| Seconds per day | 86,400 | GIVEN | — |
| Storage units | Decimal (1 PB = 10⁶ GB) | GIVEN | Consistent throughout |

### 2.2 Result 1 — centralised recording is rejected

```
80,000 cameras × 2 Mbps        = 160,000 Mbps = 160 Gbps sustained
160 Gbps ÷ 8                   = 20 GB/s
20 GB/s × 86,400 s             = 1,728,000 GB   ≈ 1.73 PB per day
1.73 PB/day × 30 days          = 51.8 PB raw
51.8 PB × 1.375 (EC 8+3)       ≈ 71 PB of physical disk
```

71 PB of storage and 160 Gbps of sustained ingress into a single state tier is
the justification for `VMS-16` — metadata central, video local. The number is
not a budget to be found; it is the reason the architecture is federated.

### 2.3 Result 2 — the metadata path is affordable

```
8,000 ANPR cameras × 25,920 events/day = 207,360,000  ≈ 207 M events/day
207.36 M ÷ 86,400 s                    ≈ 2,400 events/s average
2,400 × 4 (peak factor)                ≈ 9,600        ≈ 10,000 events/s peak

JSON:        207.36 M × 500 B = 103.7 GB/day  → ~37.8 TB/year, pre-compression
Thumbnails:  207.36 M × 8 KB  = 1.66 TB/day   → ~149 TB over a 90-day window
```

Video at 1.73 PB/day against event JSON at 0.104 TB/day is a reduction of
roughly four orders of magnitude (ratio ≈ 1.66 × 10⁴). Thumbnails are tiered
separately from JSON because they are 16× the volume.

10,000 events/s is a modest sustained write rate for a partitioned log, and a
compressed time-series store holds a year of event JSON on commodity hardware.

### 2.4 Result 3 — GPU budget, and why tiering is mandatory

```
Naive — continuous full-rate inference on everything:
  80,000 ÷ 20 streams/GPU                        = 4,000 GPUs

Tiered per VMS-14:
  8,000 full-rate      ÷ 20 streams/GPU          =   400 GPUs
  30,000 at ~2 fps     ÷ ~90 streams/GPU         =   333 GPUs
  42,000 event-driven, 5% concurrent
    → 2,100 concurrent ÷ 20 streams/GPU          =   105 GPUs
                                                 -------------
                                        Total    ≈   838 GPUs  (stated as ~840)

  838 ÷ 34 district nodes                        ≈  25 GPUs per node
```

The tiering in `VMS-14` is not an optimisation; without it the GPU count is
4,000 and the design does not exist. 25 GPUs per district node is a procurable
figure, and the derivation is more defensible than the figure.

### 2.5 Result 4 — backhaul

With inference at the edge, the backhaul to the state tier carries metadata plus
on-demand video only.

```
Metadata headroom budget                          = 10 Gbps aggregate
Video-on-demand pool, 500 concurrent × 2 Mbps     = 1 Gbps
                                                  ------------
Total                                             = 11 Gbps

Compare against the naive centralised design      = 160 Gbps
```

The 10 Gbps metadata allocation is deliberately over-provisioned against the
~104 GB/day computed in §2.3; it is headroom, not a derived requirement. The
500-concurrent-investigation figure is ASSUMED and unvalidated.

---

## 3. Load-test plan — evidence for the NFR set

| Element | Approach |
|---|---|
| Simulated fleet | 500–2,000 synthetic cameras, produced by FFmpeg looping recorded files against the real connector stack |
| Metadata path | k6 or Locust driving the event ingestion API; measure sustained events/s, p95 write latency and consumer lag |
| Query path | Synthetic event corpus of 500 M+ records; measure NFR-04 at realistic cardinality |
| Extrapolation | Measured per-node throughput × node count, with linearity assumptions stated and the binding bottleneck named |

The method is: measure one node, model the fleet, state the assumptions, name
the bottleneck. Do not simulate 80,000 cameras and do not present a modelled
number as a measured one.

### Known inconsistency in the test plan

The query-path corpus of 500 M events is about 2.4 days of the modelled fleet
(207 M events/day), not the 90 days that `NFR-04` and `VMS-21` specify. At the
modelled event rate a 90-day window holds roughly 18.7 billion events — 37×
larger than the planned corpus. Either the corpus target rises, or `NFR-04` is
validated at a stated lower cardinality and extrapolated with the extrapolation
method named above. This is unresolved.

---

## 5. Multi-point scaling curve

Same method as §2, applied at five milestones: 1 (single dev/demo camera),
100 (early pilot), 7,000 (≈ VISWAS Phase 1), 17,500 (≈ full VISWAS), 80,000
(challenge target). Figures below hold the same tier ratio as §2.1 (10%
full-rate / 37.5% sampled / 52.5% event-triggered); all `ASSUMED` except the
80,000 row, which restates §2's `GIVEN`/derived figures.

### 5.1 Tier population (proportional)

| Cameras | Full-rate (10%) | Sampled (37.5%) | Event-triggered (52.5%) |
|---|---|---|---|
| 1 | 1 (treated as full-rate — ASSUMED, the tier split is moot at n=1) | 0 | 0 |
| 100 | 10 | 38 | 52 |
| 7,000 | 700 | 2,625 | 3,675 |
| 17,500 | 1,750 | 6,563 | 9,187 |
| 80,000 | 8,000 (GIVEN) | 30,000 (GIVEN) | 42,000 (GIVEN) |

### 5.2 GPU budget (same formula as §2.4)

| Cameras | GPUs | Notes |
|---|---|---|
| 1 | 1 (floor) | Formula gives <1; a demo needs at least one GPU regardless of the arithmetic |
| 100 | ~2 (floor) | Formula gives 1.05; a minimum-viable-node floor applies below this |
| 7,000 | ~74 | Naive proportional — see §5.4, this is an upper bound in practice |
| 17,500 | ~184 | Naive proportional — see §5.4, this is an upper bound in practice |
| 80,000 | 838 (GIVEN, §2.4) | |

### 5.3 Metadata-plane load (events from the full-rate tier only, per §2.3's method)

| Cameras | Events/day | Avg events/s | Peak events/s (×4) | JSON volume/day |
|---|---|---|---|---|
| 1 | 25,920 | 0.3 | 1.2 | ~13 KB |
| 100 | 259,200 | 3 | 12 | ~130 MB |
| 7,000 | 18,144,000 | 210 | 840 | ~9.1 GB |
| 17,500 | 45,360,000 | 525 | 2,100 | ~22.7 GB |
| 80,000 | 207,360,000 (GIVEN, §2.3) | 2,400 | ~10,000 | ~103.7 GB (GIVEN) |

### 5.4 The VISWAS caveat — 7,000 and 17,500 are not hypothetical

Unlike the other three rows, 7,000 and 17,500 aren't "what if we had this
many cameras" — they are the actual size of VISWAS Phase 1 and full VISWAS
(kickoff §1.2). Per [ADR 0005](../architecture/adr/0005-edge-central-split.md)
and [`OPEN-QUESTIONS.md`](../architecture/OPEN-QUESTIONS.md) OQ-003, VISWAS
cameras are bridged: their analytics already run under ITMS, not netra-setu's
own Analytics Runtime. §5.1/§5.2's proportional figures for these two rows
are therefore an **upper bound that will not be procured in practice** at
those literal rollout points — the real GPU need at "VISWAS fully onboarded,
zero delta cameras yet" is closer to the cost of *bridging* (metadata
ingestion only, no inference) than to the 74/184 GPUs shown. The 80,000-row
is the only one where the full formula is known to apply, because by then
all ~62,500 delta cameras (which *do* need our inference) are onboarded too.
`OPEN-QUESTIONS.md` OQ-009 tracks resolving the exact split.

---

## 6. Netram-node resource envelope and cost sketch

### 6.1 Resource envelope per node, at full 80,000-camera scale

| Resource | Per node (of 34) | Basis |
|---|---|---|
| GPUs | ~25 | 838 ÷ 34 (§2.4) — pending OQ-009's downward revision |
| Cameras served | ~2,353 | 80,000 ÷ 34 — ASSUMED even distribution across nodes |
| Hot storage, 24h–72h window | 50.8 TB – 152.5 TB | Derivation: §6.2 |
| Warm storage, ~30 days, physical (post erasure-coding) | ≈ 2.1 PB | Derivation: §6.2 |

The even-distribution assumption is known to be wrong in one direction
already: VISWAS is deployed across all 34 districts today (kickoff §1.2), so
its ~17,500 cameras are already spread statewide, not concentrated. A
100-camera early pilot, by contrast, more plausibly concentrates on 1–3
nodes rather than spreading 3 cameras across all 34 — the per-node figures
above are the 80,000-camera steady state, not every milestone in §5.

### 6.2 Hot/warm storage derivation

```
Per camera: 2 Mbps × 3,600 s/hour ÷ 8 = 900 MB/hour = 21.6 GB/day
            (continuous recording, blended bitrate — ASSUMED, same figure as §2.1)

Hot tier (24-72h window, VMS-18, edge-resident):
  Lower bound (24h):  21.6 GB × 1 day   = 21.6 GB/camera
  Upper bound (72h):  21.6 GB × 3 days  = 64.8 GB/camera
  At 80,000 cameras:  1.73 PB – 5.18 PB fleet-wide, split across 34 nodes
  Per node (÷34):     50.8 TB – 152.5 TB

Warm tier (~30 days, VMS-18):
  21.6 GB/day × 30 days = 648 GB/camera
  At 80,000 cameras:     51.8 PB fleet-wide raw — the same arithmetic as
                         §2.2's rejected-centralised-option calculation,
                         same numbers, different conclusion: this is what
                         is actually built, distributed across 34 edge
                         sites instead of centralised in one place. Warm
                         tier is edge-resident, not central — `VMS-16`'s
                         "no raw video path to the state tier other than
                         VMS-17 triggers" applies to it exactly as it does
                         to the hot tier (corrected 2026-08-29; see
                         `HLD.md` §3's SVC-011 row).
  × 1.375 (EC 8+3):      ≈ 71.3 PB physical, fleet-wide
  Per node (÷34):        ≈ 2.1 PB physical per node
```

2.1 PB of erasure-coded warm storage at each of 34 sites is a serious
procurement line, not a footnote — the direct, honest consequence of
holding ~30 days of raw video per camera at all. Only reachable if the
retention window or the erasure-coding overhead is revisited later, not if
the number is wished away now.

### 6.3 Cost sketch — illustrative structure only, not a quote

No verified procurement pricing exists anywhere in this repo. The structure
below is a placeholder for real quotes, not a budget, and should not be
copied into a submission as a number:

```
Total cost ≈ (GPU count × GPU unit cost)
            + (physical storage, PB × cost per PB)
            + (34 × per-node rack/power/networking overhead)
            + GSWAN bandwidth (likely already-sunk state infrastructure, CMP-08)

  838 GPUs (pending OQ-009) × [ILLUSTRATIVE ONLY — L4-class unit cost varies
              by region, volume and date; get a real OEM/data-centre quote,
              do not reuse any figure quoted here]
  + ≈71.3 PB warm + ≈5.2 PB hot (upper bound), physical,
              × [ILLUSTRATIVE ONLY — cost per PB for erasure-coded object
              storage on commodity hardware; get a real quote]
  + 34 sites × [ILLUSTRATIVE ONLY — rack/power/cooling/networking overhead]
```

Every bracketed term is a placeholder, not a number. Filling in a total
here without a real quote would itself violate this file's "every number
carries its derivation" rule.

---

## 7. What this file does not settle

- Edge buffer capacity in hours for `VMS-08`. Not stated in the baseline.
- Whether ~90 streams/GPU at 2 fps holds on the intended hardware. It is the
  single least-supported number in the model and it moves 333 of the 838 GPUs.
- Availability targets NFR-01 and NFR-02 have no error budget, no measurement
  window and no dependency model behind them.
- `OPEN-QUESTIONS.md` OQ-009: the VISWAS-vs-tier overlap. Until resolved, the
  838-GPU figure and the §6.1 resource envelope are upper bounds, not
  validated targets.
- Real procurement pricing for every bracketed placeholder in §6.3.
- The even-distribution-across-34-nodes assumption (§6.1) — known to not
  hold for VISWAS-scale milestones, untested for the actual rollout sequence
  (which depends on `SCOPE.md`'s roadmap, itself pending team-size/timeline
  input — see `OPEN-QUESTIONS.md` OQ-011).
