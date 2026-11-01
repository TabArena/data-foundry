---
unique_name: blended_cement_concrete_strength
name: Blended Cement Concrete Database (literature-derived compressive strength records)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- Non-IID (Grouped)
- AI-Filled (Verify)
original_source: Other
year: '2026'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.5281/zenodo.18080350
- https://doi.org/10.1038/s41524-026-02304-6
- https://arxiv.org/abs/2604.22938
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: 8,979 compressive-strength tests from 260 papers (2026), the task of `concrete_compressive_strength` with nine times the rows, more binder types and the curing conditions, documented by a peer-reviewed paper that scores RMSE; the rows were extracted by an LLM pipeline, with over 80% checked by hand.
- Source: Li, Yang, He, Gong, "Blended Cement Concrete Database", Zenodo doi 10.5281/zenodo.18080350 (v1 of 2026-08-27, CC BY-NC 4.0, one file blended_cement_concrete_database.csv, 839.5 kB); paper "Large language model-enabled automated data extraction for concrete materials informatics", npj Computational Materials 12, 341 (2026), doi 10.1038/s41524-026-02304-6 (arXiv 2604.22938, read in part). As published (Zenodo): "8,979 experimental records from 260 source publications"; mixture amounts (cement, blast-furnace slag, fly ash, silica fume, limestone powder, calcined clay, water, superplasticizer, coarse and fine aggregate), curing age, temperature and relative humidity, specimen volume and aspect ratio, compressive strength, and the source DOI; extracted by an LLM pipeline, cleaned in several stages, "more than 7,500 records (over 80%)" checked by hand; binder oxides and fineness are left for a later version; about 260 cross-paper duplicates removed (Methods 4.4).
- Use case: a mix designer predicts the strength of a proposed mix at a given age before casting trial batches; the paper aims at "reliable data-driven concrete design" (Sec. 2.3.2) and calls out-of-distribution generalisation "a critical capability for practical concrete materials design" (Methods 4.5). Fit direct. Regime grouped: one mix is tested at several ages, as in `concrete_compressive_strength`, whose split groups by mix, and a new design is a mix not tested before (SPLIT-23, SPLIT-24); the source DOI would be the stricter group (a new laboratory).
- Siblings and duplicates: `concrete_compressive_strength` (Yes, shipped; Yeh's 1,030 tests, grouped by mix) and `concrete_compressive_strength_duplicate` (No). The paper calls Yeh's set "the most widely explored dataset in the field" that "contains only 1,030 records" (Sec. 2.3); whether Yeh's sources are among the 260 papers was not checked (shared rows, not a duplicate dataset, PROV-4). External collections: none found.
- Better data: found as better data for `concrete_compressive_strength`; no further search this round.
- Papers and pages: the paper above; its extraction benchmark (Zenodo doi 10.5281/zenodo.22132836, moved here from `source_links`: a companion of the paper, not the data, PROV-12). The scout also saw a UHPC set (Data in Brief 2025, 2,188 mixes) and an SCM-blended set (Mendeley, 1,456 mixes, 28-day strength only): another concrete class, or smaller.
- Metric: "Model performance was evaluated using root mean square error (RMSE) as the primary metric" (Methods 4.5): one deliberate choice (MET-5), `rmse` in MPa; inputs none. The paper's in-distribution split is random 80/20 with records of identical inputs kept together; its out-of-distribution split holds out ternary and quaternary blends.
- Risks for /add-dataset: LLM-extracted values, up to 20% not checked by hand (units, decimals; run the PROV-3 tests on the shipped columns); mix groups to build from identical proportions and curing (LEAK-17); test standards and specimen shapes differ across papers (specimen volume and aspect ratio are columns); `null` for unreported conditions.
- Priority: gap 0 (chemistry & material science, regression and grouped not thin), use case + (concrete design, named by the paper), source + (peer-reviewed paper and Zenodo deposit), shape + (8,979 tests, 16 inputs, mix and paper groups), risk - (LLM-extracted values).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `concrete_compressive_strength`.
- as published: 8,979 test records (one strength result per row) from 260 publications, one 839 kB CSV; columns: 10 mixture amounts (cement, blast-furnace slag, fly ash, silica fume, limestone powder, calcined ...; target: compressive strength (MPa) of a mix at the given curing age; access: open.
- Why: Same target and the same kind of inputs as UCI concrete (cement, slag, fly ash, water, superplasticizer, coarse and fine aggregate, age); Yeh's set is itself a compilation of lab tests from several sources, as this one is. Real measured values from published experiments, each row traced to its source DOI; rows were ...
- Adds: About 9x the rows (8,979 against 1,030) from 260 studies instead of 17 sources, newer studies, more binder types (silica fume, limestone, calcined clay) plus curing temperature, humidity and specimen size; the source DOI gives a natural group for a grouped split (the record already groups by mix). Caveats: CC BY-NC ...
