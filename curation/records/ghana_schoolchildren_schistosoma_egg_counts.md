---
unique_name: ghana_schoolchildren_schistosoma_egg_counts
name: Ghana schistosomiasis egg counts / schoolchildren of southern Ghana (Nketia and de Souza 2024)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target  / Scientific Discovery
- Too Small
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
original_source: Github
year: '2024'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/kojonketia/Using-hurdle-models-to-analyze-schistosomiasis-count-data
- https://doi.org/10.1371/journal.pone.0304681
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

Schistosoma egg counts of schoolchildren from a secondary analysis comparing count models (Nketia and de Souza 2024;
paper read via PMC11244785). Methods: "secondary analysis of de-identified data collected within a larger
epidemiological study"; the aim is "to assess the performance of the statistical models Poisson, NB" and their
zero-inflated and hurdle versions by AIC and BIC. Downloaded the repository's `Dataset.xlsx` on 2026-10-19: 1,345
children x 16 columns (age, sex, class, community, parent occupation, five water-source flags); the target sums
`S_haematobium` and `S_mansoni`, which must be dropped; no dates; 307 rows are exact duplicates.

Zero mechanism: no eggs detected, from an uninfected child or a single sample that missed an infection, which the
data cannot separate; 94.05% zeros measured, i.e. 80 positive children (median 8 eggs, maximum 296) in 12
communities, 3 of which hold 54 of the positives and 4 urban schools none. Grouped by community, that is a handful of
positives per fold. The unit is also unclear: the paper says "egg per gram" while S. haematobium is counted in urine.
No licence file in the repository.

## Reference

Nketia K., de Souza D.K. (2024). Using zero-inflated and hurdle regression models to analyze schistosomiasis data of
school children in the southern areas of Ghana. PLOS ONE 19:e0304681. doi:10.1371/journal.pone.0304681.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 57 (Ghana schistosomiasis egg counts).
