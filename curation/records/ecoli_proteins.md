---
unique_name: ecoli_proteins
name: ecoli
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Outdated
tags:
- Tiny Data
collections:
- TabArena Reject
original_source: UCI
year: '1996'
domain: biology & life sciences
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://github.com/EpistasisLab/pmlb/blob/master/datasets/ecoli/metadata.yaml
- https://doi.org/10.24432/C5388M
notebook_path: datasets/beyond_iid/new_iid/ecoli_proteins/ecoli_proteins.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/ecoli_proteins/dataset.py
source_row: 754
type_adapter_id: curation-record-v1
---

## Comments

Has some minor classes that might not be dropped for proper validation setup. Might be outdated, otherwise seems to be still an okay task from the time

need to check sequence names again

CC (2026-10-19, Andrej): Keep, with `aac` dropped (stratified 3-fold x 20).

Changed:
- Dropped `aac` (in `dataset.py`): a leak, as in `yeast` (crit. 4D). It is a discriminant-analysis score (linear classifier fitted to the labels) separating outer-membrane from periplasmic proteins, fitted on the authors' database that preceded this dataset (Nakai & Kanehisa 1991). Without it, outer-membrane (`om`) recall falls from 0.90 to 0.02 and TabPFN log loss rises from 0.359 to 0.462.
- Marker `Outdated`: the features are 1996 scores from older sequence programs; today's localisation tools work from the sequence itself.

Noted, no action (not severe):
- Arbitrary labels: `im` vs `imU` (inner membrane without/with an uncleavable signal sequence, a sorting tag at the protein's start) causes over half the errors and log loss; the authors call the split "somewhat arbitrary" (Horton & Nakai 1997). A noise floor shared by all models.
- Without `aac`, no feature identifies `om` (6% of rows), and TabPFN (0.462) beats LR (0.476) on only 68% of splits. A shared floor, and models are still ranked.
- Labels: 283 of 287 proteins keep their location in today's UniProt; 27 of 336 names no longer resolve.
- `lip` is constant in 324 of 327 rows. Kept: a real, if weak, feature.

References: Nakai K, Kanehisa M. Expert system for predicting protein localization sites in gram-negative bacteria. Proteins. 1991;11(2):95-110. doi:10.1002/prot.340110203. Horton P, Nakai K. Better prediction of protein cellular localization sites with the k nearest neighbors classifier. Proc Int Conf Intell Syst Mol Biol. 1997;5:147-152. PMID: 9322029.

## Reference

@inproceedings{horton1996probabilistic,
  title={A probabilistic classification system for predicting the cellular localization sites of proteins.},
  author={Horton, Paul and Nakai, Kenta},
  booktitle={Ismb},
  volume={4},
  pages={109--115},
  year={1996},
  organization={St. Louis, Missouri, USA}
}
