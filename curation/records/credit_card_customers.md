---
unique_name: credit_card_customers
name: Credit Card customers
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
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

## Reference

Kaggle / Broken Website
