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

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship with a note: real thrombin potencies with structures and held-out series that separate methods widely, but 11.5% of the targets are assay limits that ChEMBL records only as bounds (31 of 36 sampled), stored as exact values. Priority 2: gap 0, use case 1, source 1, shape 0, risk -1.

CC (2026-11-11, Andrej): the three open issues of the record's Review are settled; the definition and this
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

## Review

**Outcome:** added. The Meta-QSAR dataset for human thrombin (ChEMBL target CHEMBL204; OpenML 3050, 2015; Olier et
al. 2018, Machine Learning 107:285-311, https://doi.org/10.1007/s10994-017-5685-x): the median measured potency
(pXC50, minus the log of the concentration giving half the effect) of 5,704 compounds from ChEMBL 17, after the 37
salt-form copies and one impossible value left. Since 2026-11-01 each compound's ChEMBL 17 structure ships as a SMILES
in place of the authors' 1,024 FCFP6 bits, and whole chemical series (2,529 scaffold groups) are held out; RMSE is the
source's metric. The AI recommends shipping it with the censored potencies documented (issue 1). Reviewed on 2026-11-04
without a panel, from the gathered evidence (the record, the CHANGELOG, model runs on the shipped data and on
TabArena v0.1's copy) and one check of the targets against ChEMBL. Validity: a medicinal chemist's screening question
on potencies measured against one target, from the structure alone, with series held out; but 11.5% of the targets
sit at round assay limits, most of them potencies ChEMBL records only as a bound (issue 1). Value: the task probes on
the v0.2 frame give R^2 0.66 (LightGBM), 0.62 (random forest) and 0.48 (linear); on the shipped data (the bits, random
splits) the 40 benchmark methods spread from RMSE 0.677 (LimiX-2) to 0.993 (default linear model), median 0.737.
Quality:
the 474 stereoisomer rows keep their own potencies (decided 2026-10-21); the activity drifts with the ChEMBL id order,
which the shuffle removes. Weighed: real measured potencies with structures and held-out series +, wide separation of
methods +, bounds stored as exact potencies -, a larger later release screened (Papyrus) -.

**Main points:** Keep the potencies ChEMBL records only as bounds ("weaker than 50 µM") as exact values, and say so in
the notes (issue 1; 44% of them come from one PubChem screen)? Split by first publication year, since the scaffold
folds keep same-year siblings (RMSE 0.68-0.90 against 1.11-1.31 by year), or keep the scaffold split as `Timeless`
(issue 2)? Record the compounds as published over time, dated through ChEMBL (issue 3)?

**Record fields that disagree with the definition:**

- `original_source`: record `None`, definition `OpenML`.

**Record judgment:** valid. The record carries the v0.2 changes (CC and Assessment of 2026-11-01); its workbook notes
("unsure what that is", "not in TabRepo, need to clarify") are answered by them.

**Issues for Andrej:**

1. **Keep the potencies that ChEMBL records only as bounds as exact values, with a note?**

   * **Problem:**
     - 654 of the 5,704 targets (11.5%) sit exactly at round assay limits: 348 at pXC50 4.30 (50 µM), 204 at 5.00
       (10 µM), 81 at 4.00 (100 µM) and 21 at 4.70 (20 µM), where only a few dozen rows lie nearby (40 within 0.05 of
       4.30).
     - In a sample of 36 of these compounds, ChEMBL holds 31 against thrombin only as "weaker than" records (no half
       effect up to the highest concentration tested), 3 as exact values and 2 not at all, so most of these targets
       are bounds stored as if measured.
     - Keep them as exact values with a note, drop them, or recover the bounds from ChEMBL 17?
   * **Background:**
     - A record "> 50,000 nM" means the true pXC50 is below 4.30, so the stored value overstates the potency of an
       inactive compound by an unknown amount. The source describes the extraction in Sec. 2.2: potency endpoints
       of protein targets, and "a consensus value was selected as the median of those activities falling in the modal
       log unit"; it does not say how bounds were treated (arXiv 1709.03854).
     - Model runs on the shipped data found the limits series-specific: a compound's nearest analogue
       shares its exact limit value 50 to 85% of the time, since each laboratory tested its series up to its own top
       concentration. The definition's notes do not mention the limits.
   * **Effect on the task:** for an inactive compound the score rewards predicting the top concentration its
     laboratory tested rather than "inactive"; whether a compound is active, the chemist's decision, is unaffected.
     The scaffold split weakens the look-up of a series' limit but does not remove the bounds.
   * **Experiments:** target values counted on the v0.2 rows (OpenML file minus the definition's 38 dropped rows);
     ChEMBL's web service queried on 2026-11-04 (today's release, not ChEMBL 17) for 12 random compounds at each of
     4.30, 4.00 and 5.00:

     | Stored pXC50 | Rows | Sample: only bound records | Exact records | Not found |
     |---|---|---|---|---|
     | 4.30 (50 µM) | 348 | 11 of 12 | 0 | 1 |
     | 4.00 (100 µM) | 81 | 9 of 12 | 2 | 1 |
     | 5.00 (10 µM) | 204 | 11 of 12 | 1 | 0 |

   * **Consistency:** the curation rules want a capped target dropped or documented[^1a]; censored values are no
     regression target where they are the bulk (nci_aids_antiviral_screen: the effective concentration was not
     reached in 38,048 of 39,365 rows, so it ships the screen's yes/no call)[^1b]. Here they are 11.5% and mark the
     inactive end of a screen.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as exact values (implemented) | 5,704 rows, no note | the source's task as published | 11.5% of the targets are bounds scored as exact, undocumented |
     | B | Keep and document | as A, plus a note naming the limits, their counts and the bound reading | the source's task; the inactive end of the screen stays; meets the document-or-drop rule | RMSE still scores bounds as exact values |
     | C | Drop the rows at the limits | about 654 rows leave (about 5,050 remain) | only measured potencies | most inactive compounds go, so the screen loses its inactive end; a few exact values go too (3 of 36 in the sample) |
     | D | Recover the bounds from ChEMBL 17 | take each compound's activity records from the ChEMBL 17 release and drop or flag the medians that rest on bounds | exact | needs the release's full activity table; departs from the source's file; drops inactives as C does |

   * **Recommendation:** B: the bounds are the source's own reading of the inactive compounds, the screen needs them,
     and the note tells a benchmark user that a tenth of the targets are bounds. **Decision:** A, B, C or D?

   **Notes for the AI:** on B, a `curation_comments` bullet: "Assay limits: 654 targets (11.5%) sit at round
   limits (pXC50 4.30: 348, 5.00: 204, 4.00: 81, 4.70: 21); in a sample of 36, ChEMBL holds 31 only as bounds ('>'
   the top concentration tested), so these are upper bounds of the potency stored as exact values, as in the
   Meta-QSAR file (LEAK-26: documented)"; `fit_reason` may add "a tenth of the potencies are assay limits". On C,
   drop the rows whose target equals one of the four limits in `_clean` and rerun the probes. On D, take a database dump
   of the release from the EBI FTP (`pub/databases/chembl/ChEMBLdb/releases/chembl_17/`) and join its `activities`
   (`standard_relation`) on the compound ids for CHEMBL204.

   [^1a]: **LEAK-26** (Must): a target capped at a maximum (a price of 500001, a timeout): drop the capped rows or
     document the cap.
   [^1b]: molecules.md, "Use case, targets and metrics": censored values are no regression target (the NCI screen's
     EC50 was not reached in 38,048 of 39,365 rows).

   **Answer (AI, 2026-11-06):** a finding for this decision from the review of the split by time (issue 2).

   * **Where the limits come from:** 287 of the 654 targets at round limits (44%) belong to 494 compounds whose only
     thrombin record is one PubChem BioAssay deposit (ChEMBL document CHEMBL1201862, "PubChem BioAssay data set",
     loaded into ChEMBL 9 in January 2011, no year of its own). 58% of those compounds sit at a limit (mean pXC50
     5.04), against 6.6% of the compounds from journal papers; in the file they fill positions 70% to 90%.
   * **What it changes:** the bounds are mostly one screen's inactive end rather than series tested to their own top
     concentration, so an option to drop that deposit (494 rows) would remove nearly half the bounds and leave the
     papers' potencies. The options as written stand; B's note can name the deposit. Counts from today's ChEMBL web
     service (activities of CHEMBL204, 2026-11-06), script in `~/claude_jobs/time_review/qsar_tid_11/`.

   **Andrej (2026-11-11, change):** Option B: Keep and document.

   **Resolved (2026-11-11, Andrej):** B. The 654 rows stay as exact values and `curation_comments` has the assay-limit
   bullet: the four limits with their counts, the sample of 36 (31 bounds, 3 exact, 2 not found), the LEAK-26 reading,
   and the deposit's share (306 of the 654, 47%; 59% of CHEMBL1201862's 518 compounds sit at a limit against 6.7% of
   the rest, mean pXC50 5.01 against 6.36). `fit_reason` now ends "a tenth of them are assay limits stored as exact
   values".

2. **Time basis and split: split by first publication year, or keep the scaffold split as `Timeless`?**

   * **Problem:**
     - Under the shipped scaffold split 58% of the test compounds keep a close training analog, and 85% to 90% of
       those analogs were first published in the same year as the test compound, so the folds hold out ring
       skeletons, not the series of a paper.
     - The compounds were first published from 1992 to 2013, and ChEMBL dates 4,972 of the 5,704 through the
       compound ids the file carries; the record says `Samples: No Time Dimension` and the definition names no time
       basis, while its use case screens candidates before they are made.
     - On the same compounds, untuned LightGBM scores RMSE 0.68 to 0.90 out of fold under the scaffold split and 1.11
       to 1.31 when each window is predicted from the compounds published before it: split by year, or keep the
       scaffold split named `Timeless`[^2a]?
   * **Background:**
     - The use case is the definition's: "a medicinal chemist screens candidate molecules for activity on one protein
       target before making and testing them"; the split text says the test "stands for compounds of series not
       measured yet". A potency is a fixed property of the compound, so `Timeless` fits the target; what the time
       moves is which compounds exist, the series of each period. The field tests prospective use with a split by
       time (Sheridan RP, Time-split cross-validation as a method for estimating the goodness of prospective
       prediction, J Chem Inf Model 2013;53(4):783-790, https://doi.org/10.1021/ci400084k).
     - The first year is the earliest year of a compound's thrombin records among ChEMBL documents up to 2013 (ChEMBL
       17's year). Undated: 494 compounds of one PubChem BioAssay deposit (loaded into ChEMBL 9, January 2011; issue
       1's answer) and 238 without a thrombin record in today's ChEMBL, which ChEMBL 17's own tables would date.
     - Mean potency by first year: 6.66 up to 1995, 6.54 in 1996-2000, 6.22 in 2001-03, 6.33 in 2004-06, 6.09 in
       2007-09, 6.40 in 2010-11, 5.81 in 2012-13. The curation note's drift along the file order (6.8 to 5.6) is
       mostly the PubChem deposit at positions 70% to 90%; the file position follows the first year only loosely
       (Spearman 0.48). Only 5.1% of the compounds have a record from a later year than their first, so later papers
       seldom move a median label.
   * **Experiments:** the 4,972 dated compounds, four windows by first year, each trained on every compound first
     published before it; the shipped-like split is 3 x 3 scaffold-grouped folds over all 5,704 compounds, scored on
     the same window compounds; the recommended SMILES encoding, untuned LightGBM and random forest, RMSE; a close
     analog is a training compound at Tanimoto 0.7 or more (Morgan radius 2); Slurm jobs 1366166 and 1366180:

     | Test window (first year) | Compounds | Earlier compounds (share of dated) | Scaffold split: LightGBM | Random forest | Close analog | By year: LightGBM | Random forest | Close analog |
     |---|---|---|---|---|---|---|---|---|
     | 2004 | 373 | 3,105 (62%) | 0.681 | 0.712 | 63% | 1.111 | 1.185 | 15% |
     | 2005-06 | 523 | 3,478 (70%) | 0.901 | 0.951 | 75% | 1.201 | 1.206 | 20% |
     | 2007-08 | 488 | 4,001 (80%) | 0.904 | 0.923 | 62% | 1.305 | 1.249 | 12% |
     | 2009-13 | 483 | 4,489 (90%) | 0.839 | 0.913 | 67% | 1.135 | 1.250 | 26% |

     - What makes the difference: trained on as many compounds drawn from all other years (later ones included,
       scaffolds allowed) instead of the earlier years, LightGBM scores 0.859, 1.156 and 1.219 on the first three
       windows; so the same year's siblings carry most of the scaffold split's advantage, and later papers the rest
       (0.25 in 2004, 0.05 to 0.09 after).
     - The scaffold split's training side is about 3,800 compounds, between the windows' 3,105 and 4,489.
   * **Effect on the task:** the scaffold split rewards recognising a test compound's siblings of the same year, most
     likely from its own paper, which a chemist screening a new candidate does not have; the forward split keeps the earlier compounds of a
     continued series (12% to 26% close analogs), as a chemist would.
   * **Consistency:** sdss_17 issue 2 recommends a split by the date of the measurement for a fixed property (the
     class of a sky object) whose catalogue drifts with time; the molecule amendment chose scaffolds for chemicals
     whose dates are unknown, which is not the case here[^2b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Scaffold split, no time basis (implemented) | as now | nothing to change | no stated reason why a split that is not temporal is safe in time; trains on same-paper siblings |
     | B | Scaffold split, `Timeless` | as now; the tag and a `Time basis:` line that the potency is fixed and that the folds keep same-year siblings (58% close analogs, 85-90% same year) | the molecule rule's split; nothing new to build | the measured siblings stay; the line states a gap the split does not close |
     | C | By first publication year | the first year joined from ChEMBL 17; windows of one to five years from 2004, each trained on every earlier compound | the use case over time; removes same-paper siblings and later papers; the field's prospective test | a join to ChEMBL's documents; 494 deposit compounds need a year (their 2011 load) |
     | D | Grouped by first document | each compound grouped with its first ChEMBL document (paper or deposit) | holds whole papers out with the source's own key, no windows | still trains on later papers; drops the continued series a chemist would have |

   * **Recommendation:** C: the dates are recoverable, the use case is prospective, and the scaffold split leaves most
     test compounds a close analog first published in the same year. If the scaffold split stays, B, with the gap in its line.
     **Decision:** A, B, C or D?

   **Notes for the AI:** on C, in `_prepare_raw_files` add each compound's first document year from ChEMBL 17's
   `activities` and `docs` tables for CHEMBL204 (the release dump on the EBI FTP), or embed a one-off extract as
   the salt ids are; the PubChem deposit takes 2011 (its load into ChEMBL 9, when a modeller could have it); a
   `first_year` column, a feature as in the other temporal tasks; `temporal = Temporal(on="first_year",
   splits=TemporalSplits(window=None, unit="unique", ...))` with windows widened to at least about 50 compounds and
   every training side at 50% or more (the four measured windows are one choice); `grouping`, the `scaffold` column
   and the scaffold bullet's split claims go (the analog numbers stay as background); task summary `split` and
   `fit_reason`; a curation bullet with the table; record `required_split: Temporal (NON-IID)` and issue 3's facts;
   `dataset check`, CHANGELOG, record CC with `Andrej` in `checked_by`. On B, once PR #50 is in: `data_tags =
   ("Timeless",)` and a bullet `- Time basis: Timeless: a compound's potency is a fixed property; the compounds were
   first published 1992-2013, and the scaffold folds keep siblings of the same paper (58% of test compounds have a
   close training analog, 85-90% of them first published the same year), so the split is optimistic for new
   series: by first publication year LightGBM's RMSE is 1.11-1.31 against 0.68-0.90.` On D, `Grouping(on=
   "first_document", labels="per_sample", ...)` from the same join.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows (`Timeless`: the target
     is a fixed property of the item; the split is random or grouped by item family). When samples arrive over time
     and that moves the target, how often it occurs or its relation to the features, and the time is dated, the split
     is temporal. **SPLIT-7** (Must): a missing or hidden timestamp does not make a task IID. **SPLIT-1** (Must): the
     split is the one that most closely mirrors the real-world application.
   [^2b]: **SPLIT-31** (Should), as amended 2026-10-26 (Lennart): a molecule dataset whose rows carry exact
     structures groups on the Bemis-Murcko scaffold, as a new chemical often comes from a series not yet measured
     (qsar_tid_11, 2026-11-01). **SPLIT-14** (Must): at least 3 windows, none training on less than half the data;
     **SPLIT-17** (Should): widen windows below about 50 test rows. **SPLIT-24** (Must): group on a true group id.

   **Andrej (2026-11-11, change):** Option C: By first publication year.

   **Resolved (2026-11-11, Andrej):** C. `first_year` is joined from the ChEMBL 17 release dump (sqlite, EBI FTP;
   sha256 58432fcc...d2c0): the earliest year among the documents of a compound's CHEMBL204 activity records. All
   5,704 compounds are in that table, 5,186 in a dated document (1992-2013); the other 518 appear only in the undated
   PubChem deposit CHEMBL1201862 and take 2011. The extract ships as `chembl_17_first_year.csv` next to `dataset.py`,
   so a build does not need the 2 GB dump; the query is in the split bullet of `curation_comments`. The column is a
   feature as well as the time column. `Temporal(on="first_year", splits=TemporalSplits(window=None, unit="unique",
   n_windows=5, min_train_fraction=0.5), horizon=2, horizon_unit="years")` cuts the newest half of the 22 publication
   years into five windows of two: 2012-13 (159 compounds), 2010-11 (744), 2008-09 (290), 2006-07 (598), 2004-05
   (633), trained on 5,545, 4,801, 4,511, 3,913 and 3,280 earlier compounds (97% to 57% of the rows). `grouping`, the
   `scaffold` column and the scaffold bullet's split claims are gone, the analog numbers stay as background.

   The comparison above was re-measured on these windows and all 5,704 compounds (Slurm jobs 1378119 and 1378141,
   2026-11-11), since the four windows of the table were dated from the web service with the deposit left out; the
   shipped-window numbers are now the table in `curation_comments` and the four-window one is one line of context.
   LightGBM RMSE, scaffold-grouped out-of-fold against the forward split, on the same compounds:

   | Test window | Compounds | Train | Scaffold split | Close analog | By year | Close analog |
   |---|---|---|---|---|---|---|
   | 2004-05 | 633 | 3,280 | 0.844 | 67% | 1.502 | 18% |
   | 2006-07 | 598 | 3,913 | 0.800 | 72% | 1.049 | 14% |
   | 2008-09 | 290 | 4,511 | 1.038 | 58% | 1.184 | 30% |
   | 2010-11 | 744 | 4,801 | 0.804 | 24% | 1.248 | 6% |
   | 2012-13 | 159 | 5,545 | 0.812 | 71% | 0.894 | 20% |

   The scaffold split is easier on every window, and 71% to 93% of its close analogs were first published in the same
   year as the test compound. At an equal training size drawn from all years, LightGBM scores 1.281 (no test
   scaffold) and 1.305 (at random) on 2004-05 against the shipped 1.502, and within 0.08 of the shipped number on
   the later windows, where few or no compounds are published after the window: on this layout the scaffold split's
   advantage is the same-year siblings, not the later papers.

   Probes re-run on the shipped windows: task probes no flag (LightGBM R^2 0.350, skill +0.419, ahead of the dummy
   on all five windows; random forest 0.313; selected linear 0.138; plain linear -0.409). Leak probes: no exact
   feature copy across the split (0.0%), best single feature R^2 0.055 against 0.449 for all features; probe 13 reads
   a mild shift at the end (newest three years pooled, mean z -3.7), the drift the temporal split is for.
   `hidden_groups`: 61 candidates, 0 hits. `group_probes` no longer applies ("not a grouped task"). `dataset check`:
   0 errors, 0 warnings, 1 info (`meta_time_horizon_unit` cannot cross-check an integer year column against a
   calendar horizon).

3. **Correct the record's collection facts: compounds published over time, dated through ChEMBL?**

   * **Problem:**
     - The compounds entered the literature from 1992 to 2013, and ChEMBL keeps each record's document year, so the
       time is recoverable through the compound ids the file carries (4,972 of 5,704 from today's ChEMBL, the rest
       from ChEMBL 17's tables or the 2011 load of one deposit).
     - The record carries `Samples: No Time Dimension`, the fact for designed runs or a catalogue whose make-up does
       not depend on when an item was measured; here the series and the potency level move with the year (issue 2).
     - Set `Samples: Over Time` and `Time: Dated`, with no target fact[^3a]?
   * **Background:** the label is a median over a compound's measurements in ChEMBL 17; only 5.1% of the compounds
     have a record from a later year than their first, so the arrival study's reading of a target revised later
     holds for few rows, and the potency exists with its measurement.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Samples: No Time Dimension` (implemented) | as now | the potency of a compound does not depend on the year | hides a dated literature stream whose series move with the year |
     | B | `Samples: Over Time`, `Time: Dated` | the record's tag replaced and the time fact added | the source as it is; agrees with issue 2's measurements | none found |
     | C | As B, plus `Target: Revised Later` | the target fact added | names the median over later measurements | true for 5.1% of the compounds only |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B, in the record's `tags`: `'Samples: No Time Dimension'` becomes `'Samples: Over Time'`,
   plus `'Time: Dated'` (and `'Target: Revised Later'` on C); `Andrej` added to `checked_by`.

   [^3a]: **SPLIT-32** (Should): the record's collection facts: `Samples: No Time Dimension` (designed runs, or a
     catalogue of properties where it plays no role when an item was measured) or `Samples: Over Time`; for samples
     over time `Time: Dated` when the release or its source keeps the time or lets us recover it; `Target: Revised
     Later` when the target is assigned, then updated or propagated.

   **Andrej (2026-11-11, change):** Option B: Samples: Over Time, Time: Dated.

   **Resolved (2026-11-11, Andrej):** B. The record's tags are `Samples: Over Time` and `Time: Dated` in place of
   `Samples: No Time Dimension`, with no target fact; `required_split` is Temporal (NON-IID) and the split tag
   Non-IID (Temporal) (issue 2). The reading is a bullet in `curation_comments` as well.
