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
suggestion: 'Yes'
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
original_source: UCI
year: '2013'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1494
- https://doi.org/10.24432/C5H60M
notebook_path: datasets/beyond_iid/old_iid/qsar_biodeg/qsar_biodeg.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/qsar_biodeg/dataset.py
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

CC (2026-11-13, Andrej): time basis `UnseenGroup` instead of no prototype tag (2026-11-12):
- The use case aims at groups the data does not hold, which the held-out groups of the split stand for; `UnseenGroup` (SPLIT-32, the question before the prototypes) names that, where `Timeless` named the target and "no tag" named nothing.
- The split does not change; the definition's `Time basis:` line keeps the measured evidence.

## Reference

Mansouri, K., Ringsted, T., Ballabio, D., Todeschini, R., Consonni, V. (2013). Quantitative Structure - Activity Relationship models for ready biodegradability of chemicals. Journal of Chemical Information and Modeling, 53, 867-878
