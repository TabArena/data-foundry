---
unique_name: qsar_oral_toxicity
name: QSAR oral toxicity
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 4
tags:
- Many features
- Non-IID (Grouped)
- 'Samples: No Time Dimension'
collections:
- New (BeyondArena)
- ChemPile
original_source: Other
year: '2019'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/508/qsar+oral+toxicity
- https://doi.org/10.24432/C5PS4J
- http://www.michem.unimib.it/download/data/
notebook_path: datasets/_dev/feature_selection/qsar_oral_toxicity/qsar_oral_toxicity.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_oral_toxicity/dataset.py
source_row: 685
type_adapter_id: curation-record-v1
---

## Comments

Rel: https://www.centro3r.it/sites/default/files/Ballabio_et_al-2019-Molecular_Informatics.pdf

Looks like a good QSAR dataset and a valid task

**Assessment (AI, 2026-10-07):** UCI 508 is the very toxic endpoint (LD50 < 50 mg/kg) of the calibration set of the ICCVAM/NICEATM acute oral toxicity project behind CATMoS (NTP trainingset_171130.txt has the same 741 / 8,251 class counts), with Dragon ECFP bits from Ballabio et al. 2019. The file stores the authors' 6,744 training rows, then their 2,248 test rows (Table 1). The bits come from the QSAR-ready parent structure, so salt forms share a vector: the v2 definition drops 477 exact copies and 22 rows of 11 vectors with both classes (8,493 left). IID, as in both source splits; random forest AUC 0.88, no probe flags. Fingerprints are in scope as for qsar_tid_11.

**Assessment (AI, 2026-10-20):** priority 4 for the review of the added dataset: gap -, use case +, source +, shape +, no known risk. Well-documented regulatory toxicity task with 1,024 fingerprint bits; issues closed in verification, only an optional extension stays open.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes, no exclusion and no re-split. Applied: the target reads 50 mg/kg or less, the top hazard category (the 2026-10-07 line's "LD50 < 50" is the same correction; 25% of labels come from category data without a point LD50); nine parents that survived the deduplication twice lose their second row through the order linkage to the project's structure file, so 8,484 chemicals remain; the false reason for IID-only (no structure in the file) is replaced by the use case and the structure-blind source protocols; the duplicate counts, the Dragon 7 citation and the fingerprint variant are corrected; the note carries the cluster cost (random forest 0.882 to 0.842 by Butina clusters, 0.887 to 0.843 by scaffolds, ranking unchanged). Open for the curator: the fit label (the prediction set is farther from training than the test rows, 9.3% against 19.7% close analogs; the panel recommends approximate), a scaffold-grouped variant, and the extension with the evaluation set. Priority 4: gap - (no thin domain, problem type or regime), use case + (CATMoS names the screener and the decision), source + (UCI, two papers, the project's own files), shape + (8,484 rows, 1,024 features), risk none (the open items are a label and a variant, not a leak or an unclear target).

CC (2026-10-21, Lennart): 0/1 presence flags are categorical ("Assuming it is binary, the categorical dtype might be best?"); CLEAN-14 amended. The bits were checked to hold only 0 and 1.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Ballabio et al. 2019 report the non-error rate with sensitivity and specificity, the group's house measure, without costs; 25% very toxic. Original rejected: NER. roc_auc is the binary fallback.

CC (2026-10-21, Lennart): keep the scaffold-grouped variant a listed candidate (SPLIT-31), no re-split; IID stays.

CC (2026-10-21, Lennart): fit `approximate`: "this is a more simulated use case than a direct real case". The fit_reason names the gap: the random test chemicals are closer to training than the untested chemicals a screener faces (19.7% against 9.3% with a close analog at Tanimoto 0.7 or more).

CC (2026-10-21, Lennart): Extend with the package's validation set and use the further feature data, preprocessing the SMILES as for the other SMILES datasets.

**Assessment (AI, 2026-10-21):** Extended and re-featured. The definition now reads the authors' package (vt_data.mat, a copy the curator provided; public route: the group's download form, freeware with the paper cited) instead of the UCI file, which equals its ECFP_1024_02 training and test blocks row by row (8,992 of 8,992, classes too). With the project's evaluation set the source has 11,886 chemicals (984 very toxic); after the same deduplication (732 exact copies, 20 both-class vectors over 52 rows, 9 parents kept twice by InChIKey) 11,105 remain, 931 very toxic (8.4%), up from 8,484 and 708. `_prepare_raw_files` decodes the MATLAB string objects of the package, so the build reproduces from the original file; the decoded rows were checked against the project's public structure files (evaluation set by RowID on all 2,894 rows, calibration by CASRN or InChIKey, 100% class agreement) and the SMILES reproduces its row's InChIKey for 99.8% of rows. Features: the 1,024 bits plus 207 RDKit 2D descriptors of the QSAR-ready SMILES, which decide (default LightGBM over the 9 shipped splits: 0.885 bits only, 0.901 with the descriptors, better on 9 of 9; random forest 0.901 to 0.912); the SMILES is dropped as in every SMILES dataset, `rdkit_Ipc` with it (it overflows float32; open for the curator). Metric unchanged (roc_auc fallback; 8.4% very toxic). Fit stays approximate with re-measured numbers (close analogs 24.5% of test rows against 11.0% of the project's untested prediction set; random forest 0.715 for distant chemicals against 0.945 for close ones), and the scaffold-grouped cost is now 0.900 to 0.852.

