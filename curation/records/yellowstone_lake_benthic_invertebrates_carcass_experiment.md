---
unique_name: yellowstone_lake_benthic_invertebrates_carcass_experiment
name: Fish carcass / Yellowstone Lake benthic invertebrates (lake trout carcass treatment, BACI experiment)
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
year: '2022'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.c866t1g9m
- https://doi.org/10.1002/aff2.72
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Benthic invertebrate density and biomass around lake trout carcass deposits in Yellowstone Lake (Briggs et al. 2022).
A before-after-control-impact experiment at 4 sites (2 carcass, 2 control), triplicate samples on 3 monthly
pre-treatment and 4 biweekly post-treatment dates, about 84 samples by taxa (Dryad methods; files of 23-29 KB, not
downloaded because Dryad blocks automated downloads). Data analysis: "To determine if invertebrate density and
biomass changed in response to carcass treatment, we assessed the interaction between time ... and treatment", in
what the authors call "a large-scale experiment with low replication".

Zero mechanism, from the paper only: a taxon absent from a 0.25 m2 suction sample; zero-inflated models were used
for EPT and Sphaeriidae because they "had many zeros". Workbook pushback: it is a manipulated experiment, not
observational data, with 4 independent sites. Licence: CC0.

## Reference

Briggs M.A., Albertson L.K., Lujan D.R., Tronstad L.M., Glassic H.C., Guy C.S., Koel T.M. (2022). Fish carcass
deposition to suppress invasive lake trout through hypoxia causes limited, non-target effects on benthic
invertebrates in Yellowstone Lake. Aquaculture, Fish and Fisheries 2:470-483. doi:10.1002/aff2.72. Data:
doi:10.5061/dryad.c866t1g9m.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 39 (Fish carcass / Yellowstone Lake benthic
invertebrates).
