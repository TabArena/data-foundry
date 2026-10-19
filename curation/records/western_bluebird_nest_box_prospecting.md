---
unique_name: western_bluebird_nest_box_prospecting
name: Western bluebird nest-box prospecting, Napa vineyards (playback experiment)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Too Small
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
- https://doi.org/10.5281/zenodo.19428948
- https://digitalcommons.humboldt.edu/etd/2517
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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
