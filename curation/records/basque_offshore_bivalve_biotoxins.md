---
unique_name: basque_offshore_bivalve_biotoxins
name: Marine biotoxin benchmark (marine-ml-benchmark "biotoxin") / biotoxins in bivalves, Mendexa offshore aquaculture (AZTI)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Too Small
tags:
- Two-Regime Zeros
original_source: Other
year: '2025'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- '# First publication: AZTI data release on Mendeley Data (v2 2025-05-23, v1 2025-03-26; CC BY 4.0) and its Data in Brief descriptor'
- https://doi.org/10.17632/vyz9zvddz4.2
- https://doi.org/10.1016/j.dib.2025.111736
- '# Derivative: Zhou et al. 2026 cross-dataset benchmark (GitHub code, PLOS ONE paper, Zenodo processed tables)'
- https://github.com/zhm12305/marine-ml-benchmark
- https://doi.org/10.1371/journal.pone.0351325
- https://doi.org/10.5281/zenodo.19510440
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: AZTI's monitoring series names an early-warning use but
publishes no task, its toxin values are 93.6% non-detects coded at the limit of quantification, and it holds two
bivalve sites over about 290 dates; the benchmark table built on it is broken but can be rebuilt from the origin.
- Source: first published by AZTI on Mendeley Data (Solaun et al., "Long-term monitoring of potentially toxic
  phytoplankton, marine biotoxins and hydrographic variables in open waters off the Basque coast (SE Bay of Biscay)",
  v1 2025-03-26, v2 2025-05-23, CC BY 4.0), described in Solaun et al. 2025, Data in Brief 61:111736 (read in full on
  Europe PMC): three Excel tables, CTD profiles (Mendexa-Control and Mussel Farm-CTD), potentially toxic phytoplankton
  (45 taxa, cells/l) and "Biotoxins in bivalves" (24 toxin variables in six groups; AZTI pilot plant 2013-12-03 to
  2023-06-22, Mussel Farm 2019-06-17 to 2022-08-23; Data Description c, Table 2). The "biotoxin" table of Zhou et al.
  2026 (PLOS ONE; GitHub and Zenodo) is a derivative whose two predictors are the stations' coordinates and whose
  target pools the 24 toxins in five units (earlier AI triage, 2026-10-19, reproduced its 5,076 rows): a problem of
  that copy (PROV-15), repairable from the origin (PROV-13), so `Data Quality Issue` is dropped here.
  `original_source` says `Github` and `original_data_state` `One Table`, which describe the derivative; by PROV-8
  the origin is the Mendeley Data release (`Other`) in three tables. Left for the curator.
- Target and zeros: no true zeros. The earlier AI triage measured a minimum of 0.03 and 93.6% of rows flagged "<" with
  the limit of quantification as the value, so Zhou et al.'s "strongly zero-inflated (often zero or near-zero)"
  (Sec. 2.1.1) describes non-detects. Whether a below-LOQ code may count as a zero is the family's open question on
  coded and censored zeros (settled by Andrej on 2026-10-30, policy question 2 of the zero-inflated review: how a source
  codes its zeros is a cleaning choice at /add-dataset, no reason for a No).
- Use case: the descriptor states one conditionally: the series, "in combination with other sources of information
  (meteorological, hydrological, currents, nutrients, etc.), could be useful to develop early warning systems for
  toxic algal blooms" (Value of the Data). The decision it names is taken on measured toxins: "This will allow food
  safety managers to ban the sales when the biotoxins exceed the regulatory limits or temporarily close the harvesting
  areas as a precautionary measure". For example a food-safety manager deciding at a phytoplankton count whether to
  close harvesting before the toxin result, from a predicted exceedance; no source builds that task, so `No Good
  Target (yet)` and an approximate fit. Regime temporal (a dated series at two sites, SPLIT-6), near forecasting
  (SEL-10, SEL-11; TP-10 would decide).
