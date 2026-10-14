---
unique_name: aeolus
name: Aeolus
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2025'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/datasets/flnny123/mfddmulti-modal-flight-delay-dataset
- https://github.com/Flnny/Delay-data
v2_path: datasets/_dev/tabarena-v0pt2/aeolus_1m/dataset.py
source_row: 733
type_adapter_id: curation-record-v1
---

## Comments

Quite extensive. Could be the best flight data there is

**Assessment (AI, 2026-10-07):** Source: Xu et al., NeurIPS 2025 Datasets and Benchmarks (arXiv:2510.26616); the Kaggle release holds 54,674,003 completed BTS flights 2016-2024 (March 2024 missing) with hourly Meteostat weather. Added as `aeolus_1m`: arrival 15 minutes or more late (US DOT definition, the paper's classification task), predicted before departure from the schedule and the airports' weather. The release joined Meteostat's UTC hours to local clock times, so that weather was observed a median 5.2 (origin) and 3.0 hours (destination) before the departure. The minutes make a poor target: the 1% longest delays hold 56-71% of their variance, and LightGBM reaches R² 0.01-0.02 on them against ROC AUC 0.64-0.67 for the indicator. So the problem type becomes Binary Classification.

**Assessment (AI, 2026-10-12), problems in the release:** (1) The authors' release joins Meteostat's hourly weather, whose timestamps are UTC, to the local scheduled clock times, so the weather of a flight is read 4-10 hours early (origin weather a median 5.2 hours before departure); a few destination readings fall after the departure. (2) March 2024 is missing. Both are worth reporting to the authors (Xu et al., NeurIPS 2025). The definition keeps the release as published and states both as `Anomaly:` bullets; the leak of the late destination readings is a `Potential leak, kept on purpose:` bullet.

CC (2026-10-12, Lennart): Target `ARR_DEL15` (arrival 15+ minutes late, ROC AUC), the weather as released, the flight number as a categorical. Two-week test windows (2024-12-18..31, 12-04..17, 11-20..12-03) instead of the three newest weeks, two of which fall in the holiday peak (25.1-26.5% late against 20.8% for 2024). History from 2023 on: TabReD's random sample of all nine years put only about 11.5% of each train side in 2024 and mixed in COVID-19 (2020: 9.7% late), while a model refit every two weeks trains on recent data with the previous holidays; the authors' own benchmarks use 2024 alone. The test-week comparison of history pools (each pool best in one week) did not decide it. The release's data problems are noted only, not reported.

## Reference

@article{xu2025aeolus,
  title={Aeolus: A Multi-structural Flight Delay Dataset},
  author={Xu, Lin and Yuan, Xinyun and Liang, Yuxuan and Yin, Suwan and Wu, Yuankai},
  journal={arXiv preprint arXiv:2510.26616},
  year={2025}
}
