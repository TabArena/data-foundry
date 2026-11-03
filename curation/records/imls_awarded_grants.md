---
unique_name: imls_awarded_grants
name: Grant
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
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.imls.gov/grants/awarded-grants
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/grant
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the IMLS public list of awarded grants (FY1997-2024 in STRABLE's cut), where STRABLE predicts the federal funds from program, institution, place and project description; amounts follow program rules and the applicant's request, and no decision predicts them.
- Source: Institute of Museum and Library Services, "Awarded Grants" search with a "Download the Data" CSV (https://www.imls.gov/grants/awarded-grants; columns Log Number, Institution, Fiscal Year, Program, Federal Funds, Funding Office, City, State); STRABLE's raw file `awarded-grants-2025-07-09.csv`. As used by STRABLE (HF parquet, previewed): 22,424 rows x 10 columns, FY1997-2024 (no one-year snapshot here), target log-scaled; `Description` text for 47% of the rows; 56 programs, among them Native American Library Services Basic Grants (5,706 rows, small fixed awards), Grants to State Library Administrative Agencies (1,610, a population formula) and the Museum Assessment Program (1,539).
- Use case: none in the source. Fit none; regime temporal (fiscal years), institutions repeat.
- Siblings and duplicates: `imls_discretionary_grants` (STRABLE's "Discretionary Grant", IMLS `DiscGrants96to13.csv`, 13,218 rows x 37 columns, 1996-2013, target `AwardTotal`): the same agency's award records with the same target over overlapping years, a version or cut of one register (PROV-6), so the curator keeps at most one; `hrsa_bhw_awarded_grants`. External collections: STRABLE (Table C.4 row 52: "Grant ... General information on federal grants awarded by HHS. The task is to predict the project funding amount.", linked to taggs.hhs.gov, while the file is IMLS's).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19), Sec. 3 and Table C.4; the IMLS search page.
- Metric: none found (IMLS defines no task; STRABLE's R², App. D.1, is benchmark-wide, MET-5), so the fallback `rmse` on the dollars; inputs none.
- Risks for /add-dataset: no task (`No Good Target (yet)`); formula and fixed-amount programs make a large share of the target a lookup of program and year (TP-4 for that share); amendments and supplements repeat a log number (690 repeats; LEAK-17); half the rows carry a short project description (SEL-12 weighs it); STRABLE's paper link is wrong.
- Priority: gap 0, use case 0, source + (the agency's award list), shape + (22,424 awards, mixed with text, 28 years), risk - (no task, program-determined amounts, overlap with `imls_discretionary_grants`).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 22,424 rows x 10 columns incl. target (STRABLE parquet); target: Federal Funds.
- Why: Predict the federal funds awarded in an IMLS grant
- Notes: Mismatch: the paper links HHS TAGGS, but the raw file is IMLS awarded-grants-2025-07-09.csv.

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: a version of the same grants (12,588 of 13,218 log numbers shared) (`imls_discretionary_grants`; PROV-6). The curator keeps one, or both as distinct tasks.
