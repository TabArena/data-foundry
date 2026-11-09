---
unique_name: raman_wheat_lines
name: Mutant Wheat
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
- Spectral Data
collections:
- RamanBench
source_links:
- https://doi.org/10.3389/fpls.2023.1116876
- https://doi.org/10.5281/zenodo.7644521
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Too Small`, TP-5; SPLIT-29): 53,134 spectra, but they are maps of three leaves per class, twelve leaves in all, and no leaf id ships; scored on new leaves, each class has three units.
- Source: Sen, Kecoglu, Ahmed, Parlatan and Unlu, "Differentiation of advanced generation mutant wheat lines: conventional techniques versus Raman spectroscopy", Frontiers in Plant Science 14:1116876, 2023 (https://doi.org/10.3389/fpls.2023.1116876); data and MATLAB code on Zenodo (https://doi.org/10.5281/zenodo.7644521, 2023-02-15, CC BY 4.0; `Data.mat`, 694 MB, one array per class). RamanBench's cut (HF mirror, parquet footer only): 53,134 rows x 1,748 bins (296-2043 cm-1) + `target` with 4 classes `COM`, `COM_125mM`, `ML1_125mM`, `ML2_125mM` (cultivar Adana-99 without and with 125 mM NaCl, two seventh-generation NaN3 mutant lines with salt); no leaf, plant or scan column.
- The units: "The three different leaves for the commercial cultivar were scanned, i.e., commercial cultivar with 125 mM salt and two mutant lines with 125 mM salt. In each scan, 4,221 spectra were measured; thus, a total of 12,663 spectra were taken for each class." (Sec. 3.4). Each class is three leaf scans of 4,221 spectra. The paper split the spectra at random ("we first randomly split the data into 20%-80% test-train parts", Sec. 2.3), so spectra of one leaf sit on both sides.
- Use case: a breeder screens new mutant lines against the parent cultivar with a leaf scan instead of biochemical assays ("RS has potential in plant breeding programs by eliminating the disadvantages of conventional methods in the discrimination of the breeding material or the new genotype from the source from which it was obtained", Conclusion). The prediction is for a new plant's leaf, so the split groups by leaf: thousands of rows share a leaf that new data would not have, and the leaf carries the label (SPLIT-29). Under that split each class has three units in total, one per test fold of a 3-fold split, fewer than the 8 healthy voices of `parkinsons_biomedical_voice_measurements` (retired under TP-5, 2026-10-05). As shipped the leaf cannot be grouped on either (SPLIT-24, SPLIT-25), unless the row order of `Data.mat` keeps the scans in blocks of 4,221.
- Also: the four classes mix genotype with treatment, while the paper's task is binary, cultivar against mutant lines "regardless of their salt concentration" (Sec. 3.4); the 53,134 rows do not match the paper's 4 x 12,663 = 50,652.
- Siblings and duplicates: none among the records (grep for wheat, 7644521, fpls.2023.1116876). External collections: RamanBench (macro-F1 0.921, TabPFN v2.5, Table 11).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Metric: the paper reports accuracy (94.62%), sensitivity and specificity for its binary tree, side by side with no threshold fixed, so a four-class definition would take the fallback `log_loss` (MET-5, MET-6); RamanBench scores macro-F1.
- Also noted: raw spectral bins weigh against (SEL-15).
- Reject check (AI, 2026-10-31): stands. Sen et al. 2023, Sec. 3.4: 'In each scan, 4,221 spectra were measured; thus, a total of 12,663 spectra were taken for each class' (https://doi.org/10.3389/fpls.2023.1116876), so 3 leaf scans per class. The class is constant within a leaf, so a split must group by leaf (SPLIT-29), which leaves at most 3 units per class and 1 per test fold, below `parkinsons` (8 people, retired under TP-5). The leaf id is not shipped (SPLIT-25). The 53,134 rows against the paper's 4 x 12,663 do not change the order of magnitude. Not a reject on spectra as such (SEL-15).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 53,134 spectra x 1,748 wavenumber features; 4 classes (raman-data id: wheat_lines); target: wheat line.
- Why: Distinguish salt-tolerant mutant bread-wheat lines from the parent cultivar by leaf Raman spectra (breeding screen)
- Notes: Raw Raman spectral bins (1,748 wavenumber points, 296-2043 cm-1) as features; SEL-15 judges such signals case by case. Many spectra per leaf/plant (grouped). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/wheat_lines
