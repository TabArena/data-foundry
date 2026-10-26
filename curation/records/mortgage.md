---
unique_name: mortgage
name: Mortgage
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Website
year: '2016'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- http://www.creditriskanalytics.net/datasets-private2.html
v2_path: datasets/_dev/tabarena-v0pt2/mortgage/dataset.py
source_row: 702
type_adapter_id: curation-record-v1
---

## Comments

Panel data from www.internationalfinancialresearch.org, maybe we can find the source and get more as it is just a " randomized selection"

Determine how to make it a target, as it is not just one target per group

**Assessment (AI, 2026-10-07):** Added as `mortgage`: one row per loan and quarter, target the quarter's status (default, payoff, active), temporal split on the last 3 quarters, as in the book's own backtest on period 60. No larger source exists: International Financial Research was a consultancy whose site is gone. The periods are quarters 2000 Q2-2015 Q1 (Case-Shiller match). The book's models use the quarter's own balance, LTV and macro values; the balance records the event and the macro values come out after the quarter, so we take the loan's previous quarter and the macro values published by then. No HMEQ-style generation artefacts. Licence: textbook use only, no commercial use; the site's terms forbid republishing or redistributing its content.

**Assessment (AI, 2026-10-20):** priority 5 for the review of the added dataset: gap + (problem_type multiclass_classification), use case +, source +, shape +, no known risk. A rare real loan-level multiclass panel with a temporal split that fills the multiclass gap, though the quarter's overall event rate drives much of the score.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; applied: `balance_time_lag_2` added (the balance at the previous-but-one observation; the data has no delinquency field), the last row of the 501 loans that leave early without an event dropped (label not recorded, LEAK-25), the two ids that copy another id dropped (23 rows), the 37.5% placeholder rate masked, and the notes corrected (GDP vintage caveat, the level effect's own reason, re-run numbers). Priority 4: gap + (multiclass_classification), use case + (a holder's quarterly PD scoring, the book's own backtest), source + (the book's data page and codebook), shape + (621,653 loan-quarters, 18 features, temporal), risk - (open: rows scored in the quarter the loan is originated, USE-3, issue 10; the quarter's overall event rate carries 74-83% of LightGBM's gain).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: investor_orig_time.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The book uses the data for many PD/LGD examples with assorted diagnostics (ROC/AUC for binary default, calibration plots), not one metric for this three-outcome task.

CC (2026-10-22, Lennart): issue 2: keep the 3 classes; a binary default-only companion might be reasonable in the future. Issue 10: (a), reword the use case: a loan is also scored in the quarter it joins the book. Issue 11: add the ratio of the two lagged balances. Issue 12: amend CLEAN-13. Issue 14: add the market mortgage rate ("this sounds like a good way to make the data better"). Issue 13: keep both conflicting copies as real data noise we may want to simulate. Issue 15: keep the LTVs above 300% as real data noise of unclear origin.

**Assessment (AI, 2026-10-22):** applied issues 2, 10, 11, 12, 14: `use_case`/`known`/`fit_reason` reworded (8,132 origination-quarter rows kept, 24 in test); `balance_ratio_lag_1_to_2` added; FRED MORTGAGE30US (Freddie Mac, "Copyrighted: Citation Required") averaged per calendar quarter and lagged one quarter as `market_rate_30y_lag_1`, with `rate_minus_market_rate_lag_1`; CLEAN-13 amended for a reference level. Untuned LightGBM, periods 60/59/58: log loss 0.1180/0.1274/0.1293 (0.1201/0.1327/0.1364 without the ratio), default ROC AUC 0.75/0.84/0.81; the market-rate columns move the log loss by under 0.001. dataset check: 0 errors, 0 warnings. Issues 13 and 15 depart from LEAK-20 (jm1) and CLEAN-11 (caracas_cervical_cancer, melbourne) without a fact that sets them apart, so they are back on the review page as consistency checks and not applied yet. Not built yet.

CC (2026-10-22, Lennart): issue 13: (b), keep the payoff copy of the 7 doubled period-51 loans, as implemented. Issue 15: (a), make the LTVs above 300% and the conflicting balances missing.

**Exception to LEAK-20 (2026-10-22, Lennart):** for 7 loans period 51 is doubled with only the status differing (active and payoff); the payoff copy is kept instead of dropping both, because all 7 loans end at period 51, so the active copy is damage to the file (PROV-13), not an ambiguous label. Serves P5 (faithful data: the file repaired toward what was recorded).

**Assessment (AI, 2026-10-22):** issue 15 applied: the 38 source balances that put the source's LTV above 300% become missing before lagging, so no `LTV_time_lag_1` above 300% is left (highest 261.4%). Issue 13 as implemented, with the exception recorded. REVIEW.md removed (nothing left open). Not built yet.

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
