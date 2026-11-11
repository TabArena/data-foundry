---
unique_name: aeolus_rebuilt
name: US flight delays with weather (Aeolus rebuilt from BTS and Meteostat)
checked_by:
- Lennart
data_foundry_status:
- 'DF: Yes'
suggestion: 'Yes'
priority: 2
decision_markers:
- Needs extensive data wrangling
tags:
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
original_source: GOV Website
year: '2026'
domain: industry & manufacturing
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FGJ
- https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=FLL
- https://dev.meteostat.net/data/timeseries/hourly
- https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv
v2_path: datasets/_dev/tabarena-v0pt2/aeolus_rebuilt_1m/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Created on 2026-10-26 at Lennart's ask (aeolus, REVIEW issue 8): rebuild the Aeolus task from its origins, the BTS Reporting Carrier On-Time Performance table and Meteostat's hourly station weather, joined in UTC at the last reading before the scheduled departure, instead of the Aeolus release's weather join (local clock times read as UTC). A rebuild from other sources is a new dataset with its own record (PROV-11, PROV-14).

CC (2026-10-26, Lennart): "Can you rebuild this please, but keep it aeolus_correct or something? I assume we have all the information we need from the original sources, or is the data release from aeolus / the paper the only source of some information? if the paper state does not add much, we can build our better version as intended"

**Assessment (AI, 2026-10-26):** The Aeolus release and paper hold nothing this task needs that the origins lack. The Kaggle release has three parts: Flight_Tab (nine yearly CSVs: BTS flights with Meteostat temperature, precipitation and wind at both airports, the airports' coordinates and the authors' airport indexes), Flight_chain (27 PyTorch files of daily sequences) and Flight_network (3,234 daily DGL graphs, March 2024 included). All are built from BTS fields: the chains group by carrier, flight number and date (Sec. 3.2: "Dynamic grouping is then performed using (OP_CARRIER, OP_CARRIER_FL_NUM, DATE)"), not by aircraft as Sec. 1 says ("flights operated by the same tail number"), and the graphs link flights at the same airport at adjacent times (Sec. 3.3). The paper adds the task (delay over 15 minutes, AUC and ACC, App. B.2) and a split we do not follow. The origins give what the release lacks or damaged: the weather of the right hour (the release read it 3.5-11 h early), March 2024 (585,413 operated flights), the 192,954 flights of 43 airports the release dropped, tail numbers (the aircraft's previous flight), cancellations and diversions, and BTS's coordinates. Built as `aeolus_rebuilt_1m` (a `_1m` version, as the row budget requires) from the BTS on-time files, the BTS Master Coordinate table, NOAA's ISD station history and Meteostat: 13,708,650 operated flights of 2023-2024, aeolus_1m's three two-week windows, 34 features. With aeolus_1m's inputs the weather of the right hour adds 0.043-0.051 ROC AUC per window against 0.032-0.039 in aeolus_1m; the aircraft's previous flight adds 0.15-0.17, to 0.80-0.83 (untuned LightGBM, 1M training rows). Open for the curator: the aircraft-swap potential leak, cancelled flights as rows, the prediction point, and retiring aeolus_1m once this is accepted (PROV-6).

CC (2026-10-26, Lennart): issue 1: keep the operated flights only, "so we do not have these as rows in the data and could use the model as intended".

CC (2026-10-26, Lennart): issues 2 and 3 as implemented: the prediction point at the full hour before departure; the previous flight's columns kept with the note on aircraft swaps.

CC (2026-10-26, Lennart): issue 4: keep Meteostat's forecast-filled values, "remark this at least, this is good to know as a model-dependent outcome!"

CC (2026-10-26, Lennart): issue 6: "keep roc auc and label it as you see fit": the fallback (MET-5: the paper reports AUC and accuracy side by side).

CC (2026-10-26, Lennart): the record's year takes the definition's value (2026, the pinned snapshot).

**Assessment (AI, 2026-10-26):** applied: the remark on the model-filled weather in the notes, the metric relabelled as the fallback (same ROC AUC). No open issue is left, so the folder's REVIEW.md is removed; the review panel has not run (the curator's call of 2026-10-26).

