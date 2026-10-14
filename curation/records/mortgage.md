---
unique_name: mortgage
name: Mortgage
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- Non-IID (Temporal)
collections:
- New (BeyondArena)
original_source: Website
year: '2016'
domain: finance
required_split:
- Grouped (NON-IID)
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

## Reference

@book{baesens2016credit,
  title={Credit risk analytics: Measurement techniques, applications, and examples in SAS},
  author={Baesens, Bart and Roesch, Daniel and Scheule, Harald},
  year={2016},
  publisher={John Wiley \& Sons}
}
