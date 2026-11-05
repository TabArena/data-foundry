---
unique_name: pennsylvania_oak_hickory_regeneration_experiment
name: Oak-hickory forest regeneration / deer fencing x lime x herbicide experiment, central Pennsylvania, 2014-2021
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- Too Small
- Not Representative
original_source: Other
year: '2024'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.z8w9ghxnk
- https://doi.org/10.1139/cjfr-2024-0034
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a 7-year factorial field experiment (deer fencing x
lime x herbicide, 24 sites x 11 microplots) whose release also holds pre-treatment measurements per microplot, so a
regeneration outcome predicted from the 2014 inventory is a possible task; small (24 sites) and borderline.
- Source: Begley-Miller et al. 2024 (Can. J. For. Res. 54:1367-1375); Dryad doi:10.5061/dryad.z8w9ghxnk (2024-09-25,
  CC0): `DataCJFR.csv`, 262 rows x 21 columns by its README (read by the reject check): `FENCE`, `LIME`, `HERB` beside
  the 2014 soil values `PH14` and `MN`, the pre-treatment laurel and competitor volumes `PRE_TRT_KALA_VOL` and
  `PRE_TRT_ALL_COMP_VOL`, `COUNT14`, `AGGHT14`, and the 2021 levels `COUNT21` and `AGGHT21`. Not downloaded (Dryad
  answers 401 to file requests).
- Use case: the authors tested the treatments ("The statistical analysis was not exploratory but tested the three
  treatments and interactions", Sec. 2.4, reproduced on Dryad), yet report that "At higher initial seedling abundance
  ... soil pH was an important predictor" (abstract). For example a forester who prescribes fencing or herbicide from a
  pre-treatment regeneration inventory, as SILVAH does (Brose et al. 2008, USFS Treesearch 18561); the source names no
  such actor, so the fit is approximate. Regime grouped by the 24 sites (SPLIT-3).
- Siblings and duplicates: none for the data. `western_bluebird_nest_box_prospecting` (batch E2) raises the same
  question (habitat columns beside an assigned treatment) and should be decided the same way. The batch's other designed
  experiments (`clarkia_greenhouse_reciprocal_transplant_fitness`, `treeline_seedling_emergence_experiment`,
  `vernal_pool_restoration_plant_cover`) have no such columns and were rejected. External collections: none found.
- Papers and pages: the paper's Sec. 2.1-2.4 as reproduced in the Dryad methods; Brose et al. 2008 for the practice.
- Metric: none for prediction (GLMMs ranked by AIC with likelihood-ratio tests, Sec. 2.4), so the fallback `rmse`.
- Risks for /add-dataset: (1) the prediction point is the 2014 pre-treatment inventory: target `COUNT21` or `AGGHT21`
  with the 2014 values as features, not the paper's change score (USE-5), and measure the zero share (a 0 in
  `COUNT21` is no seedling over 6 inches); (2) LEAK-10: drop `BA` (averaged over 2014-2021), `CANOPY` (2016, after the
  2015 herbicide) and `POST_TRT_KALA_VOL`; (3) grouped split by the 24 sites, TP-5 on those folds; (4) the fence is
  always microplot 5 and plots 1-4 are controls, so treatment and plot position go together; (5) decide together with
  `western_bluebird_nest_box_prospecting`. `No Good Target / Scientific Discovery` stays as the marker of the concern.
- Priority: gap 0 (biology, regression and grouped are not thin), use case 0 (an example, not named by the source),
  source + (paper and a documented CC0 deposit), shape 0 (262 rows, 24 sites), risk - (leaky columns, target choice,
  24 sites).
- Reject check (AI, 2026-10-27): does not stand. The release holds measured pre-treatment covariates beside the
  treatments (README of `DataCJFR.csv`), and foresters prescribe these treatments from a pre-treatment inventory
  (SILVAH), so "no decision fits" is a reading and not the source's words.

