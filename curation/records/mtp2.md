---
unique_name: mtp2
name: OpenML-430 mtp2
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Anonymized
tags:
- AI-Filled (Verify)
- Tiny Data
- Many features
- 'Samples: No Time Dimension'
- Experimental Results
collections:
- TabBench-Bio
domain: chemistry & material science
required_split:
- Random (IID)
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

**Screening (AI, 2026-11-25):** `TBD -> 2nd Tier`, priority 1: melting points of 274 drugs from 1,142 unnamed
Adriana.Code descriptors, one of OpenML's 41 drug-design sets; the curator rejected two of its siblings (`topo_2_1`,
`yprop_4_1`), and three larger melting-point records exist. Verdict and priority unchanged; the missing structures
now show up in the split, which is forced random because no scaffold can be computed.
- Source: Bergström, Norinder, Luthman and Artursson, "Molecular descriptors influencing melting point and their role
  in classification of solid drugs", J Chem Inf Comput Sci 43:1177-1185 (2003; doi 10.1021/ci020280x, PMID 12870909):
  "The melting points for 277 structurally diverse model drugs were extracted from the 12th edition of the Merck
  Index", with descriptors from Molconn-Z, Selma, MacroModel and Marea, modelled by PLS. OpenML 430 (version 1,
  uploaded 2014-09-28, licence Public, default target `oz1143`, "Source: Unknown - Date unknown", re-checked on the
  OpenML API 2026-11-25): "This is one of 41 drug design datasets. The datasets with 1143 features are formed using
  Adriana.Code software ... The molecules and outputs are taken from the original studies", and the page names
  Bergström et al. 2003 as the original study. As published: 274 x 1,142 numeric descriptors (`oz1` ...) and the
  target `oz1143`, with no molecule names or structures.
- Use case: a formulation scientist estimates a drug candidate's melting point from its structure before making it
  (solid-state and solubility screening). Fit approximate: the OpenML table is not the paper's (other descriptors,
  274 of the 277 drugs, computed by an unnamed party). Collection: melting points of a closed set of drugs taken from
  a reference work, a fixed property of the molecule that no source dates here (`Samples: No Time Dimension`); one
  row per compound, and without structures a repeat could not be seen at all; type `Experimental Results` (a closed
  set of molecules with laboratory-measured properties, SPLIT-34; not a catalogue, which rule 4 keeps for the growing
  database itself).
- Split: leaf L-EXP.no-kind-key (Random · `ForcedIIDFromGrouped`, no kind key) because [EXP.meets] is a chemical
  series the data does not contain (the scientist asks about the next candidate, not about another of these 274
  drugs) and [EXP.kind-key] no — the table ships 1,142 unnamed descriptors and no structure, so no Bemis-Murcko
  scaffold can be computed, the `bioresponse` case (SPLIT-35); open: whether the 274 rows can be matched back to
  Bergström et al.'s compound list, which would bring structures and turn the leaf into L-EXP.kind (the scaffold),
  and how much of the overlap a random split leaves can be measured at all without them.
- Siblings and duplicates: `topo_2_1` and `yprop_4_1` (the same 41-set family, `No`, `Missing source information`,
  `Data Quality Issue`; CC: "one of 41 drug design datasets ... OpenML version seems not to match paper version and
  therefore CTR23 excluded these datasets"). What may set mtp2 apart: its target's study is named with a DOI, which
  keeps it inside PROV-2 rather than PROV-1; against that, its features were recomputed, further from the paper.
  Melting-point records with structures and many more compounds: `melting_point` (Kaggle 2025),
  `bradley_open_melting_point` (28,645 measurements, about 20,000 compounds), `melting_point_patents` (about 242,000).
  External collections: TabBench-Bio (Table 4).
- Better data: `bradley_open_melting_point` (CC0, measured melting points with SMILES) and `melting_point_patents`
  (about 242,000 compounds text-mined from patents), both recorded: the same task, two to three orders of magnitude
  larger and with the structures this table lost. No new search this round.
- Papers and pages: Bergström et al. 2003 (abstract read; full text paywalled, PROV-17); https://www.openml.org/d/430
  and its API record.
- Metric: the paper fits PLS, reports the variance explained ("explain 63% of the melting point") and a three-class
  low/intermediate/high ranking, with no single ranked criterion (MET-5); TabBench-Bio ranks regression by RMSE.
  Fallback `rmse` in degrees. Inputs: none.
- Risks for /add-dataset: consistency with the siblings' `No` (principles, "Consistent judgement") is the first
  question for the curator — the only fact that sets mtp2 apart is the named study behind its target, while the
  "OpenML version does not match the paper version" problem is the same one (PROV-15); the descriptor columns are
  unnamed (`Anonymized`); without structures, duplicates and scaffolds cannot be checked (SPLIT-24, SPLIT-35); 274
  rows (`Tiny Data`, TP-5).
- Priority: gap 0 (chemistry & material science has 15 accepted), use case 0, source 0 (the table's maker unknown),
  shape 0 (274 rows), risk - (a reworked version, and larger data with structures already recorded).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: 274 x 1,142; target: oz1143 (melting point).
- Why: Melting point of drug compounds from Adriana.Code molecular descriptors (one of the 41 OpenML drug-design sets)
- Notes: Related: topo_2_1 and yprop_4_1 (same 41-set family, both 'No') and melting_point (Kaggle 2025, a different and larger source).

**CC (2026-11-25, Andrej):** stays `TBD -> 2nd Tier`, priority 1, with the sibling question recorded as a risk rather than settled as a reject.
- `topo_2_1` and `yprop_4_1` of the same OpenML family were rejected on their own facts (`Missing source information`, `Data Quality Issue`); that is no precedent for this record, which names its target study with a DOI.
- Whether the 274 rows match the source paper's compound list stays open (the paper is paywalled) and leads the record's risks.
