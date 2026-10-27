---
unique_name: lhc_olympics_2020
name: LHC Olympics 2020 (anomaly detection challenge)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
original_source: Website
year: '2020'
domain: physics & astronomy
problem_type: Other
original_data_state: Other
source_links:
- https://lhco2020.github.io/homepage/
- https://doi.org/10.5281/zenodo.3547721
- https://doi.org/10.5281/zenodo.2629072
- https://arxiv.org/abs/2101.08320
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-16; `Wrong Domain / Source Modality`, SEL-12): simulated collider physics with its own benchmark community, like `higgs`.
- Source: LHC Olympics 2020 (Kasieczka, Nachman, Shih et al., arXiv 2101.08320; https://lhco2020.github.io/homepage/), R&D set on Zenodo (https://doi.org/10.5281/zenodo.2629072): "The events are produced using Pythia8 and Delphes 3.4.1, with no pileup or MPI included"; "1M QCD dijet events and 100k W'->XY events"; each event a list of hadrons "(pT, η, φ, ...) zero-padded up to 700 hadrons", an array of 1.1M x 2101 with a "signal/background truth bit" that "won't be included in the actual challenge". Black boxes: "These samples may contain some new signal(s)".
- Use case: a model-agnostic search for new physics (anomaly detection on unlabelled black boxes); the labelled R&D set is a simulation-vs-simulation classification, the setup `higgs` was rejected for.
- Siblings and duplicates: `higgs` (Lennart, 2026-09-22: `No`, simulated physics with dedicated benchmarks; its note names the LHC Olympics as one of the field's own benchmarks), `susy`, `hepmass`, cern_* records. External collections: HEP-ML living review, Datasets.
- Metric: none for a tabular task (the challenge scored whether teams found the signal).
- Reject check (AI, 2026-10-22): stands. Zenodo R&D set: "produced using Pythia8 and Delphes 3.4.1" (https://doi.org/10.5281/zenodo.2629072). Each event is a zero-padded list of up to 700 hadrons, and the native task is anomaly detection on unlabelled black boxes (https://lhco2020.github.io/homepage/). That is SEL-16 (simulated; the curator's higgs note names the LHC Olympics as one of the field's own benchmarks), with SEL-12 (particle lists) and SEL-3 on top. No real use case survives any of them.

Community challenge for model-agnostic anomaly detection at the LHC (Kasieczka et al., arXiv 2101.08320). Each simulated event is "a list of all hadrons (pT, eta, phi, ...) zero-padded up to 700 hadrons"; a labelled R&D dataset plus unlabelled "black boxes" that "may contain some new signal(s)". Hosted on Zenodo.

Out of scope on three counts: the task is unsupervised / weakly supervised anomaly detection, not a fixed classification or regression target; the input is a variable-length particle list, not a table; and the data are simulated (criterion 4B). Listed in the HEP-ML living review Datasets section. Data not inspected.
