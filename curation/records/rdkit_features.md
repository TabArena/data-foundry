---
unique_name: rdkit_features
name: rdkit_features
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Trivial
- AHDS (Artifical/Handmade/Deterministic/Simulated)
tags:
- AI-Filled (Verify)
collections:
- ChemPile
source_links:
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/rdkit_features ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/rdkit_features ; original: https://huggingface.co/datasets/maykcaldas/smiles-transformers'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Trivial`, `AHDS (Artifical/Handmade/Deterministic/Simulated)`, SEL-5; SEL-16): the "targets" are RDKit descriptors computed from the input SMILES by a published deterministic function, so the input is the whole task and nothing is observed.
- Source: Hugging Face maykcaldas/smiles-transformers (created 2023-04-04, MIT; the card says "TODO: Add references to the datasets we curated"): 1,009,179,703 SMILES (908,086,717 train, 50,487,919 test, 50,605,067 validation) with formula, NumHDonors, NumHAcceptors, MolLogP ("Wildman-Crippen LogP"), NumHeteroatoms, RingCount, NumRotatableBonds, NumAromaticBonds, NumAcidGroups, NumBasicGroups and Apol. ChemNLP's meta: "Molecular descriptors computed using RDKit"; its transform reads the columns as they are. The SMILES' own origin is not named either.
- Use case: none; text prompts for pretraining chemical language models (ChemPile-LIFT, 71,999,880 prompts).
- Siblings and duplicates: none; precedent for a label computed by a rule from the inputs: `central_international_medical_college_and_hospital_health_risk_prediction` (NEWS2, `Trivial`, SEL-5). External collections: ChemPile (ChemPile-LIFT `rdkit_features`), ChemNLP.
- Better data: no new search; a candidate of the benchmark ChemPile.
- Reject check (AI, 2026-10-31): stands. ChemNLP's meta: 'Molecular descriptors computed using RDKit' (https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/rdkit_features): each target (NumHDonors, RingCount, MolLogP, ...) is a published deterministic function of the input SMILES, the case SEL-5 calls `Trivial` when the inputs are the whole task, and nothing is observed (SEL-16). The SMILES origin is unnamed on the card ('TODO: Add references'), but that does not matter for the call.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 1,009,179,703 descriptor records in ChemNLP; 71,999,880 prompts in ChemPile-LIFT; in ChemPile-LIFT 71,999,880 text prompts over 1 config(s); target: RDKit descriptor values.
- Why: Report RDKit descriptors (H-bond donors, logP, ring count, ...) computed from a SMILES
- Notes: The 'labels' are deterministic functions of the input SMILES computed by RDKit, so there is nothing to predict. Out of scope.
