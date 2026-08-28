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

| ID | Property | Target | Build class | Priority |
|---|---|---|---|---|
| NFR-01 | Registry portal availability | 99.9% | MODEL | not stated |
| NFR-02 | Live-view availability per feed, excluding camera and network faults | 99.5% | MODEL | not stated |
| NFR-03 | Frame capture → operator alert | p95 < 3 s | LIVE | not stated |
| NFR-04 | Plate query across 90 days of events | p95 < 5 s | LIVE + SIM | not stated |
| NFR-05 | Live-view stream start | < 2 s | LIVE | not stated |
| NFR-06 | Metadata tier disaster recovery | RPO 5 min / RTO 30 min | MODEL | not stated |
| NFR-07 | Graceful degradation | Operable at 30% feed loss, with cause attribution per unavailable feed | LIVE | Must |
| NFR-08 | Horizontal scale-out | New node joins by registration, no central reconfiguration | MODEL | Must |

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

## 4. What this file does not settle

- Edge buffer capacity in hours for `VMS-08`. Not stated in the baseline.
- Storage sizing for the tiers that are actually built — §2.2 sizes only the
  rejected centralised option. Hot-tier (24–72 h) and warm-tier (~30 days)
  volumes under `VMS-16`/`VMS-17` retrieval triggers are not yet derived.
- Whether ~90 streams/GPU at 2 fps holds on the intended hardware. It is the
  single least-supported number in the model and it moves 333 of the 838 GPUs.
- Availability targets NFR-01 and NFR-02 have no error budget, no measurement
  window and no dependency model behind them.
