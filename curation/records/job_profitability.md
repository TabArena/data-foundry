---
unique_name: job_profitability
name: Job_Profitability
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- No Good Target  / Scientific Discovery
- Missing source information
tags:
- 2nd Tier / Scientfic Discovery
- AI-Filled (Verify)
collections:
- TabArena Reject
year: '2022'
domain: business & marketing
required_split:
- '?'
problem_type: TBD
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/ulrikthygepedersen/job-profitability/data
source_row: 814
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the proposed fast reject (SEL-3 (with SEL-5; PROV-1 supporting)) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`No Good Target  / Scientific Discovery`, SEL-3; `Missing source information`, PROV-1): the source's own aim is feature importance, and its target is computed from the shipped columns.
- Source: OpenML 44311 `Job_Profitability`, uploaded 2022-11-03 by "Leon Gross", no origin, paper or citation; the Kaggle copy (ulrikthygepedersen, 2023-02-02) names "https://www.openml.org/" as its source. As published: 14,480 jobs x 31 columns (job number, revenue, cost and hours columns, lead source), target `Jobs_Gross_Margin_Percentage`.
- Use case: none: the description is "Finding which features are most important to job profitability" (OpenML and Kaggle); every column is a closed job's revenue, cost or hours, known only after the job, so no decision before the outcome.
- Deterministic target (SEL-5): on the preview rows `Jobs_Gross_Margin_Percentage` = (`Jobs_Total` - `Jobs_Total_Costs`) / `Jobs_Total` (360 - 105.87 = 254.13 = `Jobs_Gross_Margin`, / 360 = 0.7059; 289 - 137.17 = 151.83, / 289 = 0.5254; 49 - 81.15 = -32.15, / 49 = -0.6561), and the cost components add up to `Jobs_Total_Costs`; dropping the rule's inputs leaves hours and lead flags of a finished job.
- Siblings and duplicates: none in the records. External collections: none found.
- Metric: none found (OpenML, Kaggle pages).
- The curator's workbook note: "Not much information given, but task seems interesting; used for feature selection / scientific discovery".
- Reject check (AI, 2026-10-22): does not stand. The identity is real: Jobs_Gross_Margin_Percentage = (Jobs_Total - Jobs_Total_Costs) / Jobs_Total. SEL-5 then says drop the rule's inputs and check whether a real task remains, and OpenML 44311's columns include quote-time fields: Sold_Hours, Pricebook_Price, Estimates, Jobs_Estimate_Sales_Subtotal, Jobs_Estimate_Sales_Installed, Is_Lead, Opportunity, Warranty, Recall, Converted, 'Lead Generated From Source' (https://www.openml.org/d/44311; the names look like a field-service software export). Margin from estimate-time fields is a plausible decision (price or accept a job), and checking that needs the data. On the source, PROV-1 is not a clear fail under PROV-2 as amended 2026-10-21: there is a named first uploader (OpenML, Leon Gross, 2022) to point to, and PROV-3 has not been run. The curator's workbook note was "task seems interesting".
- For /add-dataset: TBD -> 2nd Tier, priority 1. The add stage must check: (1) drop every input of the margin identity (Jobs_Total, Jobs_Subtotal, all cost, labor, burden and margin columns, the *_as_percent_of_Sales columns, Income), and probe whether the quote-time rest (sold hours, pricebook price, estimates, lead source, warranty/recall flags) beats a baseline (TP-2/TP-4). (2) Which of those fields are known before the job (LEAK). (3) PROV-3 tests on the shipped columns. (4) A search for Leon Gross and the company or software behind the export; if none and PROV-3 marks appear, then `No` with `Missing source information`.

A Kaggle dataset already tagged 2nd Tier / Scientific Discovery and placed in TabArena Reject, with the curator noting little information is given and that it seems geared to feature selection / scientific discovery rather than a clean predictive task. It may be a real profitability regression/classification, but the unclear target and provenance keep it in 2nd Tier. A human must verify the actual target column, dataset size, feature meaning, and original source before any promotion.

---

CC: "Not much information given, but task seems interesting; used for feature selection / scientific discovery"

## Reference

Kaggle
