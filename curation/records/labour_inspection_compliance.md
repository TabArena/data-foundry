---
unique_name: labour_inspection_compliance
name: LICD_LABOR_RIGHTS
checked_by:
- Lennart
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- Free Text (Sentences)
- 'Samples: Over Time'
- 'Time: Inferred'
- 'Entities: Recur'
- 'Features: Read Later'
- Non-IID (Temporal)
collections:
- TabSTAR
original_source: Other
year: '2022'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.openml.org/search?type=data&id=46640
- https://dataverse.no/dataset.xhtml?persistentId=doi:10.18710/7U6TZP
- https://dataverse.no/dataset.xhtml;jsessionid=aa0a848e0e843de40284e7be94a9?persistentId=doi%3A10.18710%2F7U6TZP&version=&q=&fileTypeGroupFacet=&fileAccess=&fileSortField=date&tagPresort=false
notebook_path: datasets/beyond_iid/new_iid/labour_inspection_compliance/labour_inspection_compliance.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/labour_inspection_compliance/dataset.py
source_row: 659
type_adapter_id: curation-record-v1
---

## Comments

Labor Rights and Corporate Governance - LICD

Depending on the task, we might not be able to use the free text feature as it is leaking or the target.

Has two targets, need to find original data source; many missing values among some columns.

"The first case is selecting a relevant labour inspection checklist for
a given organization. The second case is to predict whether an organization is non-compliant to
working environment regulations, where selected checklists can be used as independent features"

Either many-class classification problem (for checklist ID) or compliance prediction problem (binary). Either case, the text cannot be used as it is leaking the label.

You are allowed to use it: "The Non-compliance Classification Problem (NCP): Given a checklist y and a target organisation x, classify the target organisation's compliance l to any of the regulations given by the content
of y. The value of l is unknown until the completion of the inspection and belongs to a Bernoulli
distribution where l = 1 means that the target organisation is non-compliant and l = 0 means that
the organisation is compliant." from https://papers.nips.cc/paper_files/paper/2022/file/93e4d161bdd93d1dc0202b4044159edb-Paper-Datasets_and_Benchmarks.pdf

Data is missing timestamps, so it is a forced IID task

**Assessment (AI, 2026-10-14):** The Dataverse description and 00Readme.txt (https://doi.org/10.18710/7U6TZP) say the 63,634 inspections were conducted between 2012-01-01 and 2019-06-01 (timePeriodCovered gives the same). LICD.csv has no date column ('Business Age' is the organisation's age in months), so the range cannot be checked from the data. The definition's note said 'from 2021 to 2019'; it now says January 2012 to June 2019.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source precision_at_k k_fraction=0.5 — precision at the median prediction score (with balanced accuracy, accuracy, recall and AUC) (Flogard & Mengshoel 2022, NeurIPS Datasets and Benchmarks, Sec. 6.4-6.5).

CC (2026-10-21, Lennart): the metric is precision_at_k with k_fraction 0.5, precision at the median score as Flogard & Mengshoel 2022 report it.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `osha_inspection_violations` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-11, Andrej): the three Review issues, settled on the marks of 2026-11-11, applied to this branch, whose definition was the random-split one from before them. Issue 1 (discuss, reply A): all 63,634 rows stay; a curation bullet names the 497 exact copies and the 179 feature copies with the other outcome, and what the file order costs. Issue 2 (change, "Why do we need c if b is the real temporal order? we want it to be realistic, so pick the most realistic one"): b, the export's own row order: `file_row` is the time column, three windows of 10,605 rows walking back from the end, each trained on every earlier row (50%, 67%, 83%), no gap; `ForcedIIDFromTemporal` leaves `data_tags`, and the record takes `required_split` `Temporal (NON-IID)` with the tag `Non-IID (Temporal)`. Issue 3, B: the account figures stay, with a bullet saying they are one set per organisation of an unknown year and what they add. On this branch the newer framework's `dataset_sequential_id_column` check flags `file_row`, which cannot be dropped (it is the time key), so it is an accepted warning with its reason. `dataset check`: 0 errors, 1 warning (the three constant columns, as before).

