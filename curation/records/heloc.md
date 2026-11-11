---
unique_name: heloc
name: heloc
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Class-dependent Recording
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
original_source: Other
year: '2018'
required_split:
- Random (IID)
source_links:
- https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc
notebook_path: datasets/beyond_iid/old_iid/heloc/heloc.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/heloc/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Default prediction

Potential issue: preprocessing

Lennart: Likely include a version of the original data; likely time invariant

Andrej: Use the most extensive data version

**Assessment (AI, 2026-10-19):** open since the leak audit of 2026-10-01 (no leak): 588 rows are -9 in every feature, the source's code for no bureau record; the open `dataset_missing_value_sentinel` warning comes from them. To decide in the next pass: keep them as applicants without a credit file (the real population) or drop them as empty records, and say which in the notes.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The challenge defined no predictive scoring rule: judging criteria were not announced in advance and mixed an empirical evaluation with qualitative judging of explanations; only accuracy figures (~72-74%) were reported for entries.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): ordinal scales shipped as numbers, left as numbers for the curator's review: `MaxDelq2PublicRecLast12M`, `MaxDelqEver`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); the two delinquency scales ordered (FICO data dictionary), their unknown, all-other and no-record codes missing.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 2 coded columns carry their words.

CC (2026-11-11, Andrej): the review page's marks of 2026-11-11 applied to the definition on this branch (review issues 1 to 6).
- Issue 1 ("change"): the 588 applications with -9 in every feature are dropped in `_clean`; 9,871 applications remain.
- Issue 2 ("Agree."): the data stays as real; the balanced sample (5,000 Good in the released file) is now named in the task summary and the curation notes, so the 52% Bad is not read as a default rate.
- Issues 3 and 4 ("Option B" twice): the random split is tagged `ForcedIIDFromTemporal`, with the sentence in `fit_reason` and the `Time basis:` bullet.
- Issue 5 ("I don't understand why this is an issue ... I think you overdid here."): nothing changed; the differently recorded block stays as a pattern of the file, with no note.
- Issue 6 ("Agree."): `MSinceMostRecentInqexcl7days` dropped (22 features), marker `Class-dependent Recording`; `dataset check` 0 errors, 0 warnings, 1 info (1 duplicate row).

## Review

