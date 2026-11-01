---
unique_name: imls_broadband_availability
name: Broadband Availability
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
year: '2020'
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.imls.gov/
- https://huggingface.co/datasets/inria-soda/STRABLE-benchmark/tree/main/broadband-availability
- https://arxiv.org/abs/2605.12292
- '# the IMLS page of the workbook and its file (the first link above is the IMLS home page)'
- https://www.imls.gov/research-evaluation/data/imls-indicators-workbook-economic-status-and-broadband-availability-and-adoption
- https://www.imls.gov/sites/default/files/publicdata_imls_metrics.xlsx
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a county indicator workbook IMLS assembled in 2020 for applicants to its CARES Act grants; the target is one of its published indicators (the share of the population with broadband available), and no decision rests on predicting it from the others.
- Source: IMLS, "IMLS Indicators Workbook: Economic Status and Broadband Availability and Adoption" (https://www.imls.gov/research-evaluation/data/imls-indicators-workbook-economic-status-and-broadband-availability-and-adoption; file publicdata_imls_metrics.xlsx, sheet "County Data REV"), "assembled in 2020", with no planned updates; its sources: the Bureau of Labor Statistics, the Census ACS and BroadbandNow (a commercial aggregator of provider filings). As published: a state tab and a county tab (3,220 counties of the 50 states, DC and Puerto Rico) with poverty, unemployment, no-health-insurance and SNAP rates, the shares without a home computer, without home internet and with home broadband (ACS, with margins of error), the number of broadband providers, the lowest monthly cost and the population share with broadband available. STRABLE (parquet previewed 2026-10-31): 3,219 rows x 24 columns, target `Population for whom broadband available, 2019 (%)`, untransformed.
- Use case: none named. The page says the workbook supports "the IMLS CARES Act Grants for Museums and Libraries Notice of Funding Opportunity" (applicants describe the need of their area) and planning by researchers and policymakers. Availability is compiled for every county from provider filings, so nobody predicts it from ACS rates; fit none as published. Regime IID over counties (one snapshot), grouped by state if a task were defined.
- Siblings and duplicates: `acs_household_broadband` and `ntia_internet_use_survey_home_adoption` (household-level adoption: other units, other targets); `imls_discretionary_grants` and `imls_awarded_grants` share only the publisher. Not a duplicate. External collections: STRABLE (Blayer et al. 2026, arXiv 2605.12292), "Broadband Availability": the paper describes "Data on internet speed and availability across the US", links the FCC Broadband Data Collection and says "The task is to predict the maximum available download speed", while STRABLE's config and script load this IMLS workbook with the availability share as target (an error of the copy, PROV-15).
- Better data: a candidate of the benchmark STRABLE; no further search this round.
- Papers and pages: the IMLS page; its user's guide (users_guide_imls_nofo_metrics.pdf) not read (no text layer reached us); STRABLE's script `preprocess_institute-museum-library-service_broadband.py` (github.com/soda-inria/strable); papers that used the data: not searched (the session's web search budget ran out).
- Metric: none found (the IMLS page publishes indicators, no task); STRABLE scores R2 for regression and AUROC for classification over all its tables (arXiv 2605.12292v2, App. D.1), a benchmark's habit, not the source's. So the fallback, `rmse` (MET-1, MET-8, MET-11); inputs none.
- Risks for /add-dataset: no target (SEL-3, `No Good Target (yet)`); `Number of Broadband providers (2019)` and `Lowest broadband cost per month` come from the same BroadbandNow source as the target (0 providers means 0% available), and the ACS home-broadband share is adoption, the twin of availability (LEAK checks); `GEO_ID`, `NAME` and the FIPS codes are ids; one snapshot, no time axis.
- Priority: gap 0 (no domain set; regression and IID not thin), use case 0 (none named), source + (IMLS page naming its sources), shape + (3,219 counties, 20 indicators), risk - (no target; the provider count shares the target's source).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark STRABLE (https://arxiv.org/abs/2605.12292).
- as published: 3,219 rows x 24 columns incl. target (STRABLE parquet); target: Population for whom broadband available, 2019 (%).
- Why: Predict the share of the population with broadband available in an area from library and community indicators
- Notes: Mismatch: the paper links FCC broadband data and says 'maximum download speed', but the raw file is IMLS publicdata_imls_metrics.xlsx and the target is 'Population for whom broadband available, 2019 (%)'. First publication of the IMLS metrics file not pinned down.
