---
unique_name: adzuna_job_salary_prediction
name: Adzuna Job Salary Prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Free Text (Sentences)
- AI-Filled (Verify)
original_source: Kaggle
year: '2013'
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/competitions/job-salary-prediction
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a featured Kaggle competition (Adzuna, 2013, 289 teams) on the annual salary of UK job ads from their title, description, location, contract and category, scored by MAE; about 245,000 labelled ads, text-heavy like `mercari_price_suggestion`.
- Source: Kaggle competition "Job Salary Prediction" (job-salary-prediction), launched with Adzuna in Kaggle's startup programme, 2013-02-13 to 2013-04-03, $6,000 (Kaggle API; welcome post by Ben Hamner). Description: "Predict the salary of any UK job ad based on its contents". Files (Kaggle API): Train_rev1 (128 MB zipped), Valid_rev1, Test_rev1, Location_Tree.csv and two benchmarks. Columns from the scout (file not opened): Id, Title, FullDescription, LocationRaw, LocationNormalized, ContractType, ContractTime, Company, Category, SalaryRaw, SalaryNormalized, SourceName; "about 244,768" training ads as commonly reported, not counted. The files were reissued as rev1 in February 2013 after Adzuna found a bug in its salary normaliser (forum topic 3852).
- Use case: a job board estimates the salary of an ad that states none (the host's own product, per the description above); fit direct; regime IID (no posting date in the column list).
- Siblings and duplicates: `data_scientist_salary` (MachineHack, Indian data-science ads, salary bands; TBD -> 2nd Tier with `NLP (Text)` and `Data Quality Issue`) is a smaller task of the same kind from another source (PROV-7). Other salary records (`ai_jobs_net_salaries`, `it_salary`, `stackoverflow_salary_data`, `employee_salaries`) are surveys or listings without ad text. Text-heavy precedents kept: `mercari_price_suggestion` and `emscad` (both Yes). External collections: none found.
- Better data: found as better data for `data_scientist_salary`; no further search this round.
- Papers and pages: the competition page and forum, read through the Kaggle command line ("Welcome", "SalaryNormalized accuracy/rule?", "Beating the benchmark (with a linear model)", "Beating the benchmark without FullDescription"); Train_rev1 is the labelled file; the validation and test salaries were not released as far as the forum shows (a 2017 topic asks for them).
- Metric: Mean Absolute Error, the competition's leaderboard metric (Kaggle API `evaluationMetric`); deliberate (MET-4); inputs none; on the salary in GBP (MET-3: a log target is fine when scored after the inverse).
- Risks for /add-dataset: SalaryRaw is the target as text (LEAK-10: drop); SalaryNormalized is Adzuna's parse of SalaryRaw, so check what normaliser artefacts remain after rev1 (ranges, daily or hourly rates); FullDescription carries much of the signal, so SEL-12 is judged on the shipped task as for `mercari_price_suggestion`; the same ad posted on several boards (SourceName) leaks across folds (LEAK-21: drop or group); ads from 2012-2013.
- Priority: gap 0 (no thin value), use case +, source +, shape + (about 245,000 ads, text and six categorical columns), risk - (text dominance under SEL-12, reposted ads).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `data_scientist_salary`.
- as published: UK job ads: Train_rev1 (about 244,768 ads as commonly reported, 128 MB zipped; file not opened), Valid_rev1, Test_rev1, Location_Tree.csv; columns Title, FullDescription, LocationRaw, ...; target: SalaryNormalized (annual salary in GBP of the advertised job); access: registration.
- Why: Same task as data_scientist_salary (salary of a job posting from its title, description, location and company), across all job categories
- Adds: About 15x the rows, full untruncated descriptions (the record's data-quality complaint), a continuous salary instead of bands, a competition metric (MAE). Older (2012-2013) and as text-heavy (SEL-12 applies the same way); SalaryRaw must be dropped (leak)
