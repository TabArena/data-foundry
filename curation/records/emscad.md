---
unique_name: emscad
name: fraud_detec
checked_by:
- Lennart
- Alex
- Mustafa
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Grouped)
- Free Text (Sentences)
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Revised Later'
- 'Entities: Recur'
collections:
- TexTabBench
- TabSTAR
- MulTaBench
original_source: Other
year: '2017'
domain: business & marketing
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction
- https://www.kaggle.com/datasets/amruthjithrajvr/recruitment-scam
- Original website is down
- http://emscad.samos.aegean.gr/
- https://www.openml.org/search?type=data&id=46655&sort=runs&status=active
notebook_path: datasets/beyond_iid/new_iid/emscad/emscad.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/emscad/dataset.py
source_row: 681
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: reposts dropped and a grouped split by poster; ROC AUC 0.99 IID -> 0.94 grouped.** Vidros et al. 2017 (Future Internet 9(1):6), Sec. 5: labels come from Workable's review of the client ("client's suspicious activity on the system, false contact or company information, candidate complaints and periodic meticulous analysis of the clientele"), and "fraudsters can quickly and repeatedly try to post the same job ad in identical or different locations". Changes, all exact rules without similarity thresholds: (1) reposts dropped: rows identical in every field except job_id and location (1,343 rows after exact deduplication, 115 fraudulent; 0 of the 368 repost groups mix labels); (2) `poster_group`: ads sharing the exact non-empty company_profile (1,708 profiles, none mixes labels) or a masked e-mail/phone/URL hash that occurs within at most one company profile (generic contacts such as job-board URLs, shared by up to 87 companies, are ignored; linking through them made one group of 5,325 rows). Result: 16,116 rows, 737 fraudulent, 4,441 groups (largest 539, a legitimate recruiter; 3,208 single ads; 2 groups mix labels). LightGBM on the grouped splits: AUC 0.938 (0.903-0.953 over 6 folds), against about 0.99 random. Residual: about 335 single ads have a near-identical text (cosine >= 0.95) in another group; dropping them at 0.95-0.7 did not change the grouped AUC (0.918-0.934), so they are kept. The grouped split measures fraud detection for posters not seen before; a new ad from an already flagged client is caught by the account, not by a content model. The paper's own full-dataset evaluation (Sec. 6.4) tests on all 17,880 ads, including its 900 training ads. Also: " " and "\xa0" in text fields are now missing values.

Original source website seems down, dataset is very imbalanced, but seems like a good fit at first glance; multiple versions on Kaggle; paper describes some specific preprocessing and data filters, need to check if data is already preprocessed or if we need to do the same; very imbalanced

