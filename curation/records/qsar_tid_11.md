---
unique_name: qsar_tid_11
name: QSAR-TID-11
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
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
year: '2015'
domain: chemistry & material science
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=3050
- https://doi.org/10.17632/SPWGRCNJDG.1
- https://doi.org/10.1007/S10994
notebook_path: datasets/beyond_iid/old_iid/qsar_tid_11/qsar_tid_11.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_tid_11/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Chemistry dataset. features represent FCFP 1024bit Molecular Fingerprints. Unsure what that is, but I think there are no local correlations;hard to tell usability without domain expert even from paper

Potential issue: We are no domain experts

Lennart: tend towards yes - hard to tell if domain is appropiate. The papers and meta-learning use this still and it might be outdated but tabular is sitll a strong baseline (even once they have deep learning method as for other bio applicaiton domains)

Andrej: Not in TabRepo, need to clarify

CC (2026-10-21, Lennart): one domain for the molecule-property datasets (the input is the molecule): "chemistry & material science", for all ten QSAR siblings.

CC (2026-10-21, Lennart): 0/1 presence flags are categorical ("Assuming it is binary, the categorical dtype might be best?"); CLEAN-14 amended. The bits were checked to hold only 0 and 1.

CC (2026-10-21, Lennart): CLEAN-11 amended: a row whose target the source names as not the task's quantity, or a single extreme target in the training period only, may leave, with the source's words.

**Assessment (AI, 2026-10-21):** the dropped row (pXC50 -6.24) does not meet the amended clause (the split is random, so there is no training period, and the source does not name the row), but it is an impossible value: a half-effect concentration of about 1.7 million mol/L. Under CLEAN-11 the target becomes missing and the row leaves by CLEAN-15; the reason is now in curation_comments.

CC (2026-10-21, Lennart): "Yes, follow your recommendation" on the repeated fingerprints: keep the repeated FCFP vectors (different ChEMBL compounds) with the reason written down, and drop the salt-form copies of one parent as LEAK-19 does in qsar_oral_toxicity.

