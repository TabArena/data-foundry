---
unique_name: hrsa_ahrf_workforce_demographics
name: Workforce Demographics
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- STRABLE
source_links:
- https://data.hrsa.gov/data/reports
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/workforce-demographics-wide
- https://arxiv.org/abs/2605.12292
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-3; USE-2): a survey tabulation, the shares of each health occupation by sex, age and race in each state from American Community Survey five-year estimates; STRABLE predicts the female share of a cell from the age and race shares of the same cell, and no actor makes a decision with that.
- Source: HRSA National Center for Health Workforce Analysis, the AHRF demographics dashboard download `AHRF_Demographics_Dashboard_Download_2016-2020.xlsx` (STRABLE's raw file; ACS 2016-2020), continued as the Health Workforce Explorer (https://data.hrsa.gov/topics/health-workforce/nchwa/health-workforce-explorer). Its methods (July 2026, https://data.hrsa.gov/Content/Documents/Topics/Health-Workforce-Explorer-Methods.pdf): "an interactive data tool that provides an overview of the U.S. health workforce"; "Demographics – Displays the number and percentage of health professions by sex, age, and race/ethnicity"; the data "consist of data from the U.S. Census Bureau's American Community Survey (ACS), 5-year Public Use Microdata Sample (PUMS) data files"; "ACS data are suppressed for any value where the percent relative standard errors (PRSE) is greater than 30%". As used by STRABLE (HF parquet, previewed): 1,588 rows, 37 occupations x (50 states, DC and an "All States" row), some cells missing, 19 columns of percentages and suppression notes ("Hispanic: Supressed; ..."), target `Female (%)`.
- Use case: none; the tool serves "states, policymakers, workforce planners, researchers, and the public in understanding the U.S. health workforce" and "a baseline to track changes in the health workforce". A row is an aggregate estimate, not a unit anyone acts on, and the female share is published next to the shares used to predict it. Fit none (USE-8).
- Siblings and duplicates: no duplicate (grep for AHRF, workforce demographics); the other HRSA tables of STRABLE: `hrsa_clinician_dashboard`, `hrsa_health_professional_shortage_areas`, `hrsa_bhw_awarded_grants`, `hrsa_uds_hypertension_control`. External collections: STRABLE (Table C.4 row 107: "Demographic information for the health professional workforce. The task is to predict regional workforce density.", while its `config.json` sets `Female (%)`).
- Better data: a candidate of the benchmark STRABLE; no further search for this run's finds.
- Papers and pages: the Explorer methods PDF; STRABLE, Blayer et al., arXiv 2605.12292 (v2, 2026-10-19).
- Metric: none (no task).
- Reject check (AI, 2026-10-31): stands. STRABLE's parquet (downloaded) is 1,588 occupation-by-state rows of race and age shares with suppression comments, and its config sets target 'Female (%)' (https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/workforce-demographics-wide). HRSA calls its source 'an interactive data tool that provides an overview of the U.S. health workforce' built from ACS PUMS (https://data.hrsa.gov/Content/Documents/Topics/Health-Workforce-Explorer-Methods.pdf): a survey tabulation whose rows no one acts on. The paper's 'workforce density' is another cell of the same tabulation.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 1,588 rows x 20 columns incl. target (STRABLE parquet); target: Female (%).
- Why: Predict the female share of the health workforce in an area
- Notes: Raw file AHRF_Demographics_Dashboard_Download_2016-2020.xlsx (HRSA Area Health Resources Files). Paper says 'workforce density'; config target is Female (%).
