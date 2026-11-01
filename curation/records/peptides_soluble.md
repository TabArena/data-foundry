---
unique_name: peptides_soluble
name: peptides_soluble
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
original_source: Other
year: '2012'
domain: biology & life sciences
problem_type: Binary Classification
source_links:
- https://doi.org/10.1111/j.1742-4658.2012.08603.x
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/peptides_soluble ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/peptides_soluble ; original: https://github.com/ur-whitelab/peptide-dashboard (ml/data/soluble.npz, insoluble.npz) ; PSI Structural Genomics Knowledgebase'
- https://arxiv.org/abs/2505.12534
- https://github.com/ur-whitelab/peptide-dashboard/tree/master/ml/data
- https://doi.org/10.1021/acs.jcim.2c01317
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: solubility on expression in E. coli of structural-genomics targets (PROSO II), a measured pipeline outcome, but a cut of a larger published set with the amino-acid sequence as the only input (SEL-12 open).
- Source: Smialowski et al., "PROSO II - a new method for protein solubility prediction", FEBS J 279:2192, online 2012-05-21, with labels from the Protein Structure Initiative's laboratory notebooks (pepcDB; Berman et al. 2009); the abstract: "our model is trained on five times more data than used by any other method before (82 000 proteins)". Insoluble: "Comparing the experimental status at two time points, September 2009 and May 2010, we were able to derive a set of insoluble proteins defined as those which were not soluble in September 2009 and still remained in that state 8 months later" (PROSO II, quoted in ChemNLP's meta). ChemPile carries the White lab's cut (peptide-dashboard `soluble.npz`, `insoluble.npz`, 2022; Ansari and White 2023, Sec. 2.1.2: "The training data contains 18,453 sequences (47.6% positives and 52.4% negatives) based on data from PROSO II"). Counted on the files (a preview): 8,785 soluble and 9,668 insoluble unique sequences, none in both, lengths 19 to 198, so only proteins under 200 residues.
- Use case: a lab or company choosing constructs for heterologous expression ("Many fields of science and industry depend on efficient production of active protein using heterologous expression in Escherichia coli ... Prediction of solubility from sequence is therefore highly valuable", PROSO II abstract). Fit direct for target and construct selection. Regime: grouped by sequence similarity (homologous targets across PSI centres); Ansari and White note that PROSO II's reported result used clustering at 90% identity.
- Siblings and duplicates: `peptides_hemolytic` and `peptides_nonfouling` (same repository and paper, other tasks, PROV-7); all 9,668 insoluble sequences here are reused as negatives of peptides_nonfouling. No other protein-solubility record (`somas_aqueous_solubility`, `aqsoldb` are small-molecule solubility). Sequence-only precedents as for peptides_hemolytic: `antigen_avida_hil6` (`No`, the curators: "NLP task / data"), `protein_location_prediction_challenge` (`No`), `african_snake_antivenom_binding_challenge` (`TBD -> 2nd Tier`, SEL-12 reject refuted). External collections: ChemPile (ChemPile-LIFT `peptides_soluble`), ChemNLP; PeptideBERT used the same set; DeepSol (Khurana et al. 2018) and later predictors train on PROSO II-derived sets.
- Better data: no new search; a candidate of the benchmark ChemPile. The PROSO II set itself (82,000 proteins, all lengths) is the first publication and larger than this cut: a version of the same source (PROV-6), so the add stage should take its fullest public copy.
- Papers and pages: PROSO II (holdout: "accuracy 75.4%, Matthew's correlation coefficient 0.39, sensitivity 0.731, specificity 0.759, gain (soluble) 2.263"); Ansari and White 2023, Table 1: Bi-LSTM AUROC 0.76 against PROSO II 0.78 and DSResSol 0.84.
- Metric: `roc_auc`, the fallback (MET-5): PROSO II reports accuracy, MCC, sensitivity, specificity and gain side by side; Ansari and White select by AUROC and accuracy. Inputs: none.
- Risks for /add-dataset: SEL-12: the input is a protein sequence; PROSO II's own classifier is logistic regression on k-mer composition (with a similarity model) and matches the RNN here, so vectorised features look competitive, but the curators' precedent leans out. The label is a pipeline status (insoluble means not soluble after 8 more months), so targets the centres dropped may count as insoluble. Whether the full PROSO II files are still public (the MIPS server) is to check. The PROSO II full text is paywalled and was not read (PROV-17).
- Priority: gap 0 (no thin value), use case + (PROSO II names protein production by heterologous expression), source + (a peer-reviewed paper on PSI data), shape 0 (18,453 rows, but one string input), risk - (the modality under SEL-12, a cut whose full version is to find).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 6,541 sequences (ChemNLP); in ChemPile-LIFT 387,513 text prompts over 1 config(s); target: soluble (1/0).
- Why: Classify whether a protein sequence expresses solubly in E. coli, the go/no-go before a production run
- Notes: PROSO II solubility data (Smialowski et al. 2012, FEBS J 279:2192), read off the Protein Structure Initiative electronic notebooks (Berman et al. 2009). Sequence-only features. No record.
