---
unique_name: qsar_fish_toxicity
name: QSAR_fish_toxicity
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
year: '2015'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=44970
- https://doi.org/10.24432/C5JG7B
notebook_path: datasets/beyond_iid/old_iid/qsar_fish_toxicity/qsar_fish_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_fish_toxicity/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

related to other (Meta)QSAR datasets? autocorrelation and matrix-based descriptions

Lennart: seems real, distinict from other QSAR data

Andrej: Seems fine

**Assessment (AI, 2026-10-14):** no leak found, so the remark "might have a leak" is removed (Lennart's ask). All six descriptors are computed from the structure; the strongest (MLOGP, R² 0.42 alone) is the known link of logP to baseline toxicity. The 84 shared descriptor vectors (217 rows) are isomers whose LC50 differs within every vector; keeping one row per vector gives R² 0.571 against 0.577. The descriptors were selected on the paper's training set (726 of 908 chemicals): a mild optimism that cannot be measured.

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Cassotti et al. 2015 report R2/Q2 with RMSE on training and external sets; rmse is the regression fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `adore_aquatic_toxicity` (TBD -> Yes, priority 3), `aquatic_toxicity_lunghini_consensus` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): go ahead for the structure-recoverable datasets: ship the SMILES only, as for qsar_tid_11. The authors' descriptors are one modelling choice; the benchmark encodes the structure.

**Assessment (AI, 2026-11-01):** the structures are recoverable and the link is exact. The authors' own workbook (Milano Chemometrics, `toxicity_data_fish.xlsx`) holds the same 908 rows in the same order as the UCI file, with CAS-RN, SMILES, their train/test split, LC50 and the same 6 descriptors; all 6 are identical on every row. The 6 descriptors leave, which also settles the mild optimism they carried (a genetic algorithm chose them on 726 chemicals that overlap our test folds, LEAK-31). The target now comes from the workbook at full precision: the UCI file rounds LC50 to 3 decimals (every row differs by at most 0.0005). `SMILES` is the one feature; the split is scaffold-grouped (786 groups). The 24% of rows that shared a descriptor vector have distinct structures. Task probes, 30 splits: LightGBM R^2 0.640, random forest 0.614, no flags.

CC (2026-11-02, Lennart): on the target's precision, carried to the curator in the handover document as a change
that was not an instruction: "the changes look good". LC50 comes from the authors' own workbook at full precision
instead of the UCI file's three decimals; every row moves by at most 0.0005, and the workbook is the table the
structures come from anyway.

