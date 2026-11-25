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
tags:
- 'Samples: Over Time'
- 'Time: Lost'
- Database Snapshot
original_source: UCI
year: '2016'
collection_period: Unknown
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

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 6 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `popUpWidnow`, `SSLfinal_State`, `Request_URL`, `URL_of_Anchor`, `web_traffic`, `URL_Length` (the README lists their levels); left unordered: `SFH` (low confidence).

CC (2026-10-31, Lennart): marks on the review board of PR #37: SFH ordered with the suspicious 0 in the middle; which end is phishy noted from the features alone (no label).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `web_page_phishing_detection` (TBD -> Yes, priority 2), `phishing_websites_vrbancic` (TBD -> 2nd Tier, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 2, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. An adversarial domain whose central feature (HTTPS) is known to have reversed its meaning; nothing supports interchangeable later samples.

## Review

**Outcome:** added. A question on `CrossSectional` (2026-11-13) was withdrawn when the prototype was dropped.

**Main points:** Better-data check (2026-11-25, issue 5): Replace it with web_page_phishing_detection (Hannousse and Yahiouche 2021), split grouped by registered domain: the check left open on 2026-11-09 passes, since its URL-only features separate the classes far less than PhiUSIIL's (best fixed rule on the URL 0.78 ROC AUC, against 0.9998), and the task still separates methods (LightGBM 0.989 against logistic regression 0.980). Earlier: Nothing open: issue 1 was withdrawn on 2026-11-13. Issue 2 resolved on 2026-11-18: `ForcedIIDFromTemporal` stays, not `AssumedStationaryRelation`.

**Issues for Andrej:**

1. **`CrossSectional` instead of `ForcedIIDFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedIIDFromTemporal`, a forward use case whose time was lost[^fo-1].
     - The target is a present state measured with the features: whether the page is a phishing page, read from the page as it stands, and the use case reads it for new units at their own present[^cs-1].
     - The tag alone changes: the split stays random.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedIIDFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-1]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

2. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: No date or URL in the file and its order interleaves the classes (Time: Lost); the UCI parent release (Mohammad et al.) has no dates either, so neither the PhishTank report dates nor the domain-age/traffic look-up dates can be recovered.
     - Use: A browser filter rates sites made after the collection (period not stated, data from about 2012-2014, released 2016), years later in any use today.
     - Mechanism: The features are page and URL signals (SSL state, anchors, request URLs, domain age, traffic) that phishers choose; an adversary changes them in response to filters, so the relation moves with the period.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | APWG Phishing Activity Trends Reports (apwg.org), 2016-2021 | share of phishing sites served over HTTPS | not flat: from a few percent around 2016 to over 80% by 2021 | SSLfinal_State is a feature of this dataset; the same adversary population |
     | splits.md SPLIT-32 sample facts (literature, cited from memory: check) | (stated, not measured) phishing pages and malware change with their year | not flat (asserted) | same domain |

   * **For a stationary use case:**
     - Signals are read from the page as it stands at the visit, no label delay.
   * **Against:**
     - Opponents who adapt: phishers change URL, SSL and page tricks in response to filters.
     - The HTTPS signal the features rely on was inverted in meaning within a few years (APWG).
     - Classes come from two separately collected lists (Selection Bias marker), with collection dates unknown.
     - An old one-time collection used today is a span of a decade in a fast-moving domain.
   * **Earlier views:**
     - Resolved (2026-11-13, Andrej): CrossSectional withdrawn, the ForcedIIDFromTemporal tag stays.
     - CC (2026-11-17, Andrej): blind split walk reaches the shipped random split with ForcedIIDFromTemporal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | Opponents who adapt: phishers change URL, SSL and page tricks in response to filters.; The HTTPS signal the features rely on was inverted in meaning within a few years (APWG). |

   * **Recommendation:** A, an adversarial domain whose central feature (HTTPS) is known to have reversed its meaning; nothing supports interchangeable later samples. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (An adversarial domain whose central feature (HTTPS) is known to have reversed its meaning; nothing supports interchangeable later samples.)

