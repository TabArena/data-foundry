---
unique_name: credit_card_customers
name: Credit Card customers
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 1
tags:
- New IID
collections:
- New (BeyondArena)
original_source: Company
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers
v2_path: datasets/_dev/tabarena-v0pt2/credit_card_customers/dataset.py
source_row: 672
type_adapter_id: curation-record-v1
---

## Comments

"I got this dataset from a website with the URL as https://leaps.analyttica.com/home" -> was a course website

Link above is down

Unsure if it can be recovered as a non-IID task

Used in this paper (but not the source https://www.sciencedirect.com/org/science/article/pii/S1526149223004460)

We have no real source information, but I think it is good to use for now. We can filter later

Remove NB features

**Assessment (AI, 2026-10-07):** Recommend No + AHDS + Missing source information; the curator has the call. The data is a teaching case of Analyttica's LEAPS platform (sample case 11; material not archived; the platform calls another case's data "a dummy dataset"). The activity columns do not come from one transaction history. The 12-month count equals the Q4 plus the Q1 count in every row (shuffled totals: about 550 of 10,127; Home Credit card statements: 9 of 8,920). Inactive months are unrelated to it (Spearman -0.05; Home Credit -0.60). Education carries nothing beyond the label. Tenure in months tracks age in years (r 0.89), and no woman earns above $60K (0 of 5,358).

CC (2026-10-19, Lennart): Credit_Limit and Total_Revolving_Bal are clipped at percentiles of the whole file; kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

**Assessment (AI, 2026-10-20):** priority 1 for the review of the added dataset: gap -, use case -, source -, shape +, risk - (Issue 1: run recommends No + AHDS (constructed columns); issue 2 possible window-ends-at-closure leak). Popular churn table, but likely constructed teaching data with an untraceable source and a near-ceiling AUC; weak benchmark value.

**Assessment (AI, 2026-10-20):** Don't ship yet; the standard for calling data generated without a source statement or a generator decides (REVIEW.md issue 1, one standard for this dataset, hepatitis_c_egypt, stroke_prediction and framingham_heart_study_fhs). The review panel reproduced the marks (12-month count = Q4 + Q1 count in 10,127/10,127 rows; inactivity and spend independent of activity where real card tables are not; tenure set by age), but the label-linked tests are weak (label-free distance AUC 0.559; class-dependent correlations without a sign change). Unverified: the LEAPS case date (2020-04-19) and the LEAPS remark calling another case's data "a dummy dataset"; the platform is offline and not archived. If kept, the keep of the untraceable teaching source needs a PROV-1/PROV-2 amendment (issue 3). The definition now carries `ForcedIIDFromTemporal` (SPLIT-8). Priority 1: gap -, use case -, source -, shape +, risk - (approximate fit with a possible window leak; untraceable teaching source; recommendation not to ship yet).

CC (2026-10-21, Lennart): drop the `2ndTierData` tag ("we have this now with use case fit more or less"); the tag is retired from new definitions.

## Reference

Kaggle / Broken Website
