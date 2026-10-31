---
unique_name: raman_amino_acids_glycine
name: Amino Acids (Glycine)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- No Good Target / Scientific Discovery
tags:
- AI-Filled (Verify)
collections:
- RamanBench
source_links:
- https://arxiv.org/abs/2011.07470
- https://www.kaggle.com/datasets/sergioalejandrod/raman-spectroscopy
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-3): the release is unlabelled time-resolved LC-Raman frames published for unsupervised analyte detection, and RamanBench's regression target is each frame's time stamp within one elution, not a concentration.
- Source: Kaggle sergioalejandrod/raman-spectroscopy, "Liquid Chromatography Raman Spectroscopy" (files of 2020-10-21, CC BY 4.0): "produced by Hirotsugu Hiramatsu as part of his experiment revolving around the enhancement of Raman signal utilizing a vertical flow method" and "processed by Professor Stefano Rini" (NCTU); paper Rini and Hiramatsu, "An efficient label-free analyte detection algorithm for time-resolved spectroscopy", arXiv 2011.07470, 2020-11-15. As published: AminoAcids_40mM.xlsx (one sheet per amino acid: a Raman-shift column, then one column per frame), four mixture spectra files, a UV file, LCRaman data.xlsx and the manuscript PDF.
- The source's words: "We seek to change the method of analysis of the spectral data. ... Our proposed method utilizes unsupervised learning methods to minimize the requirement of expert and input" (Kaggle, Inspiration); the arXiv abstract frames analyte detection as "an unsupervised learning problem". No concentration label is published.
- Measured on the RamanBench Hugging Face mirror (the target column only): 90 rows whose target runs 4.5, 4.533, 4.567, ... 7.467 in even steps of 1/30, the frame headers of the sheet (times within one elution), which the raman-data loader reads as "concentrations" (`concentrations = np.array(df.columns.values[2:], dtype=float)`). A frame's time within one chromatographic run is no outcome anyone predicts (SEL-3; the original task decides, SEL-8), and the 90 rows are consecutive frames of a single run.
- Siblings and duplicates: the leucine, phenylalanine and tryptophan sheets are aliases of this record, built the same way; no other record of these data. External collections: RamanBench ("Amino Acids (Glycine)" and three more).
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Reject check (AI, 2026-10-31): stands. The source: 'Our proposed method utilizes unsupervised learning methods to minimize the requirement of expert and input' (https://www.kaggle.com/datasets/sergioalejandrod/raman-spectroscopy). The sheet is headed 'Gly, 40 mM', and the loader takes the frame headers as the target (`spectra = df.loc[1:, 4.5:]`, `concentrations = np.array(df.columns.values[2:], dtype=float)`; https://github.com/ml-lab-htw/raman_data/blob/main/raman_data/loaders/KaggleLoader.py): the target is the time of a frame within one elution, which nobody predicts. No concentration label is published.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 90 spectra x 1,024 wavenumber features; 1 target(s) (raman-data id: amino_acids_glycine); target: elution concentration.
- Why: Predict the glycine elution concentration profile from time-resolved LC-Raman spectra | Predict the leucine elution concentration profile from time-resolved LC-Raman spectra | Predict the phenylalanine elution concentration profile from time-resolved LC-Raman spectra | Predict the tryptophan elution concentration ...
- Notes: Raw Raman spectral bins (1,024 wavenumber points, 326-2035 cm-1) as features; SEL-15 judges such signals case by case. No model learns it (R2 < 0.05; scored as draws). Licence not stated (requested from authors). Consecutive frames of one elution (time series). HF mirror: ...
