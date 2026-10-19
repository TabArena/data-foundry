---
unique_name: boreal_postfire_lichen_biomass
name: Terrestrial lichen - Northwest Territories / Terrestrial lichen - Saskatchewan (post-fire forage-lichen biomass, Greuel et al. 2021)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Other
year: '2021'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.t1g1jwt15
- https://doi.org/10.5061/dryad.tb2rbnzzj
- https://doi.org/10.1002/ecs2.3481
- https://doi.org/10.5061/dryad.76hdr7sth
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Workbook rows 37 and 38 are one study (Greuel et al. 2021, one paper, overlapping authors) released as two regional
Dryad deposits with different field protocols, so they share this record. Northwest Territories: "346 plots were
established with 5, 1 by 1 m quadrats within predetermined burn age classes (37-38 and 46-49 years post-fire) and ...
'control' (>70 years)". Saskatchewan: "221 plots were established with 2, 2 by 2 m quadrats within three age
categories". About 1,730 and 440 quadrat rows by estimate; not downloaded (Dryad blocks automated downloads).

The study is a fire-recovery chronosequence: the abstract's hurdle GLM "identified stand age, stand type and
ecoprovince as significant predictors of lichen presence", inference on three design variables with no remote-sensing
covariates, mapping or validation mentioned. Biomass is itself estimated: "allometric equations to estimate lichen
biomass from field measurements of lichen cover and height", so cover and height would be the target's own inputs.
Zero mechanism, from the abstract only: no forage lichen in the quadrat, hence allometric biomass 0. Workbook
pushback: "Verified strict match" and "Core: Yes" rest on the hurdle model, which is inference, not a prediction task.
Paper text not read (Wiley 403). Licence: CC0.

## Reference

Greuel R.J., Degre-Timmons G.E., Baltzer J.L., Johnstone J.F., et al. (2021). Predicting patterns of terrestrial
lichen biomass recovery following boreal wildfires. Ecosphere 12:e03481. doi:10.1002/ecs2.3481. Data:
doi:10.5061/dryad.t1g1jwt15 (Northwest Territories), doi:10.5061/dryad.tb2rbnzzj (Saskatchewan).

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master rows 37 (Terrestrial lichen - Northwest
Territories) and 38 (Terrestrial lichen - Saskatchewan).
