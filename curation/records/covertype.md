---
unique_name: covertype
name: covertype
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Random (IID)
- 'Samples: One Moment'
collections:
- TabArena Reject
- TabSTAR
original_source: UCI
year: '1998'
domain: environmental science & climate
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/31/covertype
- https://doi.org/10.24432/C50K5N
notebook_path: datasets/beyond_iid/grouped/covertype/covertype.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/covertype/dataset.py
source_row: 691
type_adapter_id: curation-record-v1
---

## Comments

CC: ""The original study used random splits and it also makes sense to do so. In a real application one would collect samples randomly across the studied area, and afterwards try to fill the gaps to predict unseen areas to save collection time.

The real task would be rather solved using remote sensing data. Spatial data. TabRed says that task requires time split. I think otherwise the task does not make sense as the same locations might reoccur (but unsure about that); unclear if real task would have knowledge of close-by spatial domain or if it would be needed in that case; some of the features are distance to some place, if features are from the same area, this might be leaking.""

Results of re-investigation:
1) contains several areas (Rawah, Comanche Peak, Neota, Cache la Poudre), so these represent subgroups but can be IID
2) TabRed claims that a time split is needed for a real task (makes sense), but no time feature exists. Moreover, they claim the task is not real-world anymore as no GNSS data is included in the prediction task
3) Both the wilderness area and soil type are one-hot encoded categorical features.
4) It seems the OpenML version in TALENT (https://www.openml.org/d/150) comes with transformed features that are leaking the test distribution for any split
5) the data on UCI comes with incorrect column order based on the info file
6) After doing some basic EDA, we found that areas might be distinct in their characteristics, and classes only appear for some of the areas in general. So this is clearly a grouped dataset as trees heavily depend on the wilderness area.
7) Only the target was determined by image usage, the features depend on pre-determined information about the location and spatial data.

Besides missing a time feature, the data is also missing location features that would allow us to build spatial splits across all data points. Instead, we only have areas to filter, which by nature of collecting the data are also time splits.

From all the above, we conclude the following: if we use IID splits, we have either time or spatial leakage. To fix this, we need to perform some kind of spatial split. The only real non-relative spatial indicator is the area. This allows us to make the task a grouped-split with holding out one area at a time. However, some classes only exist for some areas, while others exist for many areas.
Thus, we reduce the dataset only to the classes which exist for all the three biggest areas and do grouped splits across areas.

CC (2026-10-01, Lennart): Back to IID splits on the full data (all 7 cover types, all 4 areas, 581,012 cells), as in Blackard & Dean (1999), who drew training and validation cells at random from the pooled areas. The leave-one-area-out split had only 3 groups, so it was three domain-shift tests rather than a grouped task, and it needed the frame cut to 3 cover types. IID is optimistic for land far from mapped cells: the cover maps are made of homogeneous stands of 2 to 80 ha, about 20 to 900 cells each, so a random test cell usually has cells of its stand in training; the data has no coordinates to split by.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Blackard & Dean 1999 report accuracy, but name no costs between the 7 types and two types hold 85% of the cells; log loss keeps the probabilities (MET-6, MET-8).

CC (2026-10-21, Lennart): Fallback log loss, not the paper's accuracy.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `Soil_ClimaticZone` (a partial order).

CC (2026-11-01, Lennart): marks on the review board of PR #37: Soil_ClimaticZone stays unordered (a second dimension within the altitude belts), noted in the definition.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `fia_forest_type` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Andrej): review marks applied (Review issues 1 and 2). Rows and split unchanged (581,012 cells, random).

- Issue 1 (B, "Option B: Random cells, measured."): the random cells of the source's design stay, with the look-up written down. `fit_reason` now says that cover types were mapped per stand (20 to 900 cells), that four location columns alone predict 93% of the test cells, and that LightGBM falls from 97% to 70% accuracy without them; the experiment table is in `curation_comments`. The score mostly measures interpolation between mapped cells inside the four areas.
- Issue 2 (B, "Option B: Random cells, Snapshot."): the split is named a `Snapshot` of one extract of the Forest Service's stand map and of the terrain, road and fire-point layers (date not documented, before the August 1998 donation). `data_tags = ("Spatial", "Snapshot")` and the `Time basis:` bullet is in the notes. Not tested: a later map, or land outside the four areas.
- The raw `covtype.data` was downloaded from UCI into the local warehouse, which had no copy; `dataset check` passes (0 errors, 0 warnings).

## Review