## Review

**Outcome:** added. The 63,634 inspections of Norwegian organisations by the Norwegian Labour Inspection Authority,
January 2012 to June 2019, each with one checklist (LICD; Flogard EL, Mengshoel OJ, "A Dataset for Efforts Towards
Achieving the Sustainable Development Goal of Safe Working Environments", Advances in Neural Information Processing
Systems 35, Datasets and Benchmarks Track, 2022,
https://papers.nips.cc/paper_files/paper/2022/hash/93e4d161bdd93d1dc0202b4044159edb-Abstract-Datasets_and_Benchmarks.html;
data https://doi.org/10.18710/7U6TZP): whether the inspection finds a breach of any rule on the checklist, predicted
from the organisation's register and account figures and the checklist's text, the source's non-compliance task. The AI
recommends shipping it after one small change (issue 1). Reviewed on 2026-11-04 without a review panel, from the
gathered evidence (the record, the hidden-group probe calibration of 2026-10-12, the paper; no model run exists
for it). Validity: the features are known before the inspection: the authority saves "information snapshots" of each
organisation "at the time of the inspection, so that inspection records are unaffected by any updates to the
organisations' registered information" (paper, Sec. 4); the checklist is chosen before the visit. The release has no
dates, so the split is a forced random one (approximate fit). Organisations inspected again recur across that split, and
the hidden-group probe measured what that is worth: 52% of the rows sit in clusters of near-identical rows, and a random
split gains 0.019 over a split by them (5.9% of the skill), below the line that requires a group split. Value: the
source's metric, precision among the half of the test fold scored highest (settled 2026-10-21), on a 74% breach rate.
Quality: 497 rows repeat another row in every column (issue 1); three account columns are constant. Weighed: the
authority's own data and task, documented in a paper +, features frozen at the inspection +, no dates and several
hundred account figures with names only -; a sibling (`osha_inspection_violations`, US inspections) is screened in its
own record.

**Main points:** All three issues resolved 2026-11-11: the 497 exact copies stay with a note (issue 1 A), windows
of file order (issue 2 b), account figures kept with a note (issue 3 B). Nothing open.

**Record judgment:** valid. The authority's targeting task on its own records; windows of the file's coarse time order stand
in for the dates the release lacks (issue 2). The three constant columns (`Credit losses on certificates, bonds and other
interest-bearing securities`, `Holdings of own shares/equity certificates`, `Extraordinary costs`) survive the
definition's five-value threshold with one distinct value; dropping them needs no decision.

**Issues for Andrej:**

1. **Drop the 497 rows that repeat another row exactly?**

   * **Problem:**
     - 497 rows (0.8%) equal another row in every column, the outcome included, and 179 rows (0.3%) equal another row
       in every feature but carry the other outcome.
     - With some 370 register and account columns an exact repeat is either one organisation inspected again with the
       same checklist before its register snapshot changed, or one inspection entered twice, and the release has no
       date or case number to tell them apart.
     - Drop the exact copies, keep everything, or drop the conflicting rows too?
   * **Background:** the release keeps one snapshot of the organisation's registered information per inspection
     (paper, Sec. 4), so a follow-up inspection within the same accounting year repeats every figure; a follow-up that
     finds a breach fixed, or a new one, gives the same features with the other outcome. Exact copies with one label
     are usually dropped rather than grouped[^1a], rows with both labels are dropped unless the ambiguity is part of the
     task[^1b], and a random split forced on undated data ships only when no row shares its outcome with the other
     side[^1c].
   * **Effect on the task:** an exact copy across the split hands a test row its own outcome, for about 0.8% of the
     test rows; the conflicting pairs are the real uncertainty of a re-inspection. The wider recurrence of
     organisations (52% of the rows in near-identical clusters) is measured above and stays below the line for a group
     split.
   * **Unknown:** whether the copies are re-inspections or double entries; the authority's case numbers or dates would
     settle it, and the release has neither.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows (implemented) | 63,634 rows; a note names the repeats as likely re-inspections | keeps every recorded inspection | 497 rows can find their own outcome on the other side of a forced random split |
     | B | Drop the exact copies | one row of each exact copy stays (63,137 rows); the 179 conflicting rows stay, with a note | no row shares its outcome across the split; the re-inspection that changed the outcome stays | a real re-inspection that repeated its outcome counts once |
     | C | Drop the copies and the conflicting rows | as B, and every row of a feature vector with both outcomes goes | no ambiguous feature vector left | drops genuine follow-ups, the part of the task the authority cannot know in advance |

   * **Recommendation:** B: the copies are the one measured way a row's outcome crosses the split, and dropping them
     costs 0.8% of the rows. **Decision:** keep all (A), drop the exact copies (B), or drop the conflicting rows too
     (C)?

   **Notes for the AI:** on B, in `_clean` after the column drops: `df = df.drop_duplicates()` (all columns, the
   target included) and a curation note with the count; re-run `dataset check` and confirm
   `dataset_duplicate_rows` is gone and `dataset_conflicting_duplicate_rows` still lists the 179 rows (accept it with
   the re-inspection reason). Drop the three constant columns in the same edit.

   [^1a]: **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped on the duplicate key.
     **LEAK-18** (Should): many degrees of freedom and an exact match point to a collection artefact (drop it and give
     the share); few features and plausible repeats are natural and stay with a note. **LEAK-16** (Must): duplicate
     rows need a decision every time.
   [^1b]: **LEAK-20** (Should): feature vectors that occur with both labels are dropped, every copy, unless they are
     genuine label ambiguity the task has.
   [^1c]: **SPLIT-8** (Must): a split forced on data without the windows a temporal task needs ships only when a leak
     test across the split finds none: no row shares its outcome, its unit's outcome or its period's outcome with the
     other side.

   **Answer (AI, 2026-11-06):**

   * **Verdict under the new entity-leakage rules: entity fix, the copies go down to one row (B).** A copy repeats
     the organisation, its business age in months and the checklist, so it is one checklist of one visit recorded
     twice, which the rules cut to one row[^1d].
     - Only 6.4% of the 497 copies sit in a visit with another checklist: mostly the copy and its original are the
       whole visit.
     - A copy lies a median 61 rows from the previous one in the file (88 adjacent, 271 within 100 rows, 28 more than
       10,000 apart), closer than two checklists of one visit (median 1,211 rows): mostly entered together.
   * **What the drop does to the target:** the 497 copies found a breach in 57.7% (287), against 74.3% of all rows.
     The drop takes 0.6% of the breach rows and 1.3% of the others, and the breach share moves from 74.28% to 74.41%.
   * **Does the target still stand for the use case?** We read yes: every recorded checklist outcome stays once, and
     the share moves by 0.1 point.
   * **The 179 conflicting rows stay under B:** the same checklist at the same visit with the other outcome; issue 2's
     answer keeps each visit on one side of a window.
   * **Recommendation stays B.**

   [^1d]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; in an entity fix, copies of one record (entered twice,
     listed again, read again) go down to one row per unit, and every drop gives the share dropped and the label
     shares before and after and asks whether the target still stands for the use case. **LEAK-19** (Should): when
     copies are uneven by class, the notes give the share per class and the class balance after the drop.

   **Andrej (2026-11-11, discuss):** Does this still matter with temporal splits?

   **Answer (AI, 2026-11-11):**

   * **Much less: under the windows of file order (issue 2 b), 3 to 11 test rows per window find their exact copy in
     training, against about 225 per fold on random folds.** A copy lies a median 61 rows from its original, so both
     mostly land on one side of a window's start.

     | Split (all 63,634 rows kept) | Test rows with an exact copy in training | Same features, other outcome in training |
     |---|---|---|
     | Window 0 (newest) | 9 (0.08%) | 4 (0.04%) |
     | Window 1 | 11 (0.10%) | 8 (0.08%) |
     | Window 2 | 3 (0.03%) | 1 (0.01%) |
     | Random 3 x 3 folds, mean | 1.06% | 0.40% |

   * What remains under the windows: each copy counts twice in training and, inside a test window, twice in the
     score.
   * The copies are uneven by class (57.7% breach against 74.3% overall), so the double count tilts the class balance
     a little.
   * The entity rule (one checklist of one visit recorded twice goes down to one row) does not depend on the
     split[^1d].
   * Dropping them costs 0.8% of the rows; the window shrinks from 10,605 to 10,522 rows.
   * Script: `~/claude_jobs/marks_1111/labour_inspection_compliance/dup_windows.py`.
   * **Options:**

     | | Option | Pro | Con |
     |---|---|---|---|
     | A | Keep all rows (implemented) | no change; the leak across the split is almost gone | 497 checklists counted twice, more of them without a breach |
     | B | Drop the exact copies | one row per recorded checklist, as the entity rule asks | 0.8% of the rows |

   * **Recommendation:** B, for the double count, no longer for the leak; the stakes are small.
     **Decision:** keep all rows (A) or drop the exact copies (B)?

   **Andrej (2026-11-11, discuss):** Reply (A): Keep all rows

   **Resolved (2026-11-11, Andrej):** A: all 63,634 rows stay; a curation bullet names the 497 exact copies and the
   179 conflicting rows, the double count in training and test windows, and the copies' class balance (57.7% breach
   against 74.3%; 74.28% against 74.41% if dropped); a CC line in the record. The window stays 10,605 rows.
   `dataset check` (Slurm job 1378123): 0 errors, 1 warning (the three constant columns, as before).

