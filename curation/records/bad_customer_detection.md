---
unique_name: bad_customer_detection
name: Is-this-a-good-customer / bad_customer_detection
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
- 'Time: Dated'
- 'Target: Varying Delay'
original_source: Kaggle
year: '2020'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=43442
- https://www.kaggle.com/datasets/podsyp/is-this-a-good-customer
notebook_path: datasets/beyond_iid/old_iid/bad_customer_detection/bad_customer_detection.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/bad_customer_detection/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Seems to be an imbalance fraud detection task, but not much information on source given.

Potential issue: -

Lennart: No objection

Andrej: Need to clarify source

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Kaggle dataset (not a competition) with no stated task metric; the original source is unknown (open item in the record).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `education` (the README lists their levels).

CC (2026-11-01, Lennart): marks on the review board of PR #37: month stays a number (a position in the year's continuous cycle, shipped as a number: the curator's cycle rule).

CC (2026-11-11, Andrej): review marks on the three issues, applied to the definition and the record.

- Issue 1 ("Reply (b): Keep, note family_status"): kept, with the gap in the source written into the approximate fit (PROV-1, PROV-2). The search for marks of generated data found none: no rule on the row number (all 13 columns at the shuffled level), no repeated rows, structural zeros only where lending policy explains them, complete integer ranges, and 9 of 13 columns tied to the rest of the row, as in real credit data. The one oddity, `family_status`, is independent of every other column, age included (shuffle-test ROC AUC 0.488; 27% married at 18 to 22 and at over 60; unrelated to children, p = 0.9); it does not separate the classes (p = 0.1) and is kept as recorded. A `curation_comments` bullet says so.
- Issue 2 (change, Option B): `data_tags = ("StationaryRelation",)` with its `Time basis:` bullet: the file runs once through twelve consecutive months in order (rank correlation with the row 0.996), the bad rate stays flat over them (6.2% to 15.4%, chi-squared p = 0.35) and five monthly windows, each trained on all earlier months, score as random splits of the same sizes (ROC AUC 0.737 against 0.728, untuned LightGBM; 0.739 against 0.731, logistic regression). A split by month could not wait for its labels, since the bad mark comes after a delay the source does not state (SPLIT-10, SPLIT-32). Folds unchanged.
- Issue 3 (change, Option B): the record's `tags` now read `Time: Dated` in place of `Time: Lost` and gain `Target: Varying Delay`, as for credit_g.
- Rows, features and the metric unchanged; not rebuilt. The review moved from the folder's `REVIEW.md` into this record's `## Review` section.

## Review

