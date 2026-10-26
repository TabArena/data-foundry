---
unique_name: fair_higgs_boson_decay
name: A FAIR and AI-ready Higgs boson decay dataset (CMS H(bb) jets)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- AHDS (Artifical/Handmade/Deterministic/Simulated)
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
original_source: Website
year: '2021'
domain: physics & astronomy
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://arxiv.org/abs/2108.02214
- https://doi.org/10.1038/s41597-021-01109-0
- https://opendata.cern.ch/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`AHDS (Artifical/Handmade/Deterministic/Simulated)`, `Wrong Domain / Source Modality`; SEL-16, SEL-12): an open simulated CMS dataset of jets, simulated physics with its own benchmarks, whose informative content is variable-length particle lists.
- Source: Chen et al., "A FAIR and AI-ready Higgs boson decay dataset", arXiv 2108.02214 (2021), Scientific Data 9:31 (2022): "an open simulated dataset produced by the CMS Collaboration at the CERN Large Hadron Collider. This dataset consists of Higgs boson decays and quark and gluon background", on the CERN Open Data Portal (ROOT and HDF5). The paper is a FAIR-ness assessment guide; the data serves H(bb) jet tagging with particle-cloud and graph models.
- Precedent: `higgs` (CC 2026-09-22, Lennart: `No`, simulated physics with dedicated benchmarks, criterion 4B; that comment names "the FAIR Higgs decay set" among the field's own benchmarks). Related: `higgsml_2014` and `fair_universe_higgsml_uncertainty`, proposed `No` on the same ground in this re-screen.
- Modality: per-jet lists of particle-flow candidates, tracks and secondary vertices of variable length (SEL-12), as the old note quoted from the paper; not re-checked in the full text.
- Reject check (AI, 2026-10-22): stands. This follows the higgs precedent directly: Lennart's CC of 2026-09-22 in curation/records/higgs.md names 'the FAIR Higgs decay set' among the field's own benchmarks and rejects simulated physics with dedicated benchmarks. The source calls it 'an open simulated dataset produced by the CMS Collaboration' (https://arxiv.org/abs/2108.02214), so SEL-16 holds. The point about variable-length particle lists (SEL-12) comes from the old note and is not needed for the reject.

Chen et al., Scientific Data 9:31 (2022). CMS open *simulation* on the CERN Open Data Portal, released in ROOT and HDF5, CC0. One record is a jet: "the dataset consists of 3.9 million H(bb) jets and 1.9 million QCD jets". Branches are per-jet scalars plus variable-length lists of particle-flow candidates, tracks and secondary vertices ("there may be a variable number per jet"), built for jet tagging with particle-cloud / graph models.

Not a tabular task: the informative content is the variable-length constituent lists (source modality), so `Wrong Domain / Source Modality`, and it is simulated (criterion 4B). Per-jet scalar summaries could be tabulated but would recreate a weaker version of a benchmark that belongs to jet-tagging models. Data not inspected.
