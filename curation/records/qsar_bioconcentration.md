---
unique_name: qsar_bioconcentration
name: QSAR_BIOCONCENTRATION
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
tags:
- Non-IID (Grouped)
collections:
- TabSTAR
original_source: UCI
year: '2016'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C56S46
- https://www.kaggle.com/datasets/ishandutta/qsar-bioconcentration-classes-data-set
- https://michem.unimib.it/download/data/
v2_path: datasets/_dev/tabarena-v0pt2/qsar_bioconcentration/dataset.py
source_row: 683
type_adapter_id: curation-record-v1
---

## Comments

Need to understand if class or regression target should be used and how they differ

Contains SMILES string that might need preprocessing in some expert way, or we drop as done by prior work

Data in paper sounds very different to data we have from Kaggle/UCI. We only have the version after feature selection

Super hard to parse if the dataset could be used but I think we can train a model to do so. Might still have problems and result in leaks but worth including for now

**Assessment (AI, 2026-10-07):** Added as the 3-class task of UCI 510 (458 / 64 / 254 chemicals). The class is read from logBCF and the experimental logKOW (Env. Int. SI Sec. 1); an inferred band of ±0.5 log units around the TGD line reproduces 600 of 607 classes with logKOW ≥ 1. So logBCF is dropped, and no descriptor completes the rule. The 779 are the chemicals of the 2015 table (1,056) with an experimental KOW. Benzene/cyclohexane, naphthalene/tetralin and chlorobenzene/chlorocyclohexane carry each other's SMILES and descriptors: swapped back (2015 SI table); triticonazole and two dioxins dropped. SMILES kept as a string. Alternative target: logBCF regression (random forest R² 0.72).

CC (2026-10-14, Lennart): Drop the SMILES as a feature, as in every SMILES dataset, and add RDKit's 2D descriptors next to the 9 Dragon descriptors.

**Assessment (AI, 2026-10-14):** LightGBM macro AUC 0.735 with the 9 descriptors, 0.752 with RDKit's 193 added (better on 13 of 15 splits), 0.723 with the SMILES as text instead. With RDKit's descriptors no two chemicals share their values; with the 9 alone 61 did, 14 of them with another class.

**Assessment (AI, 2026-10-20):** priority 3 for the review of the added dataset: gap + (problem_type multiclass_classification), use case -, source +, shape -, no known risk. Small (776 chemicals) multiclass QSAR task with repaired rows and documented source; the use case is curated.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; add the logKOW the class is read against as an input or rewrite the use case, `approximate` unless that and a drop of the 9 selected Dragon descriptors remove both gaps, and drop the 9 by LEAK-31 (open issues 8, 9, 5 in REVIEW.md). Applied in the definition: the split text (the SMILES gives exact Murcko scaffolds; 34% of chemicals in 42 congener series, random forest 0.754 to 0.650 with them held out; a SPLIT-31 candidate), the selection note corrected (at most about 0.015 macro AUC is the selection; the home_credit citation removed), the label provenance (122 shipped chemicals have a predicted logKOW in the 2015 table, so the 2026-10-07 statement that the 779 all have an experimental KOW holds only for the 2016 re-curation), the LightGBM numbers as reproduced (0.745 / 0.757). TabSTAR's copy (OpenML 46585) swaps the names of classes 2 and 3, a problem of that copy; our labels follow the archived UCI page and the rule. The tag `Free Text (Short)` is stale (no string feature since 2026-10-14), and the open issues replace the 'no known risk' of the earlier 2026-10-20 line. Priority 2: gap +, use case -, source +, shape -, risk - (multiclass is thin; the use case is the curation's and its fit is contested; Grisoni et al. document the data; 776 chemicals; an input the actor holds is missing and a potential leak is kept).

