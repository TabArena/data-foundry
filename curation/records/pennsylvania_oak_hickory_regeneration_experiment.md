---
unique_name: pennsylvania_oak_hickory_regeneration_experiment
name: Oak-hickory forest regeneration / deer fencing x lime x herbicide experiment, central Pennsylvania, 2014-2021
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

A factorial field experiment on tree regeneration (Begley-Miller et al. 2024): 24 sites x 11 microplots (7
combinations of deer fencing, lime and herbicide plus 4 controls), about 264 rows (`DataCJFR.csv`, 30 KB; not
downloaded, Dryad blocks automated downloads). Sec. 2.4 (reproduced on Dryad): "The statistical analysis was not
exploratory but tested the three treatments and interactions." The response is "the change between 2014 and 2021" in
seedling count or aggregate height.

Zero mechanism, not confirmed: the target is a change score that can be negative, so a 0 is no net change (for
example no seedlings in either year), not a structural zero. Workbook pushback: "No regeneration -> 0" misreads a
difference target, and the source states it is a designed test of treatments. Licence: CC0.

## Reference

Begley-Miller D.R., Diefenbach D.R., Domoto M.E., et al. (2024). Complex interactions of deer herbivory, soil
chemistry, and competing vegetation explain oak-hickory forest tree regeneration in central Pennsylvania, USA.
Canadian Journal of Forest Research 54:1367-1375. doi:10.1139/cjfr-2024-0034. Data: doi:10.5061/dryad.z8w9ghxnk.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 42 (Oak-hickory forest regeneration).
