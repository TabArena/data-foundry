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

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
