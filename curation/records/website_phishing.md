---
unique_name: website_phishing
name: website_phishing
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Selection Bias
original_source: UCI
year: '2016'
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://doi.org/10.24432/C5B301
notebook_path: datasets/beyond_iid/old_iid/website_phishing/website_phishing.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/website_phishing/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Only 9 features, done differently nowadays

Lennart: Unsure as this seems to be older than other datasets and am missing domain knoweldge how it is doen nowadays

Andrej: Following logic of other, more extensive phishing websites task (10.24432/C51W2X)

**Assessment (AI, 2026-10-14):** no leak in the audit's sense, but the Suspicious class (103 sites) is the donors' judgement of the same nine signals (UCI 379), not an outcome: LightGBM separates it from the rest with AUC 0.987, a depth-6 tree with 0.942. Phishy against Legitimate, from the source lists, scores 0.973 without those rows. Under the documented coding (1/0/-1 = legitimate/suspicious/phishy), 7 of the 9 features point opposite to the label (91% of Phishy sites have SFH rated legitimate), and having_IP_Address takes only 0 and 1, so the definition's renaming of the codes misleads.

CC (2026-10-14, Lennart): Binary, Phishy against Legitimate: the Suspicious class is the donors' judgement of the same signals. Raw feature codes kept.

CC (2026-10-14, Lennart): Accept `dataset_pure_feature_value` (all 167 sites with popUpWidnow = 1 are phishing): the same reversed coding as the other signals, a page property, not a leak.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Abdelhamid, Ayesh & Thabtah 2014 score 3-class accuracy; our task is binary (suspicious class dropped) and no costs are fixed.

CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: phishing sites come from the PhishTank archive and legitimate ones from Yahoo and starting-point directories, two lists collected apart (the definition's fit_reason says so), not the sites a filter meets.

## Reference

Phishing detection based Associative Classification data mining
By Neda Abdelhamid, A. Ayesh, F. Thabtah. 2014

Published in Expert systems with applications
