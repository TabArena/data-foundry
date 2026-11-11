---
unique_name: credit_g
name: credit-g
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
- 'Target: Varying Delay'
original_source: UCI
year: '1994'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=31
- https://doi.org/10.24432/C5NC77
notebook_path: datasets/beyond_iid/old_iid/credit_g/credit_g.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/credit_g/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. TabRed says that task requires time based split, but no time feature given. However, if time-invariant features are used that might not matter. Also might be outdated as nowadays other features might be used; only time dependency could be the bank's and the world's financial state as a confounding factor

Potential issue: Outdated (Deutsche Mark)

Lennart: Temporal impact unclear and not resolvable, otherwise ok and not too old

Andrej: Fits criteria, but honestly this dataset with only 1000 samples from 1994 is not representative of a credit scoring task anymore. If no better dataset is available I would not use it

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix {"labels":["good","bad"],"matrix":[[0,1],[5,0]],"prediction":"proba"} — the Statlog cost matrix (5 for a bad customer predicted good, 1 for the reverse; UCI german.doc, Michie et al. 1994), from probabilities by least expected cost.

CC (2026-10-21, Lennart): Unsure whether the cost matrix should score probabilities or labels (TabArena tunes thresholds); the AI's choice, probabilities with the least expected cost, is applied.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `employment_since`, `job` (the README lists their levels); left unordered: `checking_status` (a level outside the scale is a state of its own); `savings_status` (a level outside the scale is a state of its own); `property` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `installment_rate_percent`, `residence_since`, `existing_credits_count`; labels relabelled by the corrected code table (Groemping 2019, UCI 573 South German Credit): Statlog's german.doc is wrong for checking_status, credit_history, credit_purpose, savings_status, personal_status_sex, property, housing and foreign_worker; matched on duration, amount and age, the codes correspond one to one (990 rows). UCI 573 also corrects a few values (34 rows of other_installment_plans, 10 of foreign_worker, 1 of housing), not applied: a question for the curator..

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3); 3 columns with a state outside the scale ordered, the state placed by the rule; the source is UCI 573 (South German Credit, the corrected Statlog data): every code labelled by its code table, 57 coded values and 10 typos in amount or age corrected; 9 ordinal scales, the account and property states missing by the state rule.

CC (2026-11-11, Andrej): review marks applied (Review issues 1 and 2). Rows, columns and the random split are unchanged (1,000 loans).

- Issue 1 (`ok`): the definition keeps reading the corrected release, UCI 573 (South German Credit, Grömping 2019), whose code table relabels 8 of the 20 features and which corrects 57 coded values and an amount or an age in 10 loans. The text items that went with the switch are fixed: `task_summary.changes` now names it, the notebook leftover "We reversed the original ordinal encoding." is removed, the ordinal bullet no longer repeats its clause, and `## Reference` gains Grömping's report and the two UCI uploads (10.24432/C5X89F and the file the definition reads, 10.24432/C5QG88).
- Issue 2 (B, "Option B: Forced from temporal."): `data_tags = ("ForcedIIDFromTemporal",)` with the `Time basis:` bullet: consumer credits granted from 1973 to 1975, each judged over its own term (4 to 72 months, no stated horizon), and neither file keeps a grant date, so random loans stand in for later applicants. A dated release would allow a split by grant year. `fit_reason` and the split are unchanged.
- `dataset check` passes (0 errors, 0 warnings).

## Review

**Outcome:** added. The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a panel, from the
evidence already gathered (your review of 2026-10-15, the curator's marks of 2026-10-31, model runs on the
shipped data and on the TabArena v0.1 task of the same source). The data are the Statlog German credit data (UCI,
1994), read since 2026-10-31 from their corrected version, UCI 573 South German Credit (Grömping 2019): 1,000 consumer
loans granted in 1973-1975 by a regional bank in southern Germany, bad loans sampled up from about 5% to 30%, scored
by the Statlog cost matrix (a bad loan predicted good costs 5, the reverse 1). Validity: a real lending decision with
an outcome label (did not repay as the contract required), every feature from the application, no leak found; only
granted loans and the oversampling are the design of credit data, not defects (your call of 2026-10-15). Value: the 40
benchmark methods spread from 0.192 1-AUC (KumoRFM) over 0.196 (TabPFN-3.5) and 0.205 (tuned CatBoost) to 0.212-0.217
(logistic regression) and 0.234 (default LightGBM); a hand-built scorecard with a small boosted correction reaches
0.190, so the task is close to an additive score, but methods separate. Quality: the corrected code table and values
of UCI 573; the definition loads with 1,000 loans (700 good, 300 bad) and 37 foreign workers (3.7%, as Grömping
reports). Weighed: a documented source with corrected labels +, a real credit decision +, 50 years old and 1,000
loans from one bank -.