- Siblings and duplicates: `basque_offshore_ctd_chlorophyll` is the same release and benchmark with another target
  (chlorophyll from the same CTD cast); distinct tasks of one source are no duplicates (PROV-7). This record stands for
  the AZTI release, whose CTD and phytoplankton tables are inputs of a toxin task. No other record (grep AZTI, Basque,
  biotoxin, Biscay, Mendexa). External collections: Zhou et al. 2026's cross-dataset benchmark (the broken copy).
- Papers and pages: Solaun et al. 2025 (the data descriptor); Zhou et al. 2026, "Cross-dataset benchmarking of
  machine learning models for marine and atmospheric environmental prediction", PLOS ONE (the derivative).
- Metric: none found for the origin (the descriptor fits no model). Zhou et al. rank their benchmark by R^2 ("For
  cross-dataset comparability, we use the coefficient of determination (R²) as the primary benchmark indicator",
  Sec. 2.4), on a table that does not carry over (MET-2); so the fallback, `roc_auc` for an exceedance or `rmse` for a
  level (MET-8).
- Risks for /add-dataset: the target is unbuilt (which toxin group; an exceedance of its regulatory limit or a level);
  the phytoplankton and CTD sites are not the bivalve sites, so dates must be matched; phytoplankton sampling changed
  in 2018 (Niskin depths to hose ranges); about 290 bivalve dates in all, so a test window may hold a handful of
  exceedances (TP-5, TP-9). `required_split` (`?`) and `problem_type` (`Regression`) follow the target once built. Not
  downloaded in this pass; the numbers are the earlier triage's.
- Priority: gap 0, use case 0 (suggested, not built), source + (AZTI release with a Data in Brief descriptor), shape 0
  (two sites, about 290 dates), risk - (target mostly censored at the LOQ, and unbuilt).

**Assessment (AI, 2026-10-30):** tag `Two-Regime Zeros` kept under the curator's definition of the tag (Andrej,
2026-10-30, policy question 4 of the zero-inflated review: "If the low value is by far the most frequent one and
independent of the remaining target distribution, then we can treat it as two regime zero, otherwise not"). For the
toxins a target would use, the non-detect code is by far the most frequent value and the quantified values lie above it:
okadaic acid 67.1% at its LOQ of 40 with 92 quantified values from 41 up, yessotoxin 55.2% at 0.06 with 129 above; 16 of
the 24 variables were never quantified. Also, the family's open question on coded and censored zeros is settled (Andrej,
2026-10-30, policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task,
independent if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower
priority. That the low value is a below-LOQ code therefore needs no rule beyond the cleaning at /add-dataset. The
verdict and priority stay; the unbuilt target remains the risk.

CC (2026-10-30, Andrej): `Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening
review page).

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

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/basque_offshore_bivalve_biotoxins/` by /add-dataset with the full review panel; the open questions are in its Review. Recommend `No` (`Too Small`), to revisit when AZTI publishes seasons after 2023: on leak-free inputs (plankton surveys at least 7 days old) the windows hold 6/7/0 exceedances of 160 and the quiet window fails TP-10 (its issue 1). The target is now built (the regulated okadaic-acid group), so `No Good Target (yet)` goes; `original_data_state` is a join of three tables. Correction to the Assessment above: yessotoxin has 125 values above 0.06, not 129. Priority 1: gap 0, use case 0, source +, shape 0 (280 samples), risk - (recommendation not to ship).

CC (2026-11-03, Andrej): `No` (`Too Small`), as the review recommended: "I follow your suggestion to retire the dataset." The three test windows hold 6, 7 and 0 samples above the EU limit; to revisit when AZTI publishes seasons after 2023. The record fields take the definition's values (`original_source` Other, `required_split` Temporal). The v2 folder left the working copy; its last definition is in the run folder of 2026-11-03, the committed one in 902011b3.

## Reference

Zhou X., Zhang H., Du T., Yuan Q., Wang H. (2026). Cross-dataset benchmarking of machine learning models for marine
and atmospheric environmental prediction. PLOS ONE. doi:10.1371/journal.pone.0351325. Upstream: Solaun O. et al.
(2025). Data in Brief 61:111736; data doi:10.17632/vyz9zvddz4.2.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 26 (Marine biotoxin benchmark).
