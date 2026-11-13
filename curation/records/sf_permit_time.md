---
unique_name: sf_permit_time
name: sf_permit_time
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
- Non-IID (Temporal)
- Free Text (Sentences)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
- 'Entities: Recur'
- 'Features: Revised Later'
collections:
- TexTabBench
- STRABLE
original_source: GOV Website
year: '2026'
domain: business & marketing
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/aparnashastry/building-permit-applications-data
- https://data.sf.gov/Housing-and-Buildings/Building-Permits/i98e-djp9/about_data
notebook_path: datasets/beyond_iid/temporal/sf_permit_time/sf_permit_time.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/sf_permit_time/dataset.py
source_row: 737
type_adapter_id: curation-record-v1
---

## Comments

building permits
AP: might need spatial/temporal split

Likely preprocess and filter on permit type, and status. Revised cost and some other features might be leaking if the permit was granted or not and if it was granted might leak time to grant. A lot of spatial features, record id is also time informative

the description column: it seems to be diverse enough to be considered free text

LP: very borderline. We need to create some features or filter to meaningful descriptions as many are clearly just a category. Others include a reference to other permits, so there might also be leakage. needs some time to look at and work with.

CC (2026-10-01, Lennart): Leak audit: right-censored target fixed. The download (2026-02-05) only holds permits issued by then, so recent filings miss their slow permits: still-open share by filed year 1.8-5.3% (2015-21), 10.2% (2023), 11.1% (2024), 21.5% (2025), and the p90 of days to issue falls from about 300 days to 147 (2024) and 97 (2025). The v2 definition now keeps permits filed before 2024 (116,954 -> 99,847 rows) and uses 8 half-year test windows (2020-H1 to 2023-H2, a 6-month gap before each, train >= 50%, test 3,758-6,878 rows, horizon 6 months) instead of 6 yearly windows up to 2025. A newer download was considered and not taken: the October 2026 portal data showed 2024 and 2025 still filling in (2025 p90 97 -> 160 days; 954 more 2025 permits issued) while 2023 had nearly settled (216 -> 222), so it would only move the safe cut a few months. Revisit in a year or two. Also fixed: latitude and longitude were swapped (Location is WKT POINT (lon lat)); the download description now names the actual filter (filed_date 2015-2025; the old query link filtered on approved_date) and the portal's new domain data.sf.gov. The target is log(days to issue). (updated 2026-10-14: the windows were 9, 2019-H2 to 2023-H2 with train >= 55%; the definition now leaves a 6-month gap before each test window and trains only on the permits issued before the window starts, so 8 windows, 2020-H1 to 2023-H2, with 52,851-89,314 training rows.)

CC (2026-10-19, Lennart): `DescriptionIsStandardPhrase` counts the descriptions filed before 2020, the start of the oldest test window, instead of the whole table (the flag covers 0.66% of the rows instead of 0.77%).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — DataSF's Building Permits table defines no task or metric; rmse on the log days to issue scores relative error.

**Assessment (AI, 2026-10-21):** metric now `Metric.from_context("rmsle", target_transform="log")` instead of the fallback rmse on the log target: a waiting time's error matters relative to the time; the target still ships as log, and RMSLE is computed after the inverse, on the original scale (MET-3). Needs a rebuild to reach the container.

