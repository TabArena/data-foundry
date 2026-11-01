---
unique_name: butkiewicz_pubchem_hts
name: cav3_t-type_calcium_channels_butkiewicz, choline_transporter_butkiewicz, kcnq2_potassium_channel_butkiewicz, ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: Other
year: '2013'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://doi.org/10.3390/molecules18010735
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: cav3_t-type_calcium_channels_butkiewicz, choline_transporter_butkiewicz, kcnq2_potassium_channel_butkiewicz, m1_muscarinic_receptor_agonists_butkiewicz, m1_muscarinic_receptor_antagonists_butkiewicz, orexin1_receptor_butkiewicz, potassium_ion_channel_kir2_1_butkiewicz) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/cav3_t-type_calcium_channels_butkiewicz ; original: https://tdcommons.ai/single_pred_tasks/hts/#butkiewicz-et-al ; PubChem BioAssay'
- https://arxiv.org/abs/2505.12534
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: seven PubChem HTS campaigns, 61k to 302k compounds each with confirmed actives, a real virtual-screening task at a size the benchmark has nothing like; one record per campaign is the right shape.
- Source: Butkiewicz, Lowe, Mueller, Mendenhall, Teixeira, Weaver and Meiler 2013, "Benchmarking Ligand-Based Virtual High-Throughput Screening with the PubChem Database", Molecules 18(1):735 (doi 10.3390/molecules18010735, open access): "We assemble nine data sets from realistic HTS campaigns representing major families of drug target proteins for benchmarking LB-CADD methods. Each data set is public domain through PubChem and carefully collated through confirmation screens validating active compounds" (abstract). Table 1 gives actives / inactives / hit rate: Orexin1 receptor (SAID 435008) 230 / 218,071 / 0.11%; M1 muscarinic agonists (1798) 188 / 61,661 / 0.30%; M1 antagonists (435034) 448 / 61,407 / 0.73%; Kir2.1 (1843) 172 / 301,473 / 0.06%; KCNQ2 (2258) 213 / 302,351 / 0.07%; Cav3 T-type calcium channel (463087) 703 / 100,210 / 0.70%; choline transporter (488997) 252 / 302,246 / 0.08%; plus serine/threonine kinase 33 (2689) and tyrosyl-DNA phosphodiesterase (485290), which the ChemPile cut leaves out. How the label is built: "The inactive compounds are taken from the corresponding primary assay" and the actives come from the confirmatory screens (Sec. 3.1). The authors' own download page (meilerlab.org/qsar_pubchem_benchmark_2012) is gone (404, checked 2026-10-31); TDC and ChemNLP carry the sets as SMILES with a 0/1 label.
- Use case: a screening group with a compound library, after the primary HTS run, ranks the library to decide which compounds go into the confirmatory assay: "after virtual screening only a small fraction of compounds - the ones with predicted high activity - will be considered ... (e.g., 1% or ~10^3)" (Sec. 3.6); fit direct; regime grouped on the Bemis-Murcko scaffold (SPLIT-31), since a new candidate comes from a series not yet measured.
- Siblings and duplicates: seven configs of one collection, one per protein target: distinct assays and distinct tasks, so not duplicates (PROV-7), but the record covers seven datasets and should become one record each (the main session's call). `muv_maximum_unbiased_validation`, `cyp450_inhibition_aid1851` and `tox21` are other PubChem-derived records of this run (other assays, PROV-7); MoleculeNet's PCBA is another cut of PubChem. External collections: ChemPile / ChemNLP, TDC (its HTS tasks).
- Better data: a candidate of the benchmark ChemPile; no further search this round.
- Papers and pages: Butkiewicz et al. 2013 (the collection and its protocol, Sec. 3.1); TDC's HTS page; the ChemNLP builders `data/tabular/*_butkiewicz`.
- Metric: the paper fixes one criterion: the integral of its TNR-TPR curve "was chosen as an objective function for QSAR model training" and "The integral is identical to the well-known area under the curve (AUC) value" (Sec. 2.3), with enrichment at a TPR cutoff of 25% as an additional measure (Sec. 3.6). So `roc_auc`, a deliberate choice (MET-1, MET-5), equal to the fallback; the enrichment needs a cutoff the source gives only as an example, so it is no declared metric (MET-7). Class imbalance alone is no reason for AUPRC (MET-9). Inputs none.
- Risks for /add-dataset: hit rates of 0.05% to 0.7% leave roughly 20 to 150 actives per test fold, so check scorability per fold (TP-5, TP-8) before shipping each campaign; actives come from the confirmatory screens and inactives from the primary screen, so the class also records which assay a compound passed through (LEAK-13 to LEAK-15, `Class-dependent Recording` to check); PubChem substance-to-compound mapping, salt forms and stereoisomers collapse onto the same 2D descriptors (LEAK-17, CLEAN-24); the ChemNLP meta.yaml of `choline_transporter_butkiewicz` is a stray copy of the Bicerano polymer meta, so read the transform, not the meta.
- Priority: gap 0 (chemistry & material science and binary classification are not thin), use case +, source +, shape + (61k to 302k compounds per campaign), risk - (the primary/confirmatory label construction and the handful of actives per fold).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: per config, summary AID / compounds / actives (TDC): Cav3 T-type calcium channel 463087 / 100,875 / 703; choline transporter 488997 / 302,306 / 252; KCNQ2 potassium channel 2258 / 302,405 / 213; M1 ...; target: confirmed active (1/0), one label per campaign.
- Why: Virtual screening: classify whether a library compound is a confirmed selective active in a PubChem HTS campaign (primary screen plus confirmatory and counter screens)
- Notes: Seven configs of one curated collection: Butkiewicz et al. 2013 (Molecules 18:735), nine PubChem HTS campaigns on the Molecular Libraries Small Molecule Repository; ChemPile-LIFT leaves out serine/threonine kinase 33 (AID 2689) and tyrosyl-DNA phosphodiesterase (AID 485290), which ChemNLP does carry. Primary-screen ...
