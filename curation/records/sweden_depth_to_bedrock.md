---
unique_name: sweden_depth_to_bedrock
name: Sweden depth-to-bedrock (SGU observations, two-part model; Lin et al. 2026)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1111/ejss.70308
- https://github.com/linyq017/A-Two-Part-framework-for-Depth-to-Bedrock-Prediction-and-Uncertainty-Assessment-in-Sweden
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 2: a national depth-to-bedrock map from SGU observations,
with outcrops as true zeros, is a real mapping task, but only the code is public, and one feature (`HKDepth`) may be
an existing depth model of the same observations.
- Source: Lin, Peterson, Karlsson, Westphal, Lidberg and Ågren (2026), European Journal of Soil Science 77(2):e70308,
  open access CC BY 4.0 (SLU research portal). The full text was not read: Wiley returned 403 and SLU's PDF
  (https://research.slu.se/files/19040115/fulltext.pdf) sits behind a browser check, so a curator can open it. Abstract
  (SLU portal): the outcrop classifier reached "AUC = 0.96, F1-score = 0.83", and the fused model "outperformed both the
  existing national Inverse Distance Weighting interpolation model" and a global map. Code (GitHub, README and
  `config.py` read): training reads the authors' local fold files (`.../csvs/censored_encoded_folds/fold4_train.csv`);
  56 feature columns: coordinates `N` and `E`, LiDAR terrain derivatives, `HKDepth`, `LandAge`, soil-map one-hots
  (`jbas_merged_*`), tectonic zones (`tekt_n_*`), geomorphons and `DistanceToDeformation`. No data deposit found; the
  workbook's 1,199,920 observations are unverified.
- Target and zeros: DTB in m, 0 at outcrops (README: "Identifying bedrock outcrops (Depth = 0)"); the fold folder's
  name says some depths are censored (bedrock not reached).
- Use case: not read from the paper; for example SGU or a municipality reading depth to bedrock for groundwater,
  construction or forestry planning at a site without a borehole. Fit approximate. Regime grouped (spatial blocks), since
  a map serves places without a measurement (SPLIT-4); the code reads fold files whose design it does not state.
- Siblings and duplicates: `new_brunswick_depth_to_bedrock` (the same task in another country); soil-mapping
  precedents `lucas_topsoil` and `wosis_soil_profiles` (AI drafts). External collections: none found.
- Papers and pages: the paper (abstract only); the code repository.
- Metric: the code reports RMSE, bias, CCC and interval coverage by depth class (README: "Calculates depth-stratified
  metrics (RMSE, Bias, PICP)"), with no ranking criterion read: the fallback `rmse` (MET-5), to confirm in the paper.
- Risks for /add-dataset: `HKDepth` is not explained in the code; if it is SGU's interpolated soil-depth model built
  from the same observations, it leaks the target (LEAK); censored depths need a rule (the family's open policy
  question on coded and censored zeros); a rebuild joins SGU's observation archives (open data per the earlier triage)
  with 2 m LiDAR rasters; coordinates as features under a spatial split.
- Markers: `Not Available (from Paper))` dropped (the observations are SGU data and the authors' table was not asked
  for; a table on request is no reason for a marker, EV-4); `Needs extensive data wrangling` stays.
- Priority: gap 0, use case 0 (not read), source + (paper and code, SGU data), shape + (likely about a million points,
  56 features, spatial), risk - (`HKDepth` leak suspect, censored depths, heavy rebuild).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. The
censored depths (bedrock not reached) still need a cleaning rule at /add-dataset (drop them, or keep the recorded depth
with a flag column). The verdict and priority stay: the `HKDepth` leak suspect and the rebuild are the screening's other
risks. The family's question on species-abundance mapping is settled without a new rule (Andrej, 2026-10-30, policy
question 1 of the zero-inflated review: "I don't think there is new rule to build here. These are per dataset judgement
calls and if a dataset is useful for a predictive application although the data was collected for something else, then
this is fine"), as SEL-2 already reads the scope rules: this record is judged on its own use case. The verdict and
priority stay.

**Consistency check (AI, 2026-10-30):** the review page sets `Yes`, priority 2, while `new_brunswick_depth_to_bedrock`,
the same task in another country and also without a deposit, stays 2nd Tier, priority 2. Sweden also has the `HKDepth`
leak suspect and the censored depths. What may set it apart: the authors' code fixes the 56 features and SGU's
observation archives are open, so the rebuild is specified. Options: `Yes` with that fact (and New Brunswick stays 2nd
Tier), 2nd Tier for both, or raise New Brunswick too.

CC (2026-10-30, Andrej): `Yes`, priority 2 (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening
review page, after the AI's consistency check). "For bunswick the rebuild of the table is heavy"

**Assessment (AI, 2026-11-01):** /add-dataset stopped after the scaffold. The target is ready from SGU's open
Jorddjupsmodell (CC0, 2024: 1,204,670 bedrock-reached observations, 25.7% zeros, 0.4% more than the authors' 1,199,920),
but the authors' terrain features need Lantmaeteriet's 1 m elevation model, which must be ordered through Geotorget with
an account and a granted permission (about 1-2 TB nationally, days of flow routing, eleven indices without public
scripts): weeks of work and a manual order, heavier than New Brunswick's rebuild. Found on the way: `HKDepth` is
probably depth below the highest postglacial shoreline, not SGU's depth model (the authors' script drops that band), so
the leak suspicion likely does not hold; `jbas_merged_hall` is a leak suspect (outcrop polygons drawn from the
observations behind 203,486 zero targets); censored depths should be dropped. A lighter rebuild (open coarse DEM and SGU
vector layers, 1-2 days, fit approximate) or the authors' table would reopen it.

CC (2026-11-01, Andrej), by his rule in chat ("If you cannot find a source, it's 2nd tier") and his reason for New
Brunswick ("Rebuild is heavy"): `TBD -> 2nd Tier`, priority 2. The features have no source that can be had without a
manual order, and the rebuild is heavier than New Brunswick's.

A national depth-to-bedrock model for Sweden (Lin, Peterson, Karlsson, Westphal, Lidberg and Agren, SLU; EJSS 77,
e70308, 2026) with a two-part framework: per the abstract, outcrops "introduce 'structural zeros'", an outcrop
classifier reaches AUC 0.96 and the fused model R^2 0.67. Observations come from SGU databases (the well archive is
CC BY 4.0, SGU geological data are open since 2024). Only the code is public: its `config.py` reads the authors'
local files (`/workspace/data/soildepth/DepthData/csvs/censored_encoded_folds/fold4_train.csv`), and the feature list
holds coordinates, 2 m LiDAR terrain derivatives, `HKDepth`, land age, soil-map one-hots, tectonic zones,
geomorphons and distance to deformation zones. No data deposit was found; the workbook's 1,199,920 observations are
unverified. Only the abstract was read (Wiley and the SLU portal returned 403).

Zero mechanism, from the abstract only: outcrops, structural. Two things to check before any rebuild: what `HKDepth`
is (if it is an existing depth model such as SGU's interpolated soil-depth model, it leaks the target), and how
right-censored depths are coded (the folder name says "censored", i.e. bedrock not reached). Workbook pushback: the
"public multi-source dataset" is not public as a table. Also check the paper's data statement.

## Reference

Lin Y., Peterson G., Karlsson C., Westphal F., Lidberg W., Agren A. (2026). A Two-Part Framework for Depth to Bedrock
Prediction and Uncertainty Assessment in Sweden. European Journal of Soil Science 77:e70308. doi:10.1111/ejss.70308.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 2 (Sweden depth-to-bedrock).
