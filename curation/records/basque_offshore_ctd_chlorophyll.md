---
unique_name: basque_offshore_ctd_chlorophyll
name: Hydrographic benchmark (marine-ml-benchmark "hydrographic") / CTD profiles at Mendexa offshore aquaculture (AZTI)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
original_source: Other
year: '2025'
domain: environmental science & climate
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- '# First publication: AZTI data release on Mendeley Data (v2 2025-05-23, v1 2025-03-26; CC BY 4.0) and its Data in Brief descriptor'
- https://doi.org/10.17632/vyz9zvddz4.2
- https://doi.org/10.1016/j.dib.2025.111736
- '# Derivative: Zhou et al. 2026 cross-dataset benchmark (GitHub code, PLOS ONE paper)'
- https://github.com/zhm12305/marine-ml-benchmark
- https://doi.org/10.1371/journal.pone.0351325
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: chlorophyll from the other channels of the same CTD
cast, a target a methods benchmark chose without a stated use; a virtual-sensor or gap-filling use is plausible but
named by no source, and the target has no zeros.
- Source: first published by AZTI on Mendeley Data (Solaun et al., v1 2025-03-26, v2 2025-05-23, CC BY 4.0),
  described in Solaun et al. 2025, Data in Brief 61:111736 (read in full on Europe PMC): the "Hydrographic variables"
  table, 145 CTD profiles at Mendexa-Control (2014-05-20 to 2023-12-18) and 35 at Mussel Farm-CTD (2021-02-17 to
  2023-12-18) (Data Description a), measured with "Sea-Bird SBE-25 and 25plus CTD instruments" (Abstract). The
  "hydrographic" table of Zhou et al. 2026 (PLOS ONE; GitHub, Zenodo) is derived from it: 4,653 rows from 132 casts
  with 11 predictors after quality control and an IQR filter, published as a regression with a chronological split
  (earlier AI triage, 2026-10-19, reproduced the rows). `original_source` says `Github`, which is the derivative; by
  PROV-8 the origin is the Mendeley Data release (`Other`), left for the curator.
- Target and zeros: fluorometer chlorophyll a (ug/l) per 1-dbar bin. No zeros (minimum 0.03, earlier triage), so the
  `Two-Regime Zeros` tag is only the lead that brought it in.