CC (2026-11-02, Lennart): on how the Milano workbook was downloaded ("freeware with proper reference", fetched
through a public link rather than the authors' notification form): "that is okay for now, we can note it but it is
not blocking us here". Noted here; regularise before this ships outside the group.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: a regulator's real toxicity task that now ships the structure with held-out series and separates methods; the overlap with qsar_aquatic_toxicity and the larger ADORE/Lunghini sets is a keep-and-settle question, not a validity problem. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-12, Andrej): collection facts `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension` (Review issue 4): ECOTOX's earliest fathead minnow 96-hour LC50 test dates 850 of 908 chemicals (93.6%), 1956 to 2005. The facts describe the source and do not change with the split, which stays as it is.

CC (2026-11-11, Andrej): kept next to `qsar_aquatic_toxicity` with the overlap written into both definitions (the decision is recorded as issue 1 of `qsar_aquatic_toxicity`).
- Counted by structure, from the two authors' workbooks rather than the earlier MLOGP estimate: 237 chemicals are in both, 26.1% of this set and 43.4% of the Daphnia set, 225 of them under the same CAS-RN.
- Their LC50s correlate at r = 0.81 (Spearman 0.82), the Daphnia values 0.37 log units more toxic on average.
- The species, the exposure time and the endpoint differ, so the two are different tasks of one study design, not duplicates; a method that suits the design gains on both.

CC (2026-11-12, Andrej): the fit stays direct, the scaffold split's time basis is `Timeless`, and `problem_type` is filled (Review issues 2 and 3, record field); the input data did not change:
- Fit (issue 2, A): whole chemical series are held out and the authors' selected descriptors have left, as for qsar_bioconcentration, so the open proposal to read the fit as approximate (2026-10-26) is closed as superseded. Under the shipped scaffold splits 12.4% of the test chemicals have a close training analog (Tanimoto similarity of the structure fingerprints 0.7 or more), under random splits of the same rows 13.1%.
- Time basis (issue 3, reply a): `Timeless`, since a chemical's 96-hour LC50 for the fathead minnow is a property of the chemical. Dated through the EPA's ECOTOX database by CAS-RN, 850 of 908 chemicals (93.6%) were first tested between 1956 and 2005, 90% by 1990; the LC50 barely moves with the year (Spearman -0.06), and a forward split by first test year is no stricter than holding out series (RMSE 0.970 against 0.970, untuned LightGBM). The `Time basis:` line and the dating table are in the definition; the tag itself enters the definition's tags once the time-basis tags (PR #50) are in.
- `problem_type`: `Regression`, the definition's (the record had none).

CC (2026-11-12, Andrej): kept, and settled against a larger fish set once one is added (Review issue 1, B).
- Next to `qsar_aquatic_toxicity` it stays, as decided on 2026-11-11 (different species, exposure time and endpoint; 237 shared chemicals named in both definitions).
- ADORE (`adore_aquatic_toxicity`) and the Lunghini set (`aquatic_toxicity_lunghini_consensus`) are judged in their own records; when one is added, its fathead-minnow 96-hour entries are matched to these 908 chemicals on canonical SMILES and CAS-RN, and the share it holds and the agreement of the LC50 decide whether this dataset stays.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of `Timeless`:
- The use case predicts for items the catalogue does not hold, which the held-out scaffolds stand for; that the entry date carries no wave is a measurement for the `Time basis:` line, not a different use case.
- `Timeless` now means a fixed target in data with no time dimension. The split does not change.

## Review

**Outcome:** added. The 96-hour LC50 (the concentration that kills half the fish, as minus the log of mol/L) of 908
chemicals for the fathead minnow, compiled by Cassotti et al. (2015, SAR and QSAR in Environmental Research
26(3):217-243, https://doi.org/10.1080/1062936X.2015.1018938; UCI https://doi.org/10.24432/C5JG7B). Since 2026-11-01
the structure ships as a SMILES from the authors' own workbook (the same rows in the same order) in place of their six
descriptors, the target comes from the workbook at full precision, and whole chemical series (Bemis-Murcko scaffolds,
786 groups) are held out; RMSE is the fallback metric. The AI recommends shipping it. Reviewed on 2026-11-04 without a
panel, from the gathered evidence (the record, Andrej's review of 2026-10-15, the CHANGELOG, model runs on
the shipped data and on TabArena v0.1's copy); Andrej disputes Lennart's `Yes` (issue 1). Validity: a measured outcome
of a standard test, the question a regulatory toxicologist asks of an untested chemical; the descriptors a genetic
algorithm chose on 726 of the chemicals, the one leak concern, have left. Value: the task probes on the v0.2 frame
give R^2 0.640 (LightGBM) and 0.614 (random forest), no flags; on the shipped data (descriptors, random splits) the 40
benchmark methods spread from RMSE 0.845 (TabPFN 3.5) to 0.947 (linear models), median 0.874, and an
earlier check had TabPFN 3.5 ahead of extra trees on 30 of 30 splits. Quality: no two rows are the same chemical; the
24% of rows that shared all six descriptors are distinct isomers, now told apart by their structures. Weighed: a
regulator's real task with structures and held-out series +, methods separate +, a near-sibling in the benchmark
(qsar_aquatic_toxicity) and larger fish sets screened -.

**Main points:** Nothing open. Settled 2026-11-12: kept next to qsar_aquatic_toxicity, to be settled against ADORE or
the Lunghini set once one is added (issue 1, B); the fit stays direct (issue 2, A), the scaffold split's time basis is `Timeless`
with the ECOTOX dating written down (issue 3, a), collection facts `Samples: Over Time`, `Time: Dated` (issue 4), and
the record's `problem_type` is `Regression`.

**Record judgment:** valid. The record carries the v0.2 changes (CC and Assessment of 2026-11-01 and 2026-11-02);
Andrej's dispute of 2026-10-15 is not on the record. The workbook was fetched through a public link rather than the
authors' notification form ("freeware ... if proper reference is given"); Lennart: noted, not blocking, to regularise
before shipping outside the group.

**Issues for Andrej:**

1. **Keep this dataset next to qsar_aquatic_toxicity, and with larger fish sets screened?**

   * **Problem:**
     - Andrej disputes Lennart's `Yes`, mainly because about 150 of its chemicals are also in qsar_aquatic_toxicity,
       a sibling of the same Milano group, and because its features were the authors' selected descriptors, which v0.2
       has replaced by the structure.
     - Two larger sets for the same endpoint are screened `TBD -> Yes` but not added: ADORE (2023, fish LC50 of
       1,905 chemicals from US EPA ECOTOX) and the Lunghini consensus set (2020, 3,680 compounds).
     - Keep it now and settle it when a larger set is added, keep it for good, or retire it now?
   * **Background:** the two Milano datasets draw on the same databases (ECOTOX, EAT5, OASIS) for two species: this
     one the fathead minnow at 96 hours, qsar_aquatic_toxicity the water flea Daphnia magna at 48 hours. Records with a
     shared source and different tasks are not duplicates[^1a]; another compilation of the same endpoint is its own
     record and does not retire this one by itself[^1b].
   * **Experiments:** an earlier check (2026-10-15, UCI files without identifiers): 201 values of the logP descriptor
     MLOGP occur in both files against at most 57 after shifting the values (a chance baseline), so about 145 to 165
     chemicals are shared; on 89 one-to-one matches the two LC50s correlate at r = 0.75; seven models rank in nearly
     the same order on both (Spearman 0.89). Against the dispute: TabPFN 3.5 RMSE 0.856 against extra trees 0.905
     (ahead on 30 of 30 splits) and a linear model 0.956; the authors' held-out test R^2 of 0.65 matched the
     cross-validation, so the descriptor selection had added little optimism.
   * **Unknown:** the exact overlap with qsar_aquatic_toxicity and with ADORE: both workbooks carry CAS numbers and
     structures, so it can be counted on them, and against ADORE when that set is added.
   * **Consistency:** qsar_aquatic_toxicity issue 1 asks the same pair question from the other side and recommends
     keeping both; if one of the two goes, that one is the smaller Daphnia set. The same keep-and-settle option is
     proposed for qsar_biodeg (issue 1).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 908 chemicals, SMILES, scaffold split; the larger sets judged on their own | a regulator's real task; methods separate; the larger of the Milano pair and in TabArena v0.1 | the Milano design counts twice while qsar_aquatic_toxicity stays |
     | B | Keep, settle against ADORE or Lunghini when one is added | as A, plus a note to count the shared chemicals then and retire this one if the larger set holds most of them | no gap until a larger set ships; the duplicate question is decided on data | a second decision later |
     | C | Retire now | the folder goes, the record gets `No` | the Milano design counts once (if qsar_aquatic_toxicity stays) | a valid task with clear separation of methods leaves[^1c] |

   * **Recommendation:** B: the task is valid and separates methods; whether it duplicates a larger fish set can be
     counted once that set is in. **Decision:** keep (A), keep and settle with a larger set (B), or retire (C)?

   **Notes for the AI:** on B, an Assessment line here and in `adore_aquatic_toxicity` and
   `aquatic_toxicity_lunghini_consensus`: on adding, match the fathead-minnow 96-h entries on canonical SMILES and
   CAS-RN and report the share of these 908 chemicals and the agreement of their LC50. Decide together with
   qsar_aquatic_toxicity issue 1.

   [^1a]: **PROV-7** (Must): records that share a source but give different tasks are not duplicates.
   [^1b]: selection.md, "Small or dated, and the task is still done today": a hit from another source is its own
     record; the old record keeps the verdict its own data earns. **PROV-6** (Must): versions or cuts of one
     underlying dataset are duplicates when neither adds a distinct task.
   [^1c]: **TP-6** (Must): a valid task stays; whether it is the best version is a separate question.

   **Resolved (2026-11-12, Andrej):** B (`ok`): kept next to qsar_aquatic_toxicity, as the record's decision of
   2026-11-11 on that pair already says (keep both; the 237 shared chemicals are named in both definitions). ADORE
   (`adore_aquatic_toxicity`) and the Lunghini set (`aquatic_toxicity_lunghini_consensus`) are judged on their own;
   when one is added, its fathead-minnow 96-hour entries are matched to these 908 chemicals on canonical SMILES and
   CAS-RN, and this dataset is settled against it on the share it holds and the agreement of the LC50. `dataset.py`
   unchanged; CC line in the record.

2. **Close the open question of the use-case fit as direct, now that whole series are held out?**

   * **Problem:**
     - The curation rules hold an open proposal for this dataset and qsar_aquatic_toxicity: their fit read direct
       while random tested chemicals were the test rows, the setting in which qsar_oral_toxicity reads approximate.
     - v0.2 holds out whole chemical series and the selected descriptors have left, the setting in which
       qsar_bioconcentration reads direct.
     - Keep direct and close the proposal, or set approximate?
   * **Background:** the proposal (2026-10-26) asked for approximate as qsar_oral_toxicity, or direct with the gap
     recorded, and for the kept descriptor leak to be named in `fit_reason`[^2a]. Both of its premises are gone: the
     split holds out scaffolds and no selected descriptor ships. qsar_oral_toxicity reads approximate because its
     screening is simulated (its test chemicals have more close analogues than the project's untested ones), a fact
     this dataset does not share.
   * **Unknown:** the share of test chemicals with a close training analogue (Tanimoto 0.7 or more) under the scaffold
     split, which the other molecule sets report (qsar_bioconcentration 6.4%, qsar_oral_toxicity 16.3%); it needs
     the workbook, which is not in this checkout.
   * **Consistency:** follows qsar_bioconcentration (direct: held out by scaffold, the authors' selected descriptors
     dropped, 2026-10-26, Lennart).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Direct (implemented) | `fit="direct"`; the open proposal closed as superseded by the scaffold split | as qsar_bioconcentration; the structure is all an assessor has for an untested chemical | the analogue share is not yet measured |
     | B | Approximate | `fit="approximate"`, `fit_reason` names the curated compilation | the most cautious reading | no gap found that sets it apart from qsar_bioconcentration |

   * **Recommendation:** A: the reasons for the proposal have gone with the v0.2 changes. **Decision:** direct (A) or
     approximate (B)?

   **Notes for the AI:** on A, mark the USE-8 Cases row for qsar_fish_toxicity and qsar_aquatic_toxicity in
   use_case.md as superseded (scaffold split and SMILES of 2026-11-01) and, when the workbook is at hand, add the
   analogue shares to `curation_comments` and molecules.md's table.

   [^2a]: **USE-8** (Must): write how closely the data mirrors the use case; the Cases row for qsar_fish_toxicity and
     qsar_aquatic_toxicity is `proposed`, open for the curator.

   **Resolved (2026-11-12, Andrej):** A: direct. `fit="direct"` stays; a curation bullet closes the open proposal as
   superseded and gives the analogue shares, measured on the authors' workbook (Tanimoto 0.7 or more, Morgan radius 2,
   2,048 bits, 10 x 3 splits each):

   | Split | Test chemicals with a close training analog |
   |---|---|
   | Shipped scaffold splits | 12.4% (9.4-16.5% per split) |
   | Random 3-fold, same rows | 13.1% |

   The USE-8 Cases row in use_case.md is marked superseded, and molecules.md's table has a qsar_fish_toxicity row. CC
   line in the record.

3. **Time basis: name the scaffold split `Timeless`?**

   * **Problem:**
     - Each row is a chemical with a 96-hour LC50 for the fathead minnow, from laboratory tests that the source
       databases (ECOTOX, EAT5, OASIS) gathered over many years and the Milano group compiled in 2015; the release
       keeps no test date, and the only feature is the structure, which exists before any test.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits a catalogue of
       properties; the split holds out whole scaffolds and names no time basis yet.
     - A chemical's toxicity to one species at one exposure time is a fixed property of the chemical, the case the
       `Timeless` prototype names[^3a].
   * **Background:** the tested chemicals were not drawn at one time: which chemicals get tested changes with
     regulation and industry, and a new chemical under assessment often comes from a series not yet tested, which the
     scaffold split stands for. A split by test year would test the newest chemistry directly, but no date ships;
     ECOTOX records a publication year per test and could be joined on the CAS number in the authors' workbook, which
     is not on this machine. The overlap with qsar_aquatic_toxicity (issue 1) is no time question.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Scaffold split, `Timeless` | as now; the tag and a `Time basis:` line naming the property and the undated compilation | states the fact the split rests on; as the other molecule sets | the order in which chemicals were tested stays unmeasured |

   * **Recommendation:** B: toxicity is a property of the chemical, and the series split stands for new chemistry.
     **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: a chemical's 96-hour LC50 for the fathead minnow is a property of the
   chemical; the tests were compiled from databases in 2015 without dates, and whole scaffolds are held out for new
   series.`, `splits_comment` unchanged; `dataset check`.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family. **SPLIT-31** (Should): a molecule dataset with exact structures groups on the Bemis-Murcko
     scaffold.

   **Answer (AI, 2026-11-06):** Held back from the bulk mark: date the chemicals through ECOTOX first (a), name the
   scaffold split forced from temporal now (b), or `Timeless` as drafted (c)?

   * **Problem:**
     - You accepted two items: a catalogue whose population or feature meaning moves with time counts as samples over
       time, and screening asks which identifier a parent source could date the items by, "none published" being an
       answer too; the bulk `Timeless` item had named this dataset as one that moves if the first is accepted[^3q].
     - The release the definition reads carries an identifier: the authors' workbook gives each of the 908 chemicals its
       CAS-RN and SMILES (the definition's notes); ECOTOX, the main source database, keeps the publication year of every
       test, found by CAS-RN. The workbook is not in this machine's warehouse now.
     - Which chemicals get tested moves with regulation and industry, so a scaffold fold may train on a test chemical's
       same-period series, as the ChEMBL years showed for qsar_tid_11.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Date through ECOTOX, then decide | each CAS-RN joined to its earliest fathead minnow 96-hour LC50 test in ECOTOX; label, close analogs and a split by year measured as in qsar_tid_11 issue 2; then `Timeless`, windows by year or the forced tag | decides on a measurement; one join serves qsar_aquatic_toxicity too | ECOTOX's bulk file and the workbook (behind a form) to fetch; tests from EAT5 and OASIS stay undated |
     | b | Scaffold split, `ForcedGroupedFromTemporal` | the tag and a `Time basis:` line: tests over decades, no date in the release, likely drift in which chemical classes were tested; a dated release would test the newest classes | no join | gives up a date the CAS-RN can recover |
     | c | Scaffold split, `Timeless` (B as drafted) | the drafted tag and line | nothing to measure | assumes no drift, which the accepted item asks to check |

   * **Recommendation:** a, as qsar_tid_11 did with ChEMBL. **Decision:** a, b or c?

   [^3q]: **SPLIT-32** (Should; the items of 2026-11-06): question 1 also asks whether the use case meets items drawn
     like the catalogue's; a catalogue whose items enter in eras, or whose features mean something different by when an
     item was made, arose over time; which identifier a parent source could date the items by tells whether it drifts.
     Case: qsar_tid_11 issue 2, dated through ChEMBL.

   **Andrej (2026-11-11, discuss):** Reply (a): Date through ECOTOX, then decide

   **Answer (AI, 2026-11-11):** the dating is running; this turn records the decision, and the measurement follows.

   **Answer (AI, 2026-11-11):** dated, 850 of 908 (93.6%). A forward split is no stricter than the shipped scaffold
   split, and the grouping, not the time, is what holds a test chemical away from training.

   * **The dating:** the EPA's ECOTOX bulk release (`ecotox_ascii_09_15_2026`, gaftp.epa.gov), joined on CAS to the
     fathead minnow 96-hour LC50 records; the year is the publication year of the earliest matching test, 1956 to
     2005, median 1984 and 90% by 1990.
   * **Check on the join:** where ECOTOX reports the LC50 in mg/L, its median value per chemical converted to
     -log10(mol/L) matches the workbook target at r = 0.923 on 212 chemicals, median difference 0.02 log units, 95.3%
     within one log; so the join finds the right chemical and the right endpoint.
   * **The split, three expanding windows by first test year against the scaffold folds** (untuned LightGBM / random
     forest, `encode_smiles`, RMSE, every training side at least half the dated chemicals; Slurm 1378105):

     | Scheme | RMSE, LightGBM / RF | Close training analog | Test scaffold in training |
     |---|---|---|---|
     | T, forward by year | 0.970 / 0.974 | 7.2% | 15-18% |
     | S, scaffold-disjoint | 0.970 / 0.978 | 5.9% | 0 |
     | R, random | 0.941 / 0.941 | 6.9% | 15-20% |
     | Shipped scaffold folds, all rows | 0.872 / 0.848 | 12.0% | 0 |

     - A forward split still leaves 15 to 18% of the test chemicals a scaffold the model has seen; the scaffold split
       removes all of them.
     - The spread between windows (0.81 to 1.17) is far larger than the spread between schemes, so which chemicals
       fall in a window matters more than how they were chosen.
   * **Drift:** the target barely moves with the year (Spearman -0.06 between first year and LC50), and the authors'
     own train/test share is flat across periods (0.78 to 0.88), so their random split carries no time structure.
   * **What it means for the time basis:** the dates are old and concentrated, a catalogue of historic laboratory
     tests rather than a stream, and the relation to the structure does not move with the year; `Timeless` now rests
     on a measurement rather than on an assumption[^3t].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Scaffold split (implemented), `Timeless`, the dating written down | the tag, a `Time basis:` line and the table above in the notes | the split holds out more than a forward one does; the drift is measured, not assumed | the 58 undated chemicals stay unexamined |
     | b | Temporal split by first test year | three windows, the scaffold grouping dropped | follows the order the tests were run in | a publication year is an upper bound on the test date; it leaves scaffolds in training that the shipped split removes |
     | c | Scaffold split, no prototype tag, the dating written down | the table in the notes, no tag claimed | makes no claim beyond the measurement | leaves the definition without a stated time basis |

   * **Recommendation:** a: the use case screens an untested chemical from its structure, the catalogue is historic
     and the relation is flat across periods, which is what `Timeless` asserts and what the dating now shows.
     **Decision:** a, b or c?

   **Notes for the AI:** on a, `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`), a `Time basis:`
   bullet naming the historic compilation, the 93.6% coverage, the flat relation and what the split cannot test (a
   chemistry later than the 1990s); keep the table.

   [^3t]: **SPLIT-32** (Should): `Timeless` when the target is a fixed property of the item and the use case meets items
     drawn like the catalogue's; which identifier a parent source could date the items by tells whether the catalogue
     drifts, and a catalogue that drifts goes on to the question whether arrival affects the target. **SPLIT-34**
     (Should): the family key is the default, and the source's stated aim and scope decide which items the test set
     stands for; within that scope the entry date replaces it when the use case predicts for items the catalogue does
     not hold yet, the date is when the item entered, the labels are final, and either arrival changes how the target or
     the features are recorded, or which items are selected (as SPLIT-32's question 4 asks), or a forward split leaves
     the test items clearly fewer close training neighbours than a random draw; otherwise the family key stands and the
     time basis says why. Here the forward split leaves 7.2% of the test chemicals a close training analog against 6.9%
     for a random draw (the table above).

   **Andrej (2026-11-12, discuss):** Reply (a): Scaffold split, Timeless, the dating written down

   **Resolved (2026-11-12, Andrej):** a: the scaffold split stays, with a `- Time basis: Timeless: ...` bullet in the
   curation notes that names the historic compilation, the ECOTOX dating (850 of 908 chemicals, 93.6%, 1956 to 2005),
   the join check, the flat relation (Spearman -0.06) and the table above, and ends with what the split cannot test
   (chemistry newer than the 1990s, the 58 undated chemicals). The `Timeless` tag enters `data_tags` once PR #50 is in
   the working copy. CC line in the record.

4. **Collection facts: `Samples: Over Time` and `Time: Dated`, since a source dates the items?**

   * **Problem:** the record carries `Samples: No Time Dimension`, while ECOTOX's earliest fathead minnow 96-hour LC50
     test dates 850 of 908 chemicals (93.6%), 1956 to 2005. The facts describe the source and do not change with the
     split; whether the date carries anything belongs to the time-basis question (issue 3, open)[^4a].
   * **Change:** `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension`; the data, the split
     and the score are unchanged.

   [^4a]: **SPLIT-32** (Should): the collection facts are read from the source and do not change with the split; a
     catalogue that a parent source dates is `Samples: Over Time` with `Time: Dated` even where the date turns out to
     carry nothing, and whether it does is measured for the time basis.

   **Resolved (2026-11-12, Andrej):** applied on approval of the plan that settled the split keys of growing catalogues
   (one decision for the eighteen datasets of that review): the record's facts changed, with a CC line and `Andrej` in
   `checked_by`. No definition change.

## Reference

Cassotti, Matteo, et al. "A similarity-based QSAR model for predicting acute toxicity towards the fathead minnow (Pimephales promelas)." SAR and QSAR in Environmental Research 26.3 (2015): 217-243.

CC (2026-11-11, Andrej): kept next to `qsar_aquatic_toxicity` with the overlap written into both definitions (the decision is recorded as issue 1 of `qsar_aquatic_toxicity`).
- Counted by structure, from the two authors' workbooks rather than the earlier MLOGP estimate: 237 chemicals are in both, 26.1% of this set and 43.4% of the Daphnia set, 225 of them under the same CAS-RN.
- Their LC50s correlate at r = 0.81 (Spearman 0.82), the Daphnia values 0.37 log units more toxic on average.
- The species, the exposure time and the endpoint differ, so the two are different tasks of one study design, not duplicates; a method that suits the design gains on both.
