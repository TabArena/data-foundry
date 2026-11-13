---
unique_name: force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition
name: FORCE 2020 Well well log and lithofacies dataset for machine learning competition
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- Review Prio 1 (Atlas)
- 'Samples: Over Time'
- 'Time: Dated'
- Expanding Science Catalogue
collections:
- TabArena Submission
original_source: Github
year: '2020'
domain: environmental science & climate
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/tree/master
- https://zenodo.org/records/4351156
- https://github.com/TabArena/tabarena_dataset_curation/issues/2
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition/tree/master/lithology_competition
- https://docs.google.com/document/d/13XAftsBVHIm01ZN0lP56Q4hZ9hgdYR1G_6KeV2DdzOA/edit?tab=t.0
v2_path: datasets/_dev/tabarena-v0pt2/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/dataset.py
source_row: 660
type_adapter_id: curation-record-v1
---

## Comments

Data based on images or other data is made tabular. But competitions used tabular models?

Need to double-check. Also, once checked, update GitHub issue! "

"We held out 10 wells where we only provided the logs (test dataset) and 10 wells that were not provided at all to the contestants."
"10 random wells from the train data set were used in preparing a validation set. Two validation sets were made from each train set prepared. "

**Assessment (AI, 2026-10-07):** Valid; added as a task grouped by well. Each row holds wireline readings at one depth, not a vectorised image, and tree ensembles won: XGBoost first and second, random forests third (technical retrospective in the repository, p. 3-4), and all 13 finalists used tree ensembles. All 118 wells have published labels, so they are stacked and split by well; the Zenodo LAS files carry the same labels. GROUP and FORMATION are NPD's stratigraphic picks (Zenodo NPD tables, Interpreter NPD), not the label interpreters', and the competition gave them as features. Licence: CC BY 4.0 (Zenodo), original logs NLOD 2.0. Open: whether models may use the well's other depths (the winners added depth windows).

CC (2026-10-12, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `few_minority`, multiclass). Anhydrite (1,807 rows in 10 wells) and Halite (14,711 rows in 4 wells) are each missing from one of the 3 well-grouped test folds. These are not small classes: the well split leaves them out, which the definition already accepts as `splits_test_class_missing` with that reason.

**Assessment (AI, 2026-10-20):** priority 5 for the review of the added dataset: gap + (problem_type multiclass_classification), use case +, source +, shape +, no known risk. Large well-grouped multiclass task with a documented competition source and a direct use case; strong grouped-regime addition.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; open for the curator are the fit with NPD's GROUP and FORMATION (a released-well use case or an approximate fit) and the metric (TP-6). Applied: values below -900, impossible negatives, DCAL above 100 and DRHO in 36/7-3 and 31/4-10 masked; a splits comment (departure from 98 / 10 / 10, test wells have drilled neighbours); the GROUP and FORMATION note reworded (boundaries 4x enriched on lithology changes, shared post-well sources); off-scale wells and metric facts noted; stale numbers corrected; fit_reason names the mud-log gap; domain environmental science & climate in the definition. Corrections to earlier lines: 12 of 13 finalists used only tree ensembles (one also a neural network); the GROUP and FORMATION timing is a known risk. Priority 4: gap + (multiclass), use case + (the competition's own task, interpreting a well's lithology), source + (organisers' repository, Zenodo record, retrospective), shape +, risk - (GROUP and FORMATION may postdate the prediction point, issue 2).

**Assessment (AI, 2026-10-20):** correction to the earlier 2026-10-20 lines: the "no known risk" of the first one does not hold. Whether NPD's GROUP and FORMATION exist when a newly drilled well is first interpreted is open (Review issue 2), and the 2026-10-07 line's "all 13 finalists used tree ensembles" should read 12 of 13 used only tree ensembles (one team also a neural network).

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric set to `force_2020_penalty_matrix`, the competition's 12 x 12 penalty matrix over hard labels (was the default log loss). No listed metric ranks the same; the name is not registered downstream, so TabArena scores log loss until it is. Needs a rebuild to reach the container.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix (the competition's 11 x 11 penalty matrix without Basement, labels in the starter notebook's order) — the FORCE 2020 starter notebook's penalty matrix score on hard labels, renamed from force_2020_penalty_matrix; the scored metric changes from log_loss to cost_matrix (MET-4, MET-7, MET-12).

