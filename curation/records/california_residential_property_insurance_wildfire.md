---
unique_name: california_residential_property_insurance_wildfire
name: 'California residential property insurance: ZIP-level wildfire experience'
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Not Representative
tags:
- Non-IID (Temporal)
original_source: GOV Website
domain: insurance
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.insurance.ca.gov/01-consumers/200-wrr/WildfireRiskInfoRpt.cfm
- https://www.insurance.ca.gov/01-consumers/200-wrr/upload/Residential-Property-Coverage-Amounts-Wildfire-Risk-and-Losses.xlsx
- https://www.insurance.ca.gov/01-consumers/200-wrr/upload/Format-of-the-Report-and-Methodology.docx
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-11-02 from the California Department of Insurance's source pages, workbook preview and methodology. A human must verify the suggestion and notes.**

**Screening (AI, 2026-11-02):** `TBD -> 2nd Tier`, priority 2: real ZIP-level residential insurance experience, but a usable prediction task and its inputs are not established.
- Source: California Department of Insurance, SB 824 Wildfire Risk Information report. The current report covers 2018-2023; its methodology is dated 7 July 2025. First public release date was not established, so `year` is left empty (PROV-9). The public XLSX aggregates policy records and claims by year, policy form and ZIP; the individual policy IDs used by CDI are not public in this workbook. Preview: its `Report` sheet has 32,354 presentation rows and 28 columns, including subtotals. These are not 32,354 independent training samples. Six policy forms; Coverage A (structure) and C (contents), earned premiums/exposure, fire/PPC risk summaries, and fire/smoke incurred losses and claim counts.
- Use case: for example, an insurer before a pricing review predicts the next year's fire/smoke cost for a ZIP and policy form. Fit approximate: this actor/moment/target is a proposed task, not one defined by the report (USE-1, USE-8). CDI's page mentions use in rate-change requests, but no predictive experiment or selected model. Concern under SEL-3 and SEL-10: it could be descriptive reporting or aggregate time-series forecasting. A genuine tabular task would need prior-known portfolio characteristics and evidence beyond a naive per-ZIP history (SEL-2, SEL-11, TP-10). This uncertainty is not a source-established fast rejection.
- Split: temporal if a valid predictive task is established, with ZIPs recurring across years (SPLIT-6, SPLIT-13). Six calendar years do not by themselves guarantee three valid windows: loss development, report-release dates and lagging the aggregates affect the available training history (SPLIT-9, SPLIT-10, SPLIT-14).
- Siblings and duplicates: searched records by California homeowners/residential insurance, SB 824, official URLs and wildfire terms; no matching source found. Wisconsin is government property cover; `nfip_redacted_flood_claims` is a different flood claim-level task. No external benchmark membership verified (PROV-4 to PROV-7, EV-7).
- Papers and pages: read CDI's Residential Property Insurance Report, the linked Wildfire Risk Information Reporting page, current Format of the Report and Methodology, and the workbook preview. The methodology's "Policy Records vs. Loss Records" and "Layout of the Report" explain the construction. It states "Incurred losses include the total amount of paid losses and case loss reserves"; the target is not paid cash alone.
- Metric: no predictive scoring metric found in those source materials; proposed fallback `rmse` in dollars only if total incurred loss becomes the justified target (MET-1, MET-5). Ratios or per-exposure targets would need their own decision and denominator treatment; no source metric is being claimed.
- Risks for /add-dataset: the three source slices (`All Companies`, `Fire Risk Scores`, `PPC Scores`) overlap in companies and outcomes. Select a coherent slice; exclude subtotals and avoid counting overlapping aggregates as independent rows. Same-year incurred losses, claim counts and outcome-derived ratios cannot be predictors (LEAK-10). Even non-loss aggregates summarize the full year's insured population; their availability before the year is not established. Coverage was recorded at year-end/last in-force day in 2018-2020, versus beginning/first in-force day from 2021. Losses are valued as of 31 January of the reporting year: the methodology says 2023 losses in the 2024 collection are to be updated in the 2026 report. Check revisions and comparable maturity before selecting labels (LEAK-22 to LEAK-26). Catastrophe classification changes in 2021. No model, naive baseline or definition was run; TP-10 remains open.
- Priority: start 1; gap 0 (insurance, regression and temporal are not thin); use case 0 (our proposed prediction point); source + (CDI documents the collection and aggregates); shape + (many ZIPs, several policy forms and years); risk - (scope, prediction-time inputs, overlapping slices and immature losses).

Screen verification: real administrative data and traceable institutional source pass (SEL-16, PROV-1); no ethics objection found in the consulted release (SEL-1). Scope/use-case fit, feasible temporal windows, target completeness and metric remain concerns, not passes (SEL-3, SEL-10, USE-8, SPLIT-14, MET-1). No duplicate found by source search; benchmark membership and first publication cannot be verified. Prefer the Spanish customer-level portfolio for the next review.

**Assessment (AI, 2026-11-02):** measured on the workbook's pivot cache (the `Report` sheet's 32,354 rows are its layout, not the data): 197,290 rows in three overlapping sources; `All Companies` holds 71,928 rows, 2,522 ZIPs x 7 policy types x 2018-2023, about 12,000 rows a year, 3,507-4,379 a year with a fire or smoke loss. Test windows 2021 / 2022 / 2023 would train on 75% / 80% / 83% of the rows (2020 / 2021 / 2022 without the immature 2023 losses: 67% / 75% / 80%), so SPLIT-14 holds. The loss is concentrated in wildfire years: the 10 largest rows hold 74.5% of 2018's loss (88% catastrophic) and 41.5% of 2020's, against 4.4-20.4% in the other years.

CC (2026-11-02, Andrej): `TBD -> 2nd Tier` with `Not Representative`, priority 2: the rows are ZIP x policy type aggregates, not policies; the same call as `swedish_motorcycle_insurance_wasa` and `brazilian_vehicle_insurance_autoseg_2011` (screening review page of the Wisconsin alternatives; a `Yes` was considered and withdrawn after the precedent prompt).

## Reference

California Department of Insurance. Residential Property Insurance Report, Part II: ZIP Code Level Experience Data. https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/index.cfm

California Department of Insurance. Wildfire Risk Information Reporting, SB 824. https://www.insurance.ca.gov/01-consumers/200-wrr/WildfireRiskInfoRpt.cfm

California Department of Insurance. Format of the Report and Methodology, updated 7 July 2025. https://www.insurance.ca.gov/01-consumers/200-wrr/upload/Format-of-the-Report-and-Methodology.docx

California Department of Insurance. Residential Property Coverage Amounts, Wildfire Risk, and Losses, current 2018-2023 workbook. https://www.insurance.ca.gov/01-consumers/200-wrr/upload/Residential-Property-Coverage-Amounts-Wildfire-Risk-and-Losses.xlsx

Lead: Andrej requested screening on 2026-11-02 while reviewing Wisconsin property insurance alternatives.