CC (2026-10-21, Lennart): `rdkit_Ipc`: fix it by scaling rather than dropping it. Accept the `dataset_pure_feature_value` warning (rdkit_fr_Ar_COO) with its reason. `original_source`: take the definition's value (Other).

**Assessment (AI, 2026-10-21):** Applied. `rdkit_descriptors` (data_foundry.v2.chemistry) now ships Ipc as `rdkit_Ipc_log10` = log10(1 + Ipc) for every SMILES dataset, so the definition keeps it (208 descriptors; maximum 166.8 here instead of 6e166). apistox and qsar_bioconcentration change with it: apistox's Ipc reached 2.6e38, just below the float32 limit, now 38.4; qsar_bioconcentration's 7.7e9, now 9.9. The warning is accepted in `accepted_check_warnings`; `original_source` is Other. dataset check: 0 errors, 0 warnings on all three. Not rebuilt.

CC (2026-10-26, Lennart): reopened from qsar_bioconcentration's issue 10, option (d) ("also do the right split for oral"): SPLIT-31 amended, so the split groups on the Bemis-Murcko scaffold of the QSAR-ready SMILES, ring-less chemicals and the bare benzene ring alone. This supersedes CC 2026-10-21 (IID kept, the scaffold variant a candidate): the structures are exact since the extension of the same day.

**Assessment (AI, 2026-10-26):** applied: `scaffold_groups` on the QSAR-ready SMILES (2,577 ring-less and 1,969 bare-benzene chemicals alone; test folds of 3,365-3,918 chemicals). Close training analogs (Morgan radius 2, 2,048 bits, Tanimoto 0.7 or more) of the test chemicals: 16.3% (24.7% at random), against 11.0% for the untested chemicals of the project's prediction set, so the fit stays approximate with the new numbers in fit_reason. Task probes: random forest ROC AUC 0.864, LightGBM 0.821, linear 0.757, no flag. dataset check: 0 errors, 0 warnings.

CC (2026-10-26, Lennart): verdict ship.

