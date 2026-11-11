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

CC (2026-11-09, Andrej): the random split is tagged forced from temporal (review page issue 2, B), and the record's facts are `Samples: Over Time` and `Time: Lost` (issue 3, B). Retirement is agreed ("Of course this task should be retired"), waiting for a replacement (issue 1).

## Review

**Outcome:** added; recommended `No` (Data Quality Issue). UCI's Website Phishing data (Abdelhamid, Ayesh and Thabtah
2014): 1,250 websites, phishing ones from the PhishTank archive and legitimate ones from Yahoo and directory lists, each
described by nine page and URL signals that the donors coded -1, 0 or 1; binary since 2026-10-14 (the 103 sites the
donors rated suspicious are dropped). The AI recommends retiring it, the side Andrej took on 2026-10-15 against
Lennart's keep (issue 1). Reviewed without a panel, from the gathered evidence: the record, the experiment of 2026-10-15
for Andrej's earlier review, model runs on the shipped data and on TabArena's copy, and one cheap check.
Validity: the label is the list a site came from (`Selection Bias`, marked); the codebook and the data disagree: under
the documented coding one of the nine signals points the documented way, with the label read the other way round eight
do, and eight then match the sibling file UCI 327 of the same group, so either the target or eight signals are coded the
reverse of the documentation. Value: a logistic regression on the one-hot codes scores ROC AUC 0.978 against 0.983 for
TabPFN-3.5 (30 folds), 0.947 against 0.950 without duplicates. Quality: 47% of the rows repeat another row (625 distinct
patterns of nine few-level signals), which raises the score by about 0.01. Weighed: real sites from named lists (+), a
codebook the data contradicts (-), classes from two lists (-), a task that a linear model on the codes nearly solves
(-), better-documented data with the same signals (UCI 327, 11,055 sites) and a newer phishing set
(`web_page_phishing_detection`, priority 2) (-).

**Main points:** Parked (2026-11-11) on Andrej's note until it is decided whether better suited datasets replace this task: retirement is agreed, the replacement dataset (issue 1) and the repeated sites (issue 4) wait. The split tag and the record facts are settled (issues 2 and 3).