CC (2026-10-21, Lennart): use case restated as "a newly drilled or a released well" (option (a) of Review issue 2): NPD publishes its GROUP and FORMATION picks for released wells, the wells the labels were built for; both stay as features and the fit stays direct (USE-9).

CC (2026-10-21, Lennart): curves on a second scale: follow the recommendation. ROP in 25/6-2, ROPA in 34/4-10 R, SGR in 34/12-1 and 35/11-15 S and MUDWEIGHT above 100 (16/10-2 and 281 rows of 15/9-14) are masked; MUDWEIGHT's two main scales stay, as both occur on every training side. His question whether the scales can be normalised is open (Review issue 8).

CC (2026-10-21, Lennart): duplicate formation codes merged as proposed: Grid Mb., Skade Mb. and Ty Mb. become Grid Fm., Skade Fm. and Ty Fm. (CLEAN-14).

CC (2026-10-21, Lennart): Basement drop confirmed (103 rows, all in 16/4-1); recorded as a CLEAN-17 case.

**Assessment (AI, 2026-10-21):** domain set to environmental science & climate, the definition's. The LAS headers in the Zenodo zip were read (118 files): MUDWEIGHT and ROPA have no unit in any well, ROP says m/h in all 67 wells and SGR gAPI in all 14, so the headers were harmonised and do not identify a well's unit. From the data: ROPA is in ft/h in 32/2-1 and 16/10-5 (median ROP / ROPA 0.31 and 0.30, against 0.83-1.08 in 26 other wells); the 0.13-0.17 MUDWEIGHT wells fit bar/m (divided by 0.0981: per-well medians 1.34-1.77 g/cm3, against 1.08-1.80 in the g/cm3 wells); 16/7-4 (880 rows) and 25/3-1 (932 rows) hold both MUDWEIGHT scales; ROPA in 34/4-10 R is 1/87 of its ROP and SGR in 34/12-1 and 35/11-15 S is 1/5,283 and 1/3,323 of GR, no unit factor. Depth-window features under the declared penalty (random forest, 3 grouped folds, 2026-10-07 run before the masks): mean penalty 0.662 raw, 0.668 with windows (log loss 0.776 and 0.764).

CC (2026-10-21, Lennart): Depth context: declare the depth order (`Grouping(time_on="DEPTH_MD")`) and ship no window features. Second scales: convert as the AI recommends.

