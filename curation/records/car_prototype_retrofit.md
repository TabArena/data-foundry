---
unique_name: car_prototype_retrofit
name: Prototype vehicle retrofit occurrence, type and duration (anonymized industrial data)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
original_source: Github
year: '2026'
domain: industry & manufacturing
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://github.com/aina-vila-pons/retrofit-forecast-pipeline
- https://arxiv.org/abs/2606.15314
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: an unnamed carmaker's prototype register (284,271 vehicles) and retrofit visits (48,716) from a master's thesis, with every value hashed, the dates included, so the duration target and a temporal split cannot be built, and the binary target's AUC of 0.997 points to a leak; the 15-class retrofit type is the task left.
- Source: Vila Pons, Tzachristas and Antoniou, "LLMs on Tabular Data with Limited Semantics: Evidence from Industrial Car Retrofit Prediction", arXiv 2606.15314 (2026-06-13); data and code with the master's thesis "Automation of Forecasts for Retrofits of Development Vehicles" at github.com/aina-vila-pons/retrofit-forecast-pipeline (created 2026-05-07; README: "All rights reserved", noted only, EV-4). As published (the zip's directory and both file heads previewed 2026-10-31): `data_sources.zip` (11 MB) with anonymized_data_prototypes_DAVE.csv (57 MB, 22 columns such as derivat, vnumber, prio_int, pep_bauphase, istufe, anlauf_sop_at, hybrid, antriebsart, motortyp, rueckgabe_soll, key) and anonymized_data_retrofits_APEX.csv (16 MB, 30 columns such as derivat, v_nummer, prio, ur_paket_name, werkstatt_name, start_ur, av_ur, umruststatus, umruestart, sab_termin, ziel_i_stufe, id_fzg); the column names are kept and every value is a 12-character hash, the dates (`start_ur`, `av_ur`, `anlauf_sop_at`, `rueckgabe_soll`) too.
- Use case: the planners of a development fleet decide, for each registered prototype, whether and which retrofit to schedule and how much workshop time it takes (thesis README: "whether development vehicles will come for retrofit, what type of retrofit they will undergo, how long it will take, and when it will happen"); fit approximate; regime temporal by nature (prototypes and retrofits over development phases), but with hashed dates only a forced IID or a split grouped by vehicle line (`derivat`) is possible (SPLIT-7, SPLIT-8).
- Siblings and duplicates: none (grep retrofit, prototype). External collections: none found.
- Better data: from the curator's Zotero collection (item 207); no further search this round.
- Papers and pages: the arXiv paper (abstract read: tree ensembles strongest, binary AUC 0.982 with embeddings, multiclass weighted F1) and the thesis repository.
- Metric: the paper reports binary AUC and multiclass weighted F1 side by side, with no threshold or costs fixed, so the fallback (`roc_auc` for the binary, `log_loss` for the 15-class type; MET-5, MET-6); inputs none.
- Risks for /add-dataset: `Anonymized`: every value is hashed, so what a column measures and when it is known can only be read from the German names; the duration target needs the hashed dates and cannot be built; the binary label comes from the join itself (a prototype with a retrofit row), and the retrofit system's status and target fields may exist only once a retrofit is planned (LEAK-10; the record's AUC of 0.997); two tables joined on hashed vehicle ids.
- Priority: gap + (multiclass is thin), use case 0 (approximate), source 0 (a thesis repository; the company and its systems unnamed), shape + (48,716 visits, 30 columns), risk - (hashed dates, a likely leak).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 207: "LLMs on Tabular Data with Limited Semantics: Evidence from Industrial Car Retrofit ...".
- as published: data_sources.zip (11 MB) with anonymized_data_prototypes_DAVE.csv (284,271 prototype vehicles) and anonymized_data_retrofits_APEX.csv (48,716 cleaned retrofit visits; 54,174 rows after the join, ...; target: (a) came_for_retrofit, binary, 4.4% positive; (b) retrofit type umr_art, 15 classes; (c) retrofit duration in days (umr_av - umr_start, log1p); access: open.
- Why: Real operational manufacturing data, rare in public, with large tables and high-cardinality categoricals. The type and duration targets are not trivially solved (AutoGluon weighted F1 0.654, duration R2 0.38).
- Adds: An industrial planning task the collection lacks. Caveats: the repo has no license file and its README says 'All rights reserved', so redistribution needs the authors' permission; hashed values call for the Anonymized marker; the binary AUC of 0.997 under a random 80/20 split suggests a leak (priority or deadline ...
