---
unique_name: peptides_hemolytic
name: peptides_hemolytic
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Wrong Domain / Source Modality
tags:
- AI-Filled (Verify)
collections:
- ChemPile
original_source: Github
year: '2022'
problem_type: Binary Classification
source_links:
- https://github.com/ur-whitelab/peptide-dashboard/tree/master/ml/data
- https://doi.org/10.1093/nar/gkaa991
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/peptides_hemolytic ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/peptides_hemolytic ; original: https://github.com/ur-whitelab/peptide-dashboard (ml/data/hemo-positive.npz, hemo-negative.npz) ; DBAASP https://dbaasp.org'
- https://arxiv.org/abs/2505.12534
- https://doi.org/10.1021/acs.jcim.2c01317
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: measured hemolysis of antimicrobial peptides from DBAASP, a real safety screen, but the only input is the amino-acid sequence (sequence-only tasks went `No` as NLP data before) and one sequence often carries both labels.
- Source: compiled by the White lab (University of Rochester) from DBAASP v3 (Pirtskhalava et al. 2021, NAR 49:D288) and first published as `ml/data/hemo-positive.npz` and `hemo-negative.npz` in github.com/ur-whitelab/peptide-dashboard (committed 2022-01-14), with Ansari and White, "Serverless Prediction of Peptide Properties with Recurrent Neural Networks" (bioRxiv 2022-05-18; JCIM 2023, doi 10.1021/acs.jcim.2c01317). Sec. 2.1.1: "If the activity is below 100 μg/mL, it is considered hemolytic", the activity being the concentration at which 50% of red blood cells are lysed; "The training data contains 9316 sequences (19.6% positives and 80.4% negatives)"; "Each measurement is treated independently, so sequences can appear multiple times." Counted on the files (a preview): 1,826 positive and 7,490 negative rows, 6,076 unique sequences, 465 of them in both classes, lengths 1 to 190 (median 17; 17 rows of length 1). ChemNLP and ChemPile keep the unique sequences per class: 6,541 rows.
- Use case: a peptide designer screens antimicrobial-peptide candidates for red-cell toxicity before synthesis and testing ("It is critical to identify non-hemolytic antimicrobial peptides as a non-toxic and safe measure against bacterial infections", ChemNLP's description of the set). Fit direct for the screen; the label is a 100 μg/mL cut of HC50 values pooled from many labs. Regime: grouped by sequence at least (repeated and conflicting measurements of one sequence); a similarity-grouped split is the field's question.
- Siblings and duplicates: `peptides_nonfouling` and `peptides_soluble` come from the same repository and paper but are other tasks (PROV-7); no other hemolysis record. Sequence-only precedents: `antigen_avida_hil6` (`No`, `Wrong Domain / Source Modality`, `NLP (Text)`, Lennart, Mustafa, Alex: "NLP task / data"), `protein_location_prediction_challenge` (`No`, SEL-12, AI unverified), `african_snake_antivenom_binding_challenge` (`TBD -> 2nd Tier`: its SEL-12 reject was refuted, no evidence that sequence models are clearly better). External collections: ChemPile (ChemPile-LIFT `peptides_hemolytic`), ChemNLP; PeptideBERT (Guntuboina et al. 2023) used the same three peptide sets.
- Better data: no new search; a candidate of the benchmark ChemPile. DBAASP holds the HC50 values behind the label and is updated continuously (v3: "contains >15 700 entries"), the origin to build from.
- Papers and pages: Ansari and White 2023, Table 1: Bi-LSTM AUROC 0.84, UniRep + logistic regression 0.81, UniRep + random forests 0.78, one-hot RNN 0.87; HAPPENN (ACC 85.7%) and HLPpred-Fuse (AUROC 0.91), feature-based methods, as reported by their authors.
- Metric: `roc_auc`, the fallback (MET-5): the paper selects "in terms of the Area Under the Receiver Operating Characteristic (AUROC) curve and accuracy" (Sec. 2.2), two metrics side by side; no threshold or cost fixed. Inputs: none.
- Risks for /add-dataset: SEL-12 is the open question: whether a tabular model on sequence descriptors (composition, physico-chemical indices) is competitive. In Table 1 the classical and embedding baselines sit close to the RNN, so it is not clearly out, but the curators' precedent leans out. The conflicting labels (465 sequences in both classes) and the per-measurement rows need a rule (aggregate per sequence, or group). The length-1 rows look like decoding artefacts. ChemNLP's meta cites unrelated papers (a blood-brain-barrier paper and MoleculeNet) and gives all three peptide sets the same num_points (6,541), a problem of that copy (PROV-15).
- Priority: gap 0 (no thin value), use case + (the source names the safety screen of AMP candidates), source + (DBAASP and a peer-reviewed paper), shape 0 (thousands of sequences, but one string input and no tabular features as published), risk - (the modality under SEL-12, conflicting labels).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 6,541 peptides (ChemNLP); in ChemPile-LIFT 137,361 text prompts over 1 config(s); target: hemolytic (1/0).
- Why: Classify whether a peptide lyses red blood cells, the safety screen for antimicrobial peptide candidates
- Notes: Assembled from DBAASP (Pirtskhalava et al. 2021, NAR 49:D288) for the peptide dashboard of Barrett and White; the ChemNLP meta cites Wu et al. 2022 (doi 10.1021/acs.jcim.2c01317) as the compilation. Features: the amino-acid sequence only, so a container would add sequence descriptors. No record.
