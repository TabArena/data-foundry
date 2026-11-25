---
unique_name: esophageal_cancer_sponge_cytology
name: Oesophageal cancer screening by sponge cytology, high-risk lesion (Gao et al. 2023)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Image
tags:
- AI-Filled (Verify)
year: '2023'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://github.com/Gaooooye/Esophageal-cAncer-Screening-Trial
- https://doi.org/10.1016/S2468-1253(23)00004-3
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `No` (`Image`, SEL-13): high-risk oesophageal lesions detected from sponge-cytology slides, where 105 of the 120 model features are nuclear morphometry and grey-level descriptors from the automated slide-analysis pipeline, beside 15 epidemiological columns and a cytologist's reading of the same slide; image descriptors used to recognise what the slide shows.
- Source: Gao, Xin, Lin, Yao, Zhang, Zhou et al., "Machine learning-based automated sponge cytology for screening of oesophageal squamous cell carcinoma and adenocarcinoma of the oesophagogastric junction: a nationwide, multicohort, prospective study", Lancet Gastroenterol Hepatol 8:432-45 (2023), https://doi.org/10.1016/S2468-1253(23)00004-3 (EAST trial, NCT04609813; abstract read, full text paywalled). Data: https://github.com/Gaooooye/Esophageal-cAncer-Screening-Trial (`train.csv` 7,899 rows, `test.csv` 6,698 rows from other hospitals, prevalence 2.5% and 1.9%, diagnoses January 2021 to June 2022; no licence, the GitHub API returns `license: null`). Arasteh et al. 2024 and Shaktah et al. 2026 used these files as published.
- Decisive: the abstract, "The predictive features included 105 cytological and 15 epidemiological features"; the repo's `Feature explanations.xlsx` names f1-f105 as descriptors such as "Nuclear grayscale mean", "Edge gradient integral (E) mean", "Ellipse resemblance mean", "Four-quadrant grayscale variance mean" and "DNA index mean", per-slide aggregates of per-cell image measurements. SEL-13 names "morphological, geometric or spectral descriptors from an image-analysis pipeline", which "stay image-derived when mixed with a few non-visual columns"; precedents `wdbc` and `zooscan_pelgas_copepods` (`No`, `Image`).
- Steelman (reject-checker, 2026-11-25, the reject stands): the pipeline outputs a table and the source's own model is a gradient-boosted classifier on it, but `wdbc` was the same (Xcyt features, a clinical classifier) and SEL-13 rejects by where the columns come from; the DNA index is integrated optical density per nucleus, an image descriptor, not a SEL-15 reading of the entity; the `Cytology` column is a person scoring the slide (alone AUROC about 0.95 on train and 0.96 on test, the models' level), which SEL-13 also covers, and the SEL-14 exception does not apply because the diagnosis is made from the slide itself.
- Use case: a screening programme refers people with a positive sponge test to endoscopy, a real decision; the scope rule decides here, not the use case.
- Siblings and duplicates: no other record of the EAST trial (grep by sponge, cytology, oesophageal, esophageal, EAST). Another task from the 15 epidemiological columns alone would be a separate risk-factor candidate (endoscopy-defined labels, hospital-disjoint test set, no licence); not screened.
- Better data: none found (data scout, 2026-11-25: the ESMO GI 2024 follow-up and the Cytosponge trials release no data, and Cytosponge targets Barrett's oesophagus).

Candidate from Shaktah et al. 2026, "Established machine learning matches tabular foundation models in clinical predictions", BMC Med Inform Decis Mak 26:364 (https://doi.org/10.1186/s12911-026-03654-3), one of its twelve binary clinical tasks.
