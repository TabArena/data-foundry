---
unique_name: pva_revenue_prediction_kddcup98
name: KDD98
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- 'Samples: One Moment'
- 'Target: Later'
collections:
- TabArena Reject
- TabSTAR
original_source: Website
year: '1998'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.openml.org/d/42343
- https://kdd.ics.uci.edu/databases/kddcup98/kddcup98.html
notebook_path: datasets/beyond_iid/new_iid/pva_revenue_prediction_kddcup98/pva_revenue_prediction_kddcup98_clf.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/pva_revenue_prediction_kddcup98/dataset.py
source_row: 647
type_adapter_id: curation-record-v1
---

## Comments

CC: "Predict whether there was a response to mailing. Side story: A friend of mine used to work for a company whose customers were mainly old people still ordering stuff from physical catalogues. Predicting the response to direct mailing was one the tasks he worked on. So this good old task is still relevant :) ... In Germany? :D"

This could also be used as a classification task given the first dependent variable

The problem type is not a property of this dataset: it is *either* regression on the donation
amount *or* binary classification on whether the mailing got a response — one target or the
other, never both at once. After investigation we shipped the classification version, so
`problem_type` records `Binary Classification` and the curated dataset comes from
`pva_revenue_prediction_kddcup98_clf.ipynb`, not from the regression notebook next to it.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in roc_auc — the KDD Cup 98 net revenue of the mailing (sum of TARGET_D - $0.68 over mailed donors) needs the donation amount, which our binary-response task drops (cup98doc.txt).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 6 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `SOLP3`, `SOLIH`, `RFA_2F`, `RFA_2A`, `GEOCODE2`, `DOMAIN_ses` (the README lists their levels); left unordered: `MDMAUD_recency` (a level outside the scale is a state of its own); `MDMAUD_frequency` (a level outside the scale is a state of its own); `MDMAUD_amount` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `INCOME`, `WEALTH1`, `WEALTH2`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3); 3 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `springleaf_marketing_response` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 5 coded columns carry their words; 3 scores are numbers (INCOME, WEALTH1, WEALTH2); DOMAIN_ses read row by row in the dictionary's two schemes (urban codes 2 and 3 were misread); AGEFLAG blank and GENDER A, C and Unknown missing.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-05, Lennart): GitHub issue #48 review: `DOMAIN_urbanicity` stays an unordered category with a note: the dictionary calls `DOMAIN` nominal and gives no density order of City and Suburban. The declared metric is checked.

CC (2026-11-11, Andrej): review marks. Issue 1 (B): the target is the gift amount `TARGET_D` in dollars (0 for the donors who did not give), scored by the cup's net revenue (`net_revenue_at_cost`, cost $0.68, per test donor, a new custom metric in the shared library); `TARGET_B` is dropped as a copy of gift > 0; `problem_type` Regression. Issue 2 (B): the gift receipts dated June 1997 or later (`RDATE_k`, `RAMNT_k`) are blanked, 61 cells of 60 donors. Issue 5 (B): `Target: Later` added to the tags (the gift arrives after the June 1997 mailing). Applied on the newer framework (`Source(...)`); not rebuilt.

## Review

**Outcome:** added. The KDD Cup 1998 data of the Paralyzed Veterans of America (UCI KDD archive): 191,769 lapsed
donors (last gift 13 to 24 months earlier) who received the June 1997 renewal mailing, the cup's learning and
validation files pooled, with 477 features (age, household and neighbourhood data bought from outside sources,
interests, how the donor was acquired, and 24 months of promotion and gift history); the target is whether the donor
gave (5.1%), scored by ROC AUC as a stand-in for the cup's net revenue, on random donors (since 2026-11-11 the gift amount, scored by the cup's net revenue, issue 1). The AI recommends shipping
the cup's own task, the gift amount scored by the mailing's net revenue (issue 1), and blanking the gift receipts dated
after the mailing (issue 2). Reviewed without a review panel, from the gathered evidence: the record, the cup's
documentation, the BeyondArena results and checks on the shipped data; there is no model run for it. Validity:
the cup scored a predicted dollar amount against a $0.68 mailing cost, and the source warns that the chance to respond
and the gift size run against each other, so the shipped response target does not score the decision it names
(issue 1); 46 donors of the shipped data carry a gift received 8 to 12 months after the mailing (issue 2). Value: on
the one BeyondArena fold the methods spread from ROC AUC 0.583 (LIMIX-2) and 0.592 to 0.603 (linear model) to 0.632
(tuned LightGBM), a weak but real signal. Quality: nothing else open. Weighed: a documented charity mailing with the
cup's own cost and metric +, a changed target and a few late gift dates -.

