---
unique_name: raman_hair_dyes_sers
name: Hair Dyes SERS
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- TBD
tags:
- AI-Filled (Verify)
- Many features
- Non-IID (Grouped)
- Spectral Data
collections:
- RamanBench
original_source: Other
year: '2026'
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1016/j.talanta.2022.123762
- https://doi.org/10.5281/zenodo.18881751
- https://arxiv.org/abs/2605.02003
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 1,713 SERS spectra of hair dyed with 33 commercial dyes, labelled by brand, type and colour, for forensic hair analysis; the honest split groups by dye, which leaves about 33 units, and the source reports nearly perfect brand accuracy.
- Source: Higgins and Kurouski, "Surface-enhanced Raman spectroscopy enables highly accurate identification of different brands, types and colors of hair dyes", Talanta 251:123762, 2023 (online 2022, PMID 35931011; https://doi.org/10.1016/j.talanta.2022.123762); the data "Dataset for: ..." on Zenodo, 2026-03-05, CC BY 4.0 (https://doi.org/10.5281/zenodo.18881751: "the raw Raman spectra including labels for brand, permanence (type), and color"), so the source is the Zenodo release, 2026 (PROV-9). As published: one CSV, `All_Spectra_Raw.csv` (12.7 MB): `Label`, `Brand`, `Type`, `Color`, then 1,340 bins from 308.5 cm-1; `Label` holds the dye, the acquisition settings, a date and a spectrum number ("Clairol_Perm_Auburn_35s_1.8mW 2022 April 07  1"; header and first rows read by a range request). RamanBench: 1,713 rows, brands Clairol 301, Ion 754, L'Oréal 150, Wella 508.
- Use case: a forensic examiner identifies the colorant on a hair found at a crime scene to link a suspect or rule one out (abstract: "Hair is present at nearly all crime scenes"); fit approximate: lab-dyed hair, one dyed sample per product, and brand is the coarse label RamanBench chose, while the paper's main target is the individual colorant (33 classes). Regime grouped by dye: all spectra of one product come from one dyed hair sample, so a random split tests the sample it trained on.
- Siblings and duplicates: no duplicate (grep for the DOI, the Zenodo id, "hair dye"). External collections: RamanBench (A.18.4, Table 52; raman-data `hair_dyes_sers`, not marked grouped).
- Better data: a candidate of the benchmark RamanBench; no new search (run brief).
- Papers and pages: the paper (PLS-DA; "individual colorants could be identified with on average 97% accuracy, whereas different brands can be predicted with nearly 100% accuracy", abstract); RamanBench A.18.4.
- Metric: the paper reports accuracy only (abstract; RamanBench A.18.4: brand-level PLS-DA accuracy 99.3-100%), with no threshold or costs, so the fallback `log_loss` (multiclass; MET-6, MET-8); inputs: the dye as the group, built exactly from `Brand`, `Type`, `Color` or the `Label` stem (SPLIT-24).
- Risks for /add-dataset: under a random split the brand is nearly perfect (a `Trivial` question, TP-4); grouped by dye there are about 33 groups and L'Oréal holds about 150 spectra (dyes per brand not counted; TP-8); each dye was recorded on its own date, so instrument drift travels with the label (a `Class-dependent Recording` question, LEAK-13); the target is the curator's choice (brand, type, colour or the colorant, USE-5); raw spectral bins (SEL-15).
- Priority: gap + (multiclass thin), use case 0 (approximate), source + (paper and the authors' release), shape 0 (33 dyes as units), risk - (near-perfect separation, recording by date).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark RamanBench (https://arxiv.org/abs/2605.02003).
- as published: 1,713 spectra x 1,340 wavenumber features; 4 classes (raman-data id: hair_dyes_sers); target: brand (Ion, Wella, Clairol, L'Oreal).
- Why: Identify the hair-dye brand on coloured hair from SERS spectra (forensics)
- Notes: Raw Raman spectral bins (1,340 wavenumber points, 309-1952 cm-1) as features; SEL-15 judges such signals case by case. 33 dyes; colorant identity, type and colour are also labelled. Data posted on Zenodo in 2026, paper 2022. HF mirror: https://huggingface.co/datasets/HTW-KI-Werkstatt/RamanBench/tree/main/hair_dyes_sers
