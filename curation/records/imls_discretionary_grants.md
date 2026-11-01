---
unique_name: imls_discretionary_grants
name: Discretionary Grant
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
collections:
- STRABLE
original_source: GOV Website
year: '2014'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.imls.gov/research-evaluation/data/administrative-discretionary-grant-data
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/discretionary-grant
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: IMLS's administrative records of its discretionary grants (FY 1996-2013); the award is IMLS's own decision, the request it mostly follows is not in the file, and the same grants are in the newer IMLS awarded-grants table (`imls_awarded_grants`).
- Source: IMLS, "Administrative Discretionary Grant Data" (https://www.imls.gov/research-evaluation/data/administrative-discretionary-grant-data): "administrative records" of recipients "awarded funds by the Institute of Museum and Library Services", "from fiscal year 1996 through fiscal year 2014" (the file is discgrants96to13.zip, CSV, dated 2014-02-20, with DiscGrantsDataDoc.pdf); fields named: institution, project name, IMLS award amount, matching funds, grant period, and the grantee's latitude and longitude, census tract and block group, state and county. STRABLE (DiscGrants96to13.csv; parquet previewed 2026-10-31): 13,218 grants x 37 columns, fiscal years 1996-2013; target `AwardTotal` on a log scale; inputs log number, institution, program and program type, project title and project type (68% and 36% missing), award date, addresses, the contact's prefix, first and last name, organisation type, census geography and a project description (73% missing). Matching funds and the grant period are not in STRABLE's table.
- Use case: none named. IMLS sets the award after peer review, and an applicant knows what it requests; predicting the amount from program and institution is a stand-in no actor needs (approximate at best: a funder's budget estimate per program). Fit none as published. Regime temporal by fiscal year if a task were defined.
- Siblings and duplicates: `imls_awarded_grants` (IMLS awarded-grants file of 2025, STRABLE "Grant", 22,424 rows, FY 1997-2024, target `Federal Funds`): 12,588 of this table's 13,218 log numbers appear there (both STRABLE parquets compared on 2026-10-31), so the two are versions of one grant database with the same target (PROV-6); the newer one is larger and longer, this one has more columns (addresses, census geography, project type), and the curator decides which one enters. `hrsa_bhw_awarded_grants` (HRSA, another agency) is a different source. External collections: STRABLE (arXiv 2605.12292), "Discretionary Grant": the paper describes "Grants awarded based on competitive applications by HRSA" and links data.hrsa.gov, while STRABLE's config and data are IMLS's (an error of the copy, PROV-15).
- Better data: a candidate of the benchmark STRABLE; no further search this round (the overlap with `imls_awarded_grants` is a sibling check).
- Papers and pages: the IMLS page; DiscGrantsDataDoc.pdf not read; STRABLE's script `preprocess_institute-museum-library-service_discretionary-grant.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the IMLS page, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` on the dollar amount, shipped on a log scale (MET-3, MET-8); inputs none.
- Risks for /add-dataset: personal data of the grant contacts (`Prefix`, `FirstName`, `LastName`) to drop; `Description` is a summary written at award; `LogNumber` is an id that encodes program and year; the drivers of the target (the request, the program ceilings, matching funds) are not shipped (USE-5); the version question with `imls_awarded_grants` (PROV-6).
- Priority: gap 0 (no domain set; regression not thin), use case 0 (none named), source + (IMLS page and codebook), shape + (13,218 grants, text, categorical and geographic inputs, 18 years), risk - (a version of `imls_awarded_grants`; personal data).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 13,218 rows x 37 columns incl. target (STRABLE parquet); target: AwardTotal.
- Why: Predict the total award amount of an IMLS discretionary grant
- Notes: Mismatch: the paper links HRSA reports, but the raw file is IMLS DiscGrants96to13.csv (IMLS administrative discretionary grant data, 1996-2013).

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: a version of the same grants (12,588 of 13,218 log numbers shared) (`imls_awarded_grants`; PROV-6). The curator keeps one, or both as distinct tasks.
