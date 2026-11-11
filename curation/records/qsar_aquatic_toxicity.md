---
unique_name: qsar_aquatic_toxicity
name: qsar_aquatic_toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
tags:
- Tiny Data
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
collections:
- TabArena Reject
original_source: UCI
year: '2014'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5SG7H
notebook_path: datasets/beyond_iid/new_iid/qsar_aquatic_toxicity/qsar_aquatic_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_aquatic_toxicity/dataset.py
source_row: 3
type_adapter_id: curation-record-v1
---

## Comments

CC: "546 samples, too small for 3-fold CV. 

Same data source / type of study as for QSAR_fish_toxicity (10.24432/C5JG7B)

predict acute aquatic toxicity towards the fish Pimephales promelas (fathead minnow) on a set of 908 chemicals."

Check if any of the qsar fish datasets are used in tabaren already

Other version in TabArena "QSAR_fish_toxicity"

Generally fine to add, but we need to decide whether we allow two datasets that similar in the benchmark

**Assessment (AI, 2026-10-14):** the quoted sentence about the fathead minnow and 908 chemicals is UCI's summary of QSAR fish toxicity (UCI 504), pasted by mistake into the summary of this dataset (UCI 505). This dataset is 546 chemicals with the 48-hour LC50 for Daphnia magna, a regression target (UCI 505 abstract; Cassotti et al. 2014).

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): ok on the follow-up item: a strong kept leak does not make the fit approximate (USE-8 amended); the kept leak is named in `fit_reason` as kept, not as a gap.

**Assessment (AI, 2026-10-21):** fit set to `direct`; the authors' selection of the eight descriptors by their fit to the toxicity is named in `fit_reason` as a kept potential leak.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Cassotti et al. (2014) report Q2 with RMSE, no single task metric; r2 and rmse rank models the same within a fold.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 2: gap -, use case +, source +, shape -, risk - (a near-copy of qsar_fish_toxicity; a kept selection leak).
**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `adore_aquatic_toxicity` (TBD -> Yes, priority 3), `aquatic_toxicity_lunghini_consensus` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): go ahead for the structure-recoverable datasets: ship the SMILES only, as for qsar_tid_11. The authors' descriptors are one modelling choice; the benchmark encodes the structure.

**Assessment (AI, 2026-11-01):** the structures are recoverable and the link is exact. The authors' own workbook (Milano Chemometrics, `toxicity_data.xlsx`) holds the same 546 rows in the same order as the UCI file, with CAS-RN, SMILES, their train/test split, LC50 and the same 8 descriptors; all 8 and LC50 are identical on every row. The 8 descriptors leave, which settles the kept potential leak the record named: a genetic algorithm chose them by their fit to the measured toxicity of chemicals in our test folds (LEAK-31), and no such selection reaches the features now. `SMILES` is the one feature; the split is scaffold-grouped (463 groups). Task probes, 30 splits: LightGBM R^2 0.573, random forest 0.548, no flags.