**Outcome:** added. The AI recommends shipping it as defined, with the gap in its source kept as the curator decided
(issue 1). Reviewed on 2026-11-04 without a panel, from the evidence already gathered (the record, model
runs on the shipped data and on the TabArena v0.1 task of the same source). The data are a Kaggle upload ("Is this a
good customer?", podsyp, 2020) of 1,723 consumer loans for goods such as phones and appliances, with 13 fields of the
application, and the target is whether the client was marked bad (11.4%). The uploader names no lender, country or
period and does not define "bad"; the curator kept it on 2026-10-14 as a plausible source unclear in a detail, with
the gap written into an approximate fit. Validity: the rows look like real applications (no duplicate rows, no signal
in the row order, 72% of incomes typed on a round grid, 2 bad loans among the 117 clients aged 60 or more, an age at
which pensions start), and every field is known when the application arrives; the one recording pattern found,
incomes typed as exact figures (15.3% bad) rather than on the round grid (9.9% bad), is written at the application,
before any outcome exists, so it is a property of the applicant and not a class-dependent recording. Value: the 40
benchmark methods spread from 0.244 1-AUC (LimiX-2, EXAONE) over 0.248 (TabPFN-3.5) and 0.249 (tuned CatBoost) to
0.263-0.270 (logistic regression); a hand-built logistic score with a separate slope set for phone loans reaches
0.227, so the task is close to an additive score, but methods separate. Quality: nothing found. Weighed:
real-looking application data and a clear decision +, methods separate +, an undefined label and an anonymous
source -.

**Main points:** all issues resolved: kept with a note on `family_status`, no mark of generated data (issue 1,
2026-11-11); random as a stationary relation (issue 2) and the record's time dated with a varying delay (issue 3),
2026-11-10.

**Record judgment:** valid with a known gap, ship. The label has no stated definition or horizon, which the fit
already says.

**Issues for Andrej:**

1. **Keep it although the lender, the period and the meaning of "bad" are unknown?**

   * **Problem:**
     - The Kaggle upload names no lender, country or period and does not say what makes a client bad or by when, which your note on the record ("Need to clarify source") asked to settle.
     - No upstream has turned up since, and the curator kept the dataset on 2026-10-14 with the gap written into an approximate fit.
     - Keep it on that basis, or retire it for missing source information?
   * **Background:** a dataset whose every link ends at an anonymous upload is out, unless the data look sound and
     the upload itself is a source to point to; then the gap is taken knowingly and written into the fit[^1a]. The
     rows show the marks of real application data listed in the outcome and none of generated data.
   * **Effect on the task:** a model learns whatever the uploader's "bad" means, over an unknown horizon; the
     decision (grant a point-of-sale loan) is clear.
   * **Consistency:** follows tour_travels_churn and mobile_churn, bare Kaggle uploads kept the same way
     (2026-10-21); water_quality_and_potability, retired for its source, turned out to be generated data[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, gap in the fit (implemented) | 1,723 loans as uploaded; the fit says what is unknown | real-looking application data; methods separate; the curator's call of 2026-10-14 | the label's meaning and horizon stay unknown |
     | B | Retire | record `No (Retired)` with `Missing source information`; folder removed | no task with an undefined label | loses a small consumer-credit task; departs from the uploads kept the same way |

   * **Recommendation:** A, as the curator decided: the data pass every check for real data, and the gap is written
     down. **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** on B, the record's CC line, `No (Retired)` with `Missing source information`, folder
   removal, `v2_path` cleared and a CHANGELOG entry.

   [^1a]: **PROV-1** (Must) and **PROV-2** (Should; amended 2026-10-21, Lennart): an origin that cannot be traced is
     `No` after a thorough search, but an upload whose first platform cannot be traced is kept, case by case, when
     the data look sound and there is a source to point to, with the gap written as an approximate fit.
   [^1b]: **PROV-2** cases: bad_customer_detection kept as a plausible source unclear in a detail (2026-10-14,
     Lennart); tour_travels_churn and mobile_churn kept (2026-10-21, Lennart). **PROV-3** case:
     water_quality_and_potability stays `No`, its first upload calls itself synthetically generated (2026-10-22).

   **Andrej (2026-11-10, discuss):** I fear that this dataset might have been artificially generated. Do all you can to
   find whether this is the case.

   **Answer (AI, 2026-11-10):** not generated. None of the marks found on tour_travels_churn and bank_customer_churn
   appear, and the within-class shuffle test reads like the real credit_g. One column, `family_status`, is tied to
   nothing and looks like noise.

   | Mark of a generator | tour_travels_churn / bank_customer_churn | bad_customer_detection |
   |---|---|---|
   | Rules on the row number (best fit of `k mod m`, m 2 to 200) | every column but age | none: all 13 columns at the shuffled level (label 0.887 against 0.888) |
   | Repeated rows | 53% of tour rows | none, also without `month` |
   | Structural zeros (empty cells, 5 or more expected) | high income only with frequent flyer | 8, all lending policy: phones never on 24 or 36 months, cosmetics never on 6, no 36-month loan under 21,500 |
   | Gaps in integer columns | no 32-year-olds | ages 18 to 81 complete; terms heap at 6, 10, 12, 18, 24 and 36 months |
   | Columns tied to the rest of the row (shuffle test ROC AUC above 0.53) | 3 of 10 (bank) | 9 of 13 (0.56 to 0.68) |
   | The same test on real credit_g / on a copy shuffled within class | | 18 of 20 (0.54 to 0.70) / 0.46 to 0.49 |

   * **Dependencies a world shows:** children by age are 15% up to 25 and 69% at 36 to 45, then fall. Incomplete higher
     education has a median age of 24. Amount correlates with term (Spearman 0.52) and with income (0.37), and income
     differs by region.
   * **Row order:** the file runs through the months in blocks that interleave at their boundaries, which looks like an
     export sorted by date, not a sampler.
   * **At chance in the shuffle test:** `family_status` 0.488, `phone_operator` 0.490, `month` 0.514, `is_client` 0.521.
     The month and the operator can well be independent.
     `family_status` cannot: 27% are married at 18 to 22 and 27% at over 60, and it is unrelated to children (p 0.9). It
     looks scrambled or meaningless, but it does not separate the classes (p 0.1).
   * **Marks of rounding or anonymising, not of generation:** every amount is a multiple of 500, and 72% of incomes lie
     on a 5,000 grid shifted by 1,000 (21,000, 26,000, ...).
   * **Provenance:** the first and only upload is podsyp's of 2020-04-16 (CC0, no source stated). A GitHub code search
     for `bad_client_target` finds only later copies (OpenML, TabArena, student projects).
     The uploader's other 10 datasets are company tasks and work data (an IT company's hiring test, a roasting machine,
     an extrusion line, his own craft-beer bar in Yekaterinburg), none described as generated.
   * Scripts `~/claude_jobs/marks_1110/bad_customer_detection/marks.py` and `shuffle.py` (LightGBM, 5 folds grouped by
     row id, 3 shuffles).

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Keep (implemented) | as issue 1's A | real-data marks throughout; methods separate | source and label undefined |
   | b | Keep, note `family_status` | a, and a curation bullet: the column is independent of every other column, age included | states the one oddity | none found |
   | c | Retire as generated | `No (Retired)` | none found | no mark of generation was found |

   * **Recommendation:** b: real data with one noise-like column, kept as recorded. **Decision:** a, b or c?

   **Andrej (2026-11-11, discuss):** Reply (b): Keep, note family_status

   **Resolved (2026-11-11, Andrej):** b ("Reply (b): Keep, note family_status"): kept with the gap in the fit; a
   `curation_comments` bullet says no mark of generation was found and that `family_status` is independent of every
   other column, age included, and kept as recorded. A CC line in the record. Text only, data unchanged. The bullet is
   now in the definition on this branch as well, with the generator checks it rests on (no rule on the row number, no
   repeated rows, structural zeros only of lending policy, complete integer ranges, 9 of 13 columns tied to the rest
   of the row).

2. **Time basis and split: keep the random split as a stationary relation, or split by month?**

   * **Problem:**
     - The uploader's file runs once through twelve consecutive months in order (`month` 1 to 12, rank correlation
       with the row position 0.996, every change between neighbouring rows a step of one month, no row more than 30
       rows from its month's block), so the loans are dated to the month.
     - The record says `Time: Lost` and the definition names no time basis, because the earlier check of the row order
       ran on the shipped BeyondArena frame, which was shuffled at build.
     - Over the twelve months the bad rate stays flat and a model trained on earlier months scores later months as
       random splits do: keep random as a stationary relation, or split by month?
   * **Background:** the questions that tell the time bases apart[^2a]:
     - Can time affect the target? Yes in general: a credit climate or a changed lending policy moves defaults.
     - Does the use case predict for a time after its data? Yes: the lender decides on new applications.
     - One shared prediction moment? No: each loan at its own application; the bad mark follows after a delay the
       uploader does not state (terms run 3 to 36 months, median 12).
     - Does arrival over time move the target? Measured on the months below: no, which is what a stationary relation
       states on a dated source.
     - Why the month reads as time: a month of the year over several years, sorted by date, would cycle through 1 to
       12 several times, and a file sorted by the month column alone would have no inversions; one pass with
       neighbouring months interleaved at their boundaries is a file sorted by a date or an id over one year.
     - A split by month cannot wait for the labels: a model refit at a month's start would not yet know whether the
       previous months' loans went bad, and a gap of one loan term (a year) leaves no training data[^2b].
   * **Experiments:** today's checks on the uploader's `clients.csv` (re-downloaded):
     - Bad rate per month 6.2% to 15.4%, no trend (chi-squared p = 0.35; rank correlation with the month 0.02).
     - Five one-month windows (months 8 to 12, each trained on all earlier months, 55% to 91% of the loans; 136 to
       174 loans and 13 to 25 bad ones per window), against random splits of the same sizes (20 draws), ROC AUC:

     | Model | Windows, mean (range) | Random, same sizes, mean |
     |---|---|---|
     | LightGBM, untuned | 0.737 (0.640 to 0.821) | 0.728 |
     | Logistic regression | 0.739 (0.674 to 0.842) | 0.731 |

     - The leak test across a random split[^2c]: no copy of a loan, no row order left in the frame, the month is a
       feature and carries no period effect (flat rate above); whether one customer holds several loans cannot be
       seen.
   * **Unknown:** the year, the lender and what makes a client bad by when (issue 1); a lender or an uploader's
     statement that the twelve months are one year would settle the reading.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | no time tag; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the months in the file go unmentioned |
     | B | Random as a stationary relation | the tag `StationaryRelation` and a `Time basis:` line with the twelve months and the measurements above | the measured fact behind the random split is written down; no fold changes | rests on reading `month` as twelve months of one year, which no source states |
     | C | Five monthly windows | `month` becomes the time column; months 8 to 12, each trained on all earlier months | tests later loans, as a lender scores them | no gap is possible, so training uses labels a refit would not have; 13 to 25 bad loans per window; the windows score as random splits do |
     | D | Random, forced from temporal | the tag `ForcedIIDFromTemporal` and a line saying the period is unstated | claims no time order | ignores a time order the file shows |

   * **Recommendation:** B: the file keeps the month, the bad rate and the relation are flat across it, and a split by
     month could not wait for its labels. **Decision:** no time basis (A), stationary relation (B), monthly windows
     (C) or forced (D)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("StationaryRelation",)` and the curation bullet
   "- Time basis: StationaryRelation: loans of twelve consecutive months; the uploader's file is in month order
   (`month` 1 to 12 once, rank correlation with the row 0.996), and over the months the bad rate stays flat (6.2% to
   15.4%, chi-squared p = 0.35) and five monthly windows, each trained on all earlier months, score as random splits
   of the same sizes (ROC AUC 0.737 against 0.728, untuned LightGBM; 0.739 against 0.731, logistic regression). A
   split by month could not wait for the labels: the bad mark comes after a delay the source does not state, about a
   loan term."; the `split` text stays. On C: build a month date in `_clean` (the month as the period of a nominal
   year), `temporal = Temporal(on=<that column>, splits=TemporalSplits(window=1, unit="months", n_windows=5))`, a
   `splits_comment` on the missing gap, record `required_split` `Temporal (NON-IID)`. On D: `data_tags =
   ("ForcedIIDFromTemporal",)` with a line naming the unstated period. Record facts: issue 3. Evidence:
   `~/claude_jobs/time_review/bad_customer_detection/` (`scripts/order.py`, `order.txt`, `scripts/temporal.py`,
   `temporal.json`; Slurm job 1366161, cpuhigh32).

   [^2a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     a definition can name the use-case prototype it follows with a `Time basis:` line; a stationary relation on a
     dated source is measured (the target and its relation to the features flat across periods, a temporal split
     costing nothing). **SPLIT-22** (Should): the raw file order can be the time order without a timestamp.
   [^2b]: **SPLIT-10** (Should): when a label is known only some time after its row, a refit at a window's start knows
     only the rows whose label had arrived; the gap is part of the task. **SPLIT-14** (Must): at least 3 windows,
     none trained on less than half of the data.
   [^2c]: **SPLIT-8** (Must): a split that stands in for time gets a leak test across it: a row's, its unit's or its
     period's outcome shared with the other side, a hidden group, an order dependence.

   **Resolved (2026-11-10, Andrej):** B, random as a stationary relation: the drafted `Time basis: StationaryRelation:`
   bullet is in `curation_comments`, ending with what the split cannot test (a later year or another credit climate).
   Split unchanged. The tag `StationaryRelation` enters `data_tags` once PR #50 is in the working copy.

   **Andrej (2026-11-11, change):** Option B: Random as a stationary relation.

   **Resolved (2026-11-11, Andrej):** B, now complete on this branch, which carries PR #50: `data_tags =
   ("StationaryRelation",)` beside the `Time basis: StationaryRelation:` bullet (the twelve months in the file's own
   order, the flat bad rate, the five monthly windows that score as random splits of the same sizes, and why a split
   by month could not wait for its labels). Folds, rows and features unchanged.

3. **Correct the record's collection facts?**

   * **Problem:**
     - The record says `Time: Lost`, but the uploader's file keeps the month and runs through twelve consecutive
       months in order (issue 2).
     - The record has no `Target:` fact, though the bad mark comes after the loan, at a delay the uploader does not
       state.
     - Set `Time: Dated` and `Target: Varying Delay`?
   * **Background:** a source is dated when it keeps the time or lets us recover it, an order that tracks time or a
     value that encodes the period included; a target that arrives after a delay that differs between samples (a
     default comes when it comes, within terms of 3 to 36 months) is a varying delay, and a later target at one shared
     date or after a fixed window, which the uploader does not state, would be `Target: Later`[^3a].
   * **Consistency:** credit_g, also a consumer credit without a stated horizon, carries `Target: Varying Delay`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the facts (implemented) | `Samples: Over Time`, `Time: Lost`, no target fact | nothing changes | contradicts the file's month order; the late label goes unrecorded |
     | B | Dated, varying delay | `Time: Dated` in place of `Time: Lost`; `Target: Varying Delay` added | matches the file and credit_g | the month as time rests on the file's order, not on a statement of the uploader |
     | C | Dated, later | `Time: Dated`; `Target: Later` | a mark read at one date would fit it | no read date or window is stated |

   * **Recommendation:** B. **Decision:** keep (A), dated with a varying delay (B), or dated with a later target (C)?

   **Notes for the AI:** on B, in the record's `tags`: replace `'Time: Lost'` with `'Time: Dated'` and add
   `'Target: Varying Delay'`; `Andrej` is already in `checked_by`. On C, `'Target: Later'` instead.

   [^3a]: **SPLIT-32** (Should): the record describes the source by independent collection facts: `Samples:`,
     `Time: Dated` or `Time: Lost` for samples over time, and `Target: Later`, `Target: Varying Delay` or `Target:
     Revised Later`, with no target fact when the target exists with the features.

   **Resolved (2026-11-10, Andrej):** B: the record's `tags` have `Time: Dated` in place of `Time: Lost` and gain
   `Target: Varying Delay`, in the working copy and in the PR #50 worktree's copy of the record.

   **Andrej (2026-11-11, change):** Option B: Dated, varying delay.

   **Resolved (2026-11-11, Andrej):** B, applied to this branch's copy of the record, which still had the old facts:
   `tags` now read `Samples: Over Time`, `Time: Dated`, `Target: Varying Delay`. The file keeps the month and runs
   through twelve consecutive months in order, and the bad mark comes after a delay the uploader does not state, as
   for credit_g.

## Reference

https://www.kaggle.com/datasets/podsyp/is-this-a-good-customer
