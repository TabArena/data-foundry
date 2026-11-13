---
unique_name: anes_voting_2026
name: anes_voting_2026
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
collections:
- TableShift
original_source: Website
year: '2026'
domain: social science
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/
- https://tableshift.org/datasets.html#voting
notebook_path: datasets/beyond_iid/temporal/anes_voting_2026/anes_voting_2026.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/anes_voting_2026/dataset.py
source_row: 1029
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: VCF1005 is built from the post-election House vote, plus 56 post-election items the "no post IW" filter missed.** Codebook (Feb 5, 2026, VCF1005 "Party of Voter Respondent/ Party of U.S. House Incumbent"): "1. R Voted: R is partisan of same party as incumbent", "2. R Voted: ...", "3. R is major party partisan but R did not vote ...". So codes 1 and 2 exist only for voters (7,517 and 4,780 rows, all voted; filled 1976-2016, empty in 2020 and 2024). The other 56 list "no Post IW" (VCF0426, VCF0427) or "no post data" (54 VCF92xx: CSES module, knowledge items, thermometers, contributions) as a missing code, i.e. post-election interview. All 57 are now dropped. LightGBM mean AUC on the shipped temporal splits (9 test years): 0.930 with everything, 0.859 without VCF1005, 0.855 without all 57 (2020/2024 unchanged at ~0.87). VCF0713 (pre-election vote intent) and VCF9265 (pre-election: voted in the primary) are pre-election and stay.

task: predict voting participation from a detailed questionnaire.

Data: pre-election interview (features) and a post-election interview (target)

