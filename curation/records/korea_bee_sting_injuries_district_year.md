---
unique_name: korea_bee_sting_injuries_district_year
name: Bee-sting injuries / emergency-department bee-sting counts by district-year, South Korea 2014-2021
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Not Available (from Paper))
- No Good Target / Scientific Discovery
- Available on Request
tags:
- Two-Regime Zeros
original_source: Other
year: '2026'
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- '# The paper; no district-year table is released (outcome from NEDIS; ask the corresponding author)'
- https://doi.org/10.3389/fpubh.2026.1742966
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-19 from the two-regime-zero workbook (v4 of 2026-10-19, a list of 69 candidates, not in the repository), the source pages and papers, and the data itself where the notes say it was downloaded and measured. A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-27):** `TBD -> 2nd Tier`, priority 1: district-year counts of bee-sting emergency visits from
an association study, with no table released; the earlier `No` rests on readings, so it is no fast reject.
- Source: Kim and Min (2026), Frontiers in Public Health 14:1742966, published 2026-02-27: the "annual count of bee
  sting injuries aggregated at the administrative district level by year" (Sec. 2.2), 250 districts x 8 years
  (2014-2021), 469 zeros of 2,000 (earlier AI triage, 2026-10-19, from the paper). The outcome: "These data were
  obtained from the National Emergency Department Information System (NEDIS)" (Sec. 2.2), a KDCA platform ("All records
  were anonymized prior to acquisition"), counted by "the location of the reporting emergency department to approximate
  exposure location"; the covariates are climate, land cover and social factors per district. As published: no
  district-year table. Data Availability: "The original contributions presented in the study are included in the
  article/Supplementary material, further inquiries can be directed to the corresponding author"; the supplement holds
  the national annual counts (Supplementary Figure S1 and Table S1) and the AIC values (Table S1).
- Use case: for example a provincial health office preparing emergency departments or targeting warnings in high-risk
  districts. The source's aim is association ("we examined the epidemiological associations between potential
  environmental and social factors", Sec. 1), and its Discussion only points to "targeted awareness campaigns and
  strengthened emergency medical preparedness" and future "early warning systems" (Sec. 4), with no actor; fit
  approximate at best. Regime: temporal for next year's counts per district (a forecasting-like panel of 250 series,
  TP-10), or grouped by district for unsurveyed districts.
- Doubt: the earlier pass set `No` (`Not Available (from Paper))`, `No Good Target / Scientific Discovery`). A request
  route exists (the corresponding author), so availability alone is no reason (EV-4), unlike Lennart's `Not Available`
  rejects of the telecom churn papers ("too old to request / no request form"); and whether a decision fits is a reading
  (SEL-2, SEL-3), since the paper names preparedness and early warning as uses. The markers stay as the concerns to
  settle.
- Siblings and duplicates: none in `curation/records/` (searched bee, sting, NEDIS); external collections: none found.
- Papers and pages: the paper above (read in its JATS XML from Frontiers); no other paper on these counts found.
- Metric: AIC across count-model specifications (Sec. 2.4, Supplementary Table S1) and Moran's I on the residuals; no
  predictive score (Sec. 2.4, 3), so the fallback `rmse` (MET-1, MET-11); inputs none.
- Risks for /add-dataset: the table has to be requested, and NEDIS terms may not allow even district-year counts to be
  shared (`Data Requested` would be the next state); 2,000 rows whose covariates are mostly constant within a district;
  TP-10 for a next-year framing. None of the family's open policy questions applies: a zero is an observed district-year
  without an emergency visit.
- Priority: gap 0 (medical, regression and temporal are not thin), use case 0 (no actor named), source + (a
  peer-reviewed paper documents the variables), shape 0 (2,000 district-years of 250 districts), risk - (no released
  table).

CC (2026-10-30, Andrej): `TBD -> 2nd Tier`, priority 1, as screened (verified on the zero-inflated screening review
page).

An exploratory association study of bee-sting injuries with climate and land cover (Kim and Min 2026; paper read via
its JATS XML): the "annual count of bee sting injuries aggregated at the administrative district level by year"
(Sec. 2.2), 250 districts x 8 years = 2,000 rows, modelled with a zero-inflated negative binomial. The outcome comes
from NEDIS, the restricted national emergency-department database. Data availability: "The original contributions
presented in the study are included in the article/Supplementary material, further inquiries can be directed to the
corresponding author"; the supplement is one image and two DOCX tables that, going by their captions, hold AIC
values and annual counts, not a district-year table. So no released table, and the aim is association, not
prediction.

Zero mechanism, from the paper only: no emergency-department case in a district-year, "469 zeros among 2,000
district-year observations (23.4%)". The workbook's size is right; its access is not.

## Reference

Kim Y., Min K.-D. (2026). Associations of bee sting injuries with environmental and social factors: an exploratory
study. Frontiers in Public Health 14:1742966. doi:10.3389/fpubh.2026.1742966.

Lead: the two-regime-zero workbook (v4, 2026-10-19), Master row 12 (Bee-sting injuries).
