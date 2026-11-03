---
unique_name: tox21_challenge_2014
name: Tox21 Data Challenge 2014 (12 nuclear-receptor and stress-response assays)
checked_by:
- AI (UNVERIFIED)
suggestion: 'No'
decision_markers:
- Duplicate
tags:
- AI-Filled (Verify)
source_links:
- https://doi.org/10.3389/fenvs.2015.00085
- https://tripod.nih.gov/tox21/challenge/data.jsp
- https://tdcommons.ai/single_pred_tasks/tox/
- https://doi.org/10.3389/fenvs.2015.00080
- https://www.bioinf.jku.at/research/DeepTox/tox21.html
- https://huggingface.co/datasets/ml-jku/tox21
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `No` (`Duplicate`, PROV-4): the Tox21 Data Challenge 2014 release (training, leaderboard and final evaluation sets over 12 assays, https://tripod.nih.gov/tox21/challenge/data.jsp), which `tox21` already records with the same download page among its links and which the run's screening of `tox21` named as the broadest of five records of this source.
- Source: the Tox21 programme (NCATS, NIEHS/NTP, EPA, FDA), Tox21 Data Challenge 2014. The data page offers "The complete training dataset", a leaderboard set ("this dataset is only used to evaluate performance for the leaderboard") and a final evaluation set ("Results submitted for this dataset will be used to determine the final ranking of the competition"), over the nuclear receptor panel (AR, AhR, AR-LBD, ER, ER-LBD, aromatase, PPAR-gamma) and the stress response panel (ARE, ATAD5, HSE, MMP, p53). Huang et al. 2016 (Front. Environ. Sci. 3:85) describe the challenge and Mayr et al. 2016 (DeepTox, 3:80) the winning entry with 11,764 training, 296 leaderboard and 647 final compounds; the ml-jku/tox21 copy on Hugging Face holds the 12,060 training and leaderboard compounds with the 12 labels and CV folds.
- Use case: as `tox21` (a regulatory toxicologist or screening chemist decides which chemicals go to the next test); nothing distinct here.
- Siblings and duplicates: `tox21` (`TBD -> Yes`, priority 3, screened 2026-10-31; its links include https://tripod.nih.gov/tox21/challenge/data.jsp, the DeepChem csv and TDC Tox21) ends at the same release; so does `tox21_challenge` (the challenge files, from the curator's Zotero collection, unscreened); `tox21_nr_ahr` and `tox21_sr_mmp` were proposed as `Duplicate` (PROV-6) of `tox21`. This record adds the DeepTox page (bioinf.jku.at), the ml-jku Hugging Face copy and the two Front. Environ. Sci. DOIs, links to move to `tox21`. External collections: MoleculeNet/DeepChem, TDC, TabBench-Bio, ChemPile (through `tox21`).
- Better data: found as better data for `bioresponse`, in the awesome-chemistry-datasets list and in the curator's Zotero collection (items 202 and 85).
- Papers and pages: Huang et al. 2016 (10.3389/fenvs.2015.00085); Mayr et al. 2016 (10.3389/fenvs.2015.00080); the challenge data page.
- Metric: ROC AUC per assay, the challenge's ranking metric, as recorded on `tox21` (MET-4).
- Reject check (AI, 2026-10-31): stands. tox21 lists the same release page (https://tripod.nih.gov/tox21/challenge/data.jsp), the same 12 assays and the same training, leaderboard and final sets. Its Risks already say to build from the challenge files (12,060 + 296 + 647) rather than the MoleculeNet cut, so this record adds no task. Move the DeepTox page, the ml-jku Hugging Face copy and the two Front. Environ. Sci. DOIs to tox21. tox21_challenge (unscreened) is the same source too.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `bioresponse`; the awesome-chemistry-datasets list (github.com/kjappelbaum/awesome-chemistry-datasets); the curator's Zotero collection, item 202: "Measuring AI Progress in Drug Discovery: A Reproducible Leaderboard for the Tox21 ..."; the curator's Zotero collection, item 85: "Cyber risk and cybersecurity: a systematic review of data availability".
- as published: about 12,000 training compounds with 12 sparsely filled binary assay labels (MoleculeNet and TDC copy: 7,831 compounds), plus a 647-compound final evaluation set; target: active or inactive in one named Tox21 assay; access: open.
- Why: already found by the 2026-10-30 better-data scouting (scout_08, for bioresponse) and still without a record; listed here so the catalogue items (MoleculeNet, TDC) link to the same candidate | Same task kind as bioresponse: predict a binary biological response of a molecule from descriptors computed on its structure, ...
- Adds: see scout_08: named assays and public structures instead of the anonymized, scaled descriptors of bioresponse | ~12,000 compounds against 3,751, structures (SMILES/SDF) instead of 1,776 anonymized min-max-scaled descriptors D1..D1776, a named assay and a documented activity call (clears the Anonymized marker and the ...
