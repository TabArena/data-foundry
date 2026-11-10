# consumer_complaints

**Outcome:** added as `consumer_complaints_1m`. In the working copy since the migration; the test windows are the last
three quarters of 2025 (explicit cutoffs). The rule on test windows was rewritten on 2026-11-10; the AI proposes
keeping the newest quarter and testing January-March 2025 and July-September 2024 instead of the two quarters just
before it.

**Main points:** Which quarters to test on: April-June, July-September and October-December 2025 (as now), or
July-September 2024, January-March 2025 and October-December 2025?

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
   * **Sources:** the definition [dataset.py](dataset.py) (`temporal`, `splits_comment`, `curation_comments`), the record [consumer_complaints](../../../../curation/records/consumer_complaints.md); the statistics come from `dataset windows consumer_complaints_1m` and quarterly counts of the frame (2026-11-10).
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
