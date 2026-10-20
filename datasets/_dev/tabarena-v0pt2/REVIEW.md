# Across datasets

### Probes (`curation_probes/hidden_groups.py`)

- **Let the hidden-group probe consider float columns with repeated values.** Its single-column check takes a float
  column only when every value is a whole number (`is_candidate` in the general probe library), so a computed
  per-entity value never becomes a candidate. In airfoil_self_noise the boundary-layer thickness alone separates 104
  of the 106 wind-tunnel runs, and the probe missed the runs until composite keys were added (review-panel pilot,
  2026-10-19). Proposal: take a float column as a candidate when its distinct values are few against the rows (the
  same share rule as for integers), then re-run the hidden-group sweep and compare the hits. The probe library
  changes; no definition does.
