---
unique_name: mtp2
name: OpenML-430 mtp2
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
collections:
- TabBench-Bio
domain: chemistry & material science
problem_type: Regression
source_links:
- https://doi.org/10.1021/ci020280x
- https://www.openml.org/d/430
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 1: melting points of 274 drugs from 1,142 unnamed Adriana.Code descriptors, one of OpenML's 41 drug-design sets; the curator rejected two of its siblings (`topo_2_1`, `yprop_4_1`), and three larger melting-point records exist.
- Source: Bergström, Norinder, Luthman and Artursson, "Molecular descriptors influencing melting point and their role in classification of solid drugs", J Chem Inf Comput Sci 43:1177-1185 (2003; doi 10.1021/ci020280x, PMID 12870909): "The melting points for 277 structurally diverse model drugs were extracted from the 12th edition of the Merck Index", with descriptors from Molconn-Z, Selma, MacroModel and Marea, modelled by PLS. OpenML 430 (uploaded 2014-09-28, "Source: Unknown - Date unknown"): "This is one of 41 drug design datasets. The datasets with 1143 features are formed using Adriana.Code software ... The molecules and outputs are taken from the original studies". As published: 274 x 1,142 numeric descriptors (`oz1` ...) and the target `oz1143`, with no molecule names or structures.
- Use case: a formulation scientist estimates a drug candidate's melting point from its structure before making it (solid-state and solubility screening). Fit approximate: the OpenML table is not the paper's (other descriptors, 274 of the 277 drugs, computed by an unnamed party). Regime IID (one row per compound; a scaffold split cannot be built without structures).
- Siblings and duplicates: `topo_2_1` and `yprop_4_1` (the same 41-set family, `No`, `Missing source information`, `Data Quality Issue`; CC: "one of 41 drug design datasets ... OpenML version seems not to match paper version and therefore CTR23 excluded these datasets"). What may set mtp2 apart: its target's study is named with a DOI; against that, its features were recomputed, further from the paper. Melting-point records with structures and many more compounds: `melting_point` (Kaggle 2025), `bradley_open_melting_point` (about 20,000 compounds), `melting_point_patents` (about 275,000). External collections: TabBench-Bio (Table 4).
- Better data: a candidate of the benchmark TabBench-Bio (the run searched no further); the larger melting-point data have records already (above).
- Papers and pages: Bergström et al. 2003 (abstract read; full text paywalled); https://www.openml.org/d/430.
- Metric: the paper fits PLS, reports the variance explained ("explain 63% of the melting point") and a three-class low/intermediate/high ranking, with no single ranked criterion (MET-5); TabBench-Bio ranks regression by RMSE. Fallback `rmse` in degrees.
- Risks for /add-dataset: consistency with the siblings' `No` (principles, "Consistent judgement"): the curator decides whether the named study sets mtp2 apart, or retires it with them; the descriptor columns are unnamed (`Anonymized`); without structures, duplicates and scaffolds cannot be checked (SPLIT-24); 274 rows.
- Priority: gap 0 (chemistry has 12 accepted), use case 0, source 0 (the table's maker unknown), shape 0 (274 rows), risk - (a reworked version, larger data recorded).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 274 x 1,142; target: oz1143 (melting point).
- Why: Melting point of drug compounds from Adriana.Code molecular descriptors (one of the 41 OpenML drug-design sets)
- Notes: Related: topo_2_1 and yprop_4_1 (same 41-set family, both 'No') and melting_point (Kaggle 2025, a different and larger source).
