---
unique_name: maps_router_eta
name: Maps Routing
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Anonymized
tags:
- Non-IID (Temporal)
collections:
- TabArena Reject
- TabRed
original_source: Kaggle
year: '2024'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/pcovkrd84mejm/maps-routing
- https://github.com/yandex-research/tabred/tree/main/preprocessing#maps-router-eta
notebook_path: datasets/beyond_iid/temporal/maps_router_eta/maps_router_eta_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/maps_router_eta_1m/dataset.py
source_row: 714
type_adapter_id: curation-record-v1
---

## Comments

Was downsampled/filtered by TabRed via preprocessing.

TabRed, 1 week horizon.

Not much more, need to follow preprocessing from TabRed most likely.

CC (2026-10-19, Lennart): TabReD's quantile transform of the numeric features may be fit on all rows (undocumented); kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): check SPLIT-9 on the weekly test windows and add a gap where train labels arrive late, as for nyc_taxi_trip_duration and pkdd_15 (cross-dataset review, marked ok).

**Assessment (AI, 2026-10-21):** SPLIT-9 late labels in maps_router_eta_1m (request time + exp(target) s/km x track_length, read as metres: its minimum is 1,000.0, and the median speed is 27 km/h; drives up to 16.6 h): without a gap 656, 654 and 578 train routes per weekly window (newest first; starts 2023-12-04, 11-27, 11-20) end after the window start; with a gap of one day (TemporalSplits(..., gap=1)) none. The gap removes 292k, 313k and 299k of the 11.2M, 8.8M and 6.4M earlier routes (2.6 to 4.7%); each train side is still a random 1M. Gap set in dataset.py, counts in splits_comment; script local-data-warehouse/_runs/2026-10-21_crosscut/x21-0/late_labels.py.

**Assessment (AI, 2026-10-21):** Unit and errors of track_length (follow-up to the SPLIT-9 gap). TabReD's paper (App. B.2) defines only the target, log seconds per km; neither the paper nor its preprocessing README/code states the unit of track_length. It is metres: min 1,000.0, median 5,168, max 1,103,597, no value a multiple of 10; read as metres the drive takes 0.03 to 16.6 h (median 0.19 h), read as km the median is 194 h. Implied speed (3600 / exp(target)) is 0.97 to 160 km/h, median 27, 99.9% 90. Implausible rows: 31 of 13.64M (0.0002%): 12 above 150 km/h, 5 below 2 km/h, 14 longer than 12 h (944 longer than 6 h, median 477 km at 67 km/h, plausible long drives); 26, 19, 12 in the train sides and 5, 7, 7 in the test windows (newest first). None of the 656, 654, 578 late routes is implausible (late drives median 0.35 h, 13 km, requested median 9 min before the window start, at most 11.4 h), so the one-day gap stands; no CLEAN-11 fix proposed. Script and output: local-data-warehouse/_runs/2026-10-21_crosscut/x32-4/units.py, units.txt.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — RMSE (TabReD's regression metric) (Rubachev et al., TabReD, ICLR 2025 (https://arxiv.org/abs/2406.19380)).

## Reference

TabRed