**Outcome:** added. The AI recommends shipping it after one change (issue 1). Reviewed on 2026-11-04 without a
panel, from the evidence already gathered (the record, model runs on the shipped data and on the TabArena
v0.1 task of the same source) and one check on the shipped table. The data are FICO's Explainable Machine Learning
Challenge (2018): 10,459 applications for a home equity line of credit (a credit line of $5,000 to $150,000 secured
by the applicant's home), each with 23 summaries of the applicant's credit report; the target is whether the
borrower was 90 days or more past due within 24 months of opening the account ("Bad", 52%). Validity: a lender's
decision on a credit report, the outcome after it; one column leaked how FICO assembled the file, the inquiry
recency, whose runs of one fill code carry more Bad: dropped (issue 6, 2026-11-10); otherwise no leak (the row order
carries no time, issue 3; no near copies beyond the empty records); 588 applications had no credit report at all, every field -9, FICO's code for no
bureau record: dropped (issue 1, 2026-11-04). The data is real, not generated (issue 2). Value: the 40 benchmark methods
spread from 0.197 1-AUC (KumoRFM, TabPFN-3.5) over 0.201 (tuned
LightGBM) to 0.214 (logistic regression); the top methods lie within 0.001 of each other, so the table separates
families of methods more than the leading ones. Quality: the two delinquency scales are ordered with their unknown,
"all other" and no-record codes missing (the curator, 2026-10-31); the codes -7 (condition not met) and -8 (no usable
trades) stay in the other columns as values with a meaning, as the task summary says. Weighed: the bureau's own
challenge data and a direct decision +, methods separate +, 5.6% of the rows without any input - (dropped).

**Main points:** The 588 applications without a credit report are dropped (issue 1); real data, kept (issue 2, resolved
2026-11-09); the random split stays, tagged forced from temporal (issues 3 and 4, resolved 2026-11-09); the differently
recorded batch left as is (issue 5, resolved 2026-11-10); the inquiry recency, whose runs of one fill code mark how FICO
assembled the file and go with the label, dropped with the `Class-dependent Recording` marker (issue 6, resolved
2026-11-10).

**Record judgment:** valid, ship after issue 1. The open Assessment of 2026-10-19 (keep or drop the -9 rows) is issue
1. The ordinal bullet of `curation_comments`, which ran two sentences together, is corrected (2026-11-11).

**Issues for Andrej:**

1. **Drop the 588 applications whose credit report is empty?**

   * **Problem:**
     - In 588 applications (5.6%) every one of the 23 fields is -9, FICO's code for "no bureau record or no
       investigation", so the model gets no input at all for them.
     - A scorecard that decides from the credit report cannot be applied to an applicant without one, but such
       applicants are real and the lender decided on them by other means.
     - Drop these rows as no task rows, or keep them as part of the population?
   * **Background:** the 588 rows are identical, so they are 587 of the table's 589 duplicate rows and land in every
     test fold (184 to 212 per fold of the first repeat). Their share of Good outcomes (45%) is close to the rest's
     (48%), so they carry no recording that tells the classes apart; they only ask every model for one number, the
     base rate. Ten more applications lack only the bureau's risk estimate and keep their other fields. A row that
     lacks the input the prediction acts on is no task row[^1a]; rows that are a sentinel in every feature are a
     weighed decision of their own, with heloc as its example[^1b].
   * **Experiments:** on the shipped table (equal to the v0.2 frame in these rows): 588 rows with -9 in every
     feature, Good rate 0.451 against 0.480 for the others; without them 2 duplicate rows remain.
   * **Consistency:** follows the rows dropped for lacking the input the task acts on (bias_correction's days
     without a model run, the taxi trips without a destination).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 10,459 rows, the empty records as -9 in every field | the population the lender saw, as FICO released it | 5.6% of the rows test nothing but the base rate; one duplicated row 588 times across every fold |
     | B | Drop the empty records | 9,871 rows; the 10 rows without a risk estimate stay | every row has a credit report to score; 2 duplicate rows remain instead of 589 | applicants without a report are no longer represented |

   * **Recommendation:** B, as no scorecard is applied to an empty report. **Decision:** drop the empty records (B)
     or keep them (A)?

   **Notes for the AI:** on B, in `_clean` before `set_missing`: drop the rows where every feature is -9, with a
   note in `curation_comments` (588 rows, Good 45%, the code's meaning); add heloc as a case under the weighed factor
   "Rows that are a sentinel in every feature" in `cleaning_features.md`; re-run `dataset check` (the duplicate and
   sentinel warnings should go) and add a CHANGELOG entry.

   **Andrej (2026-11-04, change):** We go with B

   **Resolved (2026-11-04, Andrej):** B, the 588 applications with -9 in every feature are dropped in `_clean` before
   the codes are set missing; 9,871 applications remain (Bad 52.0%), the 10 without a risk estimate stay. `dataset
   check`: 0 errors, 0 warnings (the sentinel and duplicate warnings are gone; 1 duplicate row left, an info). The
   record has the decision, heloc is a case of the weighed factor on rows that are a sentinel in every feature.

   [^1a]: **USE-7** (Must): a row that lacks the input the prediction acts on is no task row: drop it rather than
     keep it as missing.
   [^1b]: **CLEAN-11** (Should; amended 2026-10-21, Lennart): rows that are a sentinel in every feature are a decision
     of their own; they can be the real population (an applicant without a credit file) or empty records.

   **Resolved (2026-11-11, Andrej):** B again (mark `change`, no note), now applied on this branch: `_clean` drops the
   applications that are -9 in every feature before the codes are set missing (9,871 rows left), with the curation
   bullet "Empty credit reports dropped". `dataset check`: 0 errors, 0 warnings, 1 info (1 duplicate row).

2. **Is the data generated?**

   * **Problem:**
     - The bureau's arithmetic holds in every one of the 9,871 applications with a report: for example, a trade opened
       in the last 12 months appears exactly when the most recent trade is 11 months old or less (0 exceptions, against
       3,740 when that column is shuffled within each class).
     - A test calibrated on real and generated bank tables finds every one of the 23 columns tied to the rest of the row
       beyond the label, more strongly than in the real bank_marketing table.
     - Keep the table as real data, or retire it as generated?
   * **Background:** FICO calls it "a real-world financial dataset provided by FICO" (challenge text, quoted on
     [OpenML 45554](https://www.openml.org/d/45554)), and IBM's tutorial, written with FICO's data dictionary, says it
     "contains anonymized information about home equity line of credit (HELOC) applications made by real homeowners"
     ([AIX360 HELOC tutorial](https://github.com/Trusted-AI/AIX360/blob/master/examples/tutorials/HELOC.ipynb)).
     Neither names the lender, the period or how the rows were sampled, and neither mentions perturbation. The one
     mark of design is the sample: exactly 5,000 Good and 5,459 Bad in the file, so FICO drew a balanced sample and
     the 52% Bad is not a default rate. A written-down generator settles this question for generated data[^2a]; here
     the tests point the other way.
   * **Experiments:** checks of 2026-11-04 on Kaggle's file (re-downloaded), the 9,871 rows with a report:

     | Check | heloc | For comparison |
     |---|---|---|
     | Trades 90+ days late at most the trades 60+ days late | 0 exceptions | 1,655 with that column shuffled within class |
     | Inquiries without the last 7 days at most all inquiries | 0 | 3,519 |
     | Trade opened in the last 12 months exactly when the newest trade is 11 months old or less | 0 | 3,740 |
     | Worst delinquency "never" means 100% of trades never delinquent | 0 | 2,284 |
     | Average age of the file at least the age of the newest trade | 0 | 131 |
     | Column shuffled within class, a model tells real from shuffled rows (ROC AUC) | 0.67 to 0.90, all 23 columns | bank_marketing (real) 0.54 to 0.76; bank_customer_churn (generated) 0.48 to 0.53 for 7 of 10 columns |
     | Cells on a straight line between file neighbours (interpolation mark) | at most 49 per column | |

   * **Effect on the task:** none: the rows behave like credit reports, not like a sampler's draws.
   * **Unknown:** whether FICO added noise when anonymising; the values lie on the integer grids of a bureau summary
     (months, counts, whole percents), with no sign of it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as real (implemented) | nothing changes | FICO's statement and every test agree; the hard constraints hold in all rows | none found |
     | B | Retire as generated | record `No (Retired)` with `AHDS` | none found | no mark of generation found; contradicts the source |

   * **Recommendation:** A: the bureau's own constraints hold without exception and no column looks drawn on its own.
     **Decision:** keep (A) or retire (B)?

   **Andrej (2026-11-04, note):** Are you sure the data was not artificially generated?

   **Answer (AI, 2026-11-04):**

   * You asked whether the data could be generated.
   * No. Five hard rules of the credit report hold in all 9,871 applications; shuffling one column within the class
     breaks them in 131 to 3,740 rows. A generator that draws each column from the class and a few others, as the
     bank_customer_churn table was drawn, breaks them too.
   * The calibrated shuffle test finds all 23 columns tied to the rest of the row (ROC AUC 0.67 to 0.90). Real
     bank_marketing gives 0.54 to 0.76, the generated churn table 0.48 to 0.53.
   * FICO calls it real-world data; IBM's tutorial says anonymised applications of real homeowners. No source mentions
     generation or noise.
   * The one designed part is the sample: exactly 5,000 Good, so the 52% Bad is FICO's balance, not a default rate.
   * Found on the way: rows 2,236 to 4,120 of the file are a batch recorded differently (issue 3); that is a mark of
     real data assembled from extracts, not of a generator.
   * Recommendation: A. **Decision:** keep (A) or retire (B)?

   **Notes for the AI:** evidence in the local job folder `ba_marks_1104/heloc` (`consistency.py`, `nullviol.py`,
   `model_checks.py`). If A, a CC line in the record and the issue closes; optionally note the balanced sample
   (5,000 Good) in `curation_comments` and in the task summary's `predicted`.

   [^2a]: **PROV-3** (Must): the data is real, not generated and not a real table someone reworked; without a source
     statement or a generator, calibrated marks from at least two of the tests, or marks linked to the label, can be
     strong enough. provenance.md, "Is the data generated?": write the generator down when you can, and report the
     decisive test first.

   **Resolved (2026-11-09, Andrej):** A, kept: the data is not generated ("Agree.").

   **Andrej (2026-11-11, ok):** Agree.

   **Resolved (2026-11-11, Andrej):** A again: the data stays as real. The notes' optional part is now written into the
   definition: `predicted` and a curation bullet say that FICO drew a balanced sample (5,000 Good in the released
   file), so the 52% Bad is the sample's design and not a default rate.

3. **Random split, or a temporal one?**

   * **Problem:**
     - Nothing in the data or in FICO's description dates an application: no date column, no period stated, and the
       outcome window (24 months) is the only time named.
     - The file order is not a time order: training on the first 80% and testing on the last 20% scores as high as a
       random split (LightGBM ROC AUC 0.819 against 0.794 to 0.815 for ten random 80/20 splits).
     - The task is temporal by its use case (a lender scores new applications with a model built on older ones), so the
       rules ship it random but tagged as forced from temporal, which the definition lacks[^3a].
   * **Background:** the file is assembled from parts. The labels come in clumps (lag-1 correlation 0.12; Bad rate
     per 500 rows 37% to 69%, up and down without a trend), as when Good and Bad cases are appended in chunks for a
     balanced sample. Update 2026-11-10 (issue 6): the clumps are mostly the inquiry recency's runs of one fill code,
     which carry 61% to 65% Bad against 38%; with those parts taken out, the lag-1 correlation falls to 0.05 and a
     model tells the first half of the file from the second at 0.51 to 0.53 within each part. Rows 2,236 to 4,120 (1,875 applications with a report) are a batch recorded differently: there
     the satisfactory trades exceed the total trades in 42% of rows (3 of 7,996 elsewhere) and the age of the oldest
     trade is unknown in 7.2% (1.3% elsewhere); the batch has 47% Bad against 53%. No source says what the batch is;
     it could be a period, a lender or an extract. Within each class the features barely drift along the file.
   * **Experiments:** checks of 2026-11-04 on the 9,871 rows with a report (models run on the cluster), ROC AUC:

     | Check | Result |
     |---|---|
     | Model telling the first half of the file from the second (label as a feature) | 0.648; random halves 0.499 |
     | Same without the batch | 0.560; random halves 0.507 |
     | Model telling the batch from the other rows | 0.887 |
     | LightGBM: random 80/20 (10 splits) / first 80% to last 20% / last 80% to first 20% | 0.808 (0.794 to 0.815) / 0.819 / 0.801 |
     | LightGBM: 5 folds in file order / 5 random folds | 0.803 / 0.804 |
     | Logistic regression: random 80/20 / first to last / last to first | 0.798 / 0.810 / 0.799 |
     | Leak probe: test rows with an exact copy in training | 0.0% |

   * **Effect on the task:** none on rows or scores under B; the tag and a split note say what the random split stands
     for.
   * **Consistency:** home_credit_default_risk, another undated credit table, ships random tagged forced from
     temporal; porto_seguro's split issue proposes the same on the same tests.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no tag (implemented) | nothing changes | none found | the score's temporal meaning is not stated; departs from the rule for undated tasks |
     | B | Random, tagged forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`; a split note with the tests above | follows the rule and home_credit_default_risk; the leak test passes (no copies, order carries no time effect) | none found |
     | C | By file order | train on the first part of the file, test on the last | none found | the order is not time: the same scores as a random split under another name; one batch would decide a fold |

   * **Recommendation:** B: the data has no dates and its order is assembly, not time, so a random split tagged as
     forced from temporal is what the release allows. **Decision:** random (A), random tagged forced from temporal
     (B), or by file order (C)?

   **Andrej (2026-11-04, discuss):** Are you sure this is not secretly a temporal dataset requiring a temporal split?

   **Answer (AI, 2026-11-04):**

   * You asked whether the data hides a time order that calls for a temporal split.
   * By its use case the task is temporal; in the data no time can be found. No date, no period in FICO's text, and
     the outcome window is the only time named.
   * The file order is not time: a model trained on the first 80% does as well on the last 20% (0.819) as on random
     splits (0.794 to 0.815); folds in file order score as random folds (0.803 and 0.804).
   * What the order does carry is assembly: labels in clumps from the balanced sample, and one batch of 1,875 rows
     recorded differently (satisfactory trades above total trades in 42% of its rows). Without the batch, the two
     halves of the file are hard to tell apart (0.560).
   * So the release allows only a random split; the rules want it tagged as forced from temporal (B).
   * Recommendation: B. **Decision:** A, B or C?

   **Answer (AI, 2026-11-06):** the time framing, from today's review of how each dataset's data arrives.

   * The tag and its `Time basis:` line are now issue 4, and the differently recorded batch issue 5, so this issue
     decides the split only: random applications (A and B are the same folds) or the file order (C).
   * How the data arrives supports the random split: applications arrived over a period FICO never states, each
     followed for 24 months, and the release keeps no time; the file order is FICO's assembly of a balanced sample,
     so no window by application date can be built, and random is the closest regime that keeps the rows[^3b].

   **Notes for the AI:** on B, add `data_tags = ("ForcedIIDFromTemporal",)` (as home_credit_default_risk
   declares it), a split note in `curation_comments` (use case temporal, no dates, file order is assembly: the numbers
   above, recover dates if a later release has them), one sentence in `fit_reason`, `dataset check`. The batch
   (file rows 2,236 to 4,120) is a candidate for a quality note; a model detects it, but it shifts the Bad rate only
   by 6 points. Evidence: `model_checks.py`, `adv2.py`, `adv3.py` in the local job folder `ba_marks_1104/heloc`.

   [^3a]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, once a leak test across the split finds no
     shared outcome, hidden group or order dependence. **SPLIT-22** (Should): the raw file order can be the time order;
     here it is not.
   [^3b]: **SPLIT-8** (Must): forced splits ship in the closest regime that keeps the rows, after a leak test across
     the split. **SPLIT-32** (Should): when samples, features and the target arrive is information for the split.

   **Resolved (2026-11-09, Andrej):** B: the random split stays, tagged `ForcedIIDFromTemporal` in `data_tags`, with a
   sentence in `fit_reason`; the split note is issue 4's `Time basis:` line.

   **Andrej (2026-11-11, change):** Option B: Random, tagged forced from temporal.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: `data_tags = ("ForcedIIDFromTemporal",)` and
   `fit_reason` says that no application date survives, so the random split is tagged as forced from temporal. The
   folds do not change.

4. **Time basis: name the random split forced from temporal (`ForcedIIDFromTemporal`)?**

   * **Problem:**
     - Applications arrived over a period FICO never states, each account was followed for 24 months, and the release
       keeps no time: no date column, and the file order is the assembly of a balanced sample (the first 80% of the
       file scores the last 20% as random splits do).
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, `Target: Later`), but
       the definition names no time basis; the rule names heloc as its example of the forced tag.
     - The use case scores new applications, and delinquency within 24 months follows the credit climate, so of the
       time bases only the forced tag fits: name it, or another one?
   * **Background:** the questions that tell the time bases apart[^4a]:
     - Can time affect the target? Yes: serious delinquency follows the economy of the 24 months after opening.
     - Does the use case predict for a time after its data? Yes: the lender scores new applications from accounts
       already observed.
     - One shared prediction moment? No: each application at its own date, with its own 24-month window, so a delayed
       target with one moment does not fit.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: credit
       climates change; with the time lost that is the forced case[^4b].
     - The sample is balanced by FICO (5,000 Good, 5,459 Bad before the empty reports were dropped), so the share of
       Bad is the design's, not a period's.
   * **Experiments:** the leak test across a forced split[^4b] is issue 3's table (no copies across the split, no
     order effect) and issue 5 (the differently recorded batch, the one structure the file has); whether applications
     of one period share their outcome cannot be tested without dates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | no time tag; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the score's meaning in time is not stated |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line naming the unstated period, the assembly order and what a dated release would change | says what the random score stands for; the rule's own example; follows home_credit_default_risk | none found |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that a credit report predicts delinquency alike in any period | none found | delinquency moves with the economy; no dated data to measure it on |

   * **Recommendation:** B: a forward use case whose time is lost is what the forced tag names. **Decision:** no time
     basis (A), forced (B) or stationary relation (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("ForcedIIDFromTemporal",)` and the curation bullet
   "- Time basis: ForcedIIDFromTemporal: HELOC applications of an unnamed lender over a period FICO does not state,
   each account followed for 24 months; the release keeps no date and its order is the assembly of a balanced sample
   (training on the first 80% of the file scores the last 20% at ROC AUC 0.819 against 0.794 to 0.815 on random
   splits), so random applications stand in for the applications to come. A dated release would allow a split by
   application date."; this bullet is issue 3's split note on B; no `splits_comment` (default split); the record's
   facts stay.

   [^4a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced; heloc is the rule's example of the forced tag.
   [^4b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split: a row's,
     its unit's or its period's outcome shared with the other side, a hidden group, an order dependence.

   **Resolved (2026-11-09, Andrej):** B: the `Time basis: ForcedIIDFromTemporal:` bullet is in `curation_comments`,
   naming the lost application dates and the file order as the assembly of a balanced sample.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: the `- Time basis: ForcedIIDFromTemporal: ...`
   bullet of the notes is in `curation_comments`, word for word; no `splits_comment` (the split stays the default
   random one) and the record's collection facts stay as they are.

5. **Write the differently recorded batch into the notes, as an extract whose own rows help a random split?**

   * **Problem:**
     - Rows 2,236 to 4,120 of FICO's file (1,875 applications with a report) are recorded differently (satisfactory
       trades above total trades in 42% of rows, against 3 of 7,996 elsewhere), a model finds them at ROC AUC 0.887,
       and they are 47.3% Bad against 53.2% elsewhere.
     - A random split puts the batch on both sides, and at equal training size LightGBM scores the batch's rows at
       ROC AUC 0.794 with the batch's other rows in training against 0.784 without them.
     - If the batch is a period or one extract, that gain is a period's outcome shared across the split; the
       definition does not mention the batch: write it into the notes, or more?
   * **Background:** the forced split's leak test asks whether rows of one period share their outcome with the
     other side[^5a]. No source says what the batch is (a period, a lender or an extract), so it cannot be a group
     key, and with one batch a grouped split would be two groups. A leak that moves little is still weighed by what it
     is, not by the score[^5b].
   * **Experiments:** today's run (Slurm, cpuhigh32), 9,871 applications with a report, 5 repeats, both arms trained
     on 7,896 rows: (a) the batch held out, training drawn from the other rows; (b) random 5 folds, the batch's rows
     scored out of fold:

     | Model | Batch held out: ROC AUC / log loss / mean prediction | Random folds, on the batch | Random folds, other rows / all |
     |---|---|---|---|
     | LightGBM, untuned | 0.784 / 0.561 / 0.478 | 0.794 / 0.552 / 0.469 | 0.805 / 0.803 |
     | Logistic regression | 0.788 / 0.556 / 0.471 | 0.791 / 0.552 / 0.472 | 0.802 / 0.801 |

     - The batch's Bad rate is 0.473: held out, LightGBM's mean prediction misses it by 0.005, inside the folds by
       0.004, so the gain is in the ranking, not the base rate. On the whole test set the batch adds about 0.002 ROC
       AUC (19% of the rows times 0.009).
   * **Effect on the task:** small; the random score is a little optimistic for a new extract recorded another way,
     which a forced split does not test anyway.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave as is (implemented) | the batch is not mentioned in the definition | nothing changes | the one structure of the file and its measured gain go unrecorded |
     | B | A note | a curation bullet on the batch: its rows, its recording, its Bad rate and the gain above; `fit_reason` unchanged | the mildest remedy; the next reader knows the batch | none found |
     | C | Drop the batch | 1,875 rows go | no differently recorded rows | 19% of real applications lost for a gain of 0.002 overall; nothing says the batch is wrong |

   * **Recommendation:** B: the batch is real data with a small, measured effect, so it is recorded rather than
     removed. **Decision:** leave (A), note (B) or drop (C)?

   **Notes for the AI:** on B, a curation bullet: "- A batch of FICO's file (rows 2,236 to 4,120, 1,875 applications
   with a report) is recorded differently: satisfactory trades above total trades in 42% of its rows (3 of 7,996
   elsewhere), the oldest trade's age unknown in 7.2% (1.3% elsewhere), 47.3% Bad against 53.2%; a model detects it
   (ROC AUC 0.887). What it is (a period, a lender, an extract) is not stated. Under the random split its own rows help
   score it (untuned LightGBM ROC AUC 0.794 against 0.784 with the batch held out, at equal training size), about
   0.002 on the whole test set; kept."; `dataset check`; CHANGELOG entry. Evidence:
   `~/claude_jobs/time_review/heloc/` (`scripts/batch_holdout.py`, `batch_holdout_eqsize.json`; Slurm job 1366168).

   [^5a]: **SPLIT-8** (Must): a split forced from temporal gets a leak test across the split: does a row share its
     outcome, its unit's outcome or its period's outcome with the other side; a leak found is weighed case by case,
     removed where it can be, otherwise measured in the notes.
   [^5b]: **LEAK-5** (Must): never argue "not a leak" because models would predict the same. **LEAK-6** (Must):
     measure before acting; a slight optimism with a known cause can stay with a note.

   **Andrej (2026-11-06, discuss):** Shouldn't there be a better way to deal with this? Find out whether the different
   recordings are due to rounding or due to real different recording paths, whether there are even more recording
   paths and reason about where these may come from, e.g. whether the data is not iid due to that?

   **Answer (AI, 2026-11-09):** Not rounding but two recording paths: in the batch two columns are not the applicant's
   and alone make its own rows help, and a second path runs through the whole file in the inquiry recency; blank the
   two columns in the batch's rows?

   * **Problem:**
     - In file rows 2,241 to 4,120 (1,870 applications), the total number of trades and the age of the oldest trade do
       not fit the rest of the row (the total lies between the satisfactory trades and 5 more in 25% of rows, 26% with
       the column shuffled within the batch, 95% elsewhere), while the other 21 columns keep their usual relations and
       no column is rounded, capped or rescaled.
     - These two columns are the batch's whole effect on models: at equal training size the batch's own rows lift its
       ROC AUC from 0.782 to 0.793 with them and from 0.792 to 0.793 without them, and no other block of the file gains
       from its own rows (+0.0006), so the batch is no group.
     - A second recording path runs through the whole file, in the months since the last inquiry, and goes with the
       label (a decision of its own, below); for the batch: blank the two columns, drop them, drop the rows, group them,
       or only a note?
   * **Not rounding** (the batch against the other 8,001 applications with a report):
     - Grids: 17.7% of the cells are multiples of 5, against 18.4%; last digits match in 12 of 14 columns (chi-square
       p 0.44 to 0.97; the two exceptions are percentages computed from the trade counts); no column sits on a
       coarser grid.
     - Codes: the shares of -7 and -8 match, except "no usable trades" (-8) for the oldest trade, 7.2% against 1.3%,
       in 132 of its 135 rows beside zero total trades (1 such row elsewhere), and the inquiry path below.
     - Scale and caps: the quartiles of the other columns match; no pile-up at a limit (installment burden above 100%:
       1.26% against 1.24%).
     - What differs: total trades below the satisfactory trades in 42% of rows (none elsewhere) and zero in 7.1%;
       their rank correlation with the satisfactory trades is 0.45 (0.98 elsewhere), the oldest trade's with the
       average months in file 0.42 (0.79); the installment share is a fraction of the total trades in 33% of rows
       (29% with the column shuffled, 90% elsewhere). Among the other 21 columns no correlation moves.
   * **The second path**, the months since the last inquiry (`MSinceMostRecentInqexcl7days`), through the whole file:
     - In file order the column runs in blocks: 21 runs where it is 0 in every row (3,592 applications), 16 runs where
       it is -7, "condition not met (e.g. no inquiries)", in every row (1,830), and 22 stretches of real values
       (4,449); 15 times a 0 run is followed directly by a -7 run. A change-point segmentation of the column (binary
       segmentation, multinomial likelihood, BIC-type penalty) puts its 42 change points at these edges; with the
       column shuffled, the longest run is 11 to 15 rows.
     - In the runs the value is not the applicant's: in a 0 run (an inquiry within the last month) 42% of the rows
       have no inquiry in the last 6 months, in a -7 run ("no inquiries") 58% have one; on the real stretches the value
       agrees with the 6-month count in 96% of rows. The 6-month count itself is alike on all three (an inquiry in
       58%, 58% and 59%).
     - It goes with the label: 64.9% Bad in the 0 runs, 61.3% in the -7 runs, 37.9% on the real stretches; in each of
       the 18 cycles that have both parts (a cycle: the runs and the real stretch after them) the runs hold the larger
       Bad share.
     - The value gives the path away: 1 or more, or -8, occurs only on the real stretches (3,434 rows), -7 almost only
       in the runs (1,830 of 1,855). A model finds the path at ROC AUC 0.968 with the column, at 0.55 and 0.56 within
       each class without it (and without the batch's two columns, outside the batch); the 0 runs and the -7 runs are
       one population (0.53).
     - The empty reports dropped in issue 1 belong to the pattern: 381 of the 588 form one run (rows 1,081 to 1,461)
       at the head of a 0 run.
   * **How the two line up:** the batch begins at row 2,241, the first row of a -7 run, and ends at row 4,120, the last
     row before a 0 run, so it is one block of the file's assembly (the earlier start, row 2,236, took in five rows
     that fit). 65% of its rows lie on real stretches against 40% elsewhere, and within each path its Bad share
     matches the rest (61% against 64% in the runs, 40% against 37% on the real stretches): its lower Bad share (47%
     against 53%) is its path mix. The label's clumps along the file (lag-1 correlation 0.12) halve (0.05) once each
     path's Bad share is taken out; the label alone has one change point (the last 290 rows, 27% Bad).
   * **Experiments:** Slurm (cpuhigh32), untuned LightGBM, random 5 folds and 5 repeats, the 9,871 applications with a
     report and their raw codes; ROC AUC on all rows and within each part (standard deviation about 0.001):

     | Columns | All rows | Runs | Real stretches | Batch |
     |---|---|---|---|---|
     | All 23 | 0.803 | 0.771 | 0.790 | 0.793 |
     | The two trade columns blank in the batch | 0.804 | 0.772 | 0.789 | 0.794 |
     | Without the two trade columns | 0.804 | 0.773 | 0.790 | 0.795 |
     | Without the inquiry recency | 0.794 | 0.774 | 0.790 | 0.789 |
     | The inquiry recency blank in the runs | 0.805 | 0.771 | 0.789 | 0.793 |
     | All 23 and an indicator of the path | 0.805 | 0.771 | 0.790 | 0.794 |
     | The inquiry recency alone | 0.62 | 0.48 | 0.60 | 0.63 |
     | The indicator of the path alone | 0.62 | | | |

     - Logistic regression (codes as indicator columns): 0.806 with all 23, 0.799 without the inquiry recency; within
       the runs 0.779 and 0.782, on the real stretches 0.792 both.
     - A segment's rows scored with and without its other rows in training, at equal training size (7,000 rows; 5
       parts, 3 to 5 repeats; the 19 cycles join those under 150 rows to the one before):

     | Segment and columns | With its own rows | Without them |
     |---|---|---|
     | Batch, all 23 | 0.793 | 0.782 |
     | Batch, without the two trade columns | 0.793 | 0.792 |
     | Batch, without them and the inquiry recency | 0.787 | 0.787 |
     | 19 cycles, all 23 (gain weighted by rows) | +0.0006, 10 cycles up, 9 down | |
     | 19 cycles, without the inquiry recency | +0.0013, 9 up, 10 down | |

     - Across paths, without the inquiry recency, 3,000 training rows: the real stretches score 0.776 trained on the
       runs and 0.779 on their own path; the runs score 0.769 trained on the real stretches and 0.759 on their own.
     - Mean prediction for Good and for Bad applications: without the inquiry recency 0.354 and 0.619 on the real
       stretches, 0.414 and 0.667 in the runs; with it 0.301 and 0.569, against 0.466 and 0.703.
     - Drift: the first and the second half of the file, within one path and outside the batch, are told apart at 0.51
       and 0.52 (0.50 to 0.53 within each class).
     - Dropping rows: without the batch, 0.803 on 8,001 applications; the real stretches alone, 0.784 on 4,449 (0.781
       without the inquiry recency).
   * **Not IID?**
     - Not in groups: a cycle's own rows add nothing, the halves of the file look alike, and the credit report predicts
       the same way on both paths (each path is scored as well from the other's rows), so a split by cycle or by the
       batch would test nothing a random split misses.
     - The batch's own-row gain is its two columns: from the batch's own rows a model learns to read trade counts that
       break the bureau's arithmetic; without the columns the gain is 0.001, so it is not a period's outcome shared
       across the split.
     - The part that is not IID is the inquiry path: the runs hold 26 points more Bad than the real stretches, about
       half of it beyond what the reports show (without the column a model predicts the two 0.12 apart, 0.05 to 0.06
       apart at equal class), and the column tells the path, so a random split lets a model score how FICO assembled
       the file: +0.010 ROC AUC on all rows (0.794 to 0.803), none of it within either path. With two paths a split by
       path would have two groups; removing what tells the path is the remedy (the next bullet but one).
   * **Where they may come from:**
     - No source says. FICO's text calls the file "a real-world financial dataset provided by FICO" (quoted on
       [OpenML 45554](https://www.openml.org/d/45554)); the data dictionary (a course copy:
       [HelocDataDict2.xlsx](https://ajzhanghk.github.io/Stat3612/HelocDataDict2.xlsx)) defines the 23 fields and the
       codes -9 "No Bureau Record or No Investigation", -8 "No Usable/Valid Trades or Inquiries" and -7 "Condition not
       Met (e.g. No Inquiries, No Delinquencies)", and names no bureau, lender, period, sampling or row order;
       [IBM's AIX360 tutorial](https://github.com/Trusted-AI/AIX360/blob/master/examples/tutorials/HELOC.ipynb) adds
       only that the applications are anonymised and real; FICO's challenge page now redirects, and its archived
       copies keep no text. No mirror or paper found mentions the order or the runs.
     - Different bureaus: could fit both. A cycle's three parts could be three bureaus' extracts, two without the
       inquiry recency, and the batch's two columns could come from another bureau's report on the same applicant
       (they follow the applicant only loosely, and zero trades come with "no usable trades", as for someone without
       a file there); against it, within each class the parts look alike (0.55 to 0.56), and no source names a bureau.
     - Periods or a format change: a change in the extract would split the file once or a few times, not in a pattern
       repeated 15 times, and the halves of the file look alike; the dictionary copy calls the target "Paid as
       negotiated flag (12-36 Months)", the one hint at several vintages.
     - Lenders: another lender brings other applicants (risk estimates, ages of the files), and within each class the
       paths barely differ.
     - FICO's balanced sample: the likeliest place. The paths differ mainly in their Bad share (64% against 38%), in
       every cycle, as when Good and Bad are drawn at different rates from parts recorded differently; the file's
       5,000 Good are a designed number. The batch's two columns look like a join to another record inside one block.
   * **Could become its own issue: drop the months since the last inquiry?** The inquiry path is a recording that goes
     with the label and that its own column gives away, which the rules on recording that differs by class ask to
     remove after measuring[^5e]:
     - Drop `MSinceMostRecentInqexcl7days`: no model finds the path any more (0.55 to 0.56 within class); ROC AUC on
       all rows 0.803 to 0.794, nothing within either path (runs 0.771 to 0.774, real stretches 0.790 both); trained on
       the real stretches alone, the column adds 0.003 there beyond the 6-month counts (0.784 against 0.781).
     - Blank it in the runs: no fix, as the blank marks the path (0.805)[^5f].
     - Keep only the real stretches: 4,449 applications, 38% Bad (0.784); 55% of the rows and two thirds of the Bad go.
     - A note only: every random-split score keeps 0.010 from how FICO assembled the file.
     - The AI would recommend dropping the column, with the `Class-dependent Recording` marker; the outcome's "no leak
       found" and issue 3's background (the labels in clumps) would then name the paths.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Leave as is (implemented) | nothing changes | none found | 1,870 rows keep two values that are not the applicant's; the batch's own rows help it by 0.011 |
     | b | A note only | the issue's curation bullet, with the findings above | the next reader knows the block | the wrong values and the 0.011 stay |
     | c | Blank the two columns in the batch | `NumTotalTrades` and `MSinceOldestTradeOpen` missing in rows 2,241 to 4,120, and a note | the values that are not the applicant's go and the rows stay; the batch's own-row gain falls to 0.001; ROC AUC unchanged (0.804) | the blank marks the batch, though its Bad share differs only by its path mix |
     | d | Drop the two columns | both columns go for all 9,871 rows | no blank marks the batch; ROC AUC unchanged (0.804) | 8,001 sound values of each column go; a column leaves for what it is, and these are sound in 81% of the rows |
     | e | Drop the batch | 1,870 applications go | only rows recorded alike | 19% of the rows lost for two columns; 0.803 on the rest, no gain |
     | f | Split or group by the batch | the batch as one group or test fold | tests a block recorded another way | one block makes two groups; the gain it would remove is the two columns', which c removes too |

   * **Recommendation:** c: the two values are neither rounded, capped nor rescaled but are not the applicant's, so
     they become missing and the rows stay[^5c]; that removes the batch's own-row gain at no cost, and as the batch is
     no group, the random split stays[^5d]. **Decision:** c, d, b, e, f, or leave a?

   **Notes for the AI:** on c, in `_clean` before the empty reports are dropped (the positions are the raw file's):
   set `NumTotalTrades` and `MSinceOldestTradeOpen` to missing in raw positions 2,240 to 4,119 (0-based; file rows
   2,241 to 4,120, 1,870 applications with a report), the block as a module constant with a comment. Curation bullet:
   "- Two columns misrecorded in one block of FICO's file (2026-11-09, Andrej, review issue 5; CLEAN-11): in file rows
   2,241 to 4,120 (1,870 applications with a report) `NumTotalTrades` and `MSinceOldestTradeOpen` do not fit the rest
   of the row: the total lies between the satisfactory trades and 5 more in 25% of rows (26% with the column shuffled
   within the block, 95% elsewhere), below them in 42%, zero in 7.1% with the oldest trade coded -8; nothing is
   rounded, capped or rescaled, and the other 21 columns keep their relations. Both are missing there; the rows stay.
   Before, the block's own rows lifted its ROC AUC from 0.782 to 0.793 at equal training size (untuned LightGBM),
   from 0.792 to 0.793 without the two columns; ROC AUC on all rows unchanged (0.803 to 0.804). The block's lower Bad
   share (47.2% against 53.2%) follows its share of rows on the inquiry recency's real stretches."; `dataset check`;
   CHANGELOG entry. On d: drop both columns in `_clean`, the same bullet with "dropped". The issue's earlier text and
   notes give the block as rows 2,236 to 4,120 (1,875 applications); the corrected rows replace them. If the inquiry
   path becomes issue 6: options keep (implemented), drop the column, blank it in the runs, keep only the real
   stretches, with the numbers above; on drop, `_clean` drops `MSinceMostRecentInqexcl7days`, a curation bullet with
   the runs, their Bad shares and the scores, the `Class-dependent Recording` marker in the record, `dataset check`,
   CHANGELOG. Evidence in the local job folder `marks_1109/heloc`: `describe.py`, `relations.py`, `checks2.py`,
   `final_numbers.py` (the two columns, grids and codes), `segment.py`, `regimes.py`, `inq_runs.py` (the paths and
   the change points), `models.py` (Slurm job 1373804) and `models2.py` (job 1373848).

   [^5c]: **CLEAN-11** (Should): impossible values become missing, and the row stays. The curator's line on
     preprocessing (Andrej, 2026-10-21, on gallstone_disease): fix what lets a model tell the classes apart for
     reasons other than the target, from preparation or from collection, tested; correct what is wrong; keep and
     document the rest.
   [^5d]: **SPLIT-8** (Must): a split forced from temporal gets a leak test across the split: a row's, its unit's or its
     period's outcome shared with the other side, a hidden group. **LEAK-6** (Must): measure before acting; a slight
     optimism with a known cause can stay with a note, a confirmed leak goes even when small.
   [^5e]: **LEAK-13** (Must): class-specific recording conventions are harmonised; a column filled in for one class
     only is dropped; first measure how much the fix removes. **LEAK-39** (Must): rows of one class recorded through a
     separate route, found by a recording fingerprint, are dropped when models recognise them and the route cannot be
     aligned; here both classes pass through both paths and the fingerprint is one column, so the column goes, not the
     rows. Marker `Class-dependent Recording` where these rules applied, kept or retired.
   [^5f]: **LEAK-40** (Should): setting values to missing is no fix when the gaps follow the classes: the missing values
     then mark a class.

   **Andrej (2026-11-09, discuss):** You wrote too much text, I don't wanna read all of it. Summarize what you found and
   why you make the current recommendation in bullets.

   **Answer (AI, 2026-11-09):** in short:

   * Not rounding: two separate recording paths.
   * This issue: in rows 2,241 to 4,120, `NumTotalTrades` and `MSinceOldestTradeOpen` do not fit the rest of the row
     (the total lies below the satisfactory trades in 42% of rows, almost never elsewhere). The other 21 columns are
     fine.
   * It does not follow the label (46% Bad against 48% in the rest of the block), and it is the block's whole own-row
     gain (0.782 to 0.793 with the two columns, 0.792 to 0.793 without).
   * Beyond that, rows of the same stretch add nothing (+0.0006), so the data is no group.
   * The second path is issue 6: the inquiry recency's runs of 0 or -7 are 61% to 65% Bad against 38% elsewhere.
   * Why c: the two values cannot be the applicant's, so they become missing and the rows stay; that removes the gain at
     no cost (ROC AUC 0.804 against 0.803), and the random split stays.
   * **Decision:** c (blank them), d (drop the two columns), or leave (a)?

   **Andrej (2026-11-10, discuss):** I don't understand why this is an issue and not a regular pattern of the data. I
   think you overdid here.

   **Answer (AI, 2026-11-10):** agreed: leave it (a).

   * The two columns disagree with the rest of the row in one block, but that does not follow the label (46% Bad against
     48% in the rest of the block).
   * Blanking them changes nothing measurable (ROC AUC 0.804 against 0.803).
   * So it is a recording quirk worth one line in the notes at most, not a fix.
   * **Recommendation:** a, leave as is (or b, a one-line note). **Decision:** a or b?

   **Andrej (2026-11-10, ok):** Agree.

   **Resolved (2026-11-10, Andrej):** a, left as is; no note needed.

   **Andrej (2026-11-11, discuss):** Agree.
   I don't understand why this is an issue and not a regular pattern of the data. I think you overdid here.

   **Answer (AI, 2026-11-11):** agreed, and nothing was changed for it.

   * The block is a regular pattern of the file: two columns disagree with the rest of the row in rows 2,241 to 4,120,
     the other 21 columns are fine, and the block does not follow the label (46% Bad against 48% in the rest of it).
   * Blanking the two columns moved no score (ROC AUC 0.804 against 0.803), so there was nothing to fix.
   * The definition is untouched for this issue and carries no note on the block; option a stands as resolved on
     2026-11-10.

6. **Drop `MSinceMostRecentInqexcl7days`, whose runs of one code mark how FICO assembled the file and go with the label?**

   * **Problem:**
     - In file order the inquiry recency sits in long runs of one value: 21 runs of 0 (3,592 rows) and 16 runs of -7
       (1,830 rows), between 22 stretches of real values (4,449 rows); 15 times a run of 0 is followed directly by a run
       of -7[^6a].
     - The run values are not the applicant's: 42% of the rows in runs of 0 have no inquiry in the last 6 months, and
       58% of the rows in runs of -7 ("no inquiries") have one. On the real stretches the value agrees with the 6-month
       count in 96% of rows.
     - The runs go with the label: 64.9% and 61.3% Bad, against 37.9% on the real stretches, in every one of the 18
       cycles that have both. The column gives the path away: values of 1 or more, and -8, occur only on the real
       stretches (ROC AUC 0.968 for the path with the column, 0.55 to 0.56 within class without it). Keep the column,
       drop it, blank it in the runs, or keep only the real stretches?
   * **Experiments:** untuned LightGBM, random 5 folds x 5 repeats, the 9,871 rows with a report (Slurm jobs 1373804 and
     1373848):
     - Dropping the column lowers ROC AUC on all rows from 0.803 to 0.794; within each path nothing changes (runs 0.771
       to 0.774, real stretches 0.790 both). Logistic regression: 0.806 to 0.799.
     - So the 0.010 the column adds comes from the assembly, not from credit risk: the reports explain only about half
       of the 26-point gap in Bad share between the paths, and they predict the same way on both (real stretches 0.776
       trained on the other path, 0.779 on their own).
     - Blanking the column in the runs scores 0.805, as the blank marks the path. Keeping only the real stretches scores
       0.784 on 45% of the rows.
   * **Origin:** no public source documents the row order. The likeliest is FICO's assembly of the balanced sample:
     extracts in parts, two of them without the inquiry field, filled with one code, and Bad drawn at a higher rate from
     those parts (issue 5's answer of 2026-11-09).
   * **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Keep (implemented) | as now | no change | a field that marks the assembly's parts and their Bad rates stays readable; 0.010 of ROC AUC comes from it |
   | B | Drop the column | `_clean` drops `MSinceMostRecentInqexcl7days` | removes the path marker; the reports predict the same on both paths | loses the recency on the real stretches; the 6-month count stays |
   | C | Blank it in the runs | the run values become missing | keeps the real values | the blank marks the path (0.805) |
   | D | Keep only the real stretches | the 5,422 rows in runs go | a clean column | 55% of the rows lost (0.784) |

   * **Recommendation:** B, with the `Class-dependent Recording` marker: the column records how the file was put
     together, and its runs carry the label beyond the credit report[^6b]. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, `_clean` drops `MSinceMostRecentInqexcl7days`; a curation bullet with the runs, their Bad
   shares and the scores above; the `Class-dependent Recording` marker in the record with a CC line; the Outcome's "no
   leak found" and issue 3's background on label clumps updated (the clumping along the file halves, lag-1 correlation
   0.12 to 0.05, once the paths are taken out); `dataset check`; CHANGELOG. Evidence in
   `~/claude_jobs/marks_1109/heloc/`: `inq_runs.py`, `regimes.py`, `segment.py`, `models.py` (job 1373804), `models2.py`
   (job 1373848).

   [^6a]: Found while answering issue 5 (2026-11-09); the trade-count block of issue 5 starts at the first row of a run
   of -7 and ends just before the next run of 0, and 381 of the 588 empty reports form one run at the head of a run of
   0.
   [^6b]: **LEAK-10** (Must): missingness or a code that encodes the outcome is out. **LEAK-39** (Must): rows of one
   class recorded through a separate route are dropped when the route cannot be aligned; here the route shows in one
   column, so the column can go instead of the rows. The curator's line on preprocessing (Andrej, 2026-10-21): fix what
   lets a model tell the classes apart for reasons other than the target, tested; keep and document the rest.

   **Andrej (2026-11-10, discuss):** Isn't that just the sorting of the file? Why would that be an issue?

   **Answer (AI, 2026-11-10):** not the sorting itself: inside those runs the column holds one fill code, not the
   applicant's value, and the runs carry far more Bad.

   | | Rows | Value matches the applicant's 6-month inquiry count | Bad |
   |---|---|---|---|
   | Runs of 0 | 3,592 | 58% | 64.9% |
   | Runs of -7 ("no inquiries") | 1,830 | 42% | 61.3% |
   | Real stretches | 4,449 | 96% | 37.9% |

   * The sorting only makes the parts visible. The issue is that a model reads "this row came from a part without the
     field", and those parts were drawn with more Bad.
   * That is worth 0.010 ROC AUC (0.803 to 0.794 without the column), and within each part the column adds nothing.
   * If you read the higher Bad share of those parts as how FICO's applicants really were, the column is harmless and
     stays (A).
   * **Recommendation:** B, drop the column, as its run values are not the applicant's; A with a note if you see it as a
     sampling pattern. **Decision:** A or B?

   **Andrej (2026-11-10, discuss):** I get that the drawing patterns differ, but what if they are natural? We should
   check and understand the exact reason before just dropping the column.

   **Answer (AI, 2026-11-10):** not natural: no reading of FICO's codes makes the run values the applicant's own.

   | Natural explanation | Test | Result |
   |---|---|---|
   | 0 counts an inquiry of the last 7 days, which the column excludes | runs of 0 whose applicant has no inquiry in 6 months excluding the last 7 days (1,497 rows) | 1,441 of them have no inquiry at all in 6 months, the last 7 days included; only 56 have one in the last 7 days |
   | Codebook meaning | the dictionary's codes: -9 no bureau record, -8 no usable trades or inquiries, -7 condition not met (e.g. no inquiries); 0 is a month count, not a code | -7 means "no inquiries", yet 1,056 of the 1,830 rows in runs of -7 have inquiries in the last 6 months |
   | Another extract or definition (e.g. a later pull) | the other inquiry columns by path | alike: an inquiry in the last 6 months in 60%, 60% and 61%, in the last 7 days in 6%, 5% and 5% |
   | The runs are riskier applicants | model without the column: mean prediction against the Bad share | runs 0.575 against 0.637, real stretches 0.454 against 0.379: about half the gap is not in the reports |
   | A source on how FICO built the file | FICO's text (OpenML 45554), the data dictionary, IBM's tutorial | none describes the order, the parts or the sampling |

   * On the real stretches the column behaves as defined: a value of 0 comes with an inquiry in the last 6 months in
     98% of rows, and applicants without any inquiry get -8 or 6 months and more.
   * So inside the runs the column holds one code written for the whole part, not a recency; the parts differ in Bad
     share beyond what the reports show, which is how FICO drew them, not how the applicants were.
   * **Recommendation:** B, drop the column. **Decision:** A (keep) or B (drop)?

   **Notes for the AI:** evidence `natural.py` in the local job folder `marks_1109/heloc`; the model numbers are from
   `models2.py` (job 1373848).

   **Resolved (2026-11-10, Andrej):** B ("Agree."): `_clean` drops `MSinceMostRecentInqexcl7days` (22 features); a
   curation bullet gives the runs, their Bad shares and the scores; the record carries the `Class-dependent Recording`
   marker with a CC line; the Outcome and issue 3's background are updated. `dataset check`: 0 errors, 0 warnings, 1 info (1 duplicate row, as before).

   **Andrej (2026-11-11, discuss):** Agree.

   **Resolved (2026-11-11, Andrej):** B again, now applied on this branch: `_clean` drops
   `MSinceMostRecentInqexcl7days` (22 features left), the curation bullet "Inquiry recency dropped" carries the runs,
   their Bad shares and the scores, and the record keeps the `Class-dependent Recording` marker. `dataset check`:
   0 errors, 0 warnings, 1 info (1 duplicate row).

## Reference

https://www.kaggle.com/datasets/averkiyoliabev/home-equity-line-of-creditheloc
