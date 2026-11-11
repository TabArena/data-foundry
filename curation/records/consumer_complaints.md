---
unique_name: consumer_complaints
name: Consumer Complaint Database
checked_by:
- Lennart
- Mustafa
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
priority: 3
tags:
- Non-IID (Temporal)
- Free Text (Sentences)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Varying Delay'
collections:
- TexTabBench
- MulTaBench
- STRABLE
original_source: GOV Website
year: '2026'
domain: finance
required_split:
- Temporal (NON-IID)
problem_type: Multiclass Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/selener/consumer-complaint-database
- https://catalog.data.gov/dataset/consumer-complaint-database
- https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
notebook_path: datasets/beyond_iid/temporal/consumer_complaints/consumer_complaints_1m.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/consumer_complaints_1m/dataset.py
source_row: 735
type_adapter_id: curation-record-v1
---

## Comments

Real world complaints about financial products and services; data might contain sub-cohorts based on reporting category; we might want to filter to only a subset of cohorts; many missing values; data might have temporal drift; contains zip code to get more tabular features; temporal; we could get a new version of the data from the website

Needs a lot of preprocessing / feature engineering to become a usable task

We got the newer version from here: https://www.consumerfinance.gov/data-research/consumer-complaints/

Ref for descriptions https://cfpb.github.io/api/ccdb/fields.html

Only "Consumer complaint narrative" is a sentence field. "Company public response" is from one a predefined list of options

CC (2026-10-01, Lennart): **Original source changed.** The CFPB stopped publishing complaint narratives on 2026-08-14 (announcement: https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-to-cease-discretionary-publication-of-complaint-narratives-and-visualizations/) and removed them from the live download on 2026-09-14. The live `complaints.csv` (checked 2026-09-30) has no narrative and no consent column, so it can no longer rebuild this text task. Every previously published complaint, narratives included, is archived in the FOIA reading room as 21 CCDB exports (exported 2026-09-14, with Complaint ID and the company response as of that date): https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
Newer data is not useful even from the archive: the share of complaints with a published narrative fell from 16% (Nov 2025) to 3.5% (Mar 2026), 1.5% (Jul 2026) and 0 (Aug 2026), and the label mix of those complaints shifted ("closed with explanation" 65% -> 81%).

CC (2026-10-01, Lennart): Leak audit: the build from the 2026-01-23 download had a right-censored test window. Complaints still "In progress" are filtered out, and that was 7% of Oct, 14% of Nov and 70% of Dec 2025, so the newest months kept mainly quickly closed complaints. The v2 definition now builds from the FOIA archive exports 1-14 (Dec 2011 - Dec 2025), keeps complaints received 2017-04-24 to 2025-12-31 and tests on Oct-Dec 2025 (3-month horizon); all those labels are settled (0 in progress). Against the January download the archive has identical labels for all 3.49M shared complaints, 64,743 more closed complaints (mostly Nov-Dec 2025), Windows line endings in 2017-2020 narratives (normalised) and fewer fully masked ZIP codes (1.8% instead of 4.8%). The archive has no "Consumer disputed?" or consent column: the dispute filter is now the date filter it was equivalent to, and the consent filter is "has a narrative" (drops 1,656 consented rows without text). Duplicates that disagree on the label are now all dropped, as the curation comments already said.

CC (2026-10-06, Lennart): Kept after the task-probe sweep of the 2026-10-06 build. The probe flagged `unstable` (consumer_complaints_1m), only because the standard error of the best skill over the 3 temporal windows is 0.060 (limit 0.05): the best probe model (random forest) beats the class shares in all 3 windows, ROC AUC 0.90 +- 0.02, log loss 0.45 against 0.73. On BeyondArena's one fold all 21 configurations beat the dummy (log loss 0.41-0.56 against 0.71). The variation is the drift between the windows, not a missing signal.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — The CFPB database is a public register with no prediction task; the task is our adaptation following a benchmark paper, not an original task with a defined metric.

