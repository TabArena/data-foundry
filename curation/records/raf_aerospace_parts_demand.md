---
unique_name: raf_aerospace_parts_demand
name: RAF aerospace spare-parts demand (Eaves and Kingsman 2004, GluonTS intermittent_raf)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- Two-Regime Zeros
original_source: Github
year: '2004'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Other
source_links:
- https://github.com/canerturkmen/gluon-ts/tree/intermittent-datasets/datasets
- https://doi.org/10.1371/journal.pone.0259764
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`Time-series (Forecasting)`, SEL-10): monthly demand of 5,000 Royal Air Force
spare parts, from a paper on forecasting for spare-parts ordering, with no column besides the part index and the month.
- Source: Eaves and Kingsman (2004), "Forecasting for the ordering and stock-holding of spare parts", Journal of the
  Operational Research Society 55(4):431-437 (https://doi.org/10.1057/palgrave.jors.2601697); the public copy is the
  GluonTS fork of Turkmen et al. (`datasets/intermittent_raf`). As published: 5,000 series x 84 months of demand; the
  earlier AI triage (2026-10-19) measured 89.8% zero cells and no missing values.
- Source's words: the paper's title; Turkmen et al. (2021, PLOS ONE, Sec. 5.2, read by the reject check): "The RAF
  data set consists of aerospace parts demand data taken from the Royal Air Force ... 84 months of data for 5000
  parts", with the last 6 periods held out. The release's `metadata/metadata.json` has only a static category of
  cardinality 5000, the part index.
- Why SEL-11 and TP-10 do not apply: as for `auto_intermittent_demand`, nothing but the series and the period.
- Use case: RAF inventory control forecasting the demand of each part, the setting SEL-10 excludes.
- Siblings and duplicates: `auto_intermittent_demand` (same fork, other data), `car_parts_intermittent_demand`; the
  copy the workbook also names (github.com/danieldehaan96/spdf) was not compared. External collections: the GluonTS
  fork; fable.intermittent (2026, per a search summary).
- Metric: none for a tabular task.
- Reject check (AI, 2026-10-27): stands. SEL-10 (Must). The release's only feature is the part index
  (https://raw.githubusercontent.com/canerturkmen/gluon-ts/intermittent-datasets/datasets/intermittent_raf/metadata/metadata.json),
  so the only task is forecasting each series from its own past.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

Monthly demand of 5,000 Royal Air Force spare parts over 84 months, attributed to Eaves and Kingsman (2004), in the
same GluonTS fork as `auto_intermittent_demand`. Downloaded on 2026-10-19: 5,000 series x 84 months, 89.8% exact
zeros, no missing values, a series id as the only feature. Turkmen et al. (2021, Sec. 5.2) hold out the last 6
periods. Univariate series forecasting, excluded.

Zero mechanism, confirmed from the data: months without demand for slow-moving spares. The alternative copy the
workbook names (github.com/danieldehaan96/spdf) was not compared. No data licence stated.

## Reference

Eaves A.H.C., Kingsman B.G. (2004). Forecasting for the ordering and stock-holding of spare parts. Journal of the
Operational Research Society 55(4):431-437. Used in Turkmen A.C. et al. (2021), PLOS ONE 16(11):e0259764.
doi:10.1371/journal.pone.0259764.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 52 (RAF aerospace-parts demand).
