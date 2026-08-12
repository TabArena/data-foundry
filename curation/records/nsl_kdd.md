---
unique_name: nsl_kdd
name: NSL-KDD
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Duplicate
- Outdated
tags:
- AI-Filled (Verify)
original_source: Website
year: '2009'
domain: technology & internet
required_split:
- Custom
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/hassan06/nslkdd
- https://github.com/defcom17/NSL_KDD
- https://web.archive.org/web/20100224055243id_/http://nsl.cs.unb.ca/NSL-KDD/KDDTest+.txt
- https://www.unb.ca/cic/datasets/nsl.html
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

⚠️ **AI-FILLED — UNVERIFIED**: this record was triaged by an AI (2026-08-12) and no human has
verified it. Check the verdict and the fields before relying on them.

Deduplicated, difficulty-resampled cut of [[kddcup99]], published by Tavallaee et al. (CISDA 2009) to
fix that dataset's two measured defects (78%/75% duplicate rows; saturation). Shipped as flat files:
KDDTrain+ 125,973 x 43 and KDDTest+ 22,544 x 43, plus KDDTrain+_20Percent (25,192) and the harder
KDDTest-21 (11,850). 43 columns = 41 features + label + a difficulty score. Labels: 23 in train, 38 in
test (17 attack types test-only), so binary attack-vs-normal is the only well-posed framing.

**Suggested No, inherited from the parent:** the rows are still the scripted MIT Lincoln Labs
DARPA'98 simulation (criterion 4B) — dedup does not touch that, and the authors concede it (Sec. VI:
"still suffers from some of the problems discussed by McHugh and may not be a perfect representative
of existing real networks"). It is also a cut of an existing record, not a new source. Counter-case if
revisited: it does fix the duplicates and the triviality, and the prescribed KDDTrain+/KDDTest+ split
is the only usable protocol — the difficulty-stratified resampling destroys any recoverable time
order, so a random split is not an option.

**Leak trap:** the 43rd column is Tavallaee's `#successfulPrediction` count (0-21) — how many of 21
supervised classifiers predicted that row's label correctly (their Tables III/IV). Label-derived;
never usable as a feature.

**Source status:** the official page is withdrawn — <https://www.unb.ca/cic/datasets/nsl.html> states
"We apologize, this dataset is no longer available", and the old http://nsl.cs.unb.ca/NSL-KDD/
redirects there. Use the mirrors in source_links: the Kaggle and GitHub copies are byte-identical to
each other, and their KDDTest+ is byte-identical to the Wayback capture of the original UNB URL.
Wayback alone is not enough — it holds KDDTest+, KDDTest-21 and KDDTrain+_20Percent but **not** the
full KDDTrain+.

## Reference

Tavallaee, M., Bagheri, E., Lu, W., Ghorbani, A. A., "A Detailed Analysis of the KDD CUP 99 Data
Set", Proceedings of the 2009 IEEE Symposium on Computational Intelligence for Security and Defense
Applications (CISDA), 2009 — <https://www.ecb.torontomu.ca/~bagheri/papers/cisda.pdf>

The dataset it is derived from, and the critiques that motivated it, are collected on [[kddcup99]].
