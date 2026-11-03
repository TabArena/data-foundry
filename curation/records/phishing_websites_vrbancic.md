---
unique_name: phishing_websites_vrbancic
name: Phishing Websites Dataset (Datasets for phishing websites detection)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
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
- https://doi.org/10.17632/72ptz43s9v.1
- https://doi.org/10.1016/j.dib.2020.106438
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 88,647 websites x 111 URL and lookup features from a Data in Brief paper (2020), but the two classes come from separate lists (PhishTank against the Alexa ranking), the kind of collection that sank `phiusil_phishing`.
- Source: Vrbančič, Fister Jr. and Podgorelec, "Datasets for phishing websites detection", Data in Brief 33:106438, 2020 (doi 10.1016/j.dib.2020.106438; read through PMC7642806); data on Mendeley Data, doi 10.17632/72ptz43s9v.1 (2020-09-24, CC BY 4.0). As published: two CSVs with 111 features; `dataset_full` 88,647 sites (58,000 legitimate, 30,647 phishing) and `dataset_small` 58,645 (27,998 legitimate, 30,647 phishing). Features: symbol counts and lengths of the whole URL, the domain, directory, file and parameters ("96 of which are extracted from the website address itself"), and 15 from lookups (DNS response time, SPF, ASN, domain activation and expiry, resolved IPs, name servers, MX servers, TTL, TLS/SSL certificate, redirects, Google index, URL shortener) (Specifications Table, Tables 1-6).
- Use case: a browser or mail filter decides, when a link is opened, whether to warn or block (written by the curation; the paper says the data serve to train classifiers and build detection systems); fit approximate: phishing came from PhishTank ("Accessed: 2018-01-17"), legitimate sites from the "Alexa ranking website" and "community labeled and organized" lists (Section 2), collected apart (`Selection Bias`); regime IID (no collection date per row).
- Siblings and duplicates: `phiusil_phishing` (`No`, `Data Quality Issue`: every legitimate row a ranked homepage, a fixed rule reaches AUC 0.9998), `website_phishing` (`Yes`, `Selection Bias`: PhishTank against Yahoo directories), `phishing_url_websites` (`TBD -> 2nd Tier`; its OpenML 43622 is another table of 11,000 URLs x 15 parameters, not this one), `web_page_phishing_detection` and `pilwd_134k_phishing` (other sources from this run); no duplicate. External collections: none found.
- Better data: found as better data for `phishing_url_websites` and `website_phishing` (the data-scouting run of 2026-10-30/31); no further search this round.
- Papers and pages: the Data in Brief article (no classifier results; the data "could also be used as a performance benchmark"); the Mendeley page.
- Metric: none found (the data paper reports no evaluation; the Mendeley page has none), so the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: class-wise recording (LEAK-13 to LEAK-15, `Class-dependent Recording`): the Alexa ranking lists domains, so the legitimate rows may be bare hosts with empty directory, file and parameter features while PhishTank rows are full URLs; measure the URL form per class and a fixed rule first, as for `phiusil_phishing`. The lookup features describe each site when it was collected (date not stated). The variant counts disagree with the text (the full file is said to hold the small one plus the Alexa sites, yet its 58,000 legitimate rows are not 27,998 plus Alexa): check which legitimate rows each file holds.
- Priority: gap 0 (technology and binary are not thin), use case 0 (no actor named by the source), source + (a data paper with a DOI), shape + (88,647 rows, 111 features), risk - (classes collected apart; the `phiusil_phishing` artefact is likely).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `phishing_url_websites`, `website_phishing`.
- as published: Full variant 88,647 websites x 111 features (58,000 legitimate, 30,647 phishing); small variant 58,645 (27,998 legitimate); target: Phishing (1) vs legitimate (0) website; access: open (Mendeley Data).
- Why: Same task as website_phishing, with URL-based features and domain lookups of the same kinds (the Data in Brief article lists them; not read here) | Same task as phishing_url_websites: a URL classified phishing or legitimate from lexical URL features and lookups. Also proposed by scout_28 for website_phishing (same ...
- Adds: About 70x the sites (88,647 vs about 1,250 binary rows) and newer; a natural class mix in the full variant (35% phishing) rather than a balanced one. Same caveat as the Hannousse hit: the classes come from separate lists (PhiUSIIL precedent, Data Quality Issue) | A traceable source with a data paper, against a record ...
