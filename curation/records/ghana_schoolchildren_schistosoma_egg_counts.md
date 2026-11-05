---
unique_name: ghana_schoolchildren_schistosoma_egg_counts
name: Ghana schistosomiasis egg counts / schoolchildren of southern Ghana (Nketia and de Souza 2024)
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Too Small
tags:
- Two-Regime Zeros
original_source: Github
year: '2024'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- '# First publication: the authors'' GitHub repository (data first committed 2023-11-16)'
- https://github.com/kojonketia/Using-hurdle-models-to-analyze-schistosomiasis-count-data
- '# The paper (PLOS ONE 2024)'
- https://doi.org/10.1371/journal.pone.0304681
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: Schistosoma egg counts of 1,345 Ghanaian schoolchildren
from a count-model comparison, with 80 positive children in 12 communities and a target that adds two species counted in
different samples; the earlier `No` rests on readings, so it is no fast reject.
- Source: Nketia and de Souza (2024), PLOS ONE 19:e0304681 (published 2024-07-12), a "secondary analysis of
  de-identified data collected within a larger epidemiological study on allergy and parasitic infections ('GLOFAL
  GHANA')" (Materials and methods). The rows were first shared in the authors' GitHub repository on 2023-11-16
  (`Schistosomiasis_count_data.xlsx`; `Dataset.xlsx` with grouped columns added 2024-04-03), so by PROV-9 the year is
  2023, not the record's 2024. As published (README): Age, Sex, Class, Community, S_haematobium, S_mansoni,
  Parent_Occupation, five water-source flags, Age_group, EduLevel, Area and schistosomiasis (the sum). Earlier AI
  triage, 2026-10-19, measured 1,345 rows x 16 columns, 94.05% zeros (80 positive children, median 8 eggs, maximum 296),
  54 of the positives in 3 communities, none in 4 urban schools, and 307 exact duplicate rows.
- Ethics (SEL-1): the paper's statement is "Not applicable. This is a secondary analysis of previously collected data.
  All data was de-identified prior to receipt from the original study investigators." For the original study, Aryeetey
  et al. (2013, AJTMH 88(6):1028-31, Methods) write that GLOFAL GHANA was "approved by the Institutional Review Board of
  the NMIMR, Accra, Ghana" and "A written informed consent was received from parents or guardian of each child." Neither
  says whether the consent covers a public release or later use; nobody asks that the data not be used for ML, so SEL-1
  holds on what the sources state. The repository has no licence, and the rows keep age, class, community and parent
  occupation of children in 12 communities: for the curator to weigh.
- Use case: none in the source: "the purpose of this analysis is to apply statistical models to the count data and
  evaluate their performance and results" (Abstract). For example a school health programme deciding which children to
  test; control usually treats whole communities by prevalence, so a per-child model has no clear actor, and the fit is
  approximate at best. Regime: grouped by community for new communities, or IID for new children of surveyed schools; no
  dates.
- Doubt: the earlier pass set `No` (`No Good Target / Scientific Discovery`, `Too Small`). Both need a reading: that no
  decision fits a per-child prediction (SEL-2, SEL-3), and that the split leaves a handful of positives per fold (TP-5:
  about 16 per fold under five random folds, fewer and uneven by community). The markers stay as the concerns to settle.
- Siblings and duplicates: none for these children (searched schistosom, Ghana); `outsmarting_outbreaks_challenge` (TBD
  -> 2nd Tier) counts schistosomiasis cases per Tanzanian hospital-month, another task. External collections: none
  found.
- Papers and pages: the paper above (read via PMC11244785: Abstract, Materials and methods, Ethics statement, Table 2);
  the original study's papers, Obeng et al. 2008 (Ann Trop Med Parasitol 102(7):625-33) and Aryeetey et al. 2013 (read
  on PMC3752797).
- Metric: AIC and BIC over six count models, two predictor sets and two intensity subsets (Materials and methods; Table
  2), plus rootograms; no held-out score, so the fallback `rmse` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: the target adds S. haematobium, counted in urine (eggs per 10 mL in the original study), and
  S. mansoni from stool, while the paper reports "egg per gram": the unit is unclear (USE-5; ship one species or the
  infection flag); drop both species columns, which sum to the target (LEAK-10); check the 307 duplicate rows. A single
  urine sample misses light infections (Aryeetey et al. 2013 found Schistosoma DNA in 102 of 673 microscopy-negative
  samples), so some zeros are false negatives: the coded and censored zeros policy question.
- Priority: gap 0 (medical and regression are not thin), use case 0 (none in the source), source + (the paper and the
  repository's README document the columns), shape 0 (1,345 children, 15 columns, but 80 positives in 12 communities),
  risk - (unclear target unit, few positives per community).

**Assessment (AI, 2026-10-30):** The family's open question on coded and censored zeros is settled (Andrej, 2026-10-30,
policy question 2 of the zero-inflated review: "We don't care. We want to add any relevant predictive task, independent
if it is zero inflated or not"), so how the source codes its zeros is no reason for a No or a lower priority. Zero egg
counts that may be false negatives stay as recorded. The verdict and priority stay on the screening's other points.

**Consistency check (AI, 2026-10-30):** the review page sets `Yes`, priority 1. The record carries `Too Small` and `No
Good Target / Scientific Discovery`: 80 children with eggs in 12 communities, 54 of them in 3, about 16 positives per
test fold, and a source that compares count models. `plains_wanderer_spotlight_counts` (41 positives at 16 sites, the
same markers) was set `No` on the same page. What sets ghana apart? If nothing: `No` like plains_wanderer, or 2nd Tier.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page,
after the AI's consistency check). The record's markers (`No Good Target / Scientific Discovery`, `Too Small`) stand as
the reason, as for plains_wanderer_spotlight_counts.

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

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 57 (Ghana schistosomiasis egg counts).