**Outcome:** added. Blackard and Dean's forest cover types (UCI, 1998, https://doi.org/10.24432/C50K5N; Computers and
Electronics in Agriculture 24(3):131-151, 1999): 581,012 cells of 30 x 30 m in four wilderness areas of the Roosevelt
National Forest, Colorado, each with its cover type from US Forest Service maps (seven types) and cartographic inputs
(elevation, slope, aspect, distances to water, road and fire ignition point, hill shade, area, soil type); random cells
as in the source (Lennart, 2026-10-01), log loss fallback (Lennart, 2026-10-21), fit approximate. The AI recommends
shipping it with the measured optimism of the random split written into `fit_reason` (issue 1). Reviewed on 2026-11-04
without a panel, from the gathered evidence (the record and the CHANGELOG; no model run exists for it) and two
checks on the v0.2 frame. Validity: a real mapping task and the source's own design, but the label is drawn per forest
stand, so cells of one stand sit on both sides of the split, and the four location columns alone predict the cover
type of 93% of the test cells by look-up (issue 1). Value: on the first shipped fold untuned LightGBM reaches log loss
0.096 against 0.630 for a logistic regression and 1.205 for the class shares, so the methods separate widely. Quality:
the one-hot blocks are reversed into named categories with their climatic and geologic zones; no issue found. Weighed:
the source's design and a real mapping question +, wide separation +, a score that is mostly spatial interpolation
between neighbouring cells -, no coordinates to split by -.

**Main points:** All settled (2026-11-10): random cells with the look-up measured (issue 1, B), named a `Snapshot` of
one map extract (issue 2, B).

**Record judgment:** valid with a known gap. The record carries Lennart's split, metric and dtype calls (CC 2026-10-01,
2026-10-21, 2026-11-01); it has not been checked by Andrej. Better data is screened: `fia_forest_type` (`TBD -> Yes`,
priority 3), forest inventory plots with locations.

**Issues for Andrej:**

