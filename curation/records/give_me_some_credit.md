---
unique_name: give_me_some_credit
name: Give Me Some Credit / credit
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
original_source: Kaggle
year: '2011'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=44089
- https://www.kaggle.com/competitions/GiveMeSomeCredit/overview
notebook_path: datasets/beyond_iid/old_iid/give_me_some_credit/give_me_some_credit.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/give_me_some_credit/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict credit delay.

Potential issue: -

Lennart: No objection

Andrej: Time-invariant features, may not be representative anymore, but still valid

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Kaggle's evaluation: AUC.

CC (2026-11-11, Andrej): BeyondArena v0.2 review page, give_me_some_credit; all four marks `change`, applied to the definition on this branch.
- Issue 1 (B): 96 and 98 in the three late-payment counters (269 borrowers, all three at once; every real count is at most 17) and one age of 0 are set to missing, the rows kept. Not a leak: the 269 are distinct borrowers (215 distinct rows), 55% in distress against 6.7%, the code is in the competition's test file too, and alone it ranks at AUC 0.51.
- Issues 2 and 3 (B): the random split over borrowers stays and is tagged `ForcedIIDFromTemporal`, with a `Time basis:` bullet: the borrowers were scored at dates the competition does not state, each followed for two years, and the row id is no time order (a model tells low from high ids at ROC AUC 0.502). A dated release would allow a split by scoring date.
- Issue 4 (B): the record's collection facts are `Samples: Over Time`, `Time: Lost` and `Target: Later`.
- "Maybe we should also update our guidelines to say that forced applies if we don't have enough evidence for how the data was collected." The rules under `knowledge-curation/references/` were not edited; the wording is noted in issue 3 for whoever amends SPLIT-8.
- `dataset check` passed (0 errors, 0 warnings, 2 info: 609 exact duplicate rows and 38 conflicting ones, both unchanged by this edit).
- The review moved from the folder's file into this record's `## Review` section.

## Review

**Outcome:** added. The AI recommends shipping it after one cleaning change (issue 1). Reviewed on 2026-11-04
without a panel, from the evidence already gathered (the record, a model run on the TabArena v0.1 task of the
same source) and one check on the shipped table. The data are the training file of Kaggle's Give Me Some Credit
competition (2011): 150,000 borrowers with ten fields of a credit file (age, income, dependents, debt ratio, use of
credit limits, open lines and real-estate loans, and how often they were 30-59, 60-89 and 90 or more days late in the
past two years); the target is serious delinquency, 90 days or more past due, within the next two years (6.7%).
Validity: a lender's scoring decision on a credit file, with the outcome after it; the label is not read off the
90-days-late counter (of borrowers with one earlier 90-day late, 34% are in distress again; with none, 4.6%), so its
window follows the counters' window; no leak found (no signal in the row order or the row ids). Lender, place and
period are not stated. Value: the benchmark methods spread from 0.131 1-AUC (TabPFN-3.5) over 0.133 (tuned CatBoost) to
0.159 (logistic regression), so methods separate, the top ones narrowly. Quality: the three late-payment counters
carry the undocumented codes 96 and 98 and one age is 0 (issue 1); the debt ratio holds the debt amount where income
is missing (29,731 rows, median 1,159 against 0.30), a source quirk to keep with a note. Weighed: a lender's own
competition and a direct decision +, methods separate +, an undated table from an unnamed lender -.