2. **Split by time, or keep the random split with no time-basis tag?**

   * **Problem:**
     - The release has no dates, but the raw file is in a coarse time order: among inspections of one organisation (identical register and account fields, 55,481 pairs), the later row in the file has the higher business age in 92% of pairs more than 40,000 rows apart, 71% at 20,000 to 30,000 and at most half within 10,000 rows.
     - The checklists confirm it: of the 228 used 30 times or more, 67 stop before the last four tenths of the file and 50 first appear after its first three tenths, and the breach rate falls from 79.8% in the first tenth to 72.5% in the last.
     - How the data was collected is information for the split, and here an authority targets future inspections while the windows cost precision: split in windows of file order, or keep random inspections with no time-basis tag[^2a]?
   * **Background:** the definition calls the split forced, as the data has no dates; the forced tag stands for a forward use case with no usable time or too few periods, and this file gives three windows with every training side at half the rows or more[^2b]. The order resolves time only at about 10,000 rows (about 14 months of the 7.5 years), so the windows are a sixth of the rows each rather than nine narrower ones. An inspection's result is known when it ends, so no gap is needed.
   * **Experiments:** the definition's rows and features, untuned LightGBM and logistic regression (LR), the source's metric (precision among the half of the test rows scored highest), ROC AUC beside it; three windows of 10,605 rows back from the end of the file, each trained on every earlier row (50%, 67% and 83%):

     | Split | LightGBM precision (ROC AUC) | LR precision (ROC AUC) | Breach rate in test |
     |---|---|---|---|
     | A, random 3 x 3 folds (implemented) | 0.897 (0.778) | 0.886 (0.760) | 74.3% |
     | B, newest window | 0.884 (0.770) | 0.878 (0.762) | 72.4% |
     | B, three windows, mean | 0.880 (0.761) | 0.875 (0.751) | 72.3% to 72.9% (training 74.7% to 76.0%) |

     - On the same test rows of the two older windows, training on as many rows drawn at random from the whole file scores 0.888 and 0.886 against 0.884 and 0.871 (LightGBM; ROC AUC 0.774 and 0.780 against 0.765 and 0.750): rows close in the file, such as the other checklists of one visit, inform each other across a random split.
     - Nine windows of 3,535 rows give the same: LightGBM 0.881 on average against 0.888 for random training on the same rows. The file row as a feature changes nothing (0.880).
   * **Unknown:** how the authority ordered the export (by case number, by year blocks); the authors (Flogard and Mengshoel) or the authority could say, and dates would turn the coarse order into calendar windows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random inspections (implemented), no time-basis tag | stratified random 3 x 3 folds; the forced tag dropped, as three valid windows exist, and no use-case prototype in its place (`StationaryRelation` is not shown: the windows cost 0.013 precision on the newest) | the source's evaluation; the most rows per fold | 0.013 precision above the newest window; rows of one visit on both sides; a recovered order left unused |
     | B | Windows of file order | `file_row` (the raw row number) kept as the time column; 3 windows of a sixth of the rows back from the end | later inspections tested on earlier ones, as the authority targets them; one visit's rows mostly on one side | the order is coarse: rows within about 10,000 of each other are not ordered, so the test is later on average, not row by row |

   * **Recommendation:** B: the file carries the time the use case needs, coarse as it is, and the windows also keep most rows of one visit together. **Decision:** windows of file order (B), or random inspections with no time-basis tag (A)?

   **Notes for the AI:** on B, in `_load_raw` or first in `_clean`: `df["file_row"] = range(len(df))` before any row is dropped (issue 1's copies, the two rows without the VAT flag); `temporal = Temporal(on="file_row", splits=TemporalSplits(window=10605, unit="rows", n_windows=3))`, the window a sixth of the rows after issue 1 (10,522 if the 497 copies go); drop `ForcedIIDFromTemporal` from `data_tags`; `splits_comment`: the order is the export's, coarse (the evidence above), windows of a sixth so that each spans more than the order's resolution, no gap; task summary `split` and `fit_reason` (the split can now keep later inspections for testing); replace the curation note "Without the inspection dates, we must treat the task as IID."; record `required_split` `Temporal (NON-IID)`, tag `Non-IID (Temporal)`; `dataset check`, rebuild. On A: `data_tags = ("Spatial",)` (the forced tag dropped, as three valid windows exist; no time-basis tag in its place; no date column, so no `meta_time_present_unused` to accept) and the curation note "- Time order: the raw file is in a coarse time order (organisations' business age rises along it in 92% of same-organisation pairs more than 40,000 rows apart; checklists retire and appear along it); the split leaves it unused: the newest of three windows of a sixth of the rows scores precision at half 0.884 against 0.897 on random folds (untuned LightGBM; logistic regression 0.878 against 0.886)", followed by the reason of your decision. Under either option the record gets the tags `Samples: Over Time` and `Time: Dated`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection facts and, where one fits, the definition's use-case prototype with its `Time basis:` line. **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it.
   [^2b]: **SPLIT-8** (Must, reworded 2026-11-05 and 2026-11-06): the forced tags cover a forward use case whose release has no usable time or too few periods for the windows **SPLIT-14** (Must) asks for (at least 3, none trained on less than half of the data). **SPLIT-15** (Should): as many windows as an IID task of that size gets folds, then check that the windows are still meaningful.

   **Answer (AI, 2026-11-06):**

   * **Verdict under the new entity-leakage rules: temporal fix for the re-inspections, with an entity part for the
     checklists of one visit.** The release records no organisation, but one can be rebuilt, and the authority meets
     organisations again, so the split holds out later inspections (B); the checklists of one visit are filled in
     together, so a visit also belongs on one side of a window's start[^2c].
   * **Is the link real?** An organisation is an identical register and 365 account figures, the county included, on
     the 78% of rows with accounts; a visit is an organisation at one business age (in months).
     - Rows that share all their account figures (a median of 53 non-zero values) share the county in 76.6% of 25,035
       pairs and county and industry code in 73.7%, against 11.2% and 0.9% for random pairs: the figures single out
       one organisation.
     - 43.8% of rows belong to an organisation with 2 or more rows (9,190 organisations); 5.5% share a visit.
   * **Does the label travel?** The breach share when the linked row found a breach against when it did not, beside
     the same for a row of another organisation with the same industry code, county and size band (the profile they
     share)[^2d]:
     - another checklist of the same visit: 70.7% against 57.6%, a gap of 13 points (1,636 rows in 735 visits),
       against 7 points for the profile;
     - another visit of the same organisation: 71.9% against 60.6%, 11 points (27,326 rows), against 7 points.
     - The earlier 73.4% against 42.3% within a visit counted repeats of one checklist (issue 1's copies and
       conflicting rows); past the profile, a visit carries about 6 points and a re-inspection about 5.
   * **Is there an order?** Business age orders an organisation's inspections exactly, and the file order resolves
     time to about 10,000 rows. The checklists of one visit lie a median 1,211 rows apart in the file, inside that
     resolution, so a window's start can cut a visit.
   * **Under B's windows** (after issue 1's drop, newest window first):
     - 43.4%, 38.0% and 29.9% of test rows have an earlier inspection of their organisation in training: what the
       authority knows when it targets, which the temporal fix keeps.
     - 1.0%, 1.0% and 0.3% of test rows (108, 106 and 32) have another row of their visit in training, from 90, 96 and
       31 visits cut by a window's start: 70, 59 and 25 through another checklist, the rest through the same
       checklist with the other outcome. Random folds: 4.0% (all rows).
   * **Keeping each visit whole:** each row takes its visit's first file row as its time, and the windows are cut
     between times. 1,610 rows (2.5%) move, by a median 645 rows, well inside the order's resolution; the test windows
     hold 10,440 to 10,557 rows, 98.4% to 99.8% of them those of B, and no test row has a row of its visit in
     training.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random inspections (implemented), no time-basis tag | issue 2's A | the source's evaluation; the most rows per fold | 4.0% of test rows share a visit with training; re-inspections not ordered |
     | b | Windows of file order | issue 2's B: three windows of a sixth of the rows | later inspections tested on earlier ones | 0.3% to 1.0% of test rows have another row of their visit in training |
     | c | Windows with each visit kept whole | b, with each row's time set to its visit's first file row and the windows cut between visits | no visit on both sides; the test rows of b within 1.6% | a visit key rebuilt from 373 columns and the business age; the 22% of rows without accounts stay unlinked |

   * **Recommendation:** c, B with each visit kept whole (a change from B): the re-inspections need the windows, and
     the checklists of one visit carry about twice the label agreement their profile does, so they stay together at
     no cost in rows. The visit key is rebuilt from the features, which is your call; b stays
     the choice without it. **Decision:** a, b or c?

   **Notes for the AI:** on c, as issue 2's B notes (`file_row` before any drop, issue 1's copies dropped), then: the
   organisation key is a hash of every column but `Business Age`, `Number of Employees`, `Checklist Content`, the
   target and `file_row`, on rows with `TOTAL ASSETS` present (each other row its own); visit = key + `Business Age`;
   `visit_row` = the smallest `file_row` of the visit; sort by (`visit_row`, `file_row`) and reset the index;
   `temporal = Temporal(on="visit_row", splits=TemporalSplits(window=None, unit="unique", n_windows=3,
   min_train_fraction=0.5))` (windows cut between distinct times, so a visit is never split); `visit_row` replaces
   `file_row` as the time column; `splits_comment` names the visit rule and its counts. Scripts:
   `~/claude_jobs/entity_review/labour_inspection_compliance/` (`entity.py` and `entity2.py` the tests, `entity3.py`
   the windows through `temporal_window_splits`).

   [^2c]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable. A temporal fix recovers each unit's order and holds out later
     periods when the use case sees the unit again; in an entity fix, several observations of one unit, each with its
     own label (inspections among the examples), are grouped; a key or an order rebuilt from the features is the
     curator's call, case by case. **SPLIT-24** (Must): a key constructed from the data, exactly or by a calibrated
     link.
   [^2d]: **LEAK-42** (Should, draft PR #62): three tests set the verdict, not the size of a score gap: is the link
     above a chance rate that keeps the data's structure, does the label travel with it beyond what the shared
     features predict (rows with the same profile that are not linked), is there an order.

   **Andrej (2026-11-11, change):** Why do we need c if b is the real temporal order? we want it to be realistic, so
   pick the most realistic one

   **Answer (AI, 2026-11-11):**

   * b is the real order: the windows follow the export's rows as they are.
   * c was offered only to keep the checklists of one visit on one side of a window's start; it moves 2.5% of the
     rows by a median 645 rows to the visit's first row, a visit rebuilt from the features.
   * Under b, 0.3% to 1.0% of test rows have another checklist of their visit in training, which the authority would
     not have when targeting; c removed that at the cost of a rebuilt key. Small either way, within the order's
     resolution of about 10,000 rows.
   * Applied b: the order as recorded, no constructed key.

   **Resolved (2026-11-11, Andrej):** b: `file_row` (the raw row number, kept before any row is dropped) is the time
   column; three windows of 10,605 rows back from the end, each trained on every earlier row (50%, 67%, 83%), no
   gap; `ForcedIIDFromTemporal` dropped from `data_tags`; `splits_comment`, the task summary's `split`, `known` and
   `fit_reason`, and the curation note on time order replace the IID note; record `required_split`
   `Temporal (NON-IID)` with the tag `Non-IID (Temporal)` (`Samples: Over Time` and `Time: Inferred` were already
   there; `Time: Inferred`, not `Time: Dated`, since only the row order survives). The window becomes 10,522 if issue
   1 drops the copies. `dataset check` (Slurm job 1378071): 0 errors, 1 warning (the three constant columns, as
   before); test windows of 10,605 rows, training 31,819 to 53,029 rows; 377 features (`file_row` added); not rebuilt.

   **Answer (AI, 2026-11-11):** carried to the branch `review-marks-20261111`, whose definition was still the random
   one; the same `dataset check` there is 0 errors, 1 warning (the three constant columns), with one addition. That
   branch's framework runs two checks the older one did not, and one of them, `dataset_sequential_id_column`, flags
   `file_row` as a running id a model can learn. The column cannot go: it is the time key this decision rests on, and
   the framework keeps a `time_on` column in the frame (377 features, as before). It is therefore an accepted warning
   in `accepted_check_warnings`, with the reason. Whether `file_row` should also be kept out of the features is a
   question for the definition, not for this decision; it is not raised here.

3. **The account figures are one set per organisation, of an unknown year: keep them with a note, or drop them?**

   * **Problem:**
     - The account figures are not snapshots at the inspection: 8,888 organisations inspected at two or more business ages carry one identical set of 365 figures on all their inspections (33,168 rows), though their first and last inspections lie a median 35 months apart and their employee count changes in 93% of them.
     - The paper says "the register has no historical records" and gives no fiscal year, and the payroll in the accounts matches the employee count of an organisation's first inspection as well as that of its last (Spearman 0.67 and 0.65 over 5,002 organisations inspected two or more years apart), so for many inspections the figures come from another year, earlier or later[^3a].
     - Keep the account figures with a note that says so, or drop them?
   * **Background:**
     - The review's outcome reads every feature as an "information snapshot" of the organisation "at the time of the inspection" (paper, Sec. 4); that holds for business age and employees, which change between inspections, not for the accounts.
     - A later year's accounts would leak only if they moved with the inspection's result (a firm that shrinks after a breach); nothing in the release says which inspections the figures postdate, so the late cells cannot be located row by row.
     - 14,003 inspections (22%) have no accounts; 77.7% of them found a breach, against 73.3% of the others.
   * **Experiments:** the v0.2 frame (63,634 inspections, 376 features), untuned LightGBM, the source's precision among the half scored highest with ROC AUC beside it, the shipped random 3 x 3 folds with and without the 367 account columns (the 365 figures, the currency code and the accounting type); scored on all test rows and on three parts of them (Slurm job 1366162):

     | Test rows | With accounts | Without accounts |
     |---|---|---|
     | All | 0.897 (0.778) | 0.893 (0.773) |
     | Organisations inspected at one business age | 0.929 (0.767) | 0.926 (0.759) |
     | Organisations inspected at two or more, whose figures belong to another year for at least all but one inspection | 0.859 (0.771) | 0.856 (0.767) |
     | Inspections without accounts | 0.903 (0.756) | 0.906 (0.759) |

     - The accounts add 0.004 precision (0.005 ROC AUC), and no more on the inspections whose figures must come from another year (0.003) than on organisations seen once (0.004): the part that can be traced shows no gain from a year after the inspection.
   * **Effect on the task:** a model reads an organisation's accounts of some year near the inspection; as context for targeting they are what the authority could look up, but they are not dated to the inspection, which the notes should say.
   * **Consistency:** values read at a later pull are blanked where their late cells can be located (zillow_prize, melbourne_housing_market); where they cannot, they go when they may carry a gain (distribution_transformers_at_cauca_department) and stay with a note when the part that can be traced shows none (onlinenewspopularity)[^3a].
   * **Unknown:** the fiscal year of the figures; the authors (Flogard and Mengshoel) or the authority could say.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, notes as they are (implemented) | the 367 account columns stay; the notes call every feature a snapshot at the inspection | no change | the notes claim a timing the accounts do not have |
     | B | Keep with a note | a curation bullet: one set of accounts per organisation, fiscal year unknown, the payroll matching first and last inspection alike, the measured gain and its split; `fit_reason` names it | keeps the wide table and its small gain; states the timing honestly | figures of another year stay in the rows |
     | C | Drop the account figures | the 367 columns leave; the model predicts from the register, the checklist and the place | no value of an unknown year left | the task loses its wide part, the dataset's character, for 0.004 precision |

   * **Recommendation:** B: the figures cannot be dated row by row, and where they must belong to another year they add nothing extra, so the rule keeps them with a note. **Decision:** A, B or C?

   **Notes for the AI:** on B, a curation bullet "- Account figures: one set per organisation, attached to all its inspections (8,888 organisations inspected at two or more business ages carry identical figures, 33,168 rows; first and last inspection a median 35 months apart); the paper says the register keeps no history and gives no fiscal year; the payroll matches the employee count of the first inspection as well as of the last (Spearman 0.67 and 0.65). Kept: they add 0.004 precision at half (untuned LightGBM, random folds), no more where they must come from another year (0.003) than for organisations seen once (0.004)."; `fit_reason` adds that the accounts are of an unknown year; the task summary's `known` says "the organisation's accounts (one set, year not stated)". On C, drop the account columns in `_clean` and say why. `dataset check`; a `CC` line in the record. Scripts: the vintage check and the runs are in the review's checks for this dataset.

   [^3a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point; attributes looked up after the outcome are out unless the data shows they did not change. Its clause amended 2026-10-26 (Lennart): a value read at a later pull goes where its late cells can be located; where they cannot, the values go when they may carry a gain and stay with a note only when the part that can be traced shows none. **LEAK-6** (Must): measure before acting.

   **Andrej (2026-11-11, change):** Option B: Keep with a note.

   **Resolved (2026-11-11, Andrej):** B: the account figures stay; a curation bullet names them one set per
   organisation of an unknown year with the measured gain; the task summary's `known` says "the organisation's
   accounts (one set, year not stated)" and `fit_reason` names the unknown year.

## Reference

A dataset for efforts towards achieving the sustainable development goal of safe working environments
