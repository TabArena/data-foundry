---
unique_name: western_bluebird_nest_box_prospecting
name: Western bluebird nest-box prospecting, Napa vineyards (playback experiment)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Too Small
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
- https://doi.org/10.5281/zenodo.19428948
- https://digitalcommons.humboldt.edu/etd/2517
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `No` (`No Good Target / Scientific Discovery`, SEL-3, USE-2): a designed playback
experiment in 10 vineyards; the target counts prospecting visits at a box, and its zeros mostly sit at the silent
control boxes, a treatment the experimenter assigned.
- Source: Jomaa, "Use of public information for prospecting and nest site selection by Western Bluebirds (Sialia
  mexicana)", MSc thesis, Cal Poly Humboldt, 2025 (https://digitalcommons.humboldt.edu/etd/2517); data: Jomaa, Pham,
  MacDonald, Karp and Johnson, Zenodo doi:10.5281/zenodo.19428948 (5 Apr 2026, CC BY 4.0), with
  `Prospecting_and_Habitat.csv` (25 KB), `Overall_Box_Use.csv`, `WEBL_Boxes_Only.csv`, R code and a README. Measured
  by the earlier AI triage (2026-10-19): the prospecting table has 110 boxes x 44 columns; `Tot_prosp` has 18 zeros
  (16.4%): 12 of 30 control, 3 of 27 near-treatment and 3 of 53 treatment boxes.
- Deciding words: "I investigated the hypothesis that prospecting Western Bluebirds" "use post-breeding public
  information to select nest sites the following year"; "In late summer of 2023, I installed 200 nest boxes across 10
  vineyards without prior box history"; boxes within the other 5 vineyards "functioned as silent controls" (thesis
  abstract); visits were filmed during the playback sessions.
- Use case: none (USE-1, USE-2). The playback treatment is the experimenter's, and no one predicts prospecting visits
  at a box to decide anything; the source names no practitioner use, and playback had "no strong effect on nest box
  use" (thesis abstract, as quoted by the reject check). `Overall_Box_Use.csv` (2024 box use, with habitat) is only a
  lead for a box-placement task the source does not name.
- Consistency point for the curator: batch E1 wrote `pennsylvania_oak_hickory_regeneration_experiment` (a designed
  field experiment with measured columns beside assigned treatments) as `TBD -> 2nd Tier` after its reject was
  refuted, and its block asks that this record be decided the same way. What sets them apart: here the zeros sit at
  the silent controls the experimenter assigned and no practitioner prediction use exists, while Pennsylvania has a
  pre-treatment inventory (`COUNT14`, soil pH) of the kind foresters prescribe treatments from with SILVAH.
- Siblings and duplicates: none for the data; the designed experiments of batch E1 without such columns
  (`clarkia_greenhouse_reciprocal_transplant_fitness`, `treeline_seedling_emergence_experiment`,
  `vernal_pool_restoration_plant_cover`) were rejected. External collections: none found.
- Metric: none (no task).
- `Too Small` stays only as a provisional marker from the earlier pass: never measured on the task's splits (TP-5) and
  no part of the reason.
- Reject check (AI, 2026-10-27): stands. SEL-3 (Must). A designed manipulation: "I installed 200 nest boxes across 10
  vineyards without prior box history" and the boxes of the other 5 vineyards "functioned as silent controls", which
  hold 12 of the 18 zeros (https://digitalcommons.humboldt.edu/etd/2517).

CC (2026-10-30, Andrej): `No`, as screened (verified on the zero-inflated screening review page).

Nest-box prospecting by western bluebirds in 10 Napa vineyards (Jomaa et al., Cal Poly Humboldt; Zenodo data, an MSc
thesis, no journal article found). A designed playback experiment: per the thesis abstract, "In late summer of
2023, I installed 200 nest boxes across 10 vineyards", and treatment boxes "broadcast adult song and nestling
begging". Downloaded and measured on 2026-10-19: the prospecting table has 110 boxes x 44 columns; the target
`Tot_prosp` has 18 zeros (16.4%), median 24.5, maximum 968.

Zero mechanism, confirmed from the data: no prospecting seen in the video sessions, mostly at the silent control
boxes (12 of 30 controls, 3 of 27 near-treatment, 3 of 53 treatment boxes). That is a treatment effect within an
observation window, not "never-prospectable" boxes, and the code's zero-inflation term (`zi = ~ Box_treat`) is a
modelling choice; the workbook's "Core: Yes" and "explicit structural component" do not hold. Ten vineyards and 18
zeros leave a handful of independent units per fold. Data quirk: `Tot_M`, `Tot_F` and `Tot_J` mostly do not equal
the sums of their behaviour columns. Licence: CC BY 4.0.

## Reference

Jomaa F., Pham C., MacDonald E., Karp D., Johnson M. (2026). Data for: Western Bluebirds (Sialia mexicana) use
public information for prospecting but not ultimate nest site selection. Zenodo. doi:10.5281/zenodo.19428948.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 13 (Western bluebird prospecting).
