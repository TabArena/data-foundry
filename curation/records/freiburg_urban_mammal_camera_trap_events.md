---
unique_name: freiburg_urban_mammal_camera_trap_events
name: Freiburg urban wildlife camera traps / NocturnalNeigborsData (urban mammal capture events, 2022-2024)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 24 (Freiburg urban wildlife camera traps).
