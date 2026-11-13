---
unique_name: qsar_biodeg
name: qsar-biodeg
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
priority: 2
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- Expanding Science Catalogue
original_source: UCI
year: '2013'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1494
- https://doi.org/10.24432/C5H60M
notebook_path: datasets/beyond_iid/old_iid/qsar_biodeg/qsar_biodeg.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_biodeg/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Nice chemistry dataset with (computed) molecular propeties to predict whether the sample is ready and not ready biodegradable. Linear model among best in TabRepo

Potential issue: -

Lennart: no objection

Andrej: Matches criteria

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Mansouri et al. (2013) report error rate / NER with sensitivity and specificity, without a threshold or costs. Original rejected: NER (balanced accuracy).

CC (2026-10-30, Lennart): `N073_chemical_substructure` and `C026_chemical_substructure` are numeric: the atom-centred fragments N-073 (Ar2NH / Ar3N / Ar2N-Al / R..N..R) and C-026 (R--CX--R) count the atoms of that type (0 to 3 and 0 to 12). The definition had typed them categorical while their meaning was unknown; the dtype probe found them in the sweep after issue #34. CLEAN-14: a count stays numeric.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `ready_biodegradability_huang_zhang` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): go ahead for the structure-recoverable datasets: ship the SMILES only, as for qsar_tid_11. The authors' descriptors are one modelling choice; the benchmark encodes the structure.

**Assessment (AI, 2026-11-01):** the structures are recoverable and the link is exact. The paper's supporting information (ACS, `ci4000213_si_001.xlsx`, taken from the Internet Archive since pubs.acs.org refuses a command-line download) holds, in its `Train+Test` sheet, the same 1,055 rows in the same order as UCI's `biodeg.csv`, with CAS-RN, SMILES, the class and all 41 descriptors: every descriptor and the class are identical on every row, so no key is needed. The 41 Dragon descriptors leave; `SMILES` is the one feature, and the split is scaffold-grouped (872 groups). Three stereoisomer pairs (maleic/fumaric acid, sorbitol/mannitol, dieldrin/endrin) stay, each agreeing on its class; they share a scaffold. The task probes raise no flag: random forest ROC AUC 0.929, LightGBM 0.928, linear 0.900 over 30 splits. The `External validation` sheet holds 670 further chemicals with structures and classes (657 new); that is a candidate of its own, noted for screening.

CC (2026-11-02, Lennart): on how the supporting information was downloaded (ACS states no licence for it, and
pubs.acs.org refuses a command-line download, so it came from the Internet Archive): "that is okay for now, we can
note it but it is not blocking us here". Noted here; regularise before this ships outside the group.

