---
unique_name: corporate_credit_rating
name: corporate-credit-rating
checked_by:
- Lennart
suggestion: 'No'
decision_markers:
- Data Quality Issue
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
source_row: 730
type_adapter_id: curation-record-v1
---

## Comments

Data and sources look good, could be a cool task, need to figure out which ratings to predict as it has minor ones

**Assessment (AI, 2026-10-07):** The uploader's script (github.com/Agewerc/ML-Finance) joins the opendatasoft ratings history to Financial Modeling Prep ratios, one rating per company and fiscal year; the Kaggle file is byte-identical to the repository's. The "minor ones" are AAA 7, CC 5, C 2, D 1: the definition merges CCC/CC/C as the uploader's table does and drops AAA and the defaults (6 classes, 2,020 rows). It departs from the Non-IID (Temporal) tag and groups by company: on temporal windows 87% of test ratings were of known companies, and carrying their last letter forward beat a random forest (log-loss skill 0.39 vs 0.31). A model from financials alone serves unrated companies (shadow rating). Caveats: 8% same-day instrument-grade label noise; delisted companies missing.

CC (2026-10-16, Lennart): retired for now. The labels mix the companies' ratings with ratings of their bonds and loans, and the uploader's build drops Moody's grades, delisted companies and most of each agency's history. To be rebuilt from the agencies' own rating histories and SEC filings as `corporate_issuer_credit_rating`.

**Assessment (AI, 2026-10-16):** compared with the agencies' Rule 17g-7(b) histories (ratingshistory.info files), 277 of the 1,594 labels that could be matched (17%) differ in letter from the agency's issuer rating in force on that date; e.g. Ball Corp, S&P, 2016-07-05: issuer rating BB+, label BBB (its secured bank loans, BBB-). The uploader's ratings file has only agency, name, date and grade, so the build cannot tell the two apart. The definition is in git at commit 2475ea2; the folder left the working copy on 2026-10-16.
