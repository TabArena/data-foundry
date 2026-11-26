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
suggestion: No (Retired)
decision_markers:
- Duplicate
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- Expanding Science Catalogue
original_source: UCI
year: '2013'
collection_period: 1971-2008
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1494
- https://doi.org/10.24432/C5H60M
notebook_path: datasets/beyond_iid/old_iid/qsar_biodeg/qsar_biodeg.ipynb
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

**Assessment (AI, 2026-11-04):** reviewed for BeyondArena v0.2, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: v0.2's structures and scaffold split settle the soft objections in Andrej's dispute, the leak/separation/duplicate objections failed when tested, and the larger Huang and Zhang set is to be weighed against it once added. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): split by the year of the test (Review issue 2, a), in place of the scaffold-grouped split; `Non-IID (Temporal)`, `Samples: Over Time`, `Time: Dated`, required split `Temporal (NON-IID)`.
- Dated through NITE: its workbook of the CSCL biodegradation results of existing chemicals (https://www.nite.go.jp/data/000064112.xlsx) gives the MITI test year for 1,006 chemicals by CAS-RN, and J-CHECK's bulletin year 44 more; 5 undated chemicals leave, so 1,050 rows, tested 1971 to 2008.
- Why: the protocol moved with the year (80% 14-day tests before 1980, 88% 28-day tests from 2000 on), the class share swings by decade (40%, 28%, 45%, 27%), and 82-88% of each decade's chemicals carry a new scaffold; a change in how the label was recorded rules out `Timeless`.
- Four expanding windows (2003-08, 2000-02, 1994-98, 1990-93; 125, 177, 112, 111 test chemicals, train 50-88%). On the same test chemicals the split by year scores like the scaffold split (ROC AUC LightGBM / RF 0.921 / 0.933 against 0.918 / 0.926), so it is chosen for the time order, not for difficulty.

CC (2026-11-12, Andrej): Review issue 1, B: keep qsar_biodeg, and settle the pair with `ready_biodegradability_huang_zhang` when that set is added: measure the overlap then and retire this one if the larger set holds most of its chemicals with the same class.

**Assessment (AI, 2026-11-12):** pair with `ready_biodegradability_huang_zhang` open: when that set is added, match its chemicals to these 1,050 on canonical SMILES and CAS-RN, report the share found and their class agreement, and put the pair to the curator; this one is retired if the larger set holds most of its chemicals with the same class.

CC (2026-11-12, Andrej): split back to whole chemical series held out (Review issue 4), on the source's scope: Mansouri et al. (2013) build a REACH screen validated on chemicals from other sources, so windows by the year Japan's programme tested a chemical leave its question. All 1,055 chemicals return; the NITE dating and the 14-day to 28-day change move into the `Time basis:` line as facts about the labels; `Non-IID (Grouped)`, required split `Grouped (NON-IID)`. Review issue 3 (the year as a model input) is moot.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of no prototype tag (2026-11-12):
- The use case aims at groups the data does not hold, which the held-out groups of the split stand for; `UnseenGroup` (SPLIT-32, the question before the prototypes) names that, where `Timeless` named the target and "no tag" named nothing.
- The split does not change; the definition's `Time basis:` line keeps the measured evidence.

CC (2026-11-17, Andrej): the declared split (grouped on `scaffold`, 10x3 folds, `UnseenGroup`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-26, Andrej): verdict dont: "retire, replaced by ready_biodegradability_huang_zhang. Huang-Zhang
contains 1,011 of its 1,055 chemicals and gives 976 of them the same class. It has 5.8× the chemistry and separates
methods three times as far. " Applied (Review issue 5, C), which is the condition the decision of 2026-11-12 set
(issue 1, B: measure the overlap when the larger set is added "and retire this one if the larger set holds most of
its chemicals with the same class"):
- `No (Retired)` with the marker `Duplicate`, on the curator's reading that each set is a cut of the same underlying
  registry data as the other (PROV-6);
- the replacement is `ready_biodegradability_huang_zhang`, added and accepted: the same question, whether a chemical
  is readily biodegradable in an OECD screening test, on 6,139 chemicals against these 1,055 and 1,308 Bemis-Murcko
  scaffolds against 209, with the same single feature (the structure as a SMILES), the same scaffold-grouped split
  and the same `roc_auc` fallback. Measured on 2026-11-25: it holds 1,011 of these 1,055 chemicals (95.8%, matched on
  canonical SMILES or CAS-RN) and gives 976 of them the same class; untuned LightGBM beats a linear model on it by
  0.076 ROC AUC (0.890 against 0.814) against 0.025 here (0.935 against 0.911), and a model trained on its other
  5,183 chemicals scores 0.938 on these 1,055, as high as one trained here under this dataset's own split;
- the folder leaves the TabArena v0.2 working copy and `v2_path` is cleared; the definition stays in the git history.

## Review

**Outcome:** added, then retired on 2026-11-26 (verdict dont, issue 5, C): replaced by
`ready_biodegradability_huang_zhang`, the same question on 6,139 chemicals against these 1,055, which holds 1,011 of
them (95.8%) with 976 at the same class and separates methods three times as far; marker `Duplicate`, the folder
removed. As added: ready biodegradability of 1,055 chemicals from the Japanese NITE/MITI database, curated by
Mansouri et al. (2013, J. Chem. Inf. Model. 53(4):867-878, https://doi.org/10.1021/ci4000213): whether a chemical
reaches 60% of its biochemical oxygen demand in the OECD 301C test (33.7% do). Since 2026-11-01 the structure ships as a
SMILES from the paper's supporting information (the same rows in the same order, linked without a key) in place of
the authors' 41 Dragon descriptors; whole chemical series are held out on the Bemis-Murcko scaffold (209 groups), the
split the source's scope asks for, restored on 2026-11-12 after the split by the year of the MITI test that had
replaced it the day before (issues 2 and 4); the metric is the ROC AUC fallback.
Reviewed on 2026-11-04 without a panel, from the gathered
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

**Main points:** Nothing open. Retired (2026-11-26, verdict dont, issue 5, C) as replaced by
`ready_biodegradability_huang_zhang`, which is added and accepted: matched on canonical SMILES or CAS-RN, that
6,139-chemical set holds 1,011 of these 1,055 chemicals (95.8%) and gives 976 of them the same class, which is the
condition the decision of 2026-11-12 set for retiring this one (issue 1, B), and it carries the same question on 5.8
times the chemistry while separating methods three times as far (untuned LightGBM over a linear model +0.076 ROC AUC
against +0.025 here); marker `Duplicate`, the folder removed. Settled before, on 2026-11-12: kept until that set was
added (issue 1, B); whole chemical series are held out again, on the source's scope (issue 4, replacing the split
by test year of issue 2), so the time-column question (issue 3) is moot. Time basis `UnseenGroup` since 2026-11-13.

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

   **Notes for the AI:** on B: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
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
     (untuned LightGBM / random forest, `encode_smiles`, every training side at least half the dated rows):

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
   keep the analog shares in the notes.

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
   required split `Temporal (NON-IID)`, CC line. No time-basis tag: the split is temporal.
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

   [^4a]: **SPLIT-37** (Should), its step on the source's purpose: the use case is the source's, cited; where the source
     keeps its model to items like those it was built from, the family key stands and the entry date is not weighed, and
     how the catalogue arrived is a fact for the notes. **SPLIT-23** (Must): the source's use case, cited, decides what
     one prediction is.

   **Resolved (2026-11-12, Andrej):** whole chemical series held out, on the source's scope ("qsar biodeg would be
   scaffold"). The definition returns to the scaffold grouping with all 1,055 rows; `test_year`, the NITE download and
   the J-CHECK constant go, and the `Time basis:` line keeps what they showed. Record: `Non-IID (Grouped)` and required
   split `Grouped (NON-IID)`, CC line. `dataset check` rerun.

5. **Keep qsar_biodeg until ready_biodegradability_huang_zhang is added, then retire it as replaced, add it next to it, or keep qsar_biodeg as it is?**

   * **Problem:**
     - Measured on the files on 2026-11-25, on the two keys the curator named: Huang and Zhang's 6,139 chemicals hold 1,011 of qsar_biodeg's 1,055 (95.8%; 953 by canonical SMILES alone, 745 by CAS-RN) and give 976 of the 1,011 the same class, which is the condition set on 2026-11-12 for retiring this one.
     - The larger set also makes the harder benchmark and keeps the labels a screener meets: untuned LightGBM beats a linear model by 0.076 ROC AUC on it (0.890 against 0.814, scaffold-grouped) against 0.025 here (0.935 against 0.911), and 4.2% of its chemicals have repeat tests that disagree, the ambiguity Mansouri's curation removed and issue 1 named as this dataset's remaining defect.
     - Keep qsar_biodeg as it is, add Huang and Zhang next to it, keep this one until that set is added and then retire it as replaced, or replace both by a merged set?
   * **Background:**
     - Parked on 2026-11-12 as issue 1, option B: keep, and settle the pair when Huang and Zhang is added - "measure the overlap then and retire this one if the larger set holds most of its chemicals with the same class". This item is that measurement; nothing else about qsar_biodeg is open.
     - Current state: 1,055 chemicals from the Japanese NITE/MITI database curated by Mansouri et al. (2013), one feature (the structure as a SMILES; the 41 Dragon descriptors left on 2026-11-01), the label whether the chemical reaches 60% of its biochemical oxygen demand in the OECD 301C test (33.7% do), whole chemical series held out on the Bemis-Murcko scaffold (209 distinct scaffolds), time basis `UnseenGroup`, metric the `roc_auc` fallback.
     - The candidate: Huang and Zhang, Environ. Sci. Technol. 2022, 56(17), https://doi.org/10.1021/acs.est.2c01764, compiled from an eChemPortal export of REACH registration dossiers. `ClassDataset_original` (4,593 chemicals) is derived from their 12,750-record regression set, `ClassDataset_external` (1,546) was compiled from the literature as a second source, and `ClassDataset_all` (6,139) is the two together; 34.9% readily biodegradable, one row per chemical, every SMILES parses, 6,137 distinct structures.
     - Its label is the same test outcome read the same way: rebuilt from their regression workbook as "at least 60% degradation at day 28 (70% for DOC die-away) in a ready-biodegradation screening test", it reproduces 4,495 of the 4,591 classes (97.9%). The guideline mix is wider than ours - OECD 301 F 24%, 301 B 24%, 301 C 18%, 301 D 18%, the rest 301 A/E and 310 - where qsar_biodeg is OECD 301C alone; the inherent-biodegradation records of the regression set do not enter the classification file.
     - Its defects, measured: 209 of the 4,966 chemicals with a 28-day ready test (4.2%) have repeat tests that disagree on pass or fail and the file keeps one class for them; 2 structures occur twice and 145 more once stereochemistry is set aside (15 of those with conflicting classes); 22 CAS numbers occur twice (6 with conflicting classes); the 1,546 literature rows carry no CAS number and no name; and 100 of those 1,546 structures (6.5%, stereochemistry set aside) also sit in the 4,593, 7 with the opposite class - the train/test leakage Körner et al. (2024) report, which matters for their published scores but not for a scaffold split built here.
     - What a definition would ship: the same single SMILES column and the same recommended encoding as qsar_biodeg, not precomputed descriptors[^smiles]; scaffold-grouped (1,308 distinct scaffolds against 209)[^smiles]; the `roc_auc` fallback. Körner's pKa and speciation columns are computed from the structure and would leave, as the Dragon descriptors did. No test dates are published for it, so there is no temporal option.
     - Candidates:

       | Candidate | Rows | What it adds | Split it allows | Access, licence | Concerns | Verdict |
       |---|---|---|---|---|---|---|
       | `ready_biodegradability_huang_zhang` (`ClassDataset_all`) | 6,139 chemicals, 6,137 structures, 34.9% RB | 5.8x the chemicals, 6.3x the scaffolds, the REACH-wide guideline mix, ambiguous chemicals kept | scaffold-grouped (no dates published) | the seven data files sit in Körner et al.'s GitHub repository (4 under `external_data`, 3 under `curated_data`), whose licence is GPL-3.0; the ACS article page refuses a command-line download (403) and the Internet Archive holds no snapshot of it, so this is the route that works; the records themselves come from ECHA's eChemPortal | repeat-test conflicts kept (4.2%); 1,546 rows with no CAS number; 100 structures shared between its two parts, 7 with opposite classes | better |
       | Körner et al. `Curated_SCS` (2024) | 5,185 chemicals | the same data with the identifiers repaired from the REACH export | scaffold-grouped | the same repository | a version of the candidate with 954 chemicals fewer | a choice inside the new record, not a dataset of its own |
       | Körner et al. `Curated_final` / `Curated_BIOWIN` | 4,298 / 3,784 chemicals | label-noise-filtered (their balanced accuracy 80.9% to 94.2%) | scaffold-grouped | the same repository | the hard cases are removed on purpose, by other models' predictions | not better |
       | OPERA `RBiodeg_QR` (US EPA; Mansouri et al.) | 1,603 QSAR-ready structures, 43.3% RB | 258 chemicals neither Mansouri sheet holds; DSSTox identifiers; the authors' train/test flag | the authors' flag, or scaffold-grouped | `OPERA_Data.zip` in the OPERA repository, open | holds 1,021 of our 1,055, and 1,444 of its own 1,603 sit inside the candidate; structures are salt-stripped, so a salt form is no longer the chemical the test used | not better |
       | `ready_biodegradability_mansouri_external` (the 670-chemical sheet, screened 2026-11-02) | 670 chemicals | the sibling candidate already on file | scaffold-grouped | the ACS workbook qsar_biodeg already downloads | 619 of its 670 structures are in the candidate | subsumed by the candidate |
       | NITE's CSCL workbook (the file the dating of 2026-11-11 used) | 1,373 test records on 1,363 chemicals | ~300 chemicals more than ours, with %BOD, the guideline and the test year | temporal or scaffold-grouped | open download from nite.go.jp | 73 structures do not parse; one programme and one guideline; the split by test year was weighed and dropped on 2026-11-12 | not better |
       | Körner's REACH export `iuclid_echa.csv` | 8,115 test records on 2,858 chemicals | the registrants' own verdict, including "readily biodegradable, but failing 10-day window" (505 records) | scaffold-grouped | the same repository | fewer than half the candidate's chemicals | not better |
       | Lunghini et al. 2020 "Global" set (3,146 compounds) | not obtained | a set larger than ours | - | the data is a publisher's supplementary file and the set mixes in one company's industrial data | smaller than the candidate | not available |
       | VEGA ready-biodegradability models (IRFMN) | - | - | - | the models are distributed, not a training table; their data is the same MITI collection | - | not better |
   * **Effect on the task:** none on the current definition until the candidate is accepted. On the recommended course the benchmark keeps the question, the use case, the single feature and the metric, and changes the data: 6,139 chemicals instead of 1,055, REACH screening results across the OECD 301 series instead of MITI's OECD 301C alone, and the ambiguous chemicals kept instead of removed, which lowers the scores and widens the gap between methods.
   * **Experiments:** Downloaded on 2026-11-25 into the run's evidence folder: `dl_koerner/` (the seven data files under `datasets/external_data/` and `datasets/curated_data/` of https://github.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals), `dl_iuclid/iuclid_echa.csv` (the REACH export in the same repository), `dl_opera/OPERA_Data.zip` (`RBiodeg_QR.sdf`, https://github.com/kmansouri/OPERA); qsar_biodeg from the workbook its definition downloads. Structures canonicalised with the pinned RDKit. Scores from one batch jobs (1411626): untuned LightGBM, a 300-tree random forest and logistic regression (median-imputed, standardised) on the recommended SMILES encoding, 3 x 10 scaffold-grouped folds, ROC AUC.

     - Counts and overlap with qsar_biodeg's 1,055 chemicals:

     | Data | Chemicals | RB | Of our 1,055 found | Same class | Distinct scaffolds |
     |---|---|---|---|---|---|
     | qsar_biodeg (as shipped) | 1,055 | 33.7% | - | - | 209 |
     | `ClassDataset_original` | 4,593 | 35.0% | 699 by structure, 745 by CAS | 669 / 717 | 1,079 |
     | `ClassDataset_external` | 1,546 | 34.7% | 254 by structure (it has no CAS) | 253 | - |
     | `ClassDataset_all` | 6,139 | 34.9% | 1,011 by structure or CAS (95.8%) | 976 | 1,308 |
     | Körner `Curated_SCS` | 5,185 | 34.6% | 759 by structure | 750 | - |
     | OPERA `RBiodeg_QR` | 1,603 | 43.3% | 1,021 by structure | 989 of 1,018 | - |

     On the union of the two keys, 1,011 of the 1,055 are found, 976 with the same class, 32 with the other class and 3 where the larger set itself holds both classes for the chemical; matching on the exact structure alone, 953 are found and 31 disagree, 20 readily biodegradable there and not here, 11 the other way. 202 of our 209 scaffolds (96.7%) are in the larger set, and our chemicals are 15.5% of it.

     - Baseline spread, 3 x 10 scaffold-grouped folds, ROC AUC (mean, sd over 30 folds):

     | Data | Chemicals | LightGBM | Random forest | Logistic | LightGBM - logistic |
     |---|---|---|---|---|---|
     | qsar_biodeg (as shipped) | 1,055 | 0.935 (0.026) | 0.937 (0.030) | 0.911 (0.036) | +0.025 |
     | `ClassDataset_original` | 4,590 | 0.878 (0.020) | 0.881 (0.020) | 0.790 (0.020) | +0.089 |
     | `ClassDataset_all` | 6,136 | 0.890 (0.016) | 0.893 (0.014) | 0.814 (0.024) | +0.076 |
     | Körner `Curated_SCS` | 5,185 | 0.904 (0.015) | 0.903 (0.017) | 0.812 (0.018) | +0.092 |
     | merged (`ClassDataset_all` + our 102, 31 conflicts dropped) | 6,207 | 0.893 (0.017) | 0.897 (0.018) | 0.818 (0.022) | +0.076 |

     - What each set knows about the other (one fit per cell, the same encoding and models):

     | Train | Test | LightGBM | Random forest | Logistic |
     |---|---|---|---|---|
     | the larger set without our 1,055 chemicals (5,183) | our 1,055 | 0.938 | 0.937 | 0.847 |
     | our 1,055 | the larger set without them (5,183) | 0.851 | 0.853 | 0.813 |

     Reading: trained on the 5,183 chemicals the larger set holds beyond ours, a model scores 0.938 on qsar_biodeg's own 1,055, as high as a model trained on qsar_biodeg under its own split (0.935); trained the other way round it reaches only 0.851 against 0.890 within the larger set. The first number is not scaffold-disjoint (120 of our 209 scaffolds appear in those 5,183 chemicals), which is itself the point: the larger set already carries this dataset's chemistry. Merging changes nothing measurable (0.893 against 0.890).

   * **Consistency:** polish_companies_bankruptcy takes the same decision in this batch (add the larger candidate, then retire the old record as replaced), and body_density_prediction and fiat_500 the same shape; all four follow the pattern that a better dataset for a task still done today is its own record and the old one keeps the verdict its own data earn until the curator decides[^better]. mic is the counter-case: there the larger candidate does not separate methods, so it is added next to the old one instead of replacing it - here the larger set separates them three times as far, which is why this one replaces.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | ships as defined; the pair stays open | nothing to change | the measurement the 2026-11-12 decision asked for is in, and it meets the condition that decision set for retiring this one |
     | B | Add `ready_biodegradability_huang_zhang` next to it, keep both | both ship once the candidate is accepted | no gap in the benchmark; two protocols for one property | one question twice, with 95.8% of the small one's chemicals inside the large one |
     | C | Keep until `ready_biodegradability_huang_zhang` is added, then retire it as replaced | ships as defined; once the candidate is accepted, `No (Retired)`, folder removed | the task stays in the benchmark meanwhile; the replacement is 5.8x larger, carries the same question and separates methods far more; it keeps the ambiguous chemicals this one removed | a second decision once the candidate is built; the labels come from many guidelines instead of one |
     | D | Replace by a merged set | one record of 6,207 chemicals: the candidate plus the 102 of ours it lacks, the 31 chemicals the two label differently dropped | nothing of this dataset is lost | one dataset from two compilations that disagree on 3.2% of the chemicals they share, which is the label noise the candidate's own literature documents; the 102 extra chemicals are 1.6% of the set |

   * **Recommendation:** C: the condition the decision of 2026-11-12 set is met on the measurement it asked for - the larger set holds 95.8% of these chemicals and agrees on the class for 96.5% of those it holds - and a model trained on its other 5,183 chemicals already scores 0.938 on this dataset's own 1,055, so this dataset adds nothing to it. The candidate carries the same question and use case on 5.8 times the chemistry, keeps the ambiguous chemicals this one removed, and separates methods three times as far. The task stays valid and this record keeps shipping until the candidate is built and accepted[^valid]; B leaves one question in the benchmark twice, and D buys 1.6% more chemicals at the price of joining two compilations that disagree on the chemicals they share, with no measurable gain. **Decision:** A, B, C or D?

   **Notes for the AI:** On C: a dated CC line in `qsar_biodeg`'s record recording the measurement (1,011 of 1,055 found on canonical SMILES or CAS-RN, 976 with the same class; scripts and outputs in the run's evidence folder) and the course "keep until `ready_biodegradability_huang_zhang` is accepted, then retire as replaced"; the Assessment of 2026-11-12 on that record and on the candidate's is then answered. When the candidate is accepted: `No (Retired)` with the reason "replaced by a larger set for the same task", folder removed, CHANGELOG entry. Build the candidate through `/add-dataset`: download `datasets/external_data/class_all.csv` (2,242,462 bytes) from `https://raw.githubusercontent.com/pkoerner6/Prediction-of-Aerobic-Biodegradability-of-Organic-Chemicals/main/datasets/external_data/class_all.csv` with a sha256 in `download_description` (keep `Huang_Zhang_RegressionDataset.xlsx`, 1,984,887 bytes, from the same folder if the record wants to rebuild the label or to document the test mix); keep `smiles` (canonicalised, declared `Smiles(column="SMILES")`) and `y_true` (1 -> `Yes`, 0 -> `No`, target `Biodegradable`); drop `name`, `name_type`, `source` and the `pka_*` and `α_*` columns, which Körner computed from the structure; `cas` is provenance only and is missing on the 1,546 literature rows. `grouping = Grouping(on="scaffold", ...)` from `scaffold_groups`, `Metric.fallback` (`roc_auc`), time basis `UnseenGroup`, no time column. Open choices for that record's own review, not for this item: `ClassDataset_all` (6,139) or Körner's `Curated_SCS` (5,185, identifiers repaired) as the version to ship, never `Curated_final` or `Curated_BIOWIN`, which drop the hard cases on purpose; what to do with the 145 pairs that are one chemical once stereochemistry is set aside (15 with conflicting classes) and the 22 repeated CAS numbers (6 with conflicting classes); and whether to fold in the 102 chemicals of `qsar_biodeg` the set lacks. Correct the candidate's screening record where this check contradicts it: `ClassDataset_original` is 4,593 chemicals and `ClassDataset_all` 6,139 (the 6,139 is the two parts together, not the original alone); the regression file is 12,750 records on 6,102 CAS numbers; the files are reachable and were downloaded. On B: both ship; the candidate's record names the 1,011 shared chemicals and `qsar_biodeg`'s record a line that a 5.8x set with 95.8% of its chemicals also ships. On D: one record from `class_all` plus the 102 chemicals of `qsar_biodeg` it lacks, the 31 chemicals the two label differently dropped (6,207 rows), the double provenance stated in `curation_comments`; `qsar_biodeg` then retires as its duplicate. On A: nothing to do beyond a CC line recording the measurement.

   [^better]: selection.md, pattern "Small or dated, and the task is still done today": a larger or newer public dataset with the same target and use case, and features of the same kind, is its own record and not a `Duplicate`; the old record is not rejected automatically and keeps the verdict its own data earn until the curator decides. PROV-4 (Must): two records are duplicates only when they end at the same original source - this one ends at NITE/MITI through Mansouri et al., the candidate at REACH dossiers and the literature, so on C this record retires as replaced, not as a `Duplicate`. PROV-6 (Must): versions or cuts of one underlying dataset are duplicates when neither adds a distinct task, which is why Körner's curated files are a choice inside the candidate's record rather than records of their own.
   [^valid]: TP-6 (Must): keep two questions apart, is the task valid and is it the best version; a valid task stays until the better version is actually there.
   [^smiles]: CLEAN-24 (Should, as amended): a molecule's structure ships as a SMILES column marked as a structure, never pre-encoded; the recommended encoding is RDKit's 2D descriptors, the 166 MACCS keys and the ECFP4 counts. SPLIT-31 (Should, as amended): a molecule dataset whose rows carry exact structures groups on the Bemis-Murcko scaffold, since a new chemical under assessment often comes from a series not yet measured.

   **Andrej (2026-11-26, verdict dont):** retire, replaced by ready_biodegradability_huang_zhang. Huang-Zhang contains
   1,011 of its 1,055 chemicals and gives 976 of them the same class. It has 5.8× the chemistry and separates methods
   three times as far.

   **Resolved (2026-11-26, Andrej):** C, its condition met: `ready_biodegradability_huang_zhang` is added and
   accepted, and the measurement the decision of 2026-11-12 asked for (issue 1, B) came out as that decision's
   condition named it - the larger set holds 1,011 of these 1,055 chemicals (95.8% on canonical SMILES or CAS-RN) and
   gives 976 of them the same class. So this dataset is retired as replaced: `suggestion: No (Retired)`, marker
   `Duplicate` (the curator's reading that each set is a cut of the same underlying registry data as the other,
   PROV-6, where this issue's footnote had read PROV-4 the other way), priority removed, the folder removed from the
   working copy and `v2_path` cleared; `data_foundry_status`, the claim and this review stay. The replacement carries
   the same question, use case, single feature (the structure as a SMILES), scaffold-grouped split and `roc_auc`
   fallback on 6,139 chemicals and 1,308 scaffolds against 1,055 and 209, keeps the ambiguous chemicals Mansouri's
   curation removed, and separates methods three times as far (untuned LightGBM over a linear model +0.076 ROC AUC
   against +0.025 here); a model trained on its other 5,183 chemicals already scores 0.938 on these 1,055.

## Reference

Mansouri, K., Ringsted, T., Ballabio, D., Todeschini, R., Consonni, V. (2013). Quantitative Structure - Activity Relationship models for ready biodegradability of chemicals. Journal of Chemical Information and Modeling, 53, 867-878
