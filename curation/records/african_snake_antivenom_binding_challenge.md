---
unique_name: african_snake_antivenom_binding_challenge
name: African Snake Antivenom Binding Challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2022'
domain: biology & life sciences
required_split:
- '?'
problem_type: TBD
source_links:
- https://zindi.africa/competitions/umojahack-africa-2022-advanced-challenge/data
source_row: 1011
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the proposed fast reject (SEL-12) did not hold in the reject check, so it stays a candidate with the doubt listed.
- Proposed reject (refuted): `No` (`Wrong Domain / Source Modality`, SEL-12): the input is a 16-mer amino-acid string per row, a protein-sequence task where sequence models are the tool; the remaining columns (toxin id, positions, antivenom, taxonomy) only index the sequence.
- Source: Zindi "UmojaHack Africa 2022: African Snake Antivenom Binding Challenge (ADVANCED)", 2022-03-19 to 2022-03-20, InstaDeep, 252 participants (Zindi API); data from a high-density peptide microarray study of eight African antivenoms (PLOS NTD, doi 10.1371/journal.pntd.0008366): "16-mer peptides ... derived from toxin protein sequences representing 40 snake species and 481 proteins"; Signal "normalised and ... represented as Z-score". Columns: ID, Toxin_UniprotID, Position_start, Position_end, Antivenom, Toxin_K_mer, Signal (target), Genus, Species, ProteinFam, ProteinSubFam, ProteinSubSubFam; Zindi `data_type` "Unstructured".
- Use case: "predict what other toxins a given antivenom could be effective against" (research screening); real, but the information is the sequence.
- Siblings and duplicates: same pattern as `instadeep_kinase_classification_challenge` (`No`, `NLP (Text)`, `Wrong Domain / Source Modality`, AI unverified) and `instadeep_enzyme_classification_challenge`; no duplicate.
- Metric: Root Mean Squared Error on Signal (Zindi Evaluation page).
- The old markers `No Good Target  / Scientific Discovery` and `Needs extensive data wrangling` are not the reason: the target is a measured signal and the table ships as one file.
- Reject check (AI, 2026-10-22): does not stand. SEL-12 is judged per dataset and needs modality-specific models to be clearly better. The input is a fixed-length 16-mer plus the antivenom name, so it vectorizes to 16 positional categoricals. The page shows only that sequence NNs were used, not that they are clearly better. The 2nd-place post: LSTM on residue embeddings, "I think the baseline was not bad after all", 1D CNNs "didn't improve the performance", ProtBERT too slow and not used. No tabular baseline is reported. Zindi tags it Unstructured/NLP. https://zindi.africa/competitions/umojahack-africa-2022-advanced-challenge/discussions/11087
- For /add-dataset: TBD -> 2nd Tier, priority 1. The add stage must: (1) probe a GBM on the 16 positional residues plus antivenom (and the toxin taxonomy) against a small CNN/LSTM on the same rows. If the sequence model is clearly better, the verdict is No with SEL-12. (2) Use a split grouped by Toxin_UniprotID. Overlapping tiled k-mers share 15 of 16 residues, and the 2nd-place author found that a grouped CV lowered the score. (3) Check consistency with instadeep_kinase/enzyme (No, NLP), which take full-length sequences, unlike this one.

Predict how well eight commercial antivenoms bind/neutralize African snake toxins (UmojaHack 2022 advanced challenge). This is a scientific binding-affinity prediction that likely relies on protein/toxin sequence or molecular descriptors rather than naturally tabular features, and it is a scientific-discovery flavored task with potentially few distinct toxins. Both the modality (sequence-derived) and very small sample concerns make it questionable for representative tabular ML. A human must inspect whether features are genuinely tabular, the number of rows, and whether the multi-antivenom target is one regression task or a multi-output problem.

---

predict how well eight different commercial antivenoms work against African snake toxins
