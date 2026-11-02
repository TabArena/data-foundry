---
unique_name: chandra_csc_xray_source_classes
name: 'MUWCLASS training dataset: Chandra Source Catalog v2 X-ray sources with established classes'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
year: '2022'
domain: physics & astronomy
required_split:
- Random (IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.3847/1538-4357/ac952b
- https://github.com/huiyang-astro/MUWCLASS_CSCv2
- https://arxiv.org/abs/2206.13656
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the released training set of the MUWCLASS classifier, 2,941 Chandra X-ray sources with classes from the literature and X-ray, Gaia, 2MASS and WISE properties, an 8-class astronomy task (physics and astronomy has no accepted dataset); small classes (26 HMXB, 44 CV) and labels only for confidently classified sources.
- Source: Yang, Hare, Kargaltsev, Volkov, Chen, Rangelov, "Classifying Unidentified X-ray Sources in the Chandra Source Catalog Using a Multiwavelength Machine-learning Approach", ApJ 941:104, 2022 (arXiv:2206.13656); data on GitHub huiyang-astro/MUWCLASS_CSCv2 (`files/TD.csv`, the AAS machine-readable `files/TD_MRT.dat`, and the raw `files/CSC_TD_MW_remove.csv` with more properties; no licence on the page). As published (Sec. II.1, Table 1): 2,941 sources, AGN 1,390, YSO 1,004, LM-STAR 207, HM-STAR 118, NS 87, LMXB 65, CV 44, HMXB 26; the final model uses 29 features (Sec. IV.3, Table 2): four X-ray fluxes, three hardness ratios, two variability probabilities, Gaia G, BP, RP, 2MASS J, H, K, WISE W1, W2 and twelve colours. Labels from the literature and catalogues; candidates, ambiguous SIMBAD types and crowded fields (globular clusters, LMC and SMC, Galactic centre) removed.
- Use case: X-ray astronomers classify the unidentified sources of the Chandra Source Catalog (the paper classifies 66,369 CSCv2 sources, about 21%) to pick candidates for follow-up, such as high-mass X-ray binaries and counterparts of H.E.S.S. TeV sources (abstract); fit approximate: the training sources are confidently classified ones outside crowded fields, while the use case predicts for the unidentified rest (`Selection Bias`). Regime IID over sources (the paper uses leave-one-out, Sec. IV.1; no grouping).
- Siblings and duplicates: none in `curation/records/` (searched Chandra, MUWCLASS, X-ray source); astronomy siblings `sdss_17` (`Yes`) and `desi_dr1_star_galaxy_quasar` (`TBD -> Yes`, 3) are other tasks. External collections: none found.
- Better data: from the gap scout for physics and astronomy; no further search this round.
- Papers and pages: the ApJ paper (arXiv abstract and HTML, Secs. II to IV); the GitHub README (`codes/builtTD` rebuilds the training set).
- Metric: the paper reports accuracy, balanced accuracy, macro F1 and MCC (Sec. IV.2), compares algorithms by macro-averaged ROC AUC (Sec. IV.4) and shows per-class recall and precision (Sec. IV.5): several, none named as the criterion, so the fallback `log_loss` (MET-5, MET-8); inputs none.
- Risks for /add-dataset: drop any model-output columns (class probabilities, predicted class, confidence); 26 HMXB and 44 CV give about 5 and 9 per test fold under 5 folds (TP-5, TP-8 to check; merge classes only where the source supports it); structured missingness where counterparts are absent; labels from mixed literature (Class_ref); several Chandra observations of one source are merged into one row (Sec. II.2).
- Priority: gap + (physics and astronomy, multiclass), use case + (the paper names the follow-up selection), source + (ApJ paper and repository), shape 0 (2,941 sources, all numeric, two classes near the size floor), risk - (confident labels only, tiny classes).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for physics and astronomy.
- as published: X-ray sources: 2,941 sources x 63 columns (TD.csv): CSCv2 soft, medium, hard and broad fluxes, intra- and inter-observation variability probabilities, Gaia, 2MASS and WISE magnitudes, parallax, ...; target: True_Class (8 classes), established in the literature (Class_ref); access: open.
- Why: A released training set with a published ML task (random forest), real observations, labels from the literature
- Adds: Multiclass astronomy with structured missingness (absent optical or infrared counterparts). Risks: drop the model-output columns (P_*, Class, Class_prob, CT); small (2,941) and imbalanced; no licence stated on GitHub
