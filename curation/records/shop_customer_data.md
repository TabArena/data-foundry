---
unique_name: shop_customer_data
name: Shop_Customer_Data
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- No Good Target / Scientific Discovery
tags:
- 2nd Tier / Scientific Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2023'
domain: business & marketing
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/datascientistanna/customers-dataset
source_row: 818
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-10-22):** the curator's `No` (CC line, TabArena Reject) stands; the source's own words decide it.
- Source: Kaggle dataset datascientistanna/customers-dataset, one file `Customers.csv` (created 2023-02-07), DbCL-1.0, usability 1. As published: "Shop Customer Data is a detailed analysis of a imaginative shop's ideal customers ... Dataset consists of 2000 records and 8 columns": Customer ID, Gender, Age, Annual Income, Spending Score ("Score assigned by the shop"), Profession, Work Experience, Family Size (read with the Kaggle CLI metadata).
- Use case: none; "imaginative shop" says the data is made up (SEL-16, PROV-3: `AHDS`), and no target is named (keywords classification, clustering); predicting the shop's own `Spending Score` simulates no decision (SEL-3). The column set extends the well-known Mall Customers toy table.
- Siblings and duplicates: none among the records (grep for customers-dataset, mall customers). External collections: none found.
- Metric: none; would be the fallback.
- No counter-argument: both markers follow from the source's words.


Kaggle 'Shop Customer Data' describing an imaginative/fictional shop's ideal customers, already tagged as a TabArena Reject. The curator notes it is likely artificial data and was not published as a predictive task (some users ad hoc predict spending score). It is excluded as artificial/handmade data without a genuine real-world predictive target.

---

CC: "Shop Customer Data is a detailed analysis of an imaginative shop's ideal customers. It helps a business to better understand its customers. Might be artificial data. Not uploaded as a predictive task. Some use the data to predict spending score"

## Reference

Kaggle
