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
collection_period: 1968-2016
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

CC (2026-11-18, Andrej): the split stays 3-fold CV over whole wells, `UnseenGroup` (Review issue 11, A; cross-dataset decision on recording changes, full-information split check): the curves a well carries change with its year (shear sonic in 0% of wells completed before 1990, 92% in the 2010s; SP and mud weight gone after 2000), a change in how features are recorded, which SPLIT-37 step 4(a) as amended today records in the notes; the newest wells are logged like the newest training wells.

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

   [^9a]: **SPLIT-37** (Should): a dataset drawn from an expanding science catalogue, a cut of a database or testing
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

11. **Split: whole wells (as now), four windows on the well's completion year, or the competition's wells?**

   * **Problem:**
     - Which curves a well carries moves with its completion year (shear sonic in 0% of wells before 1990 and 92% in the 2010s, SP and mud weight gone after 2000), which the tree's rule for catalogues counts as arrival changing what is recorded, so the tree gives windows on the entry date (B).
     - Issue 9 kept whole wells (A, 2026-11-12) on the other half of that rule, close neighbours: a forward split by release date leaves test wells as many training wells in their licence block as random wells do (62% each), and the changed curve sets were then named only as a cost of the windows, before the tree made them a reason of their own.
     - The competition's own split (C) also holds out whole wells, but ten per test set, which its organisers called too small, and no later than the training wells.
   * **Background:** Every well is dated in the national register (1968-2016) and what the loggers recorded moves with that date: shear sonic rises from 0% of wells before 1990 to 92% in the 2010s, while SP and mud weight disappear after 2000. Four expanding windows on the well year clear the rule[^split-14] with one window at 42%, so the split is temporal on the date the well entered the register, each well whole. Confidence of the blind walk: medium.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Does the use case predict for the items the catalogue adds next? (use case): yes. Evidence: The dossier's use case: after a well has been drilled and logged, or once it is released, a geologist interprets the rock type along the whole well. The well being interpreted is the one the register has just gained — the dossier's own note says the database adds wells one by one, so a new well's released neighbours are already public. The competition's framing is the same: interpret wells whose…
     - Does each item carry a final date of entry into this catalogue? (data): yes. Evidence: The file carries no date, but every well is dated in the national register. I downloaded the Sodir (NPD) FactPages wellbore table on 2026-11-17 and joined it on the well name: 116 of the 118 wells matched (the sidetracks 16/11-1 ST3 and 25/2-13 T4 did not), 1,393,694 of 1,429,694 rows dated, completion dates 1968 to 2016 (median 1991). Wells are released two years after completion, so the…
     - Does arrival change what is recorded or selected, or does the date carry waves? (measurement): yes — arrival changes what is recorded. Evidence: Which curves a well carries moves sharply with its completion year. Share of wells with a usable curve (present on more than 5% of the well's rows), by decade of completion, computed on the 98 training wells joined to their register dates: shear sonic DTS 0% in the 1960s-80s, 35% in the 1990s, 82% in the 2000s, 92% in the 2010s; ROPA 0%, 0%, 0%, 16%, 82%, 85%; PEF 0% before 1980, 68% in the…
     - Does the order give the windows the rule[^split-14] and the rule[^split-15] ask for? (data): yes. Evidence: Four expanding windows on the completion year over all 118 wells (1,429,694 rows): train <=1986 (42% of rows, 40 wells) test 1987-1992 (299,696 rows, 23 wells); train <=1992 (63%, 63 wells) test 1993-1998 (189,836 rows, 15 wells); train <=1998 (77%, 78 wells) test 1999-2008 (77,327 rows, 14 wells); train <=2008 (82%, 92 wells) test 2009-2016 (221,860 rows, 24 wells). Three of four windows train…
   * **What the blind dossier lacked, and what it changes:** My leaf disagrees with the shipped split, and the record holds a measurement I did not have. The definition ships grouped 3-fold cross-validation by `WELL` (37-41 whole wells per test fold) with time basis `UnseenGroup`, and its splits comment reports the date test I could not run: four expanding windows on the public release date against training sides of the same size on the same test wells give mean penalty 0.698 and log loss 0.811, against 0.674 and 0.802 for random wells and 0.768 and 0.924 for wells from other quadrants; 62% of the forward test wells still have a training well in their…
   * **Missing from the blind dossier:** (1) the shipped split and the release-date measurement above; (2) that the competition itself held out whole wells (98 train, 10 open test, 10 blind) and that the organisers called the blind set too small; (3) the geography numbers that make the well the right unit (median 8 km from a test well to the nearest training well, 55-76% sharing a licence block; random forest log loss 0.763 by well,…
   * **Source split:** yes, competition (FORCE 2020 machine learning contest, Bormann et al.; the repository's files and blog post): predefined files, grouped by well: 98 training wells, 10 open-test wells (logs given, labels withheld) and 10 blind wells withheld entirely; whole wells, not depth intervals. The held-out wells are… (""We held out 10 wells where we only provided the logs (test dataset) and 10 wells that were not provided at all to the contestants"; the organisers add "With hindsight we should have chosen a larger blind dataset" (blog post in the competition repository, p. 3).") https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition. Credible: yes, The unit is chosen for the use: a contestant must interpret a well it has never seen, which is what a geologist does with a newly drilled or newly released well, so whole wells are withheld rather than depth intervals sampled at random. The organisers also say what they got wrong about its size,…. Against the tree's leaf: partly, The competition holds out exactly the unit my leaf keys on, the whole well, so neither split can split a well; it does not order the held-out wells in time, so the logging-convention change I measured (shear sonic, SP, mud weight) is never tested forward, and a model may train on wells logged….
   * **Key to split on:** the well's completion year from the Sodir register (equivalently its release year, two years later), keyed on the well so that all depth samples of one well stay on one side (the order is not a column yet: the build computes it).
   * **What changes:** `dataset.py` gains the register's completion years as a helper file, a `Temporal(..., feature=False)` declaration with cutoffs 1987, 1993, 1999 and 2009 and no gap in place of `Grouping(on="WELL")`, a new `splits_comment` and `Time basis:` line; the record gets a CC line and the tree's example moves from the catalogue's 'arrival changes nothing' branch to 'Temporal · entry date'. On C instead: `dataset.py` keeps the file key from `_load_raw` (train, open test, blind) as the split key, no input, in place of `Grouping(on="WELL")`, 2 splits on one training side.
   * **Blindness:** what the walker saw of the shipped split before deciding: The type is arguable: the labels were made once, for one 2020 competition, but the wells themselves are a cut of the Norwegian offshore register, which adds released wells one by one, so I walk under the recorded type. Leaks seen: the tree's catalogue section names this dataset under its 'arrival changes nothing' branch, and an evidence table in the rules names force_2020 beside `splits_test_class_missing`, which implies a grouped or windowed split; I ignored both and measured the arrival…
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3-fold CV over whole wells (`WELL`, 118 wells, 37-41 per test fold), 1 repeat (train 931,093-973,462 rows, test 456,129-498,498), `UnseenGroup` (implemented) | No change. | Every well is tested once; test wells have drilled neighbours (median 8 km, 55-76% share a licence block), as the competition's held-out wells had. | Trains on wells completed after the test wells, so the change in which curves are logged (shear sonic, SP, mud weight) is never tested forward; a forward split by release date scored worse than random wells of the same size (mean penalty 0.698 against 0.674). |
     | B | Four expanding windows on the well's completion year, each well whole (test wells completed 1987-92: 23 wells, 299,696 rows; 1993-98: 15, 189,836; 1999-2008: 14, 77,327; 2009-16: 24, 221,860), train shares 42/63/77/82%, no gap, the year no input | `dataset.py` joins each well's completion year from the Sodir wellbore table (a raw helper file), replaces `Grouping(on="WELL")` with `Temporal(..., feature=False)` on it, puts the two undated sidetracks (16/11-1 ST3, 25/2-13 T4) in training, and replaces `UnseenGroup`; 4 splits instead of 3. | Tests later wells on earlier ones, as a model meets a newly released well logged with the tools of its time. | The measured cost over random wells is small (0.024 mean penalty); the oldest window trains on 42% (curator sign-off, the rule[^split-14]); Halite, Anhydrite and Chalk drop out of some test windows. |
     | C | The competition's files: train on the 98 training wells (1,170,511 rows), test on the 10 open-test wells (136,786 rows) and on the 10 blind wells (122,397 rows), 2 splits on one training side | `dataset.py` keeps a file key from `_load_raw` (train, open test, blind) as the split key, no input, in place of `Grouping(on="WELL")`; 2 splits instead of 3. | Matches the contest, whose unit (the whole well) was chosen for the use; scores compare with its published results. | Ten-well test sets the organisers judged too small (the open test holds no Halite); one fixed draw of wells, no later than the training wells (completion 1982-2013 and 1968-2014 against 1968-2016), so the change in logged curves is not tested either. |

   * **Recommendation:** B, because the tree's rule now counts a change in what is recorded as reason enough for windows, the curve sets change sharply with the year, and a forward split did cost something on the record's own test (0.698 against 0.674 mean penalty); this reverses issue 9, which weighed neighbours only. A stays the choice if the curator holds that a model meets new wells alongside recent wells with the same curves, as issue 9 found. **Decision:** A or B or C?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). Applying a change: the definition's split declaration, its time basis tag and line, the record's CC line; if A is kept, the tree's departure table with the reason.

   [^split-14]: **SPLIT-14** (Must): A temporal task has at least 3 windows.

   [^split-15]: **SPLIT-15** (Must): The newest window is always a test window: it is the deployment period.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Andrej (2026-11-18, discuss):** You give two decision issues for splits with different recommendations. Unify them
   and reassess.

   **Answer (AI, 2026-11-18):** one issue now, the three splits as A, B and C (the former issue 12, the competition's
   wells, is C). Reassessed, the recommendation is B.

   - The two issues answered different questions: issue 12 set only the shipped split against the competition's
     files and left wells against windows to issue 11. Side by side they read as two answers to one decision, so
     they are one issue now.
   - B is the tree's leaf: the rule for catalogues gives windows on the entry date when arrival changes what is
     recorded, and the curves a well carries change sharply with its year.
   - Against B stands issue 9 (A, 2026-11-12), decided on close neighbours alone. The changed curve sets were named
     there only as a cost of the windows; the tree has made them a reason of their own since. The release-date
     windows of issue 9 did score worse than random wells of the same size, as a change in recording would.
   - C is weaker than both: ten wells per test set, which its organisers called too small, and no later period.

     | Evidence | Value |
     |---|---|
     | Wells with shear sonic (DTS), by completion decade | 0% 1960s-80s, 35% 1990s, 82% 2000s, 92% 2010s |
     | Release-date windows against random wells, same test wells and sizes (random forest) | mean penalty 0.698 against 0.674, log loss 0.811 against 0.802 |
     | Test wells with a training well in their licence block | 62% forward, 62% random, 0% other quadrants |
     | B's windows: train share of rows | 42%, 63%, 77%, 82% (the 42% window needs your sign-off) |
     | C's test sets | 10 open-test wells (136,786 rows, no Halite), 10 blind wells (122,397 rows) |

   A stays the right choice if you hold, as issue 9 did, that a new well meets recent wells with the same curves in
   training, so the year's curve set is no shift the model faces.

   **Resolved (2026-11-18, Andrej):** A, as implemented: 3-fold CV over whole wells, `UnseenGroup`, by the cross-dataset decision on recording changes of 2026-11-18 (full-information split check, A): a change in how the features are recorded (the curves a well carries) is a fact for the notes, not a reason for windows on the entry date, as for protein_model_quality_rf_pcp; SPLIT-37 step 4(a) amended. C (the competition's wells) holds out the same unit with ten-well test sets.

## Reference

Bormann P., Aursand P., Dilib F., Dischington P., Manral S. 2020. FORCE Machine Learning Competition. https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition
