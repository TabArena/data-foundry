---
unique_name: iranian_churn
name: Iranian Churn
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
tags:
- New IID
collections:
- New (BeyondArena)
original_source: UCI
year: '2020'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5JW3Z
notebook_path: datasets/beyond_iid/new_iid/iranian_churn/iranian_churn.ipynb
source_row: 664
type_adapter_id: curation-record-v1
---

## Comments

UCI says: "All of the attributes except for attribute churn is the aggregated data of the first 9 months. The churn labels are the state of the customers at the end of 12 months. The three months is the designated planning gap." But the paper says: "The end of the observation period for each customer is the month in which the customer churns."
That means the task definition is not fully correct. It should be T1: observe fixed history of non-churn customers, WAIT, T2: collect all churns that occurred during the wait time as labels. Instead it is: collect data for each individual right up to the churn month for churners → compare with non-churners.
Nevertheless, the features are not collected after the churn and the task is still valid, if we conceptualize it as "identify customers close to churn" rather than "predict churn ahead of time".

Data was made IID
The upload to UCI in 2020 is not from the original authors. The actual collection period was from September 2006 to September 2007

CC (2026-10-01, Lennart): **Retired (No (Retired), Data Quality Issue): the feature window is anchored at the churn month, so the task detects customers who are already leaving rather than predicting churn.**
- Keramati & Ardabili 2011 (Telecommunications Policy 35(4), Sec. 4.1, p. 8): "2 months of observations of independent factors and a month of observations of customer status are recorded. The end of the observation period for each customer is the month in which the customer churns (i.e., sell or cedes SIM privilege to another person)." Churners are measured in their last weeks; non-churners presumably at the end of the 12-month collection (the paper does not say).
- The data shows the end-of-relationship pattern: median seconds of use 1,256 for churners vs 3,596 for stayers, zero calls 13% vs 2%, charge amount 0 for 84% vs 50%, and P(churn) 82.6% after a complaint vs 9.8% without (complaints are counted over the same window, including the churn month).
- `Status` is the operator's pre-churn rule on the same window (Sec. 3.4: Inactive = "have not increased their account in two sequential months while having had less than 30 min worth of calls in the last month. These customers are expected to churn in the near future."): P(churn) 47.5% when Inactive vs 5.6% when Active.
- LightGBM AUC 0.986 (typical churn tasks: about 0.7-0.85). Not fixable: the file has no dates or monthly series to re-anchor everyone at a common prediction date, and scale-free usage ratios from the same window still give AUC 0.982.
- Removed from the TabArena v0.2 working copy; the shipped notebook is unchanged.

## Reference

Keramati, A., & Ardabili, S. M. (2011). Churn analysis for an Iranian mobile operator. Telecommunications Policy, 35(4), 344-356.
