---
unique_name: web_page_phishing_detection
name: Web page phishing detection (Hannousse and Yahiouche)
checked_by:
- AI (UNVERIFIED)
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 2
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Database Snapshot
- 'Samples: Over Time'
- 'Time: Lost'
- 'Entities: Recur'
- 'Target: Varying Delay'
- 'Features: Read Later'
original_source: Other
year: '2020'
collection_period: Jul-Aug 2020
domain: technology & internet
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.17632/c2gw7fy2j4.3
- https://doi.org/10.1016/j.engappai.2021.104347
- https://data.mendeley.com/datasets/c2gw7fy2j4/3
- https://arxiv.org/abs/2010.12847
v2_path: datasets/_dev/tabarena-v0pt2/web_page_phishing_detection/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: LEAK-10 (the status look-ups kept with a note, settled for dropping when the advocate conceded), LEAK-10 and USE-7 (the takedown pages, blanked or dropped, settled for dropping by the mediator's measurement), SPLIT-8 (the forced split's time risk, a person's question); for the curator: issues 1-4. Priority 2: gap 0, use case 0, source +, shape +, risk - (use case: named by the paper, fit approximate, two lists; risk: issues 1 and 2 are confirmed late reads, the status look-ups and the takedown pages, each with a fix the definition does not apply yet).

**Assessment (AI, 2026-11-25):** corrected from today's screening, measured by the builder and the review panel: dataset_A does not keep each URL's source for the release, only for 1,000 of the 11,430 URLs (ten pickles of 100), so the Alexa-against-Yandex comparison rests on 296 Alexa and 289 Yandex pages; the pages and look-ups were read in late July to early August 2020, not March to May (`domain_age` against known registration dates, appspot creation stamps up to 3 August 2020, the release's `external_features.py` dated 27 July 2020), so `collection_period` is now Jul-Aug 2020; the source's limit of 12 URLs per domain is not met (40 hosts hold more, en.wikipedia.org 141); `domain_age` comes from an age service, not WHOIS; dropping `nb_www` costs 0.0004 ROC AUC, not 0.004.

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: the replacement for the retired `website_phishing`; open, documented raw features with URLs, and the check left open on 2026-11-09 passes (measured today: no URL rule comes near PhiUSIIL's shortcut, best depth-2 tree on the URL 0.780 ROC AUC grouped by domain, against 0.9998), but its label is still two lists and its look-ups were read at one crawl.
- Source: Hannousse and Yahiouche, Mendeley Data "Web page phishing detection" (v3, 2021-06-25, doi 10.17632/c2gw7fy2j4.3, CC BY 4.0) and "Towards benchmark datasets for machine learning based website phishing detection: An experimental study" (arXiv 2010.12847, 2020; Eng Appl Artif Intell 104:104347, 2021). As published, measured on `dataset_B_05_2020.csv` (2026-11-09 and today): 11,430 rows x 87 features plus `url` and `status`, 5,715 phishing and 5,715 legitimate; 1 repeated URL and 174 repeated feature rows; 3,971 legitimate and 2,688 phishing registered domains, 351 phishing rows on one (duilawyeryork.com, two phishing hosts under it). Sec. 4.1: legitimate URLs crawled from "the first 500 top domains provided by Alexa" (12 per domain) and "still active legitimate URLs provided by Sahingoz et al." (Yandex, published 2019); phishing URLs from "Phishtank and Openphish"; "all duplicate and dead URLs are removed and maximum of 12 URLs with the same domain name are kept".
- Use case: a runtime detection system decides whether a visited page is phishing and warns or blocks (abstract: "checking the legitimacy of visited web pages"; Sec. 6.5 weighs each feature group by extraction time "for runtime detection systems"); fit approximate: the two classes are two lists, top-ranked sites against reported phishing, not the pages a filter meets (`Selection Bias`). Collection: `Samples: Over Time` (phishing pages change with their period, SPLIT-32), `Time: Lost` (Sec. 4.3: "rows are shuffled"; no date per row; only the phishing half could be dated through PhishTank ids, which gives no key for both classes), `Entities: Recur` (up to 12 URLs per domain), `Target: Varying Delay` (a phishing label is a report to PhishTank or OpenPhish, made after the page goes live), `Features: Read Later` (all features were read at the crawl, after the URL had been listed, by a lag the paper does not give; the Yandex URLs were collected before 2019). Period: the paper says "The collection process was elaborated on March 2020" (Sec. 4.3), the Mendeley page "Datasets are constructed on May 2020" and the file is named 05_2020, so March to May 2020. Type `Database Snapshot` (one scrape, dates dropped; as `website_phishing`).
- Split: leaf [L-FORCED.groups] Grouped · `ForcedGroupedFromTemporal` because [DB.meets] new pages that arrive one by one → [ORDER.order] no (one crawl, rows shuffled) → [FORCED.test] nothing measurable (one period) → [FORCED.reason] no reason given → [FORCED.risk] the agent answers no → [FORCED.groups] yes: the registered domain (tldextract, public suffixes without private domains) is the unit a filter meets new, and grouping by it cost 0.006 ROC AUC with all features (LightGBM 0.995 random, 0.989 grouped, measured today). This corrects the 2026-11-25 issue's note, which named `ForcedIIDFromTemporal` beside a grouped split; a grouped forced split is `ForcedGroupedFromTemporal`. Open for a person: [FORCED.risk], since phishers adapt to filters, so a shift the data cannot show is likely; and whether hosting platforms (drive.google.com, sites.google.com, 39 and 37 phishing rows) group by the platform or by the host.
- Look-ups and prediction time: seven external features (Sec. 4.2, Table 4): `whois_registered_domain` and `domain_registration_length` (WHOIS), `domain_age` (WHOIS), `web_traffic` (Alexa), `dns_record` (DNS), `google_index` (Google; 1 = not indexed), `page_rank` (Openpagerank). A filter can query all seven when the page opens (Sec. 6.5: about 4 to 5 s in all, f81 and f82 in one WHOIS call), so they are known at prediction time in kind; their values are as of the crawl, not the moment a user first met the page. Direction: `domain_age` read later makes phishing domains look older (against the label); `google_index`, `page_rank` and `web_traffic` may reflect the time after the report (a reported page delisted or taken down; dead URLs were removed, so only pages still live at the crawl remain). For the Alexa half of the legitimate class, `web_traffic` and `page_rank` are close to the ranking that selected the rows (top 500 domains). Measured (grouped, LightGBM): look-ups alone 0.946, URL + content without them 0.974, all 0.989; best single features `google_index` 0.865, `page_rank` 0.812, `web_traffic` 0.691, `domain_age` 0.679.
- Siblings and duplicates: `website_phishing` (`Yes`, shipped; retirement agreed by Andrej 2026-11-09 for a codebook the data contradicts); `phiusil_phishing` (`No`, `Data Quality Issue`: a fixed rule scores 0.9998); `phishing_websites_vrbancic` (`TBD -> 2nd Tier`; path length alone 0.941, 81% of legitimate rows bare Alexa domains, measured 11-09); `phishing_url_websites` (UCI 327, `TBD -> 2nd Tier`; 30 coded signals, no URLs, 47% repeated rows, measured 11-09); `pilwd_134k_phishing` (`TBD -> 2nd Tier`, request-only raw captures); `website_phishing_duplicate`. Each another source (PROV-4), no duplicate. External collections: none of our vocabulary.
- Better data: found as better data for `website_phishing`. Nothing better than this one today (searched 2026-11-25 for the issue): PhreshPhish (Dalton et al. 2025, 666,315 dated pages, Jul 2024 to Dec 2025, CC BY 4.0) ships URL and HTML only, no feature table; CompPhish (Mendeley 10.17632/fmbs4kp9wz.4, 15,358 rows, Sep 2024 to Aug 2025) takes its legitimate side from a top-1000 list, the homepage design behind PhiUSIIL's artefact (not checked); PILWD-134K is request-only.
- Papers and pages: the Mendeley page (v3); the arXiv text (Sec. 4.1 to 4.3, 5, 6.5 and 7 read); best reported Random Forest 96.61% accuracy on all 87 features (96.83% with 73 chi-square-selected features), 10-fold cross-validation in Weka with default parameters.
- Metric: Sec. 5: "we use two main metrics": accuracy ("Accuracy metric works well for balanced datasets which is the case of the dataset used in this study") and macro F1, both reported for every model; no threshold, costs or decision fixed (Weka defaults). Two metrics side by side and an accuracy that is a habit, so the fallback `roc_auc` (MET-5, MET-6); inputs none. ROC AUC sits near 0.99 on all features, so the add stage weighs `log_loss` (MET-2).
- Risks for /add-dataset: the as-of reading of the seven look-ups above (LEAK-10), and `web_traffic` and `page_rank` against the Alexa selection: dataset_A keeps each URL's source (Alexa, Yandex, PhishTank, OpenPhish), so the legitimate rows can be split by list and the look-ups compared; `nb_www` (0.72 alone; `www.` in 67% of legitimate against 21% of phishing URLs) is a form difference of the two lists, dropping it changes grouped LightGBM by 0.004 (measured today); derive the registered domain from `url`, then drop `url` (LEAK-13 to LEAK-15 checked today on the URL features: no shortcut).
- Priority: gap 0 (technology & internet 7 accepted, binary and grouped not thin; it would keep the benchmark's only phishing task after `website_phishing` retires), use case 0 (named by the paper, fit approximate), source + (paper, scripts, URLs and DOM trees), shape + (11,430 x 87, URL, content and look-up features, grouped by domain), risk 0 (the class-form shortcut the old screening took a point for is measured away; the look-up timing is a check, not a likely leak).
- Corrected from the 2026-10-31 screening: priority 2 to 3 (the form-shortcut risk is measured, not open); regime "IID, or grouped by domain" to a forced split grouped by registered domain (`Samples: Over Time`, `Time: Lost`); the paper dates the collection to March 2020, the data page to May 2020; the paper's metrics are its "two main metrics", accuracy and macro F1; `collection_period` and the collection tags set, the arXiv text added to the links.

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

## Review

**Outcome:** added; the AI recommends shipping it after the changes of issues 1 and 2. 11,430 web pages of Hannousse and Yahiouche's Mendeley release (dataset B), half phishing from the PhishTank and OpenPhish lists, half legitimate from Alexa's top 500 domains and an older Yandex list; 81 features read off the URL, the page's HTML and seven look-ups (WHOIS, domain age, Alexa rank, DNS, Google index, Open PageRank); target `is_phishing`, ROC AUC as the fallback, since the paper reports accuracy and macro F1 side by side. Split: a forced split grouped by registered domain (6,634 domains, 3 repeats of 3 folds), since the release keeps no date. Validity: no URL or format shortcut (best fixed URL rule 0.78, format-only model 0.899 reads page content), no exploit beyond noise, and no look-up tells the two legitimate lists apart (ROC AUC 0.50 to 0.52); but the pages and look-ups were read in late July to early August 2020, after the phishing reports, on the phishing pages whose state can be traced the status look-ups move with that state, and 12 to 16% of the phishing pages of dataset A were crawled as takedown pages. Value: real signal, near the ceiling (untuned 0.981 to 0.989 ROC AUC with all features, 0.982 under issue 1's fix), and the benchmark's only phishing task once `website_phishing` retires. Applied without a decision: the collection dates, the group sizes, the meanings of the look-up codes and feature names, shares over an empty set as missing values, the number-format test and the takedown and hosting-platform pages in the notes, and the operating point in the metric reason. `dataset check`: 0 errors, 3 warnings (proposed for acceptance, not accepted).

**Main points:** Drop the five status look-ups and `statistical_report` (issue 1), drop the 493 takedown pages (issue 2), accept the untested time risk of the forced split (issue 3), keep grouping hosting platforms by registered domain (issue 4); the verdict also answers option B of `website_phishing`'s replacement item, still open.

**Record judgment:** the panel's judgment record (mediator):

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (approximate fit; USE-8 Selection Bias with no shortcut between the lists, 0.50-0.52);
  USE-7 triggered: drop the takedown rows located by fingerprint (493 rows), because blanking them fails (measured);
  LEAK-10 triggered twice:
    (1) status look-ups read after the report, with a gain on the traced phishing side -> drop google_index,
        page_rank, web_traffic, dns_record, whois_registered_domain, and statistical_report with them;
    (2) takedown pages, handled by the USE-7 drop above;
  LEAK-11 keeps domain_age (a late read weakens it; missingness does not rise on takedown rows: 0.11 against 0.20 live);
  LEAK-13 to LEAK-15 hold (format-only model 0.899 reflects page content; ratios are exact k/n in both classes);
  SPLIT-36 holds (L-FORCED.groups, 0 shared domains, hidden groups +0.0001);
  SPLIT-8 [FORCED.risk] open, for a person.
  PROV/description: dates and group sizes wrong -> text fixed.
Value: TP-2, real signal under the look-up fix (ROC AUC 0.982; 0.73 of phish caught at 1% FPR; untuned models still spread);
  MET-5/6 fallback roc_auc holds.
Quality: CLEAN-10/11 fixes applied (empty-set ratios, ratio_extRedirection > 1, code meanings).
Weighed: only phishing task in the benchmark +; selection gap and same-weeks test -; fixes cost 0.008 ROC AUC.
For the curator: issues 1-4 (the look-ups, the takedown rows, the forced-split risk, the hosting-platform groups);
  the replacement of website_phishing is that record's item.
```

**Issues for Andrej:**

1. **Drop the status look-ups that were read after the phishing report?**

   - **Problem:**
     - On the phishing pages whose state can be traced, the look-ups move with that state: `page_rank` is 0 on 59% of the pages crawled after their takedown against 29% of the live ones, and `google_index` is 1 on 0.98 against 0.88.
     - The gap holds among pages on their own domain (`page_rank` 0 on 0.56 against 0.41), so cheap hosting does not explain it, and no row is dated, so the late values cannot be located row by row.
     - The definition keeps all seven look-ups with a note, which the rule allows only when the part that can be traced shows no gain[^l10].
   - **Background:**
     - The release queried seven look-ups once at the crawl, in late July to early August 2020 (dated from `domain_age` against known registration dates), after each phishing URL had been listed by PhishTank or OpenPhish, by a lag the release does not give.
     - A report sets off de-indexing, delisting and suspension, which reach `google_index`, `page_rank`, `web_traffic`, `dns_record` and `whois_registered_domain`; `statistical_report` code 2 is a failed DNS resolution read at the same look-up (278 phishing, 28 legitimate pages).
     - The trace in the notes (Alexa against Yandex pages, 0.50 to 0.52) tests only the legitimate side, where no report acts; the trace above is the phishing side of dataset A (415 pages whose HTML ships).
   - **Effect on the task:** a model learns part of what a page looks like after its report (unindexed, unranked, its DNS gone), which a filter does not see when a user first opens a fresh phishing page, so the score overstates the task.
   - **Experiments:** the phishing pages of dataset A by page state (takedown and blank pages located from their HTML):

     | Phishing pages in dataset A | Pages | `page_rank` = 0 | `google_index` = 1 |
     |---|---|---|---|
     | live | 277 | 29% | 0.88 |
     | taken down | 64 | 59% | 0.98 |
     | blank | 74 | 57% | 0.97 |
     | own domain, live | 170 | 41% | 0.84 |
     | own domain, taken down | 55 | 56% | 0.98 |
     | own domain, blank | 64 | 61% | 0.98 |

     The cost of each option, untuned LightGBM on the shipped 3 × 3 splits (C from the builder's 5 folds × 3 seeds, grouped):

     | Features | Columns | ROC AUC | Phishing caught at 1% false alarms |
     |---|---|---|---|
     | all (A) | 81 | 0.9898 | 0.846 |
     | without the five status look-ups | 76 | 0.9817 | 0.739 |
     | without them and `statistical_report` (B) | 75 | 0.9816 | 0.740 |
     | without the seven look-ups (C) | 74 | 0.9757 on the builder's folds, where all features score 0.9905 | not measured |
     | without `google_index`, `page_rank`, `web_traffic` (D) | 78 | 0.9824 on the builder's folds, where all features score 0.9905 | not measured |

   - **Consistency:**
     - distribution_transformers_at_cauca_department (Lennart, 2026-10-21) dropped attributes looked up after the outcome changed for an unknown subset of positive cases; tunisian_fraud_detection_challenge (Lennart, 2026-11-05) dropped `CTR_CESSAT`, a status that records a later event.
     - onlinenewspopularity (Lennart, 2026-10-26) kept a late read with a note only because the traced cells showed no gain (masking them moved R² by 0.0004).
     - `domain_age` read later makes a phishing domain look older, against the label, and stays with a note, as in south_africa_coronary_heart_disease[^l11].
   - **Panel:** the advocate first argued a lag of about one day, measured on 18 appspot URLs, and withdrew it in the rebuttal: on a shared host the report cannot move the domain's look-ups, and the takedown pages show the report had already acted. Advocate, critic and mediator agree on B; the critic adds that keeping the look-ups would depart from a Must and need an amendment of the rule, not an exception.
   - **Unknown:** the lag between each report and the crawl (no PhishTank ids or dates ship).
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all seven (implemented) | The look-ups stay with the note "Potential leak, kept on purpose" | keeps 0.008 ROC AUC and 0.11 of the phishing caught at 1% false alarms; keeps the paper's external feature group | the traced phishing side shows the gain that the note's condition excludes; departs from distribution_transformers and `CTR_CESSAT`; needs an amendment of the rule |
     | B | Drop the status look-ups | Drop `google_index`, `page_rank`, `web_traffic`, `dns_record`, `whois_registered_domain` and `statistical_report`; keep `domain_age` and `domain_registration_length` with a note | removes every look-up a report can move, and `statistical_report`'s failed DNS read with them (as a missing value it would stay a flag); follows both precedents | ROC AUC 0.9898 to 0.9816; phishing caught at 1% false alarms 0.846 to 0.740; `statistical_report`'s list match (code 1) goes too, worth 0.0001 |
     | C | Drop all seven look-ups | As B, and `domain_age` and `domain_registration_length` go too | simplest; no look-up left to explain | `domain_age` goes although a late read weakens its signal; ROC AUC about 0.976 |
     | D | Drop three | Drop `google_index`, `page_rank` and `web_traffic` only (the builder's draft) | the three strongest look-ups go; ROC AUC about 0.982 | `dns_record` and `whois_registered_domain` change with a suspension in the same way and stay; `statistical_report` code 2 stays |

   - **Recommendation:** B. The trace of the phishing side shows the look-ups moving with the page's state, also within one hosting type, so the condition for keeping them with a note fails; B drops every look-up a report can move and keeps the two whose late read can only weaken the signal. The task stays real (ROC AUC 0.982, 0.74 of the phishing caught at 1% false alarms, models still spread). **Decision:** drop the five status look-ups and `statistical_report` (B), keep them (A), or drop all seven look-ups (C) or only three (D)?

   **Notes for the AI:** B: add a module constant `LATE_LOOKUPS = ["google_index", "page_rank", "web_traffic", "dns_record", "whois_registered_domain", "statistical_report"]` with a docstring (read at the crawl, after the report), drop it in `_clean` with the URL and the constant columns, and remove `web_traffic` from `LOOKUP_MISSING` and the decision table. Rewrite the "Potential leak, kept on purpose" note into a dropped-columns bullet with the trace above, a LEAK-11 note on `domain_age` (read later, makes phishing domains look older) and `domain_registration_length`, and update `known` (two look-ups left), `changes` and `fit_reason`; the "Codes that stay" bullet keeps only what is left. The metric reason's operating point becomes about 0.73 to 0.74 under B. Re-run `dataset check` and the leak and task probes; the feature count becomes 75. Record: a CC line; no marker changes.

   [^l10]: **LEAK-10** (Must), the second of its three clauses, each a case-by-case judgment of the curator (amended 2026-10-26 and 2026-11-08, Lennart): "A value read at a later pull goes where its late cells can be located: they are blanked (zillow_prize, melbourne_housing_market, aeolus_1m's weather after departure); where they cannot be located row by row, the values go when they may carry a gain (distribution_transformers_at_cauca_department) and stay with a note only when the part that can be traced shows none (onlinenewspopularity's keyword and self-reference counts, 'go with (a)')."
   [^l11]: **LEAK-11** (Should; narrows LEAK-10): "A value measured after the outcome that weakens the signal stays, with a note."

2. **Drop the 493 pages that were crawled after their takedown?**

   - **Problem:**
     - The crawler kept any page served with status 200, so 65 of the 415 phishing pages of dataset A (15.7%) are takedown pages (a suspended account, a parking or warning page, an error served as 200) and 74 more are blank, against 6 and 30 of the 585 legitimate pages.
     - The takedown templates leave fixed patterns in the content features, which locate 493 rows of the shipped table: 482 phishing and 11 legitimate.
     - Blanking the located cells, the usual remedy for late cells[^l10b], would leave a missing-content flag that is 97.8% phishing and makes those rows easier to call, not harder.
   - **Effect on the task:** the model learns what a taken-down page looks like, which no filter meets when a user opens a live phishing page; the score moves little, but the rows are not instances of the task.
   - **Experiments:** the shipped 3 × 3 splits, LightGBM on B's features of issue 1 (the mediator):

     | Variant | ROC AUC, all test rows | ROC AUC, live rows only | Phishing caught at 1% false alarms (live rows) | Mean score on takedown phishing |
     |---|---|---|---|---|
     | as is | 0.9816 | 0.9807 | 0.733 | 0.957 |
     | takedown rows blanked | 0.9820 | 0.9809 | 0.733 | 0.990 |
     | takedown rows dropped | – | 0.9805 | 0.731 | – |

     How well each kind of phishing page is told from the legitimate pages, ROC AUC of grouped LightGBM, 5 folds × 3 seeds (the column auditor, builder's folds):

     | Features | Live phishing against legitimate | Takedown phishing against legitimate |
     |---|---|---|
     | all 81 | 0.988 | 0.996 to 0.998 |
     | content only | 0.887 | 0.965 to 0.979 |

   - **Consistency:** zillow_prize and melbourne_housing_market (Lennart, 2026-10-21) blanked late cells that could be located; here the located cells sit on one class, so blanking would leave missingness that encodes the outcome, which the same rule excludes[^l10b]. Dropping rows that are no instance of the task follows the rule on rows outside the use case[^u7].
   - **Panel:** the critic proposed blanking and the advocate dropping; the mediator's experiment above settled it for dropping, and both sides then agree.
   - **Unknown:** the blank pages (74 of 415 phishing pages in dataset A) cannot be told from a live page without links, and dataset A holds only 1,000 of the 11,430 pages, so the share outside it is estimated, not counted.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the rows (implemented) | The takedown and blank pages stay, named in the "Potential leak" note and `fit_reason` | no fingerprint list to maintain; all 11,430 rows | the model learns takedown pages as phishing; the takedown phishing pages score 0.957 on average |
     | B | Blank the content features | Set the page features to missing on the 493 rows | keeps the rows and their URL features | the missing-content flag is 97.8% phishing; the takedown pages get easier (0.957 to 0.990) |
     | C | Drop the rows | Drop the 493 rows located by fingerprint, after a hand check of the 11 legitimate matches; the blank pages stay with the note | removes the shortcut; costs nothing measurable on the live rows (0.9807 to 0.9805) | 4.3% of the rows go; a fingerprint list in the definition; the blank pages stay |

   - **Recommendation:** C. The takedown pages are not pages a filter rates, the fingerprints locate them (482 of the 493 are phishing), and dropping them is the only remedy that removes the shortcut without adding another. The 11 legitimate matches are read by hand first, and a match that is a live minimal page stays. **Decision:** drop the 493 takedown pages (C), keep them (A), or blank their content features (B)?

   **Notes for the AI:** C: the fingerprints are the content-feature tuples of the takedown templates found in dataset A's HTML (read with an inert unpickler, no code from the files run): "Account Suspended" (238 rows in dataset B, 237 phishing), the ChangeIP host default page (59, all phishing), the rebrand.ly warning, the phishing-education landing page, parking pages and 404 or 500 pages served with status 200; together 493 rows (482 phishing, 11 legitimate). Rebuild them from dataset A, put them in a module constant with a docstring, and drop the matching rows in `_clean` with a guard on the count (`assert` 493 before the hand check's removals); a `Decision` table gives the matches by template and class. Check the 11 legitimate matches by reading their pages in dataset A where they are there, else by their URL. Extend the note with the drop and keep the blank pages under "Potential leak". Re-run `dataset check`, the leak and task probes and the duplicate counts (some takedown rows are exact copies).

   [^l10b]: **LEAK-10** (Must): late cells of a later pull that can be located are blanked; among what the rule keeps out is "missingness that encodes the outcome".
   [^u7]: **USE-7** (Must): "A row that lacks the input the prediction acts on is no task row: drop it rather than keep it as missing." A takedown page lacks the page a filter rates.

3. **Accept that the forced split cannot test the step forward in time?**

   - **Problem:**
     - Training and test pages come from the same weeks of one crawl, while phishing kits and lures adapt to filters within weeks, so the ROC AUC likely overstates what a deployed filter scores later.
     - The release shuffled the rows and keeps no date, PhishTank id or crawl date per page, so the shift cannot be measured and no split by time can be built.
     - Only a person can accept this risk; the definition ships the forced grouped split as if it were accepted[^s8].
   - **Background:** the split tree ends at a grouped split forced in place of a split by time, as the definition names it: new pages arrive one by one, but their order cannot be rebuilt (the row order carries no signal), nothing is dated, and the registered domain is the unit a filter meets new.
   - **Effect on the task:** the test stands for new sites from the same weeks, not for the next weeks' phishing.
   - **Experiments:**

     | Split | ROC AUC (LightGBM) |
     |---|---|
     | random rows | 0.9950 |
     | shipped, grouped by registered domain | 0.9899 |
     | coarser groups (hidden campaigns and name variants merged) | 0.9903 |

   - **Consistency:** for `website_phishing`, the same task in the same adversarial domain, Andrej kept the forced tag on 2026-11-18 and did not decline the risk; no fact sets this dataset apart.
   - **Panel:** the split auditor, the advocate and the critic agree the risk is real and cannot be measured; the advocate and the mediator recommend accepting it with the tag, the critic asks only that it be asked.
   - **Unknown:** how much the score falls on later pages; a dated release (PhishTank ids and crawl dates) or a feature table built from PhreshPhish (dated pages, 2024 to 2025) would tell.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Accept the risk (implemented) | Keep the forced grouped split, tagged, with the risk named in `time_basis` and `fit_reason` | follows `website_phishing`; keeps the benchmark's only phishing task; no better split exists | the score likely overstates a later filter's, by an unknown amount |
     | B | Decline it | Retire the dataset as `Not Representative` | no score that the deployment period might not reach | departs from `website_phishing` with no fact that sets this case apart; the benchmark loses its phishing task |

   - **Recommendation:** A, as for `website_phishing`: the risk is named, cannot be measured or removed with this release, and the grouping by domain already removes the optimism that can be measured (0.995 to 0.990). **Decision:** accept the untested time risk (A), or decline it (B)?

   **Notes for the AI:** A needs no change to the definition; record the acceptance in a CC line and in the record's review. B: set the record's verdict to `No` with the marker `Not Representative` and a CC line; the folder stays until the curator asks to remove it.

   [^s8]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the closest regime that keeps the rows, tagged as forced from temporal. **SPLIT-32** and **SPLIT-36** (Should): the split tree's risk question for a forced split is a person's to answer; the agent answers no.

4. **Keep hosting platforms as one group each?**

   - **Problem:**
     - The groups are registered domains under the public suffixes only, so a hosting platform is one group: blogspot.com (383 pages), appspot.com (265) and google.com (151, with drive.google.com and sites.google.com).
     - A filter meets a new page on such a platform with other pages of the platform already known, so grouping by the host or by the private suffixes is a little closer to deployment.
     - No past case decides how hosting platforms group.
   - **Effect on the task:** small either way: the measured difference between the three groupings is under 0.003 ROC AUC.
   - **Experiments:** grouped LightGBM, 5 folds × 3 seeds (builder):

     | Grouping | Groups | ROC AUC, all features | ROC AUC, look-ups only |
     |---|---|---|---|
     | registered domain, public suffixes (A) | 6,634 | 0.9905 | 0.947 |
     | host (B) | 8,241 | 0.9928 | 0.970 |
     | registered domain with the private suffixes (C) | 7,260 | 0.9912 | 0.957 |

   - **Consistency:** the release's own extraction sends this registered domain (public suffixes) to WHOIS, Open PageRank and the DNS, so A keeps every page with the same domain look-ups on one side[^g24].
   - **Panel:** the split auditor would keep A, the more cautious choice, and notes that C is slightly closer to deployment; no one disputes it.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Registered domain, public suffixes (implemented) | blogspot.com, appspot.com and google.com are one group each | matches the domain the look-ups were read for; one phishing campaign of 351 pages stays together | a platform's pages never appear on both sides, though a filter meets them so |
     | B | Host | each subdomain is its own group | closest to "a new page on a known platform" | the same domain look-ups land on both sides; ROC AUC 0.0023 higher, part of it from the shared look-ups (look-ups only 0.970 against 0.947) |
     | C | Registered domain with the private suffixes | x.blogspot.com is its own group, other domains as A | a middle way | blogspot's WHOIS and age are still shared across sides; no precedent either |

   - **Recommendation:** A. It keeps the look-ups of one domain on one side and costs at most 0.0023 ROC AUC against the alternatives; if issue 1 drops the status look-ups, `domain_age` and `domain_registration_length` are still read for this domain. **Decision:** keep the registered domain (A), or group by host (B) or with the private suffixes (C)?

   **Notes for the AI:** B or C: regenerate `registered_domains.csv` (host to group) with tldextract 5.4.0 (`include_psl_private_domains=True` for C; the host itself for B), update the `REGISTERED_DOMAINS` docstring, `grouping.definition`, the group bullet of the notes and the decision table, and re-run `dataset check`, the group and hidden-group probes.

   [^g24]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the rows differ, so group. **SPLIT-24** (Must): group on a true group id or one constructed from the data.

**Review panel:** ship after changes (mediator). Full tier: claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent checker, advocate and critic with one rebuttal each, mediator. Claim audit: 17 claims, 12 hold, 4 refuted (the takedown pages, the group sizes, two code meanings; the text is fixed, the takedown pages are issue 2), 1 untested (the lag after each report). Blind review: include with changes; main concerns the popular legitimate class and the ceiling. Task gamer: nothing beyond noise. Debate: agreed on the text and cleaning fixes, the split, the metric and, after the mediator's experiment, dropping the takedown rows (issue 2); disputed: keeping the look-ups with a note, settled for dropping when the advocate conceded (issue 1); the time risk is left for a person (issue 3).

<details><summary>Mediator</summary>

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (approximate fit; USE-8 Selection Bias with no shortcut between the lists, 0.50–0.52);
  USE-7 triggered: drop the takedown rows located by fingerprint (493 rows), because blanking them fails (measured);
  LEAK-10 triggered twice:
    (1) status look-ups read after the report, with a gain on the traced phishing side → drop google_index,
        page_rank, web_traffic, dns_record, whois_registered_domain, and statistical_report with them;
    (2) takedown pages, handled by the USE-7 drop above;
  LEAK-11 keeps domain_age (a late read weakens it; missingness does not rise on takedown rows: 0.11 against 0.20 live);
  LEAK-13 to LEAK-15 hold (format-only model 0.899 reflects page content; ratios are exact k/n in both classes);
  SPLIT-36 holds (L-FORCED.groups, 0 shared domains, hidden groups +0.0001);
  SPLIT-8 [FORCED.risk] open, for a person.
  PROV/description: dates and group sizes wrong → fix the text.
Value: TP-2, real signal under option b (ROC AUC 0.982; 0.73 of phish caught at 1% FPR; untuned models still spread);
  MET-5/6 fallback roc_auc holds.
Quality: CLEAN-10/11 fixes, cheap and safe (empty-set ratios, ratio_extRedirection > 1, code meanings).
Weighed: only phishing task in the benchmark +; selection gap and same-weeks test −; fixes cost 0.008 ROC AUC.
For the curator: issues 1–4 below (the replacement decision, the look-ups under LEAK-10's case-by-case clause,
  the takedown rows, the forced-split risk).
```

**The decisive experiment: blank or drop the takedown rows**

The critic proposed blanking the content features on the 493 fingerprinted rows. The advocate's rebuttal argued that blanking makes missingness a label proxy. The setup: shipped 3×3 splits, option-b features without `statistical_report`, LightGBM.

| Variant | ROC AUC, all test rows | ROC AUC, live rows only | Phish caught at 1% FPR (live rows) | Mean p on takedown phish |
|---|---|---|---|---|
| as is | 0.9816 | 0.9807 | 0.733 | 0.957 |
| takedown rows blanked | 0.9820 | 0.9809 | 0.733 | **0.990** |
| takedown rows dropped | – | 0.9805 | 0.731 | – |

- The "content missing" flag would be 97.8% phishing. Blanking makes those rows easier to call (0.957 → 0.990), so it sharpens the shortcut instead of removing it. LEAK-10 lists "missingness that encodes the outcome" as out.
- The advocate's remedy wins: drop the rows the fingerprints locate. On the rows a filter actually meets, it costs nothing measurable (0.9807 → 0.9805).
- The drop must go by fingerprint, not by label. The 11 legitimate matches are checked by hand first; any that is a real takedown page goes too.

**Changes to make now (no decision needed)**

1. **Dates** (P5; USE-8 fit text). The look-ups ran in late July to early August 2020, not March to May. Fix `row`, `curation_comments`, `time_basis` and the record's `collection_period`. The same error is in `website_phishing`'s decision item ("May 2020 crawl").
2. **Group sizes** (P5). "At most 12 per domain" is false: 40 hosts hold more (en.wikipedia.org 141). Fix `row` and `grouping.definition`.
3. **Code meanings** (CLEAN-10, note):
   - `page_rank` 0 also means "unranked";
   - `dns_record`, `google_index` and `whois_registered_domain` record a failed query as 1;
   - `domain_age` comes from the payapi age service, not WHOIS;
   - `domain_registration_length` is an absolute value, so an expired domain reads positive;
   - `ip` and `nb_subdomains` do not measure what their names say;
   - the crawler can fall back to the homepage.
4. **`nb_www` cost** (fact). Dropping it costs 0.0004 ROC AUC, not 0.004.
5. **Empty-set ratios to missing** (CLEAN-10; precedent medical_facility_operational_data):
   - hyperlink shares where `nb_hyperlinks == 0` (1,381 rows);
   - media shares where both are 0 (3,874 rows);
   - `ratio_extRedirection` > 1 to missing (CLEAN-11, 50 rows).
   - This adds no new signal: `nb_hyperlinks` already carries it.
6. **Format check in the notes** (LEAK-13 to LEAK-15). Record the k/n test (5,715/5,715 and 5,711/5,715 rows) that sets this case apart from polish_companies_bankruptcy.
7. **`fit_reason` and the notes:**
   - name the 833 hosting-platform pages (ROC AUC about 0.90 there, the hard negatives);
   - extend the "Potential leak" note to the blank pages, which cannot be located (74 of 415 phishing pages in dataset A against 30 of 585 legitimate).
8. **Metric reason** (MET). Add that the real decision runs below 1% false alarms. Untuned models catch 0.71 to 0.82 of phish there with all features, and about 0.73 under option b.

**Issues for the curator, ranked**

**1. The replacement decision is unanswered** (Precedence: who decides). The record is at `TBD -> Yes` with no CC line, and option B of `website_phishing`'s decision item is open. The build is ahead of the decision.
- **Agreed by all:** answer it before shipping.
- **Decision needed:** confirm this dataset replaces `website_phishing`.

**2. The status look-ups** (P4, LEAK-10 second clause, Must; recommendation: option b).
- **Problem:** the look-ups were read after each page was reported, and no row is dated.
- **Effect:** on the traced phishing side they move with the page's state.
  - `page_rank` = 0: 59% on taken-down pages against 29% on live ones.
  - `google_index` = 1: 0.98 against 0.88.
  - The gap holds within hosting type (own domain: `page_rank` = 0 at 0.56 against 0.41). Cheap hosting does not explain it.
- **Each side's evidence:**
  - Advocate, first brief: a one-day lag measured on 18 appspot URLs. The advocate withdrew this in the rebuttal: on a shared host the mechanism cannot act.
  - Critic: the traced part shows a gain, and the case matches distribution_transformers_at_cauca_department and `CTR_CESSAT`.
- **Settled by the rule:** keeping the look-ups with a note requires that the traced part shows no gain. It shows one.
- **Remedy:**
  - drop `google_index`, `page_rank`, `web_traffic`, `dns_record` and `whois_registered_domain`;
  - drop `statistical_report` too. Its code 2 is the same failed DNS read, and setting it to missing would keep it as a missingness flag (LEAK-10). Its 0/1 list flag adds nothing: 0.9817 → 0.9816;
  - keep `domain_age` (LEAK-11) and `domain_registration_length`, each with a note.
- **Cost:** ROC AUC 0.9898 → 0.9816; phish caught at 1% FPR 0.846 → 0.740.
- **Decision needed:** LEAK-10 makes this clause the curator's case-by-case judgment. Confirm option b. Keeping the look-ups would be a departure from a Must and needs a LEAK-10 amendment, not an exception.

**3. The takedown pages** (P4, LEAK-10 located cells; USE-7; recommendation: drop the rows).
- **Problem:** 12–16% of phishing pages in dataset A were crawled as takedown or error pages, against about 1% of legitimate ones. Fingerprints locate 493 rows in dataset B: 482 phishing, 11 legitimate.
- **Effect:** small on the score, but the model learns what a takedown page looks like, which no filter sees on a live phishing page.
- **Settled by the experiment above:** blanking (critic) creates a 97.8%-phishing missingness flag. Dropping (advocate's rebuttal) removes the shortcut.
- **Decision needed:**
  - confirm dropping 4.3% of rows by fingerprint, after a hand check of the 11 legitimate matches;
  - accept that the blank pages, which cannot be located, stay with a note.

**4. `[FORCED.risk]`** (SPLIT-8, SPLIT-32: only a person answers it; recommendation: accept, tagged).
- **Problem:** train and test come from the same weeks, while phishing adapts within weeks.
- **Effect:** cannot be measured (`Time: Lost`; no dated table with both classes exists).
- **Each side's evidence:**
  - Advocate: Andrej accepted the same risk for `website_phishing` (2026-11-18), in the same domain.
  - Critic: agrees on the substance, but the question must be asked.
- **What would settle it:** a dated release (PhishTank ids plus crawl dates), or a feature table built from PhreshPhish.
- **Decision needed:** accept the risk with the tag, or decline it, which retires the dataset as `Not Representative` and departs from the `website_phishing` precedent.

**Task-gamer exploits mapped**

| # | Exploit | Gain | Rule | Covered by a note or warning? | New or known | Issue? |
|---|---|---|---|---|---|---|
| 1–3 | Test-side group or tuple counts, value frequencies over all rows | +0.0003 to +0.0007; −0.0001 to +0.0005 over seeds (noise) | LEAK-9 (transductive), LEAK-30 | No note; no accepted warnings (`accepted: {}`) | New | No: within noise |
| 4 | Count of exact copies | 0 | LEAK-16, LEAK-19 | Duplicates note | Known | No |
| 5 | True `registered_domain` group size | −0.0001 | LEAK-33 | Group not a feature | Known | No |
| – | Look-up columns (strong signal) | alone 0.940 vs the note's 0.947; without them 0.975 vs 0.977 | LEAK-10 | "Potential leak, kept on purpose" note | Known; measured gain matches the note | Yes, but on the note's condition (issue 2), not its numbers |
| – | Format-only model 0.899 | – | LEAK-13 to LEAK-15 | Not in the notes | Known (builder and precedent checker) | No; record the k/n test (change 6) |

**Agreed facts**

- **Data:** 11,430 rows, 50/50; 6,634 registered domains; 24 domains hold both classes (833 rows).
- **Split:** 0 shared domains in every fold; leaf `L-FORCED.groups`. IID scores 0.995 against 0.990 grouped; merging the hidden groups changes +0.0001.
- **Exploits and shortcuts:**
  - none gains beyond noise; row order is flat (0.501);
  - 0.06% of test rows have a copy in training;
  - the best fixed URL rule scores 0.78.
- **Look-ups and takedowns:**
  - look-ups ran in late July to early August 2020;
  - 40 hosts hold more than 12 pages;
  - takedown pages are 12–16% of phishing in A and about 1% of legitimate; 493 fingerprinted rows in B;
  - on the traced phishing side the look-ups shift with page state, also within hosting type;
  - `statistical_report` = 2 is a failed DNS read (278 phishing, 28 legitimate);
  - 97 of the 213 phishing rows with `dns_record` = 1 are IP hosts.
- **Selection:** no look-up separates Alexa from Yandex pages (0.50–0.52).
- **Cost of the fixes:** option b ROC AUC 0.9817, 0.739 of phish caught at 1% FPR; with `statistical_report` also dropped, 0.9816.
- **Metric:** `roc_auc` fallback agreed by all.
- **Cleaning:** the CLEAN fixes and text corrections above are conceded by both sides.

**Consistency with precedent**

- **Option b** follows distribution_transformers_at_cauca_department and tunisian's `CTR_CESSAT`. It departs from onlinenewspopularity's keep-with-a-note because here the traced part shows a gain.
- **Dropping the takedown rows** departs from zillow_prize and melbourne_housing_market, where located late cells were blanked. The fact that sets this case apart: the located cells cluster on one class (97.8% phishing), so blanking would leave missingness that encodes the outcome (measured: 0.957 → 0.990).
- **`[FORCED.risk]` accepted** follows website_phishing (Andrej, 2026-11-18). Declining it would need a fact that sets this case apart; none is known.
- **`roc_auc` fallback** follows aeolus_rebuilt, gallstone_disease and website_phishing.
- **Selection Bias with `Yes`** follows website_phishing (Lennart, 2026-10-27).
- **`nb_www` kept** fits LEAK-15, with a 0.0004 cost.
- **Duplicates kept** follow hiva_agnostic (LEAK-19).

</details>

<details><summary>Claim audit</summary>

I found four claims that don't hold and one that can't be tested. None of them blocks shipping. The biggest is that about 12% of the phishing pages were saved after they had been taken down, which the definition doesn't mention.

All runs used the shipped splits.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | "The URL and page features are read from the page then" (when a user opens it) | curation_comments, Prediction point | Read the stored HTML of dataset A's 415 phishing pages safely (no code from the files ran); flag pages that are empty or show a takedown, error or parking message; compare with the 585 legitimate pages; score out-of-fold LightGBM on the shipped splits | **Refuted** for about 12% of phishing rows | 50 of 415 phishing pages (12%, roughly 9–15%) are empty or show "This function has been disabled" (×6, the same hosting path), "Account Suspended", "404 Not Found", "500 Internal server error", "tijdelijk offline", "Index of /" or a parking redirect (`ww5.<domain>`). Only 1 of 585 legitimate pages does. These pages are easier to call: mean out-of-fold score 0.977 against 0.899 for live phishing pages. Removing them moves ROC AUC on that subset only from 0.9908 to 0.9898. On all 11,430 rows, `nb_hyperlinks == 0` covers 18.6% of phishing pages and 5.6% of legitimate ones. | LEAK-10 (read after the event), LEAK-13 (classes recorded differently) |
| 2 | "at most 12 per domain"; "up to 12 per domain by the source's rule" | task_summary.row, grouping.definition | Count pages per host and per registered domain | **Refuted** | 40 single hosts hold more than 12 pages: en.wikipedia.org 141, a phishing host under duilawyeryork.com 214, youtube 42, shadetreetechnology.com 41. 55 registered domains hold more than 12. The paper's rule (Sec. 4.1) is not met by its own file. | PROV (description) |
| 3 | "`page_rank` 0 is Open PageRank's lowest rank and stays" | curation_comments, look-up codes | Read the release's `external_features.py`, then the distribution by class | **Refuted** as written | The code does `if result: return result else: return 0`, so a null rank (domain not in Open PageRank) also becomes 0. 2,666 rows have 0, 96% of them phishing; the next level (1) is 78% phishing. 0 is mostly "unranked". I did not open the API docs to confirm what the service returns for an unknown domain. | CLEAN (codes) |
| 4 | "`google_index` (1 = not indexed) and `dns_record` (1 = no NS record) had no failed queries" | curation_comments | Read the code, then inspect the `dns_record = 1` rows | **Refuted** as written | `dns_record` returns 1 on any exception. `google_index` returns 1 on any layout it fails to parse. A failure cannot be told apart from a real 1. 108 of the 230 `dns_record = 1` rows are IP-address hosts (an NS query on an IP), and most of the rest are free dynamic-DNS domains (2waky.com, xxuz.com, zzux.com). `dns_record = 1` means "IP address or failed query". | CLEAN |
| 5 | Shape 11,430 × 87, 50/50; six columns all 0 | curation_comments | Raw file | Holds | 5,715 / 5,715; `nb_or`, `ratio_nullHyperlinks`, `ratio_intRedirection`, `ratio_intErrors`, `submit_email`, `sfh` all 0 | – |
| 6 | Code counts: `domain_age` −1 1,781, −2 55, −12 one; `domain_registration_length` −1 46, 0 1,404; `web_traffic` 0 4,444 (81% phishing) | curation_comments | Counts | Holds | Exact, 81.2% | – |
| 7 | 6,634 domains; 24 hold both classes (833 pages); largest blogspot.com 383 | curation_comments | Group counts | Holds | 6,634; 24 / 833; max 383 | SPLIT |
| 8 | 291 phishing pages in 117 sets, 174 surplus copies; ~0.1% of test rows have a copy in train | curation_comments, builder | Copies of the features; copies of test rows found in train, per fold | Holds | 291 / 117 / 174, all phishing; 0–4 test rows per fold have a copy in train (≤0.1%) | LEAK-16 |
| 9 | The repeated URL's two rows differ in 8 URL and page features and in the WHOIS look-ups, read 13 days apart; within a domain the dates differ by up to 15 days | curation_comments | Compare the two rows; age spread within each domain | Holds, with a small wording error | Ages 5,627 and 5,614 (13 days); max spread within a domain 15. `domain_age` comes from the payapi age service, not WHOIS. `length_url` differs (62 vs 54) for the same stored string; 6 rows have `length_url != len(url)`, so the release cut some URLs short. | – |
| 10 | `nb_www` 67% vs 21%, ROC AUC 0.72 alone; dropping it costs 0.004 | curation_comments | Raw rates; shipped splits with and without `nb_www` | Holds, the cost is overstated | 0.671 / 0.222, AUC 0.723; on the shipped splits dropping it moves LightGBM from 0.9898 to 0.9894 (0.0004) | LEAK-13 |
| 11 | Look-ups alone 0.947, without them 0.977, all 0.990 | curation_comments | LightGBM on the shipped 3×3 splits | Holds | 0.940 ± 0.016, 0.975, 0.990 | LEAK-10 |
| 12 | Selection: no look-up tells Alexa from Yandex pages (0.50–0.52); phishing separates from either list alike | curation_comments | Checked the builder's as-of check, its design and log, plus `google_index` by source | Holds | `google_index` = 1 for 14.5% of Alexa and 14.9% of Yandex pages, against 91% of phishing. Only 296 Alexa and 289 Yandex pages have a known source. | Selection Bias |
| 13 | Metric: the paper reports accuracy and macro F1 as "two main metrics", Weka defaults, no threshold or costs; fallback `roc_auc` | `metric` reason, README Metric block | Read the arXiv text, Sec. 5 | Holds | Verbatim: "For performance evaluation, we use two main metrics: 1. Accuracy … 2. Macro F1-score", with Weka defaults and 10-fold CV. No threshold or cost is given. | MET-5, MET-6 |
| 14 | `roc_auc` is computable on every test fold; same target and balance as the source | metric (MET-2) | Count per fold; test domains vs train domains; scoring columns | Holds | Test folds 3,328–4,461 rows with 1,543–2,349 positives; no test domain also in training; no scoring columns. It sits near the ceiling (0.99); the builder already raised this as draft issue 3. | MET-2, MET-10 |
| 15 | Split: whole domains held out, as a filter meets new sites | splits_comment, time_basis | Domains shared between train and test in each of the 9 folds | Holds | 0 shared in every fold. Can't test whether time moves the score: no row is dated. | SPLIT |
| 16 | Proposed reasons for warnings: `nb_at = 1` (240 rows, 122 domains), `phish_hints = 4` (136, 71) | builder, check warnings (`accepted: {}`) | Counts | Holds | 240 / 122 and 136 / 71, all phishing. No warning is accepted in `dataset.py` yet. | – |
| 17 | How long after each report the look-ups were read | curation_comments (LEAK-10 note) | – | **Untested** | No row is dated, and there are no PhishTank ids | LEAK-10 |

**Refuted and untested claims, ranked**

1. **Page features describe pages already taken down (P4, LEAK-10 / LEAK-13, measured weak).**
   - **What it changes:** the definition says only the seven look-ups were read late. In fact about 12% of phishing rows also have page features of a suspended, parked, error or empty page. A filter would not see that state when a user first opens the live page, and legitimate pages almost never have it (1 in 585). The models learn it a little: those rows score as easier, but the effect on ROC AUC is about 0.001, so it is no reason to retire the dataset.
   - **Mildest remedy:** keep the rows and widen the "Potential leak, kept on purpose" note and `fit_reason` to cover takedown and empty pages, citing 50 of 415 in dataset A. These pages can only be found where HTML exists (1,000 of the 11,430 rows), so dropping them all is not possible; dropping only the 50 known ones would treat one part of the data differently.
   - **Optional check:** I flagged takedown pages with my own text patterns and looked only at the first 200 characters of each page's text, so 50 is approximate. A person reading a few of the flagged pages would confirm it.
2. **"At most 12 per domain" (P5, description).**
   - **What it changes:** the curator reads the wrong group sizes in the task summary. The grouping itself is unaffected.
   - **Mildest remedy:** reword `row` and `grouping.definition`, for example: "the source's limit of 12 URLs per domain is not met: 40 hosts hold more, en.wikipedia.org 141".
3. **`page_rank` 0 is mostly "unranked", not the lowest rank (P7).**
   - **What it changes:** the note's meaning. Tree models are unaffected; for linear models, unranked as lowest is roughly right.
   - **Mildest remedy:** correct the note ("0 also codes a domain Open PageRank does not list"). Keeping the values is defensible.
4. **`dns_record` and `google_index` failures cannot be seen (P7).**
   - **What it changes:** the note's meaning. `dns_record = 1` is largely the IP-address case, which the `ip` feature already covers.
   - **Mildest remedy:** reword the note to say the code records a failed query as 1, so failures can't be counted.
5. **Small wording errors:** `domain_age` is not a WHOIS look-up, and the `nb_www` cost is 0.0004 on the shipped splits, not 0.004. Fix the text.
6. **Untested:** how long after each report the look-ups were read (no dates), and the share of takedown pages outside the 1,000 rows of dataset A.

Everything else holds: the counts, the group facts, the copies, the effects of the look-ups, `nb_www` and the selection, the metric, and the grouped split. I found no copy of a row that crosses the split and no shared domain between train and test.

</details>

<details><summary>Column audit</summary>

I ran 14 analyses and edited no repository file. I found two problems that should be fixed before the curator signs off: some "phishing" pages were already taken down when they were crawled, and several stated dates are wrong. I also found three cleaning gaps and some feature names that don't match what the feature measures. The dtype probe flags 0 of 81 columns. The release's files are all accounted for: Mendeley v3 holds only `dataset_B_05_2020.csv` plus the `dataset_A_05_2020` and `scripts` folders, and `curation_comments` explains each.

**Column table**

The prediction point is when a user opens the page. Feature meanings come from the release's scripts (`url_features.py`, `content_features.py`, `external_features.py`, `feature_extractor.py`). "Fine" means: known when the page opens, numeric, no cleaning problem.

| column | meaning (from the scripts) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| length_url, length_hostname | character counts | yes | int | fine | |
| ip | regex: IPv4/hex host **or any run of 7 hex characters** in the URL. Only 97 of 1,721 flagged rows have a real IPv4 host | yes | int 0/1; the name misleads | fine; correct the meaning (finding 5) | CLEAN (meaning) |
| nb_dots, nb_hyphens, nb_at, nb_qm (`?`), nb_and, nb_eq, nb_underscore, nb_percent, nb_slash, nb_colon, nb_comma, nb_semicolumn, nb_dollar, nb_space, nb_star | counts of the character in the URL | yes | int | fine | |
| nb_tilde, nb_dslash | 0/1 flags (`~` present; `//` after position 6), not counts | yes | int 0/1 | fine (named as counts) | |
| nb_www, nb_com | URL words containing "www" / "com" | yes | int | fine; nb_www is the list-form difference already noted (0.72 alone) | |
| http_in_path | count of "http" in the path | yes | int | fine | |
| https_token | 1 if the scheme is http | yes | int | fine. 55% of legitimate pages are http, likely a form difference of the lists (AUC 0.556) | |
| ratio_digits_url, ratio_digits_host | share of digits | yes | float | fine | |
| punycode | `http://xn--` only, so https punycode is never flagged | yes | int | fine (note) | |
| port, tld_in_path, tld_in_subdomain, abnormal_subdomain, prefix_suffix, shortening_service, path_extension (`.txt`), suspecious_tld | regex flags | yes | int 0/1 | fine | |
| nb_subdomains | number of dots in the **whole URL**, capped at 3, not a count of subdomains | yes | int | fine; correct the meaning | CLEAN (meaning) |
| random_domain | NLP check of the domain | yes | int | fine | |
| nb_redirection | HTTP redirects when the crawler fetched the page | at the fetch: yes in kind | int | fine | |
| nb_external_redirection | 0/1 (the loop returns after the first hop) | as above | int | fine | |
| length_words_raw, char_repeat, shortest/longest/avg word (raw, host, path) | URL word statistics | yes | int/float | fine | |
| phish_hints | count of 16 hint words in the URL | yes | int | fine | |
| domain_in_brand, brand_in_subdomain, brand_in_path | matches against the static 257-brand list | yes | int | fine | |
| statistical_report | 0/1 = match against a static list of known phishing hosts and IPs; **2 = `gethostbyname(registered domain)` failed** at the look-up (278 phishing, 28 legitimate) | the list: yes. Code 2 is a DNS result read at the look-up, the same timing as `dns_record` | int mixing a flag with a failure code | cleaning problem (finding 3) | CLEAN-10, LEAK-10 |
| nb_hyperlinks | count of links in the fetched page | yes in kind; **for takedown rows it describes the takedown page** (finding 1) | int | see finding 1 | LEAK-10, USE-7 |
| ratio_intHyperlinks, ratio_extHyperlinks | internal/external share of links; **0 when there are no links** (1,381 rows) | as nb_hyperlinks | float | cleaning problem (finding 4) | CLEAN-10 |
| nb_extCSS | count of external CSS files | as above | int | fine | |
| ratio_extRedirection | share of external links that redirect, each fetched at the crawl; **external media are counted twice, so 50 rows lie above 1 (max 2)**; 0 when there are no external links | as above | float | cleaning problem (findings 4 and 5) | CLEAN-10, CLEAN-11 |
| ratio_extErrors | share of external links returning ≥400; 0 when there are none | as above | float | finding 4 | CLEAN-10 |
| login_form, external_favicon, iframe, popup_window, onmouseover, right_clic, empty_title, domain_in_title, domain_with_copyright | page flags | as above (finding 1) | int 0/1 | fine apart from finding 1 | |
| links_in_tags, safe_anchor | percentages; 0 when the denominator is empty (cannot be located) | as above | float | fine, with a note | |
| ratio_intMedia, ratio_extMedia | media percentages, which sum to 100; **both 0 when the page has no media** (3,874 rows) | as above | float | finding 4 | CLEAN-10 |
| whois_registered_domain | 1 when WHOIS's domain_name does not match the domain, **or when the WHOIS call raised an error** | read at the look-up (finding 2) | int; the failure is mixed in and cannot be separated | fine, note the failure meaning | CLEAN-10 (note) |
| domain_registration_length | **abs**(days to expiry) from the look-up date, so an expired domain reads positive; -1 and 0 already masked | look-up | float | fine, add a note | |
| domain_age | days since registration (payapi) at the look-up date; codes masked | look-up | float | fine; units confirmed by the dating in finding 2 | |
| web_traffic | Alexa REACH rank queried with the full URL; 0 masked | look-up | float | fine (the existing LEAK-10 note) | LEAK-10 |
| dns_record | 1 = no NS record (or any exception) | look-up | int | fine (the existing LEAK-10 note) | LEAK-10 |
| google_index | `site:<url>` search; 1 = not indexed **or the result page could not be parsed** | look-up | int | fine (existing note; failure meaning to document) | LEAK-10 |
| page_rank | Open PageRank integer; 0 = rank 0 **or domain not found** | look-up | int 0–10 | fine | |
| registered_domain | the group | split metadata | category | fine | LEAK-33 |
| dropped: url, the six all-zero columns | | | | correct | |

**Problems, ranked**

**1. Some "phishing" pages were crawled after they were taken down (LEAK-10 second clause, USE-7; Should, weak on the score).**

The release's crawler (`is_URL_accessible`) keeps any HTTP 200 response. Hosting suspension pages, link-shortener warnings and parking pages all return 200.

- **What dataset A shows.** I read the page HTML in dataset A with an inert unpickler (no code from the files ran). Of the 415 phishing pages:
  - 65 (15.7%) are takedown pages: "Account Suspended" 26, ChangeIP host default 9, rebrand.ly "Stop! Deceptive page ahead!" 4, the APWG/CMU "Phishing Education Landing Page", parking pages, and 404/500 pages served with status 200.
  - 74 more (17.8%) are blank.
  - Of the 585 legitimate pages, 6 (1.0%) are takedown pages and 30 (5%) are blank.
- **What the features then describe.** For these rows the content features describe the page after the report, not the page a user opens. 77% of phishing pages with zero links in A are dead pages, and in B 18.6% of phishing rows have zero links against 5.6% of legitimate ones.
- **The rows can be located in B.** The takedown templates leave fixed content-feature fingerprints:
  - the "Account Suspended" fingerprint matches 238 rows in B, 237 of them phishing;
  - the ChangeIP fingerprint matches 59 rows, all phishing;
  - the strong fingerprints together match 493 rows (482 phishing, 11 legitimate).
- **How much it moves the score** (grouped LightGBM, 5 folds × 3 seeds):

  | Features | Live phishing vs legitimate | Dead phishing vs legitimate |
  |---|---|---|
  | all | 0.988 | 0.996–0.998 |
  | content only | 0.887 | 0.965–0.979 |

  On the full file, all features score 0.9907. Scored without the 493 fingerprinted rows it is 0.9903.
- **Remedy.** LEAK-10 says late cells that can be located are blanked. The mildest fix is to set the content features to missing on the fingerprinted rows (a guarded fingerprint list in `_clean`) and add a note in `curation_comments` and `fit_reason` covering the blank pages, which cannot be located. The alternative is to drop those rows as pages no filter would act on (USE-7). This is the curator's call.
- **Not covered today.** The definition's "Potential leak" note covers only the look-ups.

**2. The collection dates in the definition are wrong (fact accuracy; Should).**

- **Look-ups.** `domain_age` against known registration dates (google.com, facebook.com, wikipedia.org, youtube.com, microsoft.com, apple.com, twitter.com and others) puts the look-ups for legitimate domains at **21–26 July 2020**. Phishing domains were looked up over about 15 days into early August. This matches `external_features.py`, which is dated 27 July 2020.
- **Pages.** Phishing URLs carry creation timestamps up to **3 August 2020** (18 appspot version hosts dated 23 July to 3 August; some are also in dataset A). So at least part of the page crawl happened in late July and August, not March to May.
- **Where it is wrong.** "crawled in March to May 2020" in `task_summary.row`, the "Collection" and look-up bullets in `curation_comments`, the `time_basis` text, and the record's `collection_period`. The 15-day spread within a domain comes from crawling in batches.
- **The leak itself is milder than the notes say.** appspot phishing URLs created 23–24 July were looked up at domain age 5616, and those created 3 August at 5626–5627. That puts the look-up about 1 day after each URL appeared, a short gap after the report, at least for the rows that can be dated. The LEAK-10 note should say so.
- **Remedy.** Correct the dates and the note. No change to the data.

**3. `statistical_report` mixes a flag with a failure code (CLEAN-10; Should).** Code 2 means DNS resolution failed (306 rows: 278 phishing, 28 legitimate), stored on what reads as a 0/1/2 scale. It is also a DNS result read at the look-up, the same timing as `dns_record`, yet it is not among the "seven look-ups" in the notes. Remedy: set 2 to missing (or split it into its own flag) and name it in the look-up note.

**4. Ratios over an empty set are coded 0 (CLEAN-10; Should; precedent `medical_facility_operational_data`).**

| Columns | Denominator that is empty | Rows |
|---|---|---|
| `ratio_intHyperlinks`, `ratio_extHyperlinks` | `nb_hyperlinks == 0` | 1,381 |
| `ratio_intMedia`, `ratio_extMedia` | no media (the two sum to 0, otherwise to 100) | 3,874 |
| `ratio_extRedirection`, `ratio_extErrors` | no external links | approximately locatable |

These are 0 for "undefined", not a measured 0. Remedy: mask them where the denominator can be located. Expected score effect is about 0 for tree models; it matters for linear models and kNN.

**5. Several feature names don't match what the feature measures (Weigh; document).**

- `ip`: about 94% of its 1s are 7-hex-character runs, not IP hosts. It could be recomputed from the URL before the URL is dropped.
- `nb_subdomains`: counts the dots in the whole URL, capped at 3.
- `ratio_extRedirection`: reaches 2 because the formula counts external media twice (50 rows).
- `domain_registration_length`: takes the absolute value, so an expired domain reads positive.
- Codes that also mean a failure: `whois_registered_domain` = 1, `google_index` = 1 and `page_rank` = 0.
- The crawler's homepage fallback (`is_URL_accessible` fetches `scheme://www.netloc` when the URL raises) can put the homepage's content on a URL's row.

Remedy: one bullet in `curation_comments`. None of these is a leak.

</details>

<details><summary>Split audit</summary>

The split is **right with notes**. The tree leads to the same leaf the definition names (`L-FORCED.groups`), and the grouping holds against the hidden groups I tested. Nothing needs a re-split. One question stays with a person: whether to accept the risk of temporal leakage at [FORCED.risk].

**Walking the tree (SPLIT-36)** from the record's type, `Database Snapshot`:
- **[DB.meets]:** a filter rates new pages as users open them, one by one. That sends the walk to the order and windows step, where the order would have to come from the row order or an id issued in sequence.
- **[ORDER.order]:** no order can be rebuilt.
  - The paper says the rows were shuffled (Sec. 4.3). I re-ran `time_probes.py` and the raw order is flat (p 0.22, size 0.026, no flags).
  - No row carries a date or a PhishTank id.
  - `domain_age` gives crawl dates only relative to other rows of the same domain, never across domains.
  - Dating only the phishing half through PhishTank would mix time with the class.
- **[FORCED.test]:** one crawl (March to May 2020) with nothing dated, so nothing can be measured.
- **[FORCED.reason]:** the agent answers no.
- **[FORCED.risk]:** a person's question; the agent answers no.
- **[FORCED.groups]:** yes. The registered domain is a true id rebuilt from the URL, the unit a filter meets new.
- **Leaf:** `L-FORCED.groups`, which is what `split_leaf` and the `ForcedGroupedFromTemporal` time basis say and what ships. It is not forced against the tree, other definitions already reach it, and every question had an answer that fit.

**Regime and size.** The use case meets new pages, mostly from new sites, so grouping by site matches it. Labels are per page and 24 domains hold both classes, so the scored unit is the row. The training side holds 6,969 to 8,102 rows, which puts it in SPLIT-33's 3-repeat tier, and 3 repeats × 3 folds is what ships. Each test fold holds about 2,210 domains.

The temporal checks (windows, horizon, gap, the newest period) do not apply, since no window exists.

**Measured** with LightGBM (400 trees, n_jobs 4, 3 seeds × 3 folds):

| Split | ROC AUC |
|---|---|
| IID (random rows) | 0.9950 ± 0.0006 |
| Shipped splits | 0.9899 ± 0.0023 |
| Grouped by registered domain, my folds | 0.9902 ± 0.0011 |
| Coarser groups that merge the hidden groups below | 0.9903 ± 0.0011 |

**Hidden groups and unrecorded repeats (LEAK-42, LEAK-43).** I joined three kinds of link across registered domains:
- **Same name, different suffix:** `google.*` across 10 suffixes, `blogspot.*` across 7.
- **Same path on several domains, all phishing:** the clearest is `/~u43730p39181/pki-validation` on 30 `mail.*.nl` hosts, one campaign. `/blog/profile/` repeats on 20 domains.
- **Exact feature copies across domains.**

These joins touch 1,613 rows, 76% of them phishing; the 98 pages hosted on bare IP addresses are all phishing. On the three tests:
- **Is the link above chance?** Yes.
- **Does the label travel with it?** Yes, the shared paths are all phishing.
- **Is there an order?** No.

It still does not matter: grouping by the coarser units changes the score by +0.0001. On the merged rows, phishing recall at 0.5 is 0.941 under the shipped grouping and 0.945 under the coarse one. The builder's hidden-group probe agrees (domain +0.009, near copies +0.002, no hit). LEAK-44 (a later record carrying an earlier label) has no rows it could apply to.

**Problems, ranked**

1. **[FORCED.risk] is open for a person** (SPLIT-8, SPLIT-32; Andrej, 2026-11-19).
   - *The risk:* this split trains on pages from the same weeks as the test pages, while phishing kits and lures adapt to filters within weeks. The look-ups add post-report state the record already names under LEAK-10. So the 0.990 likely overstates what a deployed filter sees later. The data cannot measure how much.
   - *Against declining it:* no dated feature table with both classes exists (the record's search found PhreshPhish, which has dated pages but only URL and HTML). This would be the benchmark's only phishing task. The time basis and `fit_reason` already say the step forward is untested.
   - *Remedy:* none in the split. Keep `ForcedGroupedFromTemporal` unless the curator declines the risk, which would retire the dataset as `Not Representative`. The main session should raise it as a decision.

2. **How hosting platforms group (the builder's issue 2) costs almost nothing either way** (USE-10).
   - The use case meets a new `x.blogspot.com` page with other blogspot pages already in training. Keeping the private suffixes (option C) is therefore a little closer to deployment than the shipped registered domain (option A).
   - The builder measured A at 0.9905, C at 0.9912 and grouping by host at 0.9928. The coarse grouping above shows that merging further also changes nothing.
   - *Remedy:* keep A, the more conservative choice, and record in the issue that the measured difference is under 0.002.

3. **Test folds vary in class share, 0.446 to 0.586.** The large single-domain groups cause it (blogspot.com 383 pages, duilawyeryork.com 351, the evesyalari.tk campaign 366 after merging). ROC AUC ignores the class share, so no remedy is needed. A stratified group split would only matter if the metric changed to accuracy or log loss.

Nothing else was found: no wrong leaf, no forced leaf against the tree, no entity leakage.

</details>

<details><summary>Domain practitioner</summary>

I would use this model. The fit is **approximate**, and I agree with the `fit_reason`. The metric scores my decision only **partly**: ROC AUC is right under the rules as they stand, but the score I would actually pick a model by is how many phish it catches at a very low false-alarm rate.

I'm judging as the engineer of a browser's or mail gateway's phishing detector, which rates a page when a user opens it and then warns or blocks.

**Fit: approximate.** Each row is one page-open decision, and the URL and page inputs are what I have at that moment. But both classes are lists: reported phish that were still live at the crawl, against top-ranked sites plus an older search-engine list. That is not the traffic my filter meets, and the external look-ups describe the crawl, not the first visit. Under USE-8 the selection is a known gap the real setting does not share, so the fit is approximate, not direct.

**The gaps, ranked by how much they change the task**

1. **The prevalence and the operating point (MET-1, MET-7, MET-9).** In real traffic, phishing is a small fraction of pages, and a false block costs me more than a miss. I run the model at a false-positive rate of about 1% or lower and care how many phish I catch there.
   - PhreshPhish (Dalton et al. 2025) builds its benchmarks at base rates of 0.05% to 5%. It scores by average precision and precision at a fixed recall, and says most published phishing results look excellent because their base rates are unrealistically high.
   - I measured this here: 3 grouped folds × 3 seeds, untuned models.

   | Model, all 81 features | ROC AUC | Phish caught at 1% false alarms | Phish caught at 0.1% false alarms | Log loss |
   |---|---|---|---|---|
   | LightGBM | 0.989 | 0.817 ± 0.065 | 0.40 ± 0.17 | 0.137 |
   | Random forest | 0.987 | 0.723 ± 0.113 | 0.33 ± 0.09 | 0.183 |
   | Logistic regression | 0.981 | 0.713 ± 0.126 | 0.25 ± 0.19 | 0.180 |

   - ROC AUC spreads the three models by 0.008. At 1% false alarms they spread by 0.10, and that is the gap I would feel in production.
   - Both metrics rank the models the same way. Log loss does not: it puts the random forest below logistic regression, and a log loss on balanced list labels says nothing about calibration at my real prevalence.
   - The rules do not let us declare my number. The source fixes no threshold, MET-7 forbids inventing one, the registry has no partial-AUC metric, and at 0.1% false alarms the folds are too noisy (± 0.17).
   - So the `roc_auc` fallback stands (MET-5, MET-6, MET-8), and I would not switch to `log_loss`. The metric reason should still say that ROC AUC weighs the whole false-positive range, while my decision lives below 1%.

2. **The legitimate side has none of my hard negatives.** The pages that cost me false blocks are long-tail and newly registered legitimate sites, small services' login pages, and legitimate pages on hosting platforms. Alexa top-500 crawls and a pre-2019 Yandex list contain few of them.
   - The closest the data comes is the 24 domains that hold both classes, mostly hosting platforms (833 pages).
   - On those pages ROC AUC falls to 0.88–0.91, against 0.98–0.99 overall. The variance is high because these few big domains fall into folds unevenly.
   - This is the selection gap `fit_reason` names (`Selection Bias`). It belongs in the review as the reason the fit is approximate. It is no reason to reject.

3. **The phishing side is pages that survived, read after their report.** My detector exists for the zero-hour page that no list has yet; Google's own production classifier (Whittaker et al., NDSS 2010) was built to find pages before the lists do. Here every phish was already on PhishTank or OpenPhish and still live at the crawl, which favours longer-lived kits. The look-ups were read after the report (LEAK-10, already named and kept on purpose). Without a date per row (`Time: Lost`), none of this can be measured, and the notes already say so.

4. **Two of the seven look-ups are inputs I cannot have.**
   - **`web_traffic`:** the Alexa rank was discontinued on 1 May 2022, so no deployed model can query it today. I would use Tranco or Cisco Umbrella instead.
   - **`google_index`:** this check scrapes Google's index for the page. That is not something I can do on every page view; I would use it offline at most.
   - The other look-ups (WHOIS age and expiry, DNS, PageRank) I do get, from cached feeds rather than a 4–5 s live query, which is the extraction time the paper's Sec. 6.5 weighs.
   - Measured without these two features, LightGBM drops from 0.989 to 0.986 ROC AUC, and from 0.817 to 0.749 caught at 1% false alarms. They carry a real part of the performance at the operating point I care about.
   - This is no leak, and the task is a 2020 detector, so I would keep both. But the `known` field and the notes should say that the Alexa rank no longer exists and that the Google-index check is a crawl-time feature.

5. **Inputs I would always have that are missing.** The TLS certificate (issuer, age, Certificate Transparency), the IP and hosting network, the redirect chain, the referrer or email context, the visible text, and visual similarity to the brand being imitated. Their absence lowers the ceiling but does not falsify the task. It should not change anything we ship.

6. **The target is a list-membership proxy, a close one.** PhishTank entries are verified by the community and OpenPhish's feed is automated. "On a phishing list" is near enough to "is phishing" for me to act on. I want a probability, so I can set my own threshold for the base rate.

**Would I use it?**

As a component, yes. I would trust its URL and page features, the split by registered domain (it tests sites I have never seen, which is the right unit), and the absence of any form shortcut (the best fixed rule on the URL scores 0.78, against 0.9998 for PhiUSIIL).

I would distrust the headline 0.99 for three reasons: it is measured at 50% prevalence, on easy legitimate sites, and with look-ups read after the report. Before deploying, I would re-check it on dated traffic at a realistic base rate.

**What an expert would change**

- **Metric:** keep `roc_auc` under the rules, and add to the metric reason that the decision runs below 1% false alarms, where untuned methods spread 0.71 to 0.82 against 0.981 to 0.989 for ROC AUC.
- **Inputs:** state in `known` and the curation notes that Alexa ended in 2022 (Tranco or Umbrella is today's substitute) and that `google_index` can only be read at crawl time.
- **`fit_reason`:** name the hosting-platform pages (833 rows, ROC AUC about 0.90) as the part closest to the hard legitimate pages a real filter meets.
- **Data:** mark PhreshPhish (dated pages, legitimate side from real browsing, its own time split) as the dataset to replace this one once a feature table is built from it. The issue file already lists it.

**Sources**

- The definition (`dataset.py`, `task_summary`, `curation_comments`), the record's screening blocks, the builder report and probes, and `website_phishing`'s decision item.
- Hannousse and Yahiouche, arXiv 2010.12847 (Sec. 4–6, as cited in the record).
- [Whittaker, Ryner, Nazif, NDSS 2010](https://www.ndss-symposium.org/wp-content/uploads/2017/09/whit.pdf) ([Google Research page](https://research.google/pubs/pub35580/)).
- [PhreshPhish, arXiv 2507.10854](https://arxiv.org/html/2507.10854v2).
- Alexa's retirement: [SecurityWeek](https://www.securityweek.com/impact-alexa-ranking-service-shutdown-cybersecurity-industry), [DomainTools](https://www.domaintools.com/resources/blog/mirror-mirror-on-the-wall-whos-the-fairest-website-of-them-all).
- Rules cited: USE-1, USE-3, USE-5, USE-8, USE-10; MET-1, MET-5, MET-6, MET-7, MET-8, MET-9, MET-10; LEAK-10.

</details>

<details><summary>Blind reviewer</summary>

**Verdict: include with changes.** This is a real phishing-detection task with honest grouped splits and no strong leak in the columns. But it is close to saturated (grouped-CV AUC 0.99), and its legitimate class mostly comes from very popular domains. Treat it as an easy, ceiling-limited dataset, and document the sampling bias.

**What the task is.** A browser, email gateway or URL-reputation service decides, when it scores a URL, whether to block or warn about the page. That is a real and common use. Each row is one URL (11,430 rows) described by 81 features in three groups: 55 from the URL's text, 19 from the page content, and 7 from outside lookups such as Google indexing, PageRank, WHOIS and Alexa traffic. The data are real, collected in May 2020 by Hannousse & Yahiouche from PhishTank and OpenPhish (phishing) and from Alexa and Yandex (legitimate). This is the widely mirrored "Web page phishing detection" set on Mendeley, Kaggle and Hugging Face.

**Concerns, most serious first**

1. **The legitimate class is skewed toward popular domains, so models can learn "is this site famous?"**
   - The source paper says legitimate URLs came from "the top 500 Alexa domains" (about 12 URLs per domain), plus a still-active Yandex set.
   - The strongest single features are exactly the popularity ones:

     | Feature | AUC on its own |
     |---|---|
     | `google_index` | 0.86 |
     | `nb_hyperlinks` | 0.82 |
     | `page_rank` | 0.81 |
     | `web_traffic` | 0.69 |
     | `domain_age` | 0.68 |

   - `page_rank` = 0 covers 2,565 phishing rows against 101 legitimate ones.
   - `web_traffic` is missing for 63% of phishing rows but only 15% of legitimate rows.
   - A real filter mostly sees obscure legitimate sites, so these scores overstate real-world performance. For comparing methods against each other this matters less, since all methods face the same bias.
   - **Change:** say this in the task notes. Optionally offer a variant without the 7 external-service columns (grouped AUC 0.974, accuracy 0.92), which is also more realistic for on-device detection where those lookups are not available.

2. **Nearly saturated, so it will separate methods only weakly.**
   - LightGBM with grouped 3-fold CV: AUC 0.990, accuracy 0.952.
   - A plain logistic regression: AUC 0.979, accuracy 0.938.
   - Random (ungrouped) CV gives 0.995, so the grouping removes only a little optimism.
   - There is still roughly 5% error, so it is usable, but differences between strong methods will be small.
   - **Change:** prefer log-loss or error rate over AUC as the metric.

3. **The external-lookup features may not hold at prediction time.**
   - `google_index`, `page_rank`, `web_traffic`, `domain_age`, `dns_record` and `whois_registered_domain` come from third-party services at the time of crawling. They are knowable when predicting, so this is not leakage.
   - However, a fresh phishing URL is by definition not yet indexed and has no traffic, and some of these services (Alexa, OpenPageRank) have changed or shut down since 2020.
   - That is a realism concern, not a leak.

4. **The 50/50 class balance is artificial** (5,715 rows per class). Real phishing prevalence is far lower. That is acceptable for a benchmark but should be stated; AUC and log-loss are less affected by it than accuracy.

5. **Duplicates and the split.**
   - There are 175 exact duplicate feature rows (292 rows involved), all with the same label, spread over only 51 domains.
   - Grouping by `registered_domain` keeps nearly all of them on the same side of the split.
   - There are 6,634 groups. 84% hold a single URL, but the largest holds 383 URLs (67% phishing, probably a shared hosting service), and only 24 groups contain both labels.
   - The grouped split is the right choice. No change is strictly needed, though collapsing the exact duplicates would be harmless.

6. **Preparation looks sensible.**
   - The raw `url` column was dropped, which is correct: a raw string would invite text-based shortcuts and copying.
   - `registered_domain` is hashed and used only for grouping. It must not be offered as a feature.
   - Six columns that are zero for every row in the public file appear to have been dropped (87 → 81).
   - Missing values exist only in `domain_age` (1,837), `domain_registration_length` (1,450) and `web_traffic` (4,444). They look like the source's -1/0 "unknown" codes turned into NaN, which is fine. The missingness itself carries signal, which is acceptable.
   - Value ranges are plausible: ratios are on 0–1 or 0–100 scales, inconsistently, as in the source.
   - The target is stored as a category with values Yes/No. No training-weight column is defined, so there is nothing to judge there.

**What I could not check**

- I could not see the raw URLs, so I could not confirm the domain grouping or how near-duplicate URLs are distributed.
- I could not tell whether the dropped columns are exactly the constant ones from the source.
- I could not confirm how the source encoded missing values (-1 vs 0) before they became NaN.
- I could not check whether any phishing pages were captured after takedown, as parking or error pages.
- I did not read the full paper beyond the source description quoted above.

Sources:
- [Mendeley dataset c2gw7fy2j4](https://data.mendeley.com/datasets/c2gw7fy2j4/3)
- [arXiv 2010.12847](https://arxiv.org/pdf/2010.12847)
- [Hugging Face mirror](https://huggingface.co/datasets/husseinnashed/phishing-url)

</details>

<details><summary>Task gamer</summary>

**Verdict: this task can hardly be gamed.** The honest LightGBM baseline already scores 0.9892 AUC, and no exploit I built gains more than about 0.0007. That gain also falls to between −0.0001 and +0.0005 when I refit with other seeds, so it is noise.

Baseline: untuned LightGBM on `features()`, scored on the 9 shipped splits. Mean 0.98920, range 0.98653–0.99324. Adding a column of random numbers moves the mean by −0.00022 to +0.00011 over 5 draws.

| # | Exploit | Honest score | Exploited score | Gain (mean; per-split range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Test-side group size: rows that share the domain-lookup tuple (`domain_age`, `domain_registration_length`, `web_traffic`, `page_rank`, `whois_registered_domain`, `dns_record`), counted within the train and test side separately | 0.98920 | 0.98993 | +0.0007 with seed 0; +0.0005 / −0.0001 / +0.0003 over 3 subsampled seeds; per split −0.0019 to +0.0016 | No: it uses the test set's makeup (the task says group context is `none`) | None needed; it is within noise |
| 2 | Same tuple count over all rows, train and test together | 0.98920 | 0.98963 | +0.0004 | No (needs the test rows) | None needed |
| 3 | How often each value appears over all rows (`domain_age`, `web_traffic`, `length_hostname`, …) | 0.98920 | 0.98951 | +0.0003 | No | None needed |
| 4 | Number of exact copies of a row's features | 0.98920 | 0.98919 | 0 | No | — |
| 5 | True `registered_domain` group size (upper bound, uses the forbidden group column) | 0.98920 | 0.98910 | −0.0001 | No | — |

**How #1–#3 work.** Group size does predict the label: single-row domains are 36% phishing, larger groups 62–73% (AUC 0.64 alone). Rows of the same domain share the six domain-lookup values, so the group can be rebuilt from features: 7,606 distinct tuples against 6,634 groups. But the page and URL features already carry this signal. The true group size adds nothing (#5). The rebuilt counts add +0.0003 to +0.0007 with seed 0, which is above the random-column spread. Across seeds the gain swings between −0.0001 and +0.0005, and individual splits go either way (−0.0019 to +0.0016). I would not count it as a real gain.

**Strong features that are signal, not exploits:**
- **`google_index`** alone gives AUC 0.865. Despite the name, 1 means "not indexed" (84% phishing), against 11% phishing when 0.
- **`page_rank` and `web_traffic`** come next. A missing `web_traffic` value means 81% phishing, against 30% when present.
- **These three plus `nb_hyperlinks`** reach 0.960 together.
- **Dropping all eight lookup columns** (whois, DNS, Google index, page rank, traffic and similar) still leaves 0.973.

A deployed model can query all of these when the page opens. One fact would decide whether they are fair: when the source authors collected them. If they were collected after a phishing URL was reported, a lookup may reflect the takedown (for example, the page dropped from the index) rather than the page at first visit. The kit cannot answer this.

**Format-only model (0.899): signal, not an artefact.** It uses only missingness flags and "is the ratio a whole number" flags. Those flags track pages with few or no links or media, where ratios come out as exactly 0 or 100: for example, `ratio_intHyperlinks` is a whole number for 51% of phishing pages against 11% of legitimate ones. That reflects page content, not the two classes being recorded differently. The domain lookups are stored as whole numbers in both classes.

**Flaws that hurt an honest model:** none found. 24 `registered_domain` groups (833 rows) mix both labels. That is expected, since labels are per URL (for example, phishing pages on a hosting domain). I did not try dropping them because nothing points to a problem.

**Attacks that found nothing:**
- **Row order:** position against label AUC 0.501; neighbouring rows share a label 49.3% of the time; label rate per tenth of the file 0.48–0.54.
- **Copies across the split:** 0.06% of test rows have an exact feature copy in training. Only 4 duplicate keys span groups (9 rows), all with the same label.
- **Values over all rows:** no columns are standardised or min-max scaled over the whole table, and no negative sentinel values remain (missing values are NaN).
- **Train against test classifier:** AUC 0.81, which is expected when whole domains are held out. It exposes no label signal.
- **Timing and weight attacks:** there is no time column and no training weight, so none apply.

**Web search:** I found no forum thread or write-up reporting a leak or "magic feature" for this dataset. One informal analysis on Hugging Face also suspects `google_index` is coded as a suspicion flag rather than "is indexed", which matches what I found. The PhreshPhish paper criticises the random splits used on older phishing datasets; the grouped split here avoids that. Looking rows up in the published file would not work: the URL column is gone and the domain is hashed, so only the feature values could match.

**What I could not check:**
- When the source authors collected the lookup columns, relative to when each URL was reported as phishing.
- Whether the kit's preparation turned the original file's −1 sentinel values into NaN. I did not download the source CSV to compare.

Sources:
- [Mendeley dataset c2gw7fy2j4/3](https://data.mendeley.com/datasets/c2gw7fy2j4/3)
- [arXiv 2010.12847](https://arxiv.org/abs/2010.12847?context=cs)
- [Hugging Face: Web_page_Phishing](https://huggingface.co/datasets/yonatane22-bh/Web_page_Phishing)
- [PhreshPhish (arXiv 2507.10854)](https://arxiv.org/html/2507.10854v1)

</details>

<details><summary>Precedent checker</summary>

I checked the builder's draft recommendations for web_page_phishing_detection against past decisions. Two findings: one real departure without a valid reason (issue 1), and one departure whose reason I tested and found sound (probe 17). The other decisions follow precedent.

One thing first: the record has no curator decision yet on replacing `website_phishing`. Its verdict is still `TBD -> Yes` with no CC line, and the decision item (`website_phishing`'s decision item, option B) is unanswered. The build is ahead of that decision, so the review should point to it rather than assume it.

**Finding 1: issue 1, keeping all seven look-ups with a note, departs without a reason that meets LEAK-10**

**Where it stands:** LEAK-10 (Must), as amended on 2026-10-26: a value read at a later pull, whose late cells can't be found row by row, "go[es] when they may carry a gain". It stays with a note "only when the part that can be traced shows none".

**Precedents:**
- **distribution_transformers_at_cauca_department** (Lennart, 2026-10-21): attributes looked up after the outcome changed for an unknown subset of the positive cases. They were dropped, and LEAK-10 was not amended. This is the closest case.
- **tunisian_fraud_detection_challenge** (Lennart, 2026-11-05):
  - Registry fields looked up at extraction were kept, because nothing links a change in them to the outcome.
  - `CTR_CESSAT`, a status that records a later event, was dropped.
- **onlinenewspopularity** (Lennart, 2026-10-26, "go with (a)"): kept with a note, but only because the traced cells were the late cells themselves. Masking them changed R² by −0.0004.
- **zillow_prize and melbourne_housing_market** (Lennart, 2026-10-21): late cells that could be located were blanked.

**Why the stated reason doesn't fit:**
- The builder's trace (Alexa against Yandex pages, ROC AUC 0.50 to 0.52) tests only the legitimate pages. No outcome changes a legitimate page.
- The mechanism LEAK-10 is about acts only on phishing pages: a report, then de-indexing, delisting or the domain being suspended. So the part that matters is never traced, and the onlinenewspopularity condition is not met.
- `google_index` and `page_rank` record a status after a later event, the same kind of field as `CTR_CESSAT`.
- The note uses LEAK-38's heading ("Potential leak, kept on purpose:"). LEAK-38's own text sends "a value looked up at extraction" back to LEAK-10, and it covers only data a company released for its own competition.

**New evidence, measured today** on `dataset_B_05_2020.csv`:
- `dns_record` = 1 (no name-server record at look-up) on **213 phishing rows against 17 legitimate ones**.
- 187 of those 213 phishing pages still have links in their crawled content (`nb_hyperlinks > 0`). So the page was served at the crawl, but the domain's DNS was missing when it was looked up.
- That is a trace of a look-up read after a change on the phishing side, which is the distribution_transformers pattern.
- Caveat: several of these hosts are dynamic-DNS providers (2waky.com, zzux.com, xxuz.com), and I did not check what the extraction script queries.
- By the same mechanism, `dns_record` and `whois_registered_domain` (a domain suspended after the report) fall under LEAK-10 too, not only the three fields in option B.
- `domain_age` read later makes phishing domains look older, which weakens the signal. LEAK-11 keeps such a value, as in south_africa_coronary_heart_disease.

**Reflection prompt (draft for the record's `## Review`):**

> **Keep the seven look-ups read at the crawl, although LEAK-10 drops a late read that may carry a gain when the late cells cannot be found?**
>
> * **Problem:**
>   - The builder recommends keeping all seven look-ups with a note (option A). LEAK-10 keeps a late read that can't be found row by row only "when the part that can be traced shows none"(LEAK-10). Here the traced part (Alexa against Yandex) is the legitimate side, where nothing changes after a report.
>   - The mechanism acts on phishing pages: a report, then de-indexing or suspension. That moves `google_index`, `page_rank` and `web_traffic` towards the label. `dns_record` is missing on 213 phishing rows against 17 legitimate ones, and 187 of those pages had been crawled with content, so the DNS was gone at look-up.
>   - Closest cases: distribution_transformers_at_cauca_department (Lennart, 2026-10-21) dropped attributes that changed for an unknown subset of positive cases, and tunisian_fraud_detection_challenge's `CTR_CESSAT` (Lennart, 2026-11-05) dropped a status recording a later event.
>   - Cost of dropping (builder, grouped LightGBM): 81 features 0.9905; minus `google_index`, `page_rank` and `web_traffic` 0.9824; minus all seven 0.9757.
>
> | | Option | Pro | Con |
> |---|---|---|---|
> | a | Keep all seven with a note, naming the fact that sets this case apart: a fresh phishing page is almost never indexed, ranked or in Alexa when a user first meets it, so the late read changes few cells | keeps 0.008 ROC AUC; the note says what is unknown | the fact can't be measured here (no dates); the `dns_record` hint suggests the opposite |
> | b | Drop the status look-ups the report can move (`google_index`, `page_rank`, `web_traffic`, `dns_record`, `whois_registered_domain`); keep `domain_age` (LEAK-11) and `domain_registration_length`, each with a note | follows distribution_transformers and `CTR_CESSAT` | costs about 0.01 ROC AUC (not measured for this exact set); loses the paper's external-feature group |
> | c | Drop all seven | simplest; follows distribution_transformers | `domain_age` would go although a late read weakens it (LEAK-11 keeps such a value) |
> | d | Amend LEAK-10 for look-ups whose late read can't be traced on the side the mechanism acts on | an explicit rule | a third kind of LEAK-10 clause in a month; amending a Must needs a reason above it |
>
> **Recommendation:** b. It is the only option that matches the precedents without a new fact. Choose a only if you accept the "fresh pages are rarely indexed" fact as what sets this case apart, and write it in the CC line.
>
> LEAK-10 (Must), second clause, amended 2026-10-26 (Lennart, onlinenewspopularity).
> LEAK-11 (Should; narrows LEAK-10): a later value that weakens the signal stays, with a note.

**Finding 2: number format alone scores 0.900, kept; departs with a reason that holds**

- **Precedent:** polish_companies_bankruptcy was retired for class-dependent recording, with label-free format markers at ROC AUC 0.96. american_companies_bankruptcy was kept, with markers at 0.54 (LEAK-13 to LEAK-15).
- **What sets this case apart:** the builder says one script wrote both classes and the decimals follow each value's denominator. I tested this:
  - `ratio_intHyperlinks`, `ratio_extHyperlinks`, `ratio_digits_url` and `ratio_digits_host` are exact fractions k/n of integer counts, within 1e-6.
  - That holds on 5,715 of 5,715 phishing rows and 5,711 of 5,715 legitimate rows.
  - So the decimals are a property of the values, not a recording convention that differs by class.
- **Verdict:** follows precedent, with a reason. Suggestion: write this test into the curation note so the distinction from polish is recorded.

**Consistent with precedent (no prompt needed)**

- **Issue 3, metric `roc_auc` as the fallback:** Sec. 5 reports accuracy and macro F1 side by side, so there is no single source metric.
  - Precedents: aeolus_rebuilt (Lennart, 2026-10-26, "keep roc auc"); website_phishing (`roc_auc` at 0.978 to 0.983); gallstone_disease and ljubljana_breast_cancer (MET-5, MET-6).
  - No binary dataset has taken `log_loss` as its fallback. Option B would be the first, under MET-10's ceiling point and the diversity point (Andrej, 2026-11-02). That would be a deliberate new call, not drift.
- **Issue 2, grouping by registered domain (public suffixes only):**
  - It follows LEAK-17 and SPLIT-24: the look-ups are keyed on the registered domain, so grouping by host would put the same look-up values on both sides.
  - No past case decides how hosting platforms such as blogspot.com group, so the decision is new but consistent with these rules.
- **Split, leaf L-FORCED.groups (`ForcedGroupedFromTemporal`):**
  - It follows the tree. It also follows website_phishing, where Andrej (2026-11-18) kept the forced tag and did not decline the risk of temporal leakage, in the same adversarial domain. website_phishing went random only because it has no URLs to group by.
  - If the curator declines that risk here, it departs from website_phishing. That would need a fact that sets this dataset apart.
- **`Selection Bias` marker with a `Yes` verdict:** follows website_phishing (Lennart, 2026-10-27) and the decision item's footnote (Andrej, 2026-10-20; Lennart, 2026-10-27).
- **`nb_www` kept:** it scores 0.72 alone and dropping it costs 0.004. That fits LEAK-15's "an artefact confined to features a practical model would not rely on … kept with a note". phiusil_phishing's single rule (0.9998, `No`) and phishing_websites_vrbancic's path length (0.941) were far stronger.
- **174 surplus copies kept (distinct URLs, same features, almost all in one domain):** follows LEAK-19's hiva_agnostic case (distinct items the features can't tell apart stay), and the grouped split keeps them on one side.
- **Failure codes set to missing, and the `web_traffic` missing flag kept (0.745 alone):** the missing value means "no Alexa rank", a real fact known when the page opens. That is case 3 of the missing-indicator row in evidence.md: no fix.
- **Decision register:** none of today's flags involves this dataset or the phishing records. The one LEAK-10 flag (loan_default_prediction_imperial_college) is unrelated. No drift or third same-kind exception for the rules used here.

The two checks above (the `dns_record` crosstab and the k/n test) were run on the raw file.

</details>

<details><summary>Advocate</summary>

**Position:** ship it. Some text needs correcting, and there is one weighing call for the curator: the look-up columns under LEAK-10. If the curator reads LEAK-10 strictly, the remedy is to drop columns, and the dataset still ships.

I concede one procedural point first. The record is still at `TBD -> Yes` with no CC line, and option B of the decision item (`website_phishing`'s decision item) is unanswered (precedent-checker). The review should ask for that decision. It should not assume it.

My own checks: `dns_record` against IP hosts, and the cost of dropping the status look-ups on the shipped splits.

**1. It is a real task, and the shortcut that sank its siblings is not there (P3; LEAK-13 to LEAK-15, Must)**
- **Evidence:**
  - The best fixed rule on the URL scores ROC AUC 0.78. PhiUSIIL's rule scores 0.9998 and vrbancic's path length 0.941 (issue file; domain-practitioner).
  - The task-gamer tried every exploit it could build. None gains more than +0.0007, and across seeds the gain falls inside the noise. Row order is flat (AUC 0.501).
  - 0.06% of test rows have a copy in training.
  - The format-only model (0.900) reflects page content. The ratios are exact k/n fractions in 5,715 of 5,715 phishing rows and 5,711 of 5,715 legitimate rows (precedent-checker). That is not a recording convention that differs by class.
  - The domain practitioner would use the model: "As a component, yes."
- **Why it outranks the objection:** LEAK-13 to LEAK-15 were the only Must rules that turned down PhiUSIIL and vrbancic, and the data clears them here. The retirement of `website_phishing` is already agreed (Andrej, 2026-11-09). Without this dataset the benchmark has no phishing task.

**2. The split is right, and the open temporal risk follows precedent (P4; SPLIT-36, SPLIT-8)**
- **Evidence:**
  - Not one domain is shared between train and test in any of the 9 folds (claim-auditor).
  - The tree walk lands on `L-FORCED.groups`, the leaf the definition names (split-auditor).
  - Merging the hidden groups (campaign paths, `google.*` across suffixes) changes the score by +0.0001.
  - The IID split scores 0.995 and the grouped split 0.990, so the grouping does remove some optimism.
- **Why it outranks the objection:** for `website_phishing`, in the same adversarial domain, Andrej kept the forced-from-temporal tag and did not decline the risk (2026-11-18). Declining it here would depart from that precedent with no fact that sets this case apart. The data cannot measure time either way (`Time: Lost`), and no dated feature table exists.

**3. The LEAK-10 objection to the look-ups is weaker than it looks, and its worst case is a fix, not an exclusion (P4; LEAK-10, Must; LEAK-11)**
I concede that the current trace does not meet LEAK-10's condition as written. The Alexa-against-Yandex comparison tests only the legitimate side, and the mechanism LEAK-10 is about acts on the phishing side. But three facts cut against the leak:
- **The lag is short where it can be measured.** appspot phishing URLs created on 23 July and 3 August 2020 were looked up about one day after they appeared (column-auditor, from `domain_age` against the creation stamps). One day leaves little time for de-indexing or a suspension after the report.
- **The `dns_record` trace is mostly not a late read.**
  - 97 of the 213 phishing rows with `dns_record = 1` are bare IP hosts, where an NS query fails by design. None of the 17 legitimate rows is an IP host (my check).
  - The 116 phishing rows left are about 1% of all rows. Most sit on free dynamic-DNS domains (2waky.com, zzux.com, xxuz.com).
- **The one late read we can sign weakens the signal.** `domain_age` read later makes phishing domains look older, so it stays under LEAK-11.

**Cost of the strict reading,** measured on the shipped splits. Option b drops `google_index`, `page_rank`, `web_traffic`, `dns_record` and `whois_registered_domain`:

| Features | ROC AUC | Phish caught at 1% false alarms |
|---|---|---|
| all 81 | 0.9898 | 0.846 |
| option b (76) | 0.9817 | 0.739 |

The dataset stays well above trivial and still a real task under option b.

**Rule that settles it:** the remedy ladder (Principles, How to decide, step 5) and "a real task against a leak" (Tensions: fix the leak, keep the task). LEAK-10 is answered in the definition, by a note or by dropping columns. Either way it is no ground for exclusion.

**My recommendation:** keep the look-ups, and record the measured one-day lag as the fact that sets this case apart from distribution_transformers. In that case the changed subset was unknown. Here, on the rows that can be dated, the lag is measured and short. If the curator does not accept that fact, take option b.

**4. Takedown pages are a real problem, but a small one, and they can be fixed in place (LEAK-10, located cells; LEAK-30 tension)**
- **Concession:**
  - Of the phishing pages in dataset A, 12–16% are takedown or error pages (50 to 65 of 415), against about 1% of legitimate pages.
  - The definition's "Potential leak" note does not cover them.
- **Effect:**
  - Removing the 493 fingerprinted rows moves ROC AUC from 0.9907 to 0.9903 (column-auditor).
  - On dataset A, removing the flagged pages moves it from 0.9908 to 0.9898 (claim-auditor).
- **Mildest remedy:** blank the content features on the 493 fingerprinted rows (a guarded fingerprint list). LEAK-10's located-cells clause does this (melbourne_housing_market, zillow_prize). Widen the note and `fit_reason` to cover the blank pages, which cannot be located. The rows stay, so the dataset ships.

**5. It is worth benchmarking: high ROC AUC, but methods still separate (P6; TP-2, MET-5, MET-6, MET-10)**
- **Evidence:**
  - Untuned models score ROC AUC 0.981 (logistic regression), 0.987 (random forest) and 0.989 (LightGBM).
  - At 1% false alarms they catch 0.713, 0.723 and 0.817 of the phish (domain-practitioner).
  - The test folds hold 3,328 to 4,461 rows, each with at least 1,543 phishing rows, so every fold can be scored.
- **Rule and precedent:**
  - amex_non_iid_1m and acquire_valued_shoppers_challenge were kept with the `no_spread` flag ("a real task with a low ceiling"). This dataset does not even raise that flag.
  - `roc_auc` as the fallback follows the multi-metric precedent (gallstone_disease) and aeolus_rebuilt.
  - Switching to log loss would be a new call under MET-10 (each dataset's metric on its own). The practitioner argues against it.

**6. The selection bias is measured and does not create a shortcut (USE-8; Selection Bias marker)**
- **Evidence:**
  - No look-up tells Alexa pages from Yandex pages (ROC AUC 0.50 to 0.52).
  - Phishing separates from either list alike (0.992 and 0.993).
  - `google_index = 1` holds for 14.5% of Alexa pages and 14.9% of Yandex pages (claim-auditor).
  - The fit is already `approximate`, and the gap is named in `fit_reason`.
- **Rule:** USE-8's cases. With the marker, the verdict usually stays `Yes` when no shortcut separates the lists (Andrej, 2026-10-20; Lennart, 2026-10-27). Hard negatives are missing, but that makes the fit approximate, not invalid. The practitioner's suggestion to name the 833 pages on hosting platforms (ROC AUC about 0.90 there) in `fit_reason` costs nothing.

**7. The rest are text and cleaning fixes: cheap and safe, none changes the verdict (P5 description; P7, CLEAN-10, CLEAN-11)**
I concede all of these and would apply them:
- **Dates:** the look-ups ran in late July to early August 2020, not March to May.
- **"At most 12 per domain":** false. 40 hosts hold more than 12 pages.
- **Look-up codes:** `page_rank` 0 also means "unranked". `dns_record`, `google_index` and `whois_registered_domain` record a failed query as 1.
- **`statistical_report = 2`:** a DNS failure. Set it to missing and name it among the look-ups.
- **Ratios over an empty set:** mask them, as in medical_facility_operational_data.
- **Small errors:** `nb_www` costs 0.0004, not 0.004. `domain_age` is not a WHOIS look-up. Some feature names mislead (`ip`, `nb_subdomains`); add a note.
- **The practitioner's points:** Alexa ended in 2022, and `google_index` can only be read at crawl time. Add both to `known`.

**Rule:** "A very real task carries cleaning imperfections when they are written down" (How to decide, step 3). These are P7 problems, fixed when the fix is cheap. Under "independent failures are not conflicts", none of them is a Must failure that blocks shipping.

**Verdict I argue for:** ship after changes. LEAK-10 is settled by a note backed by the one-day lag, or by option b. The takedown rows are blanked, and the text and cleaning fixes in point 7 are applied. The curator decides the look-up call (a against b) and option B of the replacement item.

**Rebuttal**

I'm conceding critic points 1, 3 and 5, and conceding point 2 with a better remedy than either of us proposed. On point 4 I concede the procedural half and dispute the risk half. My check splits dataset A's phishing pages by page state (live, taken down or blank) and by whether the host is a shared hosting platform.

**Critic 1: look-ups kept with only a note (LEAK-10): **concede****
- **My attempt to explain the trace away failed.** I tested whether cheap hosting explains the critic's numbers. A host that suspends pages is often one that is never indexed. If that were the cause, the gap would close within each hosting type. It doesn't:

  | Phishing pages in A, own domain | n | `page_rank` = 0 | `google_index` = 1 |
  |---|---|---|---|
  | live | 170 | 0.41 | 0.84 |
  | taken down | 55 | 0.56 | 0.98 |
  | blank | 64 | 0.61 | 0.98 |

  On shared platforms, taken-down pages read `page_rank` = 0 at 0.70, against 0.11 for live pages.
- **What this means for my one-day-lag argument.** That lag was measured on 18 appspot URLs. It says nothing about the takedown rows, where the look-ups clearly moved. So the part we can trace shows a gain, LEAK-10's condition for keeping the columns with a note fails, and no fact sets this case apart from distribution_transformers.
- **What follows:** option b, which is now my recommendation and not my fallback.
  - Drop `google_index`, `page_rank`, `web_traffic`, `dns_record` and `whois_registered_domain`.
  - Keep `domain_age` and `domain_registration_length`, each with a note (LEAK-11).
  - Measured cost: ROC AUC 0.9898 → 0.9817, and phish caught at 1% false alarms 0.846 → 0.739. The task stays real and not trivial (P6). P4 outranks P6.
  - The dataset still ships.
- **One addition, on `statistical_report` = 2.** Code 2 is a failed DNS lookup, the same late read as `dns_record`. Setting it to missing keeps that signal as a missing-value flag (278 phishing rows against 28 legitimate), so a tree model uses it exactly as before. Its treatment should follow `dns_record`: if `dns_record` is dropped, code 2 must not survive as its own value or as missingness. The 0/1 list-match flag is a static blocklist, which is fine to keep.

**Critic 2: takedown content cells (LEAK-10, LEAK-6): **concede the leak; dispute the remedy****
- **A new fact against blanking, which both of us proposed.** The 493 fingerprinted rows are 482 phishing and 11 legitimate. If their content features are set to missing, the missing pattern is itself a label proxy with 98% precision. The model would learn "content missing means phishing", which is the same takedown shortcut as before.
- **Remedy:** drop those rows under USE-7.
  - The task is a filter rating a live page, and a takedown page is not an instance of that task.
  - It costs 4.3% of rows. Removing them moved ROC AUC only from 0.9907 to 0.9903 (column-auditor).
  - First check the 11 legitimate matches by hand, as the critic says. Drop only the rows confirmed as takedown pages.
  - Widen the note and `fit_reason` to cover the blank pages, which can't be located.
  - The dataset still ships.

**Critic 3: wrong dates and group sizes (P5): **concede****
This matches my point 7.
- **Dates:** the look-ups ran in late July to early August 2020. Fix this in `row`, `curation_comments`, `time_basis` and the record's `collection_period`.
- **Group sizes:** "At most 12 per domain" is wrong, since 40 hosts hold more than 12 pages. Fix the text.

**Critic 4: the forced split and the replacement decision: **concede half, dispute half****
- **Concede:** the record at `TBD -> Yes` with no CC line, and the unanswered option B of `website_phishing`'s decision item. The curator must answer both before this ships.
- **Dispute:** that the `[FORCED.risk]` question stays open with no default.
  - The split auditor and the critic agree there is no way to re-split. No dated table with both classes exists (`Time: Lost`).
  - For `website_phishing`, in the same adversarial domain, Andrej kept the forced-from-temporal tag on 2026-11-18 (SPLIT-8).
  - Nothing measured here sets this case apart, so the recommended answer is to accept the risk, tagged, following that precedent. Changing this split would not add fidelity, because the time order is lost.

**Critic 5: missing-value codes and notes (P7, CLEAN-10, CLEAN-11): **concede****
- Mask the empty-set ratios where the denominator can be located.
- Set `ratio_extRedirection` above 1 to missing.
- Correct the meanings of `page_rank`, the failed-query codes, `domain_age`, the `nb_www` cost (0.0004, not 0.004), `ip` and `nb_subdomains`.
- The Alexa and `google_index` caveats are no longer needed in `known` once those columns are dropped under option b.

**The metric**
- We agree that `roc_auc` stays the fallback.
- Its reason should add the point the critic raised: the real decision runs below 1% false alarms.
- Under option b, untuned models catch about 0.74 of phish at 1% false alarms (my measurement).

**Verdict:** ship after changes:
1. Option b for the look-ups, with `statistical_report` = 2 treated the same way as `dns_record`.
2. Drop the confirmed takedown rows; don't blank them.
3. Fix the text and the cleaning.

The curator decides option B of the replacement item and confirms the forced-split risk tag, which I recommend accepting as in the `website_phishing` precedent.

</details>

<details><summary>Critic</summary>

My position: ship it only after changes. The task is real: a filter rates a page when a user opens it, the grouped split is right, and the task gamer found nothing it could exploit. But two LEAK-10 problems (a Must rule) are kept with a note, and the rule does not allow that here. Some stated facts are also wrong. None of this calls for excluding the dataset.

**1. The seven look-ups are kept with a note, but LEAK-10's condition for that is not met (P4, LEAK-10 second clause, Must).**
- **Problem:** The look-ups were read at the crawl, after each phishing page had been reported. The rows have no dates, so the late values cannot be located row by row. LEAK-10 then says the values go when they may carry a gain. They stay with a note only when the part that can be traced shows none.
- **The builder's trace doesn't test the right side:** it compares Alexa pages with Yandex pages (0.50 to 0.52). Both are legitimate, and a report never changes a legitimate page. The mechanism (report, then takedown, de-indexing, delisting) acts only on phishing pages.
- **Evidence:** I traced the phishing side myself, on the 415 phishing pages of dataset A, using the column auditor's takedown flags joined to the look-ups:

  | Phishing pages in A | n | `page_rank` = 0 | `google_index` = 1 |
  |---|---|---|---|
  | live | 277 | 29% | 0.88 |
  | taken down | 64 | 59% | 0.98 |
  | blank | 74 | 57% | 0.97 |

  So the look-ups move with the page's state after the report. Cheap hosting may explain part of this, but the trace does not "show none".
- **The gain is real:** `google_index` alone scores 0.865 ROC AUC, and the look-ups alone 0.94 to 0.95.
- **Two more look-ups the notes miss:**
  - `statistical_report` = 2 is a failed DNS lookup made at the look-up (278 phishing rows, 28 legitimate). It is not among the "seven look-ups" the notes name.
  - `dns_record` = 1 also means a failed query. 108 of its 230 rows are IP-address hosts, so it is weaker evidence than the precedent checker gave it.
- **Precedents:** distribution_transformers_at_cauca_department dropped attributes that changed for an unknown subset of positive cases. tunisian's `CTR_CESSAT` was dropped as a status recording a later event.
- **Fair point against me:** the column auditor dated 18 appspot URLs. Their look-ups ran about 1 day after each URL appeared. That is a small, single-host subset and says nothing about the takedown rows.
- **Remedy:**
  - Drop the status look-ups a report can move: `google_index`, `page_rank`, `web_traffic`, `dns_record`, `whois_registered_domain`.
  - Set `statistical_report` = 2 to missing.
  - Keep `domain_age` (a late read weakens it, LEAK-11) and `domain_registration_length`, each with a note.
  - Cost: about 0.01 ROC AUC (builder: 0.9905 to 0.9824 without three of the five). P4 outranks P6, and the score never decides.
  - If the curator keeps them instead, that is an exception to a Must rule, which the rules do not allow. It would need a LEAK-10 amendment stated as such.

**2. Content features of taken-down pages are late cells that can be located, and the definition does not blank them (P4, LEAK-10 second clause and LEAK-6, Must).**
- **Problem:** The crawler keeps any HTTP 200 reply. So suspension, parking, takedown-warning and error pages were stored as the "phishing page".
- **Evidence:**
  - In dataset A, 65 of 415 phishing pages (15.7%) are takedown pages and 74 more are blank. Among the 585 legitimate pages, 6 are takedown pages and 30 are blank (column auditor). The claim auditor counts 50 of 415 independently.
  - The takedown templates leave fixed patterns in the content features. These patterns locate 493 rows in dataset B: 482 phishing, 11 legitimate.
  - Those rows score as easier: 0.996 to 0.998 against 0.988 for live phishing pages.
- **Effect on the task:** the model learns what a takedown page looks like, which no filter sees when a user opens a live phishing page. The effect on the score is small (0.9907 against 0.9903), but LEAK-6 says a confirmed leak goes even when small. LEAK-10 says late cells that can be located are blanked.
- **Remedy:**
  - Set the content features to missing on the rows that match the patterns, with a guarded list in `_clean`.
  - Check the 11 legitimate matches by hand first. A pattern may also catch a live minimal page.
  - Extend the "Potential leak" note and `fit_reason` to cover the blank pages, which cannot be located.
  - Dropping the rows under USE-7 is the alternative for the curator.

**3. Stated facts are wrong (P5, and USE-8's fit statement, Must for the fit text).**
- **Dates:** The dates in the `domain_age` look-ups put the legitimate look-ups at 21 to 26 July 2020 and the phishing ones into early August. Appspot URLs were created up to 3 August. `external_features.py` is dated 27 July 2020. So "crawled in March to May 2020" is wrong in `row`, `curation_comments`, `time_basis` and the record's `collection_period`.
- **Group sizes:** "At most 12 per domain" is wrong too. 40 hosts hold more than 12 pages (en.wikipedia.org holds 141).
- **Remedy:** correct the text. The data does not change.

**4. The open person-only question on the forced split, and the decision this build skips ahead of (SPLIT-8, SPLIT-32).**
- **[FORCED.risk]:** this split trains and tests on pages from the same weeks, while phishing adapts within weeks. The split auditor leaves the risk question open for a person.
- **Replacement decision:** the record is still `TBD -> Yes` with no CC line. The website_phishing decision item (option B) is unanswered, so the build is ahead of the curator's decision.
- **Remedy:** the curator answers both before this ships. I don't ask for a re-split: no dated table with both classes exists.

**5. Missing-value codes and stated meanings (P7, CLEAN-10 and CLEAN-11, Should; quality only, not a reason to exclude).**
- **Empty-set ratios:** they are coded 0 when there is nothing to take a share of: hyperlink shares on 1,381 rows, media shares on 3,874 rows. Mask them where the denominator can be located (as in medical_facility_operational_data).
- **Out-of-range values:** `ratio_extRedirection` goes above 1 on 50 rows (external media are counted twice). These become missing.
- **Notes to correct:**
  - `page_rank` 0 also means "not ranked".
  - `google_index` = 1, `dns_record` = 1 and `whois_registered_domain` = 1 also mean a failed query, so "no failed queries" is wrong.
  - `domain_age` does not come from WHOIS.
  - The `nb_www` cost is 0.0004, not 0.004.
  - `ip` and `nb_subdomains` do not measure what their names say.
- **If point 1 is not taken:** `known` should say that Alexa's rank ended in May 2022 and that `google_index` is a crawl-time scrape (domain practitioner).

I don't contest the metric: `roc_auc` stands as the fallback (MET-5, MET-6, MET-8). Its reason should add that the real decision runs below 1% false alarms, where untuned models spread from 0.71 to 0.82.

Verdict: ship after changes 1, 2 and 3, with the curator answering point 4. Point 5 is cheap cleaning that should be done, but it does not block.

**Rebuttal**

The advocate and I agree on most of this. We split on one point: whether the look-ups can stay with a note. They can't.

**Advocate 1 (a real task, no URL shortcut): concede.** The task gamer's exploits gain at most +0.0007, within the noise. The best URL rule scores 0.78. None of my points asks for exclusion.

**Advocate 2 (split and temporal risk): concede the substance, keep the procedure.**
- The grouping is right: no domain is shared across folds, and merging the hidden groups changes the score by +0.0001.
- For website_phishing, in the same domain, Andrej kept the forced tag and did not decline the risk (2026-11-18). That is a fair precedent, and I don't know of a fact that sets this case apart.
- SPLIT-8 still makes the risk a question only a person answers. The curator can answer it by citing the precedent, but the review must ask it, not assume it.
- The replacement decision (option B) is still unanswered. The advocate concedes this too.

**Advocate 3 (keep the look-ups on the strength of the one-day lag): dispute.** LEAK-10's second clause (Must) lets the look-ups stay with a note only when the traced part shows no gain. It does show one.
- **Our own data contradicts the "little time after the report" argument.** 65 of the 415 phishing pages in dataset A were already takedown pages when crawled, and 74 more were blank. For those rows the report had already acted. Their look-ups differ from those of live phishing pages:
  - `page_rank` = 0: 59% against 29%.
  - `google_index` = 1: 0.98 against 0.88.
- **The one-day lag can't stand for the rest.** It comes from 18 URLs on one shared host, appspot.com.
  - `domain_age` and `page_rank` there are read for appspot.com as a whole, so a report against one app cannot move them.
  - The stamps date the app's deployment, not its report or takedown.
  - So this subset is the one where the mechanism cannot act. It says nothing about dedicated phishing domains, which are most of the takedown rows.
- **Not set apart from distribution_transformers.** That precedent dropped attributes that changed for an unknown subset of positives. Here part of the changed subset is known, and it shows the shift. That brings this case closer to the precedent, not further away.
- **The issue file repeats the error.** It says the look-ups "were looked up once at the May 2020 crawl". The look-ups ran in late July to early August (column auditor). The case for keeping them rests on a date that was wrong.
- **`dns_record`: concede part.** 97 of its 213 phishing rows are IP-address hosts, where the query fails by design (the advocate's check). That weakens the leak evidence for this column, but 116 non-IP failures are left, and dropping the column is cheap.
- **What the rule asks for:** option b, plus `statistical_report` = 2 set to missing. The advocate's own measurement:
  - ROC AUC 0.9898 → 0.9816.
  - Phishing caught at 1% false alarms 0.846 → 0.740.
  - The task stays well above trivial. P4 outranks P6, and the score never decides.
- **If the curator keeps the look-ups anyway,** the review should record that as a departure from a Must rule, not as a case LEAK-10's note clause covers.

**Advocate 4 (takedown pages): agreed.**
- Blank the content features on the 493 fingerprinted rows, with a guarded list.
- Check the 11 legitimate matches by hand first.
- Widen the note and `fit_reason` to cover the blank pages, which cannot be located.

**Advocate 5 (worth benchmarking, metric): concede.** `roc_auc` stays. I only ask that its reason name the operating point below 1% false alarms, where untuned models catch 0.71 to 0.82 of the phish.

**Advocate 6 (selection bias): concede.** No look-up tells the two legitimate lists apart (0.50 to 0.52), so the fit is approximate, not invalid. Also name the 833 hosting-platform pages in `fit_reason`, as the advocate suggests.

**Advocate 7 (text and cleaning fixes): agreed.** These are the same items as my points 3 and 5. The date and group-size corrections (point 3) are wrong stated facts and must be fixed before shipping. The cleaning items are Should rules and don't block.

**Where we still differ:** only the look-ups. I ask for option b as the ruling under LEAK-10 (Must), not as a fallback. Everything else is common ground: ship after the takedown blanking, the text corrections and the cleaning fixes, once the curator answers option B and the forced-split risk.

</details>
