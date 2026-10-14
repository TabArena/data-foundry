---
unique_name: corporate_credit_rating
name: corporate-credit-rating
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Temporal)
collections:
- TabSTAR
original_source: Github
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://www.kaggle.com/datasets/agewerc/corporate-credit-rating
- https://www.openml.org/search?type=data&id=43344&sort=runs&status=active
v2_path: datasets/_dev/tabarena-v0pt2/corporate_credit_rating/dataset.py
source_row: 730
type_adapter_id: curation-record-v1
---

## Comments

Data and sources look good, could be a cool task, need to figure out which ratings to predict as it has minor ones

**Assessment (AI, 2026-10-07):** The uploader's script (github.com/Agewerc/ML-Finance) joins the opendatasoft ratings history to Financial Modeling Prep ratios, one rating per company and fiscal year; the Kaggle file is byte-identical to the repository's. The "minor ones" are AAA 7, CC 5, C 2, D 1: the definition merges CCC/CC/C as the uploader's table does and drops AAA and the defaults (6 classes, 2,020 rows). It departs from the Non-IID (Temporal) tag and groups by company: on temporal windows 87% of test ratings were of known companies, and carrying their last letter forward beat a random forest (log-loss skill 0.39 vs 0.31). A model from financials alone serves unrated companies (shadow rating). Caveats: 8% same-day instrument-grade label noise; delisted companies missing.