This entry refers to the February 5, 2026 version.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — ANES (the data's first publication) defines no prediction task. TableShift (Gardner et al. 2023), which defined the voting task, scores accuracy for every task of its benchmark, a house convention, not a choice from the decision; our task differs (temporal year splits, pre-election items only) and 78% voted, so accuracy at 0.5 is coarse. Original rejected: TableShift accuracy. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): metric: the fallback (roc_auc), not TableShift's accuracy.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 71 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `VCF0110`, `VCF0111`, `VCF0114`, `VCF0130a`, `VCF0138`, `VCF0140`, `VCF0140a`, `VCF0301`, `VCF0303`, `VCF0305`, `VCF0310`, `VCF0311` and 59 more (the README lists their levels); their codes that mean unknown (don't know, refused, not asked) are missing in `VCF0110`, `VCF0111`, `VCF0114`, `VCF0130a`, `VCF0138`, `VCF0140`, `VCF0140a`, `VCF0301`, `VCF0303`, `VCF0305`, `VCF0310`, `VCF0311` and 59 more (CLEAN-10); 20 counts and indices stored as text are numbers: `VCF0138a`, `VCF0138b`, `VCF0138c`, `VCF0138d`, `VCF0316`, `VCF0317`, `VCF0320`, `VCF0321`, `VCF0322`, `VCF0323`, `VCF0324`, `VCF0403` and 8 more; left unordered: `VCF0130` (a level outside the scale is a state of its own); `VCF0137` (a partial order); `VCF0148` (a partial order); `VCF0148a` (a partial order); `VCF0149` (a partial order); `VCF0155` (a level outside the scale is a state of its own); `VCF9002` (a level outside the scale is a state of its own); `VCF9044` (a partial order); `VCF9266` (a level outside the scale is a state of its own); ordinal scales shipped as numbers, left as numbers for the curator's review: `VCF0102`, `VCF0103`; codes shipped as numbers, left for the curator's review: `VCF0104`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); 4 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ces_validated_turnout` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 157 coded columns carry their words; 12 scores are numbers (VCF0834, VCF0839, VCF0842, VCF0843, VCF9073, VCF9077, VCF9081, VCF9085 and more); codes that only mean unknown are missing in the unordered codes too; VCF0130's 0 (not ascertained or not asked) missing; age 0 and the thermometers' DK/NA codes missing; open calls on the review board's ANES sheet.

CC (2026-11-01, Lennart): on the review board's ANES sheet: read 2024's attendance 9 as never (except the short form), recover 2020's VCF0130a never from VCF0130, "all of life" as the respondent's age (VCF9001 a number, VCF9002 by age band), decode the 40 master-code columns; the mention counts' 0 left as it is.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (2 means voted (ANES codebook)); counts with a cut end are numbers: VCF0138, VCF9122.

CC (2026-11-01, Lennart): counts with a cut end stay ordered categories of the source's levels, the cut end a level of its own (CLEAN-14): the lossless form, chosen from the context rather than by model runs; the same day's numbers with censoring flags are reverted.

**Assessment (AI, 2026-11-06):** review panel (focused, re-review under LEAK-41, MET-14 to MET-16): ship after changes, made: the survey-weight note now names the measured outcome-linked selection (MET-16: weighting by `VCF0009z` lowers the share who say they voted in 8 of the 9 test years, by 2 to 9 points; scored unweighted, weighting the AUC moves it by +0.004 to +0.005); disputed: none; for the curator: no issue (optional follow-up: quote the codebook's `VCF0009z` entry, EV-2).

**Assessment (AI, 2026-11-06):** priority 3 (selection.md, Priority): a good shape (48,587 units, 261 features, temporal) +, a strong source (the ANES cumulative file and its codebook) +; no gap in the benchmark; the use case is the curation's (a pollster's likely-voter screen), so it does not count; no open issue.

CC (2026-11-08, Lennart): the declared metric (`roc_auc`) is checked, as declared; the record ships, with no open issue on the PR #47 review board.

CC (2026-11-11, Lennart): REVIEW issue 1 (which election years to test), as implemented (A): the nine studies 1996 to 2024 stay the test windows, in place of the AI's proposal of the five elections 2008 to 2024; SPLIT-14 as amended on 2026-11-11 admits the four oldest, which train on 49.2%, 46.4%, 43.2% and 40.0% of the respondents (four windows under half, not more than the five at or above it), and nine is the count a random split of this size gets.

CC (2026-11-11, Lennart): the declared horizon (one study, no gap, windows starting 2024, 2020, 2016, 2012, 2008, 2004, 2002, 2000 and 1996) is checked, as a pollster builds a likely-voter screen from the elections already studied and applies it at the next one, so each window is one election and its model up to four years old.

**Assessment (AI, 2026-11-11):** applied in dataset.py: `temporal` unchanged (`window=1, unit="unique", n_windows=9`); test 4,954, 7,442, 3,648, 5,488, 2,102, 1,066, 1,344, 1,554 and 1,534 respondents (2024 to 1996, 29,132 in all), train 43,633, 36,191, 32,543, 27,055, 24,953, 23,887, 22,543, 20,989 and 19,455 (89.8%, 74.5%, 67.0%, 55.7%, 51.4%, 49.2%, 46.4%, 43.2%, 40.0% of 48,587). `task_summary.split` and `splits_comment` now name the nine windows, the four under half with their shares, the length's reason (one election, the test Pew's likely-voter study names; no source sets a length) and why no gap is needed. `dataset check`: 0 errors, 0 warnings (README not regenerated).

CC (2026-11-11, Lennart): accepted `splits_feature_missing_in_test` with a note naming the columns (cross-dataset item "Accept splits_feature_missing_in_test where a column starts or stops being recorded within the history?", A: the data as the deployed model met it).

**Assessment (AI, 2026-11-11):** 95 questions flagged, each missing in at least one test election and recorded on its train side (e.g. VCF0401-VCF0411 last asked in 2004).

## Review

**Outcome:** added. The AI recommends shipping it: the focused re-review of 2026-11-06 under the new rules on exposure
and weights (LEAK-41, MET-14 to MET-16) leaves nothing for the curator to decide, and its one change, a sentence in
the survey-weight note, is made. The data is the ANES Time Series Cumulative Data File (February 5, 2026 version):
48,587 respondents who completed both the pre-election and the post-election interview, 1948-2024. The target is
whether the respondent says after the election that they voted (78% say so), predicted from the year and the
pre-election answers. Each of the last nine studies (1996 to 2024) is the test data once, with every earlier study for
training, and the score is ROC AUC (our default for a binary task when the source sets no score, in place of TableShift's accuracy; Lennart's call of 2026-10-21).
On 2026-11-11 you kept the nine test studies, 1996 to 2024, one election each without a gap (issue 1 and the horizon,
A), which the amended floor admits with the four oldest training on 40.0% to 49.2% of the respondents.

Validity: SEL, USE-1 (fit approximate), SPLIT (temporal, 9 test years) and PROV hold as settled before; the new rules
reopen none of them. LEAK-10 and LEAK-41 hold for the weights: none of the nine survey-weight columns is a feature, and
`VCF0009z` added as one changes LightGBM's AUC by -0.0001 (SE 0.0005, 9 test years); LEAK-41 otherwise does not apply
(no denominator).

Value: TP holds: LightGBM reaches ROC AUC 0.873 against 0.5 for a constant (skill +0.745, the share of the gap from a constant to a perfect score that the model closes; task probe, 5 of the 9
splits). MET-2 holds: ROC AUC scores every test year (the smallest class is 229 "No", in 2004). MET-16 holds: scored
unweighted with no sample weight, since the use case acts on each respondent and estimates no population share.
Weighted by `VCF0009z`, the AUC moves by +0.004 for LightGBM and +0.005 for logistic regression (SE 0.003 each, 9 test
years), and the two models change order in 1 of the 9 test years (2000). MET-15 does not apply (no rate).

Quality: MET-16 asks the notes to say when sampling depends on the outcome, and the survey-weight note did not. It now
gives the measured shift: weighting lowers the share who say they voted in 8 of the 9 test years, by 2 to 9 points,
and the most interested respondents carry the lowest mean weight (0.93 against 1.11 for the least interested).
CLEAN-16 does not apply (binary target).

Weighed: unweighted scoring (the use case acts on each respondent) against a weighted AUC (a pollster screens a design-weighted sample); weighting moves the AUC by +0.004 to +0.005 and changes the order of the two models in one test year, so the default, unweighted, stands.

For the curator: no issue; the verdict defaults to ship.

Follow-up, no decision needed: the note gives the measured shift and no cause. Whether `VCF0009z` includes a
post-election nonresponse adjustment is not checked against the ANES codebook, whose page returned 403 to the claim
auditor; quoting the codebook's weight entry when the note is next edited would settle it (EV-2: a primary document
over inference).

