---
unique_name: toxvaldb_in_vivo_toxicity_values
name: 'ToxValDB v9.7.0: experimental and derived human-health toxicity values (US EPA)'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
original_source: GOV Website
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
source_links:
- https://doi.org/10.23645/epacomptox.20394501
- https://doi.org/10.1016/j.comtox.2025.100365
- https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data
- https://comptox.epa.gov/dashboard/
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: the US EPA's ToxValDB, a large and maintained compilation of in vivo toxicity values; a repeat-dose point of departure from structure is a real task, but the table would be our own selection and aggregation from 51 compiled sources mixing experiments with derived guideline values.
- Source: US EPA, ToxValDB v9.7.0 (figshare doi 10.23645/epacomptox.20394501, CC0, version of 2025-09-24, which links the files on ScienceBase; earlier versions are archived there): "The Toxicity Value Database (ToxValDB) is a large compilation of human health-relevant in vivo toxicology data, including data on both in vivo toxicity experiments and derived toxicity and guideline values." EPA's download page: v9.7.0, "249,071 records, 41,855 chemicals (27,068 with defined chemical structure), and 51 sources (74 source tables)". The paper: Wall, Sayre, Smith, Winter, Groover, Hope et al., "Development of the toxicity values database, ToxValDB: A curated resource for experimental and derived human health-relevant toxicity data", Computational Toxicology 35:100365 (2025, doi 10.1016/j.comtox.2025.100365; not read, no abstract on Crossref). The columns and any experimental-record flag were not previewed (files on ScienceBase, not opened).
- Use case (written by the curation): a risk assessor screening a data-poor chemical estimates a repeat-dose point of departure (for example a rat oral NOAEL or LOAEL in mg/kg-day) from its structure, to prioritise it for testing or set a provisional value; fit approximate, since the table would be our own selection. Regime grouped by chemical or scaffold, because a chemical has several values and the use case is an untested chemical (SPLIT-31).
- Siblings and duplicates: `qsar_oral_toxicity` (`Yes`, acute oral toxicity, CATMoS), `ld50_zhu` (`TBD -> 2nd Tier`, rat oral LD50), `tdc_ld50_zhu` (`No`, `Duplicate`), `sigma_aldrich_safety_data` (`TBD -> 2nd Tier`, GHS hazard statements): acute or hazard endpoints, distinct from a repeat-dose point of departure (PROV-7). ToxRefDB v3.0 (EPA, "in vivo study data from over 6000 guideline or guideline-like studies for over 1000 chemicals", August 2025) is one of the kinds of source ToxValDB compiles and has no record. External collections: the awesome-chemistry-datasets list.
- Better data: from the awesome-chemistry-datasets list and the curator's Zotero collection (item 110); no further search this round.
- Papers and pages: Wall et al. 2025 (the data paper, not read); EPA's models of points of departure on ToxValDB were not checked (this session's web search budget ran out).
- Metric: none found (EPA download page, figshare page); so the fallback `rmse`, on log10 mg/kg-day as the field models it (MET-3). Inputs none.
- Risks for /add-dataset: experimental values and derived values (RfD, ADI, guideline values) are mixed and must be filtered to experimental records of one species, route and study type (PROV-11: the EPA release is the origin of our build); unit harmonisation; several values per chemical from overlapping sources, to aggregate or group (LEAK-19); structures from DSSTox and descriptors computed by us (`apistox` precedent); about 15,000 chemicals without a defined structure drop out; the per-endpoint chemical counts are unknown until the file is opened.
- Priority: gap 0 (chemistry & material science, regression and grouped are covered), use case 0 (written by the curation), source + (EPA release with a paper), shape + (249,071 records over 27,068 chemicals with a structure, before filtering), risk - (our own selection and aggregation of a compilation).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 110: "Robust White Blood Cell Classification with Stain-Normalized Decoupled Learning and ...".
- as published: 249,071 records, 41,855 chemicals (27,068 with a defined structure) from 51 sources (EPA page); one row per toxicity value with chemical, species, route, study type and duration, value and units; target: an experimental in vivo point of departure on one study type, e.g. rat oral repeat-dose NOAEL or LOAEL (mg/kg-day); access: open.
- Why: measured animal-study values, large, maintained by the agency that uses them
- Adds: a repeat-dose endpoint next to qsar_oral_toxicity (acute LD50). Risks: experimental values and derived guideline values (RfD, ADI) are mixed and must be filtered to experimental records; several values per chemical (group by chemical); heterogeneous designs and units; the table would be our own subset
