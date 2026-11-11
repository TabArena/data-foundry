# qsar_biodeg

**Outcome:** added. Ready biodegradability of 1,055 chemicals from the Japanese NITE/MITI database, curated by
Mansouri et al. (2013, J. Chem. Inf. Model. 53(4):867-878, https://doi.org/10.1021/ci4000213): whether a chemical
reaches 60% of its biochemical oxygen demand in the OECD 301C test (33.7% do). Since 2026-11-01 the structure ships as a
SMILES from the paper's supporting information (the same rows in the same order, linked without a key) in place of
the authors' 41 Dragon descriptors, and whole chemical series (Bemis-Murcko scaffolds, 872 groups) are held out; the
metric is the ROC AUC fallback. The AI recommends shipping it. Reviewed on 2026-11-04 without a panel, from the gathered
evidence (the record, Andrej's review of 2026-10-15, the CHANGELOG, model runs on the shipped data and on
TabArena v0.1's copy); Andrej disputes Lennart's `Yes` (issue 1). Validity: a measured outcome of a standard test and a
regulator's screening question; the leak, separation and duplicate objections of 2026-10-15 failed when tested, and the
descriptor selection they concerned no longer reaches the features. Value: the task probes on the v0.2 frame (30
splits) give ROC AUC 0.929 (random forest), 0.928 (LightGBM) and 0.900 (linear), no flags; on the shipped data
(descriptors, random splits) the 40 benchmark methods spread from 0.942 (TabFM) to 0.908 (default logistic regression),
median 0.933. Quality: three stereoisomer pairs stay (each one class, one scaffold); the supporting information states
no licence (Lennart, 2026-11-02: noted, not blocking; to regularise before shipping outside the group). Weighed: a
regulator's real screening task with the structures +, held-out series +, labels cleaned of ambiguous chemicals -, a
six-times larger set for the same question screened -.

**Main points:** Keep qsar_biodeg and decide it against the larger Huang and Zhang set once that set is added (issue 1)?
The time basis of the scaffold split, held back from the bulk `Timeless` mark: date the chemicals through NITE's records
by their CAS-RN first (issue 2, answer of 2026-11-06)?

**Record judgment:** valid. The record carries the v0.2 changes (CC and Assessment of 2026-11-01 and 2026-11-02);
Andrej's dispute of 2026-10-15 is not on the record.

**Issues for Andrej:**

1. **Keep this dataset, given that a larger set for the same question is screened but not added?**

   * **Problem:**
     - Andrej disputes Lennart's `Yes`; the leak, separation and duplicate objections failed when tested, and two soft
       ones, the frozen Dragon descriptors and the random split, are settled by v0.2's structures and scaffold split.
     - What remains is that the labels are cleaner than a screener meets and that Huang and Zhang (2022) compiled
       about 6,100 chemicals for the same yes/no question, screened `TBD -> Yes` (priority 2) but not added.
     - Keep this dataset now and settle the pair when the larger set is added, keep both for good, or retire this
       one now?
   * **Background:**
     - Mansouri et al. (2013), Table 2 (p. 868): of 1,309 chemicals, 254 were removed: 81 whose name and registry
       number did not match, 24 whose replicate tests "had more than 20% difference and classified differently", 4
       whose class would change with nitrification, 54 where the "experimental and NITE classification did not
       agree", and 91 disconnected structures (salts, mixtures). The 78 chemicals with an ambiguous outcome (6%) are
       ones a screener also meets, so the test folds are somewhat easier than real screening.
     - Huang and Zhang, Environ. Sci. Technol. 2022;56(17), https://doi.org/10.1021/acs.est.2c01764: ready
       biodegradability from screening-test records; Körner et al., Environ. Sci.: Processes Impacts 2024,
       https://doi.org/10.1039/d4em00431k, found label noise and identifier errors in it. Another compilation is not
       a duplicate, but some chemicals will be in both[^1a].
   * **Experiments:** an earlier check (2026-10-15, shipped data with the descriptors, 10 x 3 random splits): TabPFN
     3.5 ROC AUC 0.940, random forest 0.931, gradient boosting 0.926, logistic regression 0.923, kNN 0.906; TabPFN ahead
     of logistic regression on 30 of 30 splits and of the random forest on 26. Models trained on the paper's
     calibration chemicals scored 0.7 to 2.4 AUC points higher on its untouched 218 test chemicals than on held-out
     calibration chemicals, the wrong direction for a selection leak. Three exact duplicate pairs, none with
     conflicting classes. On v0.2: random forest 0.929, LightGBM 0.928, linear 0.900 (30 scaffold splits).
   * **Unknown:** how many of the 1,055 chemicals Huang and Zhang hold, and with which class; both carry structures,
     so the overlap is measured when that set is added.
   * **Consistency:** an older dataset keeps the verdict its own data earns when better data turns up, and the curator
     picks one only when the new one is a version of the same source[^1b]; body_density_prediction is recommended for
     shipping until its replacement candidate (NHANES body fat) is added, the same course. The same option is
     proposed for qsar_fish_toxicity (issue 1).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 1,055 chemicals, SMILES, scaffold split; Huang and Zhang judged on its own | a documented regulator's task with structures; the empirical objections failed | labels cleaned of 78 ambiguous chemicals; may overlap a larger set later |
     | B | Keep, settle the pair when Huang and Zhang is added | as A, plus a note to measure the overlap then and retire this one if the larger set holds most of its chemicals with the same class | no gap in the benchmark until the larger set ships; the overlap is decided on data | a second decision later |
     | C | Retire now | the folder goes, the record gets `No` | none beyond the soft arguments | a valid task leaves before a replacement exists[^1c] |

   * **Recommendation:** B: the task is valid and separates methods, and whether it duplicates the larger set can be
     measured once that set is in. **Decision:** keep (A), keep and settle with Huang and Zhang (B), or retire (C)?

   **Notes for the AI:** on B, an Assessment line in this record and in `ready_biodegradability_huang_zhang`: when
   that set is added, match on canonical SMILES and CAS-RN, report the share of these 1,055 chemicals found and their
   class agreement, and put the pair to the curator. On C: `No (Retired)`, remove the folder, CHANGELOG entry.

   [^1a]: **PROV-4** (Must): two records are duplicates only when they end at the same original source; **PROV-7**
     (Must): records that share a source but give different tasks are not duplicates.
   [^1b]: selection.md, "Small or dated, and the task is still done today": a hit from another source is its own
     record; the old record is not rejected automatically and keeps the verdict its own data earns. **PROV-6**
     (Must): versions or cuts of one underlying dataset are duplicates when neither adds a distinct task.
   [^1c]: **TP-6** (Must): keep two questions apart, is the task valid and is it the best version; a valid task stays.

2. **Time basis: name the scaffold split `Timeless`?**

   * **Problem:**
     - Each row is a chemical with the outcome of a standard ready-biodegradability test (OECD 301C) from the Japanese
       NITE/MITI database, tested over many years and curated in 2013 (Mansouri and colleagues); the release keeps no
       test date, and the only feature is the structure, which exists before any test.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits a catalogue of
       properties; the split holds out whole scaffolds and names no time basis yet.
     - Whether a chemical is readily biodegradable under one test is a fixed property of the chemical, the case the
       `Timeless` prototype names[^2a].
   * **Background:** the MITI programme tested existing industrial chemicals and newly notified ones over decades, so
     the mix of tested chemistry changed; a new chemical often comes from a series not yet tested, which the scaffold
     split stands for. No test date ships; the labels were cleaned once, at curation (78 ambiguous chemicals
     removed), and are not revised over time. The larger Huang and Zhang set (issue 1) is no time question.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Scaffold split, `Timeless` | as now; the tag and a `Time basis:` line naming the property and the undated compilation | states the fact the split rests on; as the other molecule sets | the order in which chemicals were tested stays unmeasured |

   * **Recommendation:** B: the test outcome is a property of the chemical, and the series split stands for new
     chemistry. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: ready biodegradability under the OECD 301C test is a property of the
   chemical; the NITE/MITI results were curated in 2013 without test dates, and whole scaffolds are held out for new
   series.`, `splits_comment` unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family. **SPLIT-31** (Should): a molecule dataset with exact structures groups on the Bemis-Murcko
     scaffold.

   **Answer (AI, 2026-11-06):** Held back from the bulk mark: date the chemicals through NITE's records first (a), name
   the scaffold split forced from temporal now (b), or `Timeless` as drafted (c)?

   * **Problem:**
     - You accepted two items: a catalogue whose population or feature meaning moves with time counts as samples over
       time, and screening asks which identifier a parent source could date the items by, "none published" being an
       answer too; the bulk `Timeless` item had named this dataset as one that moves if the first is accepted[^2q].
     - The release carries an identifier: the paper's supporting information (sheet "Train+Test", re-fetched today, the
       definition's checksum) gives all 1,055 chemicals a well-formed CAS-RN and a SMILES. NITE's J-CHECK holds the MITI
       test results by CAS-RN; whether it gives a test or notification year was not checked.
     - MITI tested existing chemicals from the 1970s and newly notified ones later, so the mix of tested chemistry moved
       over the decades the data spans.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Date through NITE, then decide | look up each CAS-RN in J-CHECK for the year of its MITI test; if dated, measure as in qsar_tid_11 issue 2; then `Timeless`, windows by year or the forced tag | decides on a measurement; the key ships in the release | J-CHECK may give no year, then b |
     | b | Scaffold split, `ForcedGroupedFromTemporal` | the tag and a `Time basis:` line: MITI tests over decades, no date in the release, likely drift from existing to newly notified chemicals; a dated release would test the newest chemistry | no lookup | gives up a date the CAS-RN may recover |
     | c | Scaffold split, `Timeless` (B as drafted) | the drafted tag and line | nothing to measure | assumes no drift, which the accepted item asks to check |

   * **Recommendation:** a; b if J-CHECK gives no year. **Decision:** a, b or c?

   [^2q]: **SPLIT-32** (Should; the items of 2026-11-06): question 1 also asks whether the use case meets items drawn
     like the catalogue's; a catalogue whose items enter in eras, or whose features mean something different by when an
     item was made, arose over time; which identifier a parent source could date the items by tells whether it drifts.
     Case: qsar_tid_11 issue 2, dated through ChEMBL.

   **Andrej (2026-11-11, discuss):** Reply (a): Date through NITE, then decide

   **Answer (AI, 2026-11-11):** the dating is running; this turn records the decision, and the measurement follows.

   **Answer (AI, 2026-11-11):** dated, 1,050 of 1,055. A split by year costs nothing measurable, but the test
   protocol changed over the span, so the choice is not between a harder and an easier split.

   * **The dating:** NITE publishes the CSCL biodegradation results of existing chemicals as a workbook next to
     J-CHECK (https://www.nite.go.jp/en/chem/qsar/evaluation.html, `000064112.xlsx`), one row per tested chemical
     with CAS, SMILES, % BOD, the test guideline and the fiscal year of the test; J-CHECK's own per-CAS records give
     the bulletin date for 44 more. Together they date 1,050 chemicals (99.5%), 1971 to 2008.
   * **Checks:** NITE's measured % BOD agrees with the shipped class on 989 of 1,006 (the 17 others are `Yes` at
     40-58% BOD, all 1975-80 tests judged on TOC or GC rather than BOD); the structures match on 958 of 1,006, the
     rest NITE tautomer conventions; where both dates exist, the workbook year and the bulletin year agree on 250 of
     253, and the 3 exceptions are the 1971 cohort announced in 1981, which is what shows `Year` is the test year.
   * **What moves with the period:**

     | Period | Chemicals | Readily biodegradable | 14-day tests | 28-day tests | New scaffolds |
     |---|---|---|---|---|---|
     | 1971-1979 | 219 | 40.2% | 80.4% | 11.4% | |
     | 1980-1989 | 306 | 27.8% | 28.1% | 65.7% | 82.0% |
     | 1990-1999 | 223 | 44.8% | 20.6% | 75.8% | 87.9% |
     | 2000-2008 | 302 | 26.8% | 6.6% | 88.4% | 81.5% |

     - The chemistry turns over wholesale: 82-88% of each period's chemicals carry a scaffold no earlier period had.
     - Of 303 chemicals looked up in J-CHECK, 241 are existing substances and 2 newly announced, so the drift is
       inside the existing-chemicals programme, not the shift from existing to notified chemicals the issue assumed.
   * **The split, four expanding windows by test year against the scaffold folds on the same test chemicals**
     (untuned LightGBM / random forest, `encode_smiles`, every training side at least half the dated rows; Slurm
     1378095):

     | Scheme | ROC AUC, LightGBM / RF | Log loss, LightGBM / RF | Close training analog | Test scaffold in training |
     |---|---|---|---|---|
     | T, forward by test year | 0.921 / 0.933 | 0.836 / 0.334 | 10.3% | 16.0% |
     | S, scaffold-disjoint | 0.918 / 0.926 | 0.818 / 0.342 | 10.3% | 0 |
     | R, random | 0.921 / 0.929 | 0.816 / 0.335 | 11.8% | 16.6% |
     | Shipped scaffold folds | 0.933 / 0.930 | 0.671 / 0.331 | 10.0% | 0 |

     - The scaffold split already puts a test chemical as far from training as the next years do: the close-analog
       share is the same under all three.
     - The one place the time order shows is calibration in the oldest window, whose test set is 53.2% readily
       biodegradable against a 33.0% training prior (log loss 1.288 against 1.134 scaffold-disjoint).
   * **What it means for the time basis:** the target is a fixed property, but how it was recorded moved, from mostly
     14-day tests to mostly 28-day ones, and the class share swings by period; that is a change in recording rather
     than in prevalence, so `Timeless` and `StationaryRelation` both overstate what the data supports[^2t].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Temporal split by test year | a `test_year` column from the NITE workbook, four expanding windows; the scaffold grouping goes | the protocol and the chemistry both move with the year, and the year is now in hand | joins an outside file; 5 chemicals undated; the windows score like the scaffold folds, so nothing is gained in difficulty |
     | b | Scaffold split (implemented), `Timeless` | the tag and a line | nothing to change | the 14-day to 28-day shift is a change in how the label was measured |
     | c | Scaffold split, the drift written down, no prototype tag | the measured table in the notes, no tag claimed | states what is known without claiming a prototype that does not fit | leaves the definition without a stated time basis |

   * **Recommendation:** a: the protocol changed over the span and the year is recoverable, which is what decides;
     that it costs nothing measurable is not a reason either way. **Decision:** a, b or c?

   **Notes for the AI:** on a, add `test_year` in `_prepare_raw_files` from the NITE workbook (joined on CAS, the
   bulletin year as fallback), drop the 5 undated chemicals or keep them in the oldest training side, declare
   `temporal = Temporal(on="test_year", ...)` with the four windows, remove `grouping` and the `scaffold` column, and
   keep the analog shares in the notes; evidence and scripts in `~/claude_jobs/qsar_nite/`.

   [^2t]: **SPLIT-32** (Should): the arrival of the samples affects the target when how the target or the features
     are recorded changes (a new grading, a new instrument, a new selection of cases); a change in how often the
     target occurs does not count by itself. `StationaryRelation` needs the target and its relation to the features
     flat across periods, always measured.
