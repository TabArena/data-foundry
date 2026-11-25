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
- Database Snapshot
original_source: UCI
year: '1994'
collection_period: 1973-1975
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

CC (2026-10-15, Andrej): Keep, with the corrected code table. Grömping (2019) traced the data back to their original sources.
- Code table, corrected in the v2 definition (container not rebuilt yet):
  - Problem: the Statlog code table mislabels 8 of the 20 features and reverses people_liable. Our "no checking account" was the safest group (11.7% bad; in fact a balance of at least 200 DM), and 96.3% were "foreign workers" (in fact 3.7%). This mattered only for models that read the category text.
  - Fix: relabelled with Grömping's corrected table, checked against South German Credit row by row. Updated 2026-11-10: the values now follow UCI 573 too (57 coded values and an amount or an age in 10 loans corrected, the curator's marks of 2026-10-31, kept by Andrej on 2026-11-10), and the banded scores are labelled by its code table. The task summary states the period, the sample, the target and that credit amounts are transformed. `year` stays 1994, the donation year, as the v2 convention asks.
- Remaining issues, none of which excludes it:
  - Age: the loans were granted in 1973-1975 by a regional bank in southern Germany (Häußler 1979; Fahrmeir & Hamerle 1984); 1994 is only the year of the UCI donation. Not severe on its own.
  - Size: 1,000 loans from one bank. Not "Too Small": about 100 bad loans per test fold. It is our small-data finance task; other datasets like heloc, give_me_some_credit, home_credit_default_risk and lending_club_1m cover modern credit.
  - Only granted loans: outcomes for rejected applicants are missing. Not severe: credit data are built this way, and the target is well defined (bad = did not comply with the loan contract as required).
  - Oversampling: bad loans are 30% here, against about 5% in the bank's portfolio. The source drew a fixed number of good and bad loans; how the loans within each group were chosen is undocumented. Predicted probabilities therefore refer to the 30% sample, not to the portfolio. Not severe: every row is a real, distinct loan (no copied or synthetic rows), sampling more of the rare class is a common design for credit data, and all methods are compared on the same sample.
  - Hand-typed data: Hofmann typed the rows in from a book appendix. Against the Open Data LMU copy (= South German Credit), 10 rows differ in one amount or age each (e.g. 731 vs 713, 50 vs 40) and 45 other values differ. Only one value (a housing level) is shown to be wrong in Statlog; the published tables cannot decide the others. Updated 2026-11-10: no longer left as is; the definition reads UCI 573, whose values are the maintainers' copy and agree with the book where the book can decide.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix {"labels":["good","bad"],"matrix":[[0,1],[5,0]],"prediction":"proba"} — the Statlog cost matrix (5 for a bad customer predicted good, 1 for the reverse; UCI german.doc, Michie et al. 1994), from probabilities by least expected cost.

CC (2026-10-21, Lennart): Unsure whether the cost matrix should score probabilities or labels (TabArena tunes thresholds); the AI's choice, probabilities with the least expected cost, is applied.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `employment_since`, `job` (the README lists their levels); left unordered: `checking_status` (a level outside the scale is a state of its own); `savings_status` (a level outside the scale is a state of its own); `property` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `installment_rate_percent`, `residence_since`, `existing_credits_count`; labels relabelled by the corrected code table (Groemping 2019, UCI 573 South German Credit): Statlog's german.doc is wrong for checking_status, credit_history, credit_purpose, savings_status, personal_status_sex, property, housing and foreign_worker; matched on duration, amount and age, the codes correspond one to one (990 rows). UCI 573 also corrects a few values (34 rows of other_installment_plans, 10 of foreign_worker, 1 of housing), not applied: a question for the curator..

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 3 ordinal scales shipped as numbers are ordered categories (point 3); 3 columns with a state outside the scale ordered, the state placed by the rule; the source is UCI 573 (South German Credit, the corrected Statlog data): every code labelled by its code table, 57 coded values and 10 typos in amount or age corrected; 9 ordinal scales, the account and property states missing by the state rule.

CC (2026-11-10, Andrej): UCI 573's corrected values kept (Review issue 1, ok, option A); the "Fix" and "Hand-typed data" bullets of the CC of 2026-10-15 are updated, `## Reference` gains UCI 573's DOI, and `task_summary.changes` names the switch to UCI 573. Time basis forced from temporal (issue 2, option B): `ForcedIIDFromTemporal` with its `Time basis:` line (credits of 1973-1975, no grant date in either file). Split unchanged.

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 3, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. A 1973-1975 bank sample scored for later applicants spans decades of changed currency, products and rules; no domain reason holds.

## Review

