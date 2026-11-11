---
unique_name: houses
name: houses
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
year: '1999'
required_split:
- Random (IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=823
- http://lib.stat.cmu.edu/datasets/
notebook_path: datasets/beyond_iid/old_iid/houses/houses.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/houses/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Regression. California Housing data from 1990 likely is outdated. Also we could collect much more data if this would be a real task. In general, likely an interpretability task anyway. Also data was preprocessed in a very special way. As the data is spatial, custom split might be required? TabRepo version of the dataset almost certainly contains a leak.

Potential issue: Outdated, spatial Data, Preprocssed

Lennart: In a task like this, I think it would count as IID as spatial information are not leaking / we can assume to have/get them.

Andrej: non-iid. Currently, we do not include spatial data as non-iid. Might change that. Temporal split required but not possible (see TabRed)

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The paper is a spatial-econometrics estimation paper: it models ln(median house value) by least squares / spatial autoregression and compares fits, without a prediction metric. RMSE on the log target follows from its least-squares setup.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a house value's error matters relative to the value; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

CC (2026-11-11, Andrej): the review page's marks of 2026-11-11 applied (review issues 1 and 2).
- Issue 1 (`ok`): kept as a valuation stand-in. The census publishes the value the task predicts, so the gap stays named in the approximate fit; the data are real and the methods separate widely (RMSE on the log value 0.178 to 0.325 on the TabArena copy).
- Issue 2 ("Option B: Random, named Snapshot"): the random split is named a `Snapshot` of the 1990 census: `data_tags = ("Spatial", "Snapshot")` and a `Time basis:` bullet in the curation notes, ending with what the split cannot test (values after 1990, block groups with no known neighbours). No change to rows or splits.
- `dataset check` could not run here: the raw file is in neither checkout's warehouse and lib.stat.cmu.edu did not answer; the definition's class-level validation passes.

## Review

**Outcome:** added. California's 1990 census by block group (a census area of a few hundred homes), as Pace and Barry
published it on StatLib: median income, median house age, totals of rooms, bedrooms, people and households, and the
block group's latitude and longitude; the target is the block group's median house value on a log scale, scored by
RMSLE on the dollar value, with a random split. The 965 block groups at the census cap of $500,001 are dropped (19,675
remain). The AI recommends shipping it as defined; the one question is whether its use case carries a decision
(issue 1). Reviewed without a panel, from the gathered evidence (the record, the definition, a model run on the
TabArena v0.1 copy of the same rows). Validity: real data from a named source; the value and the features come from
the same census, so the use case is a stand-in (fit approximate, issue 1); our experiments found no leak (all rows
distinct, the table shuffled, no feature derived from the target); the capped values are gone. Value: the methods
separate widely (RMSE on the log value on the TabArena copy: LimiX-2 0.178, TabPFN-3.5 0.180, CatBoost 0.211, KNN 0.27
to 0.29, linear regression 0.325), and the best explicit model, a comparison with the nearest block groups, ranks only
6th of 94. Quality: no open point; 60% of block groups share their exact coordinates with another (block groups of
one tract), which a random split puts on both sides, as the use case allows. Weighed: real data, a classic spatial
regression, wide method separation +; the census publishes the value it predicts, 1990 data -.

**Main points:** settled on 2026-11-11: kept as a valuation stand-in (issue 1), the random split named a
`Snapshot` of the 1990 census (issue 2), record fields filled.

**Record judgment:** valid data, weak decision. The table is Pace and Barry's census extract, the surviving copy of
the California housing data (california_housing and california_housing_prices are retired as duplicates of it, which
is no precedent for this copy). The record's split debate (Andrej: spatial, so non-IID; Lennart: IID) is settled in the
definition by the use case: a block group valued while its neighbours' values are known. The record's remark that the
TabRepo copy has a leak concerns another copy; our experiments found none in these rows.

**Issues for Andrej:**

1. **Keep the 1990 census house values as a valuation task?**

   * **Problem:**
     - The target is each block group's median house value from the 1990 census, and every feature comes from the
       same census, so in practice the value is read from the census tables, not predicted.
     - The definition calls the task a stand-in for valuing areas where no value is recorded (fit approximate), and
       Pace and Barry built the table to show a fast spatial regression, not to predict[^1a].
     - Keep it as a valuation stand-in, or retire it as a table with no decision behind it?
   * **Background:** a block group is the smallest census area with these tables; its median house value is the
     median over its owner-occupied homes. The source estimated how the value depends on income, housing and place;
     the benchmark asks a model to predict it for held-out block groups whose neighbours are known. Such area-level
     valuation from census covariates is what small-area estimates and neighbourhood valuation models do where a
     survey value is missing or too noisy, which is the stand-in the definition names[^1b].
   * **Effect on the task:** with a random split, half the test block groups have a sibling of the same tract (the
     same coordinates) in training, so the task is spatial interpolation; it would not tell how well a model values a
     region with no known neighbours.
   * **Experiments:** model run on the TabArena v0.1 copy (20,640 rows, the capped ones included; 3 splits):
     no leak; the benchmark methods spread from 0.178 (LimiX-2) and 0.180 (TabPFN-3.5) over 0.211 (CatBoost) to 0.325
     (linear regression); a spatial additive model ranks 20th of 94 and a comparison with the 8 nearest block groups
     6th, so the task is close to known spatial structure without being solved by it[^1c].
   * **Consistency:** the decided house-price tables (ames_housing, house_sales, california_house_prices_2020) are
     sales with an assessor, a buyer or an agent as the actor, a direct fit; this is the only area-level one.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as a valuation stand-in (implemented) | 19,675 block groups, random split, fit approximate | real census data; the benchmark's clearest spatial regression; methods separate widely | no one predicts a value the census publishes; 1990 values |
     | B | Retire | the folder goes; the record gets `No` with `No Good Target / Scientific Discovery` | only tasks with a decision behind them stay | loses a real task with a named stand-in; the same kind of stand-in is accepted elsewhere |

   * **Recommendation:** A, keep: the gap is named in the fit, the data are real and the methods separate; a weak
     decision is a reason to prefer a sales-based task where one exists, not to retire this one. **Decision:** keep
     (A), or retire (B)?

   **Notes for the AI:** on B, set the record's `suggestion` to `No (Retired)` with the marker `No Good Target /
   Scientific Discovery`, remove the folder and clear `v2_path`; the definition stays in git history.

   [^1a]: Pace, R. K. and Barry, R., "Sparse spatial autoregressions", Statistics & Probability Letters,
     1997;33(3):291-297, https://doi.org/10.1016/S0167-7152(96)00140-X. **SEL-3** (Must): a table without a genuine
     predictive target, such as a scientific-discovery table, is out. **USE-2** (Must): a task no decision fits is out.
   [^1b]: **USE-8** (Must): an approximate fit is a stand-in with a known gap, named as such. **USE-9** (Should):
     before settling on approximate, ask whether the data mirrors another use case practitioners have.
   [^1c]: **TP-3** (Must): if tuned methods spread, keep the dataset. **TP-4** (Must): `Trivial` needs proof.

   **Resolved (2026-11-11, Andrej):** A (ok): kept as a valuation stand-in; no definition change, a `CC` line in the
   record.

   **Andrej (2026-11-11, ok):** As implemented (A).

   **Resolved (2026-11-11, Andrej):** A, confirmed on this branch: the folder and the record stay as they are
   (`suggestion: Yes`, fit approximate, the stand-in named in `fit_reason`); option B's notes, which would retire it,
   are not applied.

2. **Time basis: if kept, name the random split a `Snapshot` of the 1990 census?**

   * **Problem:**
     - Every row is a block group of the 1990 census, and the house value and every feature come from the same census tables, so all rows share one reference date.
     - The record's collection fact fits (`Samples: One Moment`, no target tag), and the random split carries no time basis.
     - Name it a `Snapshot`, as the split rules already cite it?
   * **Background:** a split that only fills in a moment the data covers is a `Snapshot`; its line names the moment,
     and no row of the same moment may carry a test row's target[^2t1]. The use case values a block group whose value
     is not recorded, at the census date, with its neighbours known; the block groups of one tract share coordinates
     and sit on both sides, which that use case allows (the `Spatial` tag). Whether the task stays at all is issue 1.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `Snapshot` | `data_tags` gain `Snapshot`; a `Time basis:` line names the census | states one census and the fill-in; the rules cite this dataset | none found |

   * **Recommendation:** B, if issue 1 keeps the dataset. **Decision:** A or B?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Spatial", "Snapshot")` and the curation bullet "-
   Time basis: Snapshot: the 1990 census of every California block group; income, housing, population, households
   and the median house value come from the same census tables; the use case values a block group whose value is not
   recorded, at the census date, with its neighbours known."; `dataset check`. The record's facts stay.

   [^2t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `Snapshot` only fills in a time the data covers (one census, one scrape); its line names the
     moment, and no row of a test row's time may carry its target, else the split groups by that time unit. Cases:
     houses and 5g_energy_consumption.

   **Resolved (2026-11-11, Andrej):** B: the `- Time basis: Snapshot: ...` bullet of the notes is in `curation_comments`
   (ending with what the split cannot test: values after 1990, block groups with no known neighbours); the `Snapshot`
   tag enters `data_tags` once PR #50 is in the working copy. No change to rows or splits, so no `dataset check`.

   **Andrej (2026-11-11, change):** Option B: Random, named Snapshot.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch, which already carries the time-basis tags:
   `data_tags = ("Spatial", "Snapshot")` and the `- Time basis: Snapshot: ...` bullet in `curation_comments`, ending
   with what the split cannot test. Rows and splits are unchanged. `dataset check` could not be run here: the raw
   file is in neither warehouse and lib.stat.cmu.edu did not answer; the definition's class-level validation, which
   holds the time-basis rule (a prototype tag needs its `Time basis:` line and no temporal split), passes.

## Reference

Pace and Barry (1997), "Sparse Spatial Autoregressions", Statistics and Probability Letters.
