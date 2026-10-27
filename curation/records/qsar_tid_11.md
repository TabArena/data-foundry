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
suggestion: 'Yes'
year: '2015'
domain: chemistry & material science
required_split:
- Random (IID)
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