**Outcome:** added. The Statlog German credit data (UCI, 1994), read since 2026-10-31 from their corrected version,
UCI 573 South German Credit (Grömping 2019): 1,000 consumer loans granted in 1973-1975 by a regional bank in southern
Germany, bad loans sampled up from about 5% to 30%, scored by the Statlog cost matrix. Reviewed on 2026-11-04 without a
panel: a real lending decision with an outcome label, every feature from the application, no leak found; methods
separate (0.192 1-AUC for the best method to 0.234 for default LightGBM), though a hand-built scorecard comes close.
UCI 573's corrected values stay (issue 1) and the random split is tagged forced from temporal (issue 2); stationarity
reasoning of 2026-11-18: the forced tag stays (issue 3, A, Andrej).

**Main points:** Nothing open: UCI 573's corrected values stay, with the record and definition text corrected (issue 1,
A, 2026-11-10); the random split is tagged `ForcedIIDFromTemporal` (issue 2, B, 2026-11-10); the forced tag stays, not
`AssumedStationaryRelation` (issue 3, A, 2026-11-18).

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

   **Notes for the AI:** on B: `data_tags = ("ForcedIIDFromTemporal",)` and the curation bullet
   "- Time basis: ForcedIIDFromTemporal: consumer credits granted from 1973 to 1975, each judged good or bad over its
   own term (4 to 72 months, no stated horizon); neither UCI 573's file (sorted by class) nor Statlog's (no order)
   keeps a grant date, so random loans stand in for later applicants. A dated release would allow a split by grant
   year."; `fit_reason` keeps its sentence; no `splits_comment` (default split); the record's facts stay.

   [^2a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split; it says
     what a dated release would change.

   **Resolved (2026-11-10, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal",)` and the drafted `Time basis:
   ForcedIIDFromTemporal:` bullet in `curation_comments` (credits of 1973-1975, no grant date in either file, a dated
   release would allow a split by grant year). `fit_reason` keeps its sentence; split and record facts unchanged.

3. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Consumer credits granted 1973-1975 (South German Credit, Groemping 2019); neither UCI 573's file (sorted by class) nor Statlog's keeps a grant date.
     - Use: A bank decides on later applications; any use today is about 50 years after collection.
     - Mechanism: Good/bad repayment follows the applicant's finances, the bank's grant policy and the economy; Deutsche Mark amounts, 1970s products and a stratified (oversampled bad) sample tie it to its time and selection.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | lending_club (this collection, matched-v2 stationary-relation test) | 36-month LendingClub loans, issue years 2013-2015 each tested forward vs contemporaneous on the same test half (LightGBM, whole half) | not flat: forward worse by 0.0043-0.0059 ROC AUC (2.4-4.2 floors, beyond 2 SD) in all three years; default rate 10.0-15.2% by year | consumer credit default from application/bureau data, outcome over months after the grant |
     | Kelly, Hand & Adams, 'The impact of changing populations on classifier performance', KDD 1999 (doi 10.1145/312129.312285); Hand, 'Classifier technology and the illusion of progress', Statistical Science 2006 (arXiv math/0606452) (literature, cited from memory: check) | scorecard performance on UK bank unsecured personal loans 1993-1998 as the applicant population drifts | not flat: population drift degrades scorecards; Hand names drift as a particular concern in credit scoring because defaults arrive long after the grant | application scoring of consumer credit |

   * **For a stationary use case:**
     - Basic credit risk factors (checking account status, duration, history) keep their direction.
   * **Against:**
     - Old one-time study used today: a 50-year span in a market domain (currency, products, rules changed).
     - Bank grant policy decides who is in the data (only granted loans observed) and changes over time.
     - The original Statlog coding had errors corrected only in 2019: coding changes.
     - Credit-scoring literature and lending_club show drift over far shorter spans.
   * **Earlier views:**
     - CC (2026-11-17, Andrej): blind split walk: the decision tree, walked without the current split, reaches the forced split it ships.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Old one-time study used today: a 50-year span in a market domain (currency, products, rules changed).; Bank grant policy decides who is in the data (only granted loans observed) and changes over time. |

   * **Recommendation:** A, a 1973-1975 bank sample scored for later applicants spans decades of changed currency, products and rules; no domain reason holds. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (A 1973-1975 bank sample scored for later applicants spans decades of changed currency, products and rules; no domain reason holds.)

## Reference

10.24432/C5NC77

Grömping, U. (2019). South German Credit Data: Correcting a Widely Used Data Set. Reports in Mathematics, Physics and Chemistry, Report 4/2019. Department II, Beuth University of Applied Sciences Berlin. http://www1.beuth-hochschule.de/FB_II/reports/Report-2019-004.pdf

Grömping, U. (2019). South German Credit [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5X89F

Grömping, U. (2020). South German Credit (UPDATE) [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5QG88

Häußler, W. M. (1979). Empirische Ergebnisse zu Diskriminationsverfahren bei Kreditscoringsystemen. Zeitschrift für Operations Research, 23, B191-B210. https://doi.org/10.1007/BF01917956

Fahrmeir, L., & Hamerle, A. (1984). Multivariate statistische Verfahren (1st ed., Ch. 8 and Appendix C). De Gruyter, Berlin.