**Assessment (AI, 2026-10-21):** Applied. `Grouping.time_on="DEPTH_MD"` records the order inside a well (it does not change the split; the derived regime tag becomes GroupedTemporal). `_clean` converts ROP in 32/2-1 and 16/10-5 from ft/h to m/h (x 0.3048, 5,814 rows; ROPA / ROP 0.31 and 0.30 before, 1.00 and 1.00 after) and MUDWEIGHT below 0.5 from bar/m to g/cm3 (/ 0.0980665, 225,528 rows; the 28 wells' per-well medians are now 1.08-1.80 g/cm3). Correction to the review-page answer of 2026-10-21: the ft/h curve in those two wells is ROP, not ROPA (the ratio there is ROPA / ROP = 0.31). The other off-scale curves stay masked. A CLEAN-21 case row records the conversion. dataset check: 0 errors, 0 warnings. Not rebuilt.

CC (2026-10-21, Lennart): the benchmark's LightGBM default is checked on this dataset later, not now ("we dont need to check the benchmark case, we can do that later, it is fine as is for now"): untuned LightGBM with `min_child_weight` 0.001 diverged here before the impossible readings were masked (test log loss 14-15 on grouped fold 0, 0.81 with `min_child_weight=1`). Tracked in the working copy's BENCHMARK_CHANGES_TODO.md (Model defaults).

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `GROUP` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: GROUP stays unordered (regional equivalents), noted in the definition.

CC (2026-11-12, Andrej): reviewed under the rule for cuts of growing scientific catalogues. The Norwegian well database does grow and all 118 wells are datable from the national register (entry, completion and release, 115 of them released exactly two years after completion), but wells reach the public one by one on that clock rather than in waves: on four expanding windows of the release date a forward split leaves 62% of test wells a training well in their own licence block and the nearest one 10 km away, against 62% and 9.5 km for a random draw of wells and 0% and 39 km for a quadrant-disjoint draw (random forest, mean penalty 0.698, 0.674 and 0.768). The grouped split by well stands (Review issue 9, open).

CC (2026-11-12, Andrej): review page mark (issue 9, A): the grouped split by well stays. All 118 wells are dated in the national register (released two years after completion, one by one), and a split by release date held out no more than random wells of the same size (random forest mean penalty 0.698 against 0.674; quadrant-disjoint 0.768); the measurement is in the splits comment and a curation note.

CC (2026-11-12, Andrej): collection facts `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension` (Review issue 10): the national register dates all 118 wells (entry, completion and release; released 1969 to 2018). The facts describe the source and do not change with the split, which stays as it is.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of `Timeless`:
- The use case aims at groups the data does not hold, which the held-out groups of the split stand for; `UnseenGroup` (SPLIT-32, the question before the prototypes) names that, where `Timeless` named the target and "no tag" named nothing.
- The split does not change; the definition's `Time basis:` line keeps the measured evidence.

## Review

**Outcome:** added. The FORCE 2020 lithology competition's 118 Norwegian North Sea wells pooled into one frame,
1,429,591 depth samples, grouped 3-fold by well and scored with the competition's penalty matrix. Everything the
earlier review opened was settled between 2026-10-21 and 2026-11-01 and the dataset was shipped (Lennart,
2026-10-26). Reopened on 2026-11-12 under the review of how cuts of growing scientific catalogues split: the
Norwegian well database does grow as wells are drilled and released, so whether this cut should be split by when a
well entered it was never asked. The AI recommends keeping the well-grouped split.

**Main points:** Settled: the grouped split by well stays, with the release-date measurement in the notes (issue 9, A,
2026-11-12). Settled 2026-11-12: collection facts `Samples: Over Time`, `Time: Dated` (issue 10).

**Issues for Andrej:**

9. **Keep the grouped split by well, or split by when a well was released to the public?**

   * **Problem:**
     - A forward split by the release date leaves a test well the neighbourhood a random draw of wells leaves it
       (62% of test wells keep a training well in their own licence block, the nearest one 10 km away), because
       wells are released one by one two years after each is completed rather than in waves[^9a].
     - The database does grow and every well can be dated: all 118 carry an entry, completion and release date in
       the national register, 115 of them released exactly two years after completion.
     - Keep the grouped split by well, or split by the release date instead?
   * **Background:**
     - A wave here would be a drilling campaign in a licence block; the releases that follow are not a wave, because
       each well reaches the public database on its own two-year clock. The released wells span 1969 to 2018, with
       28 of the 118 released in 2010 or later.
     - The family key is spatial and was already measured for the splits comment: a random forest's log loss is
       0.763 grouped by well, 0.814 by licence block and 1.015 by quadrant, and the median distance from a test well
       to the nearest training well is 8 km.
     - The labels are not the register's: the 118 interpretations were made once, for the 2020 competition, so a
       well released in 2018 and one released in 1970 carry labels of the same vintage.
     - The rock does not change over the span, but the recording does: only the well, the depth and the gamma ray
       are guaranteed in every well, and the two mud-weight scales and the two rate-of-penetration units the
       definition converts sit in particular wells, so a split along the release order can expose a change in how
       the curves were recorded rather than a harder rock problem.
   * **Experiments:** four expanding windows on the release date (test wells from the latest releases down, each
     trained on every earlier well), against two keys on the same test wells: a family key `S`, training wells of
     the same size drawn from quadrants the test wells do not use, and a random key `R`, training wells of the same
     size drawn from the other wells. Every 5th depth sample, untuned LightGBM (200 trees) and a random forest (100
     trees), the competition's mean penalty on hard labels and multiclass log loss, three draws for `S` and `R`;
     Slurm job 1379231.

     | Scheme | Mean penalty | Log loss | Accuracy | Test wells with a training well in their licence block | Median km to the nearest training well |
     |---|---|---|---|---|---|
     | T, forward by release date | 0.698 | 0.811 | 0.738 | 62.0% | 10.1 |
     | S, quadrant-disjoint, same size | 0.768 | 0.924 | 0.721 | 0% | 38.9 |
     | R, random wells, same size | 0.674 | 0.802 | 0.746 | 61.9% | 9.5 |

     - The windows test 14, 14, 23 and 20 wells, released between January 1992 and April 2018, on training sides of
       50.0%, 62.5%, 75.0% and 87.5% of the rows.
     - The newest window cannot be compared: nothing is released after it, so its forward training side is almost
       the whole pool and the two schemes coincide (penalty 0.625 forward against 0.623 random).
     - Untuned LightGBM diverged on every scheme here, as the curator's note of 2026-10-21 records for this
       dataset, so only the random forest is read.

   * **Effect on the task:** the release order leaves a test well the neighbourhood a random draw of wells leaves it, so it holds out
     nothing the well key does not; the spatial family key is the one that holds out a neighbourhood, at a
     cost of 0.07 penalty and 0.12 log loss.
   * **Consistency:** follows the screen whose recoverable order was not the order of entry, where the family key
     was kept (`nci_aids_antiviral_screen`, 2026-11-11), and the four regulatory toxicity sets, where the testing
     programme rather than the item set the pace; it departs from the four catalogues split by entry date
     (`qsar_tid_11`, `apistox`, `superconductivity`, `sdss_17`), where the actor cannot hold the siblings that
     arrived with the test item.
   * **Sources:** the organisers' repository,
     <https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition>; the Zenodo record,
     <https://doi.org/10.5281/zenodo.4351156>; the wellbore tables of the Norwegian Offshore Directorate's
     factpages, <https://factpages.sodir.no/>.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the grouped split by well (implemented) | no change; the measurement goes in the notes | holds out a well never interpreted, which is the competition's own held-out set and the use case | it leaves the test well's block neighbours in training, which a forward split would not |
     | B | Split by the well release date | four expanding windows on the register's release date, the well grouping dropped | follows the order in which wells reach the public database | a new well's neighbours are already public, so it holds out what the interpreter has; the oldest wells carry fewer curves, so it partly tests the logging suite |
     | C | Group by licence block | whole blocks held out, the well grouping replaced | holds out a whole neighbourhood | the interpreter does have the block's released wells, and it was already weighed for the splits comment |

   * **Recommendation:** A: wells are released one by one on a fixed delay, so an interpreter meeting a new well
     already has its released neighbours, and the measurement shows the release order holding out no more than
     chance. **Decision:** A, B or C?

   **Notes for the AI:** on A, a `splits_comment` sentence with the table above beside the existing distance and
   licence-block figures, and a `curation_comments` bullet recording that all 118 wells are dated in the national
   register (entry, completion and release, the release two years after completion) and that the release order was
   measured and not taken. On B, a `released` column from the register and a temporal declaration on it, the `WELL`
   grouping dropped, and the windows checked against the floor that every training side holds at least half the rows
   and that both rare classes reach a training side.

   [^9a]: **SPLIT-34** (Should): a dataset drawn from an expanding science catalogue, a cut of a database or testing
     programme that keeps growing, can be split by the item, by its family or by when it entered the catalogue, and
     where the actor predicts for items the catalogue does not hold yet the entry date holds out what a family key
     leaves in. A catalogue that is not growing, a recoverable date that is not the date items entered, and labels
     that are not final each put a dataset outside the case, and there the family key is the one that stands for the
     use case.

   **Resolved (2026-11-12, Andrej):** A: the grouped split by well stays. `splits_comment` gives the measurement (mean
   penalty and log loss forward by release date 0.698 / 0.811, random wells 0.674 / 0.802, other quadrants 0.768 /
   0.924; 62% of forward test wells keep a block neighbour); a `curation_comments` bullet records that all 118 wells
   are dated in the national register and that the release order was measured and not taken; record CC line. Data,
   split and score unchanged; `dataset check` re-run.

10. **Collection facts: `Samples: Over Time` and `Time: Dated`, since a source dates the items?**

   * **Problem:** the record carries `Samples: No Time Dimension`, while the national register dates all 118 wells
     (entry, completion and release; released 1969 to 2018). The facts describe the source and do not change with the
     split; whether the date carries anything belongs to the measured release order (issue 9)[^10a].
   * **Change:** `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension`; the data, the split
     and the score are unchanged.

   [^10a]: **SPLIT-32** (Should): the collection facts are read from the source and do not change with the split; a
     catalogue that a parent source dates is `Samples: Over Time` with `Time: Dated` even where the date turns out to
     carry nothing, and whether it does is measured for the time basis.

   **Resolved (2026-11-12, Andrej):** applied on approval of the plan that settled the split keys of growing catalogues
   (one decision for the eighteen datasets of that review): the record's facts changed, with a CC line and `Andrej` in
   `checked_by`. No definition change.


## Reference

Bormann P., Aursand P., Dilib F., Dischington P., Manral S. 2020. FORCE Machine Learning Competition. https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition
