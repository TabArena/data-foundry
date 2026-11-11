---
unique_name: in_vehicle_coupon_recommendation
name: in_vehicle_coupon_recommendation
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
tags:
- 'Samples: No Time Dimension'
original_source: Other
year: '2017'
required_split:
- Grouped (NON-IID)
source_links:
- https://www.researchgate.net/publication/318645502_in-vehicle_coupon_recommendation
- https://doi.org/10.24432/C5GS4P
notebook_path: datasets/beyond_iid/old_iid/in_vehicle_coupon_recommendation/in_vehicle_coupon_recommendation.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/in_vehicle_coupon_recommendation/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Re-split as a cold-start task, grouped by survey respondent; ROC AUC 0.83 random -> 0.75 grouped.** Wang et al. 2017 (JMLR 18), Sec. 6.2: MTurk survey, 652 accepted surveys, 12,684 rows; "In the first part of the survey, we asked users to provide their demographic information and preferences. In the second part, we described 20 different driving scenarios ... to each user"; evaluated with random 5-fold testing (Table 3), i.e. warm start. The file has 22 scenarios per person from 19 fixed questionnaire versions, answered in one sitting without timestamps, so there is no interaction history to simulate a warm start; a random split lets a model learn each person's tendency to say yes from their other hypothetical answers. We simulate a cold-start model (as used before a recommender has history for a user): new people, known profile and stated habits (the visit-frequency columns are the base preference). The respondent id is not shipped; the raw file lists each respondent's answers as one consecutive block with identical first-part answers (13 columns), giving 587 groups (517 of 22 rows; a few blocks likely merge two adjacent respondents with identical profiles, which is stricter). The audit's profile-only id (567 groups) merged different people. LightGBM on the grouped splits: AUC 0.75 (0.742-0.764 over 6 folds). TabArena v0.1 dataset: results on the old IID container are not comparable.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

data was collected via a survey on Amazon Mechanical Turk. The survey describes different driving scenarios including the destination, current time, weather, passenger, etc., and then ask the person whether they will accept the coupon if they are the driver. features might be time invariant, but need to check

Potential issue: "faked" data via a survey

Lennart: Leaning towards yes, features seem time invariant; but data source might be fake

Andrej: Need to test whether time-invariant; Mechanical turk data might be interesting to include

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — AUC (out-of-sample, 5-fold, Table 3) (Wang et al. (2017), A Bayesian framework for learning rule sets for interpretable classification, JMLR 18(70), Sec. 6.2 and Table 3).

CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: the respondents are Amazon Mechanical Turk workers, a volunteer sample rather than the drivers of an in-vehicle recommender, as the web volunteers of obesity_estimation; the stated intentions about imagined trips are a separate gap, already in the fit_reason.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 8 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `age`, `education`, `income`, `Bar`, `CoffeeHouse`, `CarryAway`, `RestaurantLessThan20`, `Restaurant20To50` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `tianchi_o2o_coupon_redemption` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 coded columns carry their words.

CC (2026-11-11, Andrej): Review issue 1, B ("Option B: Drop direction_opp."): `direction_opp` is 1 minus `direction_same` in all 12,684 rows, so `_clean` drops it and the categorical list loses it (23 features); the nested distance flags `toCoupon_GEQ15min` and `toCoupon_GEQ25min` stay separate (CLEAN-13). This branch carried an older definition that still had both columns, and no `Time basis:` line for the settled issue 2 either, so the `Timeless` bullet and `data_tags = ("Timeless",)` went in at the same time. `dataset check`: 0 errors, 0 warnings, 2 info.

## Review

**Outcome:** added. The AI recommends shipping it as defined, with one small cleaning step (issue 1, applied 2026-11-10). Reviewed on
2026-11-04 without a panel, from the evidence already gathered (the record, the leak audit of 2026-09-24 and
2026-09-30, model runs on the TabArena v0.1 task of the same source) and one check on the source rows. The
data are Wang et al.'s (2017) Amazon Mechanical Turk survey (JMLR 18(70), Sec. 6.2): each respondent gave a profile
(sex, age, family, education, job, income) and how often they visit bars, coffee houses, take-aways and restaurants,
then answered about 22 imagined driving scenarios with a coupon offer; the target is whether they say they would
accept it (56.8%). v0.2 rebuilds the respondent from the file's consecutive blocks of identical profiles (587
respondents) and holds out whole respondents. Validity: the two gaps of the data are stated, not hidden: the answers
are stated intentions about imagined trips, not coupons accepted in a car (an approximate fit), and the respondents are
Mechanical Turk volunteers (`Selection Bias`), both Lennart's calls (2026-09-30, 2026-10-27); the split is a cold
start for a new user, since a random split let a model learn each person's habit of saying yes from their other
answers (ROC AUC 0.83 random against 0.75 grouped). Value: on the v0.1 random split the benchmark methods spread widely
(1-AUC 0.142 for TabPFN-3.5, 0.155 for tuned gradient boosting, 0.265 for logistic regression), but that split
rewarded recognising respondents (respondent and coupon type explain 51% of the target variance in-sample), so the
spread on the grouped split is not measured. Quality: `direction_opp`, the exact complement of
`direction_same`, is dropped (issue 1); 43 exact repeats and 10 conflicting rows (0.1%). Weighed: a documented survey built for this prediction +,
an honest cold-start split +, stated intentions of volunteers instead of real redemptions -, respondents rebuilt from
the file order (587 against the paper's 652 surveys, which can only merge people, a stricter grouping) -.

**Main points:** `direction_opp`, a copy of `direction_same` with the values swapped, is dropped (issue 1, resolved
2026-11-10). The respondent-grouped split is named `Timeless` (issue 2, resolved 2026-11-06).

**Record judgment:** valid, ship. The survey is a stated-preference study the paper runs as data for an in-vehicle
recommender, so a decision stands behind it; the gap between saying yes to an imagined offer and redeeming a coupon is
named in `fit_reason`. It is a response task on a person's profile and the
offer, not a ranking or click log, the distinction the 2026-10-27 reject check of
`criteo_sponsored_search_conversion_log` drew when it named this dataset as an unlike case. The data-scouting run of
2026-10-30/31 found `tianchi_o2o_coupon_redemption` (Alibaba's real coupon redemptions) as better data for the same
task; it is screened in its own record and does not change this verdict. The record has no `domain` or
`problem_type` field; the definition's values (business & marketing, binary classification) can be filled in without
a mark.

**Issues for Andrej:**

1. **Drop `direction_opp`, which is `direction_same` with 0 and 1 swapped?**

   * **Problem:**
     - In every one of the 12,684 rows `direction_opp` equals 1 minus `direction_same` (whether the venue lies in the same or the opposite direction as the trip).
     - The second column adds no information, only a second copy of the same split.
   * **Experiments:** checked on the source rows of the shipped container (Slurm job 1344881): complement in all
     rows. The distance flags `toCoupon_GEQ15min` and `toCoupon_GEQ25min` are nested (every row with 25 minutes or
     more also has 15 or more) and are left as they are: flags that can be set together stay separate columns[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | no change | as the source publishes them | one column is a relabelled copy of another |
     | B | Drop `direction_opp` | 23 features instead of 24 | no copy | none found |

   * **Recommendation:** B, a copy of another column goes[^1a]. **Decision:** keep both (A) or drop `direction_opp`
     (B)?

   **Notes for the AI:** on B, add `"direction_opp"` to the drop in `_clean` next to `toCoupon_GEQ5min`, remove it
   from the categorical list, add a curation note, re-run `dataset check`, note it in the CHANGELOG.

   [^1a]: **CLEAN-5** (Should): drop constant columns, all-missing columns and exact copies of another column.
   [^1b]: **CLEAN-13** (Must): yes/no flags that can be set together stay separate columns, the lossless form.

   **Resolved (2026-11-10, Andrej):** B ("Option B: Drop direction_opp."): `_clean` drops `direction_opp` next to
   `toCoupon_GEQ5min`, it leaves the categorical list, and a curation note says why (23 features); the nested distance
   flags stay. `dataset check`: 0 errors, 0 warnings, 2 info (43 repeats, 10 conflicting rows, as before).

   **Andrej (2026-11-11, change):** Option B: Drop direction_opp.

   **Resolved (2026-11-11, Andrej):** B, carried to this branch, whose definition still had both columns: `_clean`
   drops `direction_opp` next to `toCoupon_GEQ5min`, it leaves the categorical list (23 features), and a curation note
   says why; the nested distance flags `toCoupon_GEQ15min` and `toCoupon_GEQ25min` stay separate. The same branch had
   no `Time basis:` line either, although issue 2 was settled on 2026-11-06, and the time-basis check flagged it, so
   the `Timeless` bullet and `data_tags = ("Timeless",)` went in with it (the framework here has the tag).
   `dataset check`: 0 errors, 0 warnings, 2 info (43 repeats, 10 conflicting rows, as before).

2. **Time basis: name the respondent-grouped split `Timeless`, as the answers are a designed questionnaire's
   outcome?**

   * **Problem:**
     - Each row is one scenario of a fixed questionnaire answered minutes after the profile in the same sitting, so no
       column arises after the answer and no respondent's row is later than another's in any way the release records.
     - The record carries `Samples: No Time Dimension` with no time or target fact, and the definition names no time
       basis; the file holds no timestamp, and its only order is the respondent blocks.
     - `Timeless` names the outcome of a designed run, which this scenario grid is, while `Snapshot` would name the
       one survey as the moment the data cover[^2a].
   * **Background:**
     - The survey is a design, not a stream: part one asks the profile and the visiting habits, part two about 20
       hypothetical driving scenarios from 19 fixed questionnaire versions, all in one sitting, and no coupon is ever
       redeemed (Wang et al. 2017, Sec. 6.2; the stated-intention gap is already the approximate fit).
     - The order inside a respondent's block is an order within one entity, which the collection facts do not count as
       a time, and the recruitment period of the Mechanical Turk workers is not published.
     - The file order is mostly the questionnaire design: the coupon mix moves along it from 38-43% Coffee House in
       the first three deciles to 13.5% in the last, and from 9-15% Bar to 22-23%.
   * **Effect on the task:** none on the data, split or score; the line states why a split that is not temporal is
     safe in time, and what it cannot test (a later cohort of drivers, and real redemptions).
   * **Experiments:** measured on UCI's source file today, model-free (no model run):
     - The time probe flags an order drift: consecutive rows share the answer 58.2% of the time against 50.9% by
       chance (p 6.6e-07), which is the respondent blocks, since one person's 22 answers correlate.
     - Acceptance by file decile runs 0.586, 0.614, 0.623, 0.563, 0.524, 0.567, 0.546, 0.552, 0.568, 0.541; the
       largest part of that is the coupon mix, and after subtracting the mean of each scenario cell (coupon,
       destination, passenger, time and expiration; 122 cells) the drift along the file is Spearman -0.034
       (p 0.0002), 3 to 4 percentage points between the first and the last decile.
     - Per respondent the mean acceptance falls weakly along the block order (Spearman -0.105, p 0.011; 0.601 in the
       first fifth of the blocks against 0.539 in the last), which is as much the version mix as a recruitment order,
       and nothing says the blocks follow completion.
   * **Consistency:** the one-moment surveys and scrapes of this review whose use case looks forward
     (obesity_estimation, immoscout_german_house_prices) are recommended as `Snapshot`; they sample a population,
     while this one is a designed scenario grid, the case `Timeless` names.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped by respondent, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Grouped by respondent, `Timeless` | as now; the tag and a `Time basis:` line naming the one sitting, the designed scenarios and the measured drift along the file | states the fact the split rests on; a questionnaire's answer is the outcome of a designed run | a person's stated willingness is a state, not a property of the scenario |
     | C | Grouped by respondent, `Snapshot` | the same line with the prototype for one moment, and `Samples: One Moment` on the record | reads the survey as the one moment before 2017 that the data cover | the data are a design, not a population of a moment, and the use case offers coupons later, which no split here tests |

   * **Recommendation:** B: the scenarios are a fixed design answered in one sitting, and the only order in the file is
     the questionnaire's, not a recruitment stream; C is the close call if the survey is read as one moment of a
     population. **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds the grouped tags) and a
   curation bullet `- Time basis: Timeless: each row is one scenario of a fixed questionnaire, answered in the same
   sitting as the profile (Wang et al. 2017, Sec. 6.2), so nothing in a row arrives later and no answer is in the
   future of another. The file has no timestamp; its order is the questionnaire versions (Coffee House coupons fall
   from 38-43% of the first three deciles to 13.5% of the last), and the acceptance drift that remains after the
   scenario cells are removed is 3-4 percentage points over the file (Spearman -0.034, 2026-11-06). Not tested: a
   later cohort of drivers, and whether a stated yes becomes a redemption.`; `splits_comment` unchanged;
   `dataset check`; no rebuild (comment only). On C, the record's `tags` take `'Samples: One Moment'` in place of
   `'Samples: No Time Dimension'`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts and a definition can name the use-case prototype it follows with a `Time basis:` line.
     `Timeless`: the target is a fixed property of the item, the same whenever it is measured, among them the outcome
     of a designed run; `Snapshot`: one extract, census, scrape or exam round whose use case only fills in the time
     the data cover; a time order found only within each entity does not count as a time.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept five more routine `Timeless`
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (a later cohort of drivers, and whether a stated yes becomes a redemption); the split and `data_tags` are
   unchanged. The tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

## Reference

A Bayesian framework for learning rule sets for interpretable classification By Wang, Tong, Cynthia Rudin, Finale Doshi-Velez, Yimin Liu, Erica Klampfl, and Perry MacNeille. 2017
 Published in The Journal of Machine Learning Research 18, no. 1
