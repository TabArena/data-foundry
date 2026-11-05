---
unique_name: auto_intermittent_demand
name: Auto intermittent-demand series (Syntetos and Boylan 2005, GluonTS intermittent_auto)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Time-series (Forecasting)
tags:
- Two-Regime Zeros
original_source: Github
year: '2005'
domain: business & marketing
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

**Screening (AI, 2026-10-27):** `No` (`Time-series (Forecasting)`, SEL-10): monthly demand of 3,000 automotive
spare parts, a benchmark for intermittent-demand forecasting, with no column besides the item index and the month.
- Source: Syntetos and Boylan (2005), "The accuracy of intermittent demand estimates", International Journal of
  Forecasting 21(2):303-314 (https://doi.org/10.1016/j.ijforecast.2004.10.001), on 3,000 SKUs of the automotive
  industry; the public copy is the GluonTS fork of Turkmen et al. (`datasets/intermittent_auto`). As published: 3,000
  series x 24 months of demand; the earlier AI triage (2026-10-19) measured 22.0% zero cells and no missing values.
- Source's words: Turkmen et al. (2021, PLOS ONE 16:e0259764, Sec. 5.2): "The Auto data set consists of monthly
  demand data for 3000 items, for a period of 24 months"; "We take the last 6 demand periods of each time series as a
  held out sample". The release's `metadata/metadata.json` lists `"feat_static_real": [], "feat_dynamic_cat": [],
  "feat_dynamic_real": []` and one static category of cardinality 3000, the item index.
- Why SEL-11 and TP-10 do not apply: with no feature beyond the item and the period, a model can only learn each
  series' own past; TP-10 leg 1 has nothing to compare and leg 2 fails by construction.
- Use case: a parts planner forecasting the next months' demand of each SKU for stock control, the setting SEL-10
  excludes.
- Siblings and duplicates: `car_parts_intermittent_demand` and `raf_aerospace_parts_demand` (the same kind of
  univariate spare-parts benchmark, other data), `m5_forecasting_accuracy`. External collections: the GluonTS fork;
  fable.intermittent (Damato et al., arXiv 2609.28607, 2026) benchmarks Auto (per a search summary, not read).
- Metric: none for a tabular task; the source papers score forecast errors over a held-out horizon.
- Reject check (AI, 2026-10-27): stands. SEL-10 (Must). The release's feature lists are empty apart from the item
  index (https://raw.githubusercontent.com/canerturkmen/gluon-ts/intermittent-datasets/datasets/intermittent_auto/metadata/metadata.json),
  so the only task is forecasting each series from its own past.

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

Monthly demand of 3,000 automotive stock-keeping units over 24 months, attributed to Syntetos and Boylan (2005), in
the GluonTS fork of Turkmen et al. (2021). Downloaded on 2026-10-19: 3,000 series x 24 months, 22.0% exact zeros, no
missing values; the only feature is a series id. Turkmen et al., Sec. 5.2: "The Auto data set consists of monthly
demand data for 3000 items, for a period of 24 months"; they keep the 1,227 series classed intermittent or lumpy and
forecast "the last 6 demand periods". Univariate series forecasting, excluded.

Zero mechanism, confirmed from the data: months without demand. With 22% zero cells the full table is only mildly
zero-heavy; the intermittent benchmark is a filtered subset. No data licence stated.

## Reference

Syntetos A.A., Boylan J.E. (2005). The accuracy of intermittent demand estimates. International Journal of
Forecasting 21(2):303-314. Turkmen A.C., Januschowski T., Wang Y., Cemgil A.T. (2021). Forecasting intermittent and
sparse time series: A unified probabilistic framework via deep renewal processes. PLOS ONE 16(11):e0259764.
doi:10.1371/journal.pone.0259764.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 51 (Auto intermittent-demand benchmark).