1. **Keep the random split over cells, although the cells of one forest stand share their label?**

   * **Problem:**
     - The cover maps were drawn per homogeneous stand of 2 to 80 hectares (about 20 to 900 cells), so the cells of a
       stand share their label, and a random split puts cells of one stand in training and in test.
     - On the first shipped fold, a nearest-neighbour look-up on four location columns alone (elevation and the
       distances to water, road and fire ignition point, within the same area) gives the right cover type for 93.4%
       of the test cells, and 59.6% of them have a training cell within one cell's distance on those columns.
     - Keep the random split as Lennart decided, with this measurement in `fit_reason`, or retire the dataset because
       the stands cannot be recovered?
   * **Background:**
     - Blackard and Dean drew their cells at random from the pooled areas; the use case is mapping cells of the
       studied areas that have no inventory from cartographic data. The data has no coordinates, but the distances to
       fixed landmarks act as coordinates.
     - Holding out one wilderness area at a time was the definition until 2026-10-01; with three usable areas it was
       three domain-shift tests and dropped four of the seven cover types, so it was given up[^1a].
   * **Effect on the task:** the score mostly measures interpolation between mapped cells inside the four areas. A
     model used on land far from any mapped cell, or on another forest, would do much worse: without the location
     columns, LightGBM falls from 97.1% to 70.2% accuracy.
   * **Experiments:** first shipped fold (387,341 training and 193,671 test cells):

     | Model | Inputs | Log loss | Accuracy |
     |---|---|---|---|
     | class shares | none | 1.205 | |
     | nearest neighbours (log loss: 10, distance-weighted; accuracy: 1) | 4 location columns, within the area | 0.165 | 0.934 |
     | logistic regression (100,000 training cells) | all 14 | 0.630 | 0.724 |
     | LightGBM, untuned | all 14 | 0.096 | 0.971 |
     | LightGBM, untuned | the 10 without the location columns | 0.698 | 0.702 |

     - LightGBM is as accurate on test cells without a training cell within one cell's distance (0.972) as on those
       with one (0.969): a cell's stand is recognised from location values within a few cells, not only from an
       adjacent cell.
   * **Consistency:** IID over related entities can match how a task is framed even when optimistic, as for
     amazon_employee_access and bank_marketing[^1b]; covertype is the rules' case for few groups (IID instead of
     grouped). Against: an IID split is wrong when rows share an entity that carries the label, and when the groups
     cannot be recovered the dataset is retired rather than grouped on a guess (maternal_health_risk,
     hazelnut_spread_contaminant_detection)[^1c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random cells (implemented) | IID 1 x 3; `fit_reason` says random cells are optimistic, without numbers | the source's design; all 7 types and 4 areas | the size of the optimism is not stated |
     | B | Random cells, measured | as A; `fit_reason` and the notes give the look-up (93.4%) and the drop without location (97.1% to 70.2%) | the source's design, with the gap a user can read | the score stays mostly interpolation |
     | C | Retire | the folder goes, the record gets `No`; `fia_forest_type` screened as the replacement | no score that rests on recognising stands | a classic large multiclass task leaves; its replacement is not yet added |

   * **Recommendation:** B: the random cells are the source's design and Lennart's call, the use case of filling
     unmapped cells inside the studied areas is real, and the measurement tells a benchmark user what the score means.
     **Decision:** as is (A), with the measurement (B), or retire (C)?

   **Notes for the AI:** on B, `fit_reason`: "Cover types were mapped per stand (20 to 900 cells), so random cells give
   a look-up: four location columns alone predict 93% of the test cells, and without them LightGBM falls from 97% to
   70% accuracy; land far from mapped cells would score far lower." Add the table to `curation_comments`; `dataset
   check`. On C, `No (Retired)` with the reason under SPLIT-25, folder removed, CHANGELOG.

   [^1a]: splits.md, "Weighed factors": with only a few groups a grouped split is a domain-shift test between them
     rather than prediction for unseen entities (covertype: 3 wilderness areas, IID instead).
   [^1b]: **SPLIT-31** (Should): over related entities, IID can match how a task is framed even when it is
     optimistic: such a task is a candidate for a grouped or temporal variant, not a fix.
   [^1c]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have and
     the entity carries the label. **SPLIT-25** (Must): when the real groups matter and cannot be recovered, retire
     the dataset rather than group on a guess.

   **Answer (AI, 2026-11-06):** the time framing leads back to this question. The cells come from one map extract,
   and the use case fills in cells of the same areas at the map's moment, a `Snapshot` (issue 2). In a snapshot,
   time reaches a test row's label only through rows of the same moment; here every row shares the moment, and what
   carries a label to other rows is the stand, through space. So the random split fits the fill-in use inside the
   mapped areas (B), and what it cannot test is a later map or land outside the four areas, which the release has
   no rows for. The time basis adds no reason to retire (C).

   **Andrej (2026-11-11, change):** Option B: Random cells, measured.

   **Resolved (2026-11-10, Andrej):** B: random cells stay; `fit_reason` is the drafted text (93% from four location
   columns, 97% to 70% without them), and the experiment table is in `curation_comments`. Rows and split unchanged.

2. **Time basis: name the random split a `Snapshot` of one map, not `Timeless`?**

   * **Problem:**
     - Every cell's label is its stand's cover type on one Forest Service map, and its features come from terrain,
       soil, water, road and fire-point layers extracted once for the 1998 donation, so features and label describe
       one moment, whose date the source does not give.
     - The record carries `Samples: One Moment` and no time or target fact, which fits; the split is random over
       cells, tagged `Spatial`, with no time-basis tag yet; the arrival study classed the target as timeless.
     - The use case fills in cells of the studied areas that have no inventory, which the prototypes call a
       `Snapshot` (a site not yet mapped in a past survey); `Timeless` does not fit, since a stand's cover changes
       with fire, logging and succession[^2a].
   * **Background:** the release has no date, coordinates or stand id, and its row order is the authors' sampling
     order (training, validation, test blocks). Under a snapshot, the check is whether rows of a test row's moment
     carry its target; here that is the stand shared through space, issue 1. A later map of the same areas, or
     another forest, is a forward use the release cannot test.
   * **Unknown:** when the stand map, the road layer and the fire-ignition layer were made; an ignition point newer
     than the map could follow the stand's fuel (its cover type) rather than precede it. Blackard's 1998
     dissertation (Colorado State University) may give the dates; no evidence either way, so no issue of its own.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random cells, `Spatial` only (implemented) | as now | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random cells, `Snapshot` | as now; `Spatial` and `Snapshot`, with a `Time basis:` line naming the one map extract and the fill-in use | names the one moment and what the split cannot test; follows the rule's own example | the map's date is unknown, so the line names it only as before August 1998 |
     | C | Random cells, `Timeless` | as now; the study's class, a cover type as a fixed property of a site | none beyond matching the study | a cover type changes over decades; the tag would claim a later map scores the same |

   * **Recommendation:** B: one extract, a fill-in use, and a target that does change over time, only not within
     the extract. **Decision:** A, B or C?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Spatial", "Snapshot")` (the class adds `IID`), a
   curation bullet `- Time basis: Snapshot: one extract of the Forest Service's stand map of four wilderness areas
   and of terrain, road and fire-point layers (date not documented, before the August 1998 donation); the task fills
   in cells of the same areas at that moment, and cells of one stand share its label (see the notes on the random
   split).`, `splits_comment` unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; a definition can name the
     use-case prototype it follows with a `Time basis:` line. `Snapshot`: the use case only fills in a time the data
     covers (one census, one scrape, a site not yet mapped in a past survey), and the line names the moment; time can
     then affect a target only through samples of the same time. `Timeless`: the target is a fixed property of the
     item, the same whenever it is measured. **SPLIT-8** (Must): a release that is one moment is not forced; it
     gets `Snapshot` or `DelayedTarget`.

   **Andrej (2026-11-11, change):** Option B: Random cells, Snapshot.

   **Resolved (2026-11-10, Andrej):** B: the drafted `Time basis: Snapshot:` bullet is in `curation_comments` (one map
   extract before August 1998, the fill-in use), ending with what the split cannot test (a later map, land outside the
   four areas). `data_tags` stays `("Spatial",)`; `Snapshot` enters it once PR #50 is in the working copy.

   **Resolved (2026-11-11, Andrej):** carried out here: `data_tags = ("Spatial", "Snapshot")`, as this working copy has
   the time-basis tags. `dataset check`: 0 errors, 0 warnings.

## Reference

https://www.sciencedirect.com/science/article/abs/pii/S0168169999000460
