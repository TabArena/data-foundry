---
unique_name: american_companies_bankruptcy
name: 'Machine Learning for Bankruptcy Prediction in the American Stock Market: Dataset and Benchmarks (American bankruptcy dataset)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Data Quality Issue
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Github
year: '2022'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.3390/fi14080244
- https://github.com/sowide/bankruptcy_dataset
- https://www.kaggle.com/datasets/utkarshx27/american-companies-bankruptcy-prediction-dataset
- https://github.com/sowide/Multi-modal-bankrutpcy
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 78,682 firm-years of 8,262 US listed companies (1999-2018) with 18 raw accounting items and a legal-filing label for the next year, published with a temporal split; a preview shows a decimal-point corruption to repair before anything else.
- Source: Lombardo, Pellegrino, Adosoglou, Cagnoni, Pardalos, Poggi, "Machine Learning for Bankruptcy Prediction in the American Stock Market: Dataset and Benchmarks", Future Internet 14(8):244, 2022 (doi 10.3390/fi14080244); data on GitHub sowide/bankruptcy_dataset (`american_bankruptcy_dataset.csv`, 12.4 MB, CC-BY-4.0, plus `dataset_paper.zip`). README: "We collected accounting data from 8262 different companies in the period between 1999 and 2018", "the resulting dataset of 78682 firm-year observations"; label: "we label the fiscal year before the chapter filling as "Bankruptcy" (1) for the next year. Otherwise, the company is considered alive (0)" (Chapter 11 or Chapter 7, per the SEC). Header (previewed): company_name (anonymised `C_n`), fyear, status_label (alive/failed), X1-X18, Division, MajorGroup (SIC). The Kaggle copy (utkarshx27, 2023, CC0) is the same data without the SIC columns and names X1-X18 (current assets, COGS, D&A, EBITDA, inventory, net income, receivables, market value, net sales, total assets, long-term debt, EBIT, gross profit, current liabilities, retained earnings, revenue, total liabilities, operating expenses). "The non-anonymized version of this dataset can NOT be available because of the license used to retrieve the dataset"; the vendor is not named.
- Use case: a lender or investor scores a listed firm from its latest annual accounts for a filing within a year; the paper's own statement of who acts was not read (the MDPI pages returned 403), so the fit is approximate for now; regime temporal: the source trains on 1999-2011, validates on 2012-2014 and tests on 2015-2018 (README), with firms repeated across years.
- Siblings and duplicates: `polish_companies_bankruptcy` (`Yes`), `taiwanese_bankruptcy_prediction` (`Yes`), `qualitative_bankruptcy` (`No`), `analcatdata_bankruptcy` (`No`), `company_bankruptcy_prediction` (`No`), `v4finbench_corporate_distress` (unscreened, a rule-defined distress label for Visegrad firms): other sources, no duplicate (PROV-4). The Kaggle upload is a copy of this source, kept on this record. External collections: none found; the curator's Zotero items 49 and 182 use it.
- Better data: found as better data for `polish_companies_bankruptcy`, `qualitative_bankruptcy` and `taiwanese_bankruptcy_prediction`; no further search this round.
- Papers and pages: the Future Internet paper; Pellegrino et al. 2024, Future Internet 16(3):79 (an LSTM on the same data, cited in the README); GitHub sowide/Multi-modal-bankrutpcy.
- Metric: the paper proposes "AUC, precision, recall, type I error, type II error, and macro- and micro-F1" for future benchmarking and leads with AUC (random forest 0.748 on average), with no threshold fixed: several metrics side by side, so the fallback `roc_auc` (MET-5, MET-6, MET-8); inputs none. Read from search snippets; the full text was not reachable.
- Risks for /add-dataset: in the preview, values jump by a factor of 1,000 inside one firm's series (C_1: X2 740998 in 1999, 701.854 in 2000; X14 606337 in 2002, 651.958 in 2003, 897284 in 2005), the pattern of a decimal point read as a thousands separator when a value has three decimals; repair it from the origin or by a documented rule (`Data Quality Issue`, PROV-13). X14 and X17 are identical in all 24 previewed rows, and X1 (current assets by the Kaggle names) exceeds X10 (total assets) wherever both are on one scale, so the names need the paper's table. Whether `failed` marks only the year before the filing or every year of a firm that failed decides the label (USE-5); firms delisted for other reasons stay `alive`. Check what `dataset_paper.zip` holds (possibly the paper's own split files).
- Priority: gap 0 (finance, binary and temporal are not thin), use case 0 (the paper's statement not read), source + (a paper and the authors' repository), shape + (78,682 firm-years with a temporal split), risk - (the decimal corruption, the column names, the label's semantics).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `polish_companies_bankruptcy`, `qualitative_bankruptcy`, `taiwanese_bankruptcy_prediction`; the curator's Zotero collection, item 182: "V4FinBench: Benchmarking Tabular Foundation Models, LLMs, and Standard Methods on ..."; the curator's Zotero collection, item 49: "Are Foundation Models Useful for Bankruptcy Prediction?".
- as published: 78,682 firm-years of 8,262 US public companies (NYSE, NASDAQ), 1999-2018; 18 accounting variables (X1-X18: current assets, COGS, EBITDA, net income, total assets, long-term debt, retained earnings, ...; target: bankruptcy (Chapter 7 or Chapter 11 filing) in the following year, binary, labelled on the fiscal year before the filing; access: open.
- Why: same task as polish_companies_bankruptcy: firm-year financial statement data, target bankruptcy within the next year, features known at the fiscal year end | the same task as the Taiwan record: listed firms, legal bankruptcy as the target, financial-statement features of the year before | Same target (corporate ...
- Adds: almost twice the firm-years (78,682 vs about 43,000), 20 years instead of 2000-2012, raw accounting items instead of pre-engineered ratios (the Polish record notes the features were already engineered), a population (all listed US firms) rather than a sample, and a published temporal split; no missing values | 11.5 ...
