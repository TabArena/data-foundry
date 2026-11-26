---
unique_name: phreshphish_phishing_pages
name: 'PhreshPhish: phishing and benign web pages with collection dates (Hugging Face)'
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 3
decision_markers:
- Selection Bias
- Class-dependent Recording
tags:
- AI-Filled (Verify)
- Dated Event Log
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
- 'Target: Varying Delay'
original_source: Other
year: '2025'
collection_period: Jul 2024 - Dec 2025
domain: technology & internet
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Other
source_links:
- https://huggingface.co/datasets/phreshphish/phreshphish
- https://arxiv.org/abs/2507.10854
v2_path: datasets/_dev/tabarena-v0pt2/phreshphish_phishing_pages/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 3: the one open phishing set found whose pages of both classes carry the same collection date (666,315 pages, July 2024 to December 2025, benign pages from browsing telemetry rather than a top list), and no fixed URL rule separates the classes; it ships URL and HTML only, so the feature table is ours, and two class-dependent recording conventions must be removed first.
- Source: Dalton et al., "PhreshPhish: A Real-World, High-Quality, Large-Scale Phishing Website Dataset and Benchmark" (arXiv 2507.10854, 2025), Hugging Face `phreshphish/phreshphish` (v1.0.0 2025-05-14; v1.0.1 2026-02-07 "Added ~200k new samples collected between March and December 2025, improved temporal consistency by downsampling some earlier samples"). As published, measured on the URL, label and date of all rows today: 666,315 pages (368,989 benign, 298,326 phishing), fields `sha256`, `url`, `html`, `label` (benign or phish), `target` (impersonated brand, phishing only), `date` (collection day, 2024-07-02 to 2025-12-16), `lang`, `lang_score`; 77 parquet files, 36.6 GB compressed (about 193 GB of HTML); a train split (498,255, to 2025-09-08) and a test split (168,060, 2025-09-08 to 2025-12-16). No feature table.
- Use case: a browser plug-in or web filter decides, when a page is opened, whether to warn or block (the paper: "browser plugins serving as a convenient option for verifying websites", detection "within a few hundred milliseconds", so no host-based look-ups); fit direct: the benign side is pages real users visited ("anonymized browsing telemetry from over six million global Webroot users and Google search results for heavily targeted brands"), the phishing side pages reported to PhishTank, the APWG eCrime eXchange and NetCraft, both rendered by the same Selenium and Chrome crawler. Collection `Samples: Over Time`, `Time: Dated` (`date` on every row of both classes), `Target: Varying Delay` (a phishing label is a feed report, made after the page went live; pages scraped "within minutes of being reported"), `Entities: Recur` (registered domains repeat: wikipedia.org 15,308 benign rows; gitbook.io, webflow.io, pages.dev 15,475 to 19,872 phishing rows each; measured): time lives in `date`. Type `Dated Event Log` (each row one page seen on its day).
- Split: leaf [L-ORDER.windows] Temporal · windows on the time key because [LOG.meets] cases after the data (pages a filter meets next) → [ORDER.order] yes, `date` recorded for both classes → [ORDER.windows] yes over the months where both classes were collected: measured today, no benign page from November 2024 to May 2025 (and none in May 2025 at all), 147 benign rows in July 2024 and benign only in December 2025 (1,017 rows), so the months with both classes are 2024-08 to 2024-10 and 2025-06 to 2025-11 (547,483 rows); monthly windows 2025-08 to 2025-11 keep 57% to 96% for training. Open: the window length and refit cadence (the source is silent; a person signs off), and the source's own split (one temporal cut on 2025-09-08, test pages that were near-duplicates of a training page removed by TF-IDF cosine with LSH, Sec. 4.1) gives one window, not three.
- Siblings and duplicates: `web_page_phishing_detection` (Hannousse; `TBD -> Yes`, built, forced split grouped by domain, no dates); `website_phishing` (`Yes`, retirement agreed 2026-11-09; this record answers its Review issue 10, B); `phiusil_phishing` (`No`, a fixed rule scores 0.9998); `phishing_websites_vrbancic`, `phishing_url_websites`, `pilwd_134k_phishing` (`TBD -> 2nd Tier`); `website_phishing_duplicate`. Each another source (PROV-4), no duplicate. External collections: none of our vocabulary.
- Better data: found as better data for `website_phishing` (its Review issue 10; next to `web_page_phishing_detection`). Nothing better found: the search for that issue (2026-11-25) checked CompPhish (no date per row, top-1000 homepages), PhishVN (dates mean different events per class), URL-Phish (no dates), PILWD-134K (on request only), PhiShark2026 (no hosting found), the PhishTank and OpenPhish feeds and a phishing lifespan crawl (no legitimate class).
- Papers and pages: the data card; the paper (arXiv HTML, Sec. 2.3, 3, 4.1, 5.1, Appendix A read; Appendix C truncated); the card's benchmarks: 975 subsets of the test split at phishing base rates 0.05% to 5%, "evaluate on every benchmark in that folder and report the mean with a 95% bootstrap confidence interval".
- Metric: the paper "adopt[s] average precision and precision@recall=R as key performance metrics" (Sec. 5.1 and Conclusion), both reported side by side, at the card's fixed low base rates; two metrics and no one deliberate choice, and AP depends on the base rate, which runs from 15% to 100% phishing by month here, so the fallback `roc_auc` (MET-5, MET-9); inputs none.
- Risks for /add-dataset (measured today on the URLs, dates and 7 of 77 HTML files, 64,492 pages): query strings stripped from benign URLs (68 of 368,989 benign rows have one, against 11.7% of phishing rows; the paper, Appendix A.2: query parameters "are therefore removed from the URL"), so the query is stripped from every URL (LEAK-13); the HTML capture format changed by class over time (a leading DOCTYPE on 80% of phishing pages from October 2025, on benign pages only in December 2025; the format probes score 0.926 ROC AUC at random but 0.325 forward), so no feature from the capture format, raw length or line count (LEAK-13); whether the tag counts of phishing pages also moved in October 2025 (median links per phishing page 7 to 20 in June to September, 4 after); the feature table is built by us (URL lexical, HTML tag counts) and needs the 36.6 GB download; the class share by month runs from 15% to 100% phishing (the collection, not the world), so the date must not become a feature; registered domains recur across any cut (SPLIT-13, LEAK-42: 34% to 51% of phishing and about 70% of benign test rows by month sit on a registered domain seen in training, mostly hosting platforms; exact query-stripped URLs across a cut 0.02% to 0.55%); the card asks for "anti-phishing research" only (CC BY 4.0).
- Baselines (measured today, ROC AUC): depth-2 tree on the URL 0.77 to 0.85 (no fixed-rule shortcut); URL-only LightGBM 0.946 by month (2025-08 to 2025-11) against 0.979 at random; URL plus HTML tag counts 0.974 against 0.992 on the HTML sample.
- Priority: gap 0 (technology & internet 7 accepted, binary and temporal not thin; it would be the benchmark's only dated phishing task), use case + (the paper names the browser plug-in and real-time detection; benign pages from real browsing), source + (paper, data card, versioned release), shape + (666,315 pages, dated, URL and HTML), risk - (two class-dependent conventions to remove, a 7-month benign gap, a feature table we build from 36.6 GB).
- Corrected or set from the record as created: links (arXiv paper added), `year` 2025, `collection_period` Jul 2024 - Dec 2025, the collection facts and type, `domain`, `problem_type`, `required_split`, `original_source` Other, `original_data_state` Other (URL and raw HTML, no table).

CC (2026-11-25, Andrej): add PhreshPhish as a dated phishing task (website_phishing's Review issue 10, B: next to web_page_phishing_detection); to be screened and added.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: LEAK-42 / SPLIT-15 (whether the source's pruning of 8-30 September breaks a Must; settled by ending the data on 2025-09-07, the window layout after the cut is H), MET-1 / MET-11 (`roc_auc` or the partial ROC AUC up to a 1% false-positive rate, issue 1); for the curator: issues H and 1-3. Priority 3: gap 0, use case 0, source +, shape +, risk 0 (use case: the paper names the browser plug-in, but the fit is now approximate; risk: the class-dependent recordings are removed and no open issue raises a leak).

**Assessment (AI, 2026-11-25):** the panel's changes applied to the definition: the data end on 2025-09-07, before the source's test split, from which the source removed pages close to a training page (exact HTML repeats among September phishing pages 9.0% before the 8th, 0.4% after; 32,255 pages dropped); one floor of 10,000 characters of HTML for both classes (the release kept benign pages from 10,000 and phishing pages from 1,000 or 5,000; 24,429 pages dropped, 23,855 phishing); the URL written with the host in lower case, without a default port and without `&`, `,`, `+`, `;`, `=` and non-ASCII characters (stored for phishing URLs only); three four-week windows with a one-day gap (16 June to 7 September 2025); fit `approximate`; a protocol line against reading other test rows; the metric's original (average precision, Sec. 5.1) and reason; six 0/1 flags as categories; `title_length` over 1,000 set to missing. Frame 348,287 pages (72,759 phishing). Task probe: random forest 0.967, LightGBM 0.964, linear 0.927, the URL text alone 0.896, no flag; `dataset check` 0 errors, 4 warnings (none accepted). Markers `Selection Bias` (classes collected apart, as on website_phishing and web_page_phishing_detection) and `Class-dependent Recording` (the marker stays once the artefact is fixed).

**Assessment (AI, 2026-11-25):** corrections to today's screening block above, which predates the capture test (the block itself stays as written): its Split line names monthly windows 2025-08 to 2025-11 over the months with both classes to November 2025 (547,483 rows); October and November 2025 were then dropped for the changed HTML capture, and the data now end on 2025-09-07, so the windows are three four-week windows from 16 June to 7 September 2025 with a one-day gap. The release holds 367,989 benign pages, not 368,989. In the kept data the phishing share runs 12% to 50% by month, not 15% to 100%. The fit is approximate, not direct (the URL is cut down, the features are ours, the class mix follows the collection). The paper's metrics are argued from the cost of a false positive, not reported side by side without a choice; the fallback stands on the base rates (0.05% to 5% in the source, 13.5% to 38.0% in our windows). Two more class-dependent recordings were found: a minimum page size kept for benign pages only, and URL characters stored for phishing pages only.

CC (2026-11-26, Andrej): the declared horizon (four weeks, a one-day gap, windows starting 2025-08-11, 2025-07-14 and 2025-06-16) is checked, as implemented (A): the source names no refit cadence, so a four-week refit is assumed, close to a monthly one; the one-day gap is the time a refit takes to build, since a phishing label is its feed report made minutes before the crawl; the data end on 2025-09-07, before the source's pruned test split. The three warnings that follow from it (3 windows against 9, the gap on a date that dates the label, 2024-10-31 with phishing pages only) are accepted.

CC (2026-11-26, Andrej): issue 2, as implemented (A): the canonical URL stays a text input, the filter's own input and not an id; its identifier warning is accepted.

**Assessment (AI, 2026-11-26):** the horizon and issue 2 applied: `accepted_check_warnings` takes `dataset_identifier_column`, `splits_below_target`, `task_label_time_gap` and `dataset_pure_feature_value` with their reasons and the date. Windows as declared: 11 August, 14 July and 16 June 2025, 50,120, 35,257 and 42,194 test pages (9,899, 13,397 and 5,701 phishing), trained on 85.5%, 74.8% and 63.3% of 348,287 rows. `dataset check`: 0 errors, 0 warnings, 4 accepted. Open, with answers in the review: the metric (issue 1; average precision reweighted to 1% phishing equals the mean of the source's kind of subsets to within 0.005 and is independent of our windows' 13.5% to 38.0% share, but needs a new registry entry) and the brand feature (issue 3; a listed brand in the title on another host marks 1.4% to 1.5% of benign and 17% to 36% of phishing pages and lifts untuned LightGBM by +0.002 to +0.028 ROC AUC).

## Review

**Outcome:** added; the AI recommends shipping. Task: PhreshPhish v1.0.1 (Dalton et al. 2025, Hugging Face, CC BY 4.0) as a dated phishing task, 348,287 web pages of August to October 2024 and 1 June to 7 September 2025, 21% phishing, each read from its URL and HTML as 50 counts of ours, the page's language and the URL as text, scored by ROC AUC in three four-week windows (16 June to 7 September 2025) with a one-day gap. Validity: the release recorded the two classes differently in four ways, and each is now removed for both classes: the URL's form (query, scheme, host case, default port, some characters); the copies (one row per URL); the HTML capture form of October and November 2025 (dropped); and a minimum page size (10,000 characters, now applied to both classes). The data end on 7 September 2025, the last day before the source's own test split, from which the source removed pages that repeat earlier ones; the date orders the split and is no input. Applied after the panel: that end date, the size floor, the URL fixes, the one-day gap, fit `approximate`, the `Selection Bias` and `Class-dependent Recording` markers, a protocol line against reading other test rows, the metric's reason and original, six 0/1 flags as categories and corrected numbers. Value: in the task probe on the new windows, untuned models score ROC AUC 0.967 (random forest) and 0.964 (LightGBM), a linear model 0.927, the URL text alone 0.896 and a depth-2 tree 0.809; no flag. Decided 2026-11-26: the horizon (three four-week windows with a one-day gap, as implemented) and the URL as a text input (issue 2, A); the four warnings they bring (`url` one value per row; 3 windows against 9, the gap on a date that dates the label, a day with phishing pages only) are accepted. `dataset check`: 0 errors, 0 warnings, 4 accepted.

**Main points:** Open: the metric (issue 1): ROC AUC, the partial ROC AUC up to a 1% false-positive rate, or, closest to the source, its average precision at a fixed 1% phishing rate (needs a new registry entry); and the brand feature (issue 3). The hand list's gain is one brand of the test windows' campaigns (Robinhood), and lists fixed before the windows add little. The AI recommends the page title as a text column, encoded on each training side.

**Horizon:**

* **Verdict:** keep three four-week windows with a one-day gap, the newest ending on 7 September 2025 (high confidence on the end date, medium on the length, which no source gives).
* **Length:** the source names no refit cadence, so a vendor refitting every four weeks and scoring the next four weeks' pages is our assumption; the domain practitioner pushes "a new model about once a month". Four weeks replace the calendar months the panel reviewed, because the data now end on 7 September, and the windows walk back from there in equal steps[^h1].
* **Gap:**
  - One day, the time it takes to build the refit before using it, as decided on fugaku_hpc_job_failure_1m and ga_merchandise_store_sessions; the label itself needs none, since a phishing page is crawled "within minutes of being reported" (Sec. 3.1)[^h2].
  - In A it costs at most 0.7 points of training share (0.10, 0.71 and 0.03 points, newest window first).
* **Time frame:**
  - The data end on 7 September 2025, the last day of the source's train split. From 8 September the release holds its test split, from which the source removed pages close to a training page; the earlier months keep the reused phishing kits a filter meets again. So the newest window would mix two populations[^h3]:

    | Phishing pages | July 2025 | August 2025 | 1-7 September | 8-30 September |
    |---|---|---|---|---|
    | tag signature seen before the period | 21.2% | 28.0% | 32.2% | 3.7% |
    | exact HTML seen in training | 4.7% (8-31 July) | 6.8% (8-31 August) | 9.0% | 0.4% |

  - October and November 2025 are out for the changed HTML capture, and the months with few or no benign pages (July 2024, November 2024 to May 2025, December 2025) for the class mix. Training holds August to October 2024 and every 2025 day before the gap.
  - The oldest window, 16 June to 13 July 2025, trains on 2024 and 3,401 pages of 1 to 14 June 2025: close to the June window the definition rejected for training on 2024 alone, after 7.5 months without benign pages. The mediator raised this; the rest of the panel had backed the four-week windows without it.
* **Options:** shares and sizes measured on the frame as now defined (348,287 pages, size floor and end date applied, one-day gap); the two-week and weekly windows are those of 2025, all of which keep more than half the rows in training:

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | Four weeks, one-day gap (implemented) | Tests 11 August to 7 September, 14 July to 10 August and 16 June to 13 July 2025 | 3, of 50,120 / 35,257 / 42,194 pages (9,899 / 13,397 / 5,701 phishing); train 85.5% / 74.8% / 63.3% | one window length; the newest window, the deployment period, holds 50,120 pages | the oldest window trains on 3,401 pages of 2025 and 217,199 of 2024; four weeks are assumed; 3 windows against a target of 9 |
  | B | Calendar months, the last one short | Tests 1-7 September, August and July 2025 | 3, of 10,941 / 53,556 / 55,987 pages (2,427 / 12,190 / 11,355 phishing); train 96.8% / 80.8% / 64.6% | keeps the monthly refit first assumed; the oldest window trains on 7,853 pages of June 2025 | the newest window is one week of 10,941 pages; windows of unequal length |
  | C | Two weeks, one-day gap | Seven windows, 2 June to 7 September 2025 | 7, of 3,517 to 37,858 pages (823 to 8,079 phishing, 8% to 61%); train 62.4% to 93.8% | closer to the target of 9 | the refit is shortened to reach the count; window sizes and class shares swing |
  | D | One week, one-day gap | Fourteen weeks, 2 June to 7 September 2025 | 14, of 105 to 19,408 pages; two weeks (2-8 June, 21-27 July) hold no benign page and cannot be scored; train 62.4% to 96.8% | 12 scorable windows, above the target | a weekly refit is assumed; two windows unscorable, the rest noisy |

* **Recommendation:** A: three windows of one length, and the deployment period gets 50,120 pages rather than one week. The oldest window is mostly a 2024 model under A and B alike (3,401 or 7,853 pages of 2025 against 217,199 of 2024), so B buys little there; it passes where a June window did not because it trains on two weeks of the restarted collection of both classes. **Decision:** keep A, or change to B, C or D?

**Notes for the AI:** On sign-off of any option, `dataset check` warns three times, each a consequence of the horizon: `splits_below_target` (3 windows against 9; for A and B the reason in the splits comment: a fourth window trains on 2024 alone), `task_label_time_gap` (the one-day gap stands for the refit, not the label's delay) and `dataset_pure_feature_value` (2024-10-31 holds phishing pages only; the date is no input). Accept them in `accepted_check_warnings` with those reasons and the CC line. For B set `TemporalSplits(window=1, unit="months", cutoffs=("2025-09-01", "2025-08-01", "2025-07-01"), gap=1, gap_unit="days")` (the September window then holds 1 to 7 September only); for C or D `window=2` or `window=1`, `unit="weeks"`, with cutoffs walking back from 2025-09-08 while the training side keeps at least half the rows. On any change, rewrite `task_summary.split`, the splits comment (cadence, windows, shares, the count against SPLIT-15's target) and the oldest-window sentence, re-run `dataset check` and the task probe, and add the CC line.

[^h1]: **SPLIT-12** (Should): the horizon, the refit cadence, the gap and the time unit come from the use case and the source; the splits comment names each, or says the source is silent and what is assumed. The curator signs off on the horizon and the test windows of every new temporal dataset.
[^h2]: **SPLIT-10** (Should): a gap of about the label's delay; "A planning gap the use case has ... is a gap too." Cases: fugaku_hpc_job_failure_1m and ga_merchandise_store_sessions (one-day gap, applied).
[^h3]: **LEAK-42** (Must): repeats of a unit the data does not record get one verdict, natural here (reused kits kept); the source's own pruning after 8 September broke that verdict for the newest window, fixed by ending the data. **SPLIT-15** (Must for the newest window): the newest window is the deployment period, argued from statistics of the data, never a model's score. **SPLIT-14** (Must): at least 3 windows, each training on at least 50% of the rows.

**Andrej (2026-11-26, ok):** As implemented.

**Resolved (2026-11-26, Andrej):** A: three four-week test windows, 11 August to 7 September, 14 July to 10 August and 16 June to 13 July 2025 (50,120, 35,257 and 42,194 pages; 9,899, 13,397 and 5,701 phishing), each trained on every page collected at least one day before it (85.5%, 74.8% and 63.3% of the rows); the four-week refit is assumed, the one-day gap stands for building the refit. The three warnings that follow from the horizon are accepted in `accepted_check_warnings` with their reasons and the date: `splits_below_target` (3 windows against 9; a fourth window, 19 May to 15 June 2025, would hold 3,517 pages and train on 2024 alone), `task_label_time_gap` (the gap is the refit's, not the label's delay) and `dataset_pure_feature_value` (2024-10-31 holds 3,562 phishing pages only; the date is no input); the splits comment says so. The record carries the horizon's CC line. `dataset check`: 0 errors, 0 warnings, 4 accepted.

**Issues for Andrej:**

1. **Keep ROC AUC, or score the partial ROC AUC up to a 1% false-positive rate?**

   * **Problem:**
     - ROC AUC and the scores of the region a filter works in order the models differently: of four untuned models, among the three behind the best one, ROC AUC ranks the URL-only model last, while the partial ROC AUC up to a 1% false-positive rate, the true-positive rate at 0.1% and the average precision at 1% phishing all rank it first.
     - A filter sets its threshold at a false-positive rate of 1% or less, and the source argues its own metrics from the cost of a false positive.
     - The best model is the same under every score, and the metric registry has no partial ROC AUC, so a switch needs a new entry.
   * **Background:** the source scores average precision and precision at recall 0.9, because "Users ... are typically highly sensitive to false positives" (Sec. 5.1), on subsets of its test split at fixed phishing base rates of 0.05% to 5%; our test windows hold 13.5% to 38.0% phishing, so its average precision would measure something else here, and precision at recall 0.9 needs a threshold. So the definition declares the ROC AUC fallback, names average precision (Sec. 5.1) as the original, and its reason now states the reversals below[^m1].
   * **Experiments:** the domain practitioner's untuned models on the three monthly windows the panel reviewed (July to September 2025, before the changes), mean over the windows; the partial ROC AUC is the standardised one (McClish):

     | Model | ROC AUC | Partial ROC AUC, FPR ≤ 1% | True-positive rate at 0.1% FPR | Average precision at 1% phishing |
     |---|---|---|---|---|
     | LightGBM, all features | 0.960 | 0.824 | 0.534 | 0.686 |
     | LightGBM, small (50 trees, 7 leaves) | 0.919 | 0.673 | 0.224 | 0.374 |
     | LightGBM, URL only | 0.906 | 0.695 | 0.268 | 0.401 |
     | Logistic regression | 0.908 | 0.651 | 0.201 | 0.320 |

     The order flips within single windows too: in July ROC AUC orders logistic regression, small, URL-only, and the partial ROC AUC the reverse; in August and September the small model beats the URL-only one on ROC AUC and loses on the partial ROC AUC. Each window holds about 36,000 to 47,000 benign pages, so about 360 to 470 of them fall under a 1% false-positive rate (about 40 under 0.1%, too coarse).
   * **Consistency:** web_page_phishing_detection's panel asked for the same note on the operating point; the two phishing tasks should be decided alike.
   * **Panel:** the advocate would keep ROC AUC with the reversals in the reason; the critic and the domain practitioner argue that the partial ROC AUC is a matter of fidelity to the task, not of spreading the models (0.65 to 0.82 against 0.91 to 0.96); the mediator leaves it to your reading of when the task makes a metric obvious.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC, the fallback (implemented) | `roc_auc` on each window; the reason names the source's average precision, the base rates and the measured reversals | no new metric; independent of the class share, which follows the collection here; the best model is the same | weighs the whole curve while the filter works at its far left; orders the weaker models against the region that decides |
     | B | Partial ROC AUC up to 1% FPR, from context | standardised partial ROC AUC (McClish) at a false-positive rate of 1% or less, origin `context`, original average precision | scores the region where the filter sets its threshold; still independent of the class share; argued from the source's own false-positive cost | a new registry entry; a partial AUC the source did not name; about 400 benign pages per window decide it |

   * **Recommendation:** B: the filter decides at a false-positive rate of 1% or less, and there ROC AUC ranks the weaker models in reverse; decide web_page_phishing_detection the same way. A if a metric must be named by the source or the field before it replaces the fallback. **Decision:** keep A, or change to B?

   **Notes for the AI:** For B, add a `partial_roc_auc` entry to the metric registry (`src/data_foundry/v2/metrics.py`, standardised by McClish, parameter `max_fpr=0.01`; scikit-learn's `roc_auc_score(max_fpr=0.01)` gives this standardisation) with its tests, then declare `Metric.from_context("partial_roc_auc", params={"max_fpr": 0.01}, reason=...)` with the original average precision (Sec. 5.1) and the reversals in the reason; re-run `dataset check` and the task probe; put the same question on web_page_phishing_detection's review. For A, nothing changes.

   [^m1]: **MET-1** (Must): the declared metric scores the real task, the decision of the use case, the way a practitioner would have chosen a model for it. **MET-11** (Must): every metric has one origin; `context` is for a task that makes one metric obvious, and covers a source metric overruled under MET-2; the fallback when the source defines none the task would use (MET-5, MET-6, MET-9). **MET-9** (Should): average precision depends on the base rate.

   **Andrej (2026-11-26, discuss):** the source scores average precision and precision at recall 0.9, because "Users ... are typically highly sensitive to false positives" (Sec. 5.1), on subsets of its test split at fixed phishing base rates of 0.05% to 5%

   Is there a way to design a metric to get closer to the source?

   **Answer (AI, 2026-11-26):** yes: the source's average precision at a fixed phishing rate of 1%, computed on each whole window by giving the benign pages the weight that sets the phishing share to 1%; it equals the mean over the source's kind of subsets, needs one new registry entry, and is the closest we can get.

   * **Problem:**
     - Reweighted to a 1% base rate, average precision on each whole window equals the mean of 100 subsets drawn the source's way (every benign page, phishing pages drawn to 1%) to within 0.005 for both models in all three windows, without the draw's noise (one subset varies by 0.017 to 0.034). So it is the source's metric at a rate inside its range, fixed rather than set by our collection.
     - Raw average precision moves with the window's phishing share (19.8%, 38.0% and 13.5%, August, July and June windows): logistic regression scores its highest raw average precision (0.848) in the July window, where its ROC AUC is lowest (0.862) and 38% of the pages are phishing. ROC AUC does not depend on the share, and neither does average precision at a fixed rate.
     - The registry can express only ROC AUC and raw average precision. `average_precision` takes no weight, and a weight column could not carry the reweighting anyway: the weight depends on each window's class counts, and a `weight` input is also read as a training weight. Partial ROC AUC, average precision at a fixed rate and precision at a recall each need a new entry with its tests; `Metric.local` cannot ship.
     - Precision at recall 0.9 does not carry over: to reach recall 0.9 LightGBM lets through 3.9%, 33% and 3.4% of the benign pages (August, July, June), so at a 1% rate its precision is 0.19, 0.03 and 0.21, and at 0.1% it stays under 0.03.
   * **Experiments:** the shipped windows (August, July and June, newest first), LightGBM and logistic regression with fixed defaults on every feature but `url` and `date`. "Gap" is how far LightGBM leads, counted in standard deviations of that lead over 200 bootstrap draws of each test window (both classes resampled); the smallest of the three windows:

     | Metric | LightGBM | Logistic regression | LightGBM ahead in draws | Gap, smallest | In the registry |
     |---|---|---|---|---|---|
     | ROC AUC (implemented) | 0.984 / 0.919 / 0.986 | 0.886 / 0.862 / 0.942 | 100% | 35 SD | yes |
     | Partial ROC AUC, FPR ≤ 1% (McClish) | 0.821 / 0.796 / 0.841 | 0.612 / 0.668 / 0.624 | 100% | 30 SD | no |
     | Average precision, raw | 0.950 / 0.912 / 0.939 | 0.727 / 0.848 / 0.754 | 100% | 37 SD | yes |
     | Average precision at 1% phishing | 0.692 / 0.631 / 0.731 | 0.203 / 0.311 / 0.250 | 100% | 20 SD | no |
     | Average precision at 0.1% phishing | 0.377 / 0.474 / 0.438 | 0.035 / 0.074 / 0.038 | 100% | 9.5 SD | no |
     | Precision at recall 0.9, raw | 0.852 / 0.631 / 0.805 | 0.381 / 0.504 / 0.448 | 100% | 29 SD | no |
     | Precision at recall 0.9, 1% phishing | 0.191 / 0.027 / 0.210 | 0.025 / 0.016 / 0.050 | 100% | 13 SD | no |
     | Precision at recall 0.9, 0.1% phishing | 0.023 / 0.003 / 0.026 | 0.002 / 0.002 / 0.005 | 100% | 11 SD | no |

     The source's kind of subsets, 100 draws per window (mean ± SD of one draw):

     | Phishing share | Model | August | July | June |
     |---|---|---|---|---|
     | 1% | LightGBM | 0.692 ± 0.017 | 0.631 ± 0.032 | 0.731 ± 0.017 |
     | 1% | Logistic regression | 0.207 ± 0.018 | 0.316 ± 0.034 | 0.252 ± 0.017 |
     | 0.1% | LightGBM | 0.378 ± 0.074 | 0.460 ± 0.093 | 0.448 ± 0.073 |
     | 0.1% | Logistic regression | 0.044 ± 0.021 | 0.091 ± 0.041 | 0.047 ± 0.019 |

     Every candidate separates these two models in every draw: they are far apart. What differs is the spread across windows (LightGBM: partial ROC AUC 0.796 to 0.841, ROC AUC 0.919 to 0.986, average precision at 1% 0.631 to 0.731) and the noise at 0.1%, where 22 to 40 benign pages per window (0.1% of them) decide the score. The reversals among closer models are those of the earlier monthly windows above.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | ROC AUC, the fallback (implemented) | `roc_auc` on each window | no new code; does not depend on the phishing share | the source's metric only in the reason; weighs the whole curve while a filter works below 1% false positives |
     | b | Partial ROC AUC up to 1% FPR | as issue 1's B: a new `partial_roc_auc` entry, origin `context` | the steadiest across windows; does not depend on the share | a metric the source did not name |
     | c | Average precision at 1% phishing | a new entry `average_precision_at_base_rate` (param `base_rate=0.01`; the benign rows weighted n_phishing / n_benign × 99), origin `stand_in`, original average precision (Sec. 5.1) | the source's own metric at a rate in its range, equal to the mean of its kind of subsets; does not depend on our share | new code; one rate, where the source averages 0.05% to 5% |
     | d | Raw average precision | `Metric.source("average_precision")` | no new code; the source's name | measures each window's phishing share (13.5% to 38.0%), not the source's 0.05% to 5% |
     | e | Precision at recall 0.9 at 1% phishing | a new entry with `recall` and `base_rate` | the source's second metric | jumps between windows (LightGBM 0.03 to 0.21); near zero at 0.1% |

   * **Recommendation:** c: it is the source's metric at a rate the source uses, made independent of our collection's share. A mean over several rates (0.1%, 1%, 5%) is the same code with a list of rates, but the 0.1% term is three to four times noisier. b if you prefer a score of the ROC family; a if no new metric code is wanted now. **Decision:** a, b, c, d or e?

   [^m2]: **MET-11** (Must): a `stand_in` is the closest computable metric when the source's own cannot be computed on our data, with its closeness measured on the shipped splits. **MET-13** (Must): a custom metric ships in the shared metric library in the same change, tested against a reference, by hand and on 1M rows. **MET-9** (Should): average precision moves with the positive share.

   **Andrej (2026-11-26, discuss):** Two things:
   This does not affect only this dataset but is a more general observation: You seem reluctant to implementing new metrics and often list that as a con. However, the opposite behavior should be the case. A new metric that tests something different and has no close equivalent in our implemented metrics should be encouraged for benchmark diversity. Open up an across dataset issue for a potential rule change that could help with that.

   **Answer (AI, 2026-11-26):** the general point is now a cross-dataset item (the review's "Count a new metric as a gain for the collection, not as a cost"), which proposes rule wording so that a new metric's implementation counts against no option; read that way, the options above lose "no new code" as a pro of a and d and "needs a new entry" as a con of b, c and e, and the recommendation stays c, average precision at a 1% phishing rate. The note opens with "Two things" and names one; the issue stays open for the second and for the decision.

2. **Keep the canonical URL as a text input, and accept its identifier warning?**

   * **Problem:**
     - `dataset check` warns that `url` holds one value per row, as it must under the rule of one row per URL; but the text is the filter's main input, not an id: alone it scores ROC AUC 0.896, and it lifts all features from 0.958 to 0.963.
     - The blind reviewer would drop it: 62% of benign test hosts appear in training, against 4.5% of phishing hosts, so a model can learn an allowlist of hosts.
     - phiusil_phishing and drug_induced_autoimmunity_prediction kept such a string as the task's input, not as a row id.
   * **Effect on the task:** a filter does know the hosts it met before (wikipedia.org, docs.google.com, the hosting platforms phishing reuses), so the domain practitioner counts the repeats as knowledge a deployed filter has; the temporal split keeps the real mix of known and new hosts[^u1].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `url` as text (implemented) | the canonical URL ships as a string; the warning is accepted in the definition once you agree | the filter's own input; follows phiusil_phishing; the lexical counts stay too | a model can learn hosts seen in training, mostly benign ones |
     | B | Drop `url` | only the 27 lexical counts of the URL stay | no host lookup | drops the filter's main input; the counts carry only part of it |

   * **Recommendation:** A, as on phiusil_phishing: the host a filter has met before is part of its job. **Decision:** keep A, or change to B?

   **Notes for the AI:** For A, add `accepted_check_warnings = {"dataset_identifier_column": "The canonical URL is the filter's input, not an id: one value per row by the rule of one row per URL; alone it scores ROC AUC 0.896 (Andrej, <date>)."}` and a CC line in the record. For B, add `url` to `drop_columns` in `_clean`, remove it from `FeatureTypes(string=...)` and `task_summary.known`, and re-run `dataset check` and the task probe.

   [^u1]: **SPLIT-13** (Should): look for grouped structure inside a temporal task; an entity the deployed model meets again stays across the cut. Precedent: phiusil_phishing (the URL accepted as the task's input, not a row id), cited again for drug_induced_autoimmunity_prediction.

   **Andrej (2026-11-26, ok):** As implemented (A).

   **Resolved (2026-11-26, Andrej):** A: the canonical URL stays a text input, the filter's own input and not an id. `dataset.py` accepts `dataset_identifier_column` in `accepted_check_warnings` ("one value per row by the rule of one row per URL; alone it scores ROC AUC 0.896", with the date), and the curation notes' "Kept" line says the warning is accepted. CC line in the comments. `dataset check`: 0 errors, 0 warnings, 4 accepted.

3. **Add a feature for a brand named on the page while the host is not that brand's?**

   * **Problem:**
     - A page that names a brand on a host that is not the brand's is the signal phishing filters use most, and none of our 50 features encodes it: the word counts cover only login, password, verify, account and copyright.
     - The impersonated brand of the release (`target`) is a label of phishing pages only, so a brand list would have to come from elsewhere (a public list of targeted brands).
     - Not measured: whether it changes the scores.
   * **Panel:** the domain practitioner proposes it, "only if the curator treats it as representing the actor's inputs rather than lifting scores"; the mediator leaves it optional.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No brand feature (implemented) | the 50 counts as they are | no list of our choosing in the task | the filter's best-known signal is missing |
     | B | Add a brand-against-host flag | a fixed public list of targeted brands; the flag is set when the title or text names one and the host is not its domain | closer to the inputs a filter reads | one more feature of ours; the list is a choice; a new extraction over the HTML |

   * **Recommendation:** A: the feature is unmeasured and adds a brand list of our choosing; B if you see the flag as an input every filter reads. **Decision:** keep A, or change to B?

   **Notes for the AI:** For B, add the flag in `html_features` from a fixed list (named and dated in the notes), never from `target`; it re-runs `_prepare_raw_files` (about 20 minutes over the HTML); re-run `dataset check` and the leak and task probes.

   **Andrej (2026-11-26, discuss):** Try implementing B and then we can see what it would change.

   **Answer (AI, 2026-11-26):** B as one flag changes little, because a brand named anywhere in the text marks half the pages of both classes; the brand named in the title carries the signal, and with it the scores rise in every window, with no sign that it records the collection rather than phishing.

   * **Problem:**
     - A listed brand in the page's title on a host that is not the brand's marks 1.4% to 1.5% of benign pages in every month and 17% to 36% of phishing pages; in the visible text it marks 52% to 53% of benign and 48% to 60% of phishing pages (footer links: of the flagged benign pages, 78,842 name Facebook and 55,450 Google). So B's one flag (title or text) alone scores ROC AUC 0.50.
     - Added to the 50 features, B's flag lifts untuned LightGBM by +0.001 to +0.008 ROC AUC; a title flag plus a count of the off-host brands in the text lifts it by +0.002 to +0.028 ROC AUC and +0.007 to +0.040 partial ROC AUC (1% FPR), and logistic regression by up to +0.049 ROC AUC. Each of these gains is above the bootstrap SD of a single score (ROC AUC 0.0006 to 0.0015, partial ROC AUC 0.003 to 0.005; issue 1).
     - No sign of the collection: B's flag does not tell 2024 from 2025 pages within either class (ROC AUC 0.499 benign, 0.497 phishing), and the benign title rate is 1.4% to 1.5% in every month; the phishing title rate moves with the campaigns (36% in August 2024, 17% in June 2025). The one shift is in a third flag tried, a listed brand named on its own host: on phishing pages it fell from 7% to 10% in 2024 to 0.2% to 1.3% in 2025 (where phishing is hosted), and it carries 0.1% of the gain, so it is left out of the options.
   * **The list:** 59 often-impersonated brands, each with the registered names of its own hosts (Microsoft with live, office, outlook, sharepoint and others; Google with gmail, youtube, blogspot): Microsoft, Google, Apple, Facebook, Instagram, WhatsApp, Amazon, PayPal, Netflix, DHL, FedEx, USPS, LinkedIn, Adobe, Dropbox, DocuSign, WeTransfer, Yahoo, Naver, Roblox, Steam, Coinbase, Binance, MetaMask, Trezor, Ledger, Kraken, Bybit, Trust Wallet, WalletConnect, OpenSea, Robinhood, Chase, Wells Fargo, Bank of America, Citibank, American Express, HSBC, Santander, BNP Paribas, SBI, Rakuten, Kleinanzeigen, bet365, Betwinner, Spotify, Discord, Telegram, Twitter, TikTok, eBay, Walmart, AT&T, Verizon, Xfinity, the IRS, Royal Mail, Australia Post and Mercado Libre. Drawn up on 2026-11-26 from the brands the 2024-2025 phishing reports name most, never from the release's `target`. A host's registered name is the label before the public suffix (`co.uk` and the like handled). Measured against `target` only as a check: the title or text flag is set on 81% to 94% of the pages imitating Facebook, Meta, Robinhood and WhatsApp, and on none of the 3,251 imitating Booking.com, which the list lacks; filling such gaps from `target` would fit the feature to the labels.
   * **Experiments:** the shipped windows (August, July and June, newest first), the definition's frame, LightGBM and logistic regression with fixed defaults on every feature but `url` and `date`:

     | Model | Features | ROC AUC | Partial ROC AUC, FPR ≤ 1% | Average precision at 1% phishing |
     |---|---|---|---|---|
     | LightGBM | 50 as shipped | 0.984 / 0.919 / 0.986 | 0.821 / 0.796 / 0.841 | 0.692 / 0.631 / 0.731 |
     | LightGBM | + B's flag | 0.986 / 0.927 / 0.987 | 0.835 / 0.797 / 0.844 | 0.721 / 0.636 / 0.739 |
     | LightGBM | + title flag, text count (and the on-host flag) | 0.988 / 0.947 / 0.988 | 0.861 / 0.803 / 0.852 | 0.753 / 0.651 / 0.754 |
     | Logistic regression | 50 as shipped | 0.886 / 0.862 / 0.942 | 0.612 / 0.668 / 0.624 | 0.203 / 0.311 / 0.250 |
     | Logistic regression | + B's flag | 0.897 / 0.869 / 0.943 | 0.613 / 0.668 / 0.630 | 0.217 / 0.316 / 0.266 |
     | Logistic regression | + title flag, text count (and the on-host flag) | 0.929 / 0.911 / 0.948 | 0.641 / 0.679 / 0.660 | 0.289 / 0.343 / 0.322 |

     In LightGBM, B's flag ranks 9th to 10th of 53 features by gain (1.7% to 2.5% of it); the title flag ranks 6th to 8th of 55 (3.8% to 6.0%), the text count 11th to 14th, the on-host flag 46th to 47th. Share of pages flagged:

     | Month | Benign: title / title or text | Phishing: title / title or text |
     |---|---|---|
     | Aug 2024 | 1.4% / 52.5% | 36.3% / 53.7% |
     | Sep 2024 | 1.5% / 53.3% | 33.9% / 56.1% |
     | Oct 2024 | 1.4% / 53.3% | 18.9% / 50.7% |
     | Jun 2025 | 1.5% / 53.0% | 16.8% / 48.4% |
     | Jul 2025 | 1.5% / 52.0% | 24.5% / 52.1% |
     | Aug 2025 | 1.5% / 53.5% | 28.2% / 54.1% |
     | 1-7 Sep 2025 | 1.5% / 52.3% | 26.4% / 59.6% |

     Reading the brands off the 379,759 pages of the kept months is one more pass over the HTML, about 7 minutes on 15 processes.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | No brand feature (implemented) | the 50 counts as they are | no list of our choosing | misses the signal the title carries |
     | b | B's one flag | 0/1: a listed brand in the title or the text on a host not its own | one feature | the text half marks half of each class; +0.001 to +0.008 ROC AUC |
     | c | Title flag and text count | `brand_title_off_host` (0/1) and `n_brands_text_off_host` (how many listed brands the text names off their hosts), from the list above, named and dated in the notes | the title signal a filter reads; +0.002 to +0.028 ROC AUC, +0.007 to +0.040 partial ROC AUC; no sign of the collection | two features of ours; the list is ours and misses brands (Booking.com) |

   * **Recommendation:** c: the title carries the signal, filters read it, and nothing in it follows the collection; the list stays as fixed today rather than grown from `target`. a if you would rather ship no list of ours. **Decision:** a, b or c?

   **Andrej (2026-11-26, discuss):** I generally tend towards C, but I also believe that this should be designed based on either each train side of the split or a general rule like creating a list based on all brands that are always in every train part of the splits or something that is defined based on public knowledge from a clear source independent of this dataset. Think about that and assess additional options.

   **Answer (AI, 2026-11-26):** No list fixed before the windows reproduces option c's gain, because that gain is one brand, Robinhood, whose phishing campaign runs in the two newest test windows and which only the hand list names; the per-split way the framework already supports is the page title as a text column, which lifts the scores a little in every window without a list of ours.

   * **Problem:**
     - Robinhood carries c's gain. From 13 July to 7 September 2025, 4,409 phishing titles name it off its host, against 204 before 15 June and 6 benign pages in all. Without Robinhood, the hand list's LightGBM ROC AUC falls from 0.988 / 0.946 to 0.982 / 0.913 in the two newest windows, below the 50 features alone (0.984 / 0.919). Logistic regression falls from 0.929 / 0.911 to 0.892 / 0.859.
     - None of the dated public lists names Robinhood (Check Point, Cloudflare, Interbrand), and neither does the release's `target` on the rows before the earliest window (fewer than 20 pages). The hand list was drawn up on 2026-11-26 by a reviewer who had read this data, so it cannot show that it was fixed before the windows. Its gain is knowledge of the test campaigns, not a filter's input.
     - Lists fixed before the windows add little or nothing to LightGBM: ROC AUC moves by −0.012 to +0.002, partial ROC AUC by −0.003 to +0.008. They do lift logistic regression in partial ROC AUC (+0.001 to +0.045) and in average precision at 1% (+0.002 to +0.104).
     - A list rebuilt on each training side follows the campaigns. Robinhood enters the list for the newest window, and LightGBM's partial ROC AUC there rises by +0.042. But a shipped feature is a per-row column fixed before splitting, so this list cannot ship as a column. It would need a split-scoped transform fitted on the training rows. The framework has such transforms only for text columns (the `tfidf-svd` encoding), not for one built from `target`, a label-side column that the task would then have to carry for the training rows.
     - The release's `target` may be read on training rows, as a target encoding is. Using it on the rows before the earliest window (the training rows of every split, since the training sides are nested) ships as a fixed list. That list misses the brands that arrive later (Robinhood, Naver, Booking).
     - No list carries a sign of the collection: within benign pages, no title flag tells 2025 from 2024 pages (ROC AUC 0.500 to 0.503). The title as text tells them apart less well than the 50 features do (0.523 against 0.703).
   * **The lists:** each is matched as whole words (spaced or joined) in the title and the visible text. A brand's own hosts are its joined name plus the registered labels whose benign pages, on the training side the list belongs to, name it in at least half of their titles (5 pages at least). For the public lists that side is the earliest one, so the rule reads only benign rows that every split trains on. Check Point with the name alone as its own host gives nearly the same numbers.

     | List | Source and date | Size | Licence | Reproducible |
     |---|---|---|---|---|
     | Hand list (option c) | drawn up 2026-11-26 from reports, after reading this data | 59 | ours | text in the definition; not dated before the windows |
     | `target`, each training side | the release's `target` on that side's phishing rows, 20 pages at least | 94 / 75 / 53 | CC BY 4.0 (the release) | yes, from the data; differs per split |
     | `target`, earliest training side (= in every training side) | the same on rows before 15 June 2025 | 53 | CC BY 4.0 | yes; fixed |
     | Check Point | Brand Phishing Report top 10, Q1 2024 to Q1 2025 (published April 2024 to 21 April 2025), union | 17 | no data licence ("all rights reserved"); brand names are facts | quarterly pages and web archive copies |
     | Cloudflare | "The 50 most impersonated brands" (13 March 2023) | 50 | no terms stated | one dated page |
     | Interbrand | Best Global Brands 2024 (October 2024), a fame list, not a phishing one | 100 | "all rights reserved" | dated report |
     | Tranco | list YXL6G (2024-06-01), top 1,000 domains' registered labels | 846 | none stated; one input (Cloudflare Radar) is CC BY-NC 4.0 | fixed list id |

     Not usable: APWG's reports name sectors and a count of brands, not the brands; PhishTank's target field covers only phishes online now, with no dated archive; OpenPhish's terms forbid redistribution and commercial use; Kantar BrandZ publishes only its top 10.
   * **Experiments:** the shipped windows, newest first; the definition's frame; untuned LightGBM and logistic regression on every feature but `url` and `date`, plus the two features of option c built from each list (or the title's 16 `tfidf-svd` components fitted on each training side). Coverage is the share of test-window phishing pages whose release `target` is on the list (the hand list: one of its patterns matches the `target`). It is used only for this check; 87% to 94% of these pages name a brand. The flag columns give the rate on test-window pages: the title flag for benign and phishing pages, and a text count above 0 for benign and phishing pages.

     | List | Coverage | Benign title | Phishing title | Benign text | Phishing text |
     |---|---|---|---|---|---|
     | Hand list | 52% / 46% / 38% | 1.5% | 16% to 29% | 51% to 54% | 50% to 59% |
     | `target`, each training side | 76% / 43% / 50% | 1.2% to 1.8% | 12% to 37% | 52% to 59% | 42% to 68% |
     | `target`, earliest side | 23% / 27% / 50% | 1.1% to 1.3% | 11% to 24% | 52% to 53% | 36% to 55% |
     | Check Point | 14% / 12% / 20% | 1.0% to 1.1% | 7% to 12% | 48% to 51% | 33% to 43% |
     | Cloudflare | 26% / 26% / 38% | 1.0% to 1.1% | 8% to 17% | 45% | 27% to 44% |
     | Interbrand | 14% / 14% / 19% | 2.3% to 2.6% | 8% to 12% | 58% to 60% | 37% to 45% |
     | Tranco | 44% / 50% / 31% | 13% to 14% | 30% to 35% | 90% to 91% | 76% to 89% |

     | Features | LightGBM ROC AUC | LightGBM partial ROC AUC, FPR ≤ 1% | LightGBM average precision at 1% | Logistic regression ROC AUC | Logistic regression partial ROC AUC | Logistic regression average precision at 1% |
     |---|---|---|---|---|---|---|
     | 50 as shipped | 0.984 / 0.919 / 0.986 | 0.821 / 0.796 / 0.841 | 0.692 / 0.631 / 0.731 | 0.886 / 0.862 / 0.942 | 0.612 / 0.668 / 0.624 | 0.203 / 0.311 / 0.250 |
     | + hand list | 0.988 / 0.946 / 0.988 | 0.861 / 0.802 / 0.852 | 0.744 / 0.648 / 0.752 | 0.929 / 0.911 / 0.947 | 0.638 / 0.682 / 0.658 | 0.283 / 0.348 / 0.320 |
     | + hand list without Robinhood | 0.982 / 0.913 / 0.988 | 0.826 / 0.803 / 0.852 | 0.686 / 0.643 / 0.751 | 0.892 / 0.859 / 0.947 | 0.625 / 0.679 / 0.658 | 0.236 / 0.334 / 0.320 |
     | + `target`, each training side | 0.988 / 0.913 / 0.988 | 0.863 / 0.796 / 0.848 | 0.767 / 0.633 / 0.753 | 0.927 / 0.855 / 0.947 | 0.651 / 0.681 / 0.669 | 0.306 / 0.340 / 0.354 |
     | + `target`, earliest side | 0.983 / 0.907 / 0.988 | 0.826 / 0.799 / 0.848 | 0.702 / 0.637 / 0.753 | 0.891 / 0.856 / 0.947 | 0.623 / 0.683 / 0.669 | 0.233 / 0.342 / 0.354 |
     | + Check Point | 0.983 / 0.913 / 0.987 | 0.821 / 0.799 / 0.848 | 0.680 / 0.636 / 0.741 | 0.888 / 0.860 / 0.943 | 0.617 / 0.676 / 0.646 | 0.212 / 0.325 / 0.282 |
     | + Cloudflare | 0.983 / 0.913 / 0.988 | 0.821 / 0.798 / 0.843 | 0.687 / 0.632 / 0.743 | 0.890 / 0.858 / 0.946 | 0.618 / 0.678 / 0.651 | 0.223 / 0.331 / 0.309 |
     | + Interbrand | 0.984 / 0.917 / 0.988 | 0.823 / 0.802 / 0.846 | 0.693 / 0.642 / 0.741 | 0.889 / 0.863 / 0.944 | 0.614 / 0.673 / 0.641 | 0.206 / 0.328 / 0.270 |
     | + Tranco | 0.984 / 0.917 / 0.987 | 0.827 / 0.793 / 0.842 | 0.698 / 0.628 / 0.733 | 0.894 / 0.868 / 0.947 | 0.620 / 0.669 / 0.636 | 0.221 / 0.314 / 0.275 |
     | + title as text (`tfidf-svd`, each training side) | 0.986 / 0.919 / 0.987 | 0.845 / 0.798 / 0.849 | 0.737 / 0.634 / 0.746 | 0.923 / 0.870 / 0.961 | 0.651 / 0.673 / 0.697 | 0.301 / 0.362 / 0.394 |

     The bootstrap SD of a single score is 0.0006 to 0.0015 for ROC AUC and 0.003 to 0.005 for partial ROC AUC (issue 1).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | No brand feature (implemented) | the 50 counts as they are | nothing of ours to defend | the title's brand signal is missing |
     | b | Option c with a public list | c's two features from Check Point's quarterly top 10s (Q1 2024 to Q1 2025, 17 brands), named and dated in the notes | independent of the data, dated before the windows | LightGBM gains nothing (−0.006 to +0.001 ROC AUC); covers 12% to 20% of the targets |
     | c | Option c with the earliest training side's `target` | c's two features from the 53 brands with 20 or more phishing pages before 15 June 2025 (in every training side) | fixed and shippable; legitimate use of training labels | built from the label side; misses the later campaigns; LightGBM −0.012 to +0.002 ROC AUC |
     | d | Option c with a list per training side | the list rebuilt from each split's training `target` | follows the campaigns (+0.042 partial ROC AUC in the newest window) | cannot ship as a column; needs a split-scoped transform built from `target` and `target` kept for the training rows, which the framework does not have |
     | e | The page title as a text column | `title` as `string`, encoded per split by the framework's `tfidf-svd` (or `e5-small-v2`); no list | the brand words are learned from each training side; supported today; LightGBM +0.000 to +0.003 ROC AUC, +0.002 to +0.024 partial ROC AUC; logistic regression +0.008 to +0.036 ROC AUC; no sign of the collection | one more text input, which also carries words other than brands; the host comparison is left to the model (via `url`) |
     | f | Option c with this morning's hand list | as recommended this morning | the largest gain | the gain is Robinhood, which knowledge of the test windows put on the list |

   * **Recommendation:** e: it is the per-training-side design you ask for, and the framework already has it. a if you would rather not add a text input. b only if a brand flag must ship regardless, since it brings no measurable gain. f no longer. **Decision:** a, b, c, d, e or f?

**Review panel:** ship after changes (mediator). The panel reviewed the definition before these changes (monthly windows July to September 2025 on 404,979 pages); its numbers refer to that frame. Claim audit: 23 claims, 4 refuted and 2 partly refuted, all fixed (the benign count, the share of tiny pages, URL characters stripped from benign pages only, the metric's reason, and the near-duplicate verdict, false for 8-30 September). Column audit: a minimum page size the release applied to benign pages only, carried by the tag counts (fixed). Split audit: the leaf, floors and count hold; the newest window was mostly the source's pruned test split (fixed by ending the data). Domain practitioner: fit approximate; ROC AUC misses the region a filter works in (issue 1). Precedent check: two departures, no gap and no `Selection Bias` marker (both applied). Blind review: would include with changes; drop or declare `url` (issue 2). Task gamer: same-day burst counts over test rows gain up to +0.045 (protocol line). Debate: agreed on every fix; disputed: the window layout after the cut (H) and the metric (issue 1).

<details><summary>Mediator</summary>

The panel agrees on every point except two. Both of those go to the curator.

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL holds (CC BY 4.0, anti-phishing research use). USE-1 holds; USE-8 triggered, fixed (fit "approximate",
  Selection Bias marker). LEAK-10 holds (date is no input, bank_marketing). LEAK-13 triggered three times: query/scheme/
  copies/DOCTYPE months fixed by the builder; 10,000-character size floor and URL characters fixed below. LEAK-42
  triggered: the "natural, kept" verdict on reused kits is false for Sep 8–30 (the source pruned them), fixed by ending
  the data on 2025-09-07. LEAK-9 triggered (same-day burst), fixed by a protocol line. SPLIT-14 and SPLIT-15 (Must part)
  hold; SPLIT-10 one-day gap added (fugaku, ga_merchandise).
Value: TP non-trivial (depth-2 tree 0.765, LightGBM 0.93–0.98, linear 0.91); every fold scorable (MET-2).
Quality: CLEAN-14 five flags categorical; title_length capped; numbers corrected.
Weighed: size +, real telemetry negatives +, only open dated phishing table +; our own features −, cut-down URL −.
For the curator: issue 1, the window layout after the Sep 7 cut; issue 2, roc_auc or partial AUC (FPR ≤ 1%).
```

**Changes to make now (no decision needed)**

1. **Size floor (LEAK-13, Must).** In `_prepare_raw_files`, record the raw HTML length but never use it as a feature. In `_clean`, drop pages under 10,000 characters for both classes in every month. This removes 3,207 test rows, all phishing. The mean ROC AUC goes from 0.9591 to 0.9555. Rewrite the "Anomaly" note.
   - My check: no other size limit differs by class. Benign pages start at exactly 10,000–10,114 characters every month from Sep 2024. Phishing pages start at 1,000, then 5,000 from April 2025. The largest pages per class and month have no cap in common.
2. **`canonical_url` (LEAK-13, Must).**
   - Lower-case the host, drop `:80` and `:443`, and strip `[&,+;=]` and non-ASCII characters from every URL.
   - Add one line to the LEAK-13 bullet.
   - Until this lands, the README's claim that the URL is read "in one form for both classes" is false.
3. **End the data on 2025-09-07 (LEAK-42, Must; the remedy is a filter).** The definition says reused kits are kept as natural. That holds for July, August and Sep 1–7, but not for Sep 8–30, which the source pruned:
   - exact HTML repeats among phishing pages: 9.0% before Sep 8, 0.4% after;
   - tag signatures seen before the window: 3.7% after Sep 8, against 21–32% before.

   A fix exists, so the Must is fixed rather than noted. Both sides recommend the cut in their rebuttals. The layout of the windows after the cut is issue 1.
4. **One-day gap (SPLIT-10, Should).** Set `gap=1, gap_unit="days"`, as on fugaku_hpc_job_failure and ga_merchandise_store_sessions. It costs at most 0.7 points of training share.
5. **Fit and marker (USE-8, Must).**
   - Set `fit="approximate"`.
   - Make `fit_reason` name three gaps: the URL is cut down (no query or scheme), the 50 features are ours, and the class mix follows the collection.
   - Add `Selection Bias` to the record. The verdict stays `Yes`. This follows website_phishing, web_page_phishing_detection and naticusdroid.
6. **Metric reason (MET-11, Must; MET-2, MET-9).**
   - Set `original="average_precision"` with Sec. 5.1 as the reference.
   - Rewrite the reason: the source scores at base rates of 0.05–5%, while our folds are at 16–24% (restate after the rebuild).
   - Remove "two metrics with no one deliberate choice" and "15% to 90%".
7. **Protocol line (LEAK-9, Should).** Add: "Each test row is predicted from the training rows and its own features; a method that reads other test rows is not benchmarked." This follows medical_facility_operational_data.
8. **Quality (CLEAN-14, CLEAN-11).**
   - Make `host_is_ip`, `host_punycode`, `host_www`, `path_is_root`, `path_page_extension` and `host_port` categorical.
   - Cap `title_length`.
9. **Text.**
   - The release has 367,989 benign pages.
   - Pages under 200 characters are 1.46% of phishing in the release and 0.27% in the kept rows.
   - State the measured v1.0.0 → v1.0.1 downsampling (0.5% of v1.0.0's July 2024 benign pages remain).
   - Lead the reason the date is no input with what the date records (the time the label arrived); keep the scores as support (precedent checker, row 2).
   - Regenerate the README after the rebuild.

**Issues for the curator, ranked**

**1. The test windows after the Sep 7 cut (P4; SPLIT-15 Should for the non-newest windows; SPLIT-12 refit cadence, which needs sign-off anyway).**
- **Problem:** cutting on Sep 7 breaks the monthly grid, so the windows have to be re-cut.
- **Ruling on the dispute:** the critic reads SPLIT-15's Must too broadly. Its Must part is only that "the newest window is always a test window", and that holds either way. The Must that is broken is LEAK-42, and the cut in change 3 fixes it. What is left is a weighing.
- **Options**, measured by me with the size floor and the gap applied (348,294 rows):

  | | Windows | Training share (of all rows) | Test rows / phishing | Training rows from 2025 in the oldest window |
  |---|---|---|---|---|
  | C (split auditor, both sides) | 4 weeks: Jun 16–Jul 13, Jul 14–Aug 10, Aug 11–Sep 7 | ≈63.6% / 75.7% / 85.5% | 42.2k/5.7k, 35.3k/13.4k, 50.1k/9.9k | 3.4k |
  | B | July, August, Sep 1–7 | above the floor | the newest has about 11k rows | 11k+ |

- **Advocate's best point:** C keeps windows of equal length, with every training side above the floor.
- **Critic's best point:** the same. Both sides back C.
- **What the panel missed:** C's oldest window trains on 2024 plus only 3.4k rows from 2025. That is close to the June window the definition rejected for "training on 2024 alone, after 7.5 months without benign pages".
- **Decision needed:**
  - C with a four-week refit cadence, plus a sentence on why its oldest window passes where June did not;
  - or B, with uneven window lengths.

**2. Metric: `roc_auc` or standardised partial AUC at FPR ≤ 1% (P6; MET-1 Must, MET-11 `context`).**
- **Measured facts both sides accept** (domain practitioner's measurement):
  - the best model is the same under every score;
  - among the three weaker models, ROC AUC ranks the URL-only model last, while pAUC, TPR at 0.1% FPR and AP at 1% phishing all rank it first;
  - the order also flips within single windows.
- **Advocate:** keep `roc_auc` and write the reversals into the reason. pAUC needs a new registry entry.
- **Critic and practitioner:** the actor sets its threshold at an FPR of 1% or less, and Sec. 5.1 argues from the cost of false positives. The argument is fidelity to the task, so the "task fidelity over separability" memo does not rule pAUC out.
- **What would settle it:** whether MET-11 `context` covers a partial AUC the source did not name. That is the curator's reading.
- **Consistency:** web_page_phishing_detection's panel asked for the same operating-point note. Decide both the same way.

**3. Accept the `dataset_identifier_column` warning for the `url` text (P4, Weigh; precedent).** The advocate and the critic agree, following phiusil_phishing and drug_induced_autoimmunity_prediction. The blind reviewer dissents: 62% of benign test hosts appear in training, against 4.5% of phishing hosts. The practitioner calls those repeat hosts real allowlist-like knowledge (SPLIT-13). Accept it, or drop `url`.

**4. Optional (CLEAN; practitioner): a feature for a brand named on the page while the host is not that brand's.** Add it only if the curator sees it as representing the actor's inputs, not as a way to raise scores.

**Agreed facts**

- 404,979 rows; 25% phishing; three windows (Jul, Aug, Sep 2025) of 57,094, 54,752 and 43,499 rows; training shares 61.6%, 75.7% and 89.3%.
- A constant prediction scores 0.5; the smallest phishing count in a fold is 7,161.
- Benign pages have a 10,000-character floor and phishing pages a 1,000 or 5,000 floor. "Under 10k, so phishing" has precision 1.00 in every window, and the tag counts recover page size at AUC 0.998.
- URL form differs by class in 0.3–0.5% of phishing test rows, with an effect under 0.005 AUC.
- 74% of September (32,255 rows) is the source's pruned test split; the repeat rates are as given in change 3.
- The score drop on Sep 8–30 is not used as evidence (SPLIT-15: statistics of the data, not a model's score).
- Same-day burst counts using test rows add +0.031, +0.009 and +0.045 AUC; counts over past days only add nothing.
- My check on the task gamer's "2024 filtered differently" claim:
  - 2025 phishing pages whose exact HTML appears in 2024 are 0.4–1.4% in June to Sep 7, then 0.0% on Sep 8–30.
  - Before Sep 8 this cannot be told apart from the effect of the 7.5-month gap.
  - The gain from it (+0.003–0.004) is at noise level. It is information only.

**Task-gamer exploits mapped**

| Exploit | Rule | Note or accepted warning in the definition | New or known | Remedy |
|---|---|---|---|---|
| Same-day host, domain and HTML-fingerprint counts (#1, 1b, 1c, 1d), including a streaming counter within the day (0.976 / 0.991 / 0.968) | LEAK-9 | none | new | protocol line (change 7) |
| 2024 rows from a different process | SPLIT-11, LEAK-42 | the "downsampled" note only | partly known | none, at noise level |
| Looking up the URL in the published release | outside the protocol | none | new, not measured | none; same standing as every public dataset |

The definition has no `Potential leak, kept on purpose:` note and no accepted warnings, so no known exploit's gain needs re-checking against one.

**Consistency with precedent**

- **Follows precedent:**
  - the one-day gap (fugaku, ga_merchandise);
  - the `Selection Bias` marker (website_phishing, web_page_phishing_detection, naticusdroid);
  - the date as no input (bank_marketing);
  - the protocol line (medical_facility_operational_data);
  - `url` as text (phiusil);
  - the LEAK-13 harmonisation (hepatitis_c, gallstone);
  - keeping the 2024 rows to meet the floor (american_companies_bankruptcy).
- **New, to add as Cases rows once decided:**
  - LEAK-13: months dropped for a capture format that changed by class;
  - LEAK-13: a size floor the release applied to one class, harmonised;
  - LEAK-42: data ended at the source's cut because the source's de-duplication would make the newest window a different population.
- **Distinguished from the sibling:** keeping registered domains across windows departs in wording from web_page_phishing_detection's grouping by domain. The fact that sets it apart is that this dataset has dates. Add one sentence to the splits comment.
- **Open:** issue 2 should be decided together with web_page_phishing_detection's metric.

</details>

<details><summary>Claim audit</summary>

I found 4 problems, none of them a blocker. Two need a short rewrite and two need a small change to the definition. Most claims held when tested.

**Folder:** `datasets/_dev/tabarena-v0pt2/phreshphish_phishing_pages/`. I loaded the frame through `dataset_io.from_definition` and joined it to the builder's table of capture facts by `sha256`. I read the paper (arXiv 2507.10854v2, HTML) and the data card through a fetch agent.

**Claims table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 404,979 pages, 303,926 benign / 101,053 phishing, 25% phishing | task_summary.row/predicted, curation_comments | Rebuilt the frame | holds | 404,979 rows; 303,926 / 101,053; 0.250 | — |
| 2 | 15% to 60% phishing by month | task_summary.predicted | Crosstab of the kept months | holds | 15.1% (Aug 2024) to 59.5% (Oct 2024) | — |
| 3 | The release has "368,989 benign" pages out of 666,315 | curation_comments, record screening | Counted the raw labels | **refuted (typo)** | 367,989 benign + 298,326 phishing = 666,315; 368,989 doesn't add up | — |
| 4 | Deduplication drops 16,190 rows (16,078 phishing, 112 benign) | curation_comments | Re-ran the `_clean` logic on the raw features | holds | 16,190 / 16,078 / 112 | LEAK-13 |
| 5 | Oct–Nov 2025 dropped is 132,183 rows; July 2024 is 50,716 rows after dedup; Dec 2025 has 987 benign pages only | curation_comments | Month counts | holds | 132,183; 50,716; 987 benign, 0 phishing | — |
| 6 | Windows: Jul / Aug / Sep 2025 = 57,094 / 54,752 / 43,499 rows; 22% / 24% / 16% phishing; training 61.6% / 75.7% / 89.3% | splits_comment | Read the shipped splits | holds | Exact row counts. Training sides 249,634 / 306,728 / 361,480 rows. Each training side ends the day before its test month | SPLIT |
| 7 | No DOCTYPE form in the kept months | curation_comments (HTML) | DOCTYPE share by month and class (the builder's capture table) | holds | 0.0 phishing in every kept month; 0.7% benign in Aug 2024 only | LEAK-13 |
| 8 | `lang_score` is −1 exactly where `lang` is missing | curation_comments | Crosstab | holds | 5,575 rows where both coincide; no mismatches | — |
| 9 | 1.75% of phishing pages and 0.03% of benign pages hold under 200 characters of HTML | curation_comments (Anomaly) | Counted `raw_len < 200` | **refuted (number)** | Release: 1.46% phishing / 0.03% benign. Kept rows: 0.27% / 0.03% | — |
| 10 | No canonical URL repeats across a cut | curation_comments (Note) | Trivially true after dedup, so I also tested a looser key: lower-case, no `www.`, no trailing `/` | holds | 0.01–0.04% benign and 0.08–0.14% phishing test rows match a training URL, all with the same label | LEAK-42 |
| 11 | All URL recording differences between the classes are removed by `canonical_url` | curation_comments (URL form) | Character sets of canonical URLs by class | **refuted (small)** | Benign URLs contain no `&`, `,`, `+`, `;`, `=` and no non-ASCII at all. Phishing has them in 0.38% of rows. All 10,986 benign Wikipedia URLs have their commas stripped (`Huntington_Park_California`, `Highland_Hospital_(Oakland_California)`). Any of these characters marks the row as phishing with no false positive: 0.29–0.49% of phishing test rows, 0–0.01% of benign | LEAK-13 (Must) |
| 12 | Benign HTML is not cleaned differently from phishing HTML (implied) | — | Paper A.2; share of benign login URLs with forms and password fields | holds | A.2 cleans only benign URLs (query removal, a name filter). Benign login-like URLs: 80% have a form, 54% a password field (Facebook 95%). The `has_head_tag` gap (86% vs 97%) shows on ordinary Wikipedia pages: content, not sanitising | LEAK-13 |
| 13 | The benign-only name filter leaves no trace a model can use (implied) | Paper A.2 | Common first names as whole path tokens, by class | holds | 0.84% of benign paths have one, 0.01% of phishing: the filter did not make names a phishing marker | LEAK-13 |
| 14 | September pages from Sep 8 on had near-duplicates of earlier pages removed by the source | splits_comment | Exact-HTML and tag-skeleton repeat rates before and after the 8th, with July and August as controls | holds; **consequence unstated** | Sep phishing, same exact HTML in training: 9.0% before the 8th vs **0.4%** after. July and August after the 8th: 4.7% and 6.8%. Same skeleton: 38% → 6.6% in September, 48% → 21% in August. Benign exact repeats after the 8th: 0.0%. 32,255 of 43,499 September rows (74%) come from the source's test split | SPLIT, LEAK-42 |
| 15 | Near-duplicate kits are kept as natural (LEAK-42) | curation_comments, builder issue 3 (rec. A) | Same as 14 | **partly refuted** | They are kept in July, August and Sep 1–7, but the source already removed them after Sep 8. The deployment window is therefore a different population from the other two (see R3) | LEAK-42, SPLIT |
| 16 | No gap needed (label made minutes before the crawl) | splits_comment | Paper Sec. 3.1 | holds | "URLs are scraped within minutes of being reported to our feeds" | SPLIT |
| 17 | Date is not an input; `time_of="label"` | curation_comments | `feature_cols` from the loader; daily class counts | holds | `date` is not in the features. Sep 1 has 725 phishing and 0 benign pages: the day's class mix is the crawler's schedule, so leaving the date out is right | LEAK |
| 18 | Metric reason: "two metrics with no one deliberate choice (MET-5)" | `metric.reason`, README Metric block | Paper Sec. 5.1, Conclusions | **partly refuted** | Sec. 5.1 argues for its metrics: "Users ... are typically highly sensitive to false positives ... Accordingly, we evaluate ... AP ... and P@R=0.9". The Conclusions repeat it. Both metrics are precision-based and argued from the decision, so this is not "several metrics side by side" (gallstone_disease). No ranking criterion is named; AP is used once to call GTE the best | MET-5 |
| 19 | Metric reason: AP's base rate "runs from 15% to 90% phishing by test month" | `metric.reason` | Test-window phishing shares | **refuted (stale)** | The shipped test windows hold 16.5% / 24.4% / 21.8% phishing. 90% was November 2025, which is dropped | MET-9 |
| 20 | `roc_auc` is computable on every fold | — (MET-2) | Scored a constant and a random prediction on each fold with `data_foundry.v2.metrics.score` | holds | Constant 0.5; random 0.4975–0.5024 on all 3 folds. Smallest positive count in a fold is 7,161. No scoring columns needed | MET-2 |
| 21 | Fallback chosen correctly | `metric` | Card, paper, MET-2/MET-9 | **holds on another ground** | The source scores AP and P@R=0.9 on test subsets at 0.05–5% phishing (the card's benchmarks). Our folds are at 16–24%, so AP here would mean something else (MET-2), and P@R=0.9 is a threshold metric. The spec has `original=None, reference=None`, though the source does have a metric | MET-2, MET-9, MET-11 |
| 22 | URL+HTML LightGBM forward scores (builder: Jul 0.919, Aug 0.975, Sep 0.949) | builder report | Re-fit LightGBM on the 52 numeric features (no URL text) | holds (same range) | Jul 0.926, Aug 0.987, Sep 0.961 | — |
| 23 | Use case, collection facts, licence (CC BY 4.0, research use) | task_summary, record | Card and paper | holds | Sec. 3.1: Selenium Grid on Chrome. Benign pages from Webroot telemetry; phishing from PhishTank, APWG and NetCraft. Not checked: how benign labels were verified (the paper doesn't say) | USE-1 |

**Refuted and untested, ranked**

**R1. A recording residue is left in `url`: characters stripped from benign URLs only (LEAK-13, Must; small).**
- **What happened:** the benign URLs (most clearly Wikipedia's) were stored with commas removed, and the benign class holds none of `&`, `+`, `;`, `=` or any non-ASCII character. The query removal took the separators that follow a `?` but not those inside the path.
- **What a model can use:** the `url` text feature gives a no-error phishing marker on 0.3–0.5% of phishing test rows.
- **What it changes:** below 0.005 ROC AUC by count, so no measurable shift in the scores. But it breaks the README's claim that the URL is read "in one form for both classes", and it is the same kind of defect the builder already fixed for the scheme and the query.
- **Mildest remedy:** in `canonical_url`, drop `[&,+;=]` and non-ASCII characters from every URL. One more bullet under "Class-dependent recording (LEAK-13), removed from the URL". The rebuild only touches 0.38% of the phishing rows.

**R2. The metric's reason misreads the source and quotes a stale base rate (MET-5, MET-9, MET-11; wording, the declared metric stays).**
- **The source:** Sec. 5.1 argues for precision-based evaluation from the false-positive cost. That argument is a deliberate choice; it is not a list of metrics side by side.
- **Why the fallback still holds:**
  - The source's AP is computed at 0.05–5% phishing on test subsets; our folds run at 16–24%, so AP here measures something else (MET-2).
  - P@R=0.9 is a threshold metric (MET-6).
  - The source names no criterion it ranks models by (MET-5).
- **What is wrong in the reason:** the "15% to 90% by test month" range describes months the task drops.
- **What it changes:** the curator may read the fallback as a habit rather than a measured call.
- **Mildest remedy:**
  - Rewrite the reason on MET-2/MET-9: the source scores AP and P@R=0.9 at fixed 0.05–5% base rates; ours are 16.5–24.4%.
  - Set `original="average_precision"` and `reference` to Sec. 5.1, as sepsis_survival_minimal_clinical_records records its PR AUC.

**R3. The deployment window is three-quarters filtered by the source (SPLIT and LEAK-42, Should; changes builder issue 3).**
- **What happened:** 74% of September's rows (Sep 8 to 30) come from the source's test split, which had near-duplicates of training pages removed.
  - Exact repeats of earlier HTML among September phishing pages fall from 9.0% before the 8th to 0.4% after; July and August keep 4.7–6.8% after the 8th.
- **What it changes:**
  - The windows are not one population. Builder issue 3, option A ("keep near-duplicates, as a filter meets them") is what July and August get, but September after the 8th already has option B applied by the source.
  - Within September, a forward LightGBM scores 0.991 before the 8th vs 0.942 after. July shows a similar drop with no filtering (0.993 vs 0.914), so I can't attribute the score gap to the filter. The repeat-rate drop is clean evidence of the filtering; what it does to the score is not separable.
- **Options to put to the curator** (mildest first):
  - (a) State it in issue 3 and the splits comment: the September window mixes filtered and unfiltered pages.
  - (b) End the data on 2025-09-07, the source's cut. September then has 11,244 test rows, the last window becomes smaller, and the set gains consistency.
  - (c) Apply the same near-duplicate filter to every window (issue 3, B).
- **My recommendation:** (a) at least. Prefer (b) if the curator wants every window to be one population.

**R4. Two numbers in the notes are wrong (no rule; text only).**
- The release has 367,989 benign pages, not 368,989 (curation_comments and the record).
- Pages under 200 characters: 1.46% of phishing in the release, 0.27% in the kept rows. The notes say 1.75%.
- **Remedy:** correct both numbers in the text.

**Untested:**
- How benign labels were verified: the paper and card say nothing.
- The source's near-duplicate threshold: not given in the text, and Algorithm 2's line 15 as written is reversed.
- How many rows v1.0.1's "downsampling some earlier samples" removed: not given.
- The day-share (0.72–0.85) and weekday (0.47–0.51) scores: I didn't re-run them; leaving the date out doesn't depend on them.

Everything else I tested held: the counts, windows and splits, the DOCTYPE removal, the `lang_score` coding, the URL copies across the cut, the no-gap claim, leaving the date out, and whether the metric can be computed on each fold.

</details>

<details><summary>Column audit</summary>

I found one problem that should block shipping: the release keeps benign and phishing pages above different minimum HTML sizes. Our tag counts pick that up, so a model can label part of the test pages phishing from page size alone. The rest is minor.

**Files of the release**

v1.0.1 (commit eca603e0) has 1,057 files: 77 `data/*.parquet`, 977 under `benchmark/`, plus `README.md`, `.gitattributes` and `.gitignore`. `_load_raw` reads all 77 data files. `benchmark/` is left out with a reason (it lists subsets of the test split, no new rows), and the README is read for the field list. No file is missing.

I also compared the earlier version, v1.0.0 (commit 3d861877), reading only its sha256, label, date and URL. It held 139,229 benign and 24,767 phishing pages from July 2024 and 2,507 benign pages from March 2025. v1.0.1 keeps 147 July benign pages (0.5% of v1.0.0's July benign pages are still there) and none from March 2025. So the card's "downsampling" can be measured, although the curation notes say the amount is unknown. The source removed these rows on purpose, so this is a correction to the notes, not a missing file.

**Columns**

The cleaned frame has 404,979 rows and 55 columns: `is_phishing`, `date`, `url`, `lang`, `lang_score`, 27 URL features and 23 HTML features. "Known?" means: known when the filter rates the page.

| column | meaning | known? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| `is_phishing` | the feed label ("phish" becomes Yes) | target | category No/Yes | fine | CLEAN-25 |
| `date` | collection day; for a phishing page, minutes after its report | it dates the label and is no input (`time_of="label"`) | datetime | fine | LEAK-10 |
| `url` | canonical URL: no scheme, query or fragment; a bare host gets "/" | yes | string, one value per row, carries information | fine, apart from finding 2 (host case, default port) | LEAK-13 (weak) |
| `lang` | language the release detected (the paper names the langdetect library) | yes, read from the page | category with 86 levels. The dtype probe flagged it `ordinal_like`, but it is a nominal language code, so categorical is right | fine. Phishing pages without a language fall from 4.0–4.5% (2024) to 0.2–0.5% (2025). That step comes from the size floor in finding 1 | CLEAN-14 |
| `lang_score` | langdetect confidence; the release's -1 is set to missing | yes | float32 | fine | CLEAN-10 |
| `host_length`, `host_dots`, `host_hyphens`, `host_digits`, `host_digit_share`, `host_labels`, `host_longest_label`, `host_entropy`, `tld_length`, `host_vowel_share` | lexical counts of the lower-cased host | yes | numeric counts and shares | fine. Benign means are flat across all 7 months; phishing drifts (the feed) | — |
| `host_is_ip`, `host_punycode`, `host_www`, `path_is_root`, `path_page_extension` | 0/1 flags | yes | int64; should be categorical | cleaning (finding 4) | CLEAN-14 |
| `host_port` | 0/1: a port is written in the host | yes | int64 flag | 1 benign page against 141 phishing pages; 61 of those 141 are an explicit ":443" (finding 2), plus finding 4 | LEAK-13 (weak), CLEAN-14 |
| `url_length`, `url_entropy`, `url_at_signs`, `url_percent_signs`, `url_tildes`, `url_keywords` | counts over the canonical URL | yes | numeric | fine. The "@" and odd-Unicode URLs are real obfuscated phishing URLs (Aug 2024), not a recording quirk | — |
| `path_length`, `path_depth`, `path_dots`, `path_hyphens`, `path_digits` | counts over the path | yes | numeric | fine. A trailing "/" on a non-root path: benign 29%, phishing 8–20%. I tested stripping it on the shipped windows: URL-only LightGBM 0.9072 → 0.9064, URL+HTML 0.9541 → 0.9548. No effect | LEAK-13 checked |
| `n_forms` … `n_word_copyright` (19 tag and word counts), `n_external_links`, `n_empty_links` | regex counts over the whole HTML | yes, from the rendered page | int64 counts | fine as columns. Together they recover the page's size at ROC AUC 0.998 within phishing, which carries finding 1 | LEAK-13 |
| `external_link_share` | links to another host divided by all links; missing when the page has no links | yes | float; the missing value means "no links" | fine (missing for 4% of benign and 10–30% of phishing pages, by content) | — |
| `title_length` | length of the first `<title>` | yes | int | regex overrun: maximum 306,917 characters; 73 rows over 500, split evenly by class (finding 5) | CLEAN-11 (negligible) |

`sha256`, `target` (the brand a page imitates), the raw URL and `source_split` are dropped, which is correct (CLEAN-3, LEAK-10). No feature is computed over the whole release and none is looked up later. Every feature comes from the URL and the HTML captured minutes after the report. No column starts or stops being recorded inside the test windows (no `splits_feature_missing_in_test` warning). The only partial steps are the `lang` missing share above and missing titles in June 2025 (14% of phishing pages), both explained by content or by finding 1.

**Problems, ranked**

**1. The release keeps the two classes above different minimum HTML sizes (P4, LEAK-13 Must; the Class-dependent Recording marker).**

The definition does not see this. I measured the shortest raw HTML length week by week on the release (the builder's capture table, raw length):
- **Benign:** never under 10,000 characters from 2024-08-19 through September 2025. In every month from September 2024 on, the shortest benign page is 10,000 to 10,114 characters. Before that the floor was 5,000, except the week of Aug 12–18, 2024, whose shortest page is 23 characters.
- **Phishing:** the floor is 1,000 characters from mid-August 2024 to March 2025, and 5,000 from April 2025 on.
- **In the test windows:**
  - 8.9%, 8.9% and 12.7% of phishing pages are under 10,000 characters; no benign page is.
  - The rule "under 10,000 characters, so phishing" has precision 1.00 in each window.
  - The page size is no feature, but the HTML counts recover it at ROC AUC 0.998.
- **In training:** 27–37% of the 2024 phishing pages are under 10,000 characters.

This also corrects two curation notes:
- Pages under 200 characters exist only in August 2024. The note says they are kept "as a filter meets such pages too", but the release drops small benign pages everywhere else.
- The 2024 phishing pages are a different size population from the test months (floor 1,000 against 5,000).

**Effect:** LightGBM on all features over the shipped windows scores 0.9322, 0.9846 and 0.9604 (mean 0.9591). With the same 10,000-character floor applied to both classes, train and test, it scores 0.9252, 0.9855 and 0.9559 (mean 0.9555). That is −0.007 in July 2025.

**Mildest remedy:** in `_prepare_raw_files`, record the HTML length, but never as a feature. In `_clean`, drop every page under 10,000 characters, for both classes and in every month. This removes 3,207 test rows, all phishing. Then rewrite the anomaly note and the class-dependent-recording note.

**2. Small URL-form differences, reported URL against browser URL (P4, LEAK-13, weak).**
- Upper case in the host: 137 phishing pages, 0 benign. Browsers lower-case the host.
- An explicit default port ":443": 61 phishing pages, 1 benign.

Both mostly date from August 2024. They reach the model through `url` (as text, length and entropy) and through `host_port`. Remedy: in `canonical_url`, lower-case the host and drop ":80" and ":443". It is cheap and safe.

**3. The notes say the downsampling of v1.0.1 cannot be measured (P5, information only).** The v1.0.0 comparison above measures it. Optional: replace "by an amount it does not give" with those numbers. I would not mix the two versions.

**4. Five 0/1 flags typed int64 (P7, CLEAN-14 Should).** `host_is_ip`, `host_punycode`, `host_www`, `path_is_root` and `path_page_extension` are yes/no flags by meaning (we built them), and they hold only 0 and 1. `host_port` is a sixth, once the default ports go (finding 2). They should go into `FeatureTypes(categorical=…)`.

**5. `title_length` regex overrun (P7, negligible).** 73 rows are over 500 characters, up to 306,917, where a `<title>` is not closed or is not the page's title (an SVG `<title>`, for example). Either stop the match at 1,000 characters or set those values to missing. Note-level.

**Checked and found clean:**
- The date is not an input.
- No post-outcome field, and no figure computed over the whole release or looked up later.
- The weekly step in phishing line breaks per 1,000 characters (about 1.5 to about 10, early October 2024) is not visible in the features. The HTML counts tell the weeks on either side apart at ROC AUC 0.857, about as well as two adjacent periods with no format change (0.894–0.898).
- About 400 kept rows were re-dated between v1.0.0 and v1.0.1 (same sha256 and URL). Re-collections, too few to matter.

</details>

<details><summary>Split audit</summary>

**Split audit: `phreshphish_phishing_pages`**

**Verdict: right with notes.** The split type, the leaf, the regime, the floor and the window count are right. One substantive problem needs the curator: from 2025-09-08 on, the newest window (September 2025, the deployment period) is the source's own test split, and the source removed near-copies of earlier pages from that split. The other windows never had that done. This is note 1 below.

**Tree (SPLIT-36)**
I walked it from the collection type **Dated event log**:
- **[LOG.meets]:** the model meets cases after the data (pages a filter rates next).
- **[ORDER.order]:** yes. `date` is recorded for both classes; it is the crawl day.
- **[ORDER.windows]:** yes. Three monthly windows each train on at least 61.6% of the rows. The one-month length is our assumption and needs sign-off.
- **[ORDER.small]:** no. The table has 404,979 rows.

That reaches **[L-ORDER.windows]**. It matches `split_leaf`, the splits comment and the shipped `Temporal` split. The tree raises no question that no answer fits. Nothing is forced, and the leaf already has examples.

**Regime, floor, count**
- **Regime:** each page is new, but registered domains recur. A filter meets known domains, so a temporal split that keeps them is right (SPLIT-13, USE-10).
- **Train shares:** Sep 89.3%, Aug 75.7%, Jul 61.6%. None is under half (SPLIT-14).
- **Test windows:** 43,499, 54,752 and 57,094 rows. The smallest phishing count is about 7,161. Every window holds both classes.
- **Window count (SPLIT-15):** an IID split would get 2/3 × 405k = 270k units, which is over 250k, so 1 repeat = 3 splits. The definition ships 3, so the target is reached.
- **What stops more windows:** `dataset windows` offers only 4 candidates (June to September 2025). June would train on 2024 alone, after a 7.5-month gap without benign pages. Windows in 2024 fail the floor.
- **Choice:** walking back from the newest window is forced by the short history (SPLIT-15). No model score was used to choose.

**Horizon and time frame (for the `Horizon:` block)**
- **Length:** one month. The source states no refit cadence, so this is our assumption.
- **Gap:** none. A phishing label is the feed report, made minutes before the crawl (the source says so). The date's smallest step is a day, which is longer than that delay (SPLIT-10).
- **Lead times:** no input is issued ahead of the date. The time column is the moment a filter would meet the page (USE-3 holds; this is not the kickstarter case).

| Option | Windows above floor | Test-window size | Note |
|---|---|---|---|
| **1 month (implemented)** | 3 (Jul, Aug, Sep 2025) | 43.5k–57.1k | |
| 2 weeks | about 7 | 5.8k–26.9k | phishing share swings a lot from window to window |
| 1 week | about 13 | — | the week of 2025-07-27 holds **no benign page** (3,856 phishing, 0 benign), so ROC AUC is undefined; phishing share runs 9% to 100% by week |

Recommendation: keep one month. Its time frame should change as in note 1.

**Findings, ranked**

**1. The newest window mixes two populations; most of it was pruned by the source**
Should; SPLIT-15 (the newest window stands for deployment), SPLIT-5 (the source's split is a claim to check), and consistency with the task's own LEAK-42 "natural" verdict on reused kits.

The source's split cuts on 2025-09-08, inside our September window:
- 12,154 raw rows before the cut are in its train split; 31,692 rows after it are in its test split.
- The paper (Sec. 4.1) says test pages that were near-duplicates of training pages were removed.

The data shows that pruning. The measure is the share of pages with at least 20 tags whose exact HTML tag-count signature appeared before the period started:

| Period | Phishing pages a day | Phishing with seen signature | Benign with seen signature |
|---|---|---|---|
| Jul 2025 | 384 | 21.2% | 2.6% |
| Aug 2025 | 415 | 28.0% | 3.4% |
| Sep 1–7 | 370 | 32.2% | 3.6% |
| **Sep 8–30** | **179** | **3.7%** | **0.9%** |

- Phishing pages a day fall to 43% of August's level. The share of rows a day stays at 82% of August's, so `time_newest_period_short` does not fire. This is the "cut that keeps the rows and drops outcomes" pattern: the drop shows only in the phishing share, from 24% down to 10–15%.
- The effect on scores (LightGBM on all features except `url` and `date`, trained on everything before the window):

| Window part | ROC AUC |
|---|---|
| Sep 1–7 | 0.991 |
| **Sep 8–30** | **0.941** |
| Aug 1–7 | 0.989 |
| Aug 8–31 | 0.986 |

- Training up to Sep 8 still gives only 0.950 on Sep 8–30. So the drop comes from the pruning, not from a model gone stale.
- The task keeps reused phishing kits on purpose in July and August, because a filter meets them. In 74% of the deployment window the source removed them.

**Mildest remedy:** a filter. End the data at 2025-09-07, the last day of the source's train split; this drops 32,255 rows. Then re-cut the windows:

| Option | Newest window | Middle window | Oldest window | Drawback |
|---|---|---|---|---|
| **C: 4-week windows** | Aug 11–Sep 7: 51.3k rows, 86.2% train | Jul 14–Aug 10: 36.2k, 76.5% | Jun 16–Jul 13: 43.1k, 65.0% | |
| A: shifted months | Aug 8–Sep 7: 52.0k, 86.1% | Jul 8–Aug 7: 51.7k, 72.2% | Jun 8–Jul 7: 30.5k, 64.0% | oldest window trains on only 73 rows from 2025, the objection that ruled out June |
| B: keep Jul and Aug, newest Sep 1–7 | 11.2k rows, 97% train | Aug (as now) | Jul (as now) | uneven window length |

Recommended: C. Its oldest window trains on 3.6k rows from 2025, against 11.2k today.

If the curator keeps the current split, the splits comment should give these numbers and say plainly that the deployment window is mostly pruned. Right now it only mentions the pruning as an aside.

**2. The month is an assumed refit cadence**
Weigh; SPLIT-12. This is covered above. The `**Horizon:**` block needs the curator's sign-off.

**3. Training history: what is in and what is left out**
Weigh; SPLIT-11.
- **Left out:** the phishing-only months, November 2024 to April 2025 (about 64k raw phishing pages, before the URL dedup). A deployed vendor would hold these pages. Dropping them keeps the class mix tied to the benign collection, and it is defensible. It also removes kits that would raise the July–September near-copy shares. I did not measure its effect on scores.
- **Unknown size:** v1.0.1 "downsampled some earlier samples" by an amount the source does not give. The 2024 months could carry a class-dependent downsampling we cannot see.

Remedy: a note, no change.

**Checked, no finding**
- **Label in flight:** a phishing label arrives within minutes, at the date's resolution. How the source verified benign labels (telemetry plus checks?) is still not checked. If benign labels were confirmed by a later lookup in the feeds, that would be a late label.
- **Recurring URLs:** none repeat across a cut, since the dedup keeps each URL's first collection, including collections in dropped months. That matches a blocklist.
- **Batches in the raw order:** none, because the split is temporal.
- **Time on risk / weights:** not applicable.
- **Newest-period rows a day:** 82% of the earlier period. Normal apart from finding 1.

</details>

<details><summary>Domain practitioner</summary>

**Domain-practitioner report: `phreshphish_phishing_pages`**

I take the part of the ML lead at a vendor that ships a phishing filter, either a browser plug-in or the client-side model of a secure web gateway. When someone opens a page, I score it from its URL and HTML in a few hundred milliseconds. Above a threshold I warn or block the page, or send it on to a server-side check. I refit on newly reported pages and benign telemetry, and I push a new model about once a month.

**Fit: approximate (the definition says `direct`)**

The moment, the decision, the label timing and the forward monthly split match my job. But three things in the data are not what my filter sees:
- the inputs are cut down from what I always have (see below);
- each row is a distinct URL, not a page view;
- the mix of classes follows the collection schedule.

The definition's own `fit_reason` already lists two of these gaps ("the mix of the classes follows the collection, not the web", "the features are ours, not a product's"), which does not fit with `fit="direct"`. Under USE-8, a known gap that is named makes the fit approximate. A task changed a lot to avoid a leak counts the same way, and the query had to be removed for that reason. USE-9 does not offer a better-fitting actor: the plug-in or gateway is already the right one.

**1. Inputs at the moment of prediction**

**I have every input that ships.**
- The URL, the tag and word counts, the title length, and the page language (I detect it myself, so `lang` and `lang_score` are fine).
- The date is not an input. That is correct: the share of phishing by day reflects the crawler's schedule, not the web (USE-3).

**I always have these, but they are missing**, ranked by how much they would change the task:
1. **The query string and the scheme.** Phishing URLs carry per-victim tokens, base64-encoded e-mail addresses and redirect parameters in the query, and http against https is a classic signal. Both were removed because the release recorded them differently by class (LEAK-13). That is a necessary fix, but it removes a real input I always have, so it is a gap and not a free choice.
2. **The page itself: visible text, form targets and rendered look.** I get 50 hand-made counts instead.
   - Chrome's client-side detector uses a DOM content model plus a visual model.
   - The source paper's strongest models read the raw HTML text (TF-IDF, transformer embeddings).
   - A brand that does not match its domain is the core signal of phishing. For example, the page says "PayPal" on a non-PayPal host, or a form posts to another domain. Nothing here encodes either: `n_word_*` covers only login, password, verify, account and copyright, and the impersonated brand (`target`) is correctly dropped because it is a label.
   - This is our feature set, not the decision's. Another curator could reasonably build other features from the same 193 GB, so the task is partly defined by our extraction script.
3. **Domain reputation and age, and the TLS certificate.** The paper excludes these on purpose for latency, which is fair for a pure on-device model. Real products (BrightCloud, Safe Browsing) do use cached reputation. This is a minor gap given the stated use case.

**2. Target**

`is_phishing` is what I act on: warn or block. The label comes from feed reports (PhishTank, APWG eCrime eXchange, NetCraft). Those pages were caught by someone, which slightly favours phishing that is easy to report, but every filter vendor trains on exactly these feeds, so the selection is shared with the real setting (USE-8, selection paragraph).

I want a probability or score and then set my own threshold at a very low false-positive rate. A false block of a real bank login page is the expensive error. The benign side includes search results for heavily targeted brands, which are exactly the hard negatives I need. That part is good.

**3. Unit and test population**

- **Keeping one row per canonical URL matches my real job.** A URL already on a blocklist is handled by the list, and the model's job is new URLs.
- **The benign side is not a sample of page views.** Popular sites appear once each, not weighted by traffic, so the false-positive rate here is per distinct URL and not per user visit. That is mild and acceptable.
- **The test months (July to September 2025) are what I would face next.** Hosting platforms (gitbook.io, webflow.io, pages.dev) and reused phishing kits recur across months, and my filter meets them again in practice. Keeping them is right (SPLIT-13, LEAK-42).
- **The phishing share is 16% to 24% per test month**, against the paper's deployment base rates of 0.05% to 5%. This matters for the metric (section 5), not for the split.
- **The 7.5-month hole without benign pages in the 2024 history is unusual.** I would never refit across such a gap, but it is disclosed.

**4. Would I use the model?**

I would use a model trained on this as a client-side first filter, the way Chrome's on-device score triggers a server-side check.

**What would make me trust it:**
- forward monthly testing;
- benign pages from real browsing telemetry rather than a top-sites list, which is unlike every older phishing table (Hannousse, PhiUSIIL, vrbancic);
- the clean-up of the format differences between classes.

**What would make me distrust it:**
- No query or scheme, which I would not give up in production.
- Coarse counts where I would use page text.
- The October and November 2025 phishing pages were dropped because the crawler changed its HTML format. In production a crawler or kit change like that is exactly the drift I must survive. Dropping them is the right call for a clean benchmark, but it means the test months do not cover the hardest real drift.

**5. Metric: partly**

The declared fallback `roc_auc` does not depend on the class share. That is the right property here, because the share of phishing follows the collection, and the definition's case against the paper's average precision (MET-5, MET-9) holds.

But ROC AUC weighs the whole curve equally, and I operate only at its far left: a false-positive rate of 1% or less. The paper makes the same point: at low base rates, keeping precision at the same recall "requires a significantly lower false positive rate". Under MET-1 the metric should score that operating region.

**My measurement.** I fitted untuned models on the shipped definition's rows and the three forward windows. Mean over the three windows:

| Model | ROC AUC | pAUC (FPR ≤ 1%) | True-positive rate at 0.1% FPR | AP at 1% phishing (reweighted) |
|---|---|---|---|---|
| LightGBM, all features | 0.960 | 0.824 | 0.534 | 0.686 |
| LightGBM, small (50 trees, 7 leaves) | **0.919** | 0.673 | 0.224 | 0.374 |
| LightGBM, URL only | 0.906 | **0.695** | **0.268** | **0.401** |
| Logistic regression | 0.908 | 0.651 | 0.201 | 0.320 |

pAUC is the standardised partial ROC AUC (McClish).

- **ROC AUC and the operating-region scores put the models in a different order.** ROC AUC ranks the URL-only model last of the three weaker models. Every low-false-positive score ranks it first of them.
- **Per window the order flips too:**
  - July: ROC AUC orders logistic regression > small > URL; pAUC orders URL > small > logistic regression.
  - August and September: small beats URL on ROC AUC, and URL beats small on pAUC.
- **The best model is the same under every score, and the spread is much wider at low false-positive rates.** pAUC spans 0.65 to 0.82 across the models, against 0.91 to 0.96 for ROC AUC.

**What I would choose:** standardised partial ROC AUC up to a false-positive rate of 1%, declared as origin `context` (MET-11).
- It keeps ROC AUC's independence from the class share, which matters here (MET-9).
- It needs no fixed threshold or cost from the source (MET-6, MET-7 are not met).
- It scores the region I would set my threshold in (MET-1, MET-8).
- It has enough resolution: each test window has about 36,000 to 47,000 benign pages, so about 360 to 470 of them fall under a 1% false-positive rate. A cut at 0.1% would leave only about 40 per window, which is too coarse.

The paper's own metrics (average precision and precision at recall 0.9) are base-rate dependent, so they would need reweighting to a deployment rate. That is a construct of ours, and there are two of them, so neither is a unique original (MET-5).

The registry has no partial-AUC metric (`src/data_foundry/v2/metrics.py`), so this needs a new metric or the curator keeps `roc_auc` and names the gap. If the curator keeps `roc_auc`, the metric reason should say that it scores the whole curve while the actor works at a false-positive rate of 1% or less.

**What a domain expert would change, ranked**

1. **Set `fit` to `approximate`** and make `fit_reason` name the gaps: query and scheme removed for the recording fix, page text and rendering reduced to 50 counts of ours, one row per distinct URL with a class mix set by the collection. Today's `fit_reason` already lists the last two under `direct`.
2. **Metric:** switch to partial ROC AUC with FPR ≤ 1%, as a new `context` metric, or keep `roc_auc` and record the operating-region gap with the measured reversals above. This is the curator's call.
3. **Add a cheap brand-versus-host feature**, if the features stay ours: page text or title mentions a top-targeted brand while the host is not that brand's domain. It is the signal every practitioner uses, and it is computable from the URL and the HTML alone. It needs a fixed brand list taken from the benign side or a public list, never from the dropped `target` column. This is optional, and per the "task fidelity over separability" memo, only if the curator treats it as representing the actor's inputs rather than lifting scores.
4. **Keep as is:** date not an input, one row per URL, hosting platforms and phishing kits recurring across windows, monthly refit, dropping October and November 2025 (with the note that this hides real crawler drift).

**Sources**
- Dalton et al. 2025, PhreshPhish, [arXiv 2507.10854](https://arxiv.org/abs/2507.10854) ([HTML v2](https://arxiv.org/html/2507.10854v2)): Sec. 5.1 metrics and base rates; the point about lower false-positive rates at low base rates.
- The data card at [huggingface.co/datasets/phreshphish/phreshphish](https://huggingface.co/datasets/phreshphish/phreshphish), as quoted in the record and definition.
- [Chromium-dev thread on client-side detection](https://groups.google.com/a/chromium.org/g/chromium-dev/c/7hbmB_Vfwzc): the content and visual models' scores only trigger the server-side classifier.
- [Client-side anti-phishing longitudinal study, ASIACCS 2024](https://adamdoupe.com/publications/client-side-anti-phishing-asiaccs2024.pdf): Chrome's on-device classifier, its visual model and its false negatives.
- Repo files: `dataset.py`, the record's screening block, the builder report, the builder's window scores, `issues/website_phishing.md`, `use_case.md` (USE-1, 3, 5, 8, 9), `metrics.md` (MET-1, 5 to 9, 11).

</details>

<details><summary>Precedent check</summary>

I checked the builder's draft calls for `phreshphish_phishing_pages` against similar past decisions. Two depart from precedent without a stated reason, and the rest follow precedent or name the fact that sets them apart. Nothing was edited. One measurement was made on the prepared features file: what a one-day gap would cost.

**Decision by decision**

| # | Draft call (builder) | Status | Closest precedents |
|---|---|---|---|
| G | **No gap** before each monthly window, because a phishing label arrives within minutes | **Departs without a reason** | Andrej, 2026-11-24, `fugaku_hpc_job_failure` (issue 7, D: one-day gap for the time it takes to build a model before using it, `curation/records/fugaku_hpc_job_failure.md:451`); Andrej, 2026-11-25, `ga_merchandise_store_sessions` (issue H, b: one-day gap "though the label is known when the visit ends", `curation/records/ga_merchandise_store_sessions.md:73, 110-149`); Lennart, 2026-11-10/11, `maps_router_eta` and `pkdd_15_taxi_trip_time_prediction_ii` (one-day gap). Prompt F1 below. |
| M | Markers: `Class-dependent Recording` only, no `Selection Bias` | **Departs without a reason** (on Selection Bias) | `website_phishing` (`Selection Bias`, `Yes`; Lennart, 2026-10-27); `web_page_phishing_detection` (`Selection Bias`, AI recommendation, not yet decided); `naticusdroid_android_permissions_dataset` (Lennart, 2026-11-16); selection.md, "Selection bias": "cases and controls collected apart or in different periods (… `website_phishing`)". Prompt F2 below. |
| 1 | Drop October and November 2025 for the change in how the HTML was captured; no feature reads the DOCTYPE, raw length or line count | Consistent | LEAK-13 (Must) explicitly covers "a convention that changed over time … when the classes changed over the same time". The usual fix (write both classes the same way) does not work here: the tag counts still tell the capture format apart at 0.976. So filtering the rows is the mildest remedy that does work. No earlier case dropped a period for this, so it becomes a new Cases row once decided. Not following the source's own split rests on a Must outranking SPLIT-12 (Should). |
| 1′ | Canonical URL (no scheme, query or fragment) for both classes; one row per canonical URL | Consistent | LEAK-13 harmonisation, as in `hepatitis_c_prediction` and `gallstone_disease`. It follows `phiusil_phishing` and `phishing_websites_vrbancic`, which were turned down for URL-form shortcuts. Here the shortcut is removed instead of retiring the dataset. |
| 2 | Date is no model input (`time_of="label"`) | Consistent in outcome; the reasoning should be reordered | `bank_marketing` (Andrej, 2026-11-21, `curation/records/bank_marketing.md:92`): the date was set by the labelling event, so no input. The same fact holds here: a phishing page is crawled minutes after it is reported. But definitions.md:624-632 says "the score with or without the column does not" decide. Issue 2 and `curation_comments` lead with scores (class share of the day 0.72-0.85, weekday 0.47-0.51). Suggestion: lead with what the date dates, and keep the scores as support. |
| 3 | Near-duplicate pages across the cut kept (reused phishing kits, LEAK-42 natural) | Consistent | SPLIT-13 known entities; `diabetes_130_us` (Andrej, 2026-11-11: temporal split kept with recurring entities); LEAK-42 "natural" cases (`santander_customer_satisfaction`, `ai4d_lab_tanzania…`). Not following the source's pruning of near-duplicates from its test set is named in the splits comment. |
| 4 | Canonical `url` shipped as text; the `dataset_identifier_column` warning proposed for acceptance | Consistent | `phiusil_phishing` (URL accepted as the task's input, not a row id), cited again for `drug_induced_autoimmunity_prediction` (CHANGELOG:4185). The curator must still accept it (left empty: correct). |
| 5 | Keep Aug-Oct 2024 across the 7.5-month gap with no benign pages | Consistent | SPLIT-14 (Must) 50% floor. Without the 2024 rows no window trains on half the rows. `american_companies_bankruptcy` (Andrej, 2026-11-25) also keeps old years to meet the floor. |
| 6 | `Class-dependent Recording` marker | Consistent | leak_checks.md: the marker stays "whether the artefact was fixed". Same in `gallstone_disease`, `hepatitis_c_prediction`, `horse_colic_survival`. |
| Metric | Fallback `roc_auc` (paper: average precision and precision@recall side by side) | Consistent | MET-5: `gallstone_disease`, `early_stage_diabetes_risk_prediction`; `web_page_phishing_detection` (AI recommendation). That sibling's panel also asked its metric reason to name the real operating point (below 1% false alarms). The same note fits here, since the paper scores at base rates of 0.05% to 5%. Optional. |
| Split/entity | Registered domains recur across windows and are kept (SPLIT-13: "a filter meets known domains") | Departs from the sibling's wording, with a stated fact | `web_page_phishing_detection` groups by registered domain, calling it "the unit a filter meets new" (`curation/records/web_page_phishing_detection.md:206, 576`). The fact that sets them apart: that dataset has no dates (`ForcedGroupedFromTemporal`), so its domain groups stand in for time. This dataset is dated, and the temporal cut gives the real mix of known and new domains. That practitioner also noted that a filter meets a new `x.blogspot.com` with blogspot already in training. No prompt needed. One sentence in the splits comment would keep the two siblings from reading as contradictory under USE-10. |
| Horizon | Monthly windows, a refit cadence we assume | Consistent | `ga_merchandise_store_sessions` (Andrej, 2026-11-25, monthly refit assumed, source silent); `airqo_low_cost_air_quality_monitor_calibration_challenge` (Lennart, 2026-11-11). |

**Drift:** none found. Andrej's gap call changed from 2026-11-23 (fugaku, no gap beyond the label filter) to 2026-11-24 (fugaku issue 7, D, one-day gap). This is a newer decision replacing an older one on the same dataset, recorded as such, and `ga_merchandise_store_sessions` repeated it on 2026-11-25. **Third exception:** none due.

**Internal discrepancy on the class share by month:** the record says 15% to 100% phishing by month (all months), `TaskSummary.predicted` 15% to 60% (kept months) and the metric reason "15% to 90% phishing by test month". The test windows are 16% to 24%. This is for the claim auditor; the metric reason should give the kept months' range.

**F1: no gap, against the curator's one-day gap for the time to build a model (issue for `## Review`)**

Should each monthly test window start one day after the training data ends, for the time a refit takes, as decided on fugaku and ga_merchandise?

* **Problem:**
  - The definition sets no gap because a phishing label is a feed report, crawled within minutes. On `ga_merchandise_store_sessions` (2026-11-25) Andrej found that reason answers only the label's delay, not the time a refit takes ("The model to predict new samples still has to be trained after all"), and chose a one-day gap. He had already decided the same on `fugaku_hpc_job_failure` (2026-11-24, issue 7, D).
  - Same structure here: the rows are dated page visits, windows are one month, the refit is monthly and assumed, and the label is known within the day.
  - Cost, measured on the definition's rows (404,979):

    | Window | Rows on the previous month's last day | Phishing among them | Training share now | With a 1-day gap |
    |---|---|---|---|---|
    | Jul 2025 | 2,803 | 417 | 61.6% | 60.9% |
    | Aug 2025 | 2,524 | 218 | 75.7% | 75.1% |
    | Sep 2025 | 203 | 203 | 89.3% | 89.2% |

    Every window stays above the 50% floor. ROC AUC with the gap is not measured.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | No gap, because a filter vendor pushes refits within hours of the feeds (the AI's best guess at a fact that would set this case apart; recorded as an exception to the two precedents) | keeps the newest day; the paper stresses real-time detection | the source states no deployment lag or cadence, so the fact is assumed, not documented |
  | b | One-day gap (`TemporalSplits(..., gap=1, gap_unit="days")`), as on fugaku and ga_merchandise | treats like cases alike; costs at most 0.7 points of training share | the day is assumed; each month's last day trains no model and is tested by none |
  | c | Reopen ga_merchandise and fugaku to match no gap | | reverses two decisions of the last two days |
  | d | Amend SPLIT-10: refit lag only where the source documents one | one rule for all | changes a fresh standing practice |

* **Recommendation:** b. No fact sets this case apart from ga_merchandise, and the cost is under one point of training share (note gap).

Note (gap): SPLIT-10 (Should): "A planning gap the use case has … is a gap too"; its Cases list fugaku_hpc_job_failure_1m and ga_merchandise_store_sessions as applied.

**F2: no `Selection Bias` marker, while every phishing sibling carries one (issue for `## Review`)**

Should PhreshPhish carry `Selection Bias` next to `Class-dependent Recording`, as `website_phishing` and `web_page_phishing_detection` do?

* **Problem:**
  - The two classes were collected apart and partly in different periods. Benign pages come from Webroot telemetry plus "Google search results for heavily targeted brands" (chosen hard negatives); phishing pages come from PhishTank, APWG and NetCraft reports. No benign page exists from November 2024 to May 2025, and on 41 of 210 days there are none. The class share of a day is the collection's schedule, which is why the date was removed as an input.
  - selection.md names exactly this: "cases and controls collected apart or in different periods (… `website_phishing`)". `fit_reason` already describes it ("the mix of the classes follows the collection, not the web"), but neither the record, the builder report nor the README uses the marker or mentions selection.
  - The direct fit can stand: USE-8 allows it when the setting meets the same selection, and the benign side is real browsing. But the marker "stays either way" (Lennart, 2026-10-27).
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | No marker, because the benign pages are real user browsing, not a top-site list, so the rows are drawn from what a filter meets (the AI's best guess at the fact that sets it apart; recorded as an exception) | the benign side really is closer to the deployed population than any sibling's | the phishing side is still feed reports collected apart, the hard negatives are chosen, and the month-by-month mix is the crawler's |
  | b | Add `Selection Bias`; fit stays direct, `fit_reason` names the selection | follows website_phishing, web_page_phishing_detection and naticusdroid; costs nothing; verdict stays `Yes` | none of substance |
  | c | Remove the marker from the siblings to match | | goes against selection.md's own example |
  | d | Amend the selection rule: telemetry-sourced controls do not count | | a single case |

* **Recommendation:** b (note marker).

Note (marker): The `Selection Bias` marker (selection.md, "Selection bias"; Andrej, 2026-10-20; Lennart, 2026-10-27) and USE-8 (Must): the marker does not by itself make the fit approximate, and it stays either way.

One more point under F2, not an issue of its own: the query string is now stripped from every URL to remove a class-dependent artefact. A deployed filter would see the query, so this is a change to the task made to avoid a leak. USE-8 makes a fit approximate only when that change is large, and its size is unmeasured: the URL-only score with and without the query on phishing pages would settle it. It does not alter the recommendation above.

</details>

<details><summary>Blind review</summary>

I've finished the data checks and read the source, and I'm writing the verdict now.

**Verdict:** Include with changes. This is a real, current, large phishing-detection task with a sound time-based split and real but not trivial signal (LightGBM AUC 0.92 on later months). The free-text `url` column needs to be dropped or declared as text, and users should know that "benign" means pages popular with Webroot users, not average web pages.

**What the task is.** A browser-security or email-gateway vendor scores a page right after it is rendered and decides whether to block it or warn the user. That is a real, high-volume use. The source says pages were rendered with Selenium/Chrome "within minutes of being reported to our feeds". Phishing pages come from PhishTank, APWG and NetCraft. Benign pages come from "anonymized browsing telemetry from over six million global Webroot users and Google search results for heavily targeted brands". The licence is CC-BY-4.0, with the note "should only be used for anti-phishing research".

**My checks**
- **Size and classes:** 404,979 rows and 52 usable features (URL lexical counts, HTML structure counts, language). 25% of rows are phishing, and the share varies by month from 15% to 60%.
- **Dates:** rows run from 2024-08 to 2024-10, then nothing until 2025-06, then through 2025-09.
- **Time-based fit:** I trained LightGBM on 2024 rows and tested on 2025 rows (166k).
  - All features: AUC 0.924, average precision 0.868.
  - URL features only: AUC 0.866.
  - HTML features only: AUC 0.893.
  - So there is strong signal, it is not saturated, and it degrades over time, which is good for a benchmark.
- **Duplicates:** 7,781 rows have exactly the same feature values as another row (1,425 groups), and none of those groups has conflicting labels. Every URL is unique.

**Concerns, most serious first**

1. **The `url` column is a raw string that is unique on every row.**
   - It cannot go into a tabular method as is. As a categorical it is a pure identifier, and splitting out its host invites memorisation.
   - 62% of benign test hosts already appear in train, against 4.5% of phishing test hosts. Top benign hosts: en.wikipedia.org 10,986 rows, reddit 3,623, docs.google 3,505.
   - A "host seen before" lookup would therefore score very well. You can argue that is realistic as an allowlist, but it is not what a tabular benchmark is meant to measure.
   - **Change:** drop `url`, or mark it explicitly as a text or identifier column excluded from inputs. The 30-odd lexical features already capture it.

2. **The two classes were collected by different processes, which creates shortcut features.**
   - Benign pages are popular, mature sites. Phishing pages are kits on free hosting: gitbook.io 11.9k, webflow.io 7.8k, vercel.app 4.3k.
   - The gaps are large. Mean `n_links` is 212 for benign and 32 for phishing; on its own it reaches AUC 0.80 (inverted). `host_www` is 0.59 for benign and 0.06 for phishing. Mean `n_divs` is 368 vs 117.
   - The paper itself notes the HTML size gap: median about 250k vs 35k characters.
   - This matches what a telemetry-fed deployment actually sees, so I don't consider it disqualifying. But scores will overstate performance against hard negatives (small benign sites, login pages).
   - **Change:** state this in the task description. Optionally add a stratified evaluation, for example scoring login-form pages only.

3. **The split has a seven-month gap and the class mix shifts.**
   - There are no rows from 2024-11 to 2025-05.
   - The phishing share swings: 15% in Aug-24, 60% in Oct-24, 40% in Jun-25, 16% in Sep-25.
   - The time ordering is honest. `date` is the collection date and is correctly excluded from inputs.
   - However, the 3 test windows will have different base rates, so threshold metrics will not be comparable across windows.
   - **Change:** use AUC or log-loss averaged per window, and report each window's base rate. Make sure the first test window is not the small Jun-25 batch (11k rows).

4. **Near-duplicate phishing kits.** Kit families repeat across hosts, for example "trezor" and "walletconnect" clones on gitbook and webflow.
   - The upstream release removed near-duplicate test pages with TF-IDF and LSH. This subset may not follow the upstream train/test boundary, because its 2025 rows include data from the v1.0.1 addition.
   - Within a split, these kits mainly make the task easier. Across time, they mirror real kit reuse, so I rate this minor.

5. **Preparation is otherwise sensible.**
   - Counts are integers, shares are floats, and `lang` is a categorical with 86 levels.
   - `lang`/`lang_score` are missing for 1.4% of rows; that is natural and should be left missing.
   - No training weight is labelled.
   - The source's `target` field (the impersonated brand) has correctly been dropped, since it is only known for phishing pages and would leak the label.

**Labels and realism.** The data is real: scraped pages with plausible values and recognisable hosts. Label quality looks good. The source reports manual rejection rates of 0.97% for phishing and 0.02% for benign, but also says "we do not claim that our dataset is free of all errors", and notes that redirects to the real brand page can create mislabelled phishing rows.

**What I could not check**
- I could not reproduce the feature extraction from HTML, because there is no HTML in the clean room, so I could not verify the counts.
- I could not tell which upstream split (train/test, v1.0 or v1.0.1) each row comes from, or why 2024-11 to 2025-05 is missing.
- I could not see the exact boundaries of the 3 test windows.
- I don't know whether any benign host was itself later used for phishing.
- I read only part of the paper verbatim. Its later sections reached me as a summary.

</details>

<details><summary>Task gamer</summary>

**Verdict:** the task can be gamed by about 0.01–0.045 AUC. The gain comes from one transductive trick: count how many rows on the same `date` share a host, a registered domain or an exact HTML-count fingerprint. Phishing arrives in same-day bursts in the feeds the data came from, and that burst signal is mostly a product of how the data was collected, not something a deployed browser model would see. Every other attack found nothing.

Splits are listed as r0 = Sep 2025, r1 = Aug 2025, r2 = Jul 2025. The honest baseline is untuned LightGBM on `features()` minus the raw `url` string: **0.9550 / 0.9820 / 0.9306**. As a noise check, refitting with bagging seeds gives a spread of about ±0.003 on each split. Adding a column of random numbers changed nothing at all, so the seeds are the noise reference.

| # | Exploit | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|
| 1 | Same-day counts of host, domain and HTML fingerprint, using all rows with the same `date`, later ones included | 0.9550 / 0.9820 / 0.9306 | 0.9855 / 0.9909 / 0.9753 | +0.031 / +0.009 / +0.045 | Partly at best: see below | Test on single-day windows, or drop rows that repeat a host or HTML fingerprint on the same day |
| 1b | Same, plus counts over past days and future days | same | 0.9894 / 0.9935 / 0.9827 | +0.034 / +0.012 / +0.052 | No: future rows | as above |
| 1c | Counts within the whole test window (no `date` used) | same | 0.9756 / 0.9869 / 0.9377 | +0.021 / +0.005 / +0.007 | No | as above |
| 1d | Counts over the whole table | same | 0.9737 / 0.9877 / 0.9390 | +0.019 / +0.006 / +0.008 | No | as above |

**How #1 works.** Phishing URLs come from feeds (PhishTank, APWG, Netcraft), and one kit or campaign lands on many hosts or paths on the same day. In a test window, rows whose HTML fingerprint repeats are 82–84% phishing; unique ones are 9–12%. The fingerprint is the exact tuple of all the `n_*` counts plus `title_length`, `external_link_share` and `lang`. The count by itself scores AUC 0.74–0.75 with no model.

The information is all in the same day. Counts over past days only, which a deployed model could have, add nothing (0.9566 / 0.9839 / 0.9293). Counts over future days alone add little (0.9603 / 0.9827 / 0.9296).

I also simulated a streaming counter that only sees pages earlier on the same day, using a random order within each day. It keeps most of the gain (0.9760 / 0.9907 / 0.9675). So whether this is a leak depends on one fact: does the deployed model's input stream look like this one? A scorer for feed submissions would see bursts like these. A browser plugin classifying pages as users open them (the stated prediction point) sees user traffic, where a host recurring today mostly means a popular benign site. Under the stated prediction point I count it as an exploit.

**Mildest fix.** Make each test window a single day, so there is no within-window burst to count. Alternatively, collapse same-day clusters (same host or same HTML fingerprint) to one row each in the test windows.

**Flaw that hurts an honest model**

| What is wrong | Honest choice | Baseline | Honest choice score | Fix |
|---|---|---|---|
| The 2024 training rows come from a different process. The source paper removed 2025 rows that looked like any 2024 row (its TF-IDF "leakage filter"), but left 2024 rows untouched. Among phishing rows, the share whose domain was already seen falls from 77% (Sep 2024) to 31–39% in 2025; for benign rows it stays at 67–75%. | Train on 2025 rows only | 0.9550 / 0.9820 / 0.9306 | 0.9592 / 0.9861 / 0.9338 (+0.004 / +0.004 / +0.003, about the noise level) | Drop the 2024 rows, or say in the task that the source's train and test parts were filtered differently |

Exploit #1 on top of the 2025-only model scores 0.9865 / 0.9930 / 0.9676, so the gain is about the same as over the baseline.

**Attacks that found nothing**

- **Row order:** the rows are sorted by date and shuffled within each day. Position within the day has AUC 0.50. Agreement between neighbouring rows' labels is 0.733 against 0.733 expected.
- **URL format:** no scheme, query or fragment survives for either class. `url_length`, `path_length` and `host_length` match the string apart from a constant offset. A model with TLD, uppercase count and trailing slash added: 0.9570 / 0.9826 / 0.9309, which is noise.
- **Numeric formats:** `lang_score` has the same decimal precision in both classes. Gaps in whole-number share and missing values have plain explanations. `host_digit_share` is a whole number when the host has no digits. `external_link_share` is NaN when the page has no links, and 65% of those rows are phishing. These describe the page, so a deployed model has them. A model on format features alone scores 0.67–0.74, all of it from that meaning.
- **Domain target encoding from training labels:** this is legitimate signal, not an exploit, and the result is mixed. Time-respecting encoding: 0.9399 / 0.9911 / 0.9534, worse on Sep and better on Jul/Aug. Encoding with random out-of-fold splits: 0.9338 / 0.9777 / 0.9603.
- **Copies across the split:** there are no duplicate URLs. 4–10% of test HTML fingerprints also appear in training, and the training label agrees 97–99% of the time. That is legitimate past history, and the tree already captures it.
- **Train-vs-test classifier:** AUC 0.71–0.75 (on an 80k subsample). This is ordinary drift, and it gives no route to the label.
- **Weight and global transforms:** there is no training weight. No column is standardised or rank-transformed over all rows.

**Could not check**

- **Web search:** this dataset has no competition forum or "leak" threads. The only source I read is the arXiv paper; it is where the leakage-filter and feed details come from.
- **Looking rows up in the published file:** `url` is a unique key, so finding rows in the Hugging Face release would almost certainly work. I did not download it, and per the instructions it is not ranked.
- **What the kit changed from the source:** I did not compare the kit with the source file. The 2025 base rate (16–40%) is below the paper's 46%, so the kit likely subsampled; I did not verify how.

</details>

<details><summary>Advocate: opening brief</summary>

**Advocate's opening brief: `phreshphish_phishing_pages`**

**Position:** ship it. Make the definition fixes below first. Every problem the panel found can be fixed inside the definition (remedy ladder, step 2). None needs the dataset excluded.

**1. It is the phishing task the benchmark has been missing, and no other open source does it as well (P3, USE-1 Must; P5, PROV-4).**
- **The decision item named it.** `issues/website_phishing.md` gives "no phishing task in the benchmark until a dated table such as PhreshPhish is built" as the downside of option E (no replacement).
- **The alternatives are weaker.**
  - Hannousse has no row dates, one crawl and two lists (Alexa top domains against feeds).
  - UCI 327 has coded scores and 47% repeated rows.
  - PILWD is available on request only.
  - vrbancic and PhiUSIIL were turned down for URL shortcuts that score 0.94 and 0.9998.
- **This dataset has what those lack.** It has 404,979 rows, both classes carry the same collection date, and benign pages come from real browsing telemetry rather than a top-sites list.
- **The domain practitioner backs it:** "the plug-in or gateway is already the right one" (USE-9), and "I would use a model trained on this as a client-side first filter."

**2. The split matches how a filter is deployed and meets every floor (P4: SPLIT-14 Must, SPLIT-15, SPLIT-13).**
- **The split auditor calls it "right with notes".** It reaches the leaf L-ORDER.windows, and the tree forces no answer.
- **The floors are met.** The training sides hold 61.6%, 75.7% and 89.3% of the rows, all above the 50% floor. The three windows are the target count. The smallest phishing count in a test window is 7,161.
- **The date is not an input.** This follows `bank_marketing` (precedent check, row 2). The claim auditor confirmed it: on Sep 1 there are 725 phishing pages and no benign ones.
- **Concession: add a one-day gap.** The precedent checker's F1 is right that no fact sets this dataset apart from `ga_merchandise_store_sessions` and `fugaku_hpc_job_failure` (SPLIT-10, Should). The gap costs at most 0.7 points of training share. This is a split-parameter fix, not an objection to the dataset.

**3. The class-dependent recording was handled carefully, and what is left is small and fixable (LEAK-13 Must, fixed in the definition).**
- **The builder already removed four artefacts:** the scheme, the query, the copies and the DOCTYPE months.
- **No shallow rule separates the classes.** A depth-2 tree scores 0.765, the best single feature 0.796, and the URL format test is at noise level (task gamer). The datasets turned down for shortcuts scored 0.94 and 0.9998.
- **Concession: the column auditor's 10,000-character size floor is a real LEAK-13 problem.** In each test window, "under 10,000 characters" marks phishing with precision 1.00.
  - **Fix:** record the raw HTML length but do not use it as a feature, and drop every page under 10,000 characters for both classes.
  - **Measured cost:** the mean score goes from 0.9591 to 0.9555, and 3,207 test rows are removed (all phishing).
  - **Why this outranks retirement:** the remedy ladder says to fix the definition, and step 3 of "how to decide" says to fix a leak and keep the task.
- **Concession: also tighten `canonical_url`.**
  - Strip `[&,+;=]` and non-ASCII characters (claim auditor R1). This affects 0.3–0.5% of phishing test rows, with an effect under 0.005.
  - Lower-case the host and drop `:80` and `:443` (column auditor, finding 2).

**4. The task is worth benchmarking: it is neither easy nor saturated, and it separates methods (P6, TP, MET-2).**
- **Forward scores:** LightGBM 0.953–0.964, a linear model 0.927, a depth-2 tree 0.765.
- **Outside view:** the blind reviewer's 2024→2025 fit scores 0.924, and they call that "not saturated, and it degrades over time, which is good for a benchmark."
- **Every fold can be scored:** a constant prediction gives 0.5 and a random one 0.4975–0.5024 on all three folds.

**5. The task gamer's "same-day burst" exploit and the blind reviewer's `url` objection are not defects of the data.**
- **The burst gain needs test rows.**
  - With past rows only, which a deployed model would have, it adds nothing: 0.9566 / 0.9839 / 0.9293 against a baseline of 0.9550 / 0.9820 / 0.9306.
  - The gain comes only from counting rows of the same test window. The protocol forbids that: fit on `train_idx`, then predict each test row.
  - LEAK-30 covers transforms we apply over all rows, not a participant reading test-set statistics.
  - This is a separate failure, not a conflict with another rule. It is a protocol matter, and nothing in the definition should change.
- **Shipping `url` as text follows precedent.** `phiusil_phishing` and `drug_induced_autoimmunity_prediction` accepted the URL as a task input. It is typed `string`, not categorical, so it is not an id.
- **Recurring hosts are part of the task.** A filter meets wikipedia.org and gitbook.io again (SPLIT-13). The domain practitioner says keeping one row per URL "matches my real job."

**6. The September pruning is real, but its effect on scores is not proven, and a note is the mildest fix (SPLIT-15 Should, LEAK-42).**
- **Concession: the source thinned September.** From 2025-09-08 on, the source removed pages that repeat earlier ones. Exact HTML repeats among phishing pages fall from 9.0% to 0.4%, and 74% of the window comes from the source's test split.
- **The score effect does not separate.**
  - The claim auditor saw July drop just as much with no pruning: 0.993 against 0.914 on the same day boundary. It concluded that the score gap "is not separable."
  - The split auditor reads it the other way: training up to Sep 8 still gives only 0.950.
  - Either way, the pruning makes the window harder, not easier, so no score is inflated.
- **Remedy ladder:** option (a), write it down in the splits comment with the numbers. Option C (end the data on 2025-09-07 and use 4-week windows, dropping 32,255 rows) is acceptable if the curator wants every window to be one population. It is a weighing call, not a Must.

**7. The metric, the markers and the wording can be fixed without changing the verdict (MET-2, MET-5, MET-9, MET-11; the Selection Bias marker; USE-8).**
- **The `roc_auc` fallback holds, on a different ground.**
  - The source scores average precision at base rates of 0.05–5%. Our folds run at 16–24% phishing, so the source's average precision would measure something else here (MET-2, MET-9).
  - Concession: rewrite the reason. It should not say MET-5, and it should not say "15% to 90%". Set `original="average_precision"` and cite Sec. 5.1 as the reference.
- **Partial AUC (the domain practitioner's proposal) is not in the metric registry.** The best model ranks the same under every score, so keep `roc_auc` and state the gap at low false-positive rates.
- **Concessions, all cheap:**
  - Add the `Selection Bias` marker (precedent checker, F2, option b; the verdict stays `Yes`).
  - Set `fit="approximate"`. The `fit_reason` already names the gaps.
  - Type the six 0/1 flags as categorical (CLEAN-14).
  - Cap `title_length`.
  - Correct three numbers: 367,989 benign pages (not 368,989); 1.46% and 0.27% of pages under 200 characters (not 1.75%); and the month range in the metric reason.

**Judgment record**
- **Verdict:** ship after changes.
- **Validity:** USE-1 holds. LEAK-13 was triggered and fixed in the definition, with the size floor and the URL characters added. SPLIT-14 holds. SPLIT-10 gets a one-day gap.
- **Value:** non-trivial, and methods separate.
- **Quality:** the flag dtypes, `title_length` and the wording are fixed.
- **For the curator:** the September pruning (a note, or end the data on Sep 7) and the metric (`roc_auc` with the gap stated, or a new partial AUC).

</details>

<details><summary>Critic: opening brief</summary>

**Verdict: ship only after changes.** The task is real and none of the points below calls for exclusion. Two Must problems are still in the definition: a class-dependent recording leftover in the HTML and the URL (LEAK-13), and a newest window that is mostly a different population (SPLIT-15 / SPLIT-5). Fixing them is cheap.

**1. The fit is labelled `direct`, but its own reason names gaps, and the `Selection Bias` marker is missing (USE-8, Must; P3).**
- **Problem:** `fit_reason` already says "the mix of the classes follows the collection, not the web" and "the features are ours, not a product's". The task also changed a lot to avoid a leak: the query and the scheme are removed from every URL, though a deployed filter always sees both. USE-8 lists "a task changed a lot to avoid a leak" under approximate.
- **Effect:** the curator reads `direct` and assumes the scores carry over to a real filter. They do not: the inputs are ours and cut down, and the benign side includes chosen hard negatives (searches for targeted brands).
- **Evidence:**
  - domain-practitioner §Fit and its first change.
  - precedent-checker F2: `website_phishing`, `web_page_phishing_detection` and `naticusdroid` all carry `Selection Bias`. selection.md names "cases and controls collected apart or in different periods (… `website_phishing`)". Here no benign page exists from November 2024 to May 2025, and none on 41 of 210 days.
- **Remedy:** set `fit="approximate"`, have `fit_reason` name the three gaps, and add the `Selection Bias` marker to the record. The verdict stays `Yes`.

**2. Benign and phishing pages have different minimum HTML sizes, and the tag counts carry it (LEAK-13, Must; P4).**
- **Problem:** from 2024-08-19 on, no benign page is shorter than 10,000 characters. From September 2024 the shortest benign page each month is 10,000 to 10,114 characters, which looks like a floor the release applied to one class. The phishing floor is 1,000 characters, then 5,000 from April 2025.
- **Effect:** in the test windows, 8.9%, 8.9% and 12.7% of phishing pages are under 10,000 characters and no benign page is. The rule "under 10k, so phishing" has precision 1.00 in every window. Page length is not a feature, but the tag counts recover it at ROC AUC 0.998. This is the same kind of artefact the builder already removed for the DOCTYPE, and the "kept, as a filter meets such pages too" note is wrong: the release drops small benign pages.
- **Evidence:** column-auditor finding 1.
  - All features, shipped windows: 0.9322, 0.9846, 0.9604.
  - With a 10k floor for both classes: 0.9252, 0.9855, 0.9559 (July −0.007).
  - The measured effect is small, but LEAK-13 is not graded by size. It says "First measure how much the fix removes", then harmonise.
- **Remedy:** record the raw HTML length in `_prepare_raw_files` (never as a feature) and drop pages under 10,000 characters in every month, for both classes. That removes 3,207 test rows, all phishing. Then rewrite the "Anomaly" note.

**3. The URL still differs in form by class (LEAK-13, Must; P4; small).**
- **Problem:**
  - Benign URLs contain no `&`, `,`, `+`, `;`, `=` and no non-ASCII character. All 10,986 benign Wikipedia URLs had their commas stripped.
  - 137 phishing hosts are written in upper case, against 0 benign, and 61 phishing URLs carry an explicit `:443`.
- **Effect:** through `url`, these characters mark 0.3–0.5% of phishing test rows with no false positive. The score effect is under 0.005 AUC. Still, it contradicts the README's claim that the URL is read "in one form for both classes".
- **Evidence:** claim-auditor R1; column-auditor finding 2.
- **Remedy:** in `canonical_url`, lower-case the host, drop `:80` and `:443`, and remove `[&,+;=]` and non-ASCII characters from every URL. Add one line to the LEAK-13 bullet.

**4. The deployment window is three quarters filtered by the source (SPLIT-15, Must for the newest window; SPLIT-5, Must; LEAK-42).**
- **Problem:** September 8–30 is the source's own test split, from which it removed near-duplicates of training pages. July, August and September 1–7 keep reused kits, as this definition chose on purpose (LEAK-42, natural). So the deployment window mixes two populations, and 74% of it (32,255 rows) has the opposite treatment.
- **Evidence:**
  - Phishing pages whose tag signature was seen before the period: 21% in July, 28% in August, 32% on Sep 1–7, then **3.7% on Sep 8–30** (split-auditor).
  - Exact HTML repeats among September phishing pages fall from 9.0% before the 8th to 0.4% after, while July and August keep 4.7–6.8% after the 8th (claim-auditor 14).
  - Phishing pages a day fall to 43% of August's level, while total rows a day stay at 82%. Rows are kept and outcomes dropped, so the `time_newest_period_short` warning stays silent.
  - On scores, the evidence is mixed and I rest nothing on them. The split-auditor attributes the Sep 8–30 drop (0.991 to 0.941, 0.950 even when trained up to Sep 8) to the pruning. The claim-auditor sees a similar drop in unfiltered July (0.993 to 0.914). The repeat-rate evidence stands on its own.
- **Remedy:** filter, not exclusion. End the data on 2025-09-07, the last day of the source's train split, and re-cut into three 4-week windows (split-auditor option C). The newest window then has 51.3k rows on 86.2% training, and the oldest trains on 3.6k rows from 2025. The weakest acceptable fallback is a note in the splits comment that says plainly the deployment window is mostly pruned. I argue against that fallback, because SPLIT-15 asks the newest window to stand for deployment.

**5. No gap, against two decisions of the last two days (SPLIT-10, Should).**
- **Problem:** "a label known in minutes" answers only the label's delay, not the time a refit takes. Andrej chose a one-day gap for exactly that reason on `ga_merchandise_store_sessions` (2026-11-25) and `fugaku_hpc_job_failure` (2026-11-24). No fact sets this case apart.
- **Cost:** training share falls by at most 0.7 points (61.6→60.9, 75.7→75.1, 89.3→89.2). All windows stay above the floor.
- **Evidence:** precedent-checker F1.
- **Remedy:** `gap=1, gap_unit="days"`, or a stated exception naming the fact that sets this case apart.

**6. The metric reason is wrong, and ROC AUC misses the operating region (MET-1 and MET-11, Must; P6).**
- **Problem:**
  - The reason calls the paper's metrics "two metrics with no one deliberate choice". In fact Sec. 5.1 argues for precision-based scoring from the cost of false positives.
  - It quotes a "15% to 90%" base rate; the kept test windows run 16.5–24.4%.
  - The spec sets `original=None` although the source has a metric.
- **Effect:**
  - At a false-positive rate of 1% or less, where the actor sets its threshold, models rank differently than under ROC AUC.
  - The URL-only model is last of the three weaker models on ROC AUC and first of them on pAUC (FPR ≤ 1%), TPR at 0.1% FPR and AP at 1% phishing.
  - The order of models also flips within single windows.
- **Evidence:** claim-auditor R2 and claims 18–19; domain-practitioner §5.
- **Remedy:**
  - Rewrite the reason on MET-2/MET-9: the source scores at 0.05–5% base rates, ours are 16–24%.
  - Set `original="average_precision"` with Sec. 5.1 as the reference.
  - Put to the curator: a `context` metric, standardised pAUC at FPR ≤ 1% (it needs a registry entry), or keep `roc_auc` with the measured reversals written into the reason.

**7. A same-day burst exploit, and quality items (LEAK-9, Should; CLEAN-14, Should; text).**
- **Evaluation leak:** counting how many test rows of the same day share a host or an HTML fingerprint adds +0.031, +0.009 and +0.045 AUC (task-gamer #1). Counts over past days only add nothing, so this signal exists only inside the test block. The fix is a protocol line in the notes ("methods that read other test rows are not benchmarked"), not a change to the data.
- **Quality, not a reason to exclude:**
  - Five 0/1 flags are typed int64 and should be categorical (CLEAN-14; column-auditor 4).
  - `title_length` overruns (73 rows over 500 characters).
  - Wrong numbers: 368,989 should be 367,989 benign; under-200-character pages are 1.46% / 0.27%, not 1.75%.
  - "Downsampling by an amount it does not give" is now measurable against v1.0.0 (column-auditor 3).

</details>

<details><summary>Advocate: rebuttal</summary>

**Advocate's rebuttal: `phreshphish_phishing_pages`**

We agree on the verdict: ship it after changes, with no exclusion. We agree on most of the remedies. Two disagreements remain: what the September pruning calls for (critic's point 4), and how much weight the operating-region evidence carries against `roc_auc` (point 6).

**1. Fit `direct` → `approximate`, and add the `Selection Bias` marker (USE-8): concede.**
- I conceded both in my brief (point 7).
- The critic adds a fact I accept: the task changed a lot to avoid a leak, because the query and the scheme are removed from every URL. That is one of USE-8's own examples of an approximate fit.
- **What follows:** set `fit="approximate"` and make `fit_reason` name three gaps: the class mix comes from the collection, the features are ours, and the URL is cut down. Add the marker. The verdict stays `Yes`.

**2. The 10,000-character size floor (LEAK-13): concede in full.**
- This is the same remedy as my point 3: record the raw HTML length (never as a feature), apply the floor to both classes, and rewrite the "Anomaly" note.
- I accept the critic's framing that LEAK-13 is not graded by size. The measured effect (July −0.007) is why the fix is cheap. It is not a reason to skip the fix.

**3. URL form differs by class (LEAK-13): concede.**
- This is the same fix as mine: lower-case the host, drop `:80` and `:443`, and strip `[&,+;=]` and non-ASCII characters.
- Also add one line to the LEAK-13 bullet, because the README's claim that the URL is read "in one form for both classes" is false until this fix lands.

**4. September pruning: I concede the facts, I dispute that a Must is broken, and I now prefer option C over a note.**
- **The facts stand.** The repeat-rate evidence does not depend on any score:
  - phishing pages whose tag signature was seen before: 3.7% on Sep 8–30, against 21–32% in earlier periods;
  - exact HTML repeats among phishing pages: 0.4% after Sep 8, against 9.0% before;
  - phishing pages per day: 43% of August's level.
- **The Must is not broken.** SPLIT-15's Must reads "the newest window is always a test window", and it is. Which periods the windows cover is "Should for the others", argued from statistics. SPLIT-5 is about checking a split the source prescribes. We do not adopt the source's split; we only inherit its filtering, which is a LEAK-42/SPLIT-15 matter. Both rules call for a weighing, not a forced change.
- **But the critic's fidelity argument wins the weighing:**
  - a deployed filter meets reused kits, so a newest window with those kits removed understates what the filter will see;
  - the row count hides the drop, so the `time_newest_period_short` warning cannot catch it.
- **Option C is cheap:**
  - it drops 32,255 rows (8%);
  - the newest window keeps 51.3k rows at 86.2% training;
  - every training side stays above the 50% floor (65.0% / 76.5% / 86.2%);
  - it is a filter, step 2 of the remedy ladder.
- Its one cost is that the oldest window trains on 3.6k rows from 2025, against 11.2k today. This is acceptable because earlier data of both classes sit in the training side too.
- **What follows:** I withdraw "a note is the mildest fix" as my recommendation. Recommend option C, and keep the note as the curator's fallback.

**5. One-day gap (SPLIT-10): concede.**
- This was already conceded (my point 2): `gap=1, gap_unit="days"`. The cost is at most 0.7 points of training share.

**6. Metric: I concede the reason and the original; I dispute that MET-1 forces a change of metric.**
- **Conceded:**
  - rewrite the reason on MET-2/MET-9, using the base rates 0.05–5% against 16–24%;
  - drop "15% to 90%" and "no one deliberate choice";
  - set `original="average_precision"` with Sec. 5.1 as the reference (MET-11 Must).
- **Disputed:** that `roc_auc` fails MET-1.
  - The best model is the same under ROC AUC, pAUC (FPR ≤ 1%), TPR at 0.1% FPR and AP at 1% phishing (domain-practitioner).
  - The order flips only among the three weaker models.
  - pAUC needs a new registry entry. A metric chosen because it spreads models wider (0.65–0.82 against 0.91–0.96) is not, by itself, a reason to switch ("task fidelity over separability").
- **The fidelity argument for pAUC is real:** the actor works at an FPR of 1% or less. So this stays the curator's call, as both of us already framed it.
- **My recommendation:** keep `roc_auc` and write the measured reversals into the reason. Adopt a `context` pAUC if the curator wants the registry entry.

**7. Burst exploit and quality items: concede.**
- **The burst exploit:** we agree on the facts (past-only counts add nothing) and on the remedy, a protocol line. That line follows the LEAK-9 precedents (`medical_facility_operational_data`, `loan_default_prediction_imperial_college`): "each test row is predicted from the training rows and its own features only; a method that reads other test rows is not benchmarked."
- **The flags:** I accept the critic's count of five 0/1 flags (column-auditor 4) over the six in my brief.
- **Remaining quality items:**
  - cap `title_length`;
  - correct the numbers (367,989 benign pages; 1.46% / 0.27% of pages under 200 characters);
  - measure the downsampling against v1.0.0 and state the amount.

**Where this leaves us**
- **Verdict:** ship after changes.
- **Changes:**
  - the size floor and the URL fixes (LEAK-13);
  - fit `approximate` and the `Selection Bias` marker;
  - the one-day gap;
  - option C for the windows;
  - the metric reason and `original`;
  - the protocol line;
  - the dtypes and the numbers.
- **One open weighing call for the curator:** `roc_auc` with the reversals stated, or a new pAUC (FPR ≤ 1%) `context` metric.

</details>

<details><summary>Critic: rebuttal</summary>

**Critic's rebuttal: `phreshphish_phishing_pages`**

The advocate and I now agree on the verdict, which is to ship after changes, and on most of the fixes. Two points remain in dispute: how to treat the September pruning, and what the metric reason should say.

**Advocate 1: the task is real, alternatives are weaker.** Conceded. I never asked for exclusion.

**Advocate 2: the split meets every floor; a one-day gap is added.** Conceded. Their gap concession settles my point 5 (SPLIT-10).

**Advocate 3: the size floor and `canonical_url`.** Conceded. Their fixes are the ones I asked for in points 2 and 3. The release ships with them.

**Advocate 4: the task is not trivial and separates methods.** Conceded.

**Advocate 5: the same-day burst and `url` as text.**
- **`url` as text:** conceded.
- **The burst:** partly disputed. We agree it is not a defect of the data and that the dataset does not change. But "the protocol forbids it" holds only if the protocol says so where a participant reads it. The participant kit had no such line, and the task gamer used the exploit. My remedy stays: one protocol line in the notes saying that methods which read other test rows are not benchmarked (LEAK-9, Should). It costs nothing.

**Advocate 6: the September pruning gets a note.** Disputed.
- **Wrong strength:** the advocate files this under "SPLIT-15 Should". SPLIT-15 is **Must for the newest window** (splits.md l.609, amended 2026-11-10). The September window is the newest.
- **Wrong evidence:** the advocate's case rests on scores ("the score effect does not separate", "harder, not easier, so no score is inflated"). SPLIT-15 says: "The evidence is statistics of the data, never a model's score." Neither side should argue this point from scores, which is why I dropped them from my brief.
- **The statistics are not in dispute.** The advocate concedes all three:
  - exact HTML repeats among phishing pages fall from 9.0% to 0.4%;
  - 74% of the window comes from the source's de-duplicated test split;
  - earlier windows keep reused kits by design (LEAK-42).
- **What follows:** the newest window does not stand for the deployment period the other windows were built to represent. That breaks the Must.
- **"No score is inflated" misses the point.** SPLIT-15 is about representativeness, not inflation. A window that is harder for an artificial reason can still reorder methods.
- **The remedy is a fix, not an exclusion.** Option C ends the data on 2025-09-07 and re-cuts it into three 4-week windows. That keeps the task, all three windows and the floors (86.2% training share in the newest window). It does drop 32,255 rows. A note is acceptable only for a Should. For this Must, the fix is available and cheap, so the fix wins (remedy ladder).

**Advocate 7: the metric, the marker, `fit` and wording.**
- **Conceded:**
  - add the `Selection Bias` marker;
  - set `fit="approximate"`;
  - make the flags categorical;
  - cap `title_length`;
  - correct the numbers;
  - set `original="average_precision"` with Sec. 5.1 as the reference;
  - rewrite the reason on MET-2/MET-9.
- **Flag count:** the advocate says six 0/1 flags, column-auditor finding 4 lists five. This is a quality item; the curator should check the list.
- **Disputed: "the best model ranks the same under every score."** That is true, but it is not the test. A benchmark ranks all methods, not just the top one. The domain practitioner measured that ROC AUC puts the URL-only model last of the three weaker models, while every low-false-positive score puts it first. The order also flips within single windows (domain-practitioner l.74–75).
- **What I ask for:** keep `roc_auc` if the curator prefers no new registry entry, but the reason must state those measured reversals, not only "a gap". Whether to switch to partial AUC at FPR ≤ 1% stays the curator's call under MET-11.

**Where this leaves the panel**

All of my points have a fix inside the definition. Two weighing calls go to the curator:
1. **September:** I argue that SPLIT-15 is a Must here, so end the data on 2025-09-07 rather than add a note.
2. **The metric:** keep `roc_auc` with the reversals written into the reason, or switch to partial AUC.

</details>
