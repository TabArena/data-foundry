---
unique_name: fio_homeowners_insurance_zip_2018_2022
name: 'Analyses of U.S. Homeowners Insurance Markets, 2018-2022: ZIP Code level supporting underlying metrics'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
year: '2025'
domain: insurance
problem_type: Regression
original_data_state: One Table
source_links:
- https://home.treasury.gov/news/press-releases/jy2791
- https://home.treasury.gov/system/files/311/Supporting_Underlying_Metrics_and_Disclaimer_for_Analyses_of_US_Homeowners_Insurance_Markets_2018-2022.xlsx
- https://home.treasury.gov/system/files/311/Analyses_of_US_Homeowners_Insurance_Markets_2018-2022_Climate-Related_Risks_and_Other_Factors_0.pdf
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 3: Treasury's ZIP-by-year homeowners-insurance metrics (127,965 ZIP-years) are real and national, but they were released for aggregate analysis, carry no published task, and hold only seven insurance metrics.
- Source: U.S. Treasury, Federal Insurance Office, "Analyses of U.S. Homeowners Insurance Markets, 2018-2022: Climate-Related Risks and Other Factors", released 2025-01-16 with the "Supporting Underlying Metrics" workbook (press release jy2791: "covering over 330 insurers on more than 246 million homeowners insurance policies aggregated to the ZIP Code level"); the data come from the NAIC's Property and Casualty Market Intelligence data call (workbook). As published (workbook read 2026-10-31): sheet "Supporting Underlying Metrics", 127,965 rows = 25,593 ZIP codes x 5 years (2018-2022), 10 columns: ZIP Code, Year, Policy Decile Grouping (deciles of the number of policies), Claim Frequency, Claim Severity, Loss Ratio, Premiums Per Policy, Nonrenewal Rate, Nonpayment Cancellation Rate, Other than Nonpayment Cancellation Rate; only ZIPs with at least 10 insurers and 50 policies ("These limits reduce the total number of ZIP Codes by 22 percent"); a "Metric Definitions" sheet defines each rate per policies in force.
- Source's words: "To promote transparency and research, Treasury is releasing this large subset of aggregated data metrics"; "The Supporting Underlying Metrics include certain data anomalies which may be of more limited materiality for purposes of aggregate analyses but which may be significant for results at the individual ZIP Code level" (Disclaimer sheet).
- Use case: a state insurance regulator flagging the ZIP codes where insurers will withdraw (nonrenew) next year, from this year's losses and premiums; the workbook says "years with high paid loss ratios may precede changes in availability and cost" but names no prediction; fit approximate, written by us. Regime temporal (year t+1 from year t), the ZIP as group.
- Siblings and duplicates: `sleuth_ex1714` (AI `TBD -> 2nd Tier`, priority 1; 47 Chicago ZIPs of 1977-78, the FAIR-plan share as the measure of insurers withdrawing, an inference table); `liberty_mutual_property_inspection` (an insurer's property risk, another task). External collections: none found.
- Better data: found as better data for `sleuth_ex1714`; no further search this round.
- Papers and pages: the FIO report (PDF, link above; not read here) defines the metrics and the analyses; the workbook cites NAIC's market analyses of 2024-12-04 on the same data call.
- Metric: none found (an analysis release, no task), so the fallback `rmse` on the nonrenewal rate (MET-1, MET-8); inputs none.
- Risks for /add-dataset: the target is ours, and the same year's metrics share its denominator (policies in force), so the features come from the year before (LEAK, USE-3); the workbook's own warning on ZIP-level anomalies; demographic, housing and climate-risk features are not in the file and would be joined from other sources by ZCTA, a rebuild (PROV-11); five years give at most four lagged years, three temporal windows (SPLIT-14).
- Priority: gap + (insurance thin), use case 0 (ours), source + (Treasury report with metric definitions), shape + (127,965 ZIP-years, temporal), risk - (no task published, ZIP-level anomalies, joins for most features).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `sleuth_ex1714`.
- as published: ZIP codes; over 330 insurers and more than 246 million policies aggregated by ZIP, 2018-2022, published for ZIPs with at least 10 insurers and 50 policies (about 78% of ZIPs); metrics: premium per ...; target: Insurer-initiated nonrenewal rate per ZIP code (homeowners insurance withdrawn); access: open.
- Why: The same question and unit as sleuth_ex1714 (insurers cancelling or refusing homeowner policies by ZIP code, measured there by FAIR-plan policies in 47 Chicago ZIPs of 1977-78), with the insurance features of the same kind (claims frequency and severity in place of fire and theft rates).
- Adds: Tens of thousands of ZIPs nationwide instead of 47, 2018-2022 instead of the 1970s, an agency source. Caveat: the demographic and housing features (income, minority share, housing age) are not in the file and would be joined from the Census ACS by ZCTA, a rebuild (PROV-11); the source is an analysis report, so the ...
