---
unique_name: qsar_oral_toxicity
name: QSAR oral toxicity
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- Many features
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- Expanding Science Catalogue
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

CC (2026-11-11, Andrej): the chemicals are dated before the time basis is named (review issue 1, C). The RTECS citation of each chemical's earliest rat oral LD50 report (ToxValDB v9.6.2) dates 7,927 of 11,119, 1935 to 2023.
- A forward split by report year (four windows, Slurm 1378153) leaves 12.4% of test chemicals a close training analog against 8.6% scaffold-disjoint, a third of the test scaffolds in training, and scores the same; whether to keep the scaffold split and name it Timeless is review issue 2. The definition is unchanged.

CC (2026-11-11, Andrej): time basis Timeless (issue 2, option b): the scaffold split stays; a curation bullet "Time basis: Timeless" states the fixed property, the inventory use case, the dating by RTECS report year (7,927 of 11,119, 1935-2023) and that a forward split by report year holds out less than the scaffold split (12.4% against 8.6% close training analogs, same score). The prediction-set reference re-measured: 19.8% of the project's 48,135 prediction chemicals are in this dataset; of the others 11.2% have a close training analog, against 15.1% of the test chemicals. The tag enters `data_tags` once the time-basis tags are in the working copy.

CC (2026-11-12, Andrej): collection facts `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension` (Review issue 3): the RTECS citation years that ToxValDB keeps date 7,927 of 11,119 chemicals (71.3%), 1935 to 2023. The facts describe the source and do not change with the split, which stays as it is.

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of `Timeless`:
- The use case predicts for items the catalogue does not hold, which the held-out scaffolds stand for; that the entry date carries no wave is a measurement for the `Time basis:` line, not a different use case.
- `Timeless` now means a fixed target in data with no time dimension. The split does not change.

## Review

**Outcome:** added. The very toxic endpoint of the ICCVAM acute oral toxicity project (rat oral LD50, the data behind
CATMoS): 11,116 chemicals with their QSAR-ready structure as a SMILES, grouped on the Bemis-Murcko scaffold (7,481
groups). Opened on 2026-11-11 from the review of how catalogues of fixed properties split: the definition names no
time basis for its scaffold split.