**Assessment (AI, 2026-10-20):** the 'no known risk' of the first 2026-10-20 line no longer holds: the open issues of REVIEW.md (the logKOW input, the fit label, the 9 selected descriptors) are the known risks. Evidence task, not an issue: read Grisoni et al. 2016 (Environment International 88) for the class thresholds, which are inferred from the data (600 of 607 chemicals with a logKOW of at least 1) and match the archived UCI page.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: B02(C-N) and the 24 RDKit fragment counts that hold only 0 and 1 (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: B02(C-N) (presence of a C-N pair at topological distance 2). Reverted: the 24 RDKit fragment counts that hold only 0 and 1.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Grisoni et al. (2016) report NER (balanced accuracy) with per-class rates at argmax, no costs. Original rejected: NER.

CC (2026-10-26, Lennart): the `Free Text (Short)` tag is removed, as the definition has it: no string feature since the SMILES was dropped on 2026-10-14.

CC (2026-10-26, Lennart): issue 8, option (a): add the logKOW with its measured/predicted flag from the authors' 2015 table (USE-6, USE-3: the assessor of the use case holds it before any fish test).

**Assessment (AI, 2026-10-26):** issue 8 applied. `logKOW` and `logKOW_type` come from the Chemosphere SI table (1-s2.0-S0045653515000879-mmc2.xlsx, sha256 53787477...), matched on the CAS numbers of the cell and the logBCF both tables list: 774 of 776 chemicals (652 measured, 122 predicted), 2 missing. dataset check: 0 errors, 0 warnings; task probes: no flags; leak probe: logKOW alone 0.657, no copies. Random forest, macro ROC AUC on 30 of our splits: 0.760 with everything, 0.756 without the logKOW, 0.759 without the authors' 9 descriptors (paired -0.002, SE 0.001). Answers on the page: issue 1 (class or logBCF, raised again), issue 5 (the 9 come from commercial Dragon 6, the pool is unpublished), issue 9 (follows issue 5), issue 10 (a scaffold-grouped split recommended, as drug_induced_autoimmunity_prediction).

CC (2026-10-26, Lennart): issue 1: "let us keep the clf task": the class only, no logBCF regression.

CC (2026-10-26, Lennart): issue 5: "replace with mordred descriptors from the additional source when rebuilding". The authors' 9 Dragon descriptors are dropped (LEAK-31); this supersedes CC 2026-10-14 (RDKit next to the 9) and makes the categorical typing of B02(C-N) (CC 2026-10-21) moot. The Mordred part waits for the consistency answer on the page.

**Assessment (AI, 2026-10-26):** the 9 descriptors are dropped in dataset.py (dataset check: 0 errors, 0 warnings; RDKit's descriptors alone give all 776 chemicals distinct vectors). Mordred measured before adding it: RDKit + logKOW scores macro ROC AUC 0.759 (random forest) and 0.765 (LightGBM) on 3 x 10 folds; adding Mordred's 1,220 2D descriptors that do not copy an RDKit column gives 0.746 and 0.745 (paired -0.013 ± 0.002, -0.020 ± 0.003). The precedent check finds Mordred a departure from CLEAN-24 and the scaffold split (issue 10) a drift from qsar_oral_toxicity, whose stated reason (structures linked by row order) no longer holds; both are asked on the page.

CC (2026-10-26, Lennart): issue 5, option (b): RDKit's descriptors and the logKOW only, no Mordred "for now"; the background on Mordred goes into data_foundry.v2.chemistry, "to revisit if we want to add them at scale".

CC (2026-10-26, Lennart): issue 10, option (d): SPLIT-31 amended, molecule datasets with exact structures group on the Bemis-Murcko scaffold (ring-less molecules and a scaffold of more than a tenth of the molecules alone), "and also do the right split for oral". Issue 9: `direct`.

**Assessment (AI, 2026-10-26):** issues 5, 9 and 10 applied: no Mordred (its background is in data_foundry.v2.chemistry); scaffold groups (`scaffold_groups`: 104 ring-less and 262 bare-benzene chemicals alone; test folds of 188-345 chemicals); fit `direct` (6.4% of the test chemicals have a training analog at Tanimoto 0.7 or more, 12.6% at random). dataset check: 0 errors, 0 warnings. The task probes flag `unstable`: random forest macro ROC AUC 0.673 (0.756 under IID), log-loss skill +0.068, beating the class shares on 77% of the splits; 7 to 30 rows of the rarest class per test fold. Checked against a stronger model (TP-1): TabPFN v3.5 log loss 0.786 against 0.888 for the class shares (skill +0.118), macro ROC AUC 0.708, better on 26 of 30 splits. A weak but real signal (TP-2). No open issue left.

CC (2026-10-26, Lennart): verdict ship.

## Reference

@article{grisoni2016investigating,
  title={Investigating the mechanisms of bioconcentration through QSAR classification trees},
  author={Grisoni, Francesca and Consonni, Viviana and Vighi, Marco and Villa, Sara and Todeschini, Roberto},
  journal={Environment international},
  volume={88},
  pages={198--205},
  year={2016},
  publisher={Elsevier}
}
