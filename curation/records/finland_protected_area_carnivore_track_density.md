---
unique_name: finland_protected_area_carnivore_track_density
name: Finnish large-carnivore FWTS / matched protected-area and control track densities, 1989-2017 (Terraube et al. 2020)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2020'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.s1rn8pk4w
- https://doi.org/10.1038/s41467-020-16792-7
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Finnish Wildlife Triangle Scheme track indices for lynx, wolf, wolverine (winter) and brown bear (late summer) in 12
km triangles inside protected areas and matched controls (Terraube et al. 2020; paper read via PMC7289803). A row is
a triangle x year x species; the target is crossings per 24 h per 10 km; features are forest cover, ruggedness,
distance to settlements, human density, coordinates, year and protection status. The design is causal: "we assess
the effectiveness of Finland's PA network in supporting abundances of four large carnivore species" (Introduction),
measured as "the difference between densities in a unit located inside a PA and its matched control unit" (Methods),
after "one-to-one, nearest-neighbor covariate matching with replacement", so controls repeat. Files of 2.2-2.3 MB;
not downloaded (Dryad blocks automated downloads).

Zero mechanism, from the paper only: no fresh tracks in the 24-hour window; the paper notes "zero inflation of all
time-series" (Methods). Workbook pushback: the 1,220 are matched units, not rows (the paper counts 3,111 unit-years
for 563 pairs), and a treatment-effect design is not a prediction task. A carnivore-track task would need the full
FWTS series rather than this matched subset. Licence: CC0.

## Reference

Terraube J., Van doninck J., Helle P., Cabeza M. (2020). Assessing the effectiveness of a national protected area
network for carnivore conservation. Nature Communications 11. doi:10.1038/s41467-020-16792-7. Data:
doi:10.5061/dryad.s1rn8pk4w.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 60 (Finnish large-carnivore FWTS).
