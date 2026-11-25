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
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 1
tags:
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- Dated Event Log
original_source: Kaggle
year: '2020'
collection_period: Unknown
required_split:
- Random (IID)
problem_type: Binary Classification
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

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `education` (the README lists their levels).

CC (2026-11-01, Lennart): decided in the dtype review of PR #37: month stays a number (a position in the year's continuous cycle, shipped as a number: the curator's cycle rule).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: a Kaggle upload of 1,723 point-of-sale consumer loans with no named lender and an undefined 'bad' label, kept under the source-gap rule by the curator; the rows look real and methods separate (0.244 to 0.270 1-AUC). Priority 1: gap 0, use case 0, source 0, shape 1, risk -1.

CC (2026-11-10, Andrej): decided: time basis (issue 2, option B): random as a stationary relation; the `Time basis: StationaryRelation:` bullet is in `curation_comments` (twelve months in file order, flat bad rate, monthly windows score as random splits); the tag enters `data_tags`. Collection facts (issue 3, option B): `Time: Dated` in place of `Time: Lost`, `Target: Varying Delay` added. Split unchanged.

CC (2026-11-11, Andrej): kept, with a note on `family_status` (Review issue 1, b): no mark of generated data was found, and the gap in source and label stays in the approximate fit. `family_status` is independent of every other column, age included, and is kept as recorded with a curation note.

CC (2026-11-18, Andrej): Review issue 4, A, as implemented: Random 3-fold CV, 10 repeats (1,148-1,149 train / 574-575 test loans), `StationaryRelation`.

CC (2026-11-18, Andrej): verdict ship (blind split walk).

CC (2026-11-18, Andrej): the declared split (random, 10x3 folds, `StationaryRelation`) is checked: confirmed in the blind split walk.

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
2026-11-10; the relation measured flat across the months and the random folds kept (issue 4, A, 2026-11-18).

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
   * Runs: LightGBM, 5 folds grouped by row id, 3 shuffles.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Keep (implemented) | as issue 1's A | real-data marks throughout; methods separate | source and label undefined |
   | b | Keep, note `family_status` | a, and a curation bullet: the column is independent of every other column, age included | states the one oddity | none found |
   | c | Retire as generated | `No (Retired)` | none found | no mark of generation was found |

   * **Recommendation:** b: real data with one noise-like column, kept as recorded. **Decision:** a, b or c?

   **Resolved (2026-11-11, Andrej):** b ("Reply (b): Keep, note family_status"): kept with the gap in the fit; a
   `curation_comments` bullet says no mark of generation was found and that `family_status` is independent of every
   other column, age included, and kept as recorded. A CC line in the record. Text only, data unchanged.

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

   **Notes for the AI:** on B: `data_tags = ("StationaryRelation",)` and the curation bullet
   "- Time basis: StationaryRelation: loans of twelve consecutive months; the uploader's file is in month order
   (`month` 1 to 12 once, rank correlation with the row 0.996), and over the months the bad rate stays flat (6.2% to
   15.4%, chi-squared p = 0.35) and five monthly windows, each trained on all earlier months, score as random splits
   of the same sizes (ROC AUC 0.737 against 0.728, untuned LightGBM; 0.739 against 0.731, logistic regression). A
   split by month could not wait for the labels: the bad mark comes after a delay the source does not state, about a
   loan term."; the `split` text stays. On C: build a month date in `_clean` (the month as the period of a nominal
   year), `temporal = Temporal(on=<that column>, splits=TemporalSplits(window=1, unit="months", n_windows=5))`, a
   `splits_comment` on the missing gap, record `required_split` `Temporal (NON-IID)`. On D: `data_tags =
   ("ForcedIIDFromTemporal",)` with a line naming the unstated period. Record facts: issue 3.

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
   Split unchanged. The tag `StationaryRelation` enters `data_tags`.

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
   `Target: Varying Delay`, in the working copy.

