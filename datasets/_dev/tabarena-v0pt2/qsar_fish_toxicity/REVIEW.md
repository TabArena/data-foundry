# qsar_fish_toxicity

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

**Main points:** Keep this dataset next to qsar_aquatic_toxicity and settle it against the larger fish sets once one is
added (issue 1)? Close the open fit question as direct (issue 2)? The time basis of the scaffold split, held back from
the bulk `Timeless` mark: date the chemicals through ECOTOX by their CAS-RN first (issue 3, answer of 2026-11-06)?

**Record fields that disagree with the definition:**

- `problem_type`: record `None`, definition `Regression`.

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
   chemistry later than the 1990s); keep the table. Evidence and scripts in `~/claude_jobs/qsar_ecotox/`.

   [^3t]: **SPLIT-32** (Should): `Timeless` when the target is a fixed property of the item and the use case meets
     items drawn like the catalogue's; which identifier a parent source could date the items by tells whether the
     catalogue drifts, and a catalogue that drifts goes on to the question whether arrival affects the target.
