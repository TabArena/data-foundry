---
unique_name: basque_offshore_bivalve_biotoxins
name: Marine biotoxin benchmark (marine-ml-benchmark "biotoxin") / biotoxins in bivalves, Mendexa offshore aquaculture (AZTI)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Data Quality Issue
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Github
year: '2025'
domain: environmental science & climate
required_split:
- '?'
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/zhm12305/marine-ml-benchmark
- https://doi.org/10.1371/journal.pone.0351325
- https://doi.org/10.5281/zenodo.19510440
- https://doi.org/10.17632/vyz9zvddz4.2
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

The "biotoxin" table of a cross-dataset benchmark (Zhou et al. 2026, PLOS ONE; repository and Zenodo CC BY 4.0). Its
upstream, which the repository's README leaves as placeholders, is AZTI's monitoring of the Mendexa offshore
aquaculture site in the SE Bay of Biscay (Solaun et al. 2025, Data in Brief 61:111736; data on Mendeley,
doi:10.17632/vyz9zvddz4.2). The repository has no `clean.csv`, but running its `config.yaml` and `preprocess.py`
logic on the raw file reproduces exactly the paper's 5,076 rows. The raw file is 5,446 rows in long format: 24 toxin
variables, 293 dates from December 2013 to June 2023, 2 stations. The "two predictors" are the two stations'
latitude and longitude, and the target pools 24 toxins in 5 units, so the benchmark table is a broken derivative
(`Data Quality Issue`), and the upstream itself (2 stations, about 290 dates) is a monitoring series without a task.

Zero mechanism, confirmed from the data: there are no zeros. The minimum is 0.03, and 93.6% of the rows carry the "<"
flag with the limit of quantification as their value, i.e. non-detects coded at the LOQ. The paper's "strongly
zero-inflated (often zero or near-zero)" (Sec. 2.1.1) describes LOQ-coded non-detects, not zeros.

## Reference

Zhou X., Zhang H., Du T., Yuan Q., Wang H. (2026). Cross-dataset benchmarking of machine learning models for marine
and atmospheric environmental prediction. PLOS ONE. doi:10.1371/journal.pone.0351325. Upstream: Solaun O. et al.
(2025). Data in Brief 61:111736; data doi:10.17632/vyz9zvddz4.2.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 26 (Marine biotoxin benchmark).