4. **Split: measure the relation across the twelve months, then keep the random folds (StationaryRelation) or hold out whole months?**

   * **Problem:**
     - The definition has measured it: five monthly windows, each trained on all earlier months, score as random splits of the same sizes (ROC AUC 0.737 against 0.728 untuned LightGBM, 0.739 against 0.731 logistic regression), so the relation is flat and the tree gives random folds tagged `StationaryRelation`, as shipped.
     - No windows survive a label-delay gap: the only date is `month` 1-12 with no year, and the bad mark comes about a loan term later (credit_term median 12 months).
     - One row per loan and no customer id, so a flat relation gives random rather than grouped folds.
   * **Background:** A forward-scored loan task whose only date is a month 1-12 and whose label needs the loan term (median 12 months) to mature, so no temporal windows survive the gap. The forced step leaves random if the relation is measured flat across months (the bad rate already is, p=0.35), else whole-month periods held out. Confidence of the blind walk: medium.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Used at a place or group the data does not hold? (use case): no. Evidence: Dossier use case: a lender decides on each arriving application; no new region or lender named. region has 3 codes only.
     - Fill in the covered period or predict forward? (use case): forward. Evidence: A loan application after the data is scored.
     - Do the dates give the windows the rule[^split-14]/15 ask for (after the gap)? (data): no. Evidence: Only `month` 1-12, no year (OpenML 43442 arff, 1,723 rows, 116-174 rows and 9-25 positives per month). 'Bad customer' is known only after the loan runs: credit_term median 12 months (25% 6, max 36). A gap of about the delay (months, above the 1-month step, the rule[^split-10]) leaves no window above the 50% floor in a 12-month span. Also the 12 months are 'consecutive' but month 1 is not shown to be the…
     - ForcedFromTemporal: can the arrival order be reconstructed from the data? (data): no. Evidence: No id or date beyond month; the file is near-sorted by month (26 drops in 1,723 rows), nothing finer to check against.
     - Windows failed only for too few positives in a non-stationary sequence? (data): no. Evidence: They fail for the gap/too short span, not positives (each month holds 9-25 positives). Bad rate by month: chi2=12.2, df=11, p=0.35, flat.
     - Reason to treat later samples as interchangeable? (measurement): measurement needed. Evidence: Measure whether the target and its relation to the features are flat across the 12 months (e.g. train on months 1-6 vs 7-12, compare with in-period CV; the label rate alone is already flat, p=0.35). No person's reason is given; I answer no for Assumed.
     - Unit with several rows and new units in use? (data): no. Evidence: No customer id; no exact duplicate rows (0). One row per loan.
   * **The measurement:** Relation of bad_customer to the features flat across months (12 months, two halves or month blocks), measured on the 12-month span.
   * **What each outcome gives:** flat → Random · StationaryRelation; not flat → Grouped · ForcedGroupedFromTemporal (periods): whole month blocks held out (month is an order with >=2 periods).
   * **What the blind dossier lacked, and what it changes:** none: the definition already holds the measurement my Phase A asked for: five monthly windows score as random splits of the same sizes (ROC AUC 0.737 vs 0.728 LightGBM, 0.739 vs 0.731 LR) and the bad rate is flat (p=0.35), so the 'flat' branch holds. Shipped split: random, tag StationaryRelation. Round 1's blind leaf was a temporal label-delay leaf.
   * **What changes:** nothing in the definition until the measurement is run; then the leaf it gives decides, and only a split that differs from the shipped one needs a rebuild.
   * **Source split:** no. No split prescribed.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: split_tree.md lists bad_customer_detection as an example under the forward/'dates give windows: no' ForcedFromTemporal pointer and under 'Random · StationaryRelation'; ignored. Type itself is plausible (loans with a month number), though the 'date' is only a month 1-12 with no year.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random 3-fold CV, 10 repeats (1,148-1,149 train / 574-575 test loans), `StationaryRelation` (implemented) | No change; the measurement is already in the `Time basis:` line. | Rests on a measured flat relation over the twelve months; 30 test folds of 574 loans. | Loans of a later year or another credit climate stay untested; the file covers twelve months of one lender. |
     | B | If the relation is not flat: grouped CV over whole months of `month` (12 months of 116-174 loans and 9-25 bad customers each; fold layout not set), `ForcedGroupedFromTemporal` | `dataset.py` declares a `grouping` on `month`; `data_tags` becomes ForcedGroupedFromTemporal; the `Time basis:` line gives the measured shift. | Holds whole months out where a shift between months would show. | The definition's windows score as random splits, so the measurement does not point here; folds train on later months to test earlier ones. |

   * **Recommendation:** A, because the definition's window-against-random measurement shows the relation flat across the months.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: run the named check (CPU job), write the number into the `Time basis:` line, then apply the leaf it gives.

   [^split-14]: **SPLIT-14** (Must): A temporal task has at least 3 windows.

   [^split-10]: **SPLIT-10** (Should): When a label is known only some time after its row (a delivery time, a permit's processing time, an outcome after a follow-up), a model refit at a window's start knows only the rows whose label had arrived.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Answer (AI, 2026-11-18):** Scored on the same test loans, models trained on the earlier months match models trained on a sample that includes the test month, in each of the three newest months: the relation is flat, which reverses the earlier "not flat".

   - Twelve months of loans, in file order and without a year. The bad rate moves between 6.2% and 15.4% (p = 0.35 over all months). The largest pairwise change, month 7 against month 12 (factor 2.5), has p = 0.017, short of the 0.01 that a recording change needs. `month` is left out of the features.
   - In each window the test set is a random half of the month (80 to 87 loans, 5 to 15 of them bad). No window is not-flat for either model. Kumo-Tabular's gaps are at most +0.005 ± 0.007; LightGBM's are noise (SD 0.02 to 0.08).
   - The earlier "not flat" (forward 0.06 to 0.11 below random) scored the forward and random models on different loans, and it kept `month`, which takes an unseen value in every forward test. On the same loans the gap is gone.
   - Thin: the comparison models differ from the forward ones by only about 80 loans of the test month (5% to 6% of their rows), so only a strong change in that month would show.

   | Test period | Model | Train / test rows | Forward | Contemporaneous | Gap ± SD | Floor | Flat? |
   |---|---|---|---|---|---|---|---|
   | 12 | LightGBM | 1,561 / 81 | 0.675 | 0.675 | -0.0008 ± 0.0174 | 0.0017 | yes |
   | 12 | Kumo-Tabular | 1,561 / 81 | 0.723 | 0.729 | +0.0054 ± 0.0072 | 0.0023 | yes |
   | 11 | LightGBM | 1,387 / 87 | 0.661 | 0.641 | -0.0196 ± 0.0468 | 0.0014 | yes |
   | 11 | Kumo-Tabular | 1,387 / 87 | 0.717 | 0.721 | +0.0043 ± 0.0140 | 0.0022 | yes |
   | 10 | LightGBM | 1,227 / 80 | 0.745 | 0.679 | -0.0661 ± 0.0781 | 0.0018 | yes |
   | 10 | Kumo-Tabular | 1,227 / 80 | 0.821 | 0.814 | -0.0071 ± 0.0099 | 0.0031 | yes |

   **Verdict: flat.** Leaf: random loans as a stationary relation (`StationaryRelation`), as recorded on 2026-11-10.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: Random 3-fold CV, 10 repeats (1,148-1,149 train / 574-575 test loans), `StationaryRelation`.

## Reference

https://www.kaggle.com/datasets/podsyp/is-this-a-good-customer
