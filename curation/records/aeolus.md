---
unique_name: aeolus
name: Aeolus
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2025'
domain: industry & manufacturing
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

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap -, use case -, source +, shape +, no known risk. Large temporal flight-delay task from a documented NeurIPS release, mixed features, direct fit; only licence and version notes remain open.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, provided the curator confirms keeping the release's mis-timed weather under PROV-13 (else retire for a rebuild from BTS and Meteostat as a new record); mask the weather read after the departure (LEAK-6, against the CC of 2026-10-12, open). Applied: fit `approximate` (weather 3.5-11.4 h old, a day for the 3.6% overnight arrivals; no inbound aircraft; operated flights only), impossible temperatures and wind speeds to missing, Guam and Pago Pago coordinate signs repaired, domain `industry & manufacturing` in the definition, notes corrected (paper's > 15 threshold, paper's June 2024 split, probes `no_spread`, LightGBM 0.612 and linear 0.594 on 50k rows, LightGBM 0.629-0.630 with 1M; the 2026-10-07 "0.64-0.67" is the superseded all-years set-up, the earlier "direct fit" is stale). Priority 2: gap -, use case - (fit approximate), source +, shape +, risk - (open PROV-13 damage that may need a rebuild, and a confirmed small leak).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC and ACC for the delay-occurrence classification task (Xu et al., Aeolus: A Multi-structural Flight Delay Dataset, NeurIPS 2025 D&B, arXiv:2510.26616 (Sec. 4, Appendix: 'using Area Under the Curve (AUC) and Accuracy (ACC) as evaluation metrics')).

CC (2026-10-26, Lennart): the record's domain takes the definition's value (industry & manufacturing, as nyc_taxi_trip_duration).

CC (2026-10-26, Lennart): issue 7: "mask": the weather read after the scheduled departure is set missing (LEAK-6). This replaces CC 2026-10-12 (the weather as released) for those readings.

CC (2026-10-26, Lennart): issue 8: "Can you rebuild this please, but keep it aeolus_correct or something? I assume we have all the information we need from the original sources, or is the data release from aeolus / the paper the only source of some information? if the paper state does not add much, we can build our better version as intended": the rebuild from BTS and Meteostat is the new record aeolus_rebuilt.

CC (2026-10-26, Lennart): the declared metric, ROC AUC, is checked as declared.

**Assessment (AI, 2026-10-26):** the mask is applied: each airport's time zone from its coordinates (`AIRPORT_TIME_ZONES`, 312 airports), the scheduled departure in UTC, and every weather reading whose hour (the release's local clock read as UTC) falls after it set missing. `dataset check` clean; task probes (3 windows): LightGBM ROC AUC 0.632, linear 0.611, no flag.

## Reference

@article{xu2025aeolus,
  title={Aeolus: A Multi-structural Flight Delay Dataset},
  author={Xu, Lin and Yuan, Xinyun and Liang, Yuxuan and Yin, Suwan and Wu, Yuankai},
  journal={arXiv preprint arXiv:2510.26616},
  year={2025}
}
