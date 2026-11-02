---
unique_name: raman_comfile_stroke
name: Alzheimer's SERS Serum
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Too Small
tags:
- AI-Filled (Verify)
collections:
- RamanBench
source_links:
- https://doi.org/10.1038/s42256-025-01027-5
- https://figshare.com/articles/dataset/ComFilE_for_AD/28107578
- https://arxiv.org/abs/2605.02003
- https://figshare.com/articles/dataset/ComFilE_/28107431
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Too Small`, TP-5): both ComFilE serum releases hold a handful of patients per class (stroke 10 and controls 10; AD, MCI and controls 7, 5 and 5 serum samples), each sample measured about 200 times; scored per patient under a grouped split, a test fold holds 1-2 patients of a class.
- Source: Xue et al., "Deep spectral component filtering as a foundation model for spectral analysis demonstrated in metabolic profiling", Nature Machine Intelligence, 2025-05-23 (paywalled, not read); data on figshare by Bingsen Xue, both 2024-12-30, CC BY 4.0: "ComFilE 用于笔划" (figshare 28107431), "The serum SERS spectra of stroke patients and control", files "[1]T01_negative nobase.txt" to "[1]T10..." and "[2]H01..." to "[2]H10..."; "ComFilE for AD" (figshare 28107578), "Serum SERS spectra of Alzheimer's disease, Mild Cognitive Impairment and control", 17 files ("[1] 003 nobase.pt" and so on: 7 in [1], 5 in [2], 5 in [3]). Each file is one serum sample's SERSome of about 201 spectra (RamanBench: 4,020 and 3,417 spectra x 724 bins; the mirror's group ids, read: 10/10 and 7/5/5).
- Why the patient is the unit: the label is the patient's diagnosis, and the ~200 spectra of a file are repeated measurements of one serum sample; a random split over spectra rewards recognising the sample (SPLIT-29), and the use case is a diagnosis per patient (SPLIT-23).
- Precedent: `parkinsons_biomedical_voice_measurements`, retired as `Too Small` with 8 healthy people, 2-3 per test fold (2026-10-05, Lennart).
- Also: the AD release does not say which of [1], [2], [3] is AD, MCI or control (the loader's mapping is its guess; USE-5); the "139 serum samples" in the raman-data description are the paper's cohort, not the release. The record's name ("Alzheimer's SERS Serum") and its unique name (stroke) come from two RamanBench entries merged into one record.
- Siblings and duplicates: `raman_serum_prostate_cancer` (ComFilE for PCa, 12,601 spectra; same group and pipeline, another disease, PROV-7; screened in another batch). External collections: RamanBench ("Alzheimer's SERS Serum", "Stroke SERS Serum").
- Better data: a candidate of the benchmark RamanBench (arXiv 2605.02003); no further search in this run.
- Reject check (AI, 2026-10-31): stands. The figshare API lists 20 files, '[1]T01' to '[1]T10' and '[2]H01' to '[2]H10' ('The serum SERS spectra of stroke patients and control', https://figshare.com/articles/dataset/ComFilE_/28107431), and 17 for AD, 7/5/5 (https://figshare.com/articles/dataset/ComFilE_for_AD/28107578), one serum sample of about 201 spectra each. Grouped by sample, a test fold holds 1-2 patients per class, below parkinsons_biomedical_voice_measurements (8 healthy, retired) and the same call as raman_wheat_lines (batch 02). The paper's larger cohort is not in the release.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 3,417 spectra x 724 wavenumber features; 3 classes (raman-data id: serum_alzheimer_disease); target: diagnosis (AD / MCI / control).
- Why: Classify Alzheimer's disease, mild cognitive impairment or healthy control from serum SERS spectra | Classify stroke vs healthy control from serum SERS spectra
- Notes: Raw Raman spectral bins (724 wavenumber points, 0-723 cm-1) as features; SEL-15 judges such signals case by case. 139 serum samples, ~200 spectra per sample (SERSome): grouped by patient. Paper text says binary, table and loader say 3 classes. HF mirror: ...
