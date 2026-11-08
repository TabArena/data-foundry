---
unique_name: wadden_sea_sibes_macoma_abundance
name: Wadden Sea Macoma abundance (Lyashevska et al. 2016) / SIBES synoptic intertidal benthic survey (NIOZ, 2008-2022)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: Website
year: '2024'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- '# First publication: SIBES dataset, NIOZ data portal (Version 6, 2024-12-21; CC BY-SA 4.0), with its Scientific Data descriptor'
- https://doi.org/10.25850/nioz/7b.b.ug
- https://doi.org/10.1038/s41597-025-04540-9
- '# The workbook lead: Lyashevska et al. 2016 (2010 survey, no table released)'
- https://doi.org/10.1002/ece3.1880
v2_path: datasets/_dev/tabarena-v0pt2/wadden_sea_sibes_macoma_abundance/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> Yes`, priority 3: NIOZ's yearly survey of over 4,000 intertidal stations,
documented in Scientific Data, from which the paper behind the lead maps Macoma abundance with a cross-validated
zero-inflated model; open are whether abundance mapping counts as prediction, and a thin feature set.
- Source: SIBES (Synoptic Intertidal BEnthic Survey), NIOZ, sampled yearly since 2008. Release "SIBES dataset"
  (Version 6, production date 2024-12-21, CC BY-SA 4.0; "The most recent 3 years are under embargo, but available upon
  request") as `samples.csv` (station, date, coordinates, grain size, mud content, tidal basin, platform), `biota.csv`
  (abundance and AFDM per m2 per taxon and sample) and `species.csv`; descriptor Bijleveld et al. 2025, Scientific Data
  12:239 (its Data Records cover 2008-2021). Earlier AI triage, 2026-10-19, measured 59,463 samples from 2008-2022 at
  5,105 stations and 171 taxa. A source that grows yearly takes the year of the pinned snapshot (PROV-9), so `year`
  stays empty. Lyashevska et al. 2016 used the 2010 survey and released no table.
- Target and zeros: Macoma balthica (`sibes_id` 59) density per m2. "Note, when a species was absent in a sample, the
  row is not available. Zero values can be obtained by combining the files 'biota.csv' and 'samples.csv'"
  (Bijleveld et al. 2025, Table 4): a zero is no Macoma in the core, an observed absence. Earlier AI triage measured
  56.2% zeros (42-72% by year) and an untuned LightGBM on log1p density at R^2 0.36 grouped by station (presence AUC
  0.81; 0.28 on 2021-22 as a temporal test).
- Use case: Lyashevska et al. 2016, Introduction: "the objective of this study was to map the abundance of a bivalve
  species, using zero‐inflated and spatially correlated survey data, and to quantify the accuracy of the map"; the
  model "was used to make predictions for sites where only environmental data are available" (Abstract). SIBES "is also
  essential for management and evidence-based conservation of the Wadden Sea, such as, in relation to studying the
  effects of gas extraction, assessing the European habitat directive, monitoring the quality status of the Wadden
  Sea, and environmental impact assessments" (Bijleveld et al. 2025). For example a Wadden Sea manager mapping a key
  shorebird prey between survey stations for a habitat assessment; no source names the decision taken on the map, so
  the fit is approximate. Regime grouped by station (a place not sampled; the paper's leave-one-out cross-validation
  is the analogue), temporal by year the alternative (SPLIT-3: one, the curator's pick).
- Siblings and duplicates: none in curation/records (grep SIBES, Wadden, Macoma, NIOZ, benthic). Closest accepted
  precedent: `covertype` (Yes, Lennart), cover type mapped from site variables to "fill the gaps to predict unseen
  areas". External collections: none found.
- Papers and pages: Bijleveld et al. 2025 (the data descriptor); Lyashevska et al. 2016 (zero-inflated Poisson
  mapping on the 2010 survey, 66% of 3,451 counts zero); the SIBES R package (github.com/allertbijleveld/SIBES) has
  the zero-filling join.
- Metric: Lyashevska et al. 2016, Materials and Methods: confusion matrices for prevalence, and "For predicted
  intensity and predicted unconditional intensity, the quality measures were mean error (ME) and mean squared error
  (MSE)", by leave-one-out cross-validation. Several measures side by side: fallback `rmse` (MET-5), which ranks
  models as the paper's MSE on the unconditional intensity; inputs none. The scale (density or log1p) is part of the
  family's open metric question (MET-3).
- Risks for /add-dataset: the sediment columns come from the same sampling as the fauna, while at an unsampled site
  they would come from a sediment map (name the prediction point, USE-3); the paper's elevation covariate is not in
  the release (a bathymetry join would be ours); 769 samples without any biota row (empty core or missing record) and
  sediment missing in 3,687 samples (earlier triage); the taxon follows the paper. Open policy question: whether
  species-abundance mapping from habitat covariates counts as prediction
  (settled by Andrej on 2026-10-30, policy question 2 of the zero-inflated review: how a source codes its zeros is a
  cleaning choice at /add-dataset, no reason for a No).
- Priority: gap 0 (biology & life sciences has 4 accepted, regression and grouped are not thin), use case 0 (uses
  named, no decision on the map; approximate), source + (NIOZ release with a data descriptor), shape + (59,463
  samples at 5,105 stations over 15 years, though few features), risk 0.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 3 (the AI screening had `TBD -> Yes`, priority 3; zero-inflated screening
review page).

The workbook row is Lyashevska et al. (2016), a spatial zero-inflated Poisson model of the bivalve Macoma balthica in
the Dutch Wadden Sea. That paper released no table (its only supplement is a key-terms table), and its "3,451" is the
number of 2010 grid stations, not of counts. Its data come from SIBES, NIOZ's synoptic intertidal benthic survey,
which is public as a whole, so this record points there. Downloaded the SIBES release (18 MB) on 2026-10-19: 59,463
core samples from 2008-2022 at 5,105 stations (most sampled 13-15 years) and 171 taxa, with coordinates, grain size,
mud content, tidal basin, date and platform. The paper's use is predictive: "The model is used for prediction and
mapping the abundance of a benthic invertebrate" (Introduction), judged by leave-one-out cross-validation.

Zero mechanism, confirmed from the data: no Macoma in the core. Macoma (`sibes_id` 59) appears only as presence rows
in `biota.csv`, so the zeros come from filling against `samples.csv`: 56.2% overall, 42-72% by year. The paper's
Bernoulli/Poisson split is a model assumption. A quick LightGBM on log1p density: R^2 0.36 grouped by station
(presence AUC 0.81), 0.26 from sediment and date alone, 0.28 on 2021-22 as a temporal test. To check: whether a thin
feature set (coordinates, sediment, date) is wanted; the taxon (Macoma follows the paper); 769 samples without any
biota row (empty cores or missing records); sediment is missing in 3,687 samples, and the paper's elevation covariate
is not in the release. Licence: CC BY-SA 4.0; the latest three years are embargoed.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/wadden_sea_sibes_macoma_abundance/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping as changed after the panel: the sediment measured at the visit replaced by sediment interpolated from the year's other stations (USE-3, LEAK-10; its issue 5), the 342 samples of 2008 without a fauna record dropped, the 71 Tellinoidea samples dropped, and the use case reworded as an archive abundance map of a past survey. Corrections to the notes above: "so `year` stays empty" does not hold, PROV-9 gives 2024 (a field row in REVIEW.md waits for your mark); "ranks models as the paper's MSE" holds only by construction (V6 does not reproduce the paper's 2010 counts). Priority 3: gap 0, use case 0 (no actor named, fit approximate), source + (NIOZ SIBES), shape +, risk 0.

CC (2026-11-02, Andrej): metric (REVIEW.md issue 3, cross-dataset item zi-count-metric): `rmse` on the density kept; the Poisson deviance goes to nantucket_sound_sea_duck_aerial_survey_counts only.

**Assessment (AI, 2026-11-02):** applied; the fallback `rmse` stays, with a note in `curation_comments`. The fact that sets it apart from nantucket: Lyashevska et al. 2016 report several measures with no single criterion (MET-5), where nantucket's source names one likelihood. `mean_poisson_deviance` is now in the library if the family call is reopened.

CC (2026-11-02, Andrej): split (REVIEW.md issue 1, discuss): "Make sure there are no temporal or spatiotemporal leaks when using grouped". Leak test run; grouped by station stays.

CC (2026-11-02, Andrej): samples without a fauna record (issue 2, ok): as implemented, the 342 of 2008 dropped, the 427 of 2009-2022 kept as zeros.

CC (2026-11-02, Andrej): elevation (issue 4, change): "Join it if it is available." Joined from Rijkswaterstaat's vaklodingen (Deltares OpenEarth, no login).

CC (2026-11-02, Andrej): sediment (issue 5, ok): "My recommendation is to keep the interpolated sediment for this mapping task. It approximates information available at unsampled locations and preserves potentially useful habitat inputs." Kept as implemented.

CC (2026-11-02, Andrej): record field `year` set to the definition's 2024 (pinned snapshot, PROV-9).

**Assessment (AI, 2026-11-02):** marks applied. Leak test across the station-grouped split (untuned LightGBM, 3x3 shipped folds, R^2 0.376 on log1p): no test row has a feature copy in training; merging stations within 50/100/250 m into one group moves R^2 by +0.000/-0.002/-0.006; 6.8% of test rows have a same-year training sample within 100 m against 14.5% of map pixels; removing the test year's training rows costs R^2 0.085 against 0.002 for as many random rows (9 of 9), the same survey's other stations being the map's own input, not a leak; training only on years up to the test year scores 0.317 against 0.299 for as many random rows (later years add rows, not the outcome); no input is built from another row's outcome. Elevation (`elevation_m_nap`, latest vaklodingen survey of the station's 20 m cell on or before the sample's date) adds R^2 +0.033 (9 of 9 folds) and lowers RMSE on the density 872.8 to 863.9. Not forced, so no SPLIT-8 Cases entry. Needs a rebuild to ship.

CC (2026-11-03, Andrej): the check warning `task_target_value_dominant` accepted: "for these tasks this is natural and a core challenge" (zero-inflated target).

CC (2026-11-06, Lennart): decision D13 of the exposure study (#51; issue 6 of the folder's REVIEW.md): the 39 single boat cores (0.00866 m2, half the two-core boat sample; 20 in 2008, 9 in 2010, 10 in 2009-2019), which the data descriptor does not describe, stay with a note: 79.5% hold no tellin, against 57.4% for two-core boat samples and 60.6% at their stations' other visits, about what half the area gives by chance (77.8-82.0% for a random scatter); unusual, not wrong (CLEAN-11), 0.07% of the rows. The notes also name the effort the density folds in: the core area (CV 1.4% over the shipped rows) and a subsample correction whose fraction is chosen after the sample is seen and not released (9.55% of the positive counts per core are not whole numbers); the task scores the density unweighted with no sample weight (MET-15: an equal-area map). No earlier call covered these cores: the definition has kept them without a note since the review panel of 2026-11-01, which counted them and raised nothing; the exposure study of 2026-11-05 found that the descriptor does not describe them and measured their zeros.

**Assessment (AI, 2026-11-06):** review panel (focused, re-review under LEAK-41, MET-14 to MET-16): ship after changes, wording only, now made; disputed: the cause of the 608 positive counts below one tellin per core (issue 7: unknown, as the subsample correction can only raise a count; asking NIOZ is the curator's call) and MET-14's rebuild check, which has nothing to rebuild when no count is released (cross-dataset item X3); for the curator: issue 7. Corrections to the lines above: the elevation (Assessment of 2026-11-02) comes from the latest survey whose date stamp is on or before the sample's date, and the stamps are mostly a nominal 1 January, so 19.3% of the samples take a survey stamped 1 January of their own year (no leak under the archive-map moment); the non-whole counts per core (CC of 2026-11-06) include 608 below one that the core area and the subsample correction do not explain. The elevation join was fixed the same day: a pandas-3 run had left 40.66% of the rows without elevation, now 5 rows, the same under pandas 2.3 and 3.1.

CC (2026-11-08, Lennart): issue 7 of the folder's REVIEW.md, as implemented (ok): the note only. The 608 positive counts below one tellin per core ship as published, with the exposure note that their cause is unknown; NIOZ is not asked for now, and a question can go with a later version.

CC (2026-11-08, Lennart): the declared metric (`rmse`) is checked, as declared on the PR #47 review board.

## Reference

Lyashevska O., Brus D.J., van der Meer J. (2016). Mapping species abundance by a spatial zero-inflated Poisson model:
a case study in the Wadden Sea, the Netherlands. Ecology and Evolution 6:532-543. doi:10.1002/ece3.1880. SIBES:
Bijleveld A.I. et al. (2025), Scientific Data, doi:10.1038/s41597-025-04540-9; data doi:10.25850/nioz/7b.b.ug.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 20 (Wadden Sea Macoma abundance).
