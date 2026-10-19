---
unique_name: morocco_forest_bird_transect_counts
name: Palaearctic rear-edge forest birds / Moroccan forest-bird transect counts (Telleria et al. 2021)
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
- '?'
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.5061/dryad.34tmpg4kh
- https://doi.org/10.5281/zenodo.5011952
- https://doi.org/10.1111/jbi.14219
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Line-transect counts of 11 forest passerines in Morocco with local habitat covers, plus a presence-only occurrence
file for Maxent models (Telleria, Hernandez-Lambrano and Carbonell 2021). Dryad methods: "We counted all birds within
a belt 500 m long and 25 + 25 m wide", with grass, shrub and tree cover assessed at two points per transect. The
study tests the centre-periphery hypothesis (abstract: "we explore if habitat suitability decreases southwards"),
with Maxent habitat suitability, a model output, as the key predictor. `Transects.csv` is 11 KB, roughly 100-200
transects (estimate; not downloaded, Dryad blocks automated downloads).

Zero mechanism, from the Dryad text only: a species not counted on a transect; absence and non-detection are not
separated, and the occurrence file is presence-only, so it adds no absences. A biogeographic hypothesis test on a
small table rather than a count-regression task. Paper not read (Wiley 403). Licence: CC0.

## Reference

Telleria J.L., Hernandez-Lambrano R., Carbonell R. (2021). Ecological and geographical marginality in rear edge
populations of Palaearctic forest birds. Journal of Biogeography 48:2538-2549. doi:10.1111/jbi.14219. Data:
doi:10.5061/dryad.34tmpg4kh.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 34 (Palaearctic rear-edge forest birds).
