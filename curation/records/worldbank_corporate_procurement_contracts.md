---
unique_name: worldbank_corporate_procurement_contracts
name: Corporate Procurement Contracts
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
collections:
- STRABLE
original_source: GOV Website
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://finances.worldbank.org/Procurement/Corporate-Procurement-Contract-Awards/DS00028
- https://financesone.worldbank.org/corporate-procurement-contract-awards/DS00028
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/corporate-procurement-contract-awards
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the World Bank Group's own contract awards above a disclosure threshold, documented by the Bank, each with a text description; estimating an award's value is a plausible use, but the supplier is known only at award, the target is cut at USD 250,000 (100,000 since Q3 FY25), and 3,295 awards over twelve fiscal years is small.
- Source: World Bank Group, Finances One DS00028 "Corporate Procurement Contract Awards" (https://financesone.worldbank.org/corporate-procurement-contract-awards/DS00028; the record's finances.worldbank.org link redirects to Finances One): "This set of data includes listing of contract awards that were executed by the World Bank Group", temporal coverage "FY2014 onwards", updated quarterly; "The data prior to Q3 FY25 reflects awards of USD $250,000 or greater", now contracts "with an estimated value above USD $100,000", fixed price and IDIQ; the list is "a guide to the distribution of major contract commitments", not every award. As published by STRABLE (export 2025-07-12): 3,295 rows x 12 columns (award dates 2013-07-17 to 2025-03-28, FY14 to FY25), target `Contract Award Amount (USD)` (log-transformed by STRABLE), features award date, quarter and fiscal year, commodity category (38), contract description (text), WBG organisation (IBRD, IFC, MIGA and others), selection number, supplier, supplier country and its code, fund source, VPU description.
- Use case: a WBG procurement or budget officer estimates a contract's value from its category, description and buying unit before the tender; the Bank does not name this use (the list is a disclosure), so the fit is approximate; regime temporal by award date.
- Siblings and duplicates: `worldbank_ipf_contract_awards` (contracts that borrowers award under Bank-financed projects, DS00073; 75,000 rows in STRABLE) has the same kind of target on another population: distinct (PROV-7). The other World Bank Finances One records from STRABLE (trust funds, FIFs, MIGA, IFC, IDA) are other ledgers. No duplicate. External collections: STRABLE (config `corporate-procurement-contract-awards`).
- Better data: a candidate of the benchmark STRABLE; no new search in this run.
- Papers and pages: the DS00028 page; STRABLE, Blayer et al. 2026, "STRABLE: Benchmarking Tabular Machine Learning with Strings", arXiv:2605.12292, App. C item 22 ("Listing of contract awards executed by the World Bank Group", task "predict contract value").
- Metric: none from the Bank (a disclosure list). STRABLE, the benchmark that framed the task, scores R² for every regression table (arXiv:2605.12292, App. D.1: "R2 for regression; AUROC for classification"; 3 outer folds, rendered "33", on a target it transformed to minimise skew, App. C): one metric for the whole benchmark, not a choice for this task (MET-5), so the fallback `rmse` (MET-8) on the amount as published, with any log shipped as `target_transform` (MET-3); inputs none (MET-1, MET-6).
- Risks for /add-dataset: `Supplier` and `Supplier Country / Economy` are known only at award (LEAK-10 for a pre-tender use; decide the prediction point, USE-3); the threshold changed in Q3 FY25, so the target is truncated at two levels (USE-5); IDIQ amounts are estimates of possible value, not awards; `Fund Source` mixes "Trust Fund" and "TRUST FUND"; `Selection Number` is an id; temporal windows on 3,295 rows (SPLIT-14, SPLIT-17).
- Priority: gap 0 (regression, temporal), use case 0 (ours), source + (documented by the Bank), shape + (3,295 rows with text, categories and dates), risk - (supplier known only at award; truncated target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,295 rows x 12 columns incl. target (STRABLE parquet); target: Contract Award Amount (USD).
- Why: Predict the value of a World Bank Group corporate procurement contract award
- Notes: World Bank Finances One DS00028, export 2025-07-12.
