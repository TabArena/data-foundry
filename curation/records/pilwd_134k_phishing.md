---
unique_name: pilwd_134k_phishing
name: 'PILWD-134K: Phishing Index Login Websites Dataset'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- AI-Filled (Verify)
original_source: Website
year: '2022'
domain: technology & internet
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://gvis.unileon.es/?p=2099
- '# Sánchez-Paniagua, Fidalgo, Alegre and Alaiz-Rodríguez, Expert Systems with Applications 207:118010, 2022: the paper that published the data'
- https://doi.org/10.1016/j.eswa.2022.118010
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 134,000 balanced phishing and legitimate captures (2019-2020) whose legitimate class includes login pages, built to avoid the homepage-against-phishing artefact; but it ships raw resources (URL, HTML, screenshot, site files), not a feature table, and only on request.
- Source: GVIS group, Universidad de León (gvis.unileon.es/?p=2099); Sánchez-Paniagua, Fidalgo, Alegre and Alaiz-Rodríguez, "Phishing websites detection using a novel multipurpose dataset and web technologies features", Expert Systems with Applications 207:118010, 2022 (doi 10.1016/j.eswa.2022.118010; abstract read through OpenAlex; the full text was not opened: ScienceDirect and the university repository returned 403). As published (dataset page): "134,000 verified and balanced samples collected from August 2019 to September 2020", "six different kinds of raw resources, including URLs, HTML code, screenshots, a copy of the website files, web technologies analysis and extra metadata regarding the phishing reports"; no feature table is named. The abstract: "Since approximately three-quarters of collected phishing samples request the introduction of credentials, we decided to crawl legitimate login websites to match the phishing standpoint."
- Use case: a detector flags a page as phishing when the user opens it, also on legitimate login pages ("phishing website detection in real scenarios", abstract); fit approximate (an offline capture); regime IID, or temporal by capture date if the dates ship (to decide).
- Siblings and duplicates: `phiusil_phishing` (`No`, `Data Quality Issue`, the record this was found for), `website_phishing` (`Yes`), `phishing_websites_vrbancic` and `web_page_phishing_detection` (other sources from this run); no duplicate. External collections: none found.
- Better data: found as better data for `phiusil_phishing` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: the ESWA 2022 paper (LightGBM on 54 URL, HTML and web-technology features, "97.95% accuracy"); the GVIS dataset page.
- Metric: accuracy, the abstract's headline number, with no threshold or costs fixed (MET-6), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: the table must be built from the raw HTML, URLs and web-technology reports by re-implementing the paper's 54 features (`Needs extensive data wrangling`; SEL-12 if the HTML or the screenshots are the real inputs); access by e-mail request from an institutional account, terms not stated (a practical point, EV-4); whether the phishing captures are live pages and whether the URL form still differs by class (LEAK-13 to LEAK-15); the source of the phishing reports not read.
- Priority: gap 0 (technology and binary are not thin), use case 0 (a detector, no actor named), source + (a journal paper and the group's page), shape + (134,000 captures), risk - (no table published: the features are rebuilt from raw resources).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `phiusil_phishing`.
- as published: 134,000 verified, balanced samples; six raw resources per sample (URL, HTML, screenshot, copy of the website files, web-technology analysis, phishing-report metadata); the paper extracts 54 features ...; target: phishing or legitimate website; access: request.
- Why: Same task as phiusil_phishing; built to fix the very artefact that sank PhiUSIIL: the legitimate class holds login pages as well as homepages (index), so the classes are not separable by URL form alone
- Adds: A legitimate class collected in the same form as phishing pages, live captures with screenshots, dated collection. Needs feature extraction from the raw resources (Needs extensive data wrangling); check the phishing captures are live pages, not takedown pages