**Main points:** All settled (2026-11-10): UCI 573's corrected values stay (issue 1, A), the random split is tagged
forced from temporal (issue 2, B).

**Record judgment:** valid, ship. To correct at hand-over (no mark needed): `## Reference` cites the first South
German Credit upload (UCI 522, DOI 10.24432/C5X89F) but not the file the definition reads (UCI 573, DOI
10.24432/C5QG88); in `curation_comments` the line "We reversed the original ordinal encoding." is left from the
notebook, and the ordinal bullet repeats "9 columns are ordered categories"; `task_summary.changes` names only the
relabelling, not the switch to UCI 573. Your CC of 2026-10-15 is updated by issue 1's decision. (All four corrected
on 2026-11-10 with issue 1.)

**Issues for Andrej:**

1. **Keep UCI 573's corrected values, which replace the Statlog typos you chose to keep?**

   * **Problem:**
     - On 2026-10-15 you kept Statlog's values as typed, typos included, and relabelled only the codes.
     - The curator's marks of 2026-10-31 switched the source to UCI 573, Grömping's corrected file, which changes 57 coded values and an amount or an age in 10 loans.
     - Keep the corrected file, or go back to Statlog's values under the corrected labels?
   * **Background:** Hofmann typed Statlog's 1,000 rows from the appendix of Fahrmeir & Hamerle (1984); UCI 573 holds
     the values of the copy at Fahrmeir's university (Open Data LMU Munich), with Grömping's corrected code
     table[^1a]. Matched on duration,
     amount and age, the two copies agree except for 12 values of credit purpose, 34 of other instalment plans, 10 of
     foreign worker, 1 of housing, and one amount or age in 10 loans (731 against 713, 50 against 40). The one value
     the book's printed table can decide (a housing level) is wrong in Statlog and right in UCI 573; the book's
     shares of instalment plans and foreign workers fit both copies.
   * **Experiments:** the v0.2 definition loads 1,000 loans; its credit amounts equal Statlog's for 990 loans when
     both are sorted.
   * **Consistency:** a damaged release is repaired from its origin when the origin has the clean data[^1b]; your call
     of 2026-10-15 was made before UCI 573 was read as the source.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | UCI 573 (implemented) | reads SouthGermanCredit.asc with its own code table; 57 coded values and 10 amounts or ages differ from Statlog | one file from the data's maintainers with its own labels; agrees with the book where the book can decide | departs from your call of 2026-10-15; most differences cannot be proven either way |
     | B | Statlog values, corrected labels | reads german.data and maps its codes to UCI 573's labels, as on 2026-10-15 | the rows as Hofmann typed them; your earlier call | keeps a housing value shown to be wrong and 66 more that are probably typos |

   * **Recommendation:** A, the maintainers' corrected file, which the one checkable difference favours.
     **Decision:** UCI 573's values (A) or Statlog's values (B)?

   **Notes for the AI:** on A, rewrite the "Fix" and "Hand-typed data" bullets of the record's CC of 2026-10-15 (the
   values now follow UCI 573; "left as is" no longer holds), and fix the text items of the record judgment. On B,
   restore the Statlog read and code map of the branch's definition before the merge of 2026-11-04 (first parent of
   4a2c40f6), keep today's `ORDINAL_LEVELS` and missing states, and re-run `dataset check`.

   [^1a]: Grömping, U. (2019). South German Credit Data: Correcting a Widely Used Data Set. Reports in Mathematics,
     Physics and Chemistry, Report 4/2019, Beuth University of Applied Sciences Berlin.
     http://www1.beuth-hochschule.de/FB_II/reports/Report-2019-004.pdf; data: https://doi.org/10.24432/C5QG88
   [^1b]: **PROV-13** (Must): when a release is damaged, check whether the origin has the clean data, and repair or
     rebuild from the origin when it has them.

   **Andrej (2026-11-11, ok):** (the mark alone, no note)

   **Answer (AI, 2026-11-11):** carried out on this branch, with one part that does not apply. The definition keeps
   reading UCI 573. Of the four text items of the record judgment, three are fixed here: `task_summary.changes` now
   names the switch to UCI 573 and what it corrects, the notebook leftover "We reversed the original ordinal
   encoding." is gone, and the ordinal bullet no longer repeats its clause; the record's `## Reference` gains
   Grömping's report and the two UCI uploads (C5X89F and the file the definition reads, C5QG88). The fourth, rewriting
   the "Fix" and "Hand-typed data" bullets of the CC of 2026-10-15, has nothing to rewrite: this branch's record does
   not carry that comment.

   **Resolved (2026-11-10, Andrej):** A: the definition keeps reading UCI 573. The "Fix" and "Hand-typed data" bullets
   of the record's CC of 2026-10-15 now say the values follow UCI 573; the record's `## Reference` gains UCI 573's DOI
   (10.24432/C5QG88); in `curation_comments` the leftover "We reversed the original ordinal encoding." is gone and the
   repeated ordinal phrase is fixed; `task_summary.changes` names the switch to UCI 573. Data unchanged.

