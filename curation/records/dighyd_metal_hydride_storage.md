---
unique_name: dighyd_metal_hydride_storage
name: 'DigHyd: experimental hydrogen-storage properties of metal hydrides mined from the literature'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
original_source: Website
domain: chemistry & material science
problem_type: Regression
source_links:
- https://www.dighyd.org/
- https://doi.org/10.1007/s00339-026-09903-6
- https://doi.org/10.1039/d5sc07296d
- https://doi.org/10.1039/d5sc09921h
- https://arxiv.org/abs/2603.14139
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: gravimetric hydrogen capacity (4,643 metal-hydride values) and hydrogenation thermodynamics (652 ΔH/ΔS pairs) mined from the experimental literature with LLM tools and curated by hand, a real materials property from the composition; but no bulk download, data statement or licence was found, so the data may have to be requested.
- Source: the Digital Hydrogen Platform (DigHyd, www.dighyd.org, a Streamlit app; Jang, Zhang, Jia, Tran, ..., Orimo, Li). First described in Zhang et al., "DIVE into hydrogen storage materials discovery with AI agents", arXiv 2508.13251 (2025), Chem Sci 2026 (doi 10.1039/d5sc09921h); the data paper Jang et al., "Digital hydrogen platform (DigHyd): a rigorously curated database ...", Applied Physics A, 2026-09-04 (doi 10.1007/s00339-026-09903-6; arXiv 2603.14139, 2026-03-14); the modelling paper Jang et al., Chem Sci 2025 (doi 10.1039/d5sc07296d; arXiv 2509.04039: "a rigorously curated dataset of 5089 metal hydride compositions"). As published: ">30,000 data entries" from ">4,000 experimental literature sources"; "for metal hydride cases only, 4,643 data points of w and 652 data pairs of ΔH and ΔS were obtained through subsequent manual curation" (arXiv 2603.14139, Sec. 2); the room-temperature equilibrium pressure Peq,RT is computed from ΔH and ΔS by the van't Hoff relation (Sec. 3). Inputs: the composition and material class; features to compute from the formula.
- Use case: a hydrogen-storage researcher screens candidate alloy compositions before synthesis and PCT measurement (the papers' inverse design); fit approximate (no actor's decision named; compositions are those published). Regime: likely grouped by alloy system or host (the literature varies one prototype by small substitutions, Fig. 2d of the data paper), to decide at add time.
- Siblings and duplicates: no other record holds hydride data (grep for hydride, hydrogen storage, DigHyd). Composition-to-property siblings: `superconductivity` (Yes), `experimental_band_gap_zhuo` (this batch). External collections: none found; the awesome-chemistry-datasets list names it.
- Better data: from the curator's Zotero collection (item 159) and the awesome-chemistry-datasets list; no search for better data in this run.
- Papers and pages: the three papers above; the data paper's Fig. 3 (symbolic regression and XGBoost, an 80:20 split, R², RMSE and MAE for w and Peq,RT).
- Metric: none deliberate: the data paper shows R², RMSE and MAE side by side on one 80:20 split (Fig. 3); fallback `rmse` (MET-1, MET-5); inputs none.
- Risks for /add-dataset: access: the arXiv data paper's Data Availability section is empty and the app showed no bulk download or licence (the run's note that the GitHub repository holds only an Excel predictor was not re-checked); ask the authors (`Data Requested` once asked); LLM-assisted extraction with manual curation; one composition reported by several papers (group or deduplicate); Peq,RT is a function of ΔH and ΔS, so one target at a time and never the others as inputs (LEAK-10); the conditions behind w (temperature, pressure, cycling) may differ by paper.
- Priority: gap 0 (chemistry & material science and regression are not thin), use case 0 (no decision named), source + (a data paper and two method papers), shape + (4,643 w values), risk - (no open download found).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 159: "Retrieval-aligned Tabular Foundation Models Enable Robust Clinical Risk Prediction in ...".
- as published: 30,000+ entries from 4,000+ publications (DIVE paper); the curated metal-hydride subset has 5,089 compositions from 910 sources with gravimetric hydrogen density w and room-temperature equilibrium ...; target: gravimetric hydrogen storage capacity w (wt%) or equilibrium pressure at room temperature; access: request.
- Why: measured values from pressure-composition isotherms, manually reviewed after LLM extraction; larger than the older hydride compilations
- Adds: a materials property with a measured target, a domain the benchmark lacks. Risks: access unclear (Streamlit app only, no bulk download or licence found; the GitHub repo holds only an Excel predictor), so access would need the authors; LLM-assisted extraction; composition-only features