**Main points:** Keep the random split, or split by a donor date (issue 6, new: every donor got the same mailing,
so the dates order donors, not outcomes; rec. keep). Settled 2026-11-11: the cup's gift amount with its net-revenue
metric (issue 1), late gift receipts blanked (issue 2), `Target: Later` (issue 5); the random split is a
`DelayedTarget` of the June 1997 mailing (issue 4).

**Record judgment:** valid as a response task, and the record's fields match the definition (the record's `Website`
counts as `Other`). The cup's documentation (https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98doc.txt)
names the decision and its cost, and the definition's `changes` says the target was changed. The licence is unknown
(`license = None`), a note for the release checklist, not a curation question. A scouting run found
`springleaf_marketing_response` (`TBD -> Yes`, not added) as more recent data for the response to a direct-mail offer;
this record keeps the verdict its own data earns. One mailing stands in for the next (fit `approximate`); like the
other undated snapshots of the benchmark, the split is not tagged as forced from temporal (a note across datasets).

**Issues for Andrej:**

1. **Ship the cup's gift amount, scored by the mailing's net revenue, instead of the response?**

   * **Problem:**
     - The KDD Cup 98 scored a predicted gift amount per donor: mail every donor whose predicted gift exceeds the
       $0.68 a piece costs, and sum the actual gift minus $0.68 over the mailed donors.
     - The definition predicts only whether a donor gives and drops the amount (`TARGET_D`), so its ROC AUC is a
       stand-in that cannot score the mailing decision the definition names.
     - Keep the response, or ship the cup's amount and metric?
   * **Background:** the cup's documentation, "Evaluation rules": "the program committee will use the predicted value
     of the donation (dollar) amount"; "Sum (the actual donation amount - $0.68) over all records for which the
     expected revenue (or predicted value of the donation) is over $0.68". And under "Background and objectives": "PVA
     has found that there is often an inverse correlation between likelihood to respond and the dollar amount of the
     gift, so a straight response model (a classification or discrimination task)" (quoted up to here).
     The shipped data shows it: donors who responded had given less before (last gift $15.09
     against $17.47, average gift $11.72 against $13.25). The amount is 0 for the 94.9% who did not give and averages
     $15.62 among those who did ($1 to $200 in the learning file, up to $500 in the validation file), a zero-inflated
     target like the claim costs of the insurance tables added in PR #47. The cup's metric fixes the decision
     and its cost[^1a].
   * **Effect on the task:** the response target rewards finding responders; the cup's target rewards finding the
     donors worth $0.68, which differ when small gifts come from the likely responders.
   * **Consistency:** the rule on problem types names this dataset as having chosen the response framing, with the
     amount noted in the comments; it says a table may hold two framings, not which one to ship. The zero-inflated
     tables of PR #47 (allstate_claim_prediction_challenge_1m, liberty_mutual_fire_peril_loss_cost) ship amounts that
     are 0 for most rows with the host's own metric. Shipping both framings as two datasets would make them duplicates
     of each other[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Response, ROC AUC stand-in (implemented) | `TARGET_B` as target, `TARGET_D` dropped | a standard response-modelling task; a stable binary target; no custom metric | does not score the cup's decision; the source says response and gift size run against each other |
     | B | Gift amount, the cup's net revenue | `TARGET_D` (0 for non-donors) as target, `TARGET_B` dropped; metric: mean of (gift - $0.68) over the test donors whose predicted gift exceeds $0.68, per test donor | the cup's own task, decision and cost; adds a zero-inflated amount from outside insurance | a custom metric to write and test; a few large gifts move a fold's revenue; a rebuild |

   * **Recommendation:** B, the decision the definition names needs the amount, and the cup fixed both the target and
     the cost. **Decision:** keep the response (A), or ship the gift amount with the net revenue (B)?

   **Notes for the AI:** on B, `target = "TARGET_D"` with missing set to 0 (the cup fills it for non-donors; check),
   drop `TARGET_B`, `problem_type = "regression"`; a custom metric with a general name (for example
   `net_revenue_at_cost`, params `cost=0.68`) in the shared metric library with its reference implementation and tests
   (MET-12, MET-13), `Metric.source(...)` citing cup98doc.txt; ship the amount in dollars, as the decision compares
   it with $0.68 (the scale question of the insurance family, australian_vehicle_insurance_2004_2005 issue 5, applies);
   record `problem_type: Regression`, a CC line, the sentence of selection.md that names this dataset, CHANGELOG,
   rebuild on Andrej's ask. The metric review page lists this dataset; settle the metric there in the same call.

   [^1a]: **MET-7** (Should): when the source fixes a cost matrix, a single treatment threshold or a k from its
     decision, declare that metric; score the mean cost per row. **MET-4** (Should): a competition's leaderboard
     metric is the source's metric.
   [^1b]: **PROV-6** (Must): different versions or cuts of one dataset are duplicates when neither adds a distinct task,
     a swapped target among them. **SEL-8** (Must): the original task decides the scope.

   **Andrej (2026-11-11, change):** Option B: Gift amount, the cup's net revenue.

   **Resolved (2026-11-11, Andrej):** B: the target is `TARGET_D`, the gift in dollars (0 for the donors who did not
   give; the cup's files have no missing value), `TARGET_B` is dropped as a copy of gift > 0, `problem_type` is
   regression, and the metric is `Metric.source("net_revenue_at_cost", params={"cost": 0.68})`: the cup's sum of
   (gift - $0.68) over the donors predicted above $0.68, divided by the number of test donors. `net_revenue_at_cost` is
   a new custom metric in the shared library, tested against a transcription of the cup's rule, by hand, on 1M rows
   and by the stability checks. Record `problem_type` Regression, a CC line; the sentence of selection.md that names
   this dataset says which framing ships. Not rebuilt.

2. **Blank the gift receipts dated after the June 1997 mailing?**

   * **Problem:**
     - 46 of the 144,095 donors of the shipped data carry a gift receipt dated February to June 1998 in the
       `RDATE_*` columns (with its amount in `RAMNT_*`), credited to an earlier promotion but received 8 to 12 months
       after the mailing the label is about.
     - The cup's documentation says every field reflects the donor before June 1997 "except the gift receipt dates,
       which will follow the promotion dates", so these cells come from after the prediction point.
     - Blank these cells, or keep them?
   * **Background:** checked on the shipped data. The other dates and summaries end before the mailing (`LASTDATE`,
     `MAXRDATE` and `NEXTDATE` latest February 1997), so only these receipt cells are late; the 46 donors responded at
     10.9% (5) against 5.2% overall. A value from after the prediction point goes even when small, and the smallest fix
     blanks it[^2a][^2b].
   * **Effect on the task:** small in size (0.03% of the rows), but a model can read a gift made after the mailing.
   * **Consistency:** follows zillow_prize and melbourne_housing_market, which blank values recorded after the outcome.
   * **Unknown:** the v0.2 frame holds 47,674 more donors than the shipped data (those without a birth date); their late
     receipts are counted when the fix is applied.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | the late receipt dates and amounts stay | the file as published | a feature from after the mailing |
     | B | Blank the late cells | `RDATE_k` and `RAMNT_k` set to missing where the receipt is dated June 1997 or later | every feature precedes the mailing | 46 donors (shipped data) lose one or two old-promotion gifts |

   * **Recommendation:** B, a confirmed post-mailing value with a one-line fix. **Decision:** keep (A), or blank (B)?

   **Notes for the AI:** on B, in `_clean` before the date parsing, for k in 3..24: `late = df[f"RDATE_{k}"] >= 9706`
   (YYMM numbers), set `RDATE_k` and `RAMNT_k` to NaN on those rows; a `curation_comments` bullet with the count on
   the v0.2 frame; `dataset check`; CHANGELOG entry.

   [^2a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point. **LEAK-6** (Must): a
     confirmed leak goes even when small.
   [^2b]: **LEAK-7** (Should): the smallest fix that keeps a valid signal beats dropping the column; cases include
     blanking the values looked up after the outcome.

   **Andrej (2026-11-11, change):** Option B: Blank the late cells.

   **Resolved (2026-11-11, Andrej):** B: in `_clean`, `RDATE_k` and `RAMNT_k` (k = 3 to 24) are set to missing where
   the receipt is dated June 1997 or later: 61 cells of 60 donors on the v0.2 frame (191,769 donors), dated up to June
   1998. A `curation_comments` bullet gives the count; the `Time basis:` line now calls these receipts blanked.

3. **Keep `DOMAIN_urbanicity` unordered, with a note on why?**

   * **Problem:**
     - `DOMAIN_urbanicity` (Urban, City, Suburban, Town, Rural, the first byte of `DOMAIN`) ships as an unordered category, and the notes do not say why.
     - Issue #48 proposes Rural < Town < Suburban < City < Urban, with low confidence: it did not check City against Suburban.
   * **Background:** The dictionary lists the levels U, C, S, T, R and calls `DOMAIN` "A nominal or symbolic field" ([cup98dic.txt](https://kdd.ics.uci.edu/databases/kddcup98/epsilon_mirror/cup98dic.txt)); it does not say whether a city neighbourhood is denser than a suburb[^3a].
   * **Effect on the task:** Five levels in 191,769 rows; ordered or not, a model sees each level, so the choice changes little beyond the documented state.
   * **Consistency:** The second byte, `DOMAIN_ses`, is ordered because the dictionary names each level in words on one line.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Unordered, no note (implemented) | as now | none found | the rule asks for a note when the order stays unclear |
     | B | Unordered, with a note | one bullet in `curation_comments` | the source calls it nominal and gives no density order | a model cannot use that rural and urban are the two ends |
     | C | Ordered, Rural < Town < Suburban < City < Urban | `FeatureTypes(ordinal=...)` | the ends are clear; the dictionary's listing order read backwards | the City-Suburban step is a guess |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, add a dated bullet to `curation_comments`: the dictionary lists U, C, S, T, R and calls
   the field nominal, the density order of City and Suburban is not given, so the column stays unordered (CLEAN-14).
   On C, add it to `ORDINAL_LEVELS` and remove it from `categorical`. Then `dataset check`, a CHANGELOG entry and a CC
   line in the record. Issue #48's `WEEKDAY_APPR_PROCESS_START` point (home_credit_default_risk) is not raised: the
   curator's rule of 2026-11-01 orders a named cycle from Monday with the wrap not shown.

   **Lennart (2026-11-05, change):** Option B: Unordered, with a note.

   **Resolved (2026-11-05, Lennart):** B. `DOMAIN_urbanicity` stays unordered; `curation_comments` say why.

   [^3a]: **CLEAN-14** (Should): an order still unclear after the sources are checked stays unordered, with a note.

4. **Time basis: name the random split a `DelayedTarget` of the June 1997 renewal mailing?**

   * **Problem:**
     - Every donor received the same renewal mailing in June 1997, every history field is dated before it apart from the late gift receipts of issue 2, and the target is the response to that mailing, so all donors share one prediction moment with the target after it.
     - The record says `Samples: One Moment` without a target tag (issue 5), and the random split carries no time basis, while the definition's notes already say that one mailing stands in for the next.
     - Name it a `DelayedTarget`, with the line below?
   * **Background:** a delayed target needs its window closed for every row and every feature in existence at the
     moment[^4t1]. The window: the cup released the responses in 1998, and receipts dated up to June 1998 show at
     least a year of follow-up after the mailing, the same for every donor. The features: the cup's documentation
     says every field reflects the donor before June 1997 "except the gift receipt dates", which issue 2 blanks. The
     many date columns (`ADATE_*`, `RDATE_*`, `LASTDATE`, ...) are the shared past of one mailing, not a time to split
     on. What the split cannot test: the next mailing.
   * **Effect on the task:** none on rows, splits or scores; the same holds if issue 1 ships the gift amount.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `DelayedTarget` | `data_tags` gain `DelayedTarget`; a `Time basis:` line names the mailing and its window | states one mailing and one response window; follows the definition's own note | the next mailing is not tested |
     | C | Random, forced from temporal | `data_tags` gain `ForcedIIDFromTemporal` | marks the stand-in for the next mailing | the amended rule gives a release of one moment a prototype, not the forced tag[^4t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("DelayedTarget",)` (no tag is listed now) and the
   curation bullet "- Time basis: DelayedTarget: one renewal mailing (97NK, June 1997) to lapsed donors; every field
   is the donor before June 1997, apart from the gift receipts of earlier promotions dated after it (blanked, issue
   2); the target is the response to that mailing, recorded for every donor by the cup's release in 1998. The date
   columns are the donors' shared past, not a time to split on. Not tested: the next mailing."; `dataset check` (its
   note on date columns in a split that is not temporal is an info, answered by the line).

   [^4t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `DelayedTarget` has one prediction moment for all rows and the target after it; its line
     names the moment and the window, the window has closed for every row, and every feature existed at the moment.
     **LEAK-10** (Must): a feature holds only what existed at the prediction point.
   [^4t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the `DelayedTarget` issues of
   one-moment releases with one mark?" The `Time basis: DelayedTarget:` bullet is in `curation_comments`; it says why
   the random split is IID here (every row shares the moment and the outcome window, so no test row is later than a
   training row) and ends with what the split cannot test (the next mailing). The split and `data_tags` are unchanged;
   the tag `DelayedTarget` enters `data_tags` once PR #50 is in the working copy. As issue 2 is open, the line names the
   late gift receipt dates in the cup's own words instead of calling them blanked.

5. **Correct the record's collection facts: add `Target: Later`?**

   * **Problem:**
     - The record carries `Samples: One Moment` and no target tag, which says the target exists with the features.
     - The target is a gift sent in response to the June 1997 mailing and received after it, the same mailing for every donor.
     - Add `Target: Later`?
   * **Background:** `Target: Later` is the fact for a target after the features, at one shared date or after a fixed
     window; no tag is for a target that exists with the features[^5t1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | no target tag | none found | reads the response as existing with the history |
     | B | Add `Target: Later` | the record's `tags` gain `Target: Later` | the response comes after the mailing | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, add `Target: Later` to the record's `tags`, a `CC (<date>, Andrej):` line, and `Andrej`
   in `checked_by`.

   [^5t1]: **SPLIT-32** (Should): the record's collection facts include `Target: Later` (after the features, at one
     shared date or after a fixed window), `Target: Varying Delay` or `Target: Revised Later`; no target tag when the
     target exists with the features.

   **Andrej (2026-11-11, change):** Option B: Add Target: Later.

   **Resolved (2026-11-11, Andrej):** B: `Target: Later` added to the record's tags (also in PR #50's copy of the
   record), a CC line, `Andrej` in `checked_by`.

6. **Split: make it temporal, by one of the date columns?**

   * **Problem:**
     - Every donor got the same mailing (June 1997, `ADATE_2` = 9706 for 191,758 of 191,779 donors) and answered in
       the same window, so no donor's outcome is later than another's: the dates order donors, not outcomes.
     - A split by a donor's history date tests a kind of donor training never saw; a model trained on the older
       donors falls to the "mail everyone" baseline or below it (table 2).
     - Keep the random split, or split by `ODATEDW` or `LASTDATE`?
   * **Background:** Andrej asked on the page (2026-11-11, dataset note): "Wait it seems like there are dates. Could
     we make this a temporal split instead?" The date columns are of three kinds: the calendar of the 23 earlier
     promotions (`ADATE_k`, one date per promotion for nearly every donor), the receipts of earlier gifts
     (`RDATE_k`), and per-donor history dates (`ODATEDW` the origin 1983-1997, `FISTDATE` the first gift,
     `LASTDATE` the last gift, March 1995 to February 1997). A truly temporal split needs an earlier mailing as
     training data. The history holds the responses to the earlier promotions, but the cup selected donors who had
     stopped giving by mid-1996, so those outcomes are selected on: the promotions from March 1996 on show 0.02% to
     0.9% response, the 1994-1995 ones 14% to 36% (table 1). The use case, the next mailing, goes to the same mix of
     donors one year on; the random split with the `DelayedTarget` line (issue 4) states this, and that the next
     mailing is not tested.

     Table 1, response of the June 1997 donors to earlier promotions (share of the mailed donors with a gift recorded):

     | Promotion date | 1996-06 | 1996-04 | 1996-03 | 1996-02 | 1996-01 | 1995-06 | 1994-06 | 1997-06 (target) |
     |---|---|---|---|---|---|---|---|---|
     | Response | 0.24% | 0.31% | 0.87% | 10.3% | 23.4% | 30.4% | 30.2% | 5.1% |

     Table 2, net revenue per test donor ($, the shipped metric) of one LightGBM regressor (400 trees, one seed, not
     tuned; sbatch, `~/claude_jobs/marks_1111/pva_revenue_prediction_kddcup98/measure.py`); "Random split" is the
     5-fold prediction for the same test donors:

     | Test set (latest 20-27%) | Test donors | Gave | Mail everyone | Random split | Trained on the earlier donors |
     |---|---|---|---|---|---|
     | all donors, random 5-fold | 191,769 | 5.07% | 0.111 | 0.130 | - |
     | `ODATEDW` from 1995-01 | 51,179 | 4.09% | 0.041 | 0.083 | 0.046 |
     | `FISTDATE` from 1995-01 | 38,734 | 3.93% | 0.035 | 0.083 | 0.028 |
     | `LASTDATE` from 1996-02 | 52,111 | 6.15% | 0.201 | 0.212 | 0.185 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, `DelayedTarget` (implemented) | as now | one mailing, one window; the next mailing's donor mix | the next mailing is not tested |
     | B | Temporal by `ODATEDW` (origin) | train on donors recruited before 1995, test on the later recruits | a date-ordered split | not a later time: tests transfer to new recruits; the model falls to the baseline |
     | C | Temporal by `LASTDATE` (last gift) | train on donors who lapsed earlier, test on the most recent lapsers | a date-ordered split | the same; below the baseline |

   * **Recommendation:** A. The dates order donors within one mailing; no split of this file tests the next mailing.
     **Decision:** A, B or C?

   **Notes for the AI:** on A, nothing changes (a CC line that the split was checked). On B or C, `temporal` on the
   column in `dataset.py` (cut at the 80% quantile), the `Time basis:` line rewritten (the split orders donors, not
   outcomes), `dataset check`, the split and leak probes, CHANGELOG, record `required_split`.

## Reference

Website / readme
