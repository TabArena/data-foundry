---
unique_name: credit_card_clients_default
name: Default of Credit Card Clients / credit_card_clients_default
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: One Moment'
- 'Target: Later'
original_source: UCI
year: '2016'
required_split:
- Random (IID)
source_links:
- https://doi.org/10.24432/C55S3H
notebook_path: datasets/beyond_iid/old_iid/credit_card_clients_default/credit_card_clients_default.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_card_clients_default/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Predict default on payment or not, uses time-invariant temporal features of the payment history

Potential issue: temporal features?

Lennart: Temporal impact can likely be ignored with these features

Andrej: Seems fine

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Yeh & Lien 2009 score the lift chart's area ratio, which equals 2 x ROC AUC - 1.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `EDUCATION` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 columns with a state outside the scale ordered, the state placed by the rule.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 3 coded columns carry their words; MARRIAGE 0 (undocumented) missing.

CC (2026-11-11, Andrej): review marks applied (Review issues 1 and 2). Rows, columns and the random split are unchanged (30,000 clients).

- Issue 1 (`ok`): the repayment codes -2 and 0 stay numbers. **Exception to CLEAN-14 (2026-11-04, Andrej):** they are each status column's most common values (-2 and 0 together 58-72% of the rows), so making an undocumented code missing would blank most of each column and merge two states into one missing value; their order fits the reading (-2 card not used, -1 paid in full, 0 minimum paid, then months of delay; default rate by September's code 13%, 17%, 13%, 34%, 69%). The bullet is now in the definition's notes, with the September quirk of code 1.
- Issue 2 (a, "Reply (a): Random clients (A, with issue 3's tag)"): the split stays random over clients, with issue 3's time basis. `data_tags = ("DelayedTarget",)` and the `Time basis: DelayedTarget:` bullet: one extract of 30,000 card holders scored after the September 2005 statement, the target default on the next month's payment, so no test row is later than a training row. The client ID is not a time order (the first two quarters cannot be told apart, ROC AUC 0.504). Not tested: a later month.
- `dataset check` passes (0 errors, 0 warnings; the 35 duplicate inactive accounts stay as info).

## Review

**Outcome:** added. The AI recommends shipping it as defined, with the undocumented repayment codes kept as numbers
(issue 1). Reviewed on 2026-11-04 without a panel, from the evidence already gathered (the record, a model run
on the TabArena v0.1 task of the same source) and one check on the shipped table. The data are Yeh & Lien's (2009)
card holders of one Taiwanese bank (UCI 350, donated 2016): 30,000 clients with six months of history (April to
September 2005: credit limit, demographics, monthly repayment status, bill and payment amounts), and the target is
default on the next month's payment (22%). Validity: a real task with a decision behind it (a card issuer adjusts
limits or starts collection), every feature is dated before the payment it predicts, and no leak or class-dependent
recording was found (the row order carries nothing; the 35 duplicate rows are inactive accounts with all amounts 0,
with mixed labels). Value: the benchmark methods spread from about 0.207 1-AUC (TabFM, TabPFN-3.5) over 0.215 (tuned
gradient boosting) to 0.255 (logistic regression), so the table separates methods. Quality: the undocumented codes of
EDUCATION (0, 5, 6, with "others") and MARRIAGE (0) are missing by the curator's rules; the repayment status keeps
two undocumented codes as numbers (issue 1). Weighed: documented source and a direct decision +, methods separate +,
one snapshot month for every client (an approximate fit) -.

**Main points:** Random clients, with issue 3's `DelayedTarget` (issue 2, resolved 2026-11-09). The random split is
named a `DelayedTarget` of one extract and one payment month (issue 3, resolved 2026-11-06). The repayment codes stay
numbers (issue 1, resolved).

**Record judgment:** valid, ship. One bank, one snapshot: every client is scored for October 2005, so the random
split cannot test a model on later months; the fit says so. A separate review of metrics proposes a probability score
for this dataset; it is not part of this review.

**Issues for Andrej:**