CC (2026-10-21, Lennart): ship the target on the modelling scale, score on the original scale (target_transform).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Existing Construction Type Description`, `Proposed Construction Type Description` (the README lists their levels).

**Assessment (AI, 2026-11-01):** the benchmark STRABLE (https://arxiv.org/abs/2605.12292) carries this record's data as "SF Building Permits": Raw file sf_Building_Permits.csv from TextTabBench. Paper says 'construction cost'; config target is time_to_approve. Subsampled by STRABLE to 75,000 rows. Tagged STRABLE on 2026-11-01.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: censoring, late labels and an all-rows feature were fixed and tested in three rounds; only the domain field differs. Priority 3: gap 0, use case 0, source 1, shape 1, risk -0.

CC (2026-11-10, Andrej): review page issue 1, option C: the half-year windows, the six-month gap and the issued-before-the-start filter stay; a curation bullet gives the check of 2026-11-06 (kept fields unchanged after the issue for 18,420 permits; the review's changes go to the dropped Revised Cost), and a second one the re-read due around 2027-02-06 of the 4,106 open permits saved on 2026-11-06. Splits and data unchanged.

CC (2026-11-11, Andrej): record field set from the definition (review page field mark): `domain` business & marketing (was industry & manufacturing).

## Review

**Outcome:** added. The 99,847 building permits filed in San Francisco from 2015 to 2023 and issued by the download of
2026-02-05 (DataSF's Building Permits table): the days from filing to issue, shipped as a log and scored by RMSLE on the
days, predicted at filing from the permit's type, description, address, uses, cost estimate and flags. The AI recommends
shipping it as defined. Reviewed on 2026-11-04 without a review panel, from the gathered evidence (the record, the leak
audits of 2026-10-01, 2026-10-12 and 2026-10-19; no model run exists for it). Validity: a direct fit, settled in
three rounds: filings from 2024 on are cut because the download still misses their slow permits; each of the 8 half-year
windows (2020-H1 to 2023-H2) trains only on permits filed six months or more before it and issued before it starts, as a
refit then would; the description flag counts only filings before the oldest window; the dates and fields recorded after
filing are dropped. A building's earlier permits on the training side are the history a permit office has, not a leak.
Value: the `no_spread` probe flag after the six-month gap was kept on 2026-10-12 (random forest, LightGBM and linear
models within 0.032 skill on 5 of 8 windows, paired standard error 0.019); no tuned results yet. Quality: nothing open.
Weighed: a city's own records with a clear planning use +, censoring and late labels handled and tested +, narrow spread
among untuned models -.

**Main points:** The split is settled (issue 1, C, 2026-11-10): windows, gap and filter kept, the check in the notes,
a re-read of the open permits due around 2027-02-06. Record `domain` set to business & marketing (2026-11-11). Nothing open.

**Record judgment:** valid, and one of the most carefully cut temporal tasks of the copy (it is the precedent for
cutting where follow-up is complete). One selection is read after the outcome and was kept on purpose: the status filter
(issued or complete at the download) also drops 4,316 permits (4.1%) that were issued and later expired, were cancelled,
reinstated, suspended or revoked; their days to issue exist. The task is therefore the wait of a permit that was issued
and stayed valid; the notes say so (an `Anomaly:` bullet, Lennart, 2026-10-12).

**Issues for Andrej:**

1. **Time basis: keep the half-year windows, the six-month gap and the issued-before-the-start filter, and add today's check that the kept fields are filing values?**

   * **Problem:**
     - A permit's wait is known only at its issue, days to years after filing (one in ten over 315 days), and the
       split already trains each half-year window only on permits filed six months or more before it and issued
       before it starts, as a refit then would.
     - The record's collection facts (`Samples: Over Time`, `Time: Dated`, `Target: Varying Delay`) fit and a
       temporal split needs no time-basis tag[^1a]; the one open timing question was whether the table rewrites the
       kept fields after filing, as it rewrites `Revised Cost`.
     - Keep everything and add today's check to the notes (B), also repeat it on permits under review in three months
       (C), or keep the notes as they are (A)?
   * **Background:**
     - Settled and not reopened here: the cut at 2024 (2026-10-01), the status filter (2026-10-12), the six-month gap
       and the filter on the issue date (2026-10-14)[^1b].
     - What the gap leaves: 9% to 15% of the permits filed 6 to 12 months before a window are still open at its start
       and so out of training, which keeps the newest training stretch a little fast; a refit then knows the same
       permits, so this is the task, and the decision table shows it.
     - The table is updated daily and each row carries the time of its last change (296 distinct stamps among the
       50,462 rows filed in 2022-2023 in today's read), so rows are rewritten; the question is which fields.
   * **Experiments:** today's read of the portal's API (6 November 2026), permits filed 2022-2023, matched one to one
     to the shipped download of 5 February 2026 (issued permits only) on block, lot, street number and filing time:
     18,420 of 18,512 permits.
     - Between the two reads, all after the issue: the description changed for 1 permit; the estimated cost, the
       uses, units and stories, the permit type, the site-permit and other flags, the submission method and the
       construction type for none; occupancy and plan sets differ only in how a missing value is written (26 and 2
       rows).
     - In today's read the revised cost differs from the estimated cost for 28.5% of these permits: the review's
       changes land in the column the definition drops, and the kept cost stays the filing estimate.
     - The test cannot see a change made during the review, before the issue, since the February download holds no
       open permits; today's read of the 4,106 permits filed since 2025 and still open is saved, so a read in three
       months can show it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the split and the notes (implemented) | eight half-year windows, six-month gap, issued-before-the-start filter | no change | the card's open question about rewritten fields stays unanswered in the notes |
     | B | Keep the split, add the check to the notes | as A; a curation bullet with today's comparison | the kept fields shown to stay put after the issue, while the review's cost goes to the dropped column | a change during the review itself is argued, not seen |
     | C | B, and compare the saved read of open permits in three months | as B; a later read of the same 4,106 open permits shows whether their kept fields change while under review | closes the question with the data | an answer only in February 2027; the dataset ships meanwhile |

   * **Recommendation:** C: B's evidence is strong enough to ship on, and the saved read makes the remaining test
     cheap. **Decision:** A, B or C?

   **Notes for the AI:** on B or C, a curation bullet: "Fields rewritten after filing (checked 2026-11-06): the table
   rewrites rows (each carries the time of its last change), but comparing the February 2026 download with a read of
   November 2026 for the 18,420 permits filed in 2022-2023, the kept fields stayed put after the issue (one
   description changed; costs, uses, units, stories, types and flags none), while the revised cost differs from the
   estimated cost for 28.5%: the review's changes go to Revised Cost, which we drop." On C, in February 2027 read the
   same permits by permit number from the API and count the changes in the kept fields among those issued since;
   reopen this issue if any field changes for more than a few permits. No change to `data_tags`, the splits or the
   record.

   [^1a]: **SPLIT-32** (Should): the record carries the source's collection facts; a temporal split needs no use-case
     prototype. **LEAK-10** (Must): a feature holds only what existed at the prediction point; a value read at a later
     pull goes where its late cells can be located.
   [^1b]: **SPLIT-10** (Should): train on the rows whose outcome is known by the window's start, with a gap of about
     the label's delay (sf_permit_time: six months). **LEAK-24** (Must): a target right-censored in the newest periods
     is cut where follow-up is complete.

   **Resolved (2026-11-10, Andrej):** C: the split stays; the drafted "Fields rewritten after filing" bullet is in
   `curation_comments`, with a second bullet for the re-read due around 2027-02-06 of the 4,106 open permits saved on
   2026-11-06. No change to `data_tags`, the splits or the
   record's facts.
