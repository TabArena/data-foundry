---
unique_name: raman_mlrod
name: ML Raman Open Dataset (MLROD)
checked_by:
- Lennart
data_foundry_status:
- WIP (DF)
claimed_by: Lennart
suggestion: 'Yes'
priority: 3
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
- Many features
- Many class
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2022'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://doi.org/10.1029/2021EA002125
- https://odr.io/MLROD
- https://arxiv.org/abs/2605.02003
v2_path: datasets/_dev/tabarena-v0pt2/raman_mlrod/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: a large, documented set of measured Raman spectra of Mars-analogue minerals, mixtures and rocks, clean and under basalt dust, for a named identification task; open are how many physical specimens stand behind each class and the spectra question (SEL-12, SEL-15).
- Source: Berlanga, Williams and Temiquel, "Convolutional Neural Networks as a Tool for Raman Spectral Mineral Classification Under Low Signal, Dusty Mars Conditions", Earth and Space Science 9(10), 2022 (https://doi.org/10.1029/2021EA002125); data on ODR as the ML Raman Open Dataset (https://odr.io/MLROD; "License: BY-NC" per raman-data, a note only, EV-4). As published, the abstract: "the Machine Learning Raman Open Data set data set with 500,000+ Raman spectra of hand samples/powder mixtures (5,000+ spectra/mineral class)"; point maps on a Horiba LabRAM HR Evolution at 532 nm with "No cosmic ray removal, baseline correction, or other preprocessing applied" (raman-data card). The raman-data loader (`MiscLoader._load_mlrod`) reads 41 CSV files, one per map: 34 `*_train_*` files of 12 minerals (quartz, albite, hornblende, biotite, muscovite, forsterite, augite, enstatite, anorthite, microcline, calcite, gypsum) and 3 binary mixtures, and 7 `L_raw_*_test_*` files of gabbro and granite slabs at 0% and 50% dust; its label map has 16 classes, the 16th "Granite slab - 50% dust". RamanBench's cut: 130,061 spectra x 1,836 bins (141-1100 cm-1), 16 classes.
- Use case: a planetary scientist, or the rover itself, identifies the minerals of a dusty target from a Raman spectrum: the CNN "can facilitate scientist Raman spectral interpretation on Earth and autonomous rover decision-making on planets like Mars" (abstract). Fit direct for lab Raman identification, approximate for Mars (lab analogues). Regime grouped by specimen and map: spectra 0.1 µm apart in one map are near copies, and the source keeps whole rock slabs as test files, so a random split over spectra leaks (SPLIT-29).
- Siblings and duplicates: `raman_rruff_mineral_raw` (RRUFF reference minerals, another source, no overlap); no duplicate (grep over the records for MLROD, odr.io, Berlanga, the DOI). External collections: RamanBench (its scores, macro-F1 0.990 TabICL v2 and 0.988 TabPFN v2.5 on its own splits, are no evidence for our task, EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: Berlanga et al. 2022 (abstract read; the full text and odr.io returned 403); RamanBench (arXiv 2605.02003), Tables 3, 11, 16 and App. A.4; raman-data `MiscLoader`.
- Metric: the abstract reports "+99% success" for the CNN, an accuracy with no threshold or cost fixed, and the full text was not reachable, so no deliberate metric was found: fallback `log_loss` (MET-1, MET-5, MET-6); RamanBench scores macro-F1 as a benchmark-wide convention. Inputs: a specimen or map id for the grouped split, which ships only as the file name.
- Risks for /add-dataset: how many hand samples stand behind each class (with one specimen per class a grouped split cannot hold a class out, and the task turns into recognising a specimen; the source's train/test design by file is the fallback, SPLIT-5); the label set mixes minerals, 50/50 mixtures and one rock-slab class, and the labels of the gabbro and granite test maps (per point or per slab) are unread; 5,000+ spectra per class, so subsample by map, not at random; raw spectral bins weigh against (SEL-15, weighed factor); whether tabular models are competitive (SEL-12) is for our own probes.
- Priority: gap + (multiclass thin), use case + (the source names the scientist and the rover's decision), source + (paper and ODR deposit), shape 0 (130,061 spectra but few physical specimens, count unknown), risk - (specimen grouping unclear, one rock-slab class).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 130,061 spectra x 1,836 wavenumber features; 16 classes (raman-data id: mlrod); target: mineral / sample class.
- Why: Identify the mineral (or rock/mixture) from a point Raman spectrum of Mars-analogue samples, clean or under basalt dust
- Notes: Raw Raman spectral bins (1,836 wavenumber points, 141-1100 cm-1) as features; SEL-15 judges such signals case by case. Licence CC BY-NC. Spectra from point maps of few physical samples (likely grouped by sample). HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/mlrod

CC (2026-11-08, Lennart): accepted for adding (`Yes`) in the screening review of the large candidates (most rows, most features).

**Assessment (AI, 2026-11-09):** review panel (full): ship after changes (made: the source's split, the reference maps train and both slabs are tested in one fold, scored by rock after the fact, SPLIT-19; the 46-spectrum gypsum and forsterite-albite powder map named after the gabbro moved to training, SPLIT-24/LEAK-17; one reading per band in place of the band minimum, LEAK-13, comb ROC AUC 0.651 to 0.536; the spreadsheet fill-down of qtzalb_train_60s_3000 row 2456 masked, PROV-13/CLEAN-26; a LEAK-9 protocol line and a kept-on-purpose note with the task gamer's gains; fit_reason, metric reason, licence note and counts corrected); of the three gates the panel set, the paper (PDF supplied by Lennart, 2026-11-09) settles two: the slabs were labelled by hand, the CNN only pointing at labels to recheck (Sec. 4.2: "Over 30,000 spectra were manually labeled by the authors over the span of 500 hr and three full passes"; USE-5 holds, both rocks kept), and the reference maps are separate hand samples (Table 1: augite from Trento Province, Italy, muscovite from Ottawa, the gabbro slab from Madagascar; SPLIT-24 and LEAK-17 hold, the maps stay); the record stays `TBD` on the third, the mirror against ODR (PROV-1, PROV-13: three files, L_raw_gabbro50dust_test_015s_9740, L_raw_granite0dust_test_015s_4084_final and qtzalb_train_60s_3000, downloaded by Lennart on 2026-11-09 match the mirror byte for byte, size and sha256, a byte match as for ai4d, so the fill-down is ODR's own and stays masked; still open: L_raw_granite50dust_test_015s_10000, ODR's file list with id 63742, and the licence badge; the paper's Table 1 lists about 130,000 spectra, as the 41 files hold); TODO run (SEL-12): the source's Spec-CNN against tuned LightGBM, CatBoost, RealMLP, logistic regression and TabPFN v3.5 on the shipped split, on GPU via SkyPilot, reported for the clean and dusty slabs, the gabbro and the granite apart (untuned logistic regression 0.934 accuracy on the clean slabs against the CNN's 1.00); disputed: SPLIT-19 (one fold per rock or the source's split, settled for the source's), SPLIT-24 (the hb_ms muscovite block, settled: kept, gated with the augite map), LEAK-13 (settled: one reading per band), SEL-12 (for the curator after the run); for the curator: issue 1 (the last ODR checks), issues 2-3 (answered by the paper, to confirm), issue 4 (SEL-12 after the run), issue 5 (design A, only on request). Priority 3: gap +, use case 0, source +, shape +, risk - (gap: multiclass classification is thin among the accepted definitions; use case: the abstract names the scientist's interpretation and the rover's decision, but the fit is approximate, a lab microscope for a rover instrument, with slab labels that name the grain in the gabbro and the spot in the granite; risk: one source check open (three of four files match ODR) and a spectrum CNN far ahead of untuned tabular models, whose accuracy on the hand labels the CNN helped check is partly self-confirming, and a spectrum CNN far ahead of untuned tabular models).
