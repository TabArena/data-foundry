---
unique_name: v4finbench_corporate_distress
name: 'V4FinBench: a corporate bankruptcy prediction large-scale dataset (Visegrad group)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: Kaggle
year: '2026'
domain: finance
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.kaggle.com/datasets/sebastiantomczak10/v4-group-corporate-bankruptcy
- https://github.com/genwro-ai/V4FinBench
- https://www.emis.com/en
- https://doi.org/10.48550/arXiv.2605.10896
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 1,106,879 company-years of 203,900 Visegrád-group companies (2006-2021) with 131 financial features and a distress label set by an accounting rule on each company's final report, at six horizons; large and documented, but the label is a ratio rule, h=0 is trivial and the positives are 0.19% to 0.36%.
- Source: Kostrzewa, Tomczak, Furman, Poberezhna, Furgała, Farganus, Furman and Zięba, "V4FinBench: Benchmarking Tabular Foundation Models, LLMs, and Standard Methods on Corporate Bankruptcy Prediction", arXiv 2605.10896 (2026-05-11, v2 2026-05-13); data on Kaggle sebastiantomczak10/v4-group-corporate-bankruptcy ("The canonical public dataset", CC BY 4.0); code on GitHub genwro-ai/V4FinBench (MIT, created 2026-05-04). Built from EMIS "under an individual data-purchase agreement", and EMIS "granted explicit permission for this release" (Appendix F). As published: `company_years.parquet` (unlabelled) and `company_years_h1.parquet` to `company_years_h6.parquet` (paper horizons h=0 to h=5). The label (`docs/benchmark_protocol.md`, `labels.py`): a company's final observed report is positive when "Equity/total_assets < 0", "EBITDA/total_assets < 0" and "Current_assets/short_term_liabilities <= 0.6"; for horizon h "the final h reports are removed and the remaining latest report is labeled positive"; companies whose final report is in 2021 are unresolved (that report dropped, the earlier ones negative). Positive rates 0.36% (h=0) to 0.19% (h=5) (paper, Table 1). Counts per country from the run's Assessment (Poland 628,499, Hungary 358,486, Slovakia 62,141, Czech Republic 57,753), not checked.
- Use case: a lender or trade creditor scores a company from its latest accounts for distress in the coming years; the paper states bankruptcy prediction and that it "labels financial distress rather than formal legal bankruptcy filings" (Sec. 7), no actor; fit approximate (a ratio proxy for failure); regime grouped by company in the source ("All observations from a company must stay in the same fold", five folds within country), while a temporal split, which the paper does not consider, may fit known borrowers better (USE-10).
- Siblings and duplicates: `polish_companies_bankruptcy` (`Yes`: Zięba, Tomczak and Tomczak 2016, also from EMIS, Polish companies, a bankruptcy label): the same authors and database in a newer, wider release with another label, so a version question for the curator (PROV-6; PROV-7 if the label makes it a distinct task); `taiwanese_bankruptcy_prediction` (`Yes`); `american_companies_bankruptcy` (`TBD -> Yes`, the paper's external test set). External collections: V4FinBench is itself the benchmark (the curator's Zotero item 182).
- Better data: found as better data for `polish_companies_bankruptcy`, `taiwanese_bankruptcy_prediction` (the run's Assessment; Zotero item 182); no further search this round.
- Papers and pages: the arXiv paper (read in part through its HTML); the GitHub README, `docs/benchmark_protocol.md`, `docs/data_provenance.md`, `src/v4finbench/data/labels.py`, `src/v4finbench/evaluation/metrics.py`.
- Metric: "Given the 0.19–0.36% positive rate, F1 and ROC-AUC are the primary metrics" (Sec. 4), with the F1 threshold "calibrated on the validation split by maximizing F1" (protocol): two named criteria and no unique one, so the fallback `roc_auc` (MET-5); the threshold is tuned, not fixed by a decision (MET-6); inputs none.
- Risks for /add-dataset: h=0 labels a row by a rule on its own three ratios (SEL-5, `Trivial`), so only h>=1 is a task, and the rule's ratios of the year before stay strong inputs (TP-4 check); the positive is read off the last report, so a company that leaves the database for other reasons, or keeps reporting while distressed, is labelled by coverage (USE-5, a proxy); `operational_status` (X9) and the sector-relative ratios need a leak check (the paper has no leakage analysis); 0.19% to 0.36% positives (TP-5 per fold); the 1M cap trims the panel; the Kaggle download needs a login.
- Not checked: the rest of the paper (the feature list, Table 9); the Kaggle files (not downloaded); the per-country counts.
- Priority: gap 0 (finance has 15 accepted, binary and grouped not thin), use case 0 (no actor named), source + (paper, code, protocol, CC BY), shape + (1.1 million company-years, 131 features, metadata, grouped and dated), risk - (a rule-based proxy label, a trivial h=0, a status column to check).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `polish_companies_bankruptcy`, `taiwanese_bankruptcy_prediction`; the curator's Zotero collection, item 182: "V4FinBench: Benchmarking Tabular Foundation Models, LLMs, and Standard Methods on ...".
- as published: 203,900 companies, 1,106,879 company-years (Poland 628,499, Hungary 358,486, Slovakia 62,141, Czech Republic 57,753), 2006-2021, six sectors; 131 financial features (146 columns with country, year, ...; target: financial distress in a company's final reporting year, defined by rule: equity/total assets < 0 and EBITDA/total assets < 0 and current assets/short-term ...; access: open, registration.
- Why: the same task (corporate failure from financial ratios of earlier years) on a far larger and more recent population | Large, documented, real panel of financial statements for corporate distress prediction, with an open licence (CC BY 4.0), company-grouped folds and code. Concerns: the h=0 label is a deterministic ...
- Adds: 160 times the company-years, 2006-2021, four countries, grouped splits by company. Caveats for screening: the target is an accounting-rule distress flag, not a legal bankruptcy; h1 labels are computed from the same year's ratios (a leak), so h2 or later is the task; data from a commercial database released under CC ...
