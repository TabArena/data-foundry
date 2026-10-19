---
unique_name: sweden_depth_to_bedrock
name: Sweden depth-to-bedrock (SGU observations, two-part model; Lin et al. 2026)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
decision_markers:
- Not Available (from Paper))
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
- Non-IID (Grouped)
original_source: GOV Website
year: '2026'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.1111/ejss.70308
- https://github.com/linyq017/A-Two-Part-framework-for-Depth-to-Bedrock-Prediction-and-Uncertainty-Assessment-in-Sweden
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (`curation/inputs/two_regime_zero_datasets_v4.xlsx`), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

A national depth-to-bedrock model for Sweden (Lin, Peterson, Karlsson, Westphal, Lidberg and Agren, SLU; EJSS 77,
e70308, 2026) with a two-part framework: per the abstract, outcrops "introduce 'structural zeros'", an outcrop
classifier reaches AUC 0.96 and the fused model R^2 0.67. Observations come from SGU databases (the well archive is
CC BY 4.0, SGU geological data are open since 2024). Only the code is public: its `config.py` reads the authors'
local files (`/workspace/data/soildepth/DepthData/csvs/censored_encoded_folds/fold4_train.csv`), and the feature list
holds coordinates, 2 m LiDAR terrain derivatives, `HKDepth`, land age, soil-map one-hots, tectonic zones,
geomorphons and distance to deformation zones. No data deposit was found; the workbook's 1,199,920 observations are
unverified. Only the abstract was read (Wiley and the SLU portal returned 403).

Zero mechanism, from the abstract only: outcrops, structural. Two things to check before any rebuild: what `HKDepth`
is (if it is an existing depth model such as SGU's interpolated soil-depth model, it leaks the target), and how
right-censored depths are coded (the folder name says "censored", i.e. bedrock not reached). Workbook pushback: the
"public multi-source dataset" is not public as a table. Also check the paper's data statement.

## Reference

Lin Y., Peterson G., Karlsson C., Westphal F., Lidberg W., Agren A. (2026). A Two-Part Framework for Depth to Bedrock
Prediction and Uncertainty Assessment in Sweden. European Journal of Soil Science 77:e70308. doi:10.1111/ejss.70308.

Lead: curation/inputs/two_regime_zero_datasets_v4.xlsx, Master row 2 (Sweden depth-to-bedrock).
