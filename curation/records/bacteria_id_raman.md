---
unique_name: bacteria_id_raman
name: Pathogenic Bacteria
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 4
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Many class
- Many features
- Non-IID (Grouped)
collections:
- RamanBench
original_source: Github
year: '2019'
domain: medical & healthcare
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: Other
source_links:
- https://doi.org/10.1038/s41467-019-12898-9
- https://github.com/csho33/bacteria-ID
- https://arxiv.org/abs/2605.02003
- https://pypi.org/project/raman-data/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source pages, the release file listings and a two-column preview of the data, NOT from a build. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: the largest documented Raman classification set (78,500 spectra, 30 isolates) with a clinical decision the source names, held back by the spectral-bin question (SEL-12, SEL-15) and culture batches that do not ship as a column.
- Source: Ho et al. (Stanford), "Rapid identification of pathogenic bacteria using Raman spectroscopy and deep learning", Nature Communications 10:4927, 2019-10-30 (PMC6960993; preprint arXiv 1901.07666); data and code at github.com/csho33/bacteria-ID (created 2019-06-12, MIT), the arrays on a Dropbox link in the README. As published: .npy arrays X/y, 1,000 bins (382-1792 cm-1) per spectrum, in separate files: reference training "2000 spectra each for the 30 reference isolates", reference fine-tuning and test sets of "100 spectra for each of the 30 reference isolates", a 2018 clinical set ("30 patient isolates distributed across 5 species, with 400 spectra per isolate"; the Results say 25 patients) and a 2019 clinical set ("25 patient isolates ... with 100 spectra per isolate") (Methods, "Dataset"). Target: the isolate (30 classes); the paper also maps isolates to empiric-treatment groups and species.
- Use case: "the priority for physicians is choosing the correct antibiotic to treat a patient" (Results, "Identification of empiric treatments and antibiotic resistance"): a microbiology lab measures a culture-free sample and the physician picks the empiric antibiotic within hours instead of days. Fit approximate: the 30-class task recognises 30 known reference strains measured on cultured monolayers, while a patient brings a new strain (the clinical sets test that, 5 species). Regime grouped: each class is one isolate, so no split by isolate exists; the source tests on "an independent test dataset gathered from separately cultured samples" ("Bacterial isolates were cultured on blood agar plates each day before measurement", Methods), and the clinical sets use leave-one-patient-out. A random split over spectra of one culture rewards recognising the culture (SPLIT-29).
- Siblings and duplicates: no other record of these data (grep by DOI, repository, name); the nearest task is `micro_mass` (`Yes`, MALDI-TOF spectra of bacterial strains, grouped by strain), another modality and source. External collections: RamanBench ("Pathogenic Bacteria", 78,500 spectra pooled over the files). The run's Assessment below cites RamanBench's scores (RamanNet ahead of the TFMs): another benchmark's scores are no evidence (EV-4).
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003) and of the curator's Zotero collection (item 188); no further search in this run.
- Papers and pages: the paper and its PMC copy; the GitHub README and notebooks; reused by many Raman model papers (not read).
- Metric: accuracy, the one metric the paper reports for identification: "average isolate-level accuracies exceeding 82%" and "antibiotic treatment identification accuracies of 97.0±0.3%" (Abstract); CNN 82.2% against "logistic regression and support vector machine (SVM) achieve accuracies of 75.7% and 74.9%" (Results). An argmax identification with no threshold to fix: keeping it as a deliberate choice is arguable (MET-5, MET-6; the covertype precedent), otherwise the fallback log_loss. Inputs none.
- Risks for /add-dataset: raw spectral bins (SEL-15 weighs them out; the source's CNN leads its LR and SVM baselines by about 7 points, a modality signal under SEL-12 to judge on our splits); the culture batch is no column, so the honest grouped split rests on the source's file division (reference training vs separately cultured test) or on the clinical sets, which hold about 10 patients per species over both years (TP-5); choose the target (30 isolates, treatment groups or species; USE-5); the arrays sit on a Dropbox link (pin a copy).
- Priority: gap + (multiclass thin), use case + (physicians choosing the antibiotic, named by the source), source + (Nat Commun paper, authors' GitHub), shape + (78,500 spectra, 30 classes), risk - (spectral modality, culture batches not shipped).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003); the curator's Zotero collection, item 188: "RamanBench: A Large-Scale Benchmark for Machine Learning on Raman Spectroscopy".
- as published: 78,500 spectra x 1,000 wavenumber features; 30 classes (raman-data id: bacteria_identification); target: isolate (30 classes); access: open.
- Why: Identify the bacterial/yeast isolate from low-SNR Raman spectra for culture-free pathogen identification | large, cleanly published real measurement set with a clinical target and a held-out clinical-isolate set (a natural grouped test)
- Adds: | a spectroscopy classification task beyond micro_mass (MALDI-TOF); risks: raw spectral bins (SEL-15 weighs them out), and in RamanBench the Raman-specific RamanNet beats the TFMs on it (F1 0.947 vs about 0.89), a SEL-12 sign; many spectra per isolate
- Notes: Raw Raman spectral bins (1,000 wavenumber points, 382-1792 cm-1) as features; SEL-15 judges such signals case by case. Licence MIT. 2,000 spectra per isolate plus clinical test sets; spectra of one isolate share a culture (grouped). HF mirror: ...
