---
unique_name: physiochemical_protein
name: physiochemical_protein
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
- Missing source information
original_source: UCI
year: '2013'
required_split:
- Random (IID)
source_links:
- https://www.openml.org/search?type=data&id=44963
- https://doi.org/10.24432/C5QW3H
notebook_path: datasets/beyond_iid/old_iid/physiochemical_protein/physiochemical_protein.ipynb
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Sounds like a domain-specific prediction task. There might be clusters in the data as teh description says "There are 45730 decoys and size varying from 0 to 21 armstrong". Also the data was taken from CASP 5-9  - which could indicate different experiments

Potential issue: little source information

Lennart: No objection but also too little source information

Andrej: Seems fine

**Assessment (AI, 2026-10-06):** hidden groups that cannot be recovered. The rows are decoys (predicted structures) of CASP 5-9 target proteins; the use case, judging the models of a new target, needs new targets at test time. The groups clearly matter: 1,756 rows repeat another row's features, a decoy's nearest neighbour is about 18 times closer than a random pair with a median RMSD difference of 0.52 A (5.77 A for random pairs), and holding out similarity clusters (a diagnostic only) drops LightGBM's R^2 from 0.593 to 0.40-0.51. But no copy has a target id (UCI, OpenML 42903 and 44963, the Kaggle copy), the file order is shuffled, and no paper describes this 9-feature file. The authors' later release (Rana et al. 2015, J Bioinform Comput Biol 13:1550005; supplement RF-PCP on sourceforge.net/projects/rf-pcp) names each decoy file (CASP round and target, e.g. CASP10_T0719_PconsD_TS5.pdb; 342 CASP targets from CASP5-10 plus other decoy sets) but has other features (Area, ED, Energy, SS, SL, PN, with RMSD, TM, GDT) and cannot be joined to these rows (13 rows match on RMSD and area). The target column is RMSD of the decoy against the native structure (A), not a residue size. Precedent (maternal_health_risk): real groups that cannot be recovered mean retirement. RF-PCP could be triaged as a new candidate, grouped by target.

CC (2026-10-06, Lennart): Retired: the rows are decoys of CASP target proteins, the use case needs new targets at test time, and no copy of this file says which target a decoy belongs to (evidence in the assessment above), as for maternal_health_risk. The authors' RF-PCP release (Rana et al. 2015) has target ids but other features; it could be triaged as a new candidate.

## Reference

Rana, P. (2013). Physicochemical properties of protein tertiary structure data set.
