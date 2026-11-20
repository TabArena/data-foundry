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

CC (2026-11-17, Andrej): the declared split (random, 10x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split review, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 2, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. An adversarial domain whose central feature (HTTPS) is known to have reversed its meaning; nothing supports interchangeable later samples.

## Review

**Outcome:** added. A question on `CrossSectional` (2026-11-13) was withdrawn when the prototype was dropped.

**Main points:** Nothing open: issue 1 was withdrawn on 2026-11-13.

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

## Reference

Phishing detection based Associative Classification data mining
By Neda Abdelhamid, A. Ayesh, F. Thabtah. 2014

Published in Expert systems with applications