2. **Time basis: name the random split forced from temporal (`ForcedIIDFromTemporal`)?**

   * **Problem:**
     - The credits were granted from 1973 to 1975 and each was judged over its own term, and neither copy of the data
       keeps time: UCI 573's file is sorted by class (good loans first), and Statlog's file has no order at all (bad
       rate flat over its tenths, chi-squared p = 0.33).
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, `Target: Varying
       Delay`), but the definition names no time basis, though its `fit_reason` says the random split stands in for
       scoring later applicants.
     - The use case scores later applicants, and defaults move with the economy (the grants span the oil crisis of
       1973 and the recession of 1974-75), so of the time bases only the forced tag fits: name it, or another one?
   * **Background:** the questions that tell the time bases apart[^2a]:
     - Can time affect the target? Yes: whether a borrower repays follows the economy of the loan's years.
     - Does the use case predict for a time after its data? Yes: the bank scores new applicants from loans already
       judged.
     - One shared prediction moment? No: each credit at its own grant date, judged after a term of 4 to 72 months
       with no stated horizon, so a delayed target with one moment does not fit either.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: three years
       of grants through a recession; with the time lost that is the forced case[^2b].
     - The sample is stratified (bad loans raised from about 5% to 30%), so the share of bad loans is the design's,
       not a period's.
   * **Experiments:** today's checks, model-free: the time probe finds no date-like column and the definition's raw
     file sorted by class (good share 0.96 to 0.99 per hundred rows in the first five hundred, 0 in the last two
     hundred); in Statlog's `german.data` the bad rate (chi-squared p = 0.33), duration, amount and age (rank
     correlation with the position at most 0.06) show no order. The leak test across a forced split: no duplicate
     rows, no order in the frame; a debtor with several credits cannot be seen, and period effects cannot be tested
     without dates.
   * **Unknown:** whether `credit_history` ("existing credits paid back duly till now") and `number_credits` (the
     debtor's credits at this bank) were recorded at the application or when the sample was drawn; if the latter,
     they could reflect behaviour after the grant. The sources do not say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | no time tag; the `fit_reason` sentence alone says what the split stands for | nothing changes | `dataset check` notes a split that is not temporal and does not say why |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line naming 1973-1975, the undated files and what a dated release would change | says in the metadata what `fit_reason` already says; the leak test finds nothing | none found |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that repayment follows the application whenever granted | none found | defaults move with the economy; no dated data to measure it on |

   * **Recommendation:** B: a forward use case whose time is lost is what the forced tag names. **Decision:** no time
     basis (A), forced (B) or stationary relation (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("ForcedIIDFromTemporal",)` and the curation bullet
   "- Time basis: ForcedIIDFromTemporal: consumer credits granted from 1973 to 1975, each judged good or bad over its
   own term (4 to 72 months, no stated horizon); neither UCI 573's file (sorted by class) nor Statlog's (no order)
   keeps a grant date, so random loans stand in for later applicants. A dated release would allow a split by grant
   year."; `fit_reason` keeps its sentence; no `splits_comment` (default split); the record's facts stay. Evidence:
   `~/claude_jobs/time_review/credit_g/statlog_order.txt`, `~/claude_jobs/time_review/b3_probe/credit_g.json`.

   [^2a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split; it says
     what a dated release would change.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-10, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal",)` and the drafted `Time basis:
   ForcedIIDFromTemporal:` bullet in `curation_comments` (credits of 1973-1975, no grant date in either file, a dated
   release would allow a split by grant year). `fit_reason` keeps its sentence; split and record facts unchanged.

## Reference

10.24432/C5NC77

Grömping, U. (2019). South German Credit Data: Correcting a Widely Used Data Set. Reports in Mathematics, Physics and Chemistry, Report 4/2019. Department II, Beuth University of Applied Sciences Berlin. http://www1.beuth-hochschule.de/FB_II/reports/Report-2019-004.pdf

Grömping, U. (2019). South German Credit [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5X89F

Grömping, U. (2020). South German Credit (UPDATE) [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5QG88