**Main points:** Only the verdict: the re-review left no issue, so the dataset ships unless you decide otherwise; the
codebook follow-up in the outcome needs no decision. Settled on 2026-11-11: the nine studies 1996 to 2024 stay the
test windows (issue 1, A), and the declared horizon of one election without a gap is checked.

**Record judgment:** valid. The record fields agree with the definition (the record's `Website` counts as `Other`).
Before this review the record had no line on the survey weights; its Assessment line of 2026-11-06 adds one. The
better-data candidate it names (`ces_validated_turnout`, Assessment of 2026-10-31) is screened in its own record and
was outside this review.

**Horizon:**

* **Verdict:** keep the one-election windows (high confidence): a pollster builds a likely-voter screen from the
  elections already studied and applies it at the next one, so each test window is one election, scored by a model fit
  on the elections before it.
* **Length:** one study per window (`window=1, unit="unique"`, declared as one year, the election year). ANES sets no
  prediction task, and TableShift, which defined the voting task, splits by region, not by time ("the out-of-domain
  region is the region representing the southern United States", https://tableshift.org/datasets.html). Pew's
  likely-voter study, built on the 2014 midterm, names the next elections as the test of such a model: "Applying these
  models to other elections will reveal how well they can be generalized"
  (https://www.pewresearch.org/methods/2016/01/07/likely-voters-conclusion/). The studies are four years apart from
  2004 on (two years between 2000, 2002 and 2004), so a window's model is up to four years old, as a pollster's
  would be.
* **Gap:** none needed: a study's labels come from its post-election interview, held after the election and years
  before the next study's pre-election interview.
* **Time frame:** 21 studies from 1948 to 2024 (48,587 respondents): every presidential election and the 2002 midterm,
  the only midterm study whose respondents have both interviews in the file. The five elections from 2008 to 2024 keep
  half the respondents for training (2004 trains on 49.2%), as the studies from 2012 on hold 3,648 to 7,442
  respondents against 576 to 2,283 before.
* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One election (implemented) | one study per window, no gap: the five elections from 2008 to 2024 keep half the respondents for training (2004 trains on 49.2%) | 9 windows of 1,066 to 7,442 respondents (issue 1's B: 5 of 2,102 to 7,442) | a likely-voter screen built on the elections already studied is applied at the next one, the test Pew names; a model up to four years old, as a pollster's would be | no source sets a length (ANES sets no task; TableShift splits by region); five windows above the floor |
  | B | Two elections | windows of two studies (2020 with 2024, 2012 with 2016): two above the floor | 2 candidates above the floor, 9,136 and 12,396 respondents | more respondents per window | two windows, too few |
  | C | Four calendar years | one election cycle per window | 5 candidates above the floor, one study each, 2,102 to 7,442 respondents | a length in calendar years | the same windows as A from 2004 on, as the studies are four years apart |

* **Recommendation:** A: one election is the step at which a pollster applies a screen built on the elections before, as
  Pew describes; two elections leave two windows, and four calendar years give the same ones. **Decision:** A, B or C?

**Lennart (2026-11-11, ok):** As implemented (A).

**Resolved (2026-11-11, Lennart):** A, one study per window with no gap, kept: a pollster builds a likely-voter screen
from the elections already studied and applies it at the next one, the test Pew names, so each window is one election
and a model is up to four years old, as a pollster's would be. `temporal` is unchanged; `task_summary.split` and
`splits_comment` give this reason, that no source sets a length (ANES sets no task, TableShift splits by region), and
why no gap is needed (the labels come from the post-election interview, years before the next study). The record has
the horizon CC line. `dataset check`: 0 errors, 0 warnings (README not regenerated).

**Issues for Lennart:**

1. **Which election years should the test windows be?**

   * **Problem:**
     - The nine test windows are the studies of 1996 to 2024, and the four oldest (2004, 2002, 2000 and 1996) train on
       49.2%, 46.4%, 43.2% and 40.0% of the respondents, under the half every train side must keep[^av-split14].
     - Only the five presidential elections from 2008 to 2024 keep half the respondents for training, because the four
       studies from 2012 on hold 3,648 to 7,442 respondents each, against 1,066 to 2,102 in the five before them.
     - The newest window always stays and the others are chosen from the use case and statistics of the
       data[^av-split15]; with five eligible windows, fewer than the nine a task of this size gets, the question is
       whether to test all five.
   * **Background:**
     - The one exception to the floor, an older window on at least 40% of the rows when only two windows are above the
       floor and most test entities recur, does not apply: five windows are above it, and every study interviews new
       respondents.
     - 2002 is the data's only midterm study, so under B and C the test holds presidential elections only.
     - The column filter in `_clean` keeps questions by their answers in the last nine studies, a pipeline choice kept
       on 2026-10-19; B and C leave it as it is, so the columns do not change.
     - In 2008 every respondent answers questions first asked that year (sexual orientation, `VCF9279`, and two more),
       which no training row has; 2000 and 1996 have such questions too (99.7% and 96.7% of their respondents).
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. Questions asked only in some years make it large in every window,
       even the median over the features.
   * **Statistics:** from the candidate table, over all respondents.

     | Study | In | Test respondents | Said they voted, test | Train side | Train share | Largest / median PSI |
     |---|---|---|---|---|---|---|
     | 2024 | A, B, C | 4,954 | 83.1% | 77.4% | 89.8% | 12.7 / 1.06 |
     | 2020 | A, B, C | 7,442 | 86.0% | 75.6% | 74.5% | 8.6 / 1.51 |
     | 2016 | A, B, C | 3,648 | 78.5% | 75.3% | 67.0% | 10.5 / 1.49 |
     | 2012 | A, B, C | 5,488 | 79.8% | 74.3% | 55.7% | 8.9 / 1.61 |
     | 2008 | A, B, C | 2,102 | 76.3% | 74.2% | 51.4% | 18.4 / 1.38 |
     | 2004 | A, C | 1,066 | 78.5% | 74.0% | 49.2% | 9.1 / 0.95 |
     | 2002 (midterm) | A | 1,344 | 71.6% | 74.1% | 46.4% | 17.0 / 1.46 |
     | 2000 | A | 1,554 | 76.1% | 74.0% | 43.2% | 15.1 / 0.58 |
     | 1996 | A | 1,534 | 76.6% | 73.8% | 40.0% | 12.2 / 0.60 |

   * **Effect on the task:** A scores four of its nine windows with models fit on 40% to 49% of the respondents,
     mostly the studies of 1948 to 1992. B tests 23,634 respondents in the five elections from 2008, each model fit on
     at least 51.4%; it drops 5,498 respondents of 1996 to 2004 and the only midterm.
   * **Consistency:** california_house_prices_2020 moved its oldest window from 25% to 50% of the rows (2026-10-21).
     wisconsin_local_government_property_insurance_fund keeps a window on 40.6% under the exception, for members the
     fund re-rates every year (2026-11-08); ANES respondents are new in every study. No dataset has chosen windows under
     the rewritten rule yet; delivery_eta_1m's issue 1 is open.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/anes_voting_2026/dataset.py` (`temporal`,
     `splits_comment`, `task_summary.split`); the record `curation/records/anes_voting_2026.md` (no earlier call on the
     windows); the candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows anes_voting_2026
     --root datasets/_dev/tabarena-v0pt2` (10 studies, 1992 to 2024: the tool counts studies for the floor, and by
     rows 5 are eligible).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Nine studies, 1996 to 2024 (implemented) | tests every study from 1996 on | nine windows; the 2002 midterm; 29,132 test respondents | four train sides under the floor (49.2% to 40.0%) |
     | B | Five elections, 2008 to 2024 | tests 2024, 2020, 2016, 2012 and 2008 | every train side keeps at least 51.4%; every eligible election | five windows; no midterm; 23,634 test respondents |
     | C | Six elections, 2004 to 2024 | tests B's five and 2004 | one more election | the 2004 window trains on 49.2%, under the floor |

   * **Recommendation:** B: the floor is a hard rule, five studies meet it, and all five are tested since the nine a
     task of this size gets cannot be reached. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="VCF0004", splits=TemporalSplits(window=1, unit="unique",
   cutoffs=(2024, 2020, 2016, 2012, 2008)), horizon=1, horizon_unit="years", time_unit="years")`. Built with
   `window_bounds` on the definition's frame: test 4,954, 7,442, 3,648, 5,488 and 2,102 respondents, train 43,633,
   36,191, 32,543, 27,055 and 24,953 (89.8%, 74.5%, 67.0%, 55.7%, 51.4%). On C, add 2004 to the cutoffs (test 1,066,
   train 23,887, 49.2%); it departs from SPLIT-14 (Must) and needs an exception with the fact that sets it apart. Then
   rewrite `task_summary.split` ("Each of the last nine studies (1996 to 2024)") and `splits_comment`, and the
   curation notes that name "the last 9 years" as the test years; the `_clean` filter on `iloc[-9:]` stays (a column
   choice over all years, kept on 2026-10-19). Add a CC line to the record and a dated CHANGELOG entry, and run
   `dataset check` (SPLIT-14, SPLIT-15).

   [^av-split14]: **SPLIT-14** (Must): "A temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data. ... A release with two windows above the floor may add one older window that trains on at
     least 40% of the rows, when most test entities recur (the actor re-rates entities it knows) and folds by entity
     would test unseen ones."
   [^av-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... Every choice stays above SPLIT-14's floor; the length and the gap come from
     SPLIT-12; as many windows as an IID or grouped task of that size would get folds, then check that they are still
     meaningful (SPLIT-16 to SPLIT-18)."

   **Lennart (2026-11-11, ok):** As implemented (A).

   **Resolved (2026-11-11, Lennart):** A, as implemented: the nine studies 1996 to 2024 stay the test windows. SPLIT-14
   as amended on 2026-11-11 admits them: the five newest train on 51.4% to 89.8% of the respondents, and the four
   oldest, 2004, 2002, 2000 and 1996, on 49.2%, 46.4%, 43.2% and 40.0%, all above 30% and no more windows under half
   than at or above it. Nine is also the count a random split of 48,587 respondents gets (3 x 3 folds). `temporal` is
   unchanged; `task_summary.split` names the nine studies and that the four oldest train on 40% to 49%, and
   `splits_comment` names the windows, their test respondents (4,954, 7,442, 3,648, 5,488, 2,102, 1,066, 1,344, 1,554
   and 1,534) and train sides (43,633 down to 19,455), the four under half with their shares, the length's reason and
   the absent gap. The record has the decision and the horizon CC lines. `dataset check`: 0 errors, 0 warnings (README
   not regenerated).

**Review panel:** ship after changes (mediator). Tier focused, a re-review of 2026-11-06 under LEAK-41 and MET-14 to
MET-16: the claim auditor, then the mediator. Claims: 9; 6 hold, 1 refuted (the survey-weight note left out the
outcome-linked selection MET-16 asks for; fixed), 1 not reopened (the metric, settled 2026-10-21), 1 not applicable
(no weight, rate or deviance in the task); untested: what `VCF0009z` adjusts for (the follow-up in the outcome). Blind
review: not run (focused tier). Agreed: every point; disputed: none, so the file has no issue. One slip in both
reports, corrected from the auditor's per-fold results: the test year where weighting swaps LightGBM and the linear
model is 2000 (+0.0034 unweighted, -0.0018 weighted), not 2008, where LightGBM trails either way (-0.0011 and
-0.0020); the other 8 years keep their order.

<details><summary>Mediator</summary>

anes_voting_2026: mediator report, focused re-review of 2026-11-06 (MET-16 note). One panel agent, the claim auditor, so no advocate/critic dispute exists.

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL, USE-1 (approximate fit), SPLIT (temporal, 9 test years) and PROV are as settled before; today's change does not reopen them. LEAK-10/LEAK-41 hold for the weights: they are not features, and adding VCF0009z as a feature gains -0.0001 AUC (SE 0.0005). LEAK-41 is otherwise not applicable (no denominator).
Value: TP holds (best skill +0.745, LightGBM). MET-2 holds: roc_auc scores every fold (smallest class 229 "No", 2004; dummy 0.5000 on 9 of 9). MET-15 is not applicable. MET-16 holds: scored unweighted, no sample weight. The use case acts per respondent and is not a population estimate.
Quality: the MET-16 note leaves out the measured outcome-linked selection that MET-16's last clause asks the notes to name (Should). Fix: one added clause. CLEAN-16 is not applicable (binary target).
Weighed: none open.
For the curator: nothing that blocks shipping. One optional follow-up (issue 1 below).
```

**2. Changes to make now (no decision needed)**

1. **MET-16 (Should), last clause: "the notes name it when sampling depends on the outcome".** Add one clause to the survey-weight bullet in `curation_comments` in dataset.py. State only what was measured; the cause is not confirmed from the codebook. Suggested wording: "The survey weights lower the voted share in 8 of the 9 test years (for example 0.716 to 0.623 in 2002, 0.831 to 0.797 in 2024), and the most interested respondents get the lowest mean weight (0.93 against 1.11 for the least interested): the kept respondents are more often voters than the population the weights describe, on top of self-reported turnout." It changes no data, split or metric. It is the mildest remedy on the ladder (a documented note).
2. **House rule for the working copy.** Add a dated `CHANGELOG.md` entry for the edited definition. Leave the generated README stale (`build_stale: true`) until the next rebuild the curator asks for; builds happen only on the curator's ask.

**3. Issues for the curator, ranked**

There are no validity issues and no Must issues.

1. **Optional (quality, evidence): what VCF0009z adjusts for.** The ANES codebook page returned 403, so the auditor could not confirm whether the 1996-2024 weight includes the post-election nonresponse adjustment.
   - Effect: none on the data, split or metric. It affects only how the note in change 1 explains the cause. The measured fact (weights lower the voted share) does not depend on it.
   - Rule: EV-2 (a primary document over inference).
   - Decision: whether to quote the codebook's weight entry in the note at the next edit. Doing it costs one manual download of the codebook.

**Considered and not raised:**
- **Weighted scoring as an alternative.** The auditor calls a weighted AUC "defensible", since a pollster applies the likely-voter screen to a design-weighted sample. MET-16 (Should) defaults to unweighted unless the use case is a population estimate. This use case scores each respondent, and no fact sets the case apart, so the default stands. The measurement also shows the choice changes nothing material:
  - weighted minus unweighted AUC is +0.0043 for LightGBM (SE 0.0029) and +0.0051 for the linear model (SE 0.0029);
  - the LightGBM-over-linear gap is +0.0076 unweighted and +0.0067 weighted, with the same sign on 8 of 9 folds (2008 flips, by -0.001 to -0.002).
- **Training with the weight** lowers unweighted AUC by 0.0027 (SE 0.0011), which is a further reason not to declare one. MET-15 bars it anyway: a sample weight is always the metric's row weight.

**4. Disputed points**

None. A focused tier has one agent, and nothing in its report conflicts with another rule:
- C1 to C4 and C6 to C9 hold or do not apply.
- C5 is an independent Should omission, not a conflict. It is fixed by change 1.
- C7 (the metric: fallback roc_auc instead of TableShift's accuracy) was settled by the curator on 2026-10-21 (CC line) and is not reopened.

**5. Agreed facts**

All are measured by the claim auditor. I recomputed the fold numbers from exp_results.csv and they match.
- **Definition loads and traces to the raw data.** Lineage traces 48,587 of 48,587 rows, with target match 1.0 against the raw CSV.
- **Features.** 0 of the 9 weight columns (VCF0009x to VCF0011z) are among the 261 features. The only VCF00xx column left is VCF0004, the year (`time_on`).
- **Metric and weights.** roc_auc with no inputs; `scoring_columns=[]`; `sample_weight` is None.
- **The weights.** VCF0009z = VCF0010z = VCF0011z exactly in 1996-2024; x and y are blank in 2020 and 2024.
- **Weight as a feature:** gain -0.0001 (SE 0.0005). The weight alone scores AUC 0.44 (0.34 to 0.52 per fold).
- **Weighted against raw voted share:** lower in 8 of 9 test years, by 2 to 9 points; 2008 is the exception (0.763 to 0.776).
- **Mean weight by campaign interest:** 1.108 for not much interested, 1.025 for somewhat, 0.925 for very much.
- **Attrition within a year cannot be seen in the file.** The cumulative file keeps pre-only cases only in years without a post wave.
- **Folds.** Test sizes are 1,066 to 7,442. 0.0% of 29,132 test rows have an exact feature copy in train (leak probe).

**6. Consistency with precedent**

- MET-16's only Cases row is this dataset ("its nine survey-weight columns dropped from the features"). The recommendation matches it.
- No other v2 definition in the working copy ships a survey weight, so there is no precedent to depart from.
- Several screened records mention survey or design weights: nsduh_mental_health_treatment, nhanes_liver_elastography_fibrosis, nhanes_bmi_from_habits, knhanes_undiagnosed_diabetes, recs_2020_household_electricity, cbecs_2018_building_energy_use, statssa_gpsjs_crime_victimisation, global_findex_2025 and hsls09_postsecondary_enrollment. When they are added, treat them alike: the weights stay out of the features and scoring is unweighted unless the use case is a population estimate. Where the weights shift the outcome share, the notes say so, as in change 1.
- The record also names a better-data candidate (`ces_validated_turnout`, Assessment 2026-10-31). That is outside today's scope and does not affect this verdict.

</details>

<details><summary>Claim audit</summary>

anes_voting_2026 - claim auditor, focused re-review (2026-11-06; MET-16 note; LEAK-41, MET-14 to MET-16, CLEAN-16)

Verdict: the MET-16 note holds on the data, with one omission. The survey weights are not features, carry no
post-election signal, and do not change how models rank. The omission: the note does not say that the weights
shift the sample towards non-voters, which MET-16 asks the notes to name. Nothing is refuted at Must level. LEAK-41,
MET-14, MET-15 and CLEAN-16 do not apply: no weight, no rate, no deviance, binary target.

The definition was loaded through process(lineage=True): rows traced "by the column", 48,587 of 48,587, target match
1.0 against the raw CSV. VCF0009z was joined to each row through that lineage.

**Claims table**

| Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| C1 The nine survey-weight columns VCF0009x-VCF0011z leave the features | dataset.py _clean drop_cols; README notes; MET-16 Cases row | feature_columns(c), and every surviving VCF00xx column | holds | 0 of 9 weights in the 261 features; the only surviving VCF00xx column is VCF0004 (the year, time_on); VCF0012/0016/0017 and the IDs are gone too | MET-16 |
| C2 Scored unweighted, no training weight declared | README notes; MetricSpec | task_metadata, sample_weight(c), metric inputs | holds | roc_auc, inputs={}, scoring_columns=[], sample_weight None; no task_metric_weight_without_sample_weight case arises | MET-15, MET-16 |
| C3 "The task predicts each respondent's turnout, not a population estimate" (so unweighted) | README notes (MET-16 line) | per fold: ROC AUC of LightGBM and logistic regression, unweighted against weighted by VCF0009z (all 9 weights are equal in 1996-2024: z = 10z = 11z exactly; x/y are blank in 2020/2024) | holds (the choice does not change the ranking) | weighted minus unweighted AUC: LightGBM +0.0043 (SE 0.0029), linear +0.0051 (SE 0.0029); the LightGBM - linear gap is +0.0076 unweighted and +0.0067 weighted, same sign on 8 of 9 folds (2008 flips: gap -0.0011/-0.0019); weighted training lowers unweighted AUC by 0.0027 (SE 0.0011) | MET-16, MET-2 |
| C4 (implied) No feature encodes the weight; the weight carries no post-prediction information | MET-16 "never a feature"; LEAK-41/LEAK-10 | LightGBM with VCF0009z added as a feature, against without; VCF0009z alone | holds | gain -0.0001 (SE 0.0005) over 9 folds; the weight alone scores AUC 0.44 (0.34 to 0.52); no leak, and no reason to keep it as a feature | LEAK-41, LEAK-10, MET-16 |
| C5 (implied by MET-16's last sentence) The notes name it when sampling depends on the outcome | MET-16: "the notes name it when sampling depends on the outcome" | weighted against raw share of "Yes" per test year; mean weight by campaign interest (VCF0310) | refuted (omission, Should) | the weighted voted share is below the raw share in 8 of 9 test years: 1996 0.766->0.729, 2000 0.761->0.727, 2002 0.716->0.623, 2004 0.785->0.766, 2012 0.798->0.778, 2016 0.785->0.761, 2020 0.860->0.842, 2024 0.831->0.797 (2008 0.763->0.776). The mean weight falls with interest: 1.108 for not much interested, 1.025 somewhat, 0.925 very much interested (1996-2024). So the design and its response adjustment down-weight likely voters. The kept rows over-represent voters beyond the 78% self-report, and the notes do not say so. Attrition within a year cannot be seen in the file: post-interview completion is 1.000 by interest in every test year, because the CDF keeps the pre-only cases only in years with no post wave (pooled 0.914/0.947/0.979 for 1996-2024 comes from the 1998-type years). | MET-16 (Should), USE-fit note |
| C6 Metric fallback roc_auc computable on every fold | MetricSpec; MET-2 | scorer(c) on a constant prior per fold; class counts per test fold | holds | the dummy scores 0.5000 on 9 of 9 folds; scorer = sklearn AUC to 1e-12 for LightGBM; smallest class in a test fold: 229 "No" (2004); test n 1,066 to 7,442 | MET-2 |
| C7 Metric reason (TableShift scores accuracy as a house convention; ANES defines no task) | MetricSpec reason; record CC 2026-10-21 | settled 2026-10-21 by the curator; today's change does not touch it; MET-16 bears on weighting only | not reopened | - | MET-1, MET-5, MET-6 |
| C8 (implied) No row is a copy across the split | leak probe | probe output | holds | 0.0% of 29,132 test rows have an exact feature copy in train (leak probe) | LEAK-* |
| C9 LEAK-41 / MET-14 / MET-15 / CLEAN-16 (amended) | new rules | does the task use a weight or denominator, or ship a rate or a deviance? | not applicable | binary turnout, no weight, no rate, no deviance | LEAK-41, MET-14, MET-15, CLEAN-16 |

Skim of the rest against the new rules: nothing they contradict. The use-case line ("to weight the poll towards
likely voters") describes a decision made per respondent, so unweighted scoring follows MET-16 as written. A
pollster applies the screen to a design-weighted sample, though, so the weighted AUC is a defensible alternative.
C3 shows it changes nothing material (+0.004 to +0.005 for both families, same order on 8 of 9 folds). The README is
stale (build_stale: true); that is not a finding of today's change.

**Refuted and untested, ranked**

1. C5 (Should, MET-16): the notes do not say that selection depends on the outcome. It changes no data, split or
   metric. It changes what the label stands for: the kept respondents are more often voters than the population the
   weights describe (2 to 9 points per test year), on top of self-report overreporting. Mildest remedy: add one
   clause to the MET-16 note, for example "the weights lower the voted share in 8 of the 9 test years (0.716 to
   0.623 in 2002) and give the most interested respondents the lowest weights (0.93 against 1.11): the sample and
   its response over-represent voters, so the unweighted 78% is above the population's rate". Optionally add the
   same point to the use-case-fit gap.
2. Untested: what VCF0009z adjusts for. The codebook page returned 403 (electionstudies.org
   anes_timeseries_cdf_codebook_var_20260205), and the secondary wiki is behind a bot wall. So whether 2012-2024
   VCF0009z holds the post-election nonresponse adjustment is not confirmed from the source. The data side (the
   weights lower the voted share) does not depend on it. Remedy: quote the codebook's weight entry in the note when
   it is next edited.

</details>

## Reference

@dataset{anes_timeseries_cdf_2026,
    author       = {{American National Election Studies}},
    title        = {Time Series Cumulative Data File (1948--2024)},
    year         = {2026},
    month        = feb,
    day          = {5},
    publisher    = {American National Election Studies},
    note         = {Dataset}
    }
