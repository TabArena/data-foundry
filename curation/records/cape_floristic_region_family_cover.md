---
unique_name: cape_floristic_region_family_cover
name: Cape Floristic Region plant-family cover (ZIB_data, Crassulaceae and Restionaceae)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 1
decision_markers:
- Data Quality Issue
tags:
- Two-Regime Zeros
- Tiny Data
original_source: Github
year: '2021'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://raw.githubusercontent.com/beckytang/ZIB_data/main/cfr_zib_data.csv
- https://github.com/beckytang/ZIB_data
- https://doi.org/10.1007/s13253-022-00516-z
- https://arxiv.org/abs/2112.07249
- https://github.com/beckytang/ZIB_data/tree/97da77c9c87434e85bba0e081fa27b148a2df9a9
v2_path: datasets/_dev/tabarena-v0pt2/cape_floristic_region_family_cover/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: 180 relevé plots with four climate covariates, the
example data of a zero-inflated beta methods paper that frames prediction to unobserved sites (the family's open
species-abundance question); a tiny table, and the Restionaceae cover sits at a cap of 0.99 in 79 plots.
- Source: Tang, Frye, Gelfand and Silander (JABES 28:117-137, 2023; arXiv:2112.07249v2 read), data in the first
  author's GitHub repository `beckytang/ZIB_data` (no licence file). Sec. 2: "Our data were collected between 2010 and
  2011 from plots concentrated in two regions of South Africa: 61 plots in the Cape Point section of Table Mountain
  National Park and 119 plots in the Baviaanskloof Mega-Reserve", 10 x 5 m relevés. As published (earlier AI triage,
  2026-10-19, measured): 180 rows x 10 columns (plot, lat, lon, region, two family covers, four climate covariates),
  150 distinct covariate tuples; zeros 48.9% (Crassulaceae) and 30.6% (Restionaceae).
- Use case: the spatial models "enable prediction to unobserved sites with known environmental attributes" (Sec. 6);
  for example a conservation planner estimating family cover at sites not surveyed. No actor or decision named, fit
  approximate. Regime: the paper scores random splits ("a training set of 99 locations and a test set of 20
  locations", Sec. 5.3), while prediction to new sites argues for spatial blocks; there are only two regions.
- Siblings and duplicates: none among the records (searched for Cape Floristic, ZIB_data, zero-inflated beta);
  `dutch_vegetation_plot_species_cover` and `crms_phragmites_cover` are other plant-cover records of the family.
  External collections: none found.
- Papers and pages: the paper (Sec. 1, 2, 5.3, 6); no later use of the table found.
- Metric: Sec. 5.3 compares models by "Tjur's R2 and AUC for all five models, and the two CRPS metrics" over thirty
  random splits: several criteria, none named as the one that decides (MET-5), so the fallback `rmse`.
- Risks for /add-dataset: the cap. The paper models cover as "continuous on [0, 1)" and does "not address the notion
  of '1-inflation'" (Sec. 1), so 0.99 is probably full cover recoded (79 Restionaceae and 21 Crassulaceae plots,
  earlier AI count; a coded value, as in the family's open question on coded and censored values); the 21 plots whose
  two covers sum above 1 are possible with overlapping canopies. `Data Quality Issue` stays provisional until the
  coding is explained. Which family is the target; random or spatial split. TP-5: about 36 plots per random test fold
  is not a handful, so not `Too Small` by the rule.
- Priority: gap 0, use case 0, source + (the paper documents the plots, the release is the authors'), shape 0 (180
  plots, four covariates), risk - (target capped at 0.99, two candidate targets).

**Assessment (AI, 2026-10-30):** The family's question on species-abundance mapping is settled without a new rule
(Andrej, 2026-10-30, policy question 1 of the zero-inflated review: "I don't think there is new rule to build here.
These are per dataset judgement calls and if a dataset is useful for a predictive application although the data was
collected for something else, then this is fine"), as SEL-2 already reads the scope rules: this record is judged on its
own use case. The verdict and priority stay.

CC (2026-10-30, Andrej): `Yes`, priority 1 (the AI screening had `TBD -> 2nd Tier`, priority 1; zero-inflated screening
review page).

Plot cover of two plant families with four climate covariates, the example data of a zero-inflated beta regression
methods paper (Tang, Frye, Gelfand and Silander). Downloaded and measured on 2026-10-19: 180 plots x 10 columns
(plot, lat, lon, region, the two covers, four climate variables), no missing values, two regions (Baviaanskloof 119,
Cape Point 61), and only 150 distinct covariate tuples because plots share climate pixels. The paper frames it as
prediction: the spatial models "enable prediction to unobserved sites with known environmental attributes"
(Introduction), scored on 30 random splits into "a training set of 99 locations and a test set of 20 locations"
(Sec. 5.3). A quick LightGBM (random 5-fold, 3 seeds) reaches R^2 0.45-0.58 (Crassulaceae) and 0.56-0.64
(Restionaceae), presence AUC 0.77 and 0.89: a real signal on a tiny table.

Zero mechanism: the family was not recorded in the plot. Zeros confirmed from the data (Crassulaceae 48.9%,
Restionaceae 30.6%; Restionaceae zeros are 45% in one region and 2% in the other); the split into "unsuitable" and
"chance" zeros is the model's assumption (Sec. 2). `Data Quality Issue` is provisional: values pile up at exactly
0.99 (79 Restionaceae and 21 Crassulaceae plots), 21 plots sum to more than 1 over the two families (up to 1.98), and
the paper says "we do not address the notion of 1-inflation". To check: what 0.99 stands for, one family or both as
the target, and spatial blocks instead of random splits. The repository has no licence file.

**Assessment (AI, 2026-11-01):** added as `datasets/_dev/tabarena-v0pt2/cape_floristic_region_family_cover/` by /add-dataset with the full review panel; the open questions are in its `REVIEW.md`. Recommend shipping with the 21 plots at 0.99 kept and whole 1-minute climate cells held out (104 cells, keyed on two climate columns). Measured, superseding two readings above: in all 23 Baviaanskloof plots with both families between 0 and 0.99 the two covers share one per-plot denominator, so the target is a relative cover of undocumented scale and 0.99 a cap or a code, not "probably full cover recoded"; the plots whose covers sum above 1 follow from that denominator, not from overlapping canopies. The Dryad species file needs a manual download (not checked). The pinned commit is added to the links. `Data Quality Issue` stays until your mark on issue 1. Priority 1: gap 0, use case 0, source +, shape 0 (180 plots), risk - (the 0.99 coding decides the model ranking).

## Reference

Tang B., Frye H.A., Gelfand A.E., Silander J.A. (2023). Zero-Inflated Beta Distribution Regression Modeling. Journal
of Agricultural, Biological and Environmental Statistics 28:117-137. doi:10.1007/s13253-022-00516-z. Preprint
arXiv:2112.07249.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 18 (Cape Floristic Region plant cover).