**Main points:** The codes 96 and 98 and the age of 0 are missing now (issue 1, resolved). The random split stays,
tagged forced from temporal (issues 2 and 3, resolved 2026-11-09); the record's facts are `Samples: Over Time`, `Time:
Lost` and `Target: Later` (issue 4, resolved 2026-11-09).

**Record judgment:** valid, ship after issue 1. The definition has no note on its source quirks yet: the debt ratio's
two units, utilisation above 1 in 3,321 rows (up to 50,708; 37% in distress above 1, 7% above 10), and the codes of
issue 1.

**Issues for Andrej:**

1. **Set the late-payment counters' codes 96 and 98, and an age of 0, to missing?**

   * **Problem:**
     - The three late-payment counters hold 96 or 98 for the same 269 borrowers, where every real count is at most 17, so these are codes and not counts.
     - No meaning of the codes is documented anywhere we found, and one borrower has age 0.
     - Set them to missing, or keep the numbers the competition ships?
   * **Background:** each counter is the number of times the borrower was that many days past due in the last two
     years. The 269 borrowers carry the code in all three counters at once, and 55% of them
     are in distress (6.7% overall). Shipped as numbers, the code sits on the count axis as "98 late payments". A
     code that means unknown, or a state outside the scale, is missing when the column has no other missing
     value[^1a], and an impossible value is missing with the row kept[^1b]. As missing values the 269 rows stay
     recognisable: they are the only rows with these columns missing.
   * **Experiments:** on the shipped table (the same as the v0.2 frame apart from the target's name): the largest
     real counts are 13, 11 and 17; the label rate is 4.6% with no 90-day late, 33.7% with one, 49.9% with two, 61%
     with 3-5, 66% with 6-17, and 54.6% for the 269 coded rows.
   * **Consistency:** follows heloc (its unknown, all-other and no-record codes missing, 2026-10-31) and
     credit_card_clients_default (undocumented `MARRIAGE` and `EDUCATION` codes missing, 2026-11-01).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the numbers | 96 and 98 stay in the three counters; age 0 stays | the competition's file as shipped | a count axis holds codes; an impossible age |
     | B | Set to missing (implemented) | 96 and 98 missing in the three counters (269 rows); age 0 missing (1 row); a note says so | counts are counts; follows the curator's rule for codes | departs from the competition's file |

   * **Recommendation:** B, the curator's rule for undocumented codes, which keeps the group recognisable.
     **Decision:** missing (B) or keep the numbers (A)?

   **Notes for the AI:** on B, in `_clean`: `set_missing(df, {c: [96, 98] for c in
   ["NumberOfTime30-59DaysPastDueNotWorse", "NumberOfTime60-89DaysPastDueNotWorse", "NumberOfTimes90DaysLate"]})`
   and `age` 0 to missing; add the notes of the record judgment to `curation_comments`; re-run `dataset check` and a
   CHANGELOG entry.

   **Andrej (2026-11-04, discuss):** three late-payment counters hold 96 or 98 for the same 269 borrowers - do the 269
   borrowers mean there is a leak? How are their targets? Arte they distinct persons?

   **Answer (AI, 2026-11-04):**

   * **Your question:** are the 269 coded borrowers a leak, what are their targets, and are they distinct persons?
   * **Not a leak, and the code carries almost nothing:** the code alone ranks at AUC 0.507. LightGBM on the 9
     shipped splits scores 0.8646 with the codes, 0.8645 with them missing, and 0.8639 with them hidden as "never
     late".
   * **Their targets:** 147 of the 269 are in distress (54.6%, 95% interval 48-61%), against 6.7% overall.
     - Code 98: 143 of 264 (54.2%). Code 96: 4 of 5 (80%). Five rows cannot show a difference (Fisher p = 0.38).
     - Comparable groups: never late 2.7%; one earlier 90-day late 33.7%; two or more 55.2% (2,826 rows); no open
       credit line and no code 20.8% (1,611 rows).
   * **Why not a leak:**
     - The code is not an outcome status: 45% of the coded borrowers stay out of distress for two years. A
       charged-off or bankrupt status would put that near 0%.
     - The code is part of the file at scoring: the competition's unlabelled test file has it too, in the same
       share (214 of 101,503 rows, 0.21% against 0.18%) and with the same profile[^a1].
     - What it marks: all 269 have utilisation exactly 0.9999999 and no real-estate loan, 267 have no open credit
       line, and 209 have debt ratio 0. That reads like a credit file with no usable open account, where the
       counters could not be computed.
     - No meaning is documented: the data dictionary is silent, and users of the data treat 96/98 as special codes
       without a source[^a4].
   * **Distinct persons, yes:**
     - The 269 rows hold 215 distinct value combinations. 75 rows fall into 21 identical groups, and 10 of those
       groups mix both outcomes.
     - Identical rows are expected here: only age (47 values), income (106 values, 121 missing), dependents and debt
       ratio (56 values) vary. Their row ids spread over the file (1,734 to 149,770)[^a2].
     - Their outcomes follow these fields: 45% in distress under 30, 80% over 60; 75% with a debt ratio above 0,
       49% at 0. LightGBM ranks them among themselves at AUC 0.70.
     - Train against test: 75 of the 214 coded test rows match a coded training row exactly. That is the same thin
       profile, not copies.
   * **Models** (mean ROC AUC, 9 shipped splits; "rest" = the test rows without a code):

     | Variant | LightGBM, all | LightGBM, rest | Logistic, all | Logistic, rest |
     |---|---|---|---|---|
     | Codes kept (A) | 0.8646 | 0.8632 | 0.8405 | 0.8388 |
     | Codes missing (B) | 0.8645 | 0.8632 | 0.8420 | 0.8404 |
     | Missing plus a flag column | 0.8646 | 0.8632 | 0.8420 | 0.8404 |
     | Rows dropped (C) | - | 0.8633 | - | 0.8402 |
     | Codes hidden as 0 (control) | 0.8639 | 0.8631 | 0.8389 | 0.8390 |

     - The choice does not move LightGBM. Logistic regression gains 0.0015 when the codes are missing: 98 on a count
       scale bends a linear fit.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the numbers | 96 and 98 stay in the three counters; age 0 stays | the competition's file as shipped | a count axis holds codes; logistic regression loses 0.0015 AUC; an impossible age |
     | B | Set to missing (implemented) | 96 and 98 missing in the three counters (269 rows); age 0 missing (1 row); a note says so | counts are counts; the 269 stay recognisable as the only rows missing there; follows the rule for undocumented codes[^a3] | departs from the competition's file |
     | C | Drop the 269 rows | removes the coded borrowers | no codes at all | drops real borrowers with real outcomes (55% in distress), and a thin-file group the lender scores |

   * **Recommendation:** B, unchanged. The 269 are real, distinct borrowers whose code is known at scoring and does
     not give away the outcome. Missing values keep them recognisable without putting a code on a count axis. A
     separate flag column adds nothing.
     **Decision:** missing (B), keep the numbers (A), or drop the rows (C)?

   **Notes for the AI:** raw Kaggle files (train, test, data dictionary) in
   `~/claude_jobs/ba_marks_1104/give_me_some_credit/raw/`; checks `explore.py`, `explore2.py`; models `models.py` →
   `models.csv`, `models.log` (Slurm job 1358184, cpuhigh32, LightGBM 400 trees and quantile-transformed logistic
   regression with missing indicators; TabPFN not run on 100k training rows). The shipped parquet equals the raw
   training file (269 coded, 1 age 0, 150,000 rows). Outside this issue: utilisation 0.9999999 is itself a code on
   10,256 rows (17.7% in distress among the uncoded ones), every row without an open line included; it may deserve
   its own issue.

   **Andrej (2026-11-04, change):** I accept your suggestion.

   **Resolved (2026-11-04, Andrej):** set to missing (B): 96 and 98 in the three late-payment counters (269 rows) and
   the age of 0 (1 row) are missing in `_clean`, with a note in `curation_comments`, a CC line in the record, and
   `dataset check` re-run (0 errors, 0 warnings).

   **Andrej (2026-11-11, change):**

   **Resolved (2026-11-11, Andrej):** B again, and carried out on this branch, which did not yet have it:
   `LATE_COUNTERS` and `set_missing(df, {**{c: [96, 98] for c in LATE_COUNTERS}, "age": [0]})` are in `_clean`, with
   the note in `curation_comments`; `dataset check` passes (0 errors, 0 warnings).

   [^a1]: **LEAK-10** (Must) and **LEAK-37** (Must): a feature holds only what existed at the prediction point and
     never gives the target away; an input known at the prediction point is not a leak.
   [^a2]: **LEAK-18** (Should) and **LEAK-20** (Should): with few free features, plausible repeats are natural and
     stay; vectors with both labels stay when they are genuine ambiguity of the task.
   [^a3]: **CLEAN-14** (Should, amended 2026-10-31, Lennart): a code outside a scale that means unknown, or a state
     of its own in a column with no other missing value, is missing.
   [^a4]: Data dictionary in the competition download (https://www.kaggle.com/competitions/GiveMeSomeCredit/data);
     community treatments: https://github.com/aswanthiitm/pd-scorecard-engine (own bin),
     https://github.com/DrIanGregory/Kaggle-GiveMeSomeCredit (kept as a likely code).

   [^1a]: **CLEAN-10** (Should) and **CLEAN-14** (amended 2026-10-31, Lennart): a proxy missing code becomes a real
     missing value when the context shows the encoding; a level outside a scale that means unknown, or a state of its
     own in a column with no other missing value, is missing.
   [^1b]: **CLEAN-11** (Should): impossible values become missing, and the row stays.

2. **Keep the random split over borrowers, tagged as forced from temporal?**

   * **Problem:**
     - The file has no date, and its row id is not a time order: nothing changes along the 150,000 ids, and a model
       cannot tell low from high ids (ROC AUC 0.502).
     - No borrower is visibly repeated: the 1,000 rows in identical groups are empty credit files, and holding them
       out together scores the same as random folds (0.8647 against 0.8652).
     - By its use case the task is temporal (score new applicants with a model built on older ones), but with no
       dates the rules ship it random with the tag forced from temporal, which the definition lacks[^2a].
   * **Background:** the 11 columns are the target and 10 credit-file fields; the data dictionary lists no date, and
     neither file has one. Kaggle numbers its training file 1 to 150,000 and its test file 1 to 101,503, each on its
     own, so how the two files were cut cannot be read from the ids. The two files match: income missing in 19.8%
     of rows in both, medians equal to the third decimal.
   * **Experiments:** on Kaggle's cs-training.csv (re-downloaded 2026-11-04), cleaned as shipped, LightGBM on the 10
     features, ROC AUC:

     | Check | Result |
     |---|---|
     | Distress rate over 20 id bins | 6.3% to 7.3%, no trend (chi-squared p = 0.38); lag-1 correlation of the target in id order 0.0004 |
     | Features over the id | largest rank correlation 0.006; income missing 19.7% to 20.0% in every id quintile |
     | Model telling low from high ids (adversarial) | 0.502 (5 folds) |
     | Train on the first 80% of ids, test on the last 20% / the reverse | 0.870 / 0.864, against 0.860 to 0.870 for random 80/20 splits |
     | 5 folds: random / grouped by identical rows | 0.8652 / 0.8647 |
     | Identical rows | 1,000 rows in 354 groups (at most 12); 609 surplus copies with the same label, 148 rows in 37 groups with both labels |
     | What the identical rows are | utilisation 0 or 0.9999999 in all, debt ratio 0 in 98%, income missing in 85%, median 1 open line (8 overall); the copies of a group lie far apart in the file (median 67,026 ids) |
     | Same age, exact non-round income, dependents and real-estate loans (a person key) | 3,032 groups, 7,667 rows; utilisation identical in 0.6% of them, debt ratio in 0.4%: different people; a group's other rows predict a row's outcome no better than shuffled labels (0.498 against 0.504) |

   * **Effect on the task:** none on rows, splits or scores under B; the regime metadata and a note change.
   * **Consistency:** home_credit_default_risk, an undated credit table, ships random tagged forced from temporal;
     heloc's split issue and porto_seguro's issue 2 propose the same after the same tests (2026-11-04).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no tag (implemented) | nothing changes | none found | departs from the forced-split rule and the credit precedents; the score's temporal meaning is not stated |
     | B | Random, tagged forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`; a note says what a dated release would change | follows the rule and home_credit_default_risk; the leak test passes (no order effect, no repeated borrower, no hidden group) | none found |
     | C | Grouped by identical rows | copies of one empty credit file stay on one side | none found | the copies are different borrowers with the same empty file; scores the same (0.8647) |
     | D | Temporal by id | train on low ids, test on high ids | none found | the id is not time: the same as a random split under another name |

   * **Recommendation:** B: the data allows no temporal or grouped split, and the tag says what the random score
     stands for. **Decision:** random as now (A), random tagged forced from temporal (B), or grouped (C)?

   **Andrej (2026-11-04, discuss):** Are you sure that this is not a temporal or grouped data case?

   **Answer (AI, 2026-11-04):**

   * **Your question:** is the task really temporal or grouped?
   * **Temporal: yes by its use case, no in the data.**
     - A lender scores new applicants, so a dated release would call for a temporal split.
     - This release has no date column, and the id is not a time order. The distress rate and the features stay
       flat along it, and a model cannot tell low from high ids (0.502).
     - Training on the first 80% of ids scores 0.870 on the last 20%, inside the range of random splits (0.860 to
       0.870). No time order can be recovered, which is the forced-from-temporal case (B).
   * **Grouped: no.**
     - The 609 identical copies and the 37 groups with both labels are empty credit files, not repeated
       borrowers. They have no utilisation, no debt, mostly no income, one open line, and lie far apart in the file.
     - Holding identical rows out together scores the same as random folds (0.8647 against 0.8652)[^2b].
     - Borrowers sharing age, exact income, dependents and real-estate loans differ in every other field, and they
       do not share outcomes beyond chance (0.498 against 0.504).
     - 814 training rows match a row in Kaggle's test file. These are the same empty profiles, not leaked copies.
   * **Recommendation:** B. **Decision:** A, B or C?

   **Answer (AI, 2026-11-06):** the time framing, from today's review of how each dataset's data arrives.

   * The time basis (the tag and its `Time basis:` line) is now issue 3, and the record's missing collection facts
     issue 4, so this issue decides the split only: random borrowers (A and B are the same folds), grouped by
     identical rows (C) or by id (D).
   * How the data arrives supports the random split whichever way issue 3 ends: if the borrowers were scored on one
     date, every two-year window closed together and no test borrower is later than a training one; if they were
     scored over a period, the dates are lost and random is the closest regime that keeps the rows[^2c].
   * Neither reading makes the identical rows or the id a stand-in for time: the rows are empty credit files far
     apart in the file, and the id is no time order.

   **Notes for the AI:** scripts and output in `~/claude_jobs/ba_marks_1104/give_me_some_credit/split/` (`eda.py`;
   `cv.py`, `cv.sbatch`, `cv_1358228.out`, `cv.json`, Slurm job 1358228, cpuhigh32). The identical rows' leave-one-out
   group rate ranks at 0.723 against 0.509 for shuffled labels: that is the empty profile's risk (the 96/98 rows are 7.5%
   of them), which the features carry too, so grouping leaves the score unchanged. On B: add `ForcedIIDFromTemporal` to
   `data_tags` as home_credit_default_risk declares it; a split note in `curation_comments` (use case, no dates, ids
   not time, the numbers above); one sentence in `fit_reason`; `dataset check`; the record's CC line and Assessment.

   [^2a]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows ships
     in the closest regime that keeps the rows, tagged as forced from temporal; it ships only when a leak test across
     the split finds none (no shared outcome, no hidden group, no order dependence). **SPLIT-22** (Should): the raw
     file order can be the time order; here it is not.
   [^2b]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity new data would not have and the
     entity carries the label. **LEAK-18** (Should): with few free features, plausible repeats are natural and stay.
   [^2c]: **SPLIT-32** (Should): a delayed target from one shared prediction moment, its window closed for every row,
     is IID; a forward task whose time is lost is forced. **SPLIT-8** (Must): forced splits ship in the closest regime
     that keeps the rows.

   **Resolved (2026-11-09, Andrej):** B: the random split stays, tagged `ForcedIIDFromTemporal` in `data_tags`, with a
   sentence in `fit_reason`; the split note is issue 3's `Time basis:` line.

   **Andrej (2026-11-11, change):** Option B: Random, tagged forced from temporal.

   **Resolved (2026-11-11, Andrej):** B again, and carried out on this branch: `data_tags =
   ("ForcedIIDFromTemporal",)` and the sentence "the random split is tagged as forced from temporal" in
   `fit_reason`; the split itself is unchanged.

