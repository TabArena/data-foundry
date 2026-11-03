---
unique_name: tox21
name: nr_ahr_tox21, nr_ar_lbd_tox21, nr_ar_tox21, nr_aromatase_tox21, nr_er_tox21, nr_ppar_gamma_tox21, sr_are_tox21, sr_atad5_tox21, sr_hse_tox21, ...
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
- Non-IID (Grouped)
collections:
- ChemPile
original_source: GOV Website
year: '2014'
domain: chemistry & material science
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.3389/fenvs.2017.00003
- 'https://huggingface.co/datasets/jablonkagroup/chempile-lift/tree/main/<config> (configs: nr_ahr_tox21, nr_ar_lbd_tox21, nr_ar_tox21, nr_aromatase_tox21, nr_er_tox21, nr_ppar_gamma_tox21, sr_are_tox21, sr_atad5_tox21, sr_hse_tox21, sr_mmp_tox21, sr_p53_tox21) ; ChemNLP builder https://github.com/OpenBioML/chemnlp/tree/main/data/tabular/nr_ahr_tox21 ; original: https://tdcommons.ai/single_pred_tasks/tox/#tox21 ; https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz ; https://tripod.nih.gov/tox21/challenge/data.jsp'
- https://arxiv.org/abs/2505.12534
- '# the challenge''s own release: training, leaderboard and final evaluation sets'
- https://tripod.nih.gov/tox21/challenge/data.jsp
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the Tox21 10K qHTS screen, a large public toxicity task with a named decision, a competition and a competition metric; the open points are which assay we ship and that four other records of this run hold the same source.
- Source: the Tox21 programme (NCATS, NIEHS/NTP, EPA, FDA) screened its Tox21 10K library by quantitative high-throughput screening and released the data for the Tox21 Data Challenge 2014 (https://tripod.nih.gov/tox21/challenge/, "Participants were to predict how compounds interfere with biochemical pathways using only chemical structure data"; "A collection of compounds independent of the Tox21 10K collection will be used as the test set"). As published for the challenge (Mayr et al., "DeepTox: Toxicity Prediction using Deep Learning", Front. Environ. Sci. 3:80, https://doi.org/10.3389/fenvs.2015.00080): a training set of 11,764 compounds, a leaderboard set of 296 and a final test set of 647 (structures only), over 12 assays — the nuclear receptor panel (NR-AhR, NR-AR, NR-AR-LBD, NR-Aromatase, NR-ER, NR-ER-LBD, NR-PPAR-gamma) and the stress response panel (SR-ARE, SR-ATAD5, SR-HSE, SR-MMP, SR-p53) — each a binary active/inactive call, sparsely filled. The MoleculeNet/DeepChem copy (`tox21.csv`) holds 7,831 compounds over the same 12 labels, and the ChemNLP per-assay tables about 6,000-8,000 labelled compounds each (`nr_ahr_tox21`: `num_points: 6549`, licence CC BY 4.0). Features as published: the SMILES only.
- Use case: a regulatory toxicologist or screening chemist decides which chemicals go on to the next (animal or confirmatory) test — the stated purpose of the Tox21 programme and of the challenge; fit approximate, since an in-vitro pathway call stands in for toxicity in vivo; regime grouped on the Bemis-Murcko scaffold, because the rows are exact structures and the programme's own test set is a compound collection independent of the training library (SPLIT-31 as amended 2026-10-26).
- Siblings and duplicates: four records of this same run end at the same source and the main session should merge them into one (PROV-4, PROV-6): `tox21_challenge` (the challenge files, from the Zotero sweep), `tox21_challenge_2014` (found as better data for `bioresponse`, with the challenge release, the DeepTox page and the ml-jku copy), `tox21_nr_ahr` and `tox21_sr_mmp` (TabBench-Bio, one assay each from `tox21.csv`). This record is the broadest cut (11 ChemPile configs, links to the challenge files, the DeepChem csv and TDC), so it is the natural survivor, with the others as `Duplicate`; the per-assay records would only be distinct tasks under PROV-7 if we ship several assays, which is a curator call. `bioresponse` (`Yes`, `Anonymized`) is the dataset the scouting proposed this one against. Precedents for a SMILES-only molecule task: `apistox`, `qsar_tid_11`, `qsar_oral_toxicity` (all `Yes`). External collections: ChemPile-LIFT (11 configs), ChemNLP, TabBench-Bio, TDC (`Tox21`), MoleculeNet/DeepChem.
- Better data: a candidate of the benchmark ChemPile; no new search this run.
- Papers and pages: the challenge release (tripod.nih.gov) and its editorial, Huang & Xia, Front. Environ. Sci. 5:3, 2017 (the record's DOI; it describes the 10K library as the training set and gives no split or metric); Huang et al., Front. Environ. Sci. 3:85, 2016 on the challenge; Mayr et al. 2016 (DeepTox, the winning entry) for the challenge's setup and metric; Huang et al. 2016 Nat Commun on the Tox21 10K profiling.
- Metric: ROC AUC, the challenge's own ranking metric: DeepTox (Front. Environ. Sci. 3:80, Results) uses "the area under the ROC curve (AUC)", which it describes as reflecting "how well a method can rank toxic compounds higher than non-toxic compounds", for the 12 subchallenges and the two panels. A competition's leaderboard metric, so deliberate (MET-4); inputs none, so it needs no extra column (MET-2). It also matches the binary fallback.
- Risks for /add-dataset: which assay (or assays) is the target — 12 labels over one compound cohort, each with its own labelled subset, and `Multi-target` only if several ship at once (CLEAN-18); the four sibling records above (PROV-4); which release to build from — the challenge files (12,060 training compounds plus the 296 and 647 evaluation sets, which the MoleculeNet cut drops) rather than the 7,831-row `tox21.csv` (PROV-8, PROV-15); the active share per assay (3-15%, so check the positives per scaffold-grouped fold, TP-5); duplicate structures and salt forms across the library, as in `qsar_oral_toxicity` (LEAK-19); one column as published, so the features come from the shared RDKit descriptor helper (`apistox` precedent).
- Priority: gap 0 (chemistry & material science, binary and grouped are not thin), use case + (the programme names the triage decision), source + (NCATS/NIEHS/EPA, a challenge and several papers), shape + (about 7,800-12,000 compounds per assay), risk - (four records of one source, and the target assay is not fixed).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark ChemPile (https://arxiv.org/abs/2505.12534).
- as published: 7,831 compounds over 12 assays in tox21.csv, 5,800-8,000 labelled per assay (ChemNLP nr_ahr_tox21: 6,549); in ChemPile-LIFT 1,453,979 text prompts over 11 config(s); target: assay activity (1/0), one label per assay.
- Why: Classify whether a chemical is active in a Tox21 in-vitro assay (nuclear receptor or stress response pathway); the programme uses these calls to triage chemicals for further testing
- Notes: 11 configs of one source: the Tox21 10K library screened by qHTS, released for the Tox21 Data Challenge 2014 (NCATS/NIEHS/EPA). ChemPile-LIFT leaves out NR-ER-LBD, which ChemNLP has. Assays: NR-AhR, NR-AR, NR-AR-LBD, NR-Aromatase, NR-ER, NR-PPAR-gamma, SR-ARE, SR-ATAD5, SR-HSE, SR-MMP, SR-p53. The challenge release ...

**Assessment (AI, 2026-10-31):** cleanup flag of the data-scouting run: one Tox21 source in five records; `tox21` is the broadest cut (`tox21_challenge`, `tox21_challenge_2014`, `tox21_nr_ahr`, `tox21_sr_mmp`; PROV-4, PROV-6). The curator keeps one, or both as distinct tasks.