CC (2026-10-26, Lennart): verdict ship.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `O_COCO` (a partial order); `D_COCO` (a partial order); `INBOUND_STATUS` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 columns with a state outside the scale ordered, the state placed by the rule.

CC (2026-11-10, Lennart): REVIEW issue 1 (which fortnights of 2024 to test), "Option B: Holidays, July, March.": the test windows are 18-31 December, 3-16 July and 13-26 March 2024 instead of the newest six weeks (20 November to 31 December 2024) carried over from aeolus (its CC of 2026-10-12), under SPLIT-15 as amended on 2026-11-10.

CC (2026-11-10, Lennart): the declared horizon (14 days, a one-day gap, windows starting 2024-12-18, 2024-07-03 and 2024-03-13) is checked, kept for a new reason: no source states a refit cadence (the paper tests about three days after nine), and two weeks keep a window under the 500k-row test cap and spread a single storm or outage over fourteen days, while the cutoffs choose the seasons.

**Assessment (AI, 2026-11-10):** applied in dataset.py: `temporal` with the three cutoffs; test 264,245, 278,071 and 267,477 flights, train 13,426,458, 10,166,861 and 7,987,461 (97.9%, 74.2%, 58.3% of the 13,708,650 operated flights); the 17,947 flights of 2024-12-17, the newest window's gap day, are in no split, so the container holds 13,690,703. Cancelled and diverted flights are 1.44%, 1.96% and 1.16% of the scheduled flights of the three windows (the fit reason now says 1.2 to 2.0%; 0.4 to 1.4% on the old windows). `task_summary.split`, `splits_comment`, `TEST_WINDOWS` (the cancellation evidence table) and the row-budget note rewritten; the per-window scores and probe results in the notes are labelled as measured on the windows before 2026-11-10. Horizon audit (split-auditor, model-free): Xu et al. 2025 (arXiv 2510.26616) Sec. 4.1 split 1-15 June 2024 "temporally-stratified 6:2:2" and name no lead time or refit cadence; "a delay model is refit every two weeks" was copied from aeolus_1m, whose fortnight began with the CC of 2026-10-12; 14 days gives 25 candidates above the floor (17 January to 31 December 2024, 239k to 283k flights each), 7 days about 50, where one event can carry a window (19 July 2024, the CrowdStrike outage, 58.3% late), and a calendar month 11, each over the 500k test cap. `dataset check`: 0 errors, 0 warnings (README not regenerated).

## Review

**Outcome:** added as `aeolus_rebuilt_1m`. Under the rule on choosing test windows, rewritten on 2026-11-10, you chose
B (issue 1): the test fortnights are 18-31 December, 3-16 July and 13-26 March 2024 instead of the newest six weeks,
and the 14-day length and the one-day gap stay with a new reason. Nothing is left open.

**Main points:** Settled on 2026-11-10: the test windows are the holiday peak, the summer peak and a spring fortnight
of 2024 (issue 1, B), and the declared horizon is checked.

**Horizon:**

* **Verdict:** keep the 14-day windows with a new reason (medium confidence): no source states a refit cadence (the
  paper tests about three days after nine); two weeks keep a window under the 500,000-row test cap and spread a single
  storm or outage over fourteen days, while the cutoffs choose the seasons.
