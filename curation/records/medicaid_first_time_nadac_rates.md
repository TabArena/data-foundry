---
unique_name: medicaid_first_time_nadac_rates
name: NADAC Rates
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
year: '2020'
domain: medical & healthcare
problem_type: Regression
original_data_state: One Table
source_links:
- https://data.medicaid.gov/dataset/national-average-drug-acquisition-cost
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/first-time-nadac-rates
- https://arxiv.org/abs/2605.12292
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/national-average-drug-acquisition-cost
- '# First Time NADAC Rates by catalog id (the first link above returns 404 on 2026-10-31)'
- https://data.medicaid.gov/dataset/e3af839d-8175-5be0-b94e-4a302ed7a035
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the first NADAC rates CMS sets for drug products that had none before; the price of a new product from its description is a plausible task, but no actor is named, the inputs are thin, and the record holds two STRABLE cuts of the NADAC survey.
- Source: CMS, the National Average Drug Acquisition Cost (NADAC) survey of retail pharmacies (weekly reference files on data.medicaid.gov since 2013, "NADAC (National Average Drug Acquisition Cost) <year>"). The cut named here: "First Time NADAC Rates" (https://data.medicaid.gov/dataset/e3af839d-8175-5be0-b94e-4a302ed7a035, issued 2020-11-06, updated weekly): "new National Average Drug Acquisition Cost (NADAC) rates, sorted by Drug Product and Date. The drug products listed have not had a NADAC rate in the past." STRABLE `first-time-nadac-rates` (first-time-nadac-rates-06182025.csv; parquet previewed 2026-10-31): 1,130 rows x 10 columns, as-of dates 2020-2025; target `NADAC Rate` per billing unit (log-type scale); inputs drug product (name, strength and form in one string), brief indication, drug class (Legend, OTC, Multiple), package size, NCPDP billing unit (EA, ML, GM), number of active NDCs in the rate group, primary reason code ("New Drug/New Generic", "New on COD File", "First Time Enough Qualifying Observations", ...), as-of date, brand or generic. The record's fourth link is a second STRABLE table, `national-average-drug-acquisition-cost` (a reduced cut of the 2024 weekly files): 8,947 rows x 11 columns, 8,922 NDCs, target `NADAC Per Unit`, inputs NDC, description, effective date, pricing unit, OTC, explanation code, classification for rate setting, and for brands the corresponding generic's NADAC (90% missing).
- Use case: none named by CMS (NADAC is a reference price for state Medicaid pharmacy reimbursement). A stand-in: a state agency or a pharmacy estimating the acquisition cost of a newly marketed product before the survey gives it a rate (a cold start). Fit approximate at best. Regime temporal by as-of date.
- Siblings and duplicates: `aca_federal_upper_limits` (CMS FUL, which falls back on NADAC; `TBD -> 2nd Tier`, `No Good Target (yet)`, screened this run), `prescription_drugs` (California WAC increases, `TBD -> 2nd Tier`), `drug_directory` (FDA NDC listing, `TBD -> 2nd Tier`). The two NADAC tables in this record are cuts of one survey (PROV-6): the first-time file is the cold-start framing, the weekly file a repeated price list; the curator picks the cut. External collections: STRABLE (arXiv 2605.12292), whose list has "NADAC Rates" ("Weekly survey of drug acquisition costs for retail pharmacies. The task is to predict the acquisition cost per unit") and "National Average Drug Acquisition Cost" ("Survey of retail pharmacy drug acquisition costs. The task is to predict units costs"); the record's first link (https://data.medicaid.gov/dataset/national-average-drug-acquisition-cost) returns 404 (2026-10-31).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the data.medicaid.gov pages; the CMS NADAC methodology not read; STRABLE's scripts `preprocess_medicaid-First-Time-NADAC-Rates.py` and `preprocess_medicaid-National-Average-Drug-Acquisition-Cost.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (data.medicaid.gov, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` on the dollar price per unit, shipped on a log scale (MET-3, MET-8); a relative error from context (MET-11, as for diamonds) is the curator's call. Inputs none.
- Risks for /add-dataset: the price is per billing unit (each, mL, gram), so the unit and the strength inside the product string drive the target (USE-5); the weekly cut repeats NDCs week after week in the full files and gives brands the generic's NADAC, a near-twin price (LEAK checks); 1,130 rows for mostly text inputs is small for the first-time cut; which cut to build is open (PROV-6).
- Priority: gap 0 (medical & healthcare, regression not thin), use case 0 (none named; the cold start is ours), source + (CMS survey with a published method), shape + (1,130 and 8,947 rows, text, categorical and dates), risk - (two cuts in one record; the target depends on the billing unit).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,130 rows x 10 columns incl. target (STRABLE parquet); target: NADAC Rate.
- Why: Predict the first-time NADAC per-unit rate of a newly surveyed drug | Predict a drug's national average acquisition cost per unit
- Notes: Raw file first-time-nadac-rates-06182025.csv (CMS, June 2025). Same publisher as row 81. | Raw file nadac-national-average-drug-acquisition-cost-2024_reduced.csv (weekly survey file, reduced). Weekly repeated prices per NDC: rows of the same drug across weeks.