5. **Replace the retired website_phishing by web_page_phishing_detection (Hannousse), UCI 327, PILWD, or nothing?**

   * **Problem:**
     - The open check is done: on Hannousse's 11,430 pages the best rule on URL features alone scores ROC AUC 0.72 (one split) and 0.78 (two splits), against 0.9998 for PhiUSIIL's fixed rule and 0.94 for the path length of phishing_websites_vrbancic, so its URLs carry no form artefact of that kind.
     - Retirement of website_phishing is agreed (Andrej, 2026-11-09), and the candidates are the same as on 2026-11-09; the short search found two newer dated releases (PhreshPhish 2024-2025, CompPhish 2024-2025), neither a usable table today.
     - Replace it with Hannousse (a), UCI 327 (b), PILWD (c), or nothing (d)?
   * **Background:** "v0.2-page issue N" is the issue's number on the BeyondArena v0.2 review page; those parked issues were never written into this record, whose own issue numbers differ. website_phishing in v0.2: 1,250 sites, nine signals coded -1/0/1, binary, random split tagged forced from temporal (v0.2-page issues 2 and 3, settled); its codebook is contradicted by the data (v0.2-page issue 1), which is why it is retired. v0.2-page issue 4 (keep the repeated sites, "if kept") becomes moot once it is retired and closes with it. The candidates (counts checked on the files on 2026-11-09 and today where marked; the rest from data cards and papers):

     | Candidate | Rows | What it adds | Split it allows | Access, licence | Concerns | Verdict |
     |---|---|---|---|---|---|---|
     | web_page_phishing_detection (Hannousse and Yahiouche 2021, Mendeley v3, `dataset_B_05_2020.csv`) (checked) | 11,430 (50% phishing), 87 raw features | 9x the sites; raw values (56 URL, 24 page content, 7 external look-ups); URLs and extraction scripts; a paper | grouped by registered domain (3,971 legitimate and 2,688 phishing domains, 351 rows on the largest); no date per row, one crawl in May 2020, so forced from temporal | open, CC BY 4.0 | still two lists (PhishTank and OpenPhish against Alexa top domains), so Selection Bias; `www` in 67% of legitimate URLs against 21% of phishing ones | better |
     | UCI 327 (Mohammad, Thabtah and McCluskey; record phishing_url_websites) (checked 11-09) | 11,055, 30 coded signals | a codebook that holds | random only: no URLs or dates; 47% of rows repeat another | open, CC BY 4.0 | the same weaknesses as website_phishing: coded scores, two lists, no groups | not better |
     | PILWD (pilwd_134k_phishing, Sánchez-Paniagua et al. 2022) | 134,000 captures, Aug 2019 to Sep 2020 | legitimate login pages, so the lists are less apart; dates | temporal | on request to institutions, terms not stated | raw HTML, screenshots and files, no table: the 54 features would have to be rebuilt | not available |
     | phishing_websites_vrbancic (checked 11-09) | 88,647 | size | random | open | 81% of legitimate rows are bare Alexa domains; path length alone 0.94 | not better (form artefact) |
     | phiusil_phishing | 235,795 | size | random | open | a fixed rule scores 0.9998 | not better (record No) |
     | PhreshPhish (Dalton et al. 2025, huggingface.co/datasets/phreshphish/phreshphish) (new, card only) | 666,315 pages, Jul 2024 to Dec 2025 | dated rows; benign pages from browsing telemetry, not a top list; the authors' own split is temporal | temporal | open on Hugging Face, CC BY 4.0, "anti-phishing research" only | URL and HTML only, no feature table; 36.6 GB as listed | not a table today (not downloaded) |
     | CompPhish (Goenka, Mendeley 10.17632/fmbs4kp9wz.4) (new, card only) | 15,358, 70 features | collected Sep 2024 to Aug 2025, URLs and HTML | no per-row date stated | open, CC BY 4.0 | legitimate side is the DataForSEO top-1000 list, the homepage-against-phishing design behind PhiUSIIL's artefact | not checked; likely the same artefact |

   * **Effect on the task:** Hannousse keeps the task (is this page phishing, from URL, page and look-up signals) with features of the same kinds as the nine signals, as raw values instead of codes. The external look-ups are the strongest group (google_index alone 0.865): they were looked up once at the May 2020 crawl, which the forced-from-temporal tag already names. Grouping by registered domain costs 0.006 ROC AUC with all features, so the many pages per phishing domain did not inflate the random score much.
   * **Experiments:** 2026-11-25, Slurm, on `dataset_B_05_2020.csv` (the file downloaded on 2026-11-09, sha256 21093e29...); registered domain from the URL with tldextract's bundled suffix list; 5-fold x 3 repeats, ROC AUC; untuned models (depth-1 and depth-2 trees as fixed rules, logistic regression on standardised features, LightGBM defaults).

     | Features | Split | Depth-1 tree | Depth-2 tree | Logistic regression | LightGBM |
     |---|---|---|---|---|---|
     | URL only (56) | random | 0.724 | 0.802 | 0.933 | 0.971 |
     | URL only (56) | grouped by domain | 0.724 | 0.780 | 0.913 | 0.947 |
     | URL only without nb_www (55) | grouped by domain | 0.611 | 0.710 | 0.899 | 0.951 |
     | page content only (24) | grouped by domain | 0.750 | 0.792 | 0.829 | 0.914 |
     | external look-ups only (7) | grouped by domain | 0.865 | 0.917 | 0.925 | 0.946 |
     | URL + content (80) | grouped by domain | 0.750 | 0.828 | 0.947 | 0.974 |
     | all (87) | random | 0.865 | 0.924 | 0.985 | 0.995 |
     | all (87) | grouped by domain | 0.865 | 0.917 | 0.980 | 0.989 |

     The depth-2 rule on the URL reads `nb_www`, then `phish_hints` or the longest path word. URL strings by class: `www.` 67% of legitimate against 21% of phishing, no path 38% against 19%, a query 3% against 24%. Reference points: PhiUSIIL fixed rule 0.9998 (11-09), vrbancic path length 0.941 and its no-directory rule 0.891 (11-09, `vrbancic_check.log`), website_phishing one-hot logistic regression 0.978 against TabPFN-3.5 0.983 (2026-10-15).
   * **Consistency:** the same decision as the other nine in this batch: a better dataset is its own record and the old one keeps the verdict its own data earn; here that verdict is already retire (codebook contradicted), so the choice is only whether a replacement enters[^better]. Hannousse's two lists are a Selection Bias the benchmark keeps elsewhere when no shortcut separates them[^sel]; PhiUSIIL and vrbancic were turned down for a shortcut that separates the classes[^form], which Hannousse does not show.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep website_phishing as is (implemented) | no retirement, no replacement | no work | against the agreed retirement; codebook contradicted |
     | B | Replace by web_page_phishing_detection | retire website_phishing (v0.2-page issue 1, C) and build Hannousse with a split grouped by registered domain, forced from temporal, Selection Bias | open, documented, raw values, URLs and scripts; 9x the sites; no URL shortcut (best URL rule 0.78); separates methods (0.989 against 0.980) | still two lists; one crawl, no row dates; external look-ups dated to May 2020; ROC AUC near the ceiling, so log loss would separate methods better |
     | C | Replace by UCI 327 | retire, build UCI 327's 30 coded signals | codebook holds; closest to the retired task | coded scores, no URLs or dates, 47% repeats: the weaknesses of the retired file |
     | D | Replace by PILWD | request access, rebuild the paper's 54 features from raw captures | dated; legitimate login pages | request-only, terms not stated; heavy feature extraction |
     | E | No replacement | retire only | nothing to build | no phishing task in the benchmark until a dated table such as PhreshPhish is built |

   * **Recommendation:** B: the 2026-11-09 recommendation holds, and the one check it left open passes: no fixed rule on the URL comes near PhiUSIIL's shortcut, and gradient boosting still beats logistic regression on every feature group. E if two collected lists are too much on their own. **Decision:** A, B, C, D or E?

   **Notes for the AI:** on B: v0.2-page issue 1 of website_phishing closes as C (record No (Retired), Data Quality Issue, CC (<date>, Andrej): line, Andrej in checked_by, folder removed, CHANGELOG), v0.2-page issue 4 closes as moot; move web_page_phishing_detection to Yes with a CC line and run /add-dataset on Mendeley v3 `dataset_B_05_2020.csv` (doi 10.17632/c2gw7fy2j4.3): binary `status`, derive the registered domain from `url` (tldextract, public suffixes without private domains, so blogspot.com and appspot.com stay one group each), group the split by it, drop `url`; tags Samples: Over Time, Time: Lost; data_tags ForcedIIDFromTemporal with a Time basis: line (one crawl in May 2020, look-ups of that month); Selection Bias; consider log_loss as the metric since ROC AUC sits at 0.99. Note in curation the `www` asymmetry (0.72 alone) as a form difference of the two lists, kept since dropping `nb_www` changes LightGBM by 0.004. On C, build UCI 327's `Training Dataset.arff`. On D, request PILWD first. On E, v0.2-page issue 1 C only. Evidence: ~/claude_jobs/better_data_1125/work/website_phishing/ (scripts/url_check.py, scripts/domains.py, url_check_1411438.log); earlier: ~/claude_jobs/marks_1109/website_phishing/. Sources: https://data.mendeley.com/datasets/c2gw7fy2j4/3, https://arxiv.org/abs/2010.12847, https://huggingface.co/datasets/phreshphish/phreshphish, https://arxiv.org/abs/2507.10854, https://data.mendeley.com/datasets/fmbs4kp9wz/4.

   [^better]: Selection pattern "Small or dated, and the task is still done today" with PROV-4 (Must): a better dataset from another source is its own record, and the old one keeps the verdict its own data earn until the curator decides.
   [^sel]: The Selection Bias marker: rows not drawn from the population the use case predicts for; the verdict usually stays Yes (Andrej, 2026-10-20; Lennart, 2026-10-27).
   [^form]: LEAK-13 to LEAK-15 (Must): classes recorded in different forms or from different sources are checked for a shortcut that separates them, and such a dataset is not shipped.

## Reference

Phishing detection based Associative Classification data mining
By Neda Abdelhamid, A. Ayesh, F. Thabtah. 2014

Published in Expert systems with applications
