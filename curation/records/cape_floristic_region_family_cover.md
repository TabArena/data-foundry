---
unique_name: cape_floristic_region_family_cover
name: Cape Floristic Region plant-family cover (ZIB_data, Crassulaceae and Restionaceae)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Data Quality Issue
tags:
- AI-Filled (Verify)
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
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

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

## Reference

Tang B., Frye H.A., Gelfand A.E., Silander J.A. (2023). Zero-Inflated Beta Distribution Regression Modeling. Journal
of Agricultural, Biological and Environmental Statistics 28:117-137. doi:10.1007/s13253-022-00516-z. Preprint
arXiv:2112.07249.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 18 (Cape Floristic Region plant cover).
