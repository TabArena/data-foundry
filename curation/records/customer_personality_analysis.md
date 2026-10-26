---
unique_name: customer_personality_analysis
name: Customer_Personality_Analysis
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Missing source information
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2021'
domain: business & marketing
required_split:
- '?'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis/data
source_row: 812
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16, PROV-3): the case the data comes from calls it a
mock sample of a hypothetical company.
- Source: the Kaggle upload imakash3011/customer-personality-analysis (2021; "provided by Dr. Omar Romero-Hernandez";
  "Target: Need to perform clustering") re-uploads the iFood CRM Data Analyst Case (hiring case of the iFood Brain team,
  on GitHub since May 2020: `ml_project1_data.csv`, `iFood Data Analyst Case.pdf`). As published: 2,240 customers x 29
  columns (birth year, education, marital status, income, spend per product category over 2 years, purchases per
  channel, `AcceptedCmp1`-`5`, `Complain`, `Z_CostContact`, `Z_Revenue` (constants 3 and 11), target `Response`).
- The case text: "you are presented a sample dataset, that mocks metainformation on the customer and on iFood campaign
  interactions with that customer", and its company is hypothetical ("Consider a well-established company operating in
  the retail food sector ... wines, rare meat products, exotic fruits"), not iFood (a food-delivery app).
- Use case, had the data been real: the CMO targets the sixth campaign at likely buyers; pilot of 2,240 random
  customers, cost 6,720 MU, revenue 3,674 MU (3 MU per contact, 11 MU per sale), a cost matrix (MET-7).
- Siblings: `customer_personality_analysis_2` is the same Kaggle URL. The CC line ("source is not entirely clear ...
  rather not use this task") points the same way.
- Reject check (AI, 2026-10-22): stands. SEL-16/PROV-3 by a source statement: the iFood case the upload copies says "you are presented a sample dataset, that mocks metainformation on the customer and on iFood campaign interactions" and sets a hypothetical company (https://github.com/nailson/ifood-data-business-analyst-test); the earlier CC line also advises against the task.

Well-known Kaggle 'Customer Personality Analysis' marketing dataset (~2240 rows, demographics, spend, campaign-response columns). It was published primarily as a segmentation/clustering exercise rather than a clean supervised task; the only natural target is the binary 'Response' (accepted last campaign), but as the curator notes the collection timing is unclear, raising leakage/temporal concerns. Source provenance is also fuzzy (single Kaggle re-upload, no original company). Maps weakly to criteria 1-2 and questionably to criterion 3. A human should verify whether 'Response' is a leak-free target, the true source, and the post-cleaning size before promoting; tentatively 2nd Tier.

---

CC: "Looks like a nice dataset, but source is not entirely clear to me. Also might be more a clustering task than predictive task? - could make it a predictive task using the following feature as target: Response: 1 if customer accepted the offer in the last campaign, 0 otherwise. However, we don't know enough about the time when the features were collected, so rather not use this task"

## Reference

Kaggle