* **Length:** the definition's reason, "as in aeolus_1m: a delay model is refit every two weeks", was copied; the
  fortnight began with your call of 2026-10-12 (two-week windows so that only one window falls in the holiday peak).
  Xu et al. 2025 (https://arxiv.org/abs/2510.26616), Sec. 4.1, split 1-15 June 2024 "temporally-stratified 6:2:2" and
  name no lead time or refit cadence.
* **Gap:** one day: a delay is known when the flight lands, and the dates have day resolution.
* **Time frame:** 2023-2024, the Aeolus span; the BTS now publishes monthly files through mid-2026, so adding 2025
  would give windows in another year (a separate rebuild question).
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | Two weeks, one-day gap (implemented) | 14-day windows: 25 candidates above the floor (17 January to 31 December 2024), 264k to 278k flights each | each window under the 500,000-row test cap; a single storm or outage spread over fourteen days | no source states a refit cadence |
  | B | One week | 7-day windows: about 50 candidates | closer to the paper's test of about three days | a single event carries a window (19 July 2024, the CrowdStrike outage: 58% of flights late); no source either |
  | C | A calendar month | 11 candidates | a single event weighs less in its window | every window over the 500,000-row test cap; no source either |

* **Recommendation:** A: no source names a cadence, and two weeks is the length that keeps a window under the test
  cap without letting one event carry it. **Decision:** A, B or C?

**Resolved (2026-11-10, Lennart):** A, kept by the horizon audit, as instructed ("if the current time horizon makes
sense and is justifiable keep it and resolve them"); the record's CC line says the declared horizon is checked, and
`task_summary.split` and `splits_comment` give the new reason.

**Issues for Lennart:**

1. **Which fortnights of 2024 should the test windows be?**

   * **Problem:**
     - The three test windows are the newest six weeks (20 November to 31 December 2024), so the score measures
       early-winter delays only, while an airline or a travel app uses the model in every season.
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, preferring other seasons over the weeks just before the newest[^split15].
     - Every two-week window from 17 January 2024 on keeps at least half the flights for training, so all seasons of
       2024 are open to choose from, while no fortnight of 2023 is[^split14].
   * **Background:** The share of late flights follows the season in both years: by month it is highest in June and
     July (25 to 30%) and lowest in October and November (13 to 16%). The holiday fortnight is late in 2024 (25.9%) but
     was not in 2023 (18.2% from 20 December to 2 January). The two older windows of A are near copies of each other:
     both in the weeks before Christmas (Thanksgiving included), 16.7% and 17.5% late, with the same drift of the
     temperatures.
     The fortnight of 17-30 July holds the CrowdStrike outage of 19 July: 58.3% of that day's flights arrived late and
     92% of Delta's, Delta operated about 40% fewer flights from 19 to 22 July, and its late share stayed above 60%
     through 23 July. The length (two weeks, the refit cadence) and the one-day gap stay as they are[^split12]. Each
     train side of B holds the same season of 2023, so the model has seen each test season once. PSI, the population
     stability index, compares a feature's distribution in the window with its train side; above 0.25 is usually read
     as a large shift.
   * **Statistics:** late shares from all flights; the drift from the candidate table (100,000-row samples of each
     side); 264k to 278k flights per window.

     | Window (2024) | In | Late, test | Late, train side | Train share | Largest drift (PSI) |
     |---|---|---|---|---|---|
     | 18-31 Dec | A, B, C | 25.9% | 20.6% | 97.9% | 1.10, temperatures |
     | 4-17 Dec | A | 16.7% | 20.7% | 96.0% | 1.21, temperatures |
     | 20 Nov-3 Dec | A | 17.5% | 20.8% | 94.0% | 1.09, temperatures |
     | 3-16 Jul | B | 26.9% | 21.1% | 74.2% | 2.43, temperatures |
     | 17-30 Jul | C | 34.0% | 21.2% | 76.2% | 2.22, temperatures |
     | 13-26 Mar | B, C | 21.3% | 20.5% | 58.3% | 0.33, temperatures |

   * **Effect on the task:** Under A, models are ranked by how they handle December traffic. B adds the summer peak,
     when the most flights are late and the weather inputs differ most from training, and a spring fortnight close to
     the year's average (20.7% of all flights late).
   * **Consistency:** Today's windows come from your call of 2026-10-12 on aeolus (two-week windows, one of three in
     the holiday peak)[^split20], made before the rule allowed windows away from the newest weeks; B keeps one window in
     the holiday peak. No dataset has chosen windows under the rewritten rule yet.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/aeolus_rebuilt_1m/dataset.py` (`splits_comment`,
     `temporal`); the records `curation/records/aeolus_rebuilt.md` and `curation/records/aeolus.md` (CC 2026-10-12);
     the candidate table `.venv/bin/python -m data_foundry.curation.cli dataset windows aeolus_rebuilt_1m --root
     datasets/_dev/tabarena-v0pt2` (25 fortnights, 17 January to 31 December 2024).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Newest six weeks (implemented) | tests 18-31 Dec, 4-17 Dec and 20 Nov-3 Dec 2024 | the weeks right after a refit; one window in the holiday peak | November and December only; two windows are near copies |
     | B | Holidays, July, March | tests 18-31 Dec, 3-16 Jul and 13-26 Mar 2024 | winter, summer and spring; the summer peak and its weather shift | the older windows train on 74% and 58% of the flights |
     | C | Holidays, the outage, March | as B, with 17-30 Jul in place of 3-16 Jul | tests an event no input announces | one airline's five-day outage makes a third of the score |

   * **Recommendation:** B: it keeps the holiday fortnight and adds the two seasons that differ most from it, the
     summer peak (26.9% late, the largest drift of the weather inputs) and spring at about the year's average (21.3%).
     **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="FL_DATE", splits=TemporalSplits(window=14, unit="days",
   gap=1, cutoffs=("2024-12-18", "2024-07-03", "2024-03-13")))`. Built on the definition's frame: test 264,245, 278,071
   and 267,477 flights, train 13,426,458, 10,166,861 and 7,987,461 (97.9%, 74.2%, 58.3%). On C, the cutoffs
   `("2024-12-18", "2024-07-17", "2024-03-13")`: the July window tests 276,107 flights on 10,444,754 (76.2%). Then
   rewrite `task_summary.split` and `splits_comment` (the windows, the reasons and the numbers above; drop "The last six
   weeks of 2024" and "All three windows lie in late November and December"), add a CC line to the record and a dated
   CHANGELOG entry, and run `dataset check` (SPLIT-15).

   [^split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... The other windows are the curator's choice, per dataset,
     argued from the use case ... The evidence is statistics of the data, never a model's score ... Prefer windows in
     other years, then other seasons, then other months, weeks or days, over the windows just before the newest."
   [^split14]: **SPLIT-14** (Must): at least 3 windows, and no window's train side holds less than 50% of the data.
   [^split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source, such as the refit cadence.
   [^split20]: **SPLIT-20** (Should): "Check whether the newest windows fall in an atypical season and widen them so
     most do not. Cases: aeolus."

   **Lennart (2026-11-10, change):** Option B: Holidays, July, March.

   **Resolved (2026-11-10, Lennart):** B. `temporal` declares the cutoffs 2024-12-18, 2024-07-03 and 2024-03-13 (14
   days, one-day gap); `task_summary.split` and `splits_comment` name the windows, why each, the numbers and the
   length's new reason (no source states a refit cadence; two weeks keep a window under the 500k test cap and spread a
   single storm or outage over fourteen days, while the cutoffs choose the seasons). The evidence table of cancelled
   flights (`TEST_WINDOWS`), the fit reason's per-window share (now 1.2 to 2.0%) and the row-budget note follow the
   new windows, and the per-window scores and probes in the notes are labelled as measured on the earlier windows. Test
   264,245, 278,071 and 267,477 flights, train 13,426,458, 10,166,861 and 7,987,461 (97.9%, 74.2%, 58.3%); the 17,947
   flights of 17 December 2024, the newest window's gap day, are in no split, so the frame holds 13,690,703. The record
   has the decision and the horizon CC lines. `dataset check`: 0 errors, 0 warnings (README not regenerated).
