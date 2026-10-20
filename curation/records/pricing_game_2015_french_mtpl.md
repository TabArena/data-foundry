---
unique_name: pricing_game_2015_french_mtpl
name: pg15training / pg15pricing (CASdatasets, 2015 French pricing game)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
- Two-Regime Zeros
year: '2015'
domain: insurance
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd
- https://github.com/dutangc/CASdatasets/tree/master/data
- https://freakonometrics.hypotheses.org/20034
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from a web search for zero-inflated regression candidates, the source pages and, where the notes say so, the downloaded data. A human must verify the suggestion, the metadata and the notes before relying on them.**

`pg15training` (100,021 rows, 2009-2010) and `pg15pricing` (36,311 policies of 2011, no claims) from the first
pricing game of the French Institute of Actuaries (5 November 2015), listed in CASdatasets as "Datasets from unknown
private insurers". Measured 2026-10-20: 100,000 policies (21 split over two rows), each seen once, exposure in days;
the third-party cost `Indtppd` + `Indtpbi` is exactly 0 for 84.1% (no claim, never negative), and `Numtppd` and
`Numtpbi` copy the occurrence. Schema, years and id format differ from pg17 (`pricing_game_2017_french_mtpl`), so a
separate portfolio.

The covariates fail the generated-data checks. `Poldur` (policy age) is independent of `Age` (r = 0.05): 10,480
policies are older than the driver's years past 18, among them 168 fifteen-year policies of drivers aged 20 or less.
Mean car `Value` is the same for `Category` Small, Medium and Large (16,381-16,542) and for every `Type`, and 12,651 of
the 20,010 "Housewife" rows are male (the levels may be recoded: "most categorical levels have unknown meaning"). Only a
few dependencies exist (Age-Bonus r = -0.22, Age-Adind 0.20, Group1-Value 0.23). That points to simulated or resampled
covariates, against the documentation; the evidence is circumstantial. Untuned LightGBM, 2009 -> 2010: AUC 0.72 for a
claim, R^2 -0.04 on log1p among positives. Word from the organisers (Arthur Charpentier) that the covariates are real
would reopen it. Licence: GPL (>= 2) (CASdatasets). The 2016 game (`pg16trainpol`, `pg16trainclaim`, a fleet
portfolio) is not in the log.

## Reference

CASdatasets (Dutang C., Charpentier A.), `pg15training`, `pg15pricing`, first pricing game of the French Institute of
Actuaries (5 November 2015). https://github.com/dutangc/CASdatasets/blob/master/man/pricingame.Rd

Lead: web search 2026-10-20 for zero-inflated regression candidates (not in the v4 workbook).
