---
unique_name: phiusil_phishing
name: PhiUSIIL Phishing URL (Website)
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: Disagreement
priority: 2
tags:
- Larger IID Data
collections:
- New (BeyondArena)
original_source: Other
year: '2024'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
- https://doi.org/10.1016/j.cose.2023.103545
v2_path: datasets/_dev/tabarena-v0pt2/phiusil_phishing/dataset.py
source_row: 2
type_adapter_id: curation-record-v1
---

## Comments

Recent dataset for phishing website detection, best I know so far (AT). Features extracted from website source code. Might also be approached with LLMs, but since the paper is recent that's not a concern. Might need to double check that the feature extraction doesn't introduce leaks

Discussion: unclear if this is grouped data or not!

**Assessment (AI, 2026-10-07):** Recommend excluding it (`Data Quality Issue`). The two classes were collected differently, and every feature family shows it. All 134,850 legitimate rows are ranked domains written as https://www.<host> with no path, a form only 627 of the 100,520 phishing URLs share (URL features alone: AUC 0.9989). The phishing pages were fetched after the URLs were listed: 50.5% of phishing rows sit on 115 shared pages, none with a password field. A fixed rule with no training reaches AUC 0.9998. Andrej's leak question: the definition drops URLSimilarityIndex, Title and the two title scores, which does not change this. Hosts repeat only among phishing rows, and a host-grouped split scores the same. The file first appeared on Mendeley Data (2023).

**Assessment (AI, 2026-10-20):** priority 2 for the review of the added dataset: gap -, use case -, source +, shape +, risk - (Issue 1: run recommends exclusion; collection artefacts separate classes (fixed rule AUC 0.9998)). Not useful: a fixed rule solves it because phishing and legitimate rows were collected differently; no version of the file is a valid task.

**Assessment (AI, 2026-10-20):** The review panel recommends `No` with `Data Quality Issue` (the curator's call). The two classes were collected in different forms (LEAK-13 to LEAK-15, Must): every legitimate row is a ranked homepage written as https://www.<host>, and 50.5% of the phishing rows sit on 115 pages shared across hosts, such as takedown and 'site not found' pages fetched after the URL was listed (LEAK-10). A fixed rule with no training reaches ROC AUC 0.9998, the URL features alone 0.9989, the page features alone 0.99994, and every split (random, by host, by registered domain) ROC AUC 1.0. Mendeley v1 and v2 hold the same file, so there is nothing to repair from; `Trivial` is not proven (TP-4). Priority 2: gap -, use case -, source +, shape +, risk - (the fit is approximate, as the negatives are ranked homepages only; the panel recommends not to ship).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: 19 columns (IsDomainIP, HasObfuscation, IsHTTPS, HasTitle, HasFavicon, Robots, IsResponsive, NoOfURLRedirect, NoOfSelfRedirect, HasDescription, HasExternalFormSubmit, HasSocialNet, HasSubmitButton, HasHiddenFields, HasPasswordField, Bank, Pay, Crypto, HasCopyrightInfo).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: the 17 yes/no features (IsDomainIP, HasObfuscation, IsHTTPS, HasTitle, HasFavicon, Robots, IsResponsive, HasDescription, HasExternalFormSubmit, HasSocialNet, HasSubmitButton, HasHiddenFields, HasPasswordField, Bank, Pay, Crypto, HasCopyrightInfo). Reverted: the counts NoOfURLRedirect and NoOfSelfRedirect.

## Reference

Prasad, A., & Chandra, S. (2023). PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning. Computers & Security, 103545. doi: https://doi.org/10.1016/j.cose.2023.103545
