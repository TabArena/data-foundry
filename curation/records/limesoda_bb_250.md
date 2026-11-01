---
unique_name: limesoda_bb_250
name: 'LimeSoDa: Precision Liming Soil Datasets'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://zenodo.org/records/14936177
- http://arxiv.org/abs/2508.09888
- https://github.com/JonasSchmidinger/LimeSoDa
- https://github.com/a11to1n3/LimeSoDa
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the LimeSoDa collection, the same Zenodo deposit and packages as `limesoda_precision_liming_soil` (this record links version 1.0.1, https://zenodo.org/records/14936177, whose concept DOI 10.5281/zenodo.14932572 is the link of that record); the name points at BB.250, one of the 31 datasets, but the record's own notes describe the whole collection ("31 datasets of 30-460 samples"), so the data is recorded twice.
- Source: Schmidinger et al., "LimeSoDa: A dataset collection for benchmarking of machine learning regressors in digital soil mapping", Geoderma 459:117337 (2025, https://doi.org/10.1016/j.geoderma.2025.117337; preprint arXiv 2502.20139, read). Zenodo API for record 14936177: title "Precision Liming Soil Datasets (LimeSoDa) Zenodo Repository", version 1.0.1, conceptrecid 14932572, description "Precision Liming Soil Datasets (LimeSoDa) is a collection of 31 datasets from a field- and farm-scale soil mapping context". BB.250 (Table 1 of the paper): Brandenburg, 52 ha, 250 samples, 17 features (DEM, ERa, gamma, pH-ISE, RSS, VI), used before by Schmidinger et al. (2024b).
- If the curator wants BB.250 as a dataset of its own, it is one of the sets chosen under `limesoda_precision_liming_soil` when the collection is added (PROV-6: the cut adds no task that record lacks); the alternative is to keep this record as the BB.250 cut and narrow its name and notes to it. Its Zotero paper (item 30, arXiv 2508.09888, "Modern Neural Networks for Small Tabular Datasets: The New Default for Field-Scale Digital Soil Mapping?") is noted in `limesoda_precision_liming_soil`.
- Siblings: `limesoda_precision_liming_soil` (`TBD -> Yes`, priority 2, screened in this batch). Better data: from the curator's Zotero collection (item 30); no further search this round.
- Reject check (AI, 2026-10-31): stands. Zenodo API, record 14936177: conceptrecid 14932572 (the DOI limesoda_precision_liming_soil links), version 1.0.1, 'a collection of 31 datasets from a field- and farm-scale soil mapping context' (https://zenodo.org/records/14936177). This record's name and Assessment describe the whole collection, not BB.250. BB.250 is not lost: the surviving record names it among the mixed-sensor sets the curator picks from (PROV-6).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 30: "Modern Neural Networks for Small Tabular Datasets: The New Default for Field-Scale ...".
- as published: lab-analysed soil samples per field: 31 datasets of 30-460 samples. Features: proximal sensing (ERa, gamma-ray, pH-ISE), DEM, remote-sensing bands and indices, XRF, or vis-NIR/NIR/MIR spectra with ...; target: SOC or SOM, pH, clay content (three regression targets per dataset); access: open.
- Why: Real lab measurements with sensor features, published and maintained as an ML benchmark collection, open under CC BY-SA 4.0.
- Adds: Field-scale proximal soil sensing, against our continental surveys (lucas_topsoil, open_soil_data, africa_soil_property_prediction_challenge, open_soil_spectral_library), and a real tiny-data regime. Risks: 13 of the 31 sets are spectra (lean out, SEL-15); the rest are very small; Multi-target.
