---
unique_name: tox21_sr_mmp
name: MoleculeNet-Tox21-SR-MMP (Tox21 Mitochondrial Membrane Potential)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
collections:
- TabBench-Bio
source_links:
- https://doi.org/10.3389/fenvs.2015.00085
- https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz
- https://arxiv.org/abs/2609.07441
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-6): one assay column (SR-MMP) of MoleculeNet's `tox21.csv.gz`, as 2,048-bit ECFP4 fingerprints; `tox21` already records this file and this assay (config `sr_mmp_tox21`), so the record is a cut of a recorded dataset with no distinct task.
- Source: the Tox21 programme's 10K library screened by qHTS (NCATS, NIEHS/NTP, EPA, FDA) and released for the Tox21 Data Challenge 2014 (tripod.nih.gov/tox21/challenge); the record's DOI is Huang et al., "Tox21Challenge to Build Predictive Models of Nuclear Receptor and Stress Response Pathways as Mediated by Exposure to Environmental Chemicals and Drugs", Front Environ Sci 3:85 (doi 10.3389/fenvs.2015.00085, online 2016-01-14). The copy is MoleculeNet/DeepChem's `tox21.csv.gz` (header previewed: the 12 assay columns NR-AR, NR-AR-LBD, NR-AhR, NR-Aromatase, NR-ER, NR-ER-LBD, NR-PPAR-gamma, SR-ARE, SR-ATAD5, SR-HSE, SR-MMP, SR-p53, then `mol_id`, `smiles`; 7,831 compounds, labels sparsely filled; TDC: "7,831 compounds on 12 different targets"). TabBench-Bio registry (github.com/not-a-feature/TabBench-Bio, src/tabbench_bio/bio/data/bio_datasets.json, read 2026-10-31), `MoleculeNet-Tox21-SR-MMP`: download `https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz`, "Measured SR-MMP activity. Pinned original Tox21 CSV; missing assay labels excluded, canonical parent structures deduplicated, conflicting parent labels dropped under the existing 1% quality limit. Stateless 2048-bit ECFP4. Scaffolds linked by identical fingerprints form indivisible groups. Shares the Tox21 cohort with NR-AhR; endpoints are not independent cohorts." Not in the paper's Table 4; in the live registry and the leaderboard snapshot of 2026-10-23. The labelled count for SR-MMP was not counted (no download beyond the header).
- Use case: as on `tox21`: a regulatory toxicologist or screening chemist decides which chemicals go on to confirmatory testing, here for disruption of the mitochondrial membrane potential; regime grouped on the Bemis-Murcko scaffold (SPLIT-31).
- Siblings and duplicates: `tox21` (ChemPile; `TBD -> Yes`, priority 3) names `sr_mmp_tox21` among its 11 configs and links the same `tox21.csv.gz`; its screening asks the main session to merge `tox21_challenge`, `tox21_challenge_2014`, `tox21_nr_ahr` and `tox21_sr_mmp` into it (PROV-4, PROV-6), and which assay ships is its open point. `tox21_nr_ahr` is the sibling cut of the same file. If the curator ships several assays as separate datasets (PROV-7), they are built from `tox21`'s source, not from this fingerprint table. External collections: TabBench-Bio (live registry, not in the paper's table), MoleculeNet, TDC (`Tox21`), ChemPile.
- Better data: a candidate of the benchmark TabBench-Bio; no further search this round.
- Papers and pages: Huang et al. 2016 (Front Environ Sci 3:85); Mayr et al. 2016, DeepTox (doi 10.3389/fenvs.2015.00080); MoleculeNet (Wu et al. 2018); the TabBench-Bio registry and leaderboard.
- Metric: the Tox21 Data Challenge ranked by ROC AUC per assay (DeepTox, Results; held on `tox21`, MET-4); TabBench-Bio scores every classification task by "Macro-F1 is the primary classification metric" (Sec. 3.5), a benchmark-wide default with no threshold fixed (MET-6), with AUROC as a re-ranking in its Appendix E. The metric decision stays with `tox21`.
- Reject check (AI, 2026-10-31): stands. Registry: download_url 'https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz', target 'SR-MMP' (https://raw.githubusercontent.com/not-a-feature/TabBench-Bio/main/src/tabbench_bio/bio/data/bio_datasets.json); `tox21` links the same file and lists sr_mmp_tox21 among its configs: a recorded assay, no distinct task. TabBench-Bio's dedup and conflict rules are a note for `tox21`'s add stage.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the benchmark TabBench-Bio (https://arxiv.org/abs/2609.07441).
- as published: not stated; tox21.csv has 7,831 compounds, fewer labelled for this assay; target: SR-MMP.
- Why: Whether a compound disrupts mitochondrial membrane potential (Tox21 SR-MMP assay) from 2048-bit ECFP4
- Notes: Not in the paper's table: in the live registry and leaderboard (snapshot 2026-10-23). Shares the compound cohort with NR-AhR.
