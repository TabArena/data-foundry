---
unique_name: web_page_phishing_detection
name: Web page phishing detection (Hannousse and Yahiouche)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
original_source: Other
year: '2020'
domain: technology & internet
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17632/c2gw7fy2j4.3
- https://doi.org/10.1016/j.engappai.2021.104347
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: 11,430 URLs with 87 URL, page and third-party features, exactly half phishing, from a 2021 benchmark paper; larger and newer than the shipped `website_phishing` for the same task, but the legitimate class was crawled from Alexa's top 500 domains and Yandex results, collected apart from the phishing lists.
- Source: Hannousse and Yahiouche, Mendeley Data "Web page phishing detection" (v1 2020-09-26, v3 2021-06-25, doi 10.17632/c2gw7fy2j4.3, CC BY 4.0), with "Towards benchmark datasets for machine learning based website phishing detection: An experimental study", Eng Appl Artif Intell 104:104347 (2021; arXiv 2010.12847). As published: "11430 URLs with 87 extracted features" (56 from the URL, 24 from the page content, 7 from external services: WHOIS, Alexa, Openpagerank and Google, Sec. 4.2), "exactly 50% phishing and 50% legitimate URLs", constructed May 2020; dataset_A holds the URLs with their DOM trees, dataset_B the feature table (indexed by URL), plus the extraction scripts.
- Collection (Sec. 4.1): "Legitimate web page URLs are collected from Alexa and Yandex ... the first 500 top domains provided by Alexa for free are used. Those top domains are adopted as seeds for crawling 12 URLs per domain", the rest "still active legitimate URLs provided by Sahingoz et al." (Yandex); "For phishing URLs, both lists of URLs provided by Phishtank and Openphish are used"; duplicate and dead URLs removed, at most 12 URLs per domain.
- Use case: a browser or mail filter decides when a page opens whether to warn or block (the paper weighs features by runtime cost; the actor is our reading); fit approximate: the classes come from separate lists and the legitimate sites are top-ranked domains, not the pages a filter meets (`Selection Bias`, as on `website_phishing`). Regime IID, or grouped by domain (up to 12 URLs per domain; SPLIT-29).
- Siblings and duplicates: `website_phishing` (Lennart and Andrej, `Yes`, shipped, `Selection Bias`; UCI 2016, nine coded signals); `phiusil_phishing` (Andrej, `No`, `Data Quality Issue`: classes collected in different forms, a fixed rule reaches AUC 0.9998); `phishing_websites_vrbancic` (unscreened; Mendeley 2020, 88,647 sites) and `pilwd_134k_phishing` (unscreened), both from this run; `phishing_url_websites` (Lennart, `TBD -> 2nd Tier`). Each another source, not a duplicate (PROV-4). External collections: none of our vocabulary.
- Better data: found as better data for `website_phishing`; no further search this round.
- Papers and pages: the Mendeley pages (v1, v3); the paper (arXiv text: Sec. 4.1, 4.2 and the metrics section read).
- Metric: accuracy and macro F1 side by side ("Accuracy metric works well for balanced datasets which is the case of the dataset used in this study"), no costs or threshold fixed, so the fallback `roc_auc` (MET-5, MET-6). Inputs: none.
- Risks for /add-dataset: run the PhiUSIIL check first: whether a fixed rule or the URL form alone separates the classes (LEAK-13 to LEAK-15, TP-4); legitimate URLs are seeded from Alexa's top domains while external features come from Alexa, Openpagerank and Google (a selection-driven shortcut to measure); the URL index of dataset_B to drop; the domain grouping.
- Priority: gap 0 (technology, binary not thin), use case 0 (approximate fit, actor our reading), source + (a data paper with scripts and DOM trees), shape + (11,430 x 87, numeric and binary), risk - (class-wise collection, the PhiUSIIL precedent).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `website_phishing`.
- as published: 11,430 URLs x 87 features (56 from URL structure, 24 from page content, 7 from external services), exactly 50% phishing; dataset_A also ships the URLs with their DOM trees and the extraction scripts; target: Phishing vs legitimate web page; access: open (Mendeley Data).
- Why: Same task as website_phishing: a site labelled phishing or legitimate from URL, page and third-party signals; the old record's nine signals (SFH, pop-ups, SSL, request and anchor URLs, web traffic, URL length, domain age, IP address) are features of the same kinds
- Adds: About 9x the sites (11,430 vs about 1,250 binary rows), raw feature values instead of the donors' 3-level codes, newer pages, URLs and scripts to recompute. Caveat: phishing and legitimate pages come from separate lists and are balanced by design; PhiUSIIL was rejected for this kind of class-wise collection (Data ...
