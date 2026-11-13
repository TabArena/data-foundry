---
unique_name: superconductivity
name: superconductivity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- Expanding Science Catalogue
original_source: UCI
year: '2018'
required_split:
- Grouped (NON-IID)
source_links:
- https://www.openml.org/search?type=data&id=44964
- https://doi.org/10.24432/C53P47
notebook_path: datasets/beyond_iid/old_iid/superconductivity/superconductivity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/superconductivity/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

recent and likely still useful predictive task but I am missing domain knowledge

 Talent uses UCI version. Initially, custom train/test split. Task: Predict critical temperature. Might require some special split based on molecules.Paper uses a random split 2/3 - but might be wrong. Data was preprocessed already. Moreover, there is an additional file with information about the molecules.

Potential issue: -

Lennart: No objection

Andrej: But need to check for leaks after obtaining results due to split & preprocessing.

CC (2026-10-06, Lennart): Grouped by composition (was IID). The split follows what the task does in reality: the source predicts the critical temperature from the formula alone, and a model like that is used for compositions without a measured temperature, so a test composition must be new to it. A random split gave 35% of the test rows an identical feature row in train. The key is the composition: each element's share, from the element counts in `unique_m.csv` (shipped with the release, row-aligned with `train.csv`, same temperatures), compared at 6 decimals, which only removes floating-point noise (5 to 8 decimals give the same 15,164 compositions; 4 decimals would merge 28 different ones). It joins formulas that write one composition differently (`Dy1Ir2Rh2B4` and `Dy1Rh2Ir2B4`, `V2Zr1` and `V66.6Zr33.3`), which a key on the formula string would split; no set of identical feature rows lies in two groups. 2,422 compositions have 2 to 110 entries (6,099 repeated rows); their temperatures differ by a median standard deviation of 1.3 K and by more than 30 K for 132, likely other samples, phases or pressures, which the release does not record, so one composition can hide several materials that no model on these features can tell apart. Every entry is kept and scored per row. Not grouped by element set (R^2 on log1p(Tc) 0.913 random, 0.899 by composition, 0.845 by element set): a new composition is usually another proportion of known elements, not a new family; Meredig et al. (2018) study the new-family case. Not deduplicated: Stanev et al. (2018) average a material's entries when their standard deviation is below 5 K and drop the rest (76% of our repeated compositions would be averaged); we keep the release's rows. The cost of grouping is small but real: R^2 on Tc random / grouped, 2 x 3 folds: extra trees 0.921 / 0.919, random forest 0.919 / 0.910, LightGBM 0.916 / 0.913, kNN-5 0.890 / 0.883, ridge 0.735 / 0.732. Its size did not decide: the use case did. Task probes on the build: no flags.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — out-of-sample RMSE of the critical temperature in Hamidieh 2018 (R2 reported alongside).

CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: SuperCon lists only superconductors, and all 21,263 rows have a critical temperature above 0 K (the lowest is 0.00021 K), while the use case screens candidate compositions, most of which do not superconduct. The definition's fit_reason does not name this yet.

