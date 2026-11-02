---
unique_name: tox21_challenge
name: Tox21 Data Challenge 2014 (NCATS/NIH)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://tripod.nih.gov/tox21/challenge/data.jsp
- https://tripod.nih.gov/tox21/challenge/
- https://doi.org/10.1039/C7SC02664A
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the Tox21 Data Challenge 2014 release (tripod.nih.gov/tox21/challenge/data.jsp), which `tox21` already records with the same data page among its links; `tox21` is the run's survivor of five records of this one source.
- Source: the Tox21 Data Challenge 2014 (NCATS/NIH with NIEHS/NTP, EPA and FDA). The data page offers the training set (`tox21_10k_data_allsdf`, and one SDF and SMILES file per assay of the nuclear receptor panel, AR, AhR, AR-LBD, ER, ER-LBD, aromatase and PPAR-gamma, and of the stress response panel, ARE, ATAD5, HSE, MMP and p53), the leaderboard set (`tox21_10k_challenge_testsmiles`: "Please note this dataset is only used to evaluate performance for the leaderboard") and the final evaluation set (`tox21_10k_challenge_scoresmiles`: "Results submitted for this dataset will be used to determine the final ranking of the competition"). The record's third link, MoleculeNet (Wu et al., Chem Sci 9:513-530, 2018, doi 10.1039/C7SC02664A), is a benchmark paper that used a 7,831-compound cut of it.
- Siblings and duplicates: `tox21` (ChemPile; `TBD -> Yes`, priority 3) lists https://tripod.nih.gov/tox21/challenge/data.jsp among its links and its screening names this record among the four to merge into it; `tox21_challenge_2014` (the same release; proposed `Duplicate`, PROV-4, in batch screen_51), `tox21_nr_ahr` and `tox21_sr_mmp` (`No`, `Duplicate`, PROV-6). The run's duplicate list: "tox21 tox21_challenge tox21_challenge_2014 tox21_nr_ahr tox21_sr_mmp one Tox21 source in five records". One original source, so a duplicate (PROV-4); the assay choice, the challenge split (training, leaderboard and final evaluation sets) and the metric are `tox21`'s open points. Should several assays ship as separate datasets (PROV-7), they are built under `tox21`.
- Better data: from the curator's Zotero collection (item 52: "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ..."); no further search this round.
- Metric: ROC AUC per assay, the challenge's ranking metric (DeepTox, Mayr et al. 2016, Results; held on `tox21`, MET-4).
- Reject check (AI, 2026-10-31): stands. The record's first link, https://tripod.nih.gov/tox21/challenge/data.jsp, is in tox21's source_links ('# the challenge's own release: training, leaderboard and final evaluation sets'), with the same 12 assays and splits, and tox21's Risks already say to build from the challenge files. The identical reject of tox21_challenge_2014 stood (rejectcheck_05). Move the challenge home page and the MoleculeNet DOI (10.1039/C7SC02664A, related work, PROV-12) to tox21.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 52: "Automatic Auxiliary Task Selection and Adaptive Weighting Boost Molecular Property ...".
- as published: compounds: about 12,000 in the challenge files (MoleculeNet subset 7,831) x 12 qHTS assay outcomes (nuclear receptor and stress response), many missing labels; target: active in one of 12 toxicity assays (e.g. SR-p53, NR-AhR); one dataset per assay or a chosen assay; access: open.
- Why: A public challenge with real high-throughput assay outcomes and a stated regulatory use; the largest of the item's classification sets.
- Adds: No record. Needs a decision on which assay(s) form the target, and a check on the official challenge split (train / leaderboard / final test).
