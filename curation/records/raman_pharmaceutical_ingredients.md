---
unique_name: raman_pharmaceutical_ingredients
name: Pharmaceutical Ingredients
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Many features
- Many class
collections:
- RamanBench
original_source: Other
year: '2025'
domain: chemistry & material science
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1038/s41597-025-04848-6
- https://springernature.figshare.com/ndownloader/articles/27931131/versions/1
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: a well documented open reference library of 32 pure solvents and reagents, but each class is one commercial product scanned about 110 times, so the task likely reduces to recognising 32 bottles of pure compounds (TP-4 to probe).
- Source: Flanagan and Glavin, "Open-source Raman spectra of chemical compounds for active pharmaceutical ingredient development", Scientific Data 12, 2025-03-24 (https://doi.org/10.1038/s41597-025-04848-6; full text PMC11933687); data on Springer Nature figshare (article 27931131, 2025-03-25, CC BY): `raman_spectra_api_compounds.csv` (193 MB), `API_Product_Information.xlsx`, `code.zip`. As published: "Containing 3,510 samples spanning 32 compounds" (abstract); "an N × M matrix ... M corresponds to the 3276 wavelengths. Each row in the matrix corresponds to a single sample, with the respective target label located in the last column" (Data Records); one Endress+Hauser (Kaiser) Raman Rxn2 at 785 nm; "Thirty-two commercial solvents and reagents were collected"; "Each spectrum in the dataset corresponds to a single manual scan ... The Rxn-10 probe was moved laterally and by twisting it around its cylindrical axis to simulate various optical path lengths and positions" (Methods).
- Use case: a lab chemist identifies an intermediate or unknown chemical against a small in-house library ("small spectral libraries are typically compiled for one-shot identification of intermediates or unknown chemicals", abstract); the source publishes reference data "for referencing" and calibration, and names no prediction task. Fit approximate: a test scan always comes from the bottle the training scans came from. Regime: IID over scans by necessity, since no group other than the class exists.
- Siblings and duplicates: none (grep over the records for the DOI, the figshare id, Flanagan). External collections: RamanBench, which lists it as trivial ("perfect:LR", configs/v1/quality_exclusions.json) and skips it in its sweep; its scores are no evidence for our task (EV-4).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the Sci Data paper (full text via Europe PMC); RamanBench Tables 3, 11, 16 and its quality exclusions.
- Metric: none from the source (a data descriptor; its technical validation checks the instrument's stability, no classifier): fallback `log_loss` (MET-1, MET-5); RamanBench scores macro-F1.
- Risks for /add-dataset: Trivial (TP-4) to probe on our split: pure compounds with distinct fingerprints, one product per compound makes the task recognising a bottle (USE-8, `Not Representative` to weigh); the authors advise baseline correction and cropping above 3150 cm-1 (a cleaning choice, CLEAN); raw spectral bins weigh against (SEL-15).
- Priority: gap + (multiclass thin), use case 0 (no prediction task named), source + (Sci Data descriptor, figshare), shape 0 (3,510 scans of 32 products), risk - (one product per class, likely trivial).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 3,510 spectra x 3,276 wavenumber features; 32 classes (raman-data id: pharmaceutical_ingredients); target: compound (32 classes).
- Why: Identify the chemical compound (solvents and reagents for API development) from its Raman spectrum
- Notes: Raw Raman spectral bins (3,276 wavenumber points, 150-3425 cm-1) as features; SEL-15 judges such signals case by case. Repeated spectra of 32 pure substances. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/pharmaceutical_ingredients
