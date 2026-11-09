---
unique_name: wegeners_granulomatosis_remission_proteomics
name: Wegener's granulomatosis active disease vs remission, serum MALDI-TOF spectra (NCI-FDA CPP)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
tags:
- AI-Filled (Verify)
- Spectral Data
original_source: GOV Website
year: '? (2005)'
domain: medical & healthcare
problem_type: Binary Classification
source_links:
- https://home.ccr.cancer.gov/ncifdaproteomics/WegenersRawData.zip
- https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp
- https://doi.org/10.1002/art.20938
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: 154 serum MALDI-TOF spectra of Wegener's granulomatosis patients from the WG Etanercept Trial, active disease against extended remission, randomised against batch with a blinded test set; a real clinical question, but small, raw high-resolution spectra that need our own processing, possibly several samples per patient without ids, from the data bank whose prostate set we retired.
- Source: Stone, Rajapakse, Hoffman, Specks, Merkel, Spiera, Davis, St.Clair, McCune, Ross, Hitt, Veenstra et al., "A serum proteomic approach to gauging the state of remission in Wegener's granulomatosis", Arthritis & Rheumatism 52(3) (2005-03, https://doi.org/10.1002/art.20938; abstract through Crossref); data on the NCI-FDA Clinical Proteomics Program page (https://home.ccr.cancer.gov/ncifdaproteomics/ppatterns.asp: the study aimed "to discriminate patients with active Wegeners granulomatosis from those in remisssion" on "randomly commingled" sera; a 467 MB zip of raw data, https://home.ccr.cancer.gov/ncifdaproteomics/WegenersRawData.zip, not downloaded). As published (abstract): sera "collected in the WG Etanercept Trial", "randomized into sets for training and testing, such that remission sera and active disease sera could be analyzed without batch bias"; 82 training samples (42 remission, 40 active) and 72 blinded test samples (37 remission, 35 active); high-resolution MALDI-TOF; the page advises normalisation, baseline correction and alignment before any analysis.
- Use case: a rheumatologist, at a visit, judges whether a patient is in remission or flaring to decide on immunosuppressive treatment ("help clinicians apply immunosuppressive therapies more judiciously", abstract); fit approximate (a research assay on selected states: extended remission or a recent flare, not the grey zone a clinic meets); regime grouped by patient if patients gave several samples (ids not known), else IID; the source's training and test sets as a claim (SPLIT-5).
- Siblings and duplicates: the same data bank: `pancreatic_cancer_mouse_detection` (`Yes`, BeyondArena; binned murine spectra, kept with an open question on artefacts), `prostate_cancer_detection` (`No (Retired)`, `Data Quality Issue`: processing artefacts), `ovarian_cancer_prediction` (`No`, `Trivial`); another disease and design, no duplicate (PROV-7). External collections: none found.
- Better data: from the curator's Zotero collection (item 165, the program's data page); no further search this round.
- Papers and pages: Stone et al. 2005 (a model of 7 ions from a pattern-recognition tool; on the blinded set 35 of 37 remission and 32 of 35 active samples correct); the program's page.
- Metric: the paper reports sensitivity and specificity of its clusters on the blinded set, with no threshold or cost fixed for a probability model (MET-6), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: raw spectra need binning, baseline correction and alignment of our own (a processing choice; raw spectral bins lean out under the SEL-15 weighed factors; the pancreatic set's binning is the precedent); patient ids for a grouped split (ask the authors or the trial); batch and run-order artefacts as found in the program's other sets (PROV-13, the prostate precedent); 154 samples (about 15 per class per test fold, TP-5 holds but the signal will be noisy).
- Priority: gap 0 (medical and binary are covered), use case 0 (the paper names the clinician's decision, but the fit is approximate), source + (journal paper and the program's page), shape 0 (154 samples), risk - (our own spectral processing, possibly repeated patients, the data bank's artefact history).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 165: "Clinical Proteomics Program Databank - Proteomic Patterns".
- as published: 154 serum samples: 82 training (42 remission, 40 active) and 72 blinded test (37 remission, 35 active); raw high-resolution MALDI-TOF spectra, 478 MB zip; target: active disease vs remission (binary); access: open.
- Why: Samples were randomized against batch, with a blinded test set: the design the retired prostate set lacked. The same portal's binned PanIN set was accepted.
- Adds: A disease-activity task. It is small, the raw spectra need binning (SEL-15 counts raw bins against it), and patients may contribute several samples with no IDs known. Low priority.
