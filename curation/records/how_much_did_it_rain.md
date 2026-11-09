---
unique_name: how_much_did_it_rain
name: How Much Did It Rain? (Kaggle 2015)
checked_by:
- Andrej
suggestion: TBD -> 2nd Tier
decision_markers:
- Time-series (Regression)
tags:
- Two-Regime Zeros
original_source: Kaggle
year: '2015'
domain: environmental science & climate
problem_type: Regression
source_links:
- https://www.kaggle.com/competitions/how-much-did-it-rain
- https://www.kaggle.com/competitions/how-much-did-it-rain/data
type_adapter_id: curation-record-v1
---

## Comments

**AI-FILLED, UNVERIFIED. Drafted by an AI assistant on 2026-10-20 from the competition's pages and forum (the data was not downloaded). A human must verify the suggestion, the metadata and the notes before relying on them.**

**Screening (AI, 2026-10-20):** `TBD -> 2nd Tier`, priority 2: hourly rain-gauge totals from summaries of polarimetric
radar scans (AMS AI Committee on Kaggle, 2015), with a real zero regime, but the release has no time or place, so it
can only ship as forced IID.
- Source: the AMS Artificial Intelligence Committee's contest on Kaggle, January to May 2015. Train holds 2013 radar
  scans over US Midwest rain gauges; the test is "the same radars and gauges over the same months but in 2014" (data
  page), and its labels were never released. Not downloaded (the rules were not accepted on this account), so rows and
  columns are unmeasured.
- Target and zeros: `Expected`, the hourly gauge total in mm; the competition scored a CRPS over 70 thresholds. Rain
  falls "about 1/7th of the time" (forum thread 14245; thread 11484: "Probability of raining ... is about 14%"), so a
  dry hour is an observed zero: whether it rains and how much are two mechanisms.
- Use case: estimating the rain at a gauge from radar (quantitative precipitation estimation), as the AMS frames it;
  the source names no actor, and the operational product is a grid, not points, so the fit is approximate. Regime:
  temporal by nature (train 2013, test 2014; the host in thread 14245: "We can not randomly sample days from both years
  ... because the weather on consecutive days tends to be highly correlated"), but "Time and location information have
  been censored, and the data have been shuffled so that they are not ordered by time or place" (data page) and 2014
  has no labels, so it ships as IID, flagged forced IID from temporal (SPLIT-7, SPLIT-8).
- Doubt: the screening proposed `No` (`Data Quality Issue`, no honest split); the reject check refuted it: SPLIT-25 is
  the rule for grouped tasks, SPLIT-8 covers a temporal task released without dates, and the marker means damage to the
  values, which are faithful here.
- Siblings and duplicates: `how_much_did_it_rain_ii` (No, AI draft: radar pixels with 5 x 5 neighbourhoods, SEL-13; no
  zeros) is the same source with 2014 data and other fields. Rain I has per-gauge summary statistics and no
  neighbourhood statistics, and its top teams used gradient boosting, random forests and logistic regression (thread
  14242), so Rain II's modality reason does not carry over as is. No external collection found.
- Papers and pages: the competition's data page and forum threads 11484, 14242 and 14245; no data paper found.
- Risks for /add-dataset: whether radar-hours can be rebuilt from identical TimeToEnd sequences per radar (SPLIT-24),
  and how much the forced-IID split overstates the score; label noise ("noisy labels at 14/28/43/57mm", totals far
  above 100 mm; the competition cut at 69 mm); whether radar summaries count as remote sensing (SEL-13).
- Priority: gap 0, use case 0 (no actor named), source + (the committee's data page defines the columns), shape + (a
  season of hourly gauge records, size not measured), risk - (forced IID on storm-correlated hours, noisy labels).

**Consistency check (AI, 2026-10-30):** the review page sets `No` ("forced IID would introduce leaks for this task").
That is the first screening's reason (`No`, `Data Quality Issue`, no honest split), which the reject check refuted on
SPLIT-8: a temporal task released without dates ships as forced IID with the cost noted (`account_debt_south_africa`,
`mobile_churn`, Lennart). If the storm-correlated hours make this case worse than those (no way to bound the leak), that
is the fact for an exception to SPLIT-8, and the `No` needs a marker (`Data Quality Issue`, as first proposed);
otherwise 2nd Tier.

CC (2026-10-30, Andrej): `No` (the AI screening had `TBD -> 2nd Tier`, priority 2; zero-inflated screening review page,
after the AI's consistency check). "forced IID would introduce leaks for this task. What are you blabbing, if the data
is temporal but a temporal spliot is not possible, we cannot split the data and reject it" Marker `Time-series
(Regression)` set by the AI for this reason (the vocabulary's marker for readings whose timestamp did not survive,
SPLIT-7).

CC (2026-10-30, Andrej), in chat, on SPLIT-8: "I also disagree with that. Forced IID is to be avoided at all costs."
SPLIT-8 itself is unchanged for now (17 datasets of the v0.2 working copy ship as forced IID under it); this record's
`No` stands.

CC (2026-11-08, Lennart): re-opened, out of the PR #47 batch (review board, cross-dataset item "Re-read how_much_did_it_rain's No under the reworded SPLIT-8", go ahead: "re-open in the curation record but leave out of this batch for now, next screening can take a look at it"). The `No` of 2026-10-30 (Andrej) rested on a measured leak across a forced split (the hours of one storm on both sides); under SPLIT-8 as reworded on 2026-11-05 such a leak is weighed case by case. For the next screening: does a split grouped on storms remove the leak, or how large is it when kept? The suggestion returns to the screening's `TBD -> 2nd Tier`; the `Time-series (Regression)` marker stays until that check.

## Reference

Lead: zero-inflated screening review, policy question 6 (curator's go, Andrej, 2026-10-20); sibling of `how_much_did_it_rain_ii`.
