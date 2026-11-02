---
unique_name: snakes_and_sequences_senegalese_serpent_venom_sequencing_hackathon
name: snakes-and-sequences-senegalese-serpent-venom-sequencing-hackathon
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
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/snakes-and-sequences-senegalese-serpent-venom-sequencing-hackathon/data
source_row: 966
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `No` (`Wrong Domain / Source Modality`, SEL-12): de novo peptide sequencing from raw mass spectra; the target is a peptide sequence.
- Source: Zindi hackathon by InstaDeep at Deep Learning Indaba Senegal, 2-6 September 2024, 101 participants, 5,000 USD (https://zindi.africa/competitions/snakes-and-sequences-senegalese-serpent-venom-sequencing-hackathon, read through the Zindi API); as published: Train.csv (507 MB, 100,000 MS2 spectra from InstaNovo's validation set), Test.csv (223 MB, spectra of Senegalese snake venoms), columns precursor m/z, mass, charge, retention time, `mz_array`, `intensity_array`, ten InstaNovo beam outputs and log-probabilities, and `target`, "the ground truth peptide".
- Use case: identifying venom peptides for antivenom research; the task is sequence decoding from spectra, where spectrum models (InstaNovo, a transformer) are the tool.
- Siblings: `african_snake_antivenom_binding_challenge` (UmojaHack 2022, binding, `TBD -> 2nd Tier`, AI) is another task.
- Metric: area under the precision-recall curve of the predicted peptides ranked by confidence (Zindi Evaluation page).
- Reject check (AI, 2026-10-22): stands. SEL-12 (Must), from the source's words: "Each row contains an MS2 spectrum representing a peptide to be identified ... mz_array: Mass-to-charge values of the MS2 spectrum ... intensity_array: Intensity values ... target: This is what you are predicting: the ground truth peptide"; submissions are a peptide string plus a confidence ("ID_3qQWny VSEELED 0.4") (https://api.zindi.world/v1/competitions/snakes-and-sequences-senegalese-serpent-venom-sequencing-hackathon). De novo sequencing from raw spectra is the domain of spectrum models (InstaNovo); the target is a sequence, neither a class nor a number. A tabular 'is beam 0 correct' rescoring task would be our own reframing (SEL-8).

A Zindi hackathon about Senegalese serpent venom sequencing. By its name this is genomic/protein-sequencing biology data (a scientific-discovery / sequence-modeling task) rather than a standard tabular predictive problem with a clear target. The raw modality (sequence data) and discovery framing put it out of scope for representative tabular ML. The record has no field details, so a human should confirm whether any flat tabular target table actually exists, but the strong prior is reject.