**Assessment (AI, 2026-11-10):** priority for the review of the test windows (PR #78), which this record never had. Priority 3: gap 0, use case 0 (written by the curation, 'for example'), source + (the CFPB's database page), shape +, risk 0 (the open issue is the choice of windows).

CC (2026-11-10, Lennart): test windows (`consumer_complaints_1m`, issue 1): "Option B: Two years, three seasons." The test quarters are October-December 2025, January-March 2025 and July-September 2024 instead of the last three quarters of 2025.

CC (2026-11-10, Lennart): the declared horizon (3 months, no gap, windows starting 2025-10-01, 2025-01-01 and 2024-07-01) is checked, as a quarterly refit is our assumption (the CFPB publishes no model or cadence), longer than the 15-60 days a closure takes, with 200k-350k complaints per quarter.

**Assessment (AI, 2026-11-10):** applied: `temporal` cutoffs 2025-10-01, 2025-01-01 and 2024-07-01 (3 months, no gap); test 203,139, 350,790 and 213,655 complaints, train 3,236,122, 2,277,019 and 1,838,062 (94.1%, 66.2% and 53.4% of 3,439,261), as the issue's notes counted; `dataset check` 0 errors. `task_summary`, `splits_comment` and the class-share and row-budget notes name the new quarters. The horizon audit (model-free, 2026-11-10) found no source for a refit cadence, so the quarter is stated as our assumption, and found the notes' "180 days" wrong: they are the deadline of the optional public response, while a company responds within 15 calendar days and has up to 60 for its final response (https://www.consumerfinance.gov/compliance/consumer-complaint-program/company-process/); the old reason ("data from just a few days is likely not enough") failed, as a month holds 54,655 to 165,305 complaints. No gap: at the download of 2026-01-23, 70% of December, 14% of November and 7% of October 2025 were in progress, so each train side holds one to two months of closures a refit would not yet know, accepted because the archive's closures are final (now stated in the splits comment); a one-month gap would keep the windows (51.5%, 63.9%, 91.8%). One month gives 19 candidate windows, six months exactly three.

CC (2026-11-11, Lennart): accepted `time_newest_period_short` with its reason (cross-dataset item "What to do with a newest period that holds far fewer rows than the periods before it?", A).

**Assessment (AI, 2026-11-11):** December 2025 holds 54,655 complaints against 73,058 to 77,970 from September to November; the share closed with monetary relief rises from 1.5% to 2.2% over those four months.

## Review

**Outcome:** added as `consumer_complaints_1m`. In the working copy since the migration. Resolved on 2026-11-10: the
test windows are October-December 2025, January-March 2025 and July-September 2024 instead of the last three quarters
of 2025 (issue 1, option B); the quarter stays the window length, now argued as an assumed refit cadence, with no gap.

**Main points:** Open: none. Resolved on 2026-11-10: the test quarters are July-September 2024, January-March 2025 and
October-December 2025 (issue 1).

**Horizon:**

* **Verdict:** keep the 3-month windows with a new reason (medium confidence): the CFPB publishes no model or cadence;
  a quarterly refit is our assumption, longer than the 15-60 days a closure takes, with 200,000 to 350,000 complaints
  per quarter.
* **Length:** the notes said "data from just a few days is likely not enough ... Thus, we instead simulate a model
  that is refit every three months"; that reason does not hold, since one month holds 54,655 to 165,305 complaints.
  The three quarters date from the switch to three windows (2026-10). No source states a refit cadence.
* **Gap:** none. A company "provides a response within 15 calendar days ... up to 60 calendar days to provide a final
  response" (https://www.consumerfinance.gov/compliance/consumer-complaint-program/company-process/); the notes' "180
  days" is the deadline of the optional public response and is corrected. At the download, 70% of December, 14% of
  November and 7% of October 2025 were still in progress, so each train side holds one to two months of closures a
  refit would not yet know; the archive's closures are final, and a one-month gap would keep your windows (51.5%,
  63.9%, 91.8%).
* **Time frame:** 24 April 2017 to 31 December 2025, both ends argued in the notes; volume tripled, so half the rows
  lie before 7 May 2024, and the closure mix jumps inside quarters ("closed with explanation" 58.1% in July, 69.6% in
  August 2025).
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | A quarter, no gap (implemented) | 3-month windows: October-December 2025, January-March 2025 and July-September 2024 (203,139 to 350,790 complaints) | longer than the 15 to 60 days a closure takes | a quarterly refit is our assumption; each train side holds one to two months of closures a refit would not yet know |
  | B | One month | 19 candidates | a month already holds 54,655 to 165,305 complaints | no source either; not longer than the up to 60 days a closure takes |
  | C | Six months | exactly three windows | longer than any closure | no choice of windows left; no source either |

* **Recommendation:** A: no source gives a cadence, and a quarter is longer than any closure while holding 200,000 to
  350,000 complaints. **Decision:** A, B or C?

**Resolved (2026-11-10, Lennart):** A, kept by the horizon audit, as instructed ("if the current time horizon makes
sense and is justifiable keep it and resolve them"); the record's CC line says the declared horizon is checked, and
the definition states the quarter as our assumed refit cadence, corrects the "180 days" and says why no gap is
needed.

**Issues for Lennart:**

1. **Test on July-September 2024, January-March 2025 and October-December 2025 instead of the last three quarters of 2025?**

   * **Problem:**
     - The test windows are April-June, July-September and October-December 2025, three neighbouring quarters of one year.
     - The rule keeps the newest quarter and prefers windows in other years, then in other seasons, over the quarters just before it[^cc-newest]; with every train side at half the complaints or more, the six quarters from July 2024 on can be tested.
     - July-September 2024, January-March 2025 and October-December 2025 are spread evenly over those six quarters, fall in three seasons and two years, and hold the two changes a deployed model met in that time (below).
   * **Background:**
     - The closure mix moved between 2024 and 2025: "Closed with explanation" was 51% to 57% of each quarter of 2024 and 57% to 67% of 2025 (66.8% in the newest quarter), "Closed with non-monetary relief" 41% to 47% and 31% to 42%.
     - January 2025 had a wave of complaints: 165,305 that month against 70,896 to 98,415 in the months around it; the quarter holds 45,175 money-transfer complaints (12.9% of it, 1% to 4% in every other quarter since 2017), 27,141 about Block, Inc. (Cash App) and 14,660 about Early Warning Services (Zelle), 98.9% of them closed with an explanation.
     - The window statistics show a large drift of `Product` for every quarter (population stability index 2.3 to 4.9) because the CFPB renamed its credit-reporting product in July-September 2023 and every train side since 2017 holds the old name. Against the newest year before each quarter, which a benchmark's default sample trains on, the drift is small except in January-March 2025 (0.50 for `Issue`, 0.47 for `Company`) and July-September 2024 (0.74 for `Product`, as its year still holds the old name).
     - The 75% to 82% "unseen categories" of the window statistics come from the complaint text, which is unique per complaint; no category of the categorical columns is new to a train side, and at most 0.12% of a quarter's complaints name a company its newest year never shows.
   * **Effect on the task:** Today a model is tested three times in 2025 alone, after the closure mix moved; with B one window falls before the move and one holds the January wave, both periods a deployed model had to handle.
   * **Data statistics:** six eligible quarters, newest first (window statistics and quarterly counts, 2026-11-10).
     - Train sides 94.1%, 85.3%, 76.4%, 66.2%, 59.7% and 53.4% of the 3,439,261 complaints; test quarters of 203,139 to 350,790 complaints.
     - Share closed with an explanation: 66.8%, 64.7%, 57.2%, 65.7%, 57.2% and 55.0%; monetary relief 1.1% to 1.8% (3,274 to 3,932 complaints per quarter).
   * **Consistency:** No dataset of the working copy declares windows chosen this way yet. The quarterly length and no gap stay, as the quarterly refit sets them[^cc-length].
   * **Sources:** the definition [dataset.py](../../datasets/_dev/tabarena-v0pt2/consumer_complaints_1m/dataset.py) (`temporal`, `splits_comment`, `curation_comments`), the record [consumer_complaints](consumer_complaints.md); the statistics come from `dataset windows consumer_complaints_1m` and quarterly counts of the frame (2026-11-10).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The last three quarters of 2025 (implemented) | test April-June, July-September and October-December 2025 (307,396, 300,917 and 203,139 complaints), train sides 76.4%, 85.3% and 94.1% | the most training data; the quarters right after a refit | one year; all three after the closure mix moved; no January wave |
     | B | Two years, three seasons | test July-September 2024, January-March 2025 and October-December 2025 (213,655, 350,790 and 203,139 complaints), train sides 53.4%, 66.2% and 94.1% | spread evenly; a quarter before the move and the January wave; three seasons | the 2024 quarter trains on 53.4%, near the floor; an eighth of the January-March window is a wave about two companies |
     | C | The same quarter a year apart | test October-December 2024, April-June 2025 and October-December 2025 (225,302, 307,396 and 203,139 complaints), train sides 59.7%, 76.4% and 94.1% | spread evenly; the newest quarter against the same quarter of 2024 | two seasons only; no January wave |

   * **Recommendation:** B: it keeps the newest quarter, tests another year and three seasons, and holds both changes of the period, with every train side above half the complaints[^cc-floor]. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="Date received", splits=TemporalSplits(window=3, unit="months",
   cutoffs=("2024-07-01", "2025-01-01", "2025-10-01")))` (checked 2026-11-10: train 3,236,122, 2,277,019 and 1,838,062
   complaints; test 203,139, 350,790 and 213,655). On C, the cutoffs `("2024-10-01", "2025-04-01", "2025-10-01")` (train
   3,236,122, 2,627,809 and 2,051,717; test 203,139, 307,396 and 225,302). Then rewrite `splits_comment` (it names the
   2025 quarters), `task_summary.split`, the code comment above `temporal`, and in `curation_comments` the class-share
   bullet ("In the three test quarters of 2025 (Q2-Q4)") and the row-budget bullet ("the last three quarters of 2025",
   "203k to 307k"). Then `dataset check`, a CHANGELOG entry and a CC line in the record.

   [^cc-newest]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): the newest window is always a test window; the others are chosen per dataset from the use case (other
     years, seasons, holidays, events, a change of rules or of the data collection), with statistics of the data as
     evidence and never a model's score; windows in other years, then other seasons, then other months, weeks or days
     are preferred over the windows just before the newest, and walking back from the newest needs its reason too.
   [^cc-length]: **SPLIT-12** (Should): the window length and the gap come from the use case, here a model refit every
     three months.
   [^cc-floor]: **SPLIT-14** (Must): at least 3 windows, and no train side below 50% of the rows.

   **Lennart (2026-11-10, change):** Option B: Two years, three seasons.

   **Resolved (2026-11-10, Lennart):** B. `temporal` tests October-December 2025, January-March 2025 and
   July-September 2024 (cutoffs 2025-10-01, 2025-01-01 and 2024-07-01, newest first; 3 months, no gap): test 203,139,
   350,790 and 213,655 complaints, train 3,236,122, 2,277,019 and 1,838,062 (94.1%, 66.2%, 53.4%), as counted above.
   `task_summary.split`, `splits_comment`, the comment above `temporal` and the class-share and row-budget notes name
   the new quarters; the quarter is stated as our assumed refit cadence (the CFPB publishes none), longer than the 15
   to 60 days a closure takes, in place of the old reason; the "180 days" are corrected (the optional public response;
   a company responds within 15 days and gives its final response within up to 60), and the notes say that each train
   side holds one to two months of closures a refit would not yet know, accepted as the archive's closures are final.
   The record has the decision and the horizon sign-off as CC lines. `dataset check`: 0 errors, 0 warnings.

## Reference

Kaggle / Gov