1. **Keep the undocumented repayment codes -2 and 0 as numbers?**

   * **Problem:**
     - The six monthly repayment status columns hold -2 or 0 in 58% to 72% of the rows, codes the UCI codebook does not define (it gives -1 for paid duly and 1 to 9 for months of delay).
     - The curator's rule makes an undocumented code missing, which here would blank most of each column, so the definition keeps them as numbers without saying why.
     - Keep them as numbers with a note, or apply the rule?
   * **Background:** the codes are commonly read as -2 "card not used that month", -1 "paid in full" and 0 "minimum
     paid, balance revolving", an order of rising use of credit below the months of delay. Default rates per code
     in the latest month: -2 13%, -1 17%, 0 13%, one month late 34%, two months 69%. The value 1 (one month late)
     occurs in 12.3% of the rows for September but in at most 0.1% for the five earlier months, where two months late
     is 9-13%: the earlier months seem to record a short delay differently, alike in both classes.
   * **Experiments:** on the shipped table (the v0.2 frame for these columns): shares of -2 / -1 / 0 per column
     9-16% / 19-20% / 49-57%.
   * **Consistency:** the same rule made MARRIAGE 0 (54 rows) and EDUCATION 0, 5 and 6 (345 rows) missing on
     2026-11-01[^1a]; there the codes were rare, here they are the most common value.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as numbers (implemented) | -2, -1, 0 and 1-8 stay on one numeric scale; a note gives the reading and the September quirk | keeps the most common states; their order fits the reading | the meaning of -2 and 0 is not documented by the source |
     | B | Apply the rule | -2 and 0 missing in the six columns | follows the rule as written | blanks 58-72% of each status column and merges two different states into one missing value |

   * **Recommendation:** A, recorded as an exception: the codes are the columns' most common values with a
     consistent order. **Decision:** keep as numbers (A) or set to missing (B)?

   **Notes for the AI:** on A, add a bullet to `curation_comments` (the codes, their common reading, the shares, the
   September quirk of code 1) and an exception row under CLEAN-14 in `cleaning_features.md` with the fact that sets
   it apart (the majority value of the column). On B, `set_missing(df, {c: [-2, 0] for c in PAY_COLUMNS})`.

   **Andrej (2026-11-11, ok):** (the mark alone, no note)

   **Resolved (2026-11-04, Andrej):** A, keep the codes -2 and 0 as numbers, as an exception to the rule that makes
   an undocumented code missing (they are each column's most common values); the note is in `curation_comments`, the
   exception in the record and in the cleaning rules' cases. The split is open as issue 2.

   [^1a]: **CLEAN-14** (amended 2026-10-31, Lennart) and **CLEAN-10** (Should): a level outside the scale that means
     unknown, an undocumented code among them, is missing; keep a code and say why when it means something.

2. **Random split, or a temporal one?**

   * **Problem:**
     - Every client has the same six months (April to September 2005) and the same outcome month, the next one, so there is no second period to test on.
     - The client ID is not a time order: the first and second quarters of the IDs cannot be told apart (adversarial ROC AUC 0.504), and training on the first 80% of IDs scores 0.795 on the last 20%, inside the range of random 80/20 splits (0.766 to 0.800).
     - By its use case the task is temporal (a bank scores next month's payments with a model built on earlier months), so the rules ship it random but tagged as forced from temporal, which the definition lacks[^2a].
   * **Background:** the UCI page lists the six monthly columns by calendar month for all rows and gives no date per
     client (no account opening, no extraction date); the paper's data are one bank's card holders at one time. The
     IDs fall into two parts: IDs 1 to 15,000 are in random order (lag-1 correlation of age -0.001, of sex 0.008),
     IDs 15,001 to 30,000 are sorted in runs by sex and age (lag-1 correlation 0.99 and 0.79). A model tells the two
     halves apart at ROC AUC 0.768, mostly from the amounts around July (`PAY_AMT3`, `PAY_AMT2`, `BILL_AMT4`); no
     single column does better than 0.558, the default rate is 22.5% against 21.7%. No source says what the two parts
     are (two extracts, branches or card products); they are not months, since both cover the same six.
   * **Experiments:** checks of 2026-11-04 on the UCI file (re-downloaded), LightGBM on the 23 features, ROC AUC:

     | Check | Result |
     |---|---|
     | Default rate per 1,000 IDs | 20.6% to 24.6% in the first half, 16.5% to 29.5% in the second (chi-squared over 20 bins p < 0.001); lag-1 correlation of the target 0.001 |
     | Model telling low from high IDs: halves / first vs second quarter / random halves | 0.768 / 0.504 / 0.501 |
     | First 80% of IDs to the last 20% / last 80% to first 20% / random 80/20 (10 splits) | 0.795 / 0.757 / 0.781 (0.766 to 0.800) |
     | First half to second / second half to first / random halves (10 splits) | 0.789 / 0.754 / 0.777 (0.771 to 0.783) |
     | 5 folds in ID order / 5 random folds | 0.781 / 0.780 |
     | Shifted window: train April-August to predict "late in September", test May-September on October default (5 splits by client) | 0.756, against 0.778 for the same five months trained on October default |
     | The shifted task on its own: "late in September" from April-August | 0.926 |

   * **Effect on the task:** none on rows or scores under B; the tag and a split note say what the random split stands
     for.
   * **Consistency:** mobile_churn and the churn snapshots, one stock month of a customer base, ship random tagged
     forced from temporal; home_credit_default_risk, an undated credit table, ships the same; heloc's and
     porto_seguro's split issues propose the same today on the same tests.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no tag (implemented) | nothing changes | none found | the score's temporal meaning is not stated; departs from the rule for undated tasks |
     | B | Random, tagged forced from temporal | `data_tags` gain `ForcedIIDFromTemporal`; a split note with the tests above and the two ID parts | follows the rule and home_credit_default_risk; the leak test passes (one row per client, ID order folds score as random folds) | none found |
     | C | By ID order | train on low IDs, test on high IDs | none found | the ID is not time: the first half is random order and the second a sort by sex and age; the score then depends on which part is held out (0.789 or 0.754) |
     | D | Shifted window | features April-August, target "late in September" from `PAY_0`; test on the next month | a split along the calendar | a target we invent, not the source's default; September's status codes differ from the earlier months' (code 1 in 12.3% of rows against at most 0.1%), so train and test features are on different scales; scores 0.756 against 0.778 on the real task |

   * **Recommendation:** B: one snapshot month allows no temporal split, and the tag says what the random score
     stands for. **Decision:** random (A), random tagged forced from temporal (B), by ID order (C) or a shifted
     window (D)?

   **Andrej (2026-11-04, discuss):** I am pretty sure that this should actually be a temporal split. What do you think?

   **Answer (AI, 2026-11-04):**

   * You asked whether this should be a temporal split.
   * By its use case, yes: a bank trains on past months and scores the next. But the data hold one snapshot. Every
     client has the same six months and the same outcome month, and there is no date per client. So no split puts a
     later period in the test set.
   * The client ID is not time. Training on the first 80% of IDs scores 0.795 on the last 20%, inside the random range
     (0.766 to 0.800); folds in ID order score as random folds (0.781 and 0.780). The first two quarters of the IDs
     cannot be told apart (0.504).
   * The IDs do hold two parts: IDs 1-15,000 in random order, IDs 15,001-30,000 sorted by sex and age, with July's
     amounts recorded somewhat differently (a model separates the halves at 0.768). That is how the file was assembled,
     not two periods: both halves cover the same six months.
   * Shifting the window (predict September's late status from April-August) would make a temporal split possible.
     It changes the task to a target we invent, and September's status is coded differently from the earlier months,
     so the model is trained on one coding and applied to another. Trained that way it scores 0.756 on October
     default, against 0.778 when trained on the real target. The rules do not let our own target replace the
     source's[^2b].
   * My view: the task is temporal, the data cannot give a temporal split. That is the forced-from-temporal case, as
     for mobile_churn's one stock month and home_credit_default_risk. Ship random with the tag (B) and a note on the
     two ID parts.
   * Recommendation: B. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, add `data_tags = ("ForcedIIDFromTemporal",)` (as home_credit_default_risk declares it),
   a split note in `curation_comments` (use case temporal; one snapshot, same six months and outcome month for every
   client; ID not time: the numbers above; the two ID parts and their adversarial 0.768; recover a dated panel if a
   later release has one), one sentence in `fit_reason`, `split` text unchanged, `dataset check`; then a CC line for
   the split in the record. Evidence: `order_checks.py`, `halves.py`, `model_checks.py`, `adv_detail.py` and their
   outputs in the local job folder `ba_marks_1104/credit_card_clients_default`.

   [^2a]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows, including one
     stock month of a base, ships in the closest regime that keeps the rows, tagged as forced from temporal, once a
     leak test across the split finds no shared outcome, hidden group or order dependence. **SPLIT-22** (Should): the
     raw file order can be the time order; here it is not.
   [^2b]: **TP-6** (Must): a better version the source itself defines replaces the current task; a fix of our own
     invention does not. **USE-5** (Must): predict what the actor acts on; here the source's default, not a late
     status.

   **Answer (AI, 2026-11-06):** In time terms the split stays random and only its tag changes: random clients with the
   tag of issue 3 (a), by ID order (c), or a shifted window (d)?

   * **Problem:**
     - Every client is scored at one moment, after the September 2005 statement, and every target is the next month's payment, so the file holds one prediction moment and one outcome month, and no client's row lies after another's.
     - Since 2026-11-05 the split rules give such a release a use-case prototype, not the forced tag, and they cite this dataset's next-month payment as a delayed target[^2ta].
     - So B's tag moves to issue 3, and this issue decides only the split: random, by ID order, or a shifted window.
   * **Background:** your point stands for the use case: a bank trains on past months and scores the next. The file
     cannot test it, since it has no second moment; the prototype of issue 3 says so in the definition, and the
     record keeps `Target: Later`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random clients (A, with issue 3's tag) | random splits as now; the tag and its line in issue 3 | one moment and one outcome month, so a random split mixes no periods | the next month is not tested |
     | c | By ID order (C) | train on low IDs, test on high IDs | none found | the ID is not time (the first two quarters cannot be told apart, 0.504) |
     | d | Shifted window (D) | features April to August, target late in September | a split along the calendar | a target we invent; September's status codes differ from the earlier months' |

   * **Recommendation:** a, random clients. **Decision:** a, c or d?

   [^2ta]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`. **SPLIT-32** (Should): `Samples: One
     Moment` with the target at one shared later date is IID data, such as the October 2005 payment of
     credit_card_clients_default.

   **Andrej (2026-11-11, discuss):** Reply (a): Random clients (A, with issue 3's tag)

   **Resolved (2026-11-09, Andrej):** a: random clients, with issue 3's time basis, `DelayedTarget` (its line is in
   `curation_comments` since 2026-11-06; the tag enters `data_tags` once PR #50 is in the working copy). Andrej's note:
   "Set this to DelayedTarget, if not already done."

   **Resolved (2026-11-11, Andrej):** a, carried out here: the random split stays, the `Time basis: DelayedTarget:`
   bullet is in `curation_comments` and `data_tags = ("DelayedTarget",)`, as this working copy has the time-basis tags.
   Issue 1's exception to the cleaning rule is written into the same notes. `dataset check`: 0 errors, 0 warnings.
   One part of issue 1's notes is left: the exception row in the curation rules' cases table, which this run does not
   edit.

3. **Time basis: name the random split a `DelayedTarget`, one extract scored for the next month's payment?**

   * **Problem:**
     - Every client is scored once, after the September 2005 statement, with the same six months of history (April to September 2005), and the target is default on the next month's payment, the same month for every client.
     - The record's collection facts fit (`Samples: One Moment`, `Target: Later`), and the random split carries no time basis; issue 2 proposed the forced tag, which the amended rules no longer give a release of one moment.
     - Name it a `DelayedTarget`, with the line below?
   * **Background:** a delayed target needs its window closed for every row and every feature in existence at the
     moment[^3t1]. The window: one month, reported for all 30,000 clients. The features: the 18 monthly status, bill
     and payment columns end in September by their names (UCI: "X6 = the repayment status in September, 2005"); the
     credit limit, sex, education, marriage and age carry no date and are read as of the extract. The client ID is not
     a time order (issue 2).
   * **Effect on the task:** none on rows, splits or scores.
   * **Unknown:** the extraction date and the outcome month are not named by UCI (October 2005 by reading), nor
     whether the credit limit is as of September or of a later extract; a limit cut after a missed payment would be a
     late value, which the file cannot show.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `DelayedTarget` | `data_tags` gain `DelayedTarget`; a `Time basis:` line names the extract, the history and the month | states one moment and one outcome month; the amended rule cites this dataset | rests on the reading of the credit limit as of the extract |
     | C | Random, forced from temporal (issue 2's B) | `data_tags` gain `ForcedIIDFromTemporal` | marks the stand-in for a monthly forecast | the amended rule keeps the forced tag for lost time and too few periods[^3t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("DelayedTarget",)` (no tag is listed now) and the
   curation bullet "- Time basis: DelayedTarget: one extract of 30,000 card holders of one Taiwanese bank, scored
   after the September 2005 statement with the same six months of history for every client (April to September
   2005); the target is default on the next month's payment, one month closed for every client. The client ID is not
   a time order (the first two quarters of IDs cannot be told apart, ROC AUC 0.504). The credit limit and the
   demographics carry no date. Not tested: a later month."; `dataset check`. The record's facts stay.

   [^3t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `DelayedTarget` has one prediction moment for all rows and the target after it; its line
     names the moment and the window, the window has closed for every row, and every feature existed at the moment.
     Cases: credit_card_clients_default. **LEAK-10** (Must): a feature holds only what existed at the prediction point.
   [^3t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment is not forced; SPLIT-32 gives it
     `Snapshot` or `DelayedTarget`.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the `DelayedTarget` issues of
   one-moment releases with one mark?" The `Time basis: DelayedTarget:` bullet is in `curation_comments`; it says why
   the random split is IID here (every row shares the moment and the outcome window, so no test row is later than a
   training row) and ends with what the split cannot test (a later month). The split and `data_tags` are unchanged; the
   tag `DelayedTarget` enters `data_tags` once PR #50 is in the working copy. Issue 2 (the split) stays open for its own
   mark.

## Reference

The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients
By I. Yeh, Che-hui Lien. 2009

Published in Expert systems with applications