**Assessment (AI, 2026-10-21):** every one of the 5,742 rows has its own ChEMBL id; 870 rows sit in 387 repeated fingerprint vectors. ChEMBL's molecule_hierarchy (API) traced 798 of them (72 ids are no longer in ChEMBL): stereoisomers (179 vectors) and analogs (125 vectors) stay as different compounds with their own potency. Untuned LightGBM RMSE: random 0.765, grouped on the vector 0.781, one row per vector 0.757; a vector-mate mean gives 0.798. Salt forms: 37 pairs of ids share one ChEMBL parent and one vector (31 of them are a whole vector, target sd median 0.006; 6 sit in larger vectors; median sd over all 37 is 0.04). The definition drops the 37 non-parent rows by an embedded id list (SALT_FORM_COPIES; the raw file has no structures), keeping the parent's row or, in the one pair without it, the lowest ChEMBL id; the target is not read. Rows 5,741 -> 5,704. dataset check: 0 errors, 2 warnings (99 exact duplicate rows, 347 rows sharing features with another target). Evidence: local-data-warehouse/_runs/2026-10-21_crosscut/cleaning_features/ (tid11_repeated_chembl.csv, tid11_salt_drop.csv, scripts/tid11_salt_drop.py).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — Average root mean squared error (RMSE) with 10-fold cross-validation (Olier et al. 2018, Meta-QSAR, Machine Learning 107:285-311, doi:10.1007/s10994-017-5685-x, Sec. 2.3 (arXiv:1709.03854)).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `papyrus_bioactivity` (TBD -> Yes, priority 2), `chembl36_kinase_bioactivity` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-01):** a scaffold split is possible (SPLIT-31 as amended): ChEMBL 17, the release the data was drawn from, holds the structure of all 5,742 compound ids of the file (`chembl_17_chemreps.txt.gz`; the InChIKey equals today's ChEMBL for all 5,505 ids still served). Bemis-Murcko scaffolds (`scaffold_groups`): 2,529 groups for 5,704 compounds, 21 ring-less compounds alone, the largest group the bare benzene ring (117, 2%). Random against scaffold split: test compounds with a close training analog (Tanimoto >= 0.7, Morgan r2 2,048 bits) 79.7% against 59.2%; untuned LightGBM RMSE 0.794 against 0.920 (3 x 3 folds). Of the 356 repeated fingerprint vectors, 303 lie within one scaffold. Evidence: `local-data-warehouse/_runs/2026-11-01_scaffold_checks/qsar_tid_11/`.

CC (2026-11-01, Lennart): go ahead with the scaffold split. The definition joins each compound's ChEMBL 17 structure on `MOLECULE_CHEMBL_ID` and groups on the scaffold; `required_split` is now `Grouped (NON-IID)`. Not built.

CC (2026-11-01, Lennart): SMILES ship as a typed structure column, not pre-encoded and never as text (path C of the discussion doc "SMILES Handling in Data Foundry and TabArena v0.2" (https://claude.ai/artifact/6r49WpR9Uard5ogo7qK4rB)): the benchmark encodes it; the recommended encoding in Data Foundry is RDKit's 2D descriptors with the MACCS keys.

**Assessment (AI, 2026-11-01):** the definition now ships the ChEMBL 17 structure as `SMILES` (RDKit's canonical form, salts as ChEMBL records them) in `smiles_columns`, next to the source's 1,024 FCFP bits, which stay since the recommended encoding does not reproduce Pipeline Pilot's fingerprint. With the structure in the frame the two duplicate-row warnings are gone (rows that share a fingerprint differ in their structure).

CC (2026-11-01, Lennart): ship the SMILES only: "the real task here is going from smiles to a prediction, the bits are just one possible modelling choice by the authors".

**Assessment (AI, 2026-11-01):** the authors' 1,024 FCFP6 bits leave; `SMILES` is the one feature. RDKit cannot recompute those exact bits (with its closest settings no source bit is matched exactly by any RDKit bit). LightGBM R^2 on the 9 scaffold splits: authors' bits 0.645; the recommended encoding (RDKit 2D + MACCS) 0.601; RDKit's FCFP6-like bits 0.628; the recommended encoding with RDKit's FCFP6-like bits 0.640, with RDKit's ECFP4 counts 0.658 (better than the authors' bits on 8 of 9 splits). The 474 stereoisomer rows (217 groups, potency range median 0.45 pXC50) stay, as decided on 2026-10-21; no two rows share a SMILES. Evidence: `local-data-warehouse/_runs/2026-11-01_scaffold_checks/qsar_tid_11/encodings_compare.txt`.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the folder's `REVIEW.md`. Ship with a note: real thrombin potencies with structures and held-out series that separate methods widely, but 11.5% of the targets are assay limits that ChEMBL records only as bounds (31 of 36 sampled), stored as exact values. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): the three open issues of the folder's `REVIEW.md` are settled; the definition and this
record carry the decisions. Not built.

- Issue 2, option C, split by first publication year: the scaffold-grouped split is replaced by a temporal one on
  `first_year`, the earliest year among the documents of a compound's human thrombin (CHEMBL204) activity records in
  ChEMBL 17 (a one-off extract from the release's sqlite dump on the EBI FTP, shipped as `chembl_17_first_year.csv`
  next to `dataset.py`). All 5,704 compounds have a CHEMBL204 record there, 5,186 in a dated document (1992-2013);
  the other 518 appear only in the undated PubChem BioAssay deposit CHEMBL1201862 and take 2011, the year ChEMBL 9
  loaded it. Five windows of two years: 2012-13 (159 compounds), 2010-11 (744), 2008-09 (290), 2006-07 (598) and
  2004-05 (633), each trained on every earlier compound (5,545, 4,801, 4,511, 3,913 and 3,280 rows, 97% to 57%).
  `first_year` is a feature as well as the time column, as in apistox. Measured on these windows and all 5,704
  compounds (2026-11-11): the scaffold folds leave 58% of the test compounds a close training analog, 71-93% of them
  first published in the same year, and untuned LightGBM's RMSE is 0.80-1.04 by scaffold against 0.89-1.50 by year.
  At an equal training size drawn from all years the forward split loses about 0.2 RMSE only on the oldest window,
  where many compounds are published later, so the scaffold split's advantage is the same-year siblings rather than
  the later papers. The probes on the new windows raise no flag (LightGBM R^2 0.350, skill +0.419 over the dummy on
  all five; no exact feature copy across the split; `hidden_groups` 0 hits of 61 candidates). `required_split` is now
  Temporal (NON-IID) and the tag Non-IID (Temporal); `grouping` and the `scaffold` column are gone, the scaffold
  numbers stay as background.
- Issue 1, option B, keep and document the censored potencies: the 654 targets at round assay limits (11.5%; pXC50
  4.30: 348, 5.00: 204, 4.00: 81, 4.70: 21) stay as exact values, with a `curation_comments` bullet naming the
  limits, their counts and the bound reading (LEAK-26: documented). They are the inactive end of the screen; 306 of
  them (47%) belong to the PubChem deposit, where 59% of the 518 compounds sit at a limit against 6.7% of the rest.
- Issue 3, option B, collection facts: `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time
  Dimension`. No `Target: Revised Later`: only 5.1% of the compounds have a thrombin record from a year later than
  their first, so a median label seldom moves after the compound's first publication.
- References: Olier et al. 2018, Meta-QSAR, Machine Learning 107:285-311, doi:10.1007/s10994-017-5685-x (Sec. 2.2 on
  the median of the modal log unit, arXiv:1709.03854); ChEMBL 17 release dump,
  https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_17/; Sheridan RP, Time-split cross-validation
  as a method for estimating the goodness of prospective prediction, J Chem Inf Model 2013;53(4):783-790,
  doi:10.1021/ci400084k. Evidence: `~/claude_jobs/time_review/qsar_tid_11/`.
