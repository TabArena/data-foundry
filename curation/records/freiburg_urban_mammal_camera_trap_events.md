---
unique_name: freiburg_urban_mammal_camera_trap_events
name: Freiburg urban wildlife camera traps / NocturnalNeigborsData (urban mammal capture events, 2022-2024)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target (yet)
- Needs extensive data wrangling
tags:
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.73n5tb3bz
- https://doi.org/10.1002/wlb3.01522
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: a detection log of 24 urban camera traps in Freiburg (10
mammal species, 2022-2024) with one habitat covariate, released for analyses of activity and habitat use; there is no
target yet, and a count per camera, season and species would be ours.
- Source: Moesch, Sultana, Peerenboom and Storch, "Nocturnal neighbors: exploring residents' perceptions of urban
  wildlife related to animal traits identified by camera traps and literature", Wildlife Biology 2026,
  doi:10.1002/wlb3.01522 (read from the KIT open-access PDF); data on Dryad, doi:10.5061/dryad.73n5tb3bz (2026-02-07,
  CC0): `NocturnalNeigborsData.xlsx` and a README only. As published (README): "Each row represents one independent
  capture event", 27 columns: camera id, image path, species and individuals (two species slots), date and time fields,
  `Season`, `Year`, `SeasonYear`, day or night, `avg_impervious` per camera (the only habitat covariate, no
  coordinates), `ID_freq`, `MaxDays` (per camera) and `Adjusted_Frequency`. Not downloaded (Dryad answers 401); about
  6,884 rows by the paper's per-species counts (earlier AI triage, 2026-10-19).
- Use case: none stated. The paper models residents' acceptance ("acceptance was the response variable", Statistical
  analysis), with traits "derived from the camera trap data"; the survey of 779 residents is not released. The data's
  own aim (README): "The survey was designed to capture variation in diel activity and habitat use of mammal species in
  urban environments". For example a city's wildlife office estimating a species' activity at a site from its
  imperviousness; the source does not make it. Fit none so far. Regime grouped by camera for unseen sites, or temporal
  for known cameras.
- Doubt: this screening first proposed `No` (SEL-3); the reject check refuted it (below). The earlier marker `No Good
  Target / Scientific Discovery` is replaced by `No Good Target (yet)`, as for
  `wildlife_insights_camera_trap_detections`: no task yet, and habitat use falls under the open
  species-abundance-mapping question (settled by Andrej on 2026-10-30, policy question 1 of the zero-inflated review: no
  new rule, each survey judged on its own use case).
- Siblings and duplicates: the other camera-trap records (`southeast_asia_predator_prey_camera_trap_counts` 2nd Tier,
  `wildlife_insights_camera_trap_detections` 2nd Tier, `iwildcam_2020_camera_trap_species` No) hold other data. External
  collections: none found.
- Papers and pages: the paper (KIT PDF); the Dryad README.
- Metric: none (the paper fits a linear mixed model and tests significance); fallback `rmse` once a count target exists.
- Risks for /add-dataset: (1) download the xlsx by hand (Dryad answers 401 to scripts); (2) build counts per camera,
  `SeasonYear` and species with the per-session deployment from the paper, so that a zero is an observed absence and not
  a camera that was off (`MaxDays` is per camera only); (3) drop `ID_freq` and `Adjusted_Frequency`, computed from the
  detections themselves (LEAK-10); (4) for unseen cameras, 24 cameras with one covariate call for TP-5 and SPLIT-28
  (several model families against the mean); for known cameras, the TP-10 naive-profile test; (5) wait for the curator's
  answer on the open species-abundance question.
- Priority: gap 0, use case 0, source + (paper, README), shape 0 (24 cameras, one covariate), risk - (the target must be
  built).
- Reject check (AI, 2026-10-27): does not stand. The README states a descriptive aim but no failing Must: the release
  has no target yet, as `wildlife_insights_camera_trap_detections`, habitat use is the open question's subject, and the
  thin shape is a value fact for the add stage, not a SEL-3 failure in the source's words.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page).
No reason was given on the page; the record's markers (`No Good Target (yet)`, `Needs extensive data wrangling`) stand
as the reason.

Camera-trap capture events of 10 mammal species at 24 urban sites in Freiburg, 2022-2024, four seasonal sessions a
year (Moesch et al. 2026; paper read from the KITopen copy). One row is one independent capture event (5-minute
rule); the columns are species, individuals, date and time fields, season, year, day or night, and `avg_impervious`
as the only site covariate, plus `ID_freq` and `Adjusted_Frequency` computed from the detections. About 6,884 rows by
the paper's per-species event counts (p. 8); not downloaded (Dryad blocks automated downloads). The paper's response
is residents' acceptance of the animals from a survey that is not released; the camera data only supply species
traits (Introduction, p. 2: "we built a model to assess which of four animal traits ... are most important for the
acceptance of the animal's presence in the immediate neighborhood").

Zero mechanism: none in the file, since every row is a detection with at least one individual. Zeros would appear
only after aggregating to site x session x species, and `ID_freq` and `Adjusted_Frequency` would then leak the count.
Workbook pushback: "No detections -> 0" does not hold for the released table. Licence: CC0.

## Reference

Moesch S.S., Sultana M., Peerenboom G., Storch I. (2026). Nocturnal neighbors: exploring residents' perceptions of
urban wildlife related to animal traits identified by camera traps and literature. Wildlife Biology.
doi:10.1002/wlb3.01522. Data: doi:10.5061/dryad.73n5tb3bz.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 24 (Freiburg urban wildlife camera traps).
