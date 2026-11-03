---
unique_name: plains_wanderer_spotlight_counts
name: Plains-wanderer abundance / spotlight surveys at 16 grassland sites, 2014-2022
checked_by:
- Andrej
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
- Too Small
tags:
- Two-Regime Zeros
original_source: Other
year: '2024'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5061/dryad.t1g1jwtb9
- https://doi.org/10.1002/eap.3046
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: spotlight counts of the endangered plains-wanderer from
a regional monitoring program (16 sites, 249 surveys, 41 with birds) with grass height and fox presence, published as
an explanatory study; a multi-site survey with habitat covariates, so the family's open species-abundance question
decides it.
- Source: Parker, Cameron, Gordon and Letnic 2024, "Habitat structure and an introduced predator limit the abundance
  of an endangered ground-nesting bird", Ecological Applications 34:e3046 (doi:10.1002/eap.3046; read through
  PMC11610650); Dryad doi:10.5061/dryad.t1g1jwtb9 (CC0), one 32 KB xlsx, not downloaded. As published: "Field surveys
  were conducted at 16 sites between October 2014 and September 2022, distributed across the region", part of a
  "long-term monitoring program" on pastoral land, national parks and travelling stock routes (Methods, as quoted by
  the reject check); "giving a total of 249 surveys"; predictors mean maximum grass height, fox presence and location;
  birds on about 16% of transects, so 41 positive surveys (Methods).
- Aim, in the source's words: "The aim of this study was to investigate the impact of grassland structure and fox
  numbers on plains-wanderer abundance" (Introduction, last paragraph).
- Use case: none named for a prediction; managers act on the finding ("plains-wanderers should benefit from management
  strategies that maintain grass height at optimal levels", Abstract; fox suppression, Discussion). For example a land
  manager estimating the birds' abundance on a paddock from grass height and fox activity before setting grazing; fit
  approximate (a use case the curation wrote). Regime grouped by site (SPLIT-3).
- Zeros: no bird inside the effective strip; the authors argue the absences "were predominantly true zeroes" (earlier
  AI triage, read in the paper).
- Siblings and duplicates: none in the log; `la_paz_shorebird_abundance_disturbance` (`No` in this pass) is set apart
  as a single-site effect study. Family records on the same open question: `great_lakes_marsh_bird_point_counts`,
  `morocco_forest_bird_transect_counts`. External collections: none found.
- Metric: none for a prediction (the paper fits explanatory models of occurrence and abundance), so the fallback `rmse`.
- Risks for /add-dataset: the xlsx's columns and rows; whether fox presence comes from the same spotlight survey as
  the bird count (name the prediction point, USE-3); sites "located based on the presence of suitable grassland
  habitat" (as quoted by the reject check; a possible `Not Representative`); TP-5 on a split grouped by site (16
  sites, 41 positive surveys; `Too Small` stays a provisional marker, unmeasured); task probes, as the paper reports
  "the poor predictive power of the continuous models" (as quoted by the reject check); the open species-abundance
  question (triage summary, "Policy questions"; SEL-3, USE-1).
- Priority: gap 0 (biology & life sciences 4; regression and grouped not thin), use case 0 (none named), source +
  (paper, Dryad), shape 0 (249 surveys at 16 sites, three predictors), risk - (16 groups and 41 positives, TP-5).
- Reject check (AI, 2026-10-27): does not stand. Sixteen sites "distributed across the region" in a long-term
  monitoring program, with grass height and fox presence recorded at each survey, make a multi-site observational
  survey with habitat covariates, neither a designed experiment nor a single site; what is left is size and
  representativeness, not SEL-3.

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening review page).
No reason was given on the page; the record's markers (`No Good Target / Scientific Discovery`, `Too Small`) stand as
the reason.

Spotlight counts of the endangered plains-wanderer (Parker et al. 2024, UNSW; paper read via PMC11610650). Methods:
"Field surveys were conducted at 16 sites", one to three times a year, "giving a total of 249 surveys" (2014-2022),
with grass height, fox presence and location as predictors. The aim is explanatory ("The aim of this study was to
investigate the impact of grassland structure and fox numbers on plains-wanderer abundance", Introduction), and both
predictors came out non-significant. One 32 KB xlsx; not downloaded (Dryad blocks automated downloads).

Zero mechanism, from the paper only: no bird inside the 5.2 m effective strip. Birds were seen on 16.45% of surveys,
i.e. 41 positive surveys and about 84% zeros, and the authors argue the zeros are real ("we are confident that
absences were predominantly true zeroes because we restricted our analyses to observations within the effective
strip"). Workbook pushback: the 249 "transects" are repeat visits to 16 sites, so a grouped split leaves a handful of
sites and positives per fold. Licence: CC0.

## Reference

Parker D., Cameron M., Gordon C., Letnic M. (2024). Habitat structure and an introduced predator limit the abundance
of an endangered ground-nesting bird. Ecological Applications 34:e3046. doi:10.1002/eap.3046. Data:
doi:10.5061/dryad.t1g1jwtb9.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 16 (Plains-wanderer abundance).