CC (2026-11-01, Lennart): SMILES ship as a typed structure column, not pre-encoded and never as text (path C of the discussion doc "SMILES Handling in Data Foundry and TabArena v0.2" (https://claude.ai/artifact/6r49WpR9Uard5ogo7qK4rB)): the benchmark encodes it; the recommended encoding in Data Foundry is RDKit's 2D descriptors with the MACCS keys.

**Assessment (AI, 2026-11-01):** the definition now ships `SMILES` (RDKit's canonical form of the QSAR-ready SMILES) in `smiles_columns` next to the 1,024 published ECFP bits, which stay since the recommended encoding does not reproduce Dragon's fingerprint; RDKit's 208 descriptors no longer ship. The accepted `dataset_pure_feature_value` warning on `rdkit_fr_Ar_COO` left with the descriptor column. MACCS keys next to bits and descriptors: +0.009 (LightGBM) / -0.003 (random forest) ROC AUC.

CC (2026-11-01, Lennart): ship the SMILES only, as for qsar_tid_11: the authors' fingerprint is one modelling choice; the benchmark encodes the structure.

**Assessment (AI, 2026-11-01):** the 1,024 ECFP bits (Dragon 7) leave; `SMILES` is the one feature. The copies are now found on the 2D structure (`canonical_smiles(..., stereo=False)`) instead of the bit vector: 720 exact copies, the 20 structures with both classes (52 rows) and 10 tautomer pairs by InChIKey leave, so 11,116 chemicals remain (933 very toxic), 11 more than before, since bit collisions had joined different chemicals. Scaffold groups: 7,481 (2,579 ring-less and 1,973 bare-benzene chemicals alone).

CC (2026-11-02, Lennart): on the de-duplication change of 2026-11-01, carried to the curator in the handover
document as a change that was not an instruction: "the changes look good". The copies are found on the 2D structure
instead of the published ECFP bit vector, which moves the shipped row count from 11,105 to 11,116: the old key
merged chemicals whose bit vectors collided rather than chemicals that are the same.

## Review

**Outcome:** added. The very toxic endpoint of the ICCVAM acute oral toxicity project (rat oral LD50, the data behind
CATMoS): 11,116 chemicals with their QSAR-ready structure as a SMILES, grouped on the Bemis-Murcko scaffold (7,481
groups). Opened on 2026-11-11 from the review of how catalogues of fixed properties split: the definition names no
time basis for its scaffold split.

**Main points:** Name the scaffold split `Timeless`, with the project's own untested chemicals as the reference for
how far a test chemical stands from training (issue 1)?

**Issues for Andrej:**

1. **Time basis: name the scaffold split `Timeless`, or date the chemicals first?**

   * **Problem:**
     - The definition splits on the scaffold and names no time basis, while the record carries
       `Samples: No Time Dimension`.
     - Whether a chemical is very toxic when swallowed is a fixed property of the chemical, the case the `Timeless`
       prototype names[^1a].
     - The project that compiled the data also published the chemicals it was built to screen, so how new the test
       chemicals are can be measured against the actor's real population rather than guessed.
   * **Background:** the use case is a chemical without an acute oral test, judged before any animal test; the fit is
     already recorded as approximate, because the test chemicals are members of the tested reference set.
   * **Experiments:** the share of chemicals with a close training analog (Tanimoto 0.7 or more, Morgan radius 2,
     2,048 bits), measured when the scaffold split was adopted:

     | Population | Close analog in training | Median nearest similarity |
     |---|---|---|
     | Test chemicals, random split | 24.7% | |
     | Test chemicals, scaffold groups | 16.3% | 0.519 |
     | The project's 48,137 untested chemicals | 11.0% | 0.486 |

   * **Effect on the task:** the scaffold groups move the test chemicals most of the way toward the untested
     inventory the actor meets, which is what the split is for here; nothing in this task arrives later, since the
     inventory already exists.
   * **Consistency:** on 2026-11-11 the three sibling Milano sets (qsar_biodeg, qsar_fish_toxicity,
     qsar_aquatic_toxicity) were sent to be dated through NITE and ECOTOX before their time basis is named; this
     dataset differs in having its screening population published, so the question it answers is already measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | no change | nothing to write | the definition does not say why a split that is not temporal is safe in time |
     | B | Scaffold split, `Timeless` | the tag and a `Time basis:` line naming the fixed property and the untested inventory as the reference | states the fact the split rests on; the inventory measures what the split cannot reach | the order in which the chemicals were tested stays unmeasured |
     | C | Date the chemicals first | look for a test or registry year per chemical, then decide as the sibling sets will | same route as the three siblings | the use case fills in an existing inventory, where nothing comes later; the ICCVAM compilation pools many databases and registries |

   * **Recommendation:** B: the actor screens an inventory that already exists, and that inventory is published, so
     it is the reference rather than a year. **Decision:** A, B or C?

   **Notes for the AI:** on B, `data_tags = ("Timeless",)` (the class adds `Non-IID`, `Grouped`) and a
   `curation_comments` bullet: `- Time basis: Timeless: acute oral toxicity is a property of the chemical, and the
   use case fills in an inventory that already exists. The split holds out whole series: 16.3% of the test chemicals
   have a close training analog, against 24.7% at random and 11.0% for the project's 48,137 untested chemicals, so
   the split stands between a random one and the screening population.` Then `dataset check`, a CHANGELOG entry and a
   record CC line with `Andrej` in `checked_by`.

   [^1a]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows; `Timeless` when the target
     is a fixed property of the item, the same whenever it is measured, and the use case meets items drawn like the
     catalogue's. **SPLIT-34** (Should, proposed): where the actor fills in an inventory that already exists, nothing
     comes later and the family key stands for the less similar items of that inventory; the inventory itself, where
     the source has it, is the reference for how close the test items should be to training.

   **Andrej (2026-11-11, change):** Option C: Date the chemicals first.

   **Answer (AI, 2026-11-11):** dated, 7,927 of 11,116 (71.3%). The year does not hold out chemistry, and the
   untested set this issue leans on is closer to the data than the issue says.

   * **The dating:** EPA's ToxValDB keeps the RTECS citation per ChemIDplus record (its own `YEAR` column is empty
     for that source), and the year parses out of the citation string for 85% of the rat oral LD50 records. Joined on
     DTXSID and then CASRN, 7,927 chemicals carry a year, 1932 to 2023, median about 1979, 52% of them 1976 or
     earlier. Where both keys give a year they agree for 99.95% of 6,184 chemicals.
   * **What the date means:** the publication year of the report the LD50 came from, not a registry year and not a
     first publication of the substance.
   * **Check:** of 6,030 chemicals with a point LD50 in the file and a ChemIDplus rat oral record, 93.8% have a
     record whose LD50 equals the shipped value to within 2%, so the label is the ChemIDplus value; for the 4,870
     where that record itself carries a year, the year assigned equals it for 100%.
   * **The split, four expanding windows by report year** (random forest / LightGBM, ROC AUC, every training side at
     least 52% of the dated rows; Slurm 1378153):

     | Scheme | ROC AUC, RF / LightGBM | Close training analog | Untested set's analog share | Test scaffold in training |
     |---|---|---|---|---|
     | T, forward by year | 0.770 / 0.713 | 12.4% | 17.6% | 31.5% |
     | S, scaffold-disjoint | 0.770 / 0.717 | 8.6% | 17.0% | 0 |
     | R, random | 0.793 / 0.747 | 13.1% | 18.3% | 32.8% |
     | Shipped scaffold folds, all rows | 0.844 / 0.850 | 16.3% | 23.3% | 0 |

     - A forward split's test chemicals have about as many close analogs as a random draw, and 31.5% share a scaffold
       with training; the scaffold-disjoint draw is the one that pushes them away, at the same AUC.
     - A chemical first reported in 1991 is often a close relative of one reported in 1965, so the year separates when
       somebody ran the test, not which chemistry a screener has not met.
   * **A correction to this issue's own table:** the 11.0% close-analog share quoted for the project's 48,137
     untested chemicals understates how close that population is. Measured against all the dataset's chemicals,
     31.4% of the prediction set has a close analog and 22.4% an identical fingerprint, and 9,588 of them (19.9%)
     share a QSAR-ready InChIKey with a dataset chemical, 7,295 a CASRN. The 11.0% holds only after the identical
     ones are dropped. So a fifth of the "untested" set is not untested, and the inventory is a weaker reference for
     the split than the issue assumed.
   * **Options:** as above, with the measurement now in hand: a, scaffold split with `Timeless` and the dating and
     the corrected inventory figures written down; b, temporal split by report year; c, scaffold split, the dating
     written down, no prototype tag.
   * **Recommendation:** a, but on the dating rather than on the inventory, since the inventory overlaps the data.
     **Decision:** a, b or c?

   **Notes for the AI:** on a, correct the 11.0% figure wherever it appears in the notes before leaning on it, and
   state the overlap. The frame was reproduced from the public NICEATM files (11,119 rows against the shipped
   11,116, 7,483 scaffolds against 7,481, the scaffold close-analog share 16.3% exactly as recorded), since the
   Milano package is not in this clone. Evidence in `~/claude_jobs/qsar_dating2/`.

## Reference

@article{ballabio2019integrated,
  title={Integrated QSAR models to predict acute oral systemic toxicity},
  author={Ballabio, Davide and Grisoni, Francesca and Consonni, Viviana and Todeschini, Roberto},
  journal={Molecular informatics},
  volume={38},
  number={8-9},
  pages={1800124},
  year={2019},
  publisher={Wiley Online Library}
}