**Main points:** the chemicals dated by the year of their rat oral LD50 report (issue 1, C, resolved 2026-11-11): 7,927
of 11,119, and a split by report year holds out less than the scaffold split. Settled: the scaffold split stays, named
`Timeless` with the dating in its `Time basis:` line (issue 2, tag waits for PR #50). Settled 2026-11-12: collection
facts `Samples: Over Time`, `Time: Dated` (issue 3).

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

   **Resolved (2026-11-11, Andrej):** C ("Option C: Date the chemicals first"): dated, and the split by year measured;
   the result and the decision it leaves are issue 2. No change to the definition.

2. **Time basis after the dating: keep the scaffold split and name it `Timeless`?**

   * **Problem:** a forward split by report year leaves more close training analogs than the scaffold split
     (12.4% against 8.6%) and a third of the test scaffolds in training, and scores the same.
   * **The dating:** ToxValDB v9.6.2 keeps the RTECS citation of each ChemIDplus LD50 record (the source of most
     ICCVAM values); the year read from the citation of a chemical's earliest rat oral LD50 report dates 7,927 of
     11,119 chemicals (71.3%, by DTXSID, else CAS), 1935 to 2023, median 1976.
   * **The split, four expanding windows by report year** (1977-80, 1981-85, 1986-90, 1991-2023; 756 to 1,196 test
     chemicals; training sides 52% to 90% of the dated), on the same test chemicals, untuned LightGBM / random forest
     on the recommended encoding, means over the windows (Slurm 1378153):

     | Scheme | ROC AUC, LightGBM / RF | Log loss, LightGBM / RF | Close training analog | Test scaffold in training |
     |---|---|---|---|---|
     | T, forward by report year | 0.713 / 0.770 | 0.514 / 0.283 | 12.4% | 31.5% |
     | S, scaffold-disjoint | 0.717 / 0.770 | 0.514 / 0.281 | 8.6% | 0 |
     | R, random | 0.747 / 0.793 | 0.486 / 0.272 | 13.1% | 32.8% |
     | Shipped scaffold folds, all rows | 0.850 / 0.844 | 0.301 / 0.223 | 16.3% | 0 |

   * The undated 28.7% are half as often very toxic (5.2% against 9.7%), and 1981-85 reports are 13.9% very toxic
     against about 7% in the other windows, so a split on the dated rows would change the class mix too.
   * Checked on the way: 22.4% of the project's 48,137 prediction chemicals have an identical structure among the
     11,119 here (31.4% a close analog), so the 11.0% figure issue 1 drafted for the notes is to be re-measured on
     the prediction chemicals not in the dataset before it is written down.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Temporal split by report year | a `report_year` column, windows by year, 3,192 undated chemicals dropped | follows the dated order | drops 28.7% of the rows, unevenly by class; holds out less than the scaffold groups |
     | b | Scaffold split (implemented), `Timeless` | a `Time basis:` line: fixed property, the inventory use case, the dating and the table above | states what was measured; nothing dropped | the order of the undated rows stays unknown |
     | c | Scaffold split, the measurement written down, no prototype tag | the table in the notes only | claims nothing beyond the numbers | leaves the time basis unnamed |

   * **Recommendation:** b. **Decision:** a, b or c?

   **Notes for the AI:** on b, a `curation_comments` bullet `- Time basis: Timeless: ...` naming the fixed property,
   the inventory use case, the RTECS dating (7,927 of 11,119, 1935-2023) and the forward-against-scaffold numbers,
   ending with what the split cannot test (the order of the undated rows); the prediction-set reference re-measured
   first; the tag enters `data_tags` once PR #50 is in the working copy; then `dataset check`, a CHANGELOG entry and a
   record CC line.

   **Resolved (2026-11-11, Andrej):** b (`ok` on the recommendation): the scaffold split stays; a `Time basis:
   Timeless` bullet in `curation_comments` names the fixed property, the inventory use case, the RTECS dating (7,927 of
   11,119, 1935-2023), the forward-against-scaffold numbers and the undated rows' class mix, and ends with what the
   split cannot test (the order of the undated chemicals). The tag enters `data_tags` once PR #50 is in the working
   copy. Record CC line. The prediction-set reference, re-measured first (no model, scaffold 3x3 folds on the public
   files' 11,119 chemicals):

   | Prediction chemicals (48,135 readable) | Share | Close training analog | Median nearest similarity |
   |---|---|---|---|
   | 2D structure already in this dataset | 19.8% (9,537); 22.4% by identical fingerprint | | |
   | Not in the dataset (38,598), against a fold's training side | | 11.2% | 0.487 |
   | Not in the dataset, against all 11,119 chemicals | | 14.4% | 0.522 |
   | Test chemicals of the same folds, for comparison | | 15.1% | 0.510 |

   The 11.0% of the notes holds for the prediction chemicals not in the dataset (11.2%), so `fit_reason` keeps it.
   `dataset check` not run: the curator's copy of `vt_data.mat` is not in `local-data-warehouse/` on this machine; the
   edit is a curation note only, and the README's notes are regenerated at the next check.

3. **Collection facts: `Samples: Over Time` and `Time: Dated`, since a source dates the items?**

   * **Problem:** the record carries `Samples: No Time Dimension`, while the RTECS citation years that ToxValDB keeps
     date 7,927 of 11,119 chemicals (71.3%), 1935 to 2023. The facts describe the source and do not change with the
     split; whether the date carries anything belongs to the time basis `Timeless` (issue 2)[^3a].
   * **Change:** `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension`; the data, the split
     and the score are unchanged.

   [^3a]: **SPLIT-32** (Should): the collection facts are read from the source and do not change with the split; a
     catalogue that a parent source dates is `Samples: Over Time` with `Time: Dated` even where the date turns out to
     carry nothing, and whether it does is measured for the time basis.

   **Resolved (2026-11-12, Andrej):** applied on approval of the plan that settled the split keys of growing catalogues
   (one decision for the eighteen datasets of that review): the record's facts changed, with a CC line and `Andrej` in
   `checked_by`. No definition change.


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
