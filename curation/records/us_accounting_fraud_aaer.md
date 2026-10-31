---
unique_name: us_accounting_fraud_aaer
name: 'Detecting Accounting Fraud in Publicly Traded U.S. Firms Using a Machine Learning Approach: data (data_FraudDetection_JAR2020.csv)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Github
year: '2020'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1111/1475-679X.12292
- https://github.com/JarFraud/FraudDetection
- https://econjwatch.org/articles/critique-of-an-article-on-machine-learning-in-the-detection-of-accounting-fraud
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: Bao et al.'s published firm-year data (Journal of Accounting Research 2020): Compustat items and ratios of US listed firms, fiscal years 1991-2014, labelled by later SEC enforcement releases (AAERs), with the authors' rolling temporal protocol and AUC tuning; a real, documented fraud-screening task.
- Source: Yang Bao, Bin Ke, Bin Li, Julia Yu and Jie Zhang, "Detecting Accounting Fraud in Publicly Traded U.S. Firms Using a Machine Learning Approach", Journal of Accounting Research 58(1):199-235, 2020 (doi 10.1111/1475-679X.12292); data and code on GitHub JarFraud/FraudDetection (last commit "update code and data", 2022-08-10). README: the fraud sample comes from the AAERs "as compiled by the University of California-Berkeley's Center for Financial Reporting and Management (CFRM)", plus hand-collected AAERs up to 2018-12-31; accounting data from "COMPUSTAT fundamental annual database fiscal year 1991 to 2014". As published: `data_FraudDetection_JAR2020.csv` (47.8 MB; header previewed: `fyear`, `gvkey`, `p_aaer`, `misstate`, 28 raw items `act` to `prcc_f`, 14 ratios `dch_wc` to `ch_fcf`; the first rows have fyear 1990), `AAER_firm_year.csv`, `identifiers.csv`, Matlab code. "The variable "misstate" is the fraud label (1 denotes fraud, and 0 denotes non-fraud)"; "The variable "p_aaer" is used for handling the serial fraud issue". Counts from the run's Assessment (146,045 firm-years, 964 fraud firm-years, 413 AAER cases) not recounted here.
- Use case: the SEC, an auditor or an investor screens firm-years when the annual report is filed and investigates the riskiest; the authors evaluate the top 1% to 5% of firm-years (`evaluate.m`: precision and sensitivity at top k, NDCG@k), an inspection budget; fit direct; regime temporal: `run_RUSBoost.m` trains on 1991 to t-2 and tests on year t (2003-2014) "with 2-year gap".
- Siblings and duplicates: `audit_data` (`TBD -> 2nd Tier`, Andrej, Missing source information: 777 Indian firms with audit risk scores); `american_companies_bankruptcy` (`TBD -> Yes`, US firm-years, a bankruptcy label); `polish_companies_bankruptcy`, `taiwanese_bankruptcy_prediction` (`Yes`, bankruptcy). No duplicate. External collections: none found.
- Better data: found as better data for `audit_data` (the run's Assessment); no further search this round.
- Papers and pages: the JAR paper (not read: Wiley); the README data sheet; Walker, "Critique of an Article on Machine Learning in the Detection of Accounting Fraud", Econ Journal Watch 18(1):61-70, 2021 ("some fraudulent firms were contained in both the training and test samples"), the authors' reply, and the corrected code and data of 2022.
- Metric: AUC, the criterion the authors tune by ("the model is trained using the training period 1991-1999, and then evaluated in terms of AUC in the validating year 2001", README on `tune_RUSBoost.m`); NDCG@k at the top 1% is reported next to it, so `roc_auc` as their deliberate choice (MET-5); inputs none; the source's protocol also needs `fyear` (the split) and `p_aaer` (training labels of a test-year case set to 0), both shipped, neither a feature.
- Risks for /add-dataset: serial frauds span years, so one case's firm-years must not sit on both sides (the Walker critique; `p_aaer`; SPLIT, LEAK); AAERs come years after the fiscal year, so the last years are under-labelled (SPLIT-9, SPLIT-10; the source's 2-year gap); about 0.66% positives (TP-5 per test year); `gvkey` and `p_aaer` are ids; the Compustat items are redistributed without a stated licence (EV-4: no reason for a verdict).
- Not checked: the JAR paper's text (sample selection, Table 1 counts); the row and positive counts of the CSV.
- Priority: gap 0 (finance has 15 accepted, binary and temporal not thin), use case + (screening with an inspection budget, fit direct), source + (peer-reviewed paper with a data sheet and code), shape + (about 146,000 dated firm-years, 42 features), risk - (serial frauds and unmatured labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `audit_data`.
- as published: 146,045 firm-years of US public firms, fiscal years 1991-2014, 964 fraud firm-years from 413 SEC AAER cases (Walker 2021); 28 raw Compustat accounting items, 14 financial ratios, identifiers fyear, ...; target: misstate (1 = the firm-year's financial statements were later the subject of an SEC Accounting and Auditing Enforcement Release); access: open.
- Why: same task as audit_data (UCI 475: classify fraudulent firms to direct auditors' effort), with a regulator's enforcement outcome as label and the firm's reported financial figures, known at filing, as inputs
- Adds: 188 times the units and 24 fiscal years instead of 777 Indian firms in 2015-2016, a peer-reviewed source with a defined temporal evaluation; caveats: inputs are financial-statement items rather than audit-discrepancy risk scores, the label arrives years later (the paper leaves a 2-year gap), serial frauds need care ...