CC (2026-10-27, Lennart): fit approximate (was direct): a screen meets mostly materials that do not superconduct, so the selection is a known gap (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `supercon_mdr_2024` (TBD -> Yes, priority 2), `systematically_verified_thermoelectric_zt` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: formula-only features with compositions held out whole and the source's RMSE; selection (only superconductors) already marked; methods spread. Priority 3: gap 1, use case 0, source 1, shape 1, risk -1.

**Assessment (AI, 2026-11-08):** one vote per unit (the scan of 2026-11-08 after boreal_postfire_lichen_biomass's issue 7): the per-row RMSE counts a composition as often as SuperCon lists it, 1 to 110 times (YBa2Cu3O7 110); the 2,422 compositions with two or more entries hold 40% of the 21,263 rows, and all 81 inputs are equal within 99.8% of them, so a model predicts per composition. Weighting each entry by 1 over its composition's entries (each composition counts once) ranks 8 untuned models at Kendall tau 0.98 per split (lowest 0.93) and 0.93 for the ranking by the mean over the 9 shipped splits, the same best model on 9 of 9. Open for Lennart as issue 1 of the record's Review; recommended: each composition counts once (B), RMSE already takes the weight.

CC (2026-11-08, Lennart): issue 1, B: each composition counts once. The RMSE weights an entry by 1 over its composition's number of SuperCon entries (`composition_weight`, a scoring column for the metric only, no training weight; the bundle warning accepted, since the composition fixes all 81 inputs), and the metric is declared from context with Hamidieh's per-entry RMSE named as the original, overruled on the unit the scientist decides on (MET-1, MET-17), as Stanev et al. (2018) count each material once. Every entry is still kept (SPLIT-26). Supersedes "Every entry is kept and scored per row" of Lennart's CC of 2026-10-06.

CC (2026-11-08, Lennart): the declared metric (rmse, weighted by composition_weight) is checked.

CC (2026-11-11, Andrej): ship as defined (issue 1): 21,263 entries, compositions held out whole, RMSE in kelvin; nothing changed. Time basis (issue 2): date the materials through SuperCon first, then decide; open, the split is unchanged.

**Assessment (AI, 2026-11-11):** dated through the NIMS SuperCon datasheet Ver.240322 (CC BY 4.0, doi:10.48505/nims.4487; reference year per entry, 1913-2023): 18,057 of the 21,263 rows (85%) match an entry by formula and Tc, 1,432 more by formula only, 1,774 (8%, 97% cuprates with variable oxygen) stay undated. The catalogue drifts: cuprates make 4,885 of 5,431 dated rows in 1987-1995, iron-based 1,574 of 3,018 after 2008; median Tc 4.4 K to 1986, 58 K 1987-95, 10.5 K 2009-19. Trained on compositions first reported up to 2008, LightGBM and extra trees score RMSE 13.2 K (R^2 0.55) on the later ones against 8.5 K (0.81) with a random training set of the same size from all eras, on the same test rows (after 2001: 14.6 K against 8.5 K). `Timeless` and `StationaryRelation` do not fit; options in Review issue 2.

CC (2026-11-11, Andrej): temporal split by the first report year (review issue 2, option a), in place of the grouped split on the composition.

- Dated through the parent database's own export, the MDR SuperCon Datasheet Ver.240322 (NIMS, doi:10.48505/nims.4487, CC BY 4.0, which asks to be cited; the definition's download notes do so), which gives every entry the publication year of its reference. A datasheet entry belongs to a composition when it holds the same elements and its element shares lie within 0.003 (L1) of the composition's, a variable oxygen read as its number (`O7-z` as 7) and a second time as a single oxygen, because UCI writes some cuprates as `...Cu3O`. `first_year` is the earliest year of a composition's matched entries. This dates 21,163 of the 21,263 rows (99.5%) and 15,065 of the 15,164 compositions, against 92% for the earlier match on the formula as written.
- Checked: 99.9% of the dated rows have a matched entry whose critical temperature is within 0.01 K of their own, so the match finds the row's own entry, against 0.9% with the compositions shuffled; using only entries above 0 K, or only the entries without the oxygen variant, moves the year of 2.7% and 0.9% of the rows.
- The 100 undated rows leave (63 cuprates, median critical temperature 22.1 K, 99 compositions): a row without a year belongs to no window. Everything else is kept and nothing is deduplicated; the score still counts each composition once (`composition_weight`, the CC of 2026-11-08), and since every entry of a composition carries its first year, a window never splits that one vote.
- Three expanding windows by that year, the eras of the catalogue, compositions whole inside a window (every entry of a composition carries its first year):

  | Test window | Train rows | Share | Test rows | Test compositions |
  |---|---|---|---|---|
  | 2009-2019 (split 0) | 18,654 | 88% | 2,509 | 2,082 |
  | 2002-2008 | 16,488 | 78% | 2,166 | 1,605 |
  | 1996-2001 | 13,180 | 62% | 3,308 | 2,740 |

- Why the split moved: untuned LightGBM, the RMSE of a random half of each window's compositions over 3 seeds (Slurm job 1377613), trained on the earlier years against as many rows from all eras with no test composition (the old split): 18.2 against 14.2 K (1996-2001), 14.9 against 10.0 K (2002-2008), 12.6 against 8.6 K (2009-2019). The old split's ease came from other dopings of the test composition's element set (79-86% of the test compositions had one in training; by year 23-51%), and holding the iron-based family out of every year is harder still (20.1 K). `Timeless` and `StationaryRelation` are ruled out by the drift (median critical temperature 4.4 K up to 1986, 60 K in 1987-1995, 10.9 K in 2009-2019).
- Checked on the built splits: no test row shares its 81 features with a training row, which was the composition split's reason for existing.
- `first_year` is the split's time column and therefore one of the model's inputs, as the joined year is in qsar_tid_11 and apistox. Inside a test window every value lies after the newest training year, so it tells a model only that the row is new; the 81 features stay formula-only.
- Collection facts corrected: `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension`, `required_split` Temporal (NON-IID), tag `Non-IID (Temporal)`.

CC (2026-11-12, Andrej): split back to whole compositions held out (Review issue 5), on the source's scope: Hamidieh (2018) keeps the model to known chemistry ("We should not expect good predictions for completely new superconductors"), so the windows by first report year, which test later families, leave its question. The per-composition score stays; the NIMS dating and the drift between eras move into the `Time basis:` line; `Non-IID (Grouped)`, required split `Grouped (NON-IID)`. Review issue 3 (the year as a model input) is moot.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of no prototype tag (2026-11-12):
- The use case aims at groups the data does not hold, which the held-out groups of the split stand for; `UnseenGroup` (SPLIT-32, the question before the prototypes) names that, where `Timeless` named the target and "no tag" named nothing.
- The split does not change; the definition's `Time basis:` line keeps the measured evidence.

## Review

**Outcome:** added. Hamidieh's superconductor data (UCI 464, 2018): 21,263 entries of the SuperCon database, each a
superconducting material's critical temperature in kelvin, predicted from 81 statistics of the elements in its
chemical formula; since 2026-11-11 the entries are dated through the parent database and held out by the year their
composition was first reported (issue 2, a), which keeps whole compositions on one side, and since 2026-11-08 the
RMSE counts each composition once (issue 4). The AI recommends shipping it as defined.
Reviewed without a panel, from the gathered evidence: the record, the curator's decisions of 2026-10-06 and
2026-10-27, and a model run on TabArena's copy (the same rows, random splits). Validity: the features come from
the formula alone, which a chemist has before synthesis; the grouping removes the identical rows a random split put on
both sides (35% of the test rows had one); every row is a known superconductor, while a screen meets mostly materials
that are not, which the `Selection Bias` marker and the approximate fit already state. Value: on TabArena's random
split the benchmark methods range from RMSE 8.62 K (best) and 8.78 K (TabPFN-3.5) over a median of 9.44 K to 17.4 K
(linear regression); grouping by composition costs little (extra trees R² 0.921 random against 0.919 grouped, the
curator's numbers), so the spread should hold. Quality: entries of one composition differ by more than 30 K for 132
compositions (other samples, phases or pressures the release does not record), and our experiments found a few
probable label errors among the worst-predicted rows (Cu1Cr1O2 at 132 K; Bi2Sr2Ca2O, a supposed cuprate without
copper, at 109 K); kept as the release has them. Weighed: a widely used materials task with a documented source and a
split that matches screening (+), only superconductors and some label noise (-).

**Main points:** Settled 2026-11-12: whole compositions are held out again, on the source's scope (issue 5), so the
time-column question (issue 3) is moot.

**Record judgment:** valid. The composition key, the decision not to group by element set and not to average repeated
entries (Stanev et al. 2018 do) are the curator's (2026-10-06); the selection gap is his (2026-10-27). The metric is the
source's RMSE in kelvin, overruled on the unit it counts (issue 4). The release's second file (`unique_m.csv`) has the element counts behind the 81 statistics;
the definition uses them only for the group key, and the source's model uses the 81 statistics. The data-scouting run of
2026-10-31 found better data for the same task, `supercon_mdr_2024` (priority 2), screened in its own record and not
added yet. The record has no `problem_type` or `domain`; the definition's values can be filled in without a mark.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: features from the formula alone, whole compositions held out, the source's metric, and
       the selection (only superconductors) already marked with an approximate fit.
     - Some entries are noisy or probably wrong (more than 30 K apart within 132 compositions; a few implausible
       temperatures), kept as the release has them.
     - Ship as defined, or retire?
   * **Experiments:** on TabArena's random split the benchmark methods spread from RMSE 8.62 K to 17.4 K (median 9.44
     K); grouping by composition changes untuned scores little (extra trees R² 0.921 random, 0.919 grouped).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 21,263 entries, 15,164 compositions held out whole, RMSE in kelvin | a documented materials task; methods spread; split matches screening | only superconductors; some label noise |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | leaves the place to `supercon_mdr_2024` once added | no defect of the data found; the newer set is not added yet |

   * **Recommendation:** A: the methods spread and the gaps are marked[^1a]. **Decision:** A or B?

   [^1a]: **TP-3** (Must): if tuned methods spread, keep the dataset.

   **Resolved (2026-11-11, Andrej):** A: ship as defined; nothing changed in the definition.

2. **Time basis: name the composition split `Timeless`?**

   * **Problem:**
     - Each row is one SuperCon entry, a reported critical temperature of one composition, gathered from the
       literature over decades and extracted by Hamidieh in 2018; no report year or reference ships, and the 81
       features are computed from the formula alone, before any synthesis.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits a catalogue of material
       properties; the split holds out whole compositions (Lennart, 2026-10-06) and names no time basis yet.
     - A material's critical temperature is a fixed property of the material, the case the `Timeless` prototype
       names[^2a].
   * **Background:** the catalogue grew in waves of families (the cuprates from 1986, MgB2 in 2001, the iron-based
     superconductors from 2008), so a screen for new superconductors meets families the training data may lack. The
     composition split keeps other dopings of a family on both sides, by the curator's choice. A split by report year
     would test the newest families, but the release has no year; `supercon_mdr_2024`, screened as better data, may
     carry the references.
   * **Unknown:** the report year of each entry; whether later families inform earlier ones cannot be measured on this
     release.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Composition split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Composition split, `Timeless` | as now; the tag and a `Time basis:` line naming the property, the undated entries and the waves of families | states the fact the split rests on; as the other materials and molecule sets | the order of discovery stays unmeasured |

   * **Recommendation:** B: the temperature is a property of the material and nothing in the release is dated; a
     split by discovery belongs to `supercon_mdr_2024` if its references give years. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: a critical temperature is a property of the material; the SuperCon
   entries carry no report year, and the families came in waves (cuprates 1986, iron-based 2008), so the composition
   split does not test a family discovered after the training data.`, `splits_comment` unchanged; `dataset check`;
   an Assessment line in `supercon_mdr_2024` to check for report years when it is added.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family. **SPLIT-4** (Must): the split follows what the task does in reality (superconductivity: grouped
     by composition).

   **Answer (AI, 2026-11-06):** Held back from the bulk mark: date the compositions through the NIMS SuperCon datasheet
   first (a), name the composition split forced from temporal now (b), or `Timeless` as drafted (c)?

   * **Problem:**
     - You accepted two items: a catalogue whose population or feature meaning moves with time counts as samples over
       time, and screening asks which identifier a parent source could date the items by, "none published" being an
       answer too; the bulk `Timeless` item had named this dataset as one that moves if the first is accepted[^2q].
     - The release carries an identifier, the formula (`material` in UCI's `unique_m.csv`), and the parent dates it: the
       MDR SuperCon Datasheet Ver.240322 (NIMS, CC BY 4.0, https://doi.org/10.48505/nims.4487) gives each entry its
       formula and the publication year of its reference (33,302 of 33,458 entries, 1913 to 2023).
     - Matched today by the formula as written (no model): 17,403 of the 21,263 UCI rows (81.8%; 12,338 of 15,542
       formulas) get a year; by the earliest year per formula, 5,544 rows up to 1986, 5,021 in 1987-1995, 2,516 in
       1996-2001, 1,841 in 2002-2008 and 2,479 in 2009-2018, the families' waves the issue names.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Date through SuperCon, then decide | each formula joined to its earliest SuperCon year; drift of Tc and of the families by year, and the cost of a split by year, measured as in qsar_tid_11 issue 2; then `Timeless`, windows by year or the forced tag | decides on a measurement; an open parent with the year in its own column | 18% of the rows stay undated by an exact match |
     | b | Composition split, `ForcedGroupedFromTemporal` | the tag and a `Time basis:` line: entries reported from 1913 on, families in waves (cuprates 1986, MgB2 2001, iron-based 2008), no year in the release; a dated release would test the newest family | no join | gives up a year the parent gives for 82% of the rows |
     | c | Composition split, `Timeless` (B as drafted) | the drafted tag and line | nothing to measure | assumes no drift, which the accepted item asks to check |

   * **Recommendation:** a, as qsar_tid_11 did with ChEMBL; the same datasheet is the one `supercon_mdr_2024` would
     ship, so its record can carry the year too. **Decision:** a, b or c?

   [^2q]: **SPLIT-32** (Should; the items of 2026-11-06): question 1 also asks whether the use case meets items drawn
     like the catalogue's; a catalogue whose items enter in eras, or whose features mean something different by when an
     item was made, arose over time; which identifier a parent source could date the items by tells whether it drifts.
     Case: qsar_tid_11 issue 2, dated through ChEMBL.

   **Andrej (2026-11-11, discuss):** Reply (a): Date through SuperCon, then decide.

   **Answer (AI, 2026-11-11):** Dated: the catalogue drifts. Trained on older materials, models do much worse on newer
   ones than on the same rows with a random training set of the same size (RMSE 13.2 K against 8.5 K after 2008).

   * The NIMS SuperCon datasheet Ver.240322 (CC BY 4.0, https://doi.org/10.48505/nims.4487) gives each entry the year
     of its reference (33,302 of 33,458 entries, 1913 to 2023). No other open export carries years for these entries:
     SuperCon2 (NIMS MDR, https://doi.org/10.48505/nims.3735) is a separate set extracted from papers automatically.
   * Matched to the 21,263 UCI rows: 18,057 (85%) by formula and the same Tc, so the very entry; 1,432 more by formula
     only (earliest year); 1,774 (8%) stay undated, 97% of them cuprates whose oxygen SuperCon writes as a variable
     (median Tc 72 K).
   * The families come in waves: cuprates 4,885 of 5,431 dated rows in 1987-1995; iron-based 1,574 of 3,018 after 2008.
     Median Tc by period: 4.4 K (to 1986), 58 K (1987-95), 40 K (1996-2001), 19 K (2002-08), 10.5 K (2009-19).
   * Test: each composition gets its first year; train on the compositions up to a year, test on the later ones,
     against training on a random set of the same size from all eras (other compositions of the test era included),
     scored on the same test rows (LightGBM and extra trees, 3 seeds, sbatch).

     | Test: compositions first reported | Train rows | Test rows | RMSE (R²), older only | RMSE (R²), random eras | Random composition split |
     |---|---|---|---|---|---|
     | after 2008 | 16,931 | 1,292 | 13.2 K (0.55) | 8.5 K (0.81) | 9.0 K (0.93) |
     | after 2001 | 14,678 | 2,413 | 14.6 K (0.67) | 8.5 K (0.89) | 9.2 K (0.92) |
     | after 1986 | 5,504 | 7,046 | 46.2 K (-0.86) | 12.6 K (0.86) | 10.5 K (0.90) |

   * So `Timeless` and `StationaryRelation` are ruled out: the population moves and a split by year costs much[^2r].
   * The gap is mostly new families (the iron-based after 2008), the case the curator did not group for on
     2026-10-06 (not by element set); a split by year tests it the way discovery met it.
   * Windows for a split by year: test 1996-2001, 2002-2008, 2009-2019, the first trained on 54% of the dated rows.

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Temporal split by first report year | a `first_year` column from the datasheet (by formula and Tc, else the formula's earliest year); 3 windows by year, compositions kept whole; the 1,774 undated rows dropped | the split the measured drift asks for; same route as qsar_tid_11 with ChEMBL | joins an outside file; drops 8% of rows, mostly cuprates; a harder task than the screening of dopings |
     | b | Composition split, `ForcedGroupedFromTemporal` | as now; the tag and a `Time basis:` line with the measured cost (13.2 against 8.5 K after 2008) | nothing to join; keeps every row | the rows are dated, so the split is not forced: SPLIT-8 does not apply |
     | c | Composition split, `StationaryRelation` | as now, tag and line | nothing to change | contradicted by the measurement |
     | d | Composition split, `Timeless` (as drafted) | as now, tag and line | nothing to change | assumes no drift; the measurement shows drift |

   * **Recommendation:** a: the dates exist for 92% of the rows and the drift is large, so the rules ask for a split by
     year[^2s]; it gets its own issue with the windows and the undated rows once you choose it. **Decision:** a, b, c
     or d?

   [^2r]: **SPLIT-32** (Should): a catalogue that a parent source dates goes on to the question whether arrival
     affects the target; `StationaryRelation` needs a flat target and a temporal split that costs nothing, and is
     always measured. Case: qsar_tid_11 (predicting each year from earlier ones raised RMSE from 0.68-0.90 to
     1.11-1.31).
   [^2s]: **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID. **SPLIT-14** (Must): at least
     3 windows, none training on less than half the data. **SPLIT-8**: a split is forced only when the time is lost
     or too short for three windows.

   **Answer (AI, 2026-11-11, later):** a fifth option from a second measurement: group by element set instead of by
   year (e). On the same test compositions, holding out the element set is nearly as hard as the split by year, and
   the shipped composition split is 4 to 5 K easier than both.

   * **Dating, rechecked:** matching on element shares within a small tolerance, with variable oxygen (`O7-z`) read
     as its number, dates 21,163 of 21,263 rows (99.5%) instead of 92%. 99.9% of the dated rows have an entry within
     0.01 K of their own Tc (0.9% with the compositions shuffled). With this dating, the 1996-2001 window trains on 62%
     of the rows. The drift is the same: median Tc 4.4 K up to 1986, 60 K in 1987-95, 10.9 K in 2009-19.
   * **Design:** each window's compositions are halved at random (3 seeds). One half is the test set, and the other
     half is open to the splits that may train on the same era. T trains on everything first reported before the
     window. S trains on as many rows from all other years, with no test composition (the shipped kind of split). R
     does the same with no test element set. F holds out the iron-based family of any year. All are scored with the
     definition's composition-weighted RMSE, untuned LightGBM (random forest within 0.6 K), Slurm job 1377613:

     | Test window | T: by year | S: by composition | R: by element set | Same element set in training: T / S | F: iron-based family out |
     |---|---|---|---|---|---|
     | 1996-2001 | 18.2 K | 14.2 K | 18.0 K | 51% / 86% | |
     | 2002-2008 | 14.9 K | 10.0 K | 14.6 K | 42% / 84% | |
     | 2009-2019 | 12.6 K | 8.6 K | 11.6 K | 23% / 79% | |
     | 2009-2019, iron-based only | 12.8 K | 8.3 K | 11.9 K | 18% / 84% | 20.1 K |

     - R trains on 90-93% of T's rows; at that size S changes by at most 0.15 K, so the size does not explain the gap.
     - Over all rows, a 3-fold split by element set scores 14.0 K (R² 0.83) against 10.0 K (0.91) by composition.
   * **What it says:** the shipped split's ease comes from other dopings of the test composition's element set in
     training (79-86% of test compositions have one). A split by year removes most of them (23-51% remain), and so
     does an element-set split, whatever the years. Holding out a whole family is harder than either: the iron-based
     compositions after 2008 met 18% of their element sets in earlier years.
   * **Options added:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | e | Grouped by element set | a group per set of elements (the composition's elements, whatever their shares); every row kept, no outside join | holds out every other proportion of a test composition's elements, the new-system case; no outside join; 3 x 3 folds over all rows | does not test the order of discovery; a doping of a known system, the common case the curator kept in 2026-10-06, is never tested |

   * **Recommendation:** still a: the use case screens compositions not yet made, the dates exist, and the split by year
     tests both new systems and new dopings the way discovery met them. e is the choice if no outside join should
     enter the definition. **Decision:** a, b, c, d or e?


   **Andrej (2026-11-11, discuss):** Reply (a): Temporal split by first report year

   **Resolved (2026-11-11, Andrej):** a: a temporal split by the first report year, built from the 99.5% dating.

   * Each composition is dated through the MDR SuperCon Datasheet Ver.240322 (NIMS, doi:10.48505/nims.4487, CC BY
     4.0, attribution asked and given in the definition's download notes), by element set and element shares within
     0.003 (L1), a variable oxygen read as its number and once as a single oxygen; `first_year` is the earliest year
     of a composition's matched entries. The dating runs in `_load_raw` (`first_report_year`), takes about 4 seconds
    .
   * The 100 undated rows (0.5%; 63 cuprates, median Tc 22.1 K) leave: a row without a year belongs to no window.
     99 compositions go with them. Nothing else is dropped and nothing is deduplicated.
   * Three expanding windows, the eras the issue proposed, every entry of a composition on one side:

     | Test window | Train rows | Share of the rows | Test rows | Test compositions |
     |---|---|---|---|---|
     | 2009-2019 (split 0) | 18,654 | 88% | 2,509 | 2,082 |
     | 2002-2008 | 16,488 | 78% | 2,166 | 1,605 |
     | 1996-2001 | 13,180 | 62% | 3,308 | 2,740 |

   * Checked on the built splits: no test row shares its 81 features with a training row (the composition split's
     reason for existing is covered by the year), and each window's years lie after its training side's.
   * The windows are 6, 7 and 11 calendar years, so `Temporal(horizon=7, horizon_unit="years")` declares the middle
     one; `splits_comment` says so. `first_year` is the time column and therefore one of the model's inputs, as the
     joined year is in qsar_tid_11 and apistox; inside a window every value lies after the newest training year, so
     it carries no information about the test era, and the 81 features stay formula-only.
   * `dataset check`: 0 errors, 1 warning (`dataset_conflicting_duplicate_rows`, 6,026 rows, as before this change:
     the repeated entries of a composition with their own measured temperature), 2 info.

3. **Should the time column be a model input?**

   * **Problem:**
     - `first_year` is the year the composition was first reported, in the paper that reports its critical temperature, which arrives with the target: the scientist screens a candidate composition before synthesising and measuring it[^3a].
     - A declared time column is a model input unless the definition says otherwise, so the task hands models a column the actor does not hold at the prediction point.
     - Keep it an input, or keep it only to order and split the rows?
   * **Background:**
     - The curation notes already say the year is an input only because it is the time column, and that inside a test window it tells a model only that the row is new.
     - Every entry of a composition carries that composition's first year.
     - Since 2026-11-12 `Temporal(..., feature=False)` keeps the time column in the frame for the split and the README's split table and leaves it out of `feature_columns`; sdss_17 (date of the spectrum) is the first user.
   * **Effect on the task:** under B the windows and every split number stay; only the inputs lose the column. Inside a test window every value lies after every training row's, so a model gains from it mainly the order within the window; the size is not measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it an input (implemented) | `first_year` orders the split and is a feature | nothing to change | a model reads a column the actor does not hold |
     | B | Time column only | `Temporal(..., feature=False)`: same windows, `first_year` no model input | the model's inputs are the actor's; the split unchanged | one input fewer; a rebuild |

   * **Recommendation:** B, since the actor does not hold `first_year` when predicting[^3b]. **Decision:** A or B?

   **Notes for the AI:** on B, add `feature=False` to the `Temporal(...)` declaration in `dataset.py`; in `task_summary.known` replace "and the year the composition was first reported, which orders the split." with "the year the composition was first reported orders the split but is no model input." (adjust the sentence around it); add a curation bullet: "`first_year` orders and splits the rows and is no model input (`Temporal(..., feature=False)`): it arrives with the target (2026-11-12, Andrej)."; remove any bullet that calls it a feature; re-run `dataset check` (expect one feature fewer and `time_is_feature: false` in the README). Update the record's `features` count if it names one.

   [^3a]: **USE-3** (Must): name the prediction point, when the model is used and what is known then; a value that
     did not exist at that point is a leak. **LEAK-10** (Must): a feature holds only what existed at the prediction
     point.
   [^3b]: **USE-6** (Must): anything known at the prediction point is a legitimate input, so the question is the
     actor's knowledge, not the score. **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID, so
     B keeps the split as it is.

   **Resolved (2026-11-12, Andrej):** moot: the split holds out whole compositions again (issue 5), so there is no time
   column and the year is no model input.

4. **Count each composition once in the RMSE, or each SuperCon entry, as now?** (issue 1 of the round of
   2026-11-08, renumbered when the issues of 2026-11-11 and 2026-11-12 were added; the CC lines of that day call it
   issue 1)

   * **Problem:**
     - A row is one SuperCon entry, and the per-row RMSE counts a composition as often as SuperCon lists it, from 1 to 110 times (YBa2Cu3O7 110, Bi2Sr2Ca1Cu2O8 83).
     - Every input is computed from the formula, so a model predicts one value per composition, and the materials scientist decides per composition which to synthesize.
     - Should each entry weigh 1 over its composition's number of entries in the score, so that each composition counts once, as each plot of boreal_postfire_lichen_biomass does since 2026-11-08?
   * **Background:**
     - 15,164 compositions: 12,742 with one entry, and 2,422 (16%) with 2 to 110 entries that hold 40% of the 21,263
       rows. Their entries are other samples, phases or pressures, which the release does not record; their critical
       temperatures differ by a median standard deviation of 1.3 K, and 1.6% of the target's variance lies within a
       composition.
     - All 81 inputs are equal within 99.8% of the compositions with several entries. With one prediction per
       composition, the per-entry squared error splits into a floor (the spread of a composition's entries around
       their mean, the same for every model) plus each composition's squared error counted by its number of entries.
     - The source, Hamidieh (2018), scores RMSE per entry on a random split; Stanev et al. (2018) average a material's
       entries when they spread less than 5 K, drop the rest, and so count each material once. The weight keeps the
       release's rows and counts each composition once.
   * **Rules:** the use case decides at which unit the score counts[^sc-unit], and the source's rows stay[^sc-rows]. A
     score weight that follows from the inputs needs no training weight[^sc-weight]; this one follows from the
     composition, which fixes the inputs. A score that departs from the source's names the original[^sc-origin].
   * **Effect on the task:** per entry, the compositions SuperCon lists often (well-studied cuprates among them) weigh
     by their number of entries; per composition, the 12,742 compositions with one entry carry 84% of the weight
     (60% of the rows), and an error on YBa2Cu3O7 counts like an error on any other composition.
   * **Experiments:** the scan of 2026-11-08, 8 untuned predictors (random forest, extra trees, two LightGBM, two
     ridge, kNN and the training mean) on the 9 shipped splits. The weighted score ranks the models like the
     per-entry one at Kendall tau 0.98 per split on average (lowest 0.93) and 0.93 for the ranking by the mean over the
     splits, with the same best model on 9 of 9 splits. Kendall tau measures how far two orders of the models agree, 1
     when they are the same.
   * **Consistency:**
     - boreal_postfire_lichen_biomass counts each plot once since 2026-11-08 (1 over the plot's quadrats, for scoring
       only), on the same grounds: every input belongs to the unit, and the actor acts per unit[^sc-boreal].
     - Your call of 2026-10-06 keeps every entry and scores per row[^sc-cc]; B keeps the entries and changes how much
       each counts.
     - The same scan raised pancreatic_cancer_mouse_detection (per mouse) and dementia_prediction (per person), where
       the inputs differ within the unit.
   * **Panel:** none; raised by the one-vote-per-unit scan of 2026-11-08 (boreal_postfire_lichen_biomass issue 7).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Per entry (implemented) | RMSE over all SuperCon entries, as the source scores it | the source's score; nothing changes | a composition counts as often as SuperCon lists it; YBa2Cu3O7 weighs 110 times a composition measured once |
     | B | Each composition counts once | RMSE weighted by 1 over the composition's entries, a scoring column for the metric only, no training weight | one vote per composition, the unit the scientist acts on; the pattern boreal follows; RMSE takes a weight already | departs from the source's per-entry score; the ranking moves little (tau 0.93 to 0.98) |

   * **Recommendation:** B: every input belongs to the composition, so a model predicts per composition and the
     scientist decides per composition; RMSE already takes a weight, so the cost is one scoring column and the
     departure from the source's score named in the metric. **Decision:** A or B?

   **Notes for the AI:** on B: (1) in `_load_raw`, after `composition`, add `composition_weight`, 1 over the number of
   rows of the composition (`1.0 / df.groupby("composition")["composition"].transform("size")`); (2) declare
   `scoring_columns = (ScoringColumn(column="composition_weight", role="weight", used_by="rmse", description="1 over
   the number of SuperCon entries of the row's composition, so that each composition counts once in the RMSE; for
   scoring only, never a feature or a training weight"),)`; (3) map it in the metric, `inputs={"weight":
   "composition_weight"}`, keep `Metric.source` with `original` naming Hamidieh's RMSE per entry and a `definition`
   that says each composition counts once (MET-11); if the precedent check reads a weighted score as no longer the
   source's, `Metric.from_context("rmse", reason=..., inputs=...)` with the same text; no `sample_weight`; (4) accept
   `task_metric_weight_without_sample_weight` with MET-15's reason: the weight follows from the composition, which
   fixes all 81 inputs in 99.8% of the compositions with several entries, as boreal's `plot_weight` follows from
   `jurisdiction`; (5) replace "Every entry is kept and scored per row" in the notes and "Each row is one prediction"
   in the grouping's definition with the weighting and the scan's taus; (6) `dataset check`, a CC line in the record
   (it supersedes the "scored per row" part of Lennart's CC of 2026-10-06), a CHANGELOG entry, and a Cases row in
   metrics.md next to boreal's (MET-1, MET-15, SPLIT-23). On A: a sentence in the notes that a composition counts by
   its number of entries (1 to 110) and that counting each once ranks 8 untuned models at tau 0.98 per split (0.93
   for the mean ranking). The scan's table and script: the run folder `one_vote_scan/` of the exposure review.

   [^sc-unit]: **SPLIT-23** (Must): the source's use case, cited, decides what one prediction is (a row, or a whole
     group: replicates averaged, any instance positive, the latest row, the best of several candidates). **MET-1**
     (Must): the declared metric scores the real task, at the unit the actor acts on.
   [^sc-rows]: **SPLIT-26** (Should): keep the source's rows; deduplicating with averaged targets is a different
     dataset. Cases: superconductivity.
   [^sc-weight]: **MET-15** (Must), its clause on score weights: a metric weight that is a function of the features
     (liberty_mutual_fire_peril_loss_cost's `var11_weight`, boreal_postfire_lichen_biomass's `plot_weight`) needs no
     sample weight; the bundle check `task_metric_weight_without_sample_weight` is then accepted with that reason.
   [^sc-origin]: **MET-11** (Must): every metric has one origin, and the notes name the original whenever the declared
     metric is not exactly it.
   [^sc-boreal]: boreal_postfire_lichen_biomass, issue 7, Lennart, 2026-11-08: "Option B: Each plot counts once."
   [^sc-cc]: Lennart, CC of 2026-10-06: "Every entry is kept and scored per row."

   **Lennart (2026-11-08, change):** Option B: Each composition counts once.

   **Resolved (2026-11-08, Lennart):** B, each composition counts once. The RMSE is weighted by `composition_weight`,
   1 over the composition's number of SuperCon entries, a scoring column for the metric only with no training weight
   (the bundle warning accepted: the composition fixes all 81 inputs); the metric is now
   `Metric.from_context("rmse")`, its reason naming Hamidieh's per-entry RMSE as the original and Stanev et al.
   counting each material once. Every entry is kept; the notes, the grouping's definition and the record say so, and
   the CC line supersedes "scored per row" of 2026-10-06.

5. **Split: hold out whole compositions again, as the source's scope asks, instead of windows by first report year?**

   * **Problem:** The source keeps its model to known chemistry: Hamidieh (2018) offers it to researchers "interested in
     finding high temperature superconductors" to "narrow their search", warns "We should not expect good predictions
     for completely new superconductors" and scored random 2/3 train, 1/3 test splits. The windows by first report year
     put exactly those later families (the iron-based superconductors from 2008) in the test set.
   * **Rule:** the source's purpose sets which items the test set stands for[^5a].
   * **Change:** The composition-grouped split of 2026-10-06 returns, with each composition counted once in the RMSE
     (issue 4); the dating through the NIMS datasheet and the measured drift move into a `Time basis:` line with no
     prototype tag; there is no time column, so issue 3 is moot.

   [^5a]: **SPLIT-34** (Should), its step on the source's purpose: the use case is the source's, cited; where the source
     keeps its model to items like those it was built from, the family key stands and the entry date is not weighed, and
     how the catalogue arrived is a fact for the notes. **SPLIT-23** (Must): the source's use case, cited, decides what
     one prediction is.

   **Resolved (2026-11-12, Andrej):** whole compositions held out, on the source's scope ("superconductivity would be
   decided to be composition held out"). The definition returns to `Grouping(on="composition")` with the per-composition
   weight; `first_year` and its 100 undated rows' removal go; the `Time basis:` line names Hamidieh's scope, the dating
   and the drift measured between eras. Record: `Non-IID (Grouped)` and required split `Grouped (NON-IID)`, CC line.
   `dataset check` rerun.

## Reference

Hamidieh, Kam. "A data-driven statistical model for predicting the critical temperature of a superconductor." Computational Materials Science 154 (2018): 346-354.