**Record judgment:** valid as a task in form (real sites, signals computed from the page, a binary label from two
lists), but not as documented: the meaning of the codes cannot be checked against the codebook. Lennart's calls stand
until the decision: binary with raw codes (2026-10-14), the popUpWidnow warning accepted (2026-10-14), `Selection Bias`
(2026-10-27), the seven three-level signals ordered with the suspicious 0 in the middle and the phishy end read from the
features alone (2026-10-31). If the dataset stays, a garbled sentence in the curation notes ("...in the order of the
source's codebook (`ORDINAL_LEVELS`)the seven three-level signals...") needs fixing, without a mark. The record has no
`domain`; the definition's `technology & internet` can be filled in without a mark.

**Issues for Andrej:**

1. **Retire website_phishing, or keep it?**

   * **Problem:**
     - The release's codebook and data disagree: under the documented coding (1 legitimate, 0 suspicious, -1 phishy, for
       the signals and the label) only `web_traffic` points the documented way, and with the label swapped eight of the
       nine do, so either the target or eight signals are stored the reverse of the documentation.
     - The label is the list a site came from, and a logistic regression on the one-hot codes comes within 0.005 ROC AUC
       of TabPFN-3.5.
     - Retire it (Andrej, 2026-10-15) or keep it (Lennart, 2026-10-14)?
   * **Background:** the sibling file UCI 327 (Mohammad, Thabtah and McCluskey; the same signal names and coding,
     11,055 sites) follows the documentation. Share of phishing sites at code 1 (documented "legitimate"), here and in
     UCI 327: `SSLfinal_State` 81% and 11%, `SFH` 89% and 21%, `URL_of_Anchor` 70% and 6%; `web_traffic` falls toward
     code 1 in both (43% and 26%). Two readings fit: the label is stored the wrong way round (then eight signals match
     UCI 327 and only `web_traffic` does not), or eight signals are (then the label matches the data page's counts, 548
     legitimate and 702 phishing, and the definition's own label-free reading of the signals). The files cannot settle
     which.
   * **Effect on the task:** the signals enter models as categories, and a label stored the wrong way round would leave
     every ranking unchanged, so the disagreement moves no score; what it removes is the check that the task is the
     one documented. A filter that codes the signals as the codebook says would meet a model trained on the reverse.
     The two lists add their own gap: the sites are not the ones a filter meets (`Selection Bias`).
   * **Experiments:** the experiment of 2026-10-15 for Andrej's review (stratified 3 folds x 10 with the shipped seed,
     ROC AUC): TabPFN-3.5 0.983, one-hot logistic regression 0.978, gradient boosting 0.976, random forest 0.973,
     logistic regression on the raw codes 0.965, a depth-3 tree 0.964; TabPFN-3.5 beats the one-hot regression on 29 of
     30 folds by 0.004. Without duplicates (663 rows): 0.950 against 0.947, 21 of 30 folds. On unseen patterns
     TabPFN-3.5 scores 0.973. The vote of the nine codes under the documented direction scores 0.087, under the
     direction read from the data 0.902. A check of 2026-11-04 on the same files measured the directions above (one of
     nine documented; eight of nine with the label swapped; eight of nine then match UCI 327). The benchmark
     spread on the shipped three-class version (log loss 0.206 best, 0.357 logistic regression on the raw codes) does
     not carry over: it includes the suspicious class, which v0.2 drops.
   * **Consistency:** Andrej retired hepatitis_c_prediction (classes from separate collections, labels that do not
     match the cited paper) and hepatitis_survival_prediction (a UCI file that differs from its published source) on
     2026-10-27; a dataset whose rows were collected apart otherwise stays, with the `Selection Bias` marker, as this
     one did on 2026-10-27[^1a]. Here the collection gap alone would be a keep; the contradicted codebook is what sets it
     apart[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | binary, raw codes, `Selection Bias`, fit approximate | real sites; no leak; TabPFN-3.5 still ahead on 29 of 30 folds | the codebook is contradicted; a linear model nearly matches; two lists |
     | B | Keep, document the reversal | marker `Data Quality Issue` added; `known` and the notes state that the target or eight signals run against the codebook, with the UCI 327 numbers | keeps a small categorical task; the doubt is written down | the benchmark ships a task whose meaning we cannot state |
     | C | Retire | record `No (Retired)`, markers `Data Quality Issue` and `Selection Bias`, folder removed | no contradicted codebook in the benchmark; better-documented phishing data exists | one categorical task fewer until a replacement is added |

   * **Recommendation:** C: the codebook is contradicted either way, the label is list membership, and a linear model
     on the codes is within 0.005 of the best; UCI 327 and `web_page_phishing_detection` carry the same task with
     documentation that holds. **Decision:** retire (C), keep and document (B), or keep as is (A)?

   **Notes for the AI:** on C, record `suggestion: No (Retired)`, add `Data Quality Issue`, a `CC (<date>, Andrej):`
   comment with the bullets above, remove the folder from the working copy, a CHANGELOG entry, and update the
   disagreement memory. On B, a `known` sentence and a curation note with the direction table, the marker, and the
   garbled note fixed. The direction check: per signal, the phishing share at each code in the v0.2 rows and in UCI
   327's `Training Dataset.arff`, the sign of the Spearman correlation with the label.

   [^1a]: The `Selection Bias` marker: the rows are not drawn from the population the use case predicts for; the
     verdict usually stays Yes (Lennart, 2026-10-27, on PR #16).
   [^1b]: **PROV-3** (Must): the data is real, not a real table someone reworked (relabelled, columns renamed, values
     replaced); **PROV-13** (Must): when a release is damaged, check whether the origin has the clean data before
     keeping the damage or retiring the dataset (no other release of these 1,353 sites is known).

   **Andrej (2026-11-09, discuss):** Of course this task should be retired. But what would we use as a replacement?

   **Answer (AI, 2026-11-09):** Replace it with `web_page_phishing_detection` (Hannousse and Yahiouche 2021)?

   * **Problem:**
     - Of the phishing records, only `web_page_phishing_detection` is open, documented and free of a class-form artefact: 11,430 URLs, 87 raw features, CC BY 4.0, a paper and the extraction scripts.
     - It ships the URLs, so it can be deduplicated and split by domain, but its label is still two lists (PhishTank and OpenPhish against pages crawled from Alexa's top domains and Yandex), so `Selection Bias` stays.
     - Add it as the replacement (a), or another option?
   * **Background** (checked on the files today):
     - **Hannousse:** no fixed rule solves it: the best single feature, `google_index`, scores ROC AUC 0.865, and the
       paper's random forest 96.6% accuracy. Only 174 rows repeat; phishing rows pile up on a few domains (351 on one),
       so the split should group by registered domain.
     - **Hannousse, time:** one collection in May 2020, no date per row, so no temporal split, as here; but the month
       is known, and the domain-age, traffic and PageRank look-ups date from it. Phishing pages change by year, so the
       split is forced from temporal[^1c].
     - **UCI 327** (Mohammad, Thabtah and McCluskey, 11,055 sites, inside `phishing_url_websites`): its codebook holds,
       but it has the same weaknesses as this one: 30 coded -1/0/1 signals, no URLs or dates, 47% of rows repeat
       another, two lists.
     - **`phishing_websites_vrbancic`** has PhiUSIIL's artefact: 81% of legitimate rows are bare Alexa domains with no
       path, against 2% of phishing ones; path length alone scores 0.941[^1d].
     - **`pilwd_134k_phishing`** has the best design (legitimate login pages, dated Aug 2019 to Sep 2020), but it is
       given only on request to institutions, as raw HTML and screenshots without a table: not shippable.
     - `phiusil_phishing` is `No` for the same artefact (a fixed rule scores 0.9998); `website_phishing_duplicate` is
       this file. Overlap with this dataset cannot be checked (no URLs here) and is unlikely (2020 against about 2013).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | `web_page_phishing_detection` | 11,430 URLs, 87 raw features, split grouped by registered domain, `Selection Bias` | open, documented, raw values, URLs and scripts; 9x the sites; not trivial | still two lists; one snapshot (May 2020), so no temporal split |
     | b | UCI 327 | 11,055 sites, 30 coded signals | codebook holds; same group and signals as this one | coded scores, no URLs or dates, 47% repeats: the same weaknesses as this one |
     | c | `pilwd_134k_phishing` | rebuild the paper's 54 features from raw captures | dated; legitimate login pages, so the lists are less apart | request-only, terms not stated; heavy feature extraction |
     | d | No replacement | retire only | nothing to add | no phishing task in the benchmark |

   * **Recommendation:** a: the one candidate that is open, documented, raw and free of the form artefact; its two
     lists are a `Selection Bias` we keep elsewhere. d if the two lists are too much on their own. **Decision:** a,
     b, c or d?

   **Notes for the AI:** on a, run `/add-dataset` on the `web_page_phishing_detection` record (Mendeley v3,
   `dataset_B_05_2020.csv`; drop `url` after deriving the registered domain for the grouped split) and retire
   website_phishing in the same change (issue 1, C). First check that URL-only features do not separate the classes
   the way PhiUSIIL's do. Evidence: `~/claude_jobs/marks_1109/website_phishing/` (`hannousse_check.log`,
   `vrbancic_check.log`, `uci327_check.log`; scripts in `scripts/`).

   [^1c]: **SPLIT-32** (Should): samples over time whose period moves the target, such as phishing pages that change
     with their year, get a forced split when the dates are lost.
   [^1d]: **LEAK-13** to **LEAK-15** (Must): classes recorded in different forms or from different sources are
     checked for a shortcut that separates them, and such a dataset is not shipped.

   **Deferred (2026-11-11):** parked on Andrej's note ("Park it until we decide on checking in with better suited datasets for this task.").

2. **Time basis: tag the random split as forced from temporal?**

   * **Problem:**
     - Phishing sites entered PhishTank's archive as users reported them and the legitimate ones were gathered by a script, at times the source never gives; the file holds no date or URL, so the time is lost.
     - The record says `Samples: No Time Dimension` (issue 3), and the definition splits at random and names no time basis.
     - A filter rates sites made after its training data, and phishers change their pages to get past filters, so the five questions give the forced tag[^2a].
   * **Background:**
     - Read literally, the five questions stop at the first: whether a site is phishing does not change once it is
       made, which reads as `Timeless`. That misses the adversary: what phishing pages look like moves with the
       period, and the period is what separates a filter's training sites from the sites it meets.
     - The raw file interleaves the classes: the phishing share per tenth of the file runs from 46% to 70% without a
       trend, and the nine signals show no drift along it, so the order is no time axis.
     - The leak test across the split: 47% of the rows repeat another row's nine codes; with 625 patterns of nine
       few-level codes identical rows need not be one site, the definition keeps them on purpose (its `split` text),
       and they add about 0.01 ROC AUC (issue 1). When the donors looked up domain age and traffic for the archived
       phishing sites, relative to their report, is not stated and cannot be tested.
     - If issue 1 retires the dataset, this issue closes with it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | as now | nothing to write | `dataset check` notes a split that is not temporal without a basis; the adversary's drift unstated |
     | B | Forced from temporal | `ForcedIIDFromTemporal` and a `Time basis:` line | says that later sites are the use and the dates are missing; the leak test finds only the kept repeats | none found |
     | C | Timeless | `Timeless` and its line | the label of a site does not change | hides that phishing pages change with the period, the drift a filter meets |

   * **Recommendation:** B, if the dataset stays (issue 1, A or B). **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in this working copy, on B: `data_tags = ("ForcedIIDFromTemporal",)` and in
   `curation_comments` the bullet `- Time basis: ForcedIIDFromTemporal: phishing sites reported to PhishTank and
   legitimate sites gathered from directories, at times the source does not give; a filter rates sites made later,
   and phishing pages change with the period. The file has no date or URL, and its order interleaves the classes
   (Time: Lost). Leak test across the split: 47% of the rows repeat another row's codes (kept, about 0.01 ROC AUC);
   the dates of the domain-age and traffic look-ups are unknown. Collection dates would allow a split by time.`; the
   `split` sentence names the forced split; `dataset check`.

   [^2a]: **SPLIT-32** (Should): the record's collection facts and the five questions; `Timeless` only when time
     cannot affect the target at all; samples over time whose period moves the target, with the time lost, get a
     forced split. **SPLIT-8** (Must): the closest regime, tagged as forced from temporal, after a leak test across the
     split.

   **Andrej (2026-11-11, change):** Option B: Forced from temporal.

   **Resolved (2026-11-09, Andrej):** B: the random split is tagged `ForcedIIDFromTemporal` in `data_tags`, with its
   `Time basis:` line and the `split` sentence naming it.

3. **Correct the record's collection facts?**

   * **Problem:**
     - The record carries `Samples: No Time Dimension`, the fact for designed runs or a catalogue where it plays no role when an item was measured.
     - The phishing sites were reported to PhishTank over time and phishing pages change with the period, so the samples arose over a period, and the release keeps no date of either list.
     - Set `Samples: Over Time` and `Time: Lost`, with no target fact, since the label (the list a site came from) exists with the site?
   * **Background:** UCI: "Phishing websites were collected from Phishtank data archive", "The legitimate websites
     were collected from Yahoo and starting point directories using a web script developed in PHP"; no period is
     given (https://archive.ics.uci.edu/dataset/379/website+phishing; paper 2014, donated 2016)[^3a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the record's fact (implemented) | `Samples: No Time Dimension` | no edit | states that time plays no role, which the adversary contradicts |
     | B | Correct it | `Samples: Over Time`, `Time: Lost` | the facts the source supports; fits issue 2 | none found |

   * **Recommendation:** B. **Decision:** keep (A) or correct (B)?

   **Notes for the AI:** on B, in the record's `tags` replace `'Samples: No Time Dimension'` with `'Samples: Over
   Time'` and add `'Time: Lost'`; a `CC (<date>, Andrej):` line and `Andrej` in `checked_by`.

   [^3a]: **SPLIT-32** (Should): `Samples: No Time Dimension` for designed runs or a catalogue where it plays no role
     when an item was measured; `Samples: Over Time` when the samples arose over a period, with `Time: Dated` or
     `Time: Lost`; no target fact when the target exists with the features.

   **Andrej (2026-11-11, change):** Option B: Correct it.

   **Resolved (2026-11-09, Andrej):** B: the record's `tags` carry `Samples: Over Time` and `Time: Lost`.

4. **If kept: keep the repeated sites, as distinct sites with the same nine codes?**

   * **Problem:**
     - Half of the 1,250 sites (625) repeat another site's nine codes exactly, 587 of them with the same label (the 47% the notes name), so under a random split 62% of test sites have an exact copy in training.
     - The new rules for repeats of a unit the data does not record set the verdict by three tests (is the link above chance, does the label travel with it, is there an order), and they read these as distinct sites with the same coarse signals: the natural verdict, which keeps the random split[^4a].
     - Keep the copies as now, or drop the 587 same-label copies?
   * **Experiments** (2026-11-06, the 1,250 shipped rows):
     - **Link near chance:** nine signals with two or three codes that hang together; a null that keeps each class's
       strongest links between signals (a tree of pairwise dependences, 200 draws) gives 581 repeated sites (95%
       555-608) against 625 observed, and as many identical pairs (1,602, 95% 1,409-1,865, against 1,587): an excess
       of 44 repeated sites (8%), with no excess in pairs. Shuffling each column within its class, which breaks the
       links, gives 364.
     - **The label does not travel:** copies share the label in 95.1% of pairs, against 94.5% that their codes
       predict, 92.9% for sites one code apart and 51% from the class shares; 38 of the 268 groups of identical sites
       hold both labels (110 sites).
     - **No order:** no date or URL, and the file interleaves the classes without a trend (issue 2).
     - **Overlap:** random 3-fold splits (20 repeats): 62.5% of test sites have an exact copy in training, and the
       copies' majority label is right for 92.4% of them. The copies are worth about 0.01 ROC AUC: TabPFN-3.5 scores
       0.973 on test sites whose pattern is not in training, 0.983 on all (issue 1).
   * **Consistency:** follows ai4d_lab_tanzania_tourism_classification_challenge, which keeps 965 exact copies of
     coarse survey answers as distinct respondents[^4b]; the 38 groups with both labels are an ambiguity of nine
     coarse signals that the task has[^4c]. The definition already keeps the copies on purpose (its `split` text).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | 1,250 sites, random split; the notes gain the verdict and the 62% overlap | the copies are distinct sites with the same signals, as a filter meets them; they occur about as often as the signals' links predict | most test sites have a look-alike in training, worth about 0.01 ROC AUC |
     | B | Drop the same-label copies | 663 sites (349 of 702 phishing and 238 of 548 legitimate dropped); phishing 56.2% to 53.2% | no identical row with one label on both sides | drops 47% of real sites on a link the tests find near chance; each pattern then counts once, whatever its frequency among sites |

   * **Recommendation:** A, if issue 1 keeps the dataset: the copies are about as frequent as the signals' own links
     predict and share the label only as often as their codes predict, so they are distinct sites. **Decision:** keep
     (A) or drop the copies (B)?

   **Notes for the AI:** on A, once PR #62 is in, replace the bullet "Anomaly: about half the rows are exact
   duplicates (47% of the 1,250 rows)." with "- Entity leakage, natural (2026-11-06): 625 of 1,250 sites repeat
   another's nine codes (587 with the same label); a null keeping the signals' links gives about as many (581, 95%
   555-608) and as many identical pairs, copies share the label as often as their codes predict (95.1% against
   94.5%), and the file has no order, so they are distinct sites with the same coarse signals. Under random 3-fold
   splits 62% of test sites have an exact copy in training, worth about 0.01 ROC AUC."; no data change, no rebuild;
   the `Time basis:` line of issue 2 can refer to it. On B, `drop_duplicates()` in `_clean`, `row`, `split`, `changes`
   and the notes updated, a `CC (<date>, Andrej):` line in the record. Evidence:
   `~/claude_jobs/entity_review/website_phishing/` (`dupcheck.log`, `structure_null.log`, `drop_effect.log`; scripts
   one level up).

   [^4a]: **LEAK-41** (Must, draft PR #62): repeats of a unit the data does not record get one verdict; natural when
     the look-alikes are distinct units: the random split stays and the notes give the share of test rows with a
     look-alike in training. **LEAK-42** (Should, draft PR #62): three tests set the verdict: matches against a chance
     rate that keeps the data's structure, label agreement against what the shared features predict, and an order.
   [^4b]: **LEAK-18** (Should): few features and plausible repeats are natural: keep them and say so
     (ai4d_lab_tanzania_tourism_classification_challenge, Lennart, 2026-11-05: 17 of 19 inputs coarse survey
     answers, copies kept).
   [^4c]: **LEAK-20** (Should): feature vectors that occur with both labels are dropped, unless they are genuine
     label ambiguity the task has.

   **Deferred (2026-11-11):** parked on Andrej's note ("Park it until we decide on checking in with better suited datasets for this task.").

## Reference

Phishing detection based Associative Classification data mining
By Neda Abdelhamid, A. Ayesh, F. Thabtah. 2014

Published in Expert systems with applications