3. **Time basis: forced from temporal, or a delayed target from one scoring date?**

   * **Problem:**
     - The release never says when the borrowers were scored, on one date for the whole book or one by one over a
       period, and the data cannot tell, as it keeps no time (a model tells low from high ids at ROC AUC 0.502).
     - The record carries no collection facts (issue 4), and the definition names no time basis.
     - Name the random split forced from temporal (scored over a period whose dates are lost) or a delayed target
       (one scoring date, every two-year window closed)?
   * **Background:** the questions that tell the time bases apart[^3a]:
     - Can time affect the target? Yes: serious delinquency follows the credit climate; the two-year windows ended
       before the release of September 2011, so the scoring dates lie before about September 2009, and windows that
       close near the release span the financial crisis.
     - Does the use case predict for a time after its data? Yes: "Credit scoring algorithms ... are the method banks
       use to determine whether or not a loan should be granted" (the competition's overview).
     - One shared prediction moment? Unknown, and this decides the basis. One scoring date gives a delayed target:
       no test borrower is later than a training one, so time cannot reach a target through other borrowers, and what
       the split cannot test is the next scoring date. Scoring over a period whose dates are lost gives the forced
       tag[^3b].
     - The sources lean to a period: the overview speaks of granting loans and of "Historical data ... on 250,000
       borrowers", not of one portfolio date; the fields (open lines, utilisation, delinquencies of the last two
       years) fit either.
   * **Experiments:** the leak test across the split is issue 2's table: no order along the id, identical rows are
     empty credit files that score the same held out together (0.8647 against 0.8652), and borrowers sharing a person
     key share no outcome beyond chance. Nothing in the data can date a borrower.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | no time tag; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the score's meaning in time is not stated |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line: borrowers scored over an unstated period before about 2009, the dates lost | claims no shared date the sources do not state; follows heloc's proposal and home_credit_default_risk | if the book was scored on one date, the tag overstates what is lost |
     | C | Delayed target | the tag `DelayedTarget` and a line naming one scoring date and the two-year window | if true, says the random split is the right one, not a stand-in | asserts a shared scoring date no source states |

   * **Recommendation:** B: the use case scores loan applicants and the sources state no shared date, so the forced
     tag claims only what is known; C if the sponsor's documentation turns up one date. **Decision:** no time basis
     (A), forced (B) or delayed target (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("ForcedIIDFromTemporal",)` and the curation bullet
   "- Time basis: ForcedIIDFromTemporal: borrowers of an unnamed lender scored at dates the competition does not
   state (before about September 2009, as the two-year windows closed before the release of September 2011), each
   followed for two years; the release keeps no date and the row id is no time order (a model tells low from high
   ids at ROC AUC 0.502), so random borrowers stand in for the borrowers to come. A dated release would allow a split
   by scoring date."; on C: `data_tags = ("DelayedTarget",)` and "- Time basis: DelayedTarget: one scoring date of
   the lender's book (<the source>), serious delinquency within the following two years, the window closed for every
   borrower."; no `splits_comment` (default split). The record's facts follow issue 4.

   [^3a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     a definition can name the use-case prototype it follows (`Timeless`, `Snapshot`, `DelayedTarget`,
     `StationaryRelation`) with a `Time basis:` line stating the fact behind it; a delayed target needs one shared
     prediction moment and a window closed for every row; a forward task whose time is lost is forced.
   [^3b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split; it says
     what a dated release would change.

   **Resolved (2026-11-09, Andrej):** B: forced from temporal; the `Time basis: ForcedIIDFromTemporal:` bullet is in
   `curation_comments`. Andrej added: "Maybe we should also update our guidelines to say that forced applies if we don't
   have enough evidence for how the data was collected." SPLIT-32 in PR #50 now says so: a forward use case whose source
   does not show how the data was collected takes the forced tag.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   Maybe we should also update our guidelines to say that forced applies if we don't have enough evidence for how the
   data was collected.

   **Resolved (2026-11-11, Andrej):** B again, and carried out on this branch: the `Time basis:
   ForcedIIDFromTemporal:` bullet is in `curation_comments` (no scoring date in the release, the row id is no time
   order at ROC AUC 0.502, a dated release would allow a split by scoring date). The guideline wording is not in this
   branch's rules: the files under `knowledge-curation/references/` were not edited here, and the SPLIT-32 sentence
   that carries it rides with PR #50. Whoever lands that change should take the wording above.

4. **Correct the record's collection facts?**

   * **Problem:**
     - The record carries no collection facts at all, while the other undated credit tables carry them (heloc:
       `Samples: Over Time`, `Time: Lost`, `Target: Later`).
     - The target is known only after a fixed window, serious delinquency within two years of the scoring date, so
       `Target: Later` holds either way; whether the samples arose over time is issue 3's open point.
     - Set `Samples: Over Time`, `Time: Lost` and `Target: Later`?
   * **Background:** the record describes the source by independent collection facts; a target after the features
     at one shared date or after a fixed window is `Target: Later`; samples over a period whose time the release
     cannot give are `Samples: Over Time` with `Time: Lost`, one extract is `Samples: One Moment`[^4a]. Nothing in the
     data can decide between the two: no date, no time order (issue 2).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | no collection facts | nothing changes | the record says nothing of how the data arrived |
     | B | Over time, lost, later | `Samples: Over Time`, `Time: Lost`, `Target: Later` | matches heloc and the forced reading of issue 3 | a reading of the sources, not a statement in them |
     | C | One moment, later | `Samples: One Moment`, `Target: Later` | matches the delayed-target reading of issue 3 | asserts a shared scoring date no source states |

   * **Recommendation:** B, with issue 3's B; C goes with issue 3's C. **Decision:** keep (A), over time (B) or one
     moment (C)?

   **Notes for the AI:** on B, add to the record's `tags`: `'Samples: Over Time'`, `'Time: Lost'`, `'Target:
   Later'`; on C, `'Samples: One Moment'` and `'Target: Later'`. `Andrej` is already in `checked_by`.

   [^4a]: **SPLIT-32** (Should): the record describes the source by independent collection facts: `Samples: No Time
     Dimension`, `Samples: One Moment` or `Samples: Over Time`; `Time: Dated` or `Time: Lost` for samples over time;
     `Target: Later`, `Target: Varying Delay` or `Target: Revised Later`.

   **Resolved (2026-11-09, Andrej):** B: the record's `tags` carry `Samples: Over Time`, `Time: Lost` and `Target:
   Later`.

   **Andrej (2026-11-11, change):** Option B: Over time, lost, later.

   **Resolved (2026-11-11, Andrej):** B again, and carried out on this branch: the record's `tags` are now
   `Samples: Over Time`, `Time: Lost` and `Target: Later` (it had none).

## Reference

https://www.kaggle.com/competitions/GiveMeSomeCredit/overview