**Assessment (AI, 2026-11-02):** the `External validation` sheet this record set aside is now screened as its own
candidate, `ready_biodegradability_mansouri_external` (`TBD -> 2nd Tier`, priority 2). It is not a cut of this
dataset: the 1,055 chemicals here were curated from NITE/MITI, while those 670 "[were] constructed from two data
sources, Cheng et al. and the Canadian DSL database" (Chakravarti and Alla, arXiv 1808.04456, Table 1), and only 8
of the 670 canonical structures occur here, one of them with the opposite class. The other record notes that its
most useful role may be as an external check on this dataset's scaffold split rather than as a dataset of its
own.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: v0.2's structures and scaffold split settle the soft objections in Andrej's dispute, the leak/separation/duplicate objections failed when tested, and the larger Huang and Zhang set is to be weighed against it once added. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): split by the year of the test (review issue 2, a), in place of the scaffold-grouped split; `Non-IID (Temporal)`, `Samples: Over Time`, `Time: Dated`, required split `Temporal (NON-IID)`.
- Dated through NITE: its workbook of the CSCL biodegradation results of existing chemicals (https://www.nite.go.jp/data/000064112.xlsx) gives the MITI test year for 1,006 chemicals by CAS-RN, and J-CHECK's bulletin year 44 more; 5 undated chemicals leave, so 1,050 rows, tested 1971 to 2008.
- Why: the protocol moved with the year (80% 14-day tests before 1980, 88% 28-day tests from 2000 on), the class share swings by decade (40%, 28%, 45%, 27%), and 82-88% of each decade's chemicals carry a new scaffold; a change in how the label was recorded rules out `Timeless`.
- Four expanding windows (2003-08, 2000-02, 1994-98, 1990-93; 125, 177, 112, 111 test chemicals, train 50-88%). On the same test chemicals the split by year scores like the scaffold split (ROC AUC LightGBM / RF 0.921 / 0.933 against 0.918 / 0.926), so it is chosen for the time order, not for difficulty.
- Evidence: `~/claude_jobs/qsar_nite/` (Slurm 1378095).

CC (2026-11-12, Andrej): review page mark (issue 1, B): keep qsar_biodeg, and settle the pair with `ready_biodegradability_huang_zhang` when that set is added: measure the overlap then and retire this one if the larger set holds most of its chemicals with the same class.

**Assessment (AI, 2026-11-12):** pair with `ready_biodegradability_huang_zhang` open: when that set is added, match its chemicals to these 1,050 on canonical SMILES and CAS-RN, report the share found and their class agreement, and put the pair to the curator; this one is retired if the larger set holds most of its chemicals with the same class.

CC (2026-11-12, Andrej): split back to whole chemical series held out (Review issue 4), on the source's scope: Mansouri et al. (2013) build a REACH screen validated on chemicals from other sources, so windows by the year Japan's programme tested a chemical leave its question. All 1,055 chemicals return; the NITE dating and the 14-day to 28-day change move into the `Time basis:` line as facts about the labels; `Non-IID (Grouped)`, required split `Grouped (NON-IID)`. Review issue 3 (the year as a model input) is moot.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of no prototype tag (2026-11-12):
- The use case aims at groups the data does not hold, which the held-out groups of the split stand for; `UnseenGroup` (SPLIT-32, the question before the prototypes) names that, where `Timeless` named the target and "no tag" named nothing.
- The split does not change; the definition's `Time basis:` line keeps the measured evidence.

## Review

**Outcome:** added. Ready biodegradability of 1,055 chemicals from the Japanese NITE/MITI database, curated by
Mansouri et al. (2013, J. Chem. Inf. Model. 53(4):867-878, https://doi.org/10.1021/ci4000213): whether a chemical
reaches 60% of its biochemical oxygen demand in the OECD 301C test (33.7% do). Since 2026-11-01 the structure ships as a
SMILES from the paper's supporting information (the same rows in the same order, linked without a key) in place of
the authors' 41 Dragon descriptors; since 2026-11-11 the split is by the year of the MITI test (four windows,
1,050 chemicals dated through NITE), in place of the scaffold-grouped split (issue 2); the metric is the ROC AUC
fallback. The AI recommends shipping it. Reviewed on 2026-11-04 without a panel, from the gathered
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

**Main points:** Settled 2026-11-12: whole chemical series are held out again, on the source's scope (issue 4), so the
time-column question (issue 3) is moot.

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

   **Andrej (2026-11-12, change):** Option B: Keep, settle the pair when Huang and Zhang is added.

   **Resolved (2026-11-12, Andrej):** B: kept. An Assessment line in this record and in
   `ready_biodegradability_huang_zhang`: when that set is added, match on canonical SMILES and CAS-RN, report the share
   of these chemicals found and their class agreement, and put the pair to the curator; record CC line. No change to
   the definition.

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

   **Andrej (2026-11-11, discuss):** Reply (a): Temporal split by test year

   **Resolved (2026-11-11, Andrej):** a: split by the year of the MITI test. `test_year` comes from NITE's workbook
   (`000064112.xlsx`, now downloaded by the definition, sha256 in `download_description`) joined on the CAS-RN, with
   J-CHECK's bulletin year for 44 chemicals the workbook misses (a constant in `dataset.py`); the 5 undated chemicals
   leave (1,050 rows). Four expanding windows declared through `Temporal(on="test_year")` and `_make_splits`:

   | Test window | Test chemicals | Train chemicals | Train share |
   |---|---|---|---|
   | 2003-08 | 125 | 925 | 88% |
   | 2000-02 | 177 | 748 | 71% |
   | 1994-98 | 112 | 636 | 61% |
   | 1990-93 | 111 | 525 | 50% |

   `grouping` and the `scaffold` column are gone; `test_year` is a feature as well as the time column (as in
   qsar_tid_11). The measured table and the drift go into `curation_comments`, the task summary names the year, and a
   window table goes into the README's decisions. Record: `Non-IID (Temporal)`, `Samples: Over Time`, `Time: Dated`,
   required split `Temporal (NON-IID)` (mirrored in PR #50's copy), CC line. No time-basis tag: the split is temporal.
   `dataset check`: 0 errors, 0 warnings (1 info: the year horizon on an integer column, as intended).

3. **Should the time column be a model input?**

   * **Problem:**
     - `test_year` is the year of the chemical's ready-biodegradability test, the test that gives the label, which arrives with the target: the regulator or manufacturer screens a structure to decide whether it needs that test[^3a].
     - A declared time column is a model input unless the definition says otherwise, so the task hands models a column the actor does not hold at the prediction point.
     - Keep it an input, or keep it only to order and split the rows?
   * **Background:**
     - The curation notes keep the year as a feature 'as in the other temporal tasks (apistox, qsar_tid_11)', which this issue reopens for all three.
     - The task summary lists the test year among what is known.
     - Since 2026-11-12 `Temporal(..., feature=False)` keeps the time column in the frame for the split and the README's split table and leaves it out of `feature_columns`; sdss_17 (date of the spectrum) is the first user.
   * **Effect on the task:** under B the windows and every split number stay; only the inputs lose the column. Inside a test window every value lies after every training row's, so a model gains from it mainly the order within the window; the size is not measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it an input (implemented) | `test_year` orders the split and is a feature | nothing to change | a model reads a column the actor does not hold |
     | B | Time column only | `Temporal(..., feature=False)`: same windows, `test_year` no model input | the model's inputs are the actor's; the split unchanged | one input fewer; a rebuild |

   * **Recommendation:** B, since the actor does not hold `test_year` when predicting[^3b]. **Decision:** A or B?

   **Notes for the AI:** on B, add `feature=False` to the `Temporal(...)` declaration in `dataset.py`; in `task_summary.known` replace "and the year it was tested." with "the year it was tested orders the split but is no model input." (adjust the sentence around it); add a curation bullet: "`test_year` orders and splits the rows and is no model input (`Temporal(..., feature=False)`): it arrives with the target (2026-11-12, Andrej)."; remove any bullet that calls it a feature; re-run `dataset check` (expect one feature fewer and `time_is_feature: false` in the README). Update the record's `features` count if it names one.

   [^3a]: **USE-3** (Must): name the prediction point, when the model is used and what is known then; a value that
     did not exist at that point is a leak. **LEAK-10** (Must): a feature holds only what existed at the prediction
     point.
   [^3b]: **USE-6** (Must): anything known at the prediction point is a legitimate input, so the question is the
     actor's knowledge, not the score. **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID, so
     B keeps the split as it is.

   **Resolved (2026-11-12, Andrej):** moot: the split holds out whole chemical series again (issue 4), so there is no
   time column and the year is no model input.

4. **Split: hold out whole chemical series again, as the source's scope asks, instead of windows by test year?**

   * **Problem:** The source builds a regulatory screen: Mansouri et al. (2013) open with REACH, which "requires
     information on ready biodegradation" and encourages QSAR predictions in place of tests, and they validate on 670
     chemicals from other sources. Its question is a chemical from outside the collection, not the next chemical in the
     order Japan's programme tested its existing chemicals; by year, test chemicals keep as many close training analogs
     as under the scaffold split (10.3% each, 11.8% at random).
   * **Rule:** the source's purpose sets which items the test set stands for[^4a].
   * **Change:** The scaffold-grouped split of 2026-11-01 returns with all 1,055 chemicals; the NITE dating, the move
     from 14-day to 28-day tests and the measurement move into a `Time basis:` line with no prototype tag, as a fact
     about the labels; there is no time column, so issue 3 is moot.

   [^4a]: **SPLIT-34** (Should), its step on the source's purpose: the use case is the source's, cited; where the source
     keeps its model to items like those it was built from, the family key stands and the entry date is not weighed, and
     how the catalogue arrived is a fact for the notes. **SPLIT-23** (Must): the source's use case, cited, decides what
     one prediction is.

   **Resolved (2026-11-12, Andrej):** whole chemical series held out, on the source's scope ("qsar biodeg would be
   scaffold"). The definition returns to the scaffold grouping with all 1,055 rows; `test_year`, the NITE download and
   the J-CHECK constant go, and the `Time basis:` line keeps what they showed. Record: `Non-IID (Grouped)` and required
   split `Grouped (NON-IID)`, CC line. `dataset check` rerun.

## Reference

Mansouri, K., Ringsted, T., Ballabio, D., Todeschini, R., Consonni, V. (2013). Quantitative Structure - Activity Relationship models for ready biodegradability of chemicals. Journal of Chemical Information and Modeling, 53, 867-878
