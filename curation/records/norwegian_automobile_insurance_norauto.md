---
unique_name: norwegian_automobile_insurance_norauto
name: norauto (CASdatasets, Norwegian automobile insurance, one year)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Not Representative
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
domain: insurance
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://dutangc.github.io/CASdatasets/reference/norauto.html
- https://github.com/dutangc/CASdatasets/blob/master/data/norauto.rda
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

183,999 automobile policies of an unnamed Norwegian insurer over one year ("Unknown Norwegian insurer", downloaded by
CASdatasets from the University of Oslo; each row is a policy). Columns: `Male`, `Young` (binary), `DistLimit` (6
levels), `GeoRegion` (6 levels), exposure `Expo`, `ClaimAmount`, `NbClaim`. The workbook merged its rows 32 and 64
("Insurance norauto", "norauto / CASdatasets"); they are the same table.

Zero mechanism, confirmed from the data: `ClaimAmount` is 0 for the 95.4% of policies with `NbClaim` = 0, no claim in
the year. A quick untuned LightGBM (3-fold random CV) reaches ROC AUC 0.69 for a claim and R^2 0.02 on the log1p
amount.

The decisive fact is the feature space: the four rating factors form only 142 distinct cells, and 145,367 of the
183,999 rows are exact copies of another row. A model can do no more than estimate 142 cell means scaled by
exposure, which tests little that a GLM tariff does not. Licence: GPL (>= 2) (CASdatasets). To check: whether tuned
methods spread at all on it (task probes), which would overturn this.

## Reference

CASdatasets (Dutang C., Charpentier A.), `norauto`: "Unknown Norwegian insurer", downloaded from the University of
Oslo. https://dutangc.github.io/CASdatasets/reference/norauto.html

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 31 (Insurance norauto; norauto / CASdatasets,
original audit rows 32 and 64).