Also contains non-English text (at least German, didn't check yet for more); title contains a lot of information as well

CC (2026-10-14, Lennart): No ForcedIIDFromTemporal tag: the grouped split already marks the task as Non-IID. The dates are lost, though they could have been used for modelling too.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Vidros et al. 2017 report accuracy with precision, recall and F-measure on a balanced 450/450 sample, while the shipped release is 4.6% fraudulent and no threshold or costs are fixed (MET-2, MET-6).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `required_experience` (a level outside the scale is a state of its own); `required_education` (a partial order).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 columns with a state outside the scale ordered, the state placed by the rule.

**Assessment (AI, 2026-11-01):** the benchmark MulTaBench (https://arxiv.org/abs/2605.10616) carries this record's data as "Fake Job Postings": Text-tabular; EMSCAD (Vidros et al. 2017) via OpenML 46655. Paper notes no significant TAR gain here. Tagged MulTaBench on 2026-11-01.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship: a documented platform task (Vidros et al. 2017) with reposts dropped and posters held out, which removed the client-recognition leak (ROC AUC 0.99 random to 0.94 grouped). Priority 3: gap 0, use case 0, source 1, shape 1, risk -0.

CC (2026-11-10, Andrej): review page marks: ship as defined (issue 1, ok, option A). Time basis forced from temporal, grouped (issue 2, option B): `ForcedGroupedFromTemporal` in `data_tags` next to `Spatial`, its `Time basis:` bullet in place of the note on the missing dates. The CC of 2026-10-14 refused the IID forced tag for a grouped split; the grouped tag now names the lost time. Grouping by poster unchanged.

## Review

**Outcome:** added. The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a panel, from the
evidence already gathered (the record, the leak audit of 2026-09-24 and 2026-09-30, the definition's notes); no
model run exists for it. The data are EMSCAD (Vidros et al. 2017, Future Internet 9(1):6,
<https://doi.org/10.3390/fi9010006>): 16,116 job ads posted through Workable's recruiting software in 2012-2014, with
title, company profile, description, requirements, benefits, salary range and the ad's categorical fields; the
target is whether the ad is fraudulent (4.6%), as Workable labelled the posting client after reviewing its activity,
contact details and candidate complaints. Validity: a real task with a decision behind it (the platform holds back an
ad before it is published); the leak the release had is fixed: exact duplicates and reposts (identical except the id
and location, as the paper describes them) are dropped, and the split holds out whole posters (same company profile
or a poster-specific masked contact), since the label is set per client and a random split let models recognise
known clients (LightGBM ROC AUC about 0.99 on random rows, 0.938 on posters). Value: a strong but not saturated
signal on unseen posters; mostly a text task, which the benchmark embeds. Quality: about 335 lightly edited reposts
remain across groups, and dropping them at similarity thresholds 0.95 to 0.7 did not change the grouped score.
Weighed: documented source and labels +, a real platform decision +, no dates, so the test posters come from the same
2012-2014 period (approximate fit) -.

**Main points:** All settled (2026-11-10): ship as defined (issue 1, A), the grouped split tagged forced from
temporal (issue 2, B).

**Record judgment:** valid, ship. The curator's decisions of 2026-09-30 (reposts dropped, grouped by poster) and
2026-10-14 (no `ForcedIIDFromTemporal` tag, since the grouped split already marks the task as non-IID) are in the
definition. The use case follows the paper: a content classifier for ads of posters the platform has not seen, as a
known client is caught by its account. Two notes, no decision needed: the licence `CC0: Public Domain` is the Kaggle
uploader's statement (the paper states none and the EMSCAD site is down); and `salary_range_max` keeps a maximum
salary only when it is 50,000 or more, a parsed helper column next to the raw `salary_range` string. Nothing in the
record disagrees with the definition (source Other, 2017, business & marketing, grouped, binary).

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the repost leak is fixed as the source paper describes reposts, the split holds out whole posters because the labels are set per client, and the remaining near-copies across posters were tested and change nothing.
     - The ads carry no dates, so the test posters come from the same 2012-2014 period, a gap the fit states.
     - Ship as defined, or retire?
   * **Background:** Workable labelled ads "based on client's suspicious activity on the system, false contact or
     company information, candidate complaints and periodic meticulous analysis of the clientele", and "fraudsters can
     quickly and repeatedly try to post the same job ad in identical or different locations" (Vidros et al. 2017,
     Sec. 5, as quoted in the record). Reposts identical except an id or a location are dropped, as the paper did[^1a];
     a random split of the ads rewarded recognising known clients[^1b].
   * **Experiments:** the leak audit (2026-09-30), LightGBM: ROC AUC about 0.99 on random rows, 0.938 on posters
     (0.903 to 0.953 over 6 folds); dropping the about 335 ads with a near-identical text in another group (cosine
     0.95 down to 0.7) left 0.918 to 0.934. 2 of 4,441 posters (34 ads) carry both labels.
   * **Sources:** Vidros S, Kolias C, Kambourakis G, Akoglu L. Automatic detection of online recruitment frauds:
     characteristics, methods, and a public dataset. Future Internet. 2017;9(1):6.
     <https://doi.org/10.3390/fi9010006>
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 16,116 ads, 4,441 posters, grouped 3 x 3, ROC AUC | documented labels and a real platform decision; the client leak removed | no dates; mostly a text task |
     | B | Retire | record `No (Retired)`, folder removed | none found | no defect found; loses a documented fraud task |

   * **Recommendation:** A: the source documents the data and labels, and the leak it had is fixed and tested.
     **Decision:** A or B?

   [^1a]: **LEAK-21** (Should): reposts identical except an id or a location are dropped, as the source paper did;
     emscad is its case.
   [^1b]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have and
     the entity carries the label.

   **Resolved (2026-11-10, Andrej):** A, ship as defined; a CC line in the record.

2. **Time basis: name the grouped split forced from temporal (`ForcedGroupedFromTemporal`)?**

   * **Problem:**
     - Ads were posted from 2012 to 2014 and the release keeps no time: no date column, `job_id` does not follow
       posting time (a low id describes a job of 2014), and only some free texts name a year.
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, `Target: Revised Later`,
       as a client's verdict is set on all its ads after review), and the definition names no time basis, following
       Lennart's call of 2026-10-14 against the IID forced tag because the split is grouped.
     - The use case screens new ads and scams change over time, so the grouped test posters also stand in for later
       ones: name that with the grouped form of the forced tag, which a grouped definition can carry?
   * **Background:** the questions that tell the time bases apart[^2a]:
     - Can time affect the target? Yes: the definition itself notes that scams change over time.
     - Does the use case predict for a time after its data? Yes: the platform screens an ad before it is published.
     - One shared prediction moment? No: each ad at its own posting; the label is the client's verdict, revised after
       the ad by review and complaints.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: fraudsters
       and the platform's review adapt to each other; with the time lost that is the forced case[^2b].
     - The grouping by poster has its own reason, the label set per client, and stays whatever the tag; the 2026-10-14
       call answered the IID tag, which a grouped definition refuses, and builds on here: the grouped tag names the
       lost time without calling the split IID.
   * **Experiments:** the leak test across a forced split[^2b], from the audits of 2026-09-24 and 2026-09-30: a
     client's label on both sides was the leak (ROC AUC about 0.99 on random rows), removed by the grouping (0.938);
     the about 335 near-identical ads across groups leave the grouped score unchanged when dropped (0.918 to 0.934).
     Whether ads of one period share their outcome across posters (a wave of one fraud ring under several accounts)
     cannot be tested without dates.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | `data_tags = ("Spatial",)`; the curation note says why the dates are missing | the 2026-10-14 call as made | `dataset check` notes a split that is not temporal and does not say why |
     | B | Forced from temporal, grouped | the tag `ForcedGroupedFromTemporal` and a `Time basis:` line in place of the note on the missing dates | says in the metadata what the note says in prose; no fold changes | the grouping is not there because of time, so the tag reads as if it stood in for windows |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that what marks a scam does not change | none found | the definition says scams change; no dated data to measure it on |

   * **Recommendation:** B: the task looks forward and its time is lost, which the grouped forced tag names; it fits
     loosely, as the grouping answers the client, not the time. **Decision:** no time basis (A), forced grouped (B)
     or stationary relation (C)?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Spatial", "ForcedGroupedFromTemporal")` and, in
   place of the curation bullet "The ads were posted from 2012 to 2014, but the release has no dates, ...", the
   bullet "- Time basis: ForcedGroupedFromTemporal: ads posted from 2012 to 2014 with no date in the release
   (`job_id` does not follow posting time); the split groups by poster because the label is set per client, so the
   test posters come from the same period as the training ones. Scams change over time; a dated release would allow
   a split by posting date."; no other change (the `grouping` stays). The record's CC of 2026-10-14 gets a line that
   the grouped tag now names the lost time.

   [^2a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal (`ForcedGroupedFromTemporal` when it ships
     grouped), after a leak test across the split; it says what a dated release would change.

   **Resolved (2026-11-10, Andrej):** B: `data_tags = ("Spatial", "ForcedGroupedFromTemporal")` and the drafted `Time
   basis: ForcedGroupedFromTemporal:` bullet in place of the note on the missing dates; the grouping by poster stays.
   The record's CC line says the grouped tag now names the lost time.

## Reference

https://doi.org/10.3390/fi9010006
