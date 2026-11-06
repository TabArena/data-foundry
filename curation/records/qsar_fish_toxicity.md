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
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- Timeless
original_source: UCI
year: '2015'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
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

## Reference

Cassotti, Matteo, et al. "A similarity-based QSAR model for predicting acute toxicity towards the fathead minnow (Pimephales promelas)." SAR and QSAR in Environmental Research 26.3 (2015): 217-243.