**Assessment (AI, 2026-10-30):** to the curator's question ("How many samples are there per site?"): about 11. The
release's README gives 262 rows for 24 sites x 11 microplots (264, so two are missing); the file itself was not
downloaded (Dryad answers 401). A split grouped by site has 24 independent units, about 5 sites (55 rows) per test fold
in 5 folds; microplots of one site share soil, canopy and deer pressure, so a split by microplot would leak the site. On
the same page `south_nation_riparian_birds_insect_emergence` (24 sites) was confirmed `No` with `Too Small` (TP-5), so
the same call would follow here unless the curator accepts 24 sites.

CC (2026-10-30, Andrej): `Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening
review page, after the AI's answer to the curator's question). "LGTM"

A factorial field experiment on tree regeneration (Begley-Miller et al. 2024): 24 sites x 11 microplots (7
combinations of deer fencing, lime and herbicide plus 4 controls), about 264 rows (`DataCJFR.csv`, 30 KB; not
downloaded, Dryad blocks automated downloads). Sec. 2.4 (reproduced on Dryad): "The statistical analysis was not
exploratory but tested the three treatments and interactions." The response is "the change between 2014 and 2021" in
seedling count or aggregate height.

Zero mechanism, not confirmed: the target is a change score that can be negative, so a 0 is no net change (for
example no seedlings in either year), not a structural zero. Workbook pushback: "No regeneration -> 0" misreads a
difference target, and the source states it is a designed test of treatments. Licence: CC0.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/pennsylvania_oak_hickory_regeneration_experiment/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping as defined: the 2021 count of seedlings of all tree species from the 2014 inventory and the planned treatment, whole sites held out. Superseding readings above: the Dryad version download works without a token (SHA-256 matches; 261 microplots, 28 columns), not "Dryad answers 401" / "262 rows x 21 columns"; the splits are 3 folds of 8 sites (85-88 rows), not 5 folds; south_nation's recorded reason was "No good target", not `Too Small`; the change-score paragraph no longer applies (the target is the 2021 level). `Two-Regime Zeros` removed under your definition of 2026-10-30 (48 zeros against 38 ones; the zeros follow the 2014 count). Domoto's initials corrected to E.J. (Crossref). The marker stays until your mark on issue 1. Priority 2: gap 0, use case 0, source + (CC0 deposit and a paper), shape 0 (261 rows), risk 0.

CC (2026-11-02, Andrej): metric (REVIEW.md issue 4, cross-dataset item zi-count-metric): `rmse` on the seedling count kept, neither RMSLE nor the Poisson deviance.

**Assessment (AI, 2026-11-02):** applied; the fallback `rmse` stays, with a note in `curation_comments`. The source's AIC stays read as an in-sample model choice, so the origin stays fallback, not a stand-in for a likelihood as at nantucket_sound_sea_duck_aerial_survey_counts.

CC (2026-11-03, Andrej): `Yes` on the reworded use case, and the `No Good Target / Scientific Discovery` marker is removed (issue 1 (B) in pennsylvania_oak_hickory_regeneration_experiment): "I go with your suggestion".

CC (2026-11-03, Andrej): issue 2, B: site folds stratified by state forest, tagged `ForcedGroupedFromTemporal` (training and test share the 2014-2021 years). Issue 3 asked whether scoring the same forests on the same dates leaks; answered on the review page.

CC (2026-11-03, Andrej): `No` (`Too Small`, `Not Representative`): "Since it is both too small and not representative, I lean towards rejecting it now." 24 sites in two forests and one 2014-2021 cohort: training and test share the years' weather, deer and seed crops, so the score cannot test the forester's forecast of a later cohort. The v2 folder left the working copy; its last definition (with the forest-stratified split of today) is in the run folder of 2026-11-03, the committed one in 902011b3.

## Reference

Begley-Miller D.R., Diefenbach D.R., Domoto E.J., et al. (2024). Complex interactions of deer herbivory, soil
chemistry, and competing vegetation explain oak-hickory forest tree regeneration in central Pennsylvania, USA.
Canadian Journal of Forest Research 54:1367-1375. doi:10.1139/cjfr-2024-0034. Data: doi:10.5061/dryad.z8w9ghxnk.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 42 (Oak-hickory forest regeneration).
