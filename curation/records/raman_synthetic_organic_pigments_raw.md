---
unique_name: raman_synthetic_organic_pigments_raw
name: Synthetic Organic Pigments (Raw)
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
- https://doi.org/10.1002/jrs.4054
- https://soprano.kikirpa.be (KIK-IRPA SOP spectral library; raman-data downloads a SharePoint zip)
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`No Good Target / Scientific Discovery`, SEL-3 via SEL-8; USE-2): a reference library of one spectrum per pigment, published for spectral library search; the colour-family label is the loader's own construction from the file names, and no decision rests on it.
- Source: Fremout and Saverwyns (KIK-IRPA, Brussels), "Identification of synthetic organic pigments: the role of a comprehensive digital Raman spectral library", J. Raman Spectrosc. 43(11):1536-1544, online 2012-07-25 (https://doi.org/10.1002/jrs.4054); the spectra on KIK-IRPA's SOP Spectral Library (then modern.kikirpa.be, now https://soprano.kikirpa.be). As published: "a digital spectral library that comprehends almost 300 spectra of different SOPs", one reference spectrum per pigment. RamanBench's raw cut (HF mirror, parquet footer only): 325 rows x 561 bins (1189-1651 cm-1) + `target` with 8 classes (PB, PBK, PBR, PG, PO, PR, PV, PY).
- Original task (SEL-8): identifying an unknown pigment in a painting by matching its spectrum against the library: "To ensure a correct identification, however, an as complete as possible library of reference spectra is needed", earlier spectra are "hardly usable for spectral matching algorithms", and "Published flow charts have been evaluated in relation to digital search algorithms" (abstract). With one spectrum per pigment no class holds a second example, so the source's task is a library search, not a classification.
- The label: raman-data builds it (`MiscLoader._load_sop_spectral_library`, docstring): "each filename encodes a specific pigment (e.g. "PB12_A_785"), essentially unique per sample -- using that directly as the label would give ~300 singleton classes, useless for any train/test split. The leading letters (before the first digit) encode a coarser color-family grouping [...] that's the real, learnable classification target used here." The prefix is the Colour Index hue (Pigment Red, Pigment Yellow, ...), which the conservator sees on the painting before any spectrum is taken; the decisions the abstract names (conservation strategy, degradation, authenticity) need the specific pigment. No decision fits the hue (USE-2, USE-5). RamanBench lists the set as a regression with one target (Table 16, Table 31; best R2 0.255, Deep CNN), which matches neither the source nor the loader.
- RamanBench's own inclusion rule excludes "single-spectrum-per-compound reference libraries" (Sec. 3.1; Table 17 drops RamanBioLib and the adulterant and organic-compound libraries for about one spectrum per compound); this library stays in only through the relabelling.
- Siblings and duplicates: the baseline-corrected variant (raman-data `synthetic_organic_pigments_baseline_corrected`, left out of RamanBench as a "Baseline-corrected variant of Synthetic Organic Pigments (Raw)", Table 17) has no record; no other pigment record (grep for pigment, kikirpa, jrs.4054). External collections: RamanBench.
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Metric: the source evaluates library-search hits, no classification or regression metric; RamanBench scores macro-F1 or RMSE as benchmark-wide conventions.
- Also noted: raw spectral bins weigh against (SEL-15). Access: "not publicly hosted; interested users should contact KIK-IRPA" (RamanBench A.18.1, licence "research use only"), while raman-data downloads a SharePoint zip: a note only (EV-4). Read as a retrieval task, the original task would fall under SEL-9 (`Out-of-scope Task (CTR/RecSys/Ranking)`), the alternative marker.
- Reject check (AI, 2026-10-31): stands. The source is a reference library for search: 'a digital spectral library that comprehends almost 300 spectra of different SOPs', with earlier spectra 'hardly usable for spectral matching algorithms' (Fremout and Saverwyns 2012, abstract via https://api.crossref.org/works/10.1002/jrs.4054). The class label exists only in the loader: 'using that directly as the label would give ~300 singleton classes ... The leading letters ... encode a coarser color-family grouping' (https://github.com/ml-lab-htw/raman_data/blob/main/raman_data/loaders/MiscLoader.py, l. 2548-2553). The hue is the visible colour, and no decision rests on it. Not a reject on spectra as such (SEL-15).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 325 spectra x 561 wavenumber features; 1 classes (raman-data id: synthetic_organic_pigments_raw); target: pigment colour family (PR, PY, PO, PV, PB, PBR, PG, PBK) in the current loader; the paper lists it as regression with 1 target.
- Why: Identify synthetic organic pigments in artworks from their Raman spectrum
- Notes: Raw Raman spectral bins (561 wavenumber points, 1189-1651 cm-1) as features; SEL-15 judges such signals case by case. Reference library (~300 pigments, one spectrum each). Not publicly hosted per the paper (contact KIK-IRPA); licence 'research use only'. Task type inconsistent between paper (Regr.) and loader ...
