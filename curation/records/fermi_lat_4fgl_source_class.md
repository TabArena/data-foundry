---
unique_name: fermi_lat_4fgl_source_class
name: 'Fermi-LAT 4FGL-DR4 gamma-ray source catalog: source class of associated sources'
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/
- https://arxiv.org/abs/2307.12546
- https://doi.org/10.3847/1538-4365/ac6751
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the same NASA FSSC 4FGL-DR4 catalog file (gll_psc_v35.fit, "The catalog has 7194 sources") and the same CLASS1 source-class target as `fermi_4fgl_dr4_source_classes` (screened `TBD -> Yes`, priority 3, in this run), which keeps the task; this record adds only the DR3 ApJS DOI (https://doi.org/10.3847/1538-4365/ac6751), to carry over to that record.
- Source: the Fermi-LAT collaboration's 14-year catalog page (https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/): "The catalog has 7194 sources", gll_psc_v35.fit (DR4 revision 4 of 2024-07-24, first DR4 release 2023-07-24), "covering the time period August 4, 2008, to August 2, 2022", "Upper case in the CLASS1 column means identified", and "Please cite both documents when you use this data release" (DR4, arXiv 2307.12546; DR3, "Incremental Fermi Large Area Telescope Fourth Source Catalog", ApJS 2022, the DOI above).
- Siblings and duplicates: `fermi_4fgl_dr4_source_classes` links the same FSSC page and arXiv 2307.12546 and takes the same CLASS1 target; its own block says "`fermi_lat_4fgl_source_class` ... the same catalog file and the same CLASS1 target, a duplicate record (PROV-4)". This record came from the curator's Zotero collection (item 45, "Higgs Real world dataset and co"), the other from the physics and astronomy gap scout; the Zotero origin can be noted there.
- Better data: from the curator's Zotero collection (item 45); no search for better data in this run.
- The task stays a candidate under `fermi_4fgl_dr4_source_classes`, with its risks (selection bias of associated sources, the class set, class-dependent spectral models).
- Reject check (AI, 2026-10-31): stands. Both records link the same FSSC page (https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/: 'The catalog has 7194 sources', gll_psc_v35.fit, 'Upper case in the CLASS1 column means identified', checked 2026-10-31) and arXiv 2307.12546. This record's own Assessment takes the same CLASS1 target of associated sources, so it adds no task and the source is confirmed (PROV-5). Carry the DR3 ApJS DOI (10.3847/1538-4365/ac6751) and the Zotero origin (item 45) over to fermi_4fgl_dr4_source_classes.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 45: "Higgs Real world dataset and co".
- as published: 7,194 gamma-ray sources, 14 years of LAT data (2008-2022), a few dozen spectral, variability and position columns (FITS gll_psc_v35.fit); roughly a third unassociated (count to verify on CLASS1); target: source class (e.g. pulsar vs blazar subtypes BLL/FSRQ/BCU) of associated sources, CLASS1; access: open.
- Why: A real-world labelled physics classification task from catalog measurements (not Monte Carlo), with a long ML literature on classifying unassociated sources; it answers the 'real-world instead of simulated Higgs' reading of the note.
- Adds: A real, non-simulated physics task. The Higgs/SUSY/HEPMASS/MiniBooNE family is all simulated and rejected. Tentative: the note has no text, so its intent is a guess. Risk: associated sources are brighter than unassociated ones (selection bias between labelled and deployment rows).
