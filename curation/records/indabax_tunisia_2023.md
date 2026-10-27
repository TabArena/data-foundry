---
unique_name: indabax_tunisia_2023
name: indabax-tunisia-2023
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/indabax-tunisia-2023/data
source_row: 976
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Wrong Domain / Source Modality`, SEL-12): "Sequence-based predictor for the impact of mutation on protein stability", a 20-hour IndabaX Tunisia 2023 hackathon with InstaDeep (13 to 14 May 2023), predicting ddG of a single amino-acid mutation from protein sequences.
- Source: https://zindi.africa/competitions/indabax-tunisia-2023; as published: train.csv (54 MB), test.csv, columns ID, pdb_id, mutation (XnY), wt_seq, mut_seq, ddg; the page names the "Mega-scale dataset" as its origin (Tsuboyama et al., Nature 2023), so the first publication is not Zindi (PROV-8).
- Why out: the inputs are raw amino-acid sequences, where protein language and structure models are the tool; the page itself asks for "a Deep Learning algorithm that is trained on the amino acid sequences". The only tabular-looking columns (pdb_id, the mutation code) are identifiers of the sequence pair.
- Siblings: `instadeep_enzyme_classification_challenge`, `instadeep_kinase_classification_challenge` (sequence tasks of the same sponsor, proposed `No` on SEL-12 in the same batch).
- Metric: RMSE, Zindi Evaluation page ("The evaluation metric for this competition is Root Mean Squared Error").
- Reject check (AI, 2026-10-22): stands. The page asks for 'a Deep Learning algorithm that is trained on the amino acid sequences of wild-type (WT) proteins and mutant proteins'. The inputs are wt_seq and mut_seq (Mega-scale ddG data, Tsuboyama et al. 2023), where sequence and protein language models are the tool (SEL-12); the only other columns are identifiers. https://zindi.africa/competitions/indabax-tunisia-2023

IndabaX Tunisia 2023 is a Zindi hackathon with no task description in the record, so target, modality, and size are unknown. IndabaX hackathons are usually real tabular prediction tasks, so it should not be rejected for missing info alone. A human must check the Zindi page for the actual target, confirm tabular modality, and verify size and split regime.