CC (2026-11-02, Lennart): on how the Milano workbook the structures come from was downloaded ("freeware with proper
reference", fetched through a public link rather than the authors' notification form): "that is okay for now, we can
note it but it is not blocking us here". Noted here; regularise before this ships outside the group.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Keep with a note on its overlap with qsar_fish_toxicity: a different task (species, exposure time) of the same Milano design, now shipping the recovered structures with a scaffold split, so the old selection leak is gone; Andrej's redundancy dispute (issue 1) is the open call. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): keep both, note the overlap (BeyondArena v0.2 review page, issue 1, B; disagreement settled, `Yes`): a sibling of qsar_fish_toxicity from the same group, databases and pipeline, but another species (Daphnia magna, not the fathead minnow) and exposure time (48 h, not 96 h), so a different task (PROV-7). The overlap is in `curation_comments`: about 145 to 165 shared chemicals, estimated from matching MLOGP values, LC50s correlated at r = 0.75 on 89 one-to-one matches. The count by structure waits for the two authors' workbooks, which are not on this machine.

## Review

**Outcome:** added. The 48-hour LC50 (the concentration that kills or immobilises half the animals) of 546 chemicals
for the water flea Daphnia magna (Cassotti et al. 2014, UCI 505, https://doi.org/10.24432/C5SG7H). Since 2026-11-01
each chemical's structure, from the authors' own workbook (the same 546 rows in the same order), is the one feature,
as a SMILES string, and the split holds out whole chemical series (Bemis-Murcko scaffolds, 463 groups). Reviewed
without a panel, from the gathered evidence (the record, Andrej's review of 2026-10-15, the earlier experiments, a
model run on the shipped data). The record reads `Yes (Disagreement)`: Andrej disputes Lennart's keep as
redundant with qsar_fish_toxicity (issue 1); the AI recommends keeping it with a note on the overlap. Validity: a
chemist or regulator estimating acute toxicity before or instead of an animal test, a direct fit; the authors' 8
descriptors, chosen by a genetic algorithm on the toxicity of chemicals that sit in our test folds, left with the
structure recovery, so the kept selection leak of the earlier review is gone; the labels pool laboratories, clones and
two endpoints (death and immobilisation). Value: on the scaffold splits with the recommended encoding, LightGBM R^2
0.573 and random forest 0.548 (30 splits, no probe flag); on the shipped data (8 descriptors, random splits) the 40
benchmark methods span RMSE 1.03 (TabPFN 3.5) to 1.29 (linear model), median 1.08, and a hand-written narcosis model
(toxicity rising with fat solubility, plus offsets for polar groups) is as good as the best, so the task is close to
classic QSAR but not to one feature (fat solubility alone R^2 0.28 against 0.60 for TabPFN 3.5 in an earlier check).
Quality: the rows are the authors' own workbook, 546 chemicals with one structure each, all 546 distinct and none
missing, in a canonical form, and what the labels pool is written into the curation notes.
Weighed: a real regulatory task and an exact structure link +, models separate +, a sibling of qsar_fish_toxicity
from the same group and pipeline -, larger open sets for the same endpoint found on 2026-10-31 -, 546 chemicals -.

**Main points:** kept next to qsar_fish_toxicity with a note on the overlap (issue 1, B, resolved 2026-11-11;
the count by structure waits for the workbooks). Open: the time basis of the scaffold split, date the chemicals
through ECOTOX by their CAS-RN first (issue 2, answer of 2026-11-06)?

**Record judgment:** valid and current to 2026-11-02: the fish dataset's summary sentence pasted by mistake is
corrected (2026-10-14), the kept selection leak named on 2026-10-21 left with the descriptors on 2026-11-01, and the
workbook's download through a public link instead of the authors' notification form is noted (CC 2026-11-02,
Lennart; a release-checklist item, not an issue). Lennart's question "whether we allow two datasets that similar" has
no answer yet (issue 1). The fit row the knowledge files propose for the two Milano toxicity sets (descriptors only, so
neither a scaffold split nor the share of close training analogs can be computed) is overtaken: both ship structures
and scaffold splits since 2026-11-01, so qsar_oral_toxicity's analog-share comparison can now be run here. The
record's first comment ("546 samples, too small for 3-fold CV") is an outdated criterion: size alone is no reason.

**Issues for Andrej:**

1. **Keep this dataset next to qsar_fish_toxicity, or retire it as redundant?**

   * **Problem:**
     - Both datasets come from the same Milano group, the same databases (ECOTOX, EAT5, OASIS) and the same pipeline
       (Dragon descriptors, a few chosen by a genetic algorithm for a k-nearest-neighbour model), and about 145 to 165
       chemicals appear in both.
     - qsar_fish_toxicity predicts the 96-hour LC50 for the fathead minnow (908 chemicals, in TabArena v0.1 and this
       working copy), this dataset the 48-hour LC50 for the water flea Daphnia magna (546 chemicals).
     - Lennart's record comment leaves open "whether we allow two datasets that similar" and Andrej disputes the keep,
       so: keep both, or retire this one?
   * **Background:** since 2026-11-01 both definitions ship the structure in place of the authors' descriptors and
     split by chemical series, so they now differ only in species, exposure time and chemicals. Records that share a
     source but give different tasks are not duplicates[^1a]. Two larger open sets with this endpoint were found on
     2026-10-31 and are screened in their own records: ADORE (Schür C, Gasser L, Perez-Cruz F, Schirmer K, Baity-Jesi
     M. A benchmark dataset for machine learning in ecotoxicology. Sci Data. 2023;10:718.
     https://doi.org/10.1038/s41597-023-02612-2; crustacean tests on 1,444 chemicals) and the consensus set of
     Lunghini et al. 2020 (https://doi.org/10.5281/zenodo.3708082; 3,680 compounds over Daphnia, fish and algae).
     The same Milano group's later set of 1,555 chemicals covers the endpoint too. Better data from another source
     does not retire a dataset by itself; the old one keeps the verdict its own data earns[^1b].
   * **Effect on the task:** two near-copies of one study design weigh that design twice in the benchmark, so a method
     that suits it gains on two datasets.
   * **Experiments:** an earlier check on the UCI files, before the structures were recovered, 20 x 3 random folds:
     - The overlap: 201 values of the logP descriptor MLOGP (fixed by the structure) appear in both files, against at
       most 57 when the values are shifted as a null; on 89 one-to-one matches the two LC50s correlate at r = 0.75.
     - The ranking: seven models rank the same on both (Spearman 0.89), on the authors' descriptors.
     - The signal: TabPFN 3.5 RMSE 1.04 against ExtraTrees 1.11, ahead on 58 of 60 splits; random forest 1.15,
       linear model 1.22, MLOGP alone 1.41, the mean 1.67.
     - Points that no longer apply since the descriptors left on 2026-11-01: the authors chose the 8 descriptors on
       436 of the 546 chemicals, for a model that declined to predict about a third of them, and random forest errors
       were higher on the last 110 rows of the file (+0.48 squared error, p = 0.058; a linear model showed none).
   * **Further points against:** the labels pool laboratories, clones and two endpoints (death and immobilisation),
     and the larger sets above cover the endpoint with more data.
   * **Consistency:** heart_disease merged three hospital files of one study, one protocol and one label, and retired
     the sites as its duplicates, since a model from the other hospitals ranked each site's patients nearly as
     well[^1c]; here the label differs (species, exposure time, endpoint), so neither a merge nor the duplicate rule
     applies. qsar_fish_toxicity's own record is `Yes`, also disputed by Andrej on this overlap.
   * **Unknown:** the exact overlap: both workbooks now give structures, so the shared chemicals can be counted by
     structure instead of MLOGP (the workbooks are not in this checkout); and whether models still rank the same on
     both under the scaffold split with the structure.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep both (implemented) | no change; the record stays `Yes (Disagreement)` | another species, exposure time and UCI entry with its own DOI; models separate | the overlap is not in the notes; the design counts twice |
     | B | Keep both, note the overlap | a `curation_comments` bullet on the shared chemicals and their correlation with qsar_fish_toxicity; record `Yes` | users know the two are siblings; follows the rule on different tasks from one source | the design still counts twice |
     | C | Retire as redundant | record `No (Retired)` with the overlap in its CC line, folder removed; qsar_fish_toxicity (larger, in TabArena v0.1) stays | the design counts once | no rule names redundancy as a reason and the duplicate marker does not fit; a small regression task with a real signal leaves |

   * **Recommendation:** B: the two are different tasks of one design, a note tells users so, and the larger Daphnia
     sets are judged in their own records. **Decision:** keep as is (A), keep with a note on the overlap (B), or
     retire (C)?

   **Notes for the AI:** on B, count the overlap by canonical SMILES from the two workbooks first (`toxicity_data.xlsx`
   and `toxicity_data_fish.xlsx`, as the definitions download them), then add a `curation_comments` bullet: "Sibling of
   qsar_fish_toxicity (same group, databases and pipeline): N chemicals are in both, their LC50s correlate at r = ...;
   another species and exposure time, so a different task (PROV-7)." Record: a CC line (Andrej) and `suggestion: Yes`;
   the same bullet in qsar_fish_toxicity. On C: record `No (Retired)` with no `Duplicate` marker, the CC line gives the
   overlap, folder removed, `v2_path` cleared, CHANGELOG entry.

   [^1a]: **PROV-7** (Must): records that share a source but give different tasks are not duplicates; the comments say
     why they are distinct, ideally each with its own DOI.
   [^1b]: Selection guidelines, "Small or dated, and the task is still done today": a hit from another source is its
     own record, not a duplicate, and the old record is not rejected automatically.
   [^1c]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates when neither adds a
     distinct task; case heart_disease (2026-10-27, Lennart).

   **Andrej (2026-11-05, change):** Do B for now.

   **Answer (AI, 2026-11-05):**

   * **Not applied yet:** B starts with the count of shared chemicals by structure, and the two structure workbooks the
     definitions read (`toxicity_data.xlsx` and `toxicity_data_fish.xlsx`, Milano Chemometrics) are not on this
     machine. The site blocks automated downloads and gives the files only after a form asking for personal details,
     which the AI did not fill in.
   * **Needed from you:** the two files (from Lennart's warehouse, where they were downloaded on 2026-11-01, or a
     download through the form). Then the count by canonical SMILES and the Pearson r of the two LC50s, the bullet in
     both definitions, `dataset check`, the record set to `Yes` with a CC line, and this issue resolved.
   * **Until then:** the earlier estimate from matching MLOGP values is 145 to 165 shared chemicals (r = 0.75 on 89
     one-to-one matches), not from structures. Species and exposure times are confirmed: Daphnia magna, 48 h (546
     chemicals) here; fathead minnow, 96 h (908) in qsar_fish_toxicity.

   **Notes for the AI:** the count script and folders are prepared; resume once the workbooks are in place (sha256 of
   `toxicity_data.xlsx` begins 61bcf1b0, of `toxicity_data_fish.xlsx` 98ae9433).

   **Resolved (2026-11-11, Andrej):** B ("Option B: Keep both, note the overlap"): a `curation_comments` bullet names
   the sibling qsar_fish_toxicity (same group, databases and pipeline; about 145 to 165 shared chemicals estimated from
   MLOGP values, LC50s at r = 0.75 on 89 matches; another species and exposure time, so a different task); record
   `Yes` with a CC line. Not done: the count by structure, since the two workbooks are still not on this machine (no
   warehouse copy; the download needs a form with personal details), and the same bullet in qsar_fish_toxicity, which
   was outside this round. Text only, data unchanged.

   **Andrej (2026-11-11, change):** Option B: Keep both, note the overlap.

   **Answer (AI, 2026-11-11):** B is confirmed and still blocked on the same two workbooks; a run is under way
   to fetch them from the authors' pages and, if they arrive, to count the shared chemicals by structure and
   give the correlation of the two LC50 values, which is what B's bullet needs.

2. **Time basis: name the scaffold split `Timeless`?**

   * **Problem:**
     - Each row is a chemical with a 48-hour LC50 for Daphnia magna, from laboratory tests that the source databases
       (ECOTOX, EAT5, OASIS) gathered over many years and the Milano group compiled in 2014; the release keeps no
       test date, and the only feature is the structure, which exists before any test.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits a catalogue of
       properties; the split holds out whole scaffolds and names no time basis yet.
     - A chemical's toxicity to one species at one exposure time is a fixed property of the chemical, the case the
       `Timeless` prototype names[^2a].
   * **Background:** the tested chemicals were not drawn at one time: which chemicals get tested changes with
     regulation and industry, and a new chemical under assessment often comes from a series not yet tested, which the
     scaffold split stands for. A split by test year would test the newest chemistry directly, but no date ships;
     ECOTOX records a publication year per test and could be joined on the CAS number in the authors' workbook, which
     is not on this machine (issue 1's answer). The overlap with qsar_fish_toxicity (issue 1) is no time question.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Scaffold split, `Timeless` | as now; the tag and a `Time basis:` line naming the property and the undated compilation | states the fact the split rests on; as the other molecule sets | the order in which chemicals were tested stays unmeasured |

   * **Recommendation:** B: toxicity is a property of the chemical, and the series split stands for new chemistry.
     **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`),
   a curation bullet `- Time basis: Timeless: a chemical's 48-hour LC50 for Daphnia magna is a property of the
   chemical; the tests were compiled from databases in 2014 without dates, and whole scaffolds are held out for new
   series.`, `splits_comment` unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
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
       answer too; the bulk `Timeless` item had named this dataset as one that moves if the first is accepted[^2q].
     - The release the definition reads carries an identifier: the authors' workbook gives each of the 546 chemicals its
       CAS-RN and SMILES (the definition's notes); ECOTOX, the main source database, keeps the publication year of every
       test, found by CAS-RN. The workbook is not in this machine's warehouse now.
     - Which chemicals get tested moves with regulation and industry, so a scaffold fold may train on a test chemical's
       same-period series, as the ChEMBL years showed for qsar_tid_11.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Date through ECOTOX, then decide | each CAS-RN joined to its earliest Daphnia magna 48-hour LC50 test in ECOTOX; label, close analogs and a split by year measured as in qsar_tid_11 issue 2; then `Timeless`, windows by year or the forced tag | decides on a measurement; the key ships in the workbook | ECOTOX's bulk file and the workbook (behind a form) to fetch; tests from EAT5 and OASIS stay undated |
     | b | Scaffold split, `ForcedGroupedFromTemporal` | the tag and a `Time basis:` line: tests over decades, no date in the release, likely drift in which chemical classes were tested; a dated release would test the newest classes | no join | gives up a date the CAS-RN can recover |
     | c | Scaffold split, `Timeless` (B as drafted) | the drafted tag and line | nothing to measure | assumes no drift, which the accepted item asks to check |

   * **Recommendation:** a, as qsar_tid_11 did with ChEMBL. **Decision:** a, b or c?

   [^2q]: **SPLIT-32** (Should; the items of 2026-11-06): question 1 also asks whether the use case meets items drawn
     like the catalogue's; a catalogue whose items enter in eras, or whose features mean something different by when an
     item was made, arose over time; which identifier a parent source could date the items by tells whether it drifts.
     Case: qsar_tid_11 issue 2, dated through ChEMBL.

   **Andrej (2026-11-11, discuss):** Reply (a): Date through ECOTOX, then decide

   **Answer (AI, 2026-11-11):** the dating is running; this turn records the decision, and the measurement follows.

   **Answer (AI, 2026-11-11):** dated, 394 of 546 on the strict join (72.2%) and 481 (88.1%) when only the species
   has to match. As for the fish set, a forward split is no stricter than the shipped scaffold split.

   * **The dating:** the EPA's ECOTOX bulk release (`ecotox_ascii_09_15_2026`, gaftp.epa.gov), joined on CAS to the
     Daphnia magna 48-hour LC50 records; the year is the publication year of the earliest matching test, 1965 to
     2018, median 1985. The chemicals that stay undated came to the authors from EAT5 and OASIS rather than ECOTOX.
   * **Check on the join:** where ECOTOX reports the LC50 in mg/L, its median value per chemical converted to
     -log10(mol/L) matches the workbook target at r = 0.903 on 170 chemicals, median difference 0.06 log units, 89.4%
     within one log.
   * **The split, three expanding windows by first test year against the scaffold folds** (untuned LightGBM / random
     forest, `encode_smiles`, RMSE, every training side at least half the dated chemicals; Slurm 1378106):

     | Scheme | RMSE, LightGBM / RF | Close training analog | Test scaffold in training |
     |---|---|---|---|
     | T, forward by year | 1.207 / 1.214 | 2.3% | 12-25% |
     | S, scaffold-disjoint | 1.264 / 1.300 | 0.6% | 0 |
     | R, random | 1.217 / 1.216 | 2.6% | 9-23% |
     | Shipped scaffold folds, all rows | 1.065 / 1.050 | 3.8% | 0 |

     - The forward split scores better than the scaffold-disjoint one here, and leaves 12 to 25% of the test
       chemicals a scaffold the model has seen.
     - The looser species-only join, 481 dated chemicals, gives the same picture (forward 1.146, scaffold-disjoint
       1.200 for LightGBM).
   * **Drift:** Spearman between first year and LC50 is +0.15 on the strict join and +0.11 on the species join, and
     the authors' own train/test share is flat across periods.
   * **What it means for the time basis:** as for qsar_fish_toxicity, the compilation is a catalogue of historic
     laboratory tests whose relation to the structure does not move with the year, so `Timeless` is now a measured
     statement rather than an assumption[^2t].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Scaffold split (implemented), `Timeless`, the dating written down | the tag, a `Time basis:` line and the table above | the split holds out more than a forward one; the drift is measured | 152 chemicals stay undated on the strict join |
     | b | Temporal split by first test year | three windows, the scaffold grouping dropped | follows the order the tests were run in | lower coverage than the fish set; a publication year is an upper bound; it leaves scaffolds in training |
     | c | Scaffold split, no prototype tag, the dating written down | the table in the notes, no tag claimed | makes no claim beyond the measurement | leaves the definition without a stated time basis |

   * **Recommendation:** a, and the same answer as for qsar_fish_toxicity, which was measured the same way on the
     same source. **Decision:** a, b or c?

   **Notes for the AI:** on a, `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`), a `Time basis:`
   bullet naming the historic compilation, the coverage on both joins, the flat relation and what the split cannot
   test; keep the table. Evidence and scripts in `~/claude_jobs/qsar_ecotox/`.

   [^2t]: **SPLIT-32** (Should): `Timeless` when the target is a fixed property of the item and the use case meets
     items drawn like the catalogue's; which identifier a parent source could date the items by tells whether the
     catalogue drifts.

## Reference

@article{cassotti2014prediction,
  title={Prediction of acute aquatic toxicity toward daphnia magna by using the ga-k nn method},
  author={Cassotti, Matteo and Ballabio, Davide and Consonni, Viviana and Mauri, Andrea and Tetko, Igor V and Todeschini, Roberto},
  journal={Alternatives to Laboratory Animals},
  volume={42},
  number={1},
  pages={31--41},
  year={2014},
  publisher={SAGE Publications Sage UK: London, England}
}

CC (2026-11-11, Andrej): kept next to `qsar_fish_toxicity` with the overlap written into both definitions (review issue 1, B).
- Counted by structure, from the two authors' workbooks rather than the earlier MLOGP estimate of 145 to 165: 237 chemicals are in both, 43.4% of this set and 26.1% of the fish set, 225 of them under the same CAS-RN.
- Their LC50s correlate at r = 0.81 (Spearman 0.82), the Daphnia values 0.37 log units more toxic on average.
- The species, the exposure time and the endpoint differ (Daphnia magna 48 h against the fathead minnow 96 h), so the two are different tasks of one study design, not duplicates; the notes of both now say so, since a method that suits the design gains on both.