- Use case: no source states one. The descriptor's uses are trends, toxin limits and shellfish management, and early
  warning "for toxic algal blooms" (Value of the Data), named for the series as a whole; Zhou et al. give no reason for
  the chlorophyll target beyond a cross-dataset benchmark ("we fill this gap by building a unified cross-dataset
  benchmark", Sec. 1). For example AZTI filling fluorometer gaps, or estimating chlorophyll for casts made without a
  fluorometer, a virtual sensor as in `electric_motor_temperature_prediction` (Yes); fit approximate at best. Regime
  grouped by cast or temporal (SPLIT-3, SPLIT-5); bins within a cast are dependent.
- Siblings and duplicates: `basque_offshore_bivalve_biotoxins` (same release and benchmark, a toxin target;
  `TBD -> 2nd Tier`, priority 1, this run): one source, distinct tasks (PROV-7). That record rests on the descriptor's
  own early-warning sentence for the toxins; nothing of the kind is said for chlorophyll, which is why this record is
  the weaker of the two. No other record (grep AZTI, Basque, Biscay, Mendexa, chlorophyll). External collections: Zhou
  et al. 2026's benchmark.
- Papers and pages: Solaun et al. 2025 (the data descriptor); Zhou et al. 2026,
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0351325 (the derivative; its "nutrient
  concentrations" are not in the file). Zheng et al. 2024, Sci Rep 14 (doi:10.1038/s41598-024-76748-5), estimate 3D
  chlorophyll from temperature, salinity and depth (abstract only, from the reject check; unverified).
- Metric: none for the origin; Zhou et al. rank their benchmark by R^2 ("we use the coefficient of determination (R²)
  as the primary benchmark indicator", Sec. 2.4), one choice for comparability across datasets rather than for a
  decision: the fallback `rmse` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: (1) write a use case with an actor (AZTI filling fluorometer gaps, casts without a
  fluorometer) and look for a source that names it, else the curator decides whether a "for example" virtual sensor is
  enough (USE-1, USE-8); (2) restrict the inputs to what that platform has, and score with and without light
  transmission and PAR, co-measured optical channels (TP-4, `one_feature`); (3) rebuild from AZTI's Mendeley v2
  (https://doi.org/10.17632/vyz9zvddz4.2), not Zhou's IQR-filtered copy (PROV-13): -999 codes to missing, bloom values
  kept; (4) split grouped by cast or temporal (SPLIT-3, SPLIT-5), with TP-5 on 132 to 180 casts at two stations;
  (5) no zeros, so it sits outside the family and the tag is only a lead. Not downloaded in this pass.
- Priority: gap 0, use case 0 (a "for example" virtual sensor), source + (AZTI release with a Data in Brief
  descriptor), shape 0 (132-180 casts, the unit of a split), risk - (co-measured channels, a target no source
  motivates).
- Reject check (AI, 2026-10-27): does not stand. The proposed SEL-3 reject rested on the inference that a co-measured
  channel serves no decision, not on the source's words, and virtual sensors have precedent in the benchmark.

**Assessment (AI, 2026-10-30):** tag `Two-Regime Zeros` removed under the curator's definition of the tag (Andrej,
2026-10-30, policy question 4 of the zero-inflated review: "If the low value is by far the most frequent one and
independent of the remaining target distribution, then we can treat it as two regime zero, otherwise not"). Measured on
the hydrographic table (8,195 rows): the minimum, 0.03 ug/l, is the most frequent value but holds 3.5% of the rows
against 1.9% for the next (0.21), and it is the low end of a continuous spread (5th percentile 0.06, median 0.43), not a
regime of its own. One row carries -999, a missing-value code.

CC (2026-10-30, Andrej): `Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening
review page).

The "hydrographic" table of the same benchmark as `basque_offshore_bivalve_biotoxins`, from the same AZTI upstream.
The raw file is 8,195 rows of 1-dbar CTD depth bins from 2 stations on 146 dates (May 2014 to December 2023);
reproducing the repository's pipeline (quality control plus an IQR filter) gives exactly the paper's 4,653 rows from
132 casts with 11 predictors (latitude, longitude, time of day, pressure, temperature, salinity, sigma-theta, light
transmission, PAR, dissolved oxygen, oxygen saturation). The task is predicting fluorometer chlorophyll from the
other sensor channels of the same cast, which has no use case; rows within a cast are dependent, the IQR filter cuts
the bloom values, and the "nutrient concentrations" the paper mentions are not in the file. -999 missing codes occur
in PAR (297), salinity (95) and temperature (47).

Zero mechanism, confirmed from the data: none, chlorophyll has no exact zeros (minimum 0.03). Workbook pushback: "not
clearly established" is generous; the target has no zero regime at all.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/basque_offshore_ctd_chlorophyll/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping with the fill of a survey whose fluorometer failed as the use case (its issue 1; otherwise `No` + `No Good Target / Scientific Discovery`). Re-split temporal after the panel (nine windows of two survey days, 2022-09 to 2023-12) with the station's last measured chlorophyll as a feature. Correction to the 2026-10-30 Assessment above: 0.03 ug/l is a reporting floor of 2018-11-19 to 2022-09-12 (287 bins in 25 casts, against 37 at 0.04), not "the low end of a continuous spread"; the tag's removal stands (3.5% against 1.9%). Priority 2: gap 0, use case 0, source + (AZTI data descriptor), shape +, risk - (the use case is a validity call).

CC (2026-11-03, Andrej): `No` (`No Good Target / Scientific Discovery`): "The resons to not ship this dataset outweigh the reasons to ship, it seems like this is a made up task." The record fields take the definition's values (`original_source` Other, `required_split` Temporal). The v2 folder left the working copy; its last definition is in the run folder of 2026-11-03, the committed one in 902011b3.

## Reference

Zhou X., Zhang H., Du T., Yuan Q., Wang H. (2026). Cross-dataset benchmarking of machine learning models for marine
and atmospheric environmental prediction. PLOS ONE. doi:10.1371/journal.pone.0351325. Upstream: Solaun O. et al.
(2025). Data in Brief 61:111736; data doi:10.17632/vyz9zvddz4.2.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 27 (Hydrographic benchmark).
