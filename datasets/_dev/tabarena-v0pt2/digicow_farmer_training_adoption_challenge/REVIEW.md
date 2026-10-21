# digicow_farmer_training_adoption_challenge

**Outcome:** added; recommended `No` (`Data Quality Issue`, `Too Small`). Zindi's DigiCow Train.csv as a binary task
tested on later trainings than it trains on: does a farmer adopt a practice within 7 days of a training? Verdict: don't
ship. Validity: the use case and the prediction point hold (USE-1, USE-3); the stored dates had day and month swapped
and are repaired (PROV-13); the 90- and 120-day labels and a topic flag recorded with the adoption are dropped
(LEAK-10), and the day's topic list stays as an input known at training time, with a note (LEAK-37); the split holds
(SPLIT-3, SPLIT-14, SPLIT-16). LEAK-25 (Must) is triggered and cannot be fixed: the label records when trainers followed
farmers up, not when farmers adopted. Value: TP-9 (Must), too few adopters per test window. Quality: topic spellings
vary (CLEAN-1), kept with a note. Weighed: a real use case and data from the company that runs the programme, against
the size; neither can outweigh a Must. Left for the curator: the verdict fields (issue 1).

**Main points:** Confirm `No` with `Data Quality Issue` and `Too Small`: the label tracks follow-up recording, and the
newest test windows hold 9 and 5 adopters.

**Issues for Lennart:**

1. **Confirm `No` with the markers `Data Quality Issue` and `Too Small`?** The record still has `suggestion: 'Yes'` and
   neither marker, while every panel report recommends not shipping.
   - Problem, validity (LEAK-25, Must: a label whose 0 mixes "no event" with "not recorded" is retired unless the
     recording process can be recovered). Adoptions appear in waves: a trainer's farmers have adopters only in the
     months that trainer went back and recorded them. A 0 therefore mixes "did not adopt" with "nobody asked".
   - Problem, value (TP-9, Must: a temporal task needs enough minority rows in every test window). The four test windows
     hold 9, 5, 19 and 103 adopter rows, newest first.
   - Effect: a model learns which trainer recorded in which month, and the score ranks methods on recognising those
     waves. With 9 and 5 adopters in the two newest windows, the scores cannot tell a good method from a lucky one.
   - Evidence for LEAK-25:
     - in Train.csv, of the farmers who adopted within 120 days, 1 of 95 trained in August-October 2024 adopted within 7
       days, against 69 of 77 trained in December 2024; a delay set by farmers cannot jump like that between
       neighbouring months;
     - TRA_gertumxc's farmers have 0 adopters within 7, 90 or 120 days in 4,906 rows of March-July 2025 (Train.csv and
       Prior.csv, Zindi's file of the farmers' other trainings), although those 120 days had passed before the release;
     - a model given only the subcounty, or only the trainer, ranks adopters better than one given all columns (ROC AUC
       0.778 and 0.762 against 0.691 on the test windows): who recorded predicts the label better than anything about
       the farmer; under a random split a lookup of trainer and month scores 0.937;
     - the September-December 2024 window trains on 17 adopters, all from TRA_hyodnntj, and a linear model scores ROC
       AUC 0.49 on it, against 0.88-0.94 on the other windows.
   - Evidence that no split fixes TP-9: the rule that every training side keeps at least half the rows (SPLIT-14) fixes
     the test pool at 136 adopters, 33 of them in 2025, so wider windows (SPLIT-17) cannot add adopters; 6-month windows
     leave only 2 windows, and 3-month windows leave April-June 2025 without an adopter. A random split is barred for
     this temporal task (SPLIT-16), and 97.5% of its test rows would have a farmer from the same session in train.
   - Remedies checked: no dropped column, row filter, other split or other target recovers who was followed up; the 90-
     and 120-day targets show the same waves.
   - Precedents: follows ghanas_indigenous_intel (Lennart, 2026-10-01: LEAK-25, the same markers and a revisit clause,
     on weaker evidence), seismic_bumps (TP-9, no fallback to a random split) and alvin (`No`, not `No (Retired)`, for a
     dataset never shipped). african_credit_scoring_challenge was kept: its windows hold 20-56 defaults from many
     customers and show no recording waves.
   - Implemented: the definition recommends `No`; the folder stays for your decision.
   - Alternative: ship with the approximate fit. Cost: the benchmark scores the recording waves, on 9 and 5 adopters in
     the newest windows.
   - Recommended: yes (mediator, advocate and critic agree).
   - Decision: set `suggestion` to `No` with `Data Quality Issue` and `Too Small`, and the clause "revisit if DigiCow
     documents who was followed up and when"?

**Review panel:** don't ship, `No` with `Data Quality Issue` and `Too Small` (mediator). Claim audit: 63 claims, 49
hold, 3 hold with a correction, 4 refuted (wording and numbers; none changes the verdict), 7 untested. Blind review:
exclude; main concern too few adopters, arriving in bursts. Debate: agreed on the verdict (issue 1); four disputes, all
settled by the mediator: whether the standard error of the probes' mean skill counts as evidence for `Too Small`,
whether the probes' `no_spread` flag counts for it, which rule backs the `topics_list` note, and why Prior.csv (the
farmers' other trainings) stays out. The mediator's issue 1 is issue 1 here; its optional issue 2 (a rule for that kind
of note) is in the cross-dataset review file. The panel's references to issues 2-5 point to the draft it reviewed; the
mediator settled them as changes to the notes.

<details><summary>Claim audit</summary>

**Claim audit: digicow_farmer_training_adoption_challenge (2026-10-20, re-check)**

Tests on the definition's frame, the raw Train/Test/Prior files and the Zindi API's competition record.
63 claims: 49 hold, 4 refuted (wording/numbers, no code change), 3 hold with a correction, 7 untested. One finding
nobody wrote down (U1) changes what the 2025 test windows are.

**Table**

| # | Claim (source) | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| 1 | Task: adoption within 7 days as DigiCow records it (D task_summary) | Zindi description via API | holds | "predict ... adopt a practice within 7, 90 and 120 days of their first training"; rubric puts 0.80 on the 7-day target | USE-5 |
| 2 | Use case: score at end of training day (D) | source text | holds | "using only information available at the time of training"; "prioritise follow-ups" | USE-1 |
| 3 | Row: one farmer, Mar 2024-Dec 2025, 13,536 (D) | frame | holds with correction | 13,536 rows = 13,536 farmers, 2024-03-01..2025-12-04; but 2025 holds true days 1-4 only (U1) | USE-8 |
| 4 | Country not named (D) | read D | holds | API field `helping: Kenya` would let it be named | writing |
| 5 | 1.1% adopted (D) | frame | holds | 153 / 13,536 = 1.13% | |
| 6 | Adoption undefined by source; 0 mixes not adopted / not recorded (D) | dictionary + API pages | holds | dictionary and evaluation page say only "adopt a DigiCow-supported practice"; 0-mixing supported by #32-33 tests | USE-5 |
| 7 | All kept features known at prediction point (D) | column semantics; leak probe | holds | profile, location, group, trainer, day's topics, date are set by the end of the day; no exact test copy in train (0.0%); registration (Ussd 1.42% vs Manual 0.66%) is the enrolment channel, not an outcome | LEAK-1, LEAK-2 |
| 8 | 4 windows Sep 2024-Dec 2025, train = all earlier (D) | make_splits | holds | train max < test min in all 4; gaps 28/27/51/20 days | SPLIT |
| 9 | Changes (D) | code read | holds | swap, drop 90/120, flag, ID, farmer_name | |
| 10-11 | fit approximate; 9-103 adopters from 1-7 trainers (D) | make_splits | holds | 9/5/19/103; trainers 1/1/2/7 | USE-8, TP-5 |
| 12 | domain environmental science & climate (D) vs "agriculture" (R) | schema Domain list | holds (closest?) | no agriculture value; the task (farmer behaviour after extension training) is arguably `social science`; a judgment | writing |
| 13, 54 | Licence "Zindi Competition Rules", quote (D, R) | none | untested | licence is never evidence | EV-4 |
| 14 | File sizes, manifest 2026-02-10T12:40:23 (D) | manifest JSON + API `datafiles` | holds | Train 3,239,613; Test 1,254,202; Prior 7,454,788; dict 880 | PROV-8 |
| 15 | Kaggle and GitHub copies byte-identical (D) | sha256 of the pinned GitHub raw file | holds (GitHub); Kaggle untested | GitHub Train.csv sha256 = 4977559d...; Kaggle not downloaded | PROV-9 |
| 16 | sha256 values (D) | sha256 local | holds | both match | |
| 17 | Competition 2026-01-28 to 2026-03-01 (D bibtex) | API start/end | holds | 2026-01-28T21:00Z to 2026-03-01T23:59Z | |
| 18 | Train.csv final release, 13,536 rows one per farmer (D) | counts | holds | 13,536 unique farmer_name; 0 Train farmers in Test | |
| 19-20 | Recommendation; prediction point (D) | judgment | holds as stated | | |
| 21 | Host removed counts over later trainings after leak reports (D) | discussion page needs login | untested | | EV-6 |
| 22, 45 | Dates swapped; Sundays rare; 42.7% vs 14.5% whole-week group gaps (D, D1) | weekday shares, group gaps both readings; extra: Kenyan holidays | holds | swapped: Sat 5.5%, Sun 4.9%, Fri 11.1%; stored: 10.7-17.6% every day; gaps 42.7% vs 14.5% (546 gaps). Holiday test inconclusive (stored day 1 = true January confounds): swapped reading puts 2,060 of 58,418 Train+Prior rows (3.5%) on 9 holidays, about the uniform rate | PROV-13..15, EV-1 |
| 23 | Day never above 12: release holds days 1-12 (D) | day of month per file | holds with correction | true day <= 12 in all files; but Train.csv 2025 holds days 1-4 only (U1) | |
| 24 | 20.3% of Prior rows of Train farmers come after the Train row in true dates (D) | merge | holds | 20.30% of 16,441 rows (0.0% in stored order) | LEAK-1 |
| 25 | 7-day is the main target (D) | API rubric | holds | 7d log loss 0.65 + 7d AUC 0.15 | USE-5 |
| 26 | 90/120 contain 7-day label in every row (D) | per-row check | holds | 7<=90<=120 in all rows; 153/214/302 positives | LEAK-2 |
| 27, 46 | Flag goes with adoption for TRA_szrwyfzz, TRA_hyodnntj; 221 of 4,195 rows hold all adopters, 71% adopted within 120 d; other trainers flag 1 on almost every row (D, D2) | groupby trainer x flag | holds with correction | 221/4,195, 57/57 7d and 157/157 120d adopters flagged, 0.710; others: flag 0 on 70 of 9,341 rows, but TRA_dttdgplk 10/10 flag 0 and TRA_twwcfcum 23/24 flag 0, whose single flagged row is its single adopter: the pattern is not limited to two trainers; flag 0 never adopts in any trainer (4,044 Train rows, 5,201 Train+Prior) | LEAK-1 |
| 28 | topics_list predicts flag AUC 0.87 in the two trainers' rows (D) | 5-fold GroupKFold by session, binary topic tokens + logistic | holds | 0.902 | LEAK-1 |
| 29-30 | ID / farmer_name ids; text formats; 8 categoricals (D) | code + frame dtypes | holds | 3 two-trainer rows become combined categories | CLEAN |
| 31, 50 | 6,590 duplicate rows, distinct farmers of one session, same window (D) | duplicated(); copies across windows | holds | 6,590 full-row duplicates (6,641 on features, 51 conflicting); 0.0% of test rows have a copy in train | LEAK-16..21 |
| 32 | 0% Aug-Oct 2024; 45%, 64%, 95% for Nov, Dec 2024, Feb 2025 (D curation_comments) | share 7d among 120d adopters by true month, Train only vs Train+Prior | refuted as written | these are Train+Prior figures (147/326, 445/691, 112/118; Aug-Oct 1/1,021); the data the definition ships give 73%, 90%, 100% (33/45, 69/77, 19/19) and 1/95, which D3 itself states. One definition, two sets of numbers, the file unnamed | EV-1, writing |
| 33, 48, 58 | TRA_gertumxc never adopted Mar-Jul 2025; adopted Aug-Dec 2024 at 5-13% (D, D4, R) | by trainer x month | holds | Train: 0 in 618 rows Mar-Jul 2025 (and 36 in Nov 2025); T+P: 0 of 4,906; Aug-Dec 2024 120d rates 5.1-13.0% | USE-5, LEAK-24 |
| 34 | Trainer and location are the leak probes' strongest single features (D) | leak probe | holds | subcounty 0.778, ward 0.775, trainer 0.762, county 0.760 | |
| 35 | One row per farmer = latest training in stored-date order; selection uses dates, not labels (D) | Train row vs the farmer's Prior rows, both orders | holds | stored: Train row latest for 3,193/3,193 farmers with Prior rows (first for 0); true: latest 67.8%, first 20.5%. See U2 for the "first training" wording | LEAK-22 |
| 36, 41, 44, 49, 52 | Windows 718/9, 773/5, 727/19, 4,264/103; last train 7,054/17; adopters from 3/3/8/52 sessions, 1/1/2/7 trainers; newest two all TRA_rkvyofbh (D) | make_splits | holds | exact match; the 17 train adopters of the 2024 window are all TRA_hyodnntj | TP-5, TP-9 |
| 37, 59 | Random split, group_name folds, leave-one-trainer-out do not fix it; LGBM 0.959 vs lookup 0.937, grouped 0.937 vs 0.916 (D, R) | LGBM vs trainer x month lookup, 5-fold random and GroupKFold(group_name) | holds (numbers differ) | random 0.963 vs 0.950; grouped 0.893 vs 0.910 (lookup ahead); adopters by trainer 54/39/28/18/11/2/1/0: LOTO folds hold one trainer's adopters | TP-5 |
| 38-40, 43 | Train side's newest training >=19 days old (17 after Feb); walk with 50% floor stops at Sep 2024 (D) | arithmetic + split | holds | gaps 20-51 days; May-Aug 2024 window would train on 1,444 rows (<50%) | SPLIT, LEAK-23 |
| 42 | 3-month windows leave Apr-Jun 2025 without adopter (D) | quarter counts | holds | 2025Q2 0 adopters | TP-9 |
| 47 | 1 of 95 Aug-Oct adopters within 7 d; 33/45, 69/77, 19/19; 36 of 38 Aug on days 91-120; 40 of 57 Sep-Oct on days 8-90; 10 of 21 months no 7d adopter (D3) | by month | holds | exact | USE-5 |
| 51 | TRA_ubcgvofe 0/1,456, suiifsur 2/2,190, gertumxc 11/3,049 (D) | counts | holds | exact | |
| 53 | Front matter (R) | read | holds as fact | suggestion 'Yes', markers lack Too Small / Data Quality Issue while the definition recommends No: the curator's field, noted only | |
| 55 | Record comment "log loss 25%, ROC AUC 75%" (R) | Zindi evaluation page + rubric via API | refuted (the line is stale) | page: Log Loss 75%, ROC-AUC 25%; rubric 7d LL 0.65, 7d AUC 0.15, 90/120 LL and AUC 0.05 each (the rubric part holds) | EV-1 |
| 56-57 | 1 of 1,021 Aug-Oct; 2024-12-12 inside the adoption interval of 1,028 of 2,389 adopters (R) | Train+Prior | holds | exact | |
| 60 | Assessment scores (R) | judgment | untested | | |
| 61 | Whole-week gaps 49.3% vs 14.7% "trainer-days"; Sundays 5.4% of trainer-days; Labour Day 700, Easter Monday 331 (REVIEW) | gaps per trainer, group, group x trainer, ward, Train+Prior | refuted (49.3/14.7 not reproducible) | trainer-day gaps 3.8% / 3.9% (trainers hold sessions daily); group gaps T+P 47.3% / 14.5%; Sunday 5.6% of trainer-days; 700 and 331 hold (Train only: 60 and 115) | EV-1, writing |
| 62 | Prior history features add AUC -0.02..+0.16 (REVIEW) | not re-run | untested | needs the true-date history rebuild | |
| 63 | Mixed sessions: 195 flagged hold all 56 adopters; flag 0 never adopts in 5,201 rows (REVIEW) | sessions = true date x group x trainer | holds | 82 mixed sessions, 195 flagged, 56/56; 5,201 = all trainers' flag-0 rows in Train+Prior (Train: 4,044), not the two trainers' (4,523) | |

**Unwritten claims attacked**

| # | Implied claim | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|
| U1 | The test windows are the trainings of their calendar months ("days 1-12 of each month") | true day of month per file and year | refuted | Train.csv 2025 holds true days 1-4 only (2,218 rows: 361/619/522/716); days 5-12 of 2025 are in Test.csv (5,621 rows) because Zindi cut Train/Test in stored order (Train <= stored 2025-04-12, Test >= 2025-05-02). The three 2025 test windows are a day-of-month slice of each month (a third of the days), and that is why they hold ~720-770 rows against ~4,300 for Sep-Dec 2024. Not label-driven, no leak; it adds to Too Small and makes 2025 a different sampling than 2024 | SPLIT, USE-8 |
| U2 | The 7-day label is anchored to the row's training day (the use case scores "at the end of a farmer's training day") | source wording; label variation within farmer; Train label vs the farmer's first Prior label | holds (supported), wording unsettled | source says "within 7 days of their first training"; but 248 of 6,719 Prior farmers have different 7d labels on different rows, and of 54 Train 7d adopters with Prior rows only 5 have a 7d-positive first Prior row: labels are per training row, not per farmer's first training. 2,540 Train rows (18.8%) are not the farmer's first training in true dates; nothing in D says a row can be a repeat training | USE-5, LEAK-22 |
| U3 | No row is a copy across the split | exact copy with strings/dates; farmer overlap | holds | 0.0%; no farmer in two rows | LEAK-16 |
| U4 | Target is the real-world target | rubric + recording tests | approximate, as D says | recorded adoption in waves (#32-33, #47) | USE-5 |

**Ranked: refuted and untested**

1. U1 (P3/P4 validity, Should): 2025 windows are days 1-4 of each month only. Changes: the split statement ("four calendar months of trainings") and the row coverage are overstated; strengthens Too Small; no leak. Mildest remedy: one sentence in `row`/`splits_comment` and curation_comments ("Train.csv holds days 1-4 of each 2025 month; days 5-12 went to Zindi's Test.csv"); no code change.
2. #32 (procedure, notes match the code): comment's 45/64/95% and 0% are Train+Prior; the shipped data give 73/90/100% and 1/95. Changes nothing in the verdict (the wave holds in both). Remedy: name the file ("Train + Prior") or quote D3's Train figures.
3. #55 (record): "log loss 25% / ROC AUC 75%" is stale; source says 75/25. Remedy: fix or strike the record line (the assessment already notes it).
4. #61 (REVIEW.md): 49.3%/14.7% "trainer-days" not reproducible; use D's 42.7%/14.5% (Train, group gaps) or 47.3%/14.5% (Train+Prior).
5. #27/#46 (minor, strengthens D2): the flag-with-adoption pattern also holds for TRA_twwcfcum (1 flagged row = its 1 adopter), and flag 0 never adopts for any trainer. Remedy: reword "two trainers" to "the trainers where the flag is mostly 0".
6. #12 domain: judgment (no agriculture value; `social science` may fit better). Curator's call.
Untested: #13/#54 licence (never evidence), #15 Kaggle copy (GitHub verified), #21 leak-report history (login), #62 Prior history AUC (rebuild not re-run), #60 assessment scores (judgment).

</details>

<details><summary>Column audit</summary>

**Column audit: digicow_farmer_training_adoption_challenge (2026-10-20, re-check)**

Prediction point (first curation bullet, task_summary): the end of a farmer's training day. Frame: 13,536 rows, 11
features + target, rebuilt from the definition via `dataset_io.from_definition`. Codebook:
`dataset_data_dictionary.csv` (15 lines; no entry for
`group_name`; names `topics`, `first_training_date`, `has_topic_traine_on` that differ from the file). Prior.csv read for the timing tests only. No missing value in any column.

**Column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| training_day | "Date of the farmer's first training" (codebook calls it first_training_date); in the data the farmer-day of this row, not the first training (below) | yes, the day itself | datetime, day and month swapped back; 152 dates, days 1-12 only | fine (swap is the claim auditor's) | LEAK-1, CLEAN-14, PROV-13 |
| gender | gender of the farmer | yes; differs across a farmer's records for 1.4% of farmers | category, 2 values | fine | CLEAN-14 |
| registration | registration method (Ussd / Manual) | yes, recorded per training record (changes across a farmer's records for 12.3%: Manual->Ussd 1,211, Ussd->Manual 881) | category, 2 values; Ussd share drifts to 15.5% in 2025Q4 | fine (drift, not a leak) | CLEAN-14 |
| age | age band | yes | category, 2 values (Above/Below 35) | fine | CLEAN-14 |
| group_name | unknown (no codebook entry); by the data a farmer group, nested in one trainer (100%) and mostly one ward (98.2%) | yes; but 24.4% of farmers appear in several groups, and Train keeps one group per farmer-day by an unstated rule | category, 864 values | fine; question: which session's group/cooperative value the challenge kept | CLEAN-14, USE-3 |
| belong_to_cooperative | cooperative member (1/0) | yes, per record (4.4% of farmers change); share falls from 49.6% (2024Q1) to 0-4% in 2025 | int 0/1 | fine | CLEAN-14 |
| county | county of residence (pseudonymised) | yes | category, 8 values; each county ~one trainer (97.4%) | fine as a column; carries the recording process (alone 0.760) | LEAK-25 (dataset level) |
| subcounty | sub-county | yes | category, 26 values, nested in county (100%) | fine as a column; best single feature 0.778 > all features 0.691: recording process | LEAK-25 (dataset level) |
| ward | ward | yes | category, 66 values, nested in subcounty (100%) | fine as a column; alone 0.775 | LEAK-25 (dataset level) |
| trainer | "list of trainers who delivered the training on a given day" | yes | category, 12 values; 3 two-trainer rows become combined levels (1 row each) | fine as a column; alone 0.762; TRA_ubcgvofe 0/1,456, TRA_suiifsur 2/2,190 adopters | LEAK-25 (dataset level) |
| topics_list | "list of list of possible training topics"; by the data the sessions of this farmer-day (Prior.csv holds 1-12 records per farmer-day; topics differ between farmers of one session in 936 of 1,413 sessions) | yes, but carries the dropped flag: in TRA_szrwyfzz/TRA_hyodnntj rows topics predict `has_topic_trained_on` AUC 0.885 and the 7-day label 0.877 (5-fold grouped by session), 0.649 within the 82 mixed sessions (56 adopters; adopters 4.71 topics vs 3.22) | string; 141 topic spellings, 123 after case/punctuation ("Poultry Management Practises." / "Practises.." / "Practices" / "Poultry Mngt Practices"; "Herd. Health. Management") | maybe a leak, weak (question); cleaning: spelling variants (minor) | LEAK-10, LEAK-2, CLEAN-1, CLEAN-14 |
| adopted_within_07_days (target) | adoption within 7 days "of first training" (codebook); by the data within 7 days of this row's training: for 22 Train adopters with earlier Prior rows, the earliest Prior row is positive for 6 | outcome | category Yes/No, 153 Yes (1.1%) | target as recorded: 0 mixes not adopted / not recorded | LEAK-25, USE-5 |
| dropped: ID | row id | - | dropped | fine | CLEAN-3 |
| dropped: farmer_name | farmer id, one row per farmer | - | dropped | fine (no repeated entity to group) | CLEAN-3, LEAK-17 |
| dropped: adopted_within_90/120_days | later targets, contain the 7-day label | no | dropped | fine (leak removed) | LEAK-10 |
| dropped: has_topic_trained_on | "whether the farmer was trained on that topic" | recorded with adoption for two trainers | dropped | fine, but incomplete (topics_list) | LEAK-10, LEAK-2 |

**Problems, ranked (principles.md)**

1. **P4, LEAK-25 (Must), dataset level, not fixable by a column drop.** The label records follow-up: county,
   subcounty, ward and trainer are near one-to-one with the trainer (97-100%) and each alone beats all features
   (subcounty 0.778, depth-2 tree 0.776, all 0.691). Dropping them does not help (without subcounty 0.669): the
   recording sits in the label. Remedy: the definition's recommendation (retire, `Data Quality Issue`) stands.
2. **P4, LEAK-10/LEAK-2 (weak, maybe a leak; curator question).** `topics_list` carries the dropped flag (0.885) and
   predicts adoption within mixed sessions at 0.649 on 56 adopters; the mechanism is circumstantial (more sessions
   attended, a genuine engagement signal, is the other reading). Mildest remedy: keep the flag dropped and keep
   `topics_list` with a `Potential leak, kept on purpose:` note giving these numbers; or drop both. Moot if retired.
3. **Procedure, codebook vs data (writing).** The codebook anchors the labels to the "first training" and calls the
   date `first_training_date`; the data anchors them to the row's own farmer-day (above). The definition says what the
   row is but not that the codebook is wrong here; one sentence would settle the claimants' doubt (checklist item P3/P4 b).
4. **P7, CLEAN-1 (Should), cheap.** Topic spellings differ by trainer (141 -> 123 after lower-case and punctuation
   strip, more with "Practises"/"Mngt"). Mildest remedy: a note; optional normalisation in `trainer`-independent form.
   Shipping the list as string rather than one flag per topic (CLEAN-13 style) is acceptable; curator's taste.
5. **Question (USE-3).** Prior.csv shows several records per farmer-day with different `group_name` /
   `belong_to_cooperative` (e.g. FAR_hfkybdg on one day: coop 0 and 1); Train keeps one value per farmer-day by a rule
   the source does not state. Not a leak (values are pre-training); note it.

No dtype or proxy-missing problem: every column is typed by meaning, no sentinel or impossible values, ids dropped.

</details>

<details><summary>Split audit</summary>

**Split audit: digicow_farmer_training_adoption_challenge (2026-10-20, re-check)**

Verdict: **right with notes.** The temporal regime and the 4-month windows mirror the use case. No re-split, gap or
filter fixes the minority counts: the split is not where this dataset fails. The TP-9 `Too Small` holds under every
legal alternative, which supports the retirement recommendation.

The frame is loaded from the definition.

**Regime (USE-10, USE-11, SPLIT-1..4, SPLIT-13): holds**
- One row per farmer (13,536 distinct `farmer_name`), Prior.csv not used, so every prediction is for a new farmer with
  no history. Farmers do not recur. The entities that do recur (trainer, group, ward, subcounty) are features that
  new rows keep (SPLIT-4). In the test windows, 100% of rows have a trainer seen in train, 33.8-61.2% a group seen in
  train, and 93.2% a subcounty seen in train (hidden-group probe).
- The use case is a stream: score each farmer at the end of the training day and refit over time. Temporal is the
  regime the use case implies (SPLIT-3).
- Hidden groups: 48.7% of rows are session copies (same day, group and trainer). The copies always share a window, so
  0.0% of temporal test rows have a session-mate in train. Under a random split it is 97.5%.

**Windows, gap, late labels (SPLIT-9..12, SPLIT-14..17): hold, with one open question**
| window | test rows | test adopters | adopter sessions / trainers | train rows (share) | train adopters | gap (days) |
|---|---|---|---|---|---|---|
| Sep-Dec 2025 | 718 | 9 | 3 / 1 | 12,818 (94.7%) | 144 | 28 |
| May-Aug 2025 | 773 | 5 | 3 / 1 | 12,045 (89.0%) | 139 | 27 |
| Feb-Apr 2025 | 727 | 19 | 8 / 2 | 11,318 (83.6%) | 120 | 51 |
| Sep-Dec 2024 | 4,264 | 103 | 52 / 7 | 7,054 (52.1%) | 17 | 20 |
- The true day is never above 12. The train side ends 20-51 days before each test start, and 0 train rows fall within
  7 days of a test start, so every training row's 7-day label has matured (SPLIT-9/10 met for the stated horizon).
  The expanding train side starts from the newest window (SPLIT-11). Four windows with at least 50% train (SPLIT-14).
- Wider windows do not help. 6-month windows give only 2 windows above the 50% floor (14 and 19 adopters), which
  breaks SPLIT-14. 5-month windows give 11, 3 and 122 adopters. Only 33 adopters fall in all of 2025, from 2 trainers
  (TRA_rkvyofbh, TRA_kkzpfdtu), so any 3 or more windows leave at least two windows with a handful.
- Open question (SPLIT-9, cannot verify). The labels are as of the 2026-02 release. Decision 3 shows adoptions
  back-filled around December 2024 (Aug-Oct 2024: 0-1 adopters within 7 days, 36 of 38 August adopters on days
  91-120). So when DigiCow recorded a label is not the 7-day horizon, and a train side at a 2024 refit may hold labels
  that were not yet recorded then. A gap would not fix this: the recording lag is unknown and varies by trainer.

**Problems, ranked (principles.md)**
1. **P6, TP-9 / TP-5 (Must) `Too Small`**: 9, 5, 19 and 103 test adopters, from 3, 3, 8 and 52 sessions and 1, 1,
   2 and 7 trainers. The two newest windows each test one trainer's 3 sessions. Remedy: none by splitting (SPLIT-16
   bars an IID fallback, and SPLIT-17's wider windows break SPLIT-14). Retire, as recommended.
2. **P4 (via P3/P5), SPLIT-20 (Should), atypical windows**: the label process shifts between windows. The Sep-Dec
   2024 window's train side holds 17 adopters, all TRA_hyodnntj (one of the two flag trainers), while its 103 test
   adopters come from 7 trainers in the Nov-Dec 2024 recording wave. Linear AUC on that window is 0.49 (LightGBM 0.51)
   against 0.88-0.94 on the others, so the window measures the shift in recording, not adoption. Remedy: none in the
   split. Note it with the Data Quality Issue.
3. **P4, SPLIT-9 (Must if confirmed), label anchor**: the data dictionary anchors the label to the farmer's *first*
   training. Curation comment 35 says the kept row is the latest training in stored-date order, which in true dates is
   ordered by day of month before month. If so, the label's event can precede the row's training day and sit in
   another window. This cannot be checked without Prior.csv (not in the warehouse). Remedy: verify against Prior.csv.
   If confirmed, keep each farmer's first training, or date the row by it.

**Alternative splits (quick fits: one-hot logistic plus topics, untuned LightGBM; ROC AUC)**
| split | linear | LightGBM |
|---|---|---|
| temporal, shipped 4 windows | 0.810 (0.88 / 0.93 / 0.94 / 0.49) | 0.751 |
| IID random 5-fold | 0.883 | 0.902 |
| IID random + month as a feature | 0.959 | 0.959 |
| grouped by session | 0.799 | 0.671 |
| grouped by session + month | 0.932 | 0.886 |
| grouped by group_name | 0.803 | 0.688 |
| trainer x month lookup, random 5-fold | 0.937 | |
Under a random split, a lookup of who recorded in which month reaches 0.937. With 97.5% of test rows having a
session-mate in train, an IID split rewards recognising the recording wave (SPLIT-29). The grouped splits reach 20-52
adopters per fold, but group/session is not the entity of the use case (the trainer and group recur in new data,
SPLIT-4). A grouped split would also not be the one regime the use case implies (SPLIT-3). Neither alternative is
right; both confirm that the temporal split is the honest one.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: digicow_farmer_training_adoption_challenge (2026-10-20, re-check)**

Actor: a DigiCow programme manager in Kenya who plans the follow-up of the farmers its trainers (extension officers)
trained, with a fixed number of follow-up calls/visits per week. Zindi states the purpose: predictions help DigiCow
"prioritise follow-ups, tailor support more effectively, and design stronger extension strategies", using only what is
known at the time of training. The practice adopted is only called a "DigiCow-supported practice".

**Fit: approximate (at the low edge, close to none)**

The decision is real (USE-1, USE-2 not triggered) and the prediction point is right (USE-3), but the label is mostly
"did a trainer go back and record an adoption in this month", not "did the farmer adopt" (USE-5), so what the model
learns is the follow-up schedule I would be planning with it.

**1. Inputs at the prediction point (USE-3, USE-6, USE-10)**

- Have, and in the data: gender, age band, registration route, cooperative, group, county/sub-county/ward, trainer,
  the day's topics, the date. All are fixed at the end of the training day; no leak in the inputs as shipped, except
  `topics_list` still carrying the dropped `has_topic_trained_on` for TRA_szrwyfzz / TRA_hyodnntj (AUC 0.87).
- Would always have, and missing:
  1. The farmer's history with us (earlier trainings attended, earlier adoptions). Most of our farmers are known
     entities (USE-10, "an entity seen before" +); Prior.csv holds it, but it is not used because, after the date
     swap, 20.3% of its rows come after the Train row. Rebuilt in true dates it adds AUC -0.02 to +0.16 per window.
     A real deployment would use it.
  2. What practice the training was about in a form I act on (the topic list is there; the practice adopted is not).
  3. Herd size / dairy production, phone type (smartphone vs USSD), distance to the trainer: DigiCow's own app logs
     these for registered farmers. Not in the release.
- Would not have: nothing in the shipped columns.

**2. Target (USE-5, USE-8)**

- What I act on: whether the farmer adopts the practice at all (90-120 days is the horizon an extension programme
  reports on), and really whether a follow-up changes that (uplift). 7 days is the challenge's main target; it is a
  plausible short-horizon signal, but most real adoption in the source is at days 8-120.
- What the label is: adoption as recorded. Of 120-day adopters, 0 of 339 / 0 of 237 / 1 of 445 adopted within 7 days
  for trainings of Aug / Sep / Oct 2024, against 45%, 64%, 95% for Nov 2024, Dec 2024, Feb 2025; 2024-12-12 lies
  inside the adoption interval of 1,028 of 2,389 adopters; TRA_gertumxc's 2025 farmers never adopt at any horizon;
  TRA_ubcgvofe has no 7-day adopter in 4,447 rows. A farmer's behaviour does not jump like that between neighbouring
  months; a recording campaign does. A 0 mixes "did not adopt" with "nobody asked".
- This is worse than a noisy proxy for my decision: if adoption is recorded when a follow-up happens, then a model
  trained on it ranks farmers by "will be followed up", and using it to plan follow-ups is circular. The leak probe's
  best single features are sub-county 0.778, ward 0.775, trainer 0.762, i.e. who recorded.
- Form: I want a calibrated probability (to size the follow-up list and to report expected adoption), so Zindi's
  rubric (7-day log loss 0.65, 7-day AUC 0.15, 90/120-day log loss and AUC 0.05 each; the page says log loss 75%,
  ROC AUC 25%) matches the actor better than ROC AUC alone. But with the base rate moving from 0.06% (Mar-Oct 2024) to
  8.7% (Nov-Dec 2024) by recording, calibration over time is not learnable; log loss would mostly score the guessed
  recording rate of the next window. ROC AUC is the defensible benchmark metric here (ranking for a follow-up list),
  and the right one for a fixed-capacity list. Neither metric repairs the label.

**3. Row, test data**

- One row = one farmer at one training day: matches one decision (score this farmer after today's session). But the
  release keeps one training per farmer (the latest in stored-date order), while I score every attendance; one row per
  entity is fine only when the use case is that row (USE-11), and here it is a construction of the challenge.
- 48.7% of rows are exact copies (different farmers, same session and profile): realistic, since farmers of one
  group share everything I know about them; that also means within a session I cannot rank them at all, and the
  decision collapses to ranking sessions / trainers.
- Test = the next four months of trainings: what I would face (next season, same trainers, mostly known wards). The
  windows hold 9, 5, 19, 103 adopters from 1, 1, 2, 7 trainers and 3, 3, 8, 52 sessions: one trainer decides each of
  the two newest windows. I could not tell a good model from a lucky one on that.

**4. Would I use this model?**

No, not as built. I would distrust any model whose top features are trainer and ward, because those encode which
officer did follow-up recording in which month; and in the probes, a linear model (AUC 0.794) beats LightGBM (0.704)
with a single-feature probe at 0.551 and standard error 0.157 on mean skill, too unstable to choose a method.
What would make me trust it: adoption verified for every trained farmer at a fixed day (e.g. a call at day 7 and
day 90 for all, or a random audit sample), a column saying whether the farmer was followed up, and the farmer's
history. With those, the task is direct.

**Gaps, ranked by how much they change the task**

1. Label = recording, not adoption (USE-5): 0 means "not followed up" for whole trainers and months; the model learns
   the follow-up schedule it is meant to plan. Changes the task into "who recorded when".
2. Too few independent test units (1-7 trainers with adopters per window): the benchmark cannot rank methods.
3. Missing farmer history (USE-10): a known-entity task served as cold start; real use would carry prior trainings
   and prior adoptions.
4. Horizon: 7 days rather than the 90/120-day adoption a programme acts on; dropping the longer labels is right for
   leakage, but the actor's main target is the longer one.
5. Metric: Zindi weights calibrated probability (log loss); the benchmark scores ROC AUC. Acceptable for a
   follow-up list; secondary to 1-2.
6. One row per farmer by the challenge's construction; the swapped dates leave only days 1-12 of each month.

**What a domain expert would change**

- Get from DigiCow, per farmer and training, whether and when a follow-up contact happened; restrict the label to
  farmers who were contacted (or model "not followed up" as missing, not 0). Without it, retire.
- Predict 90-day adoption among followed-up farmers, with the farmer's history from Prior.csv rebuilt in true dates.
- Keep all trainings per farmer with a temporal split, not one row per farmer.
- Say what practice was adopted; split the task by practice if they differ.

**Verdict**

Agree with the definition's fit `approximate` and its retirement recommendation (`Too Small`, `Data Quality Issue`).
The fit_reason could say plainly that the label tracks follow-up recording, which is the input to the very decision
the model would serve. Rules: USE-1, USE-3, USE-5, USE-8, USE-10, USE-11, USE-12 (a leak alone would not reject it;
the label and the size do).

**Sources**

- dataset.py, README.md, REVIEW.md of datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/
- curation/records/digicow_farmer_training_adoption_challenge.md
- dataset_data_dictionary.csv (Zindi)
- the panel's task and leak probes
- Zindi challenge page: https://zindi.world/competitions/digicow-farmer-training-adoption-challenge
- https://en.reset.org/how-digicow-is-transforming-farming-in-kenya-one-voice-note-at-a-time/
- https://bigdata.cgiar.org/?p=600076
- https://www.citinewsroom.com/2019/04/kenya-taps-into-technology-to-attract-youth-to-farm/

</details>

<details><summary>Blind review</summary>

**Blind review: DigiCow farmer training adoption (adopted_within_07_days)**

**Verdict: exclude.** The use case is real, but there are too few positives to score: 153 of 13,536 rows (1.1%), and they fall in a few bursts. Half of the rows are duplicates. The 7-day horizon is the weakest of the source's three targets.

**Task**
DigiCow (Kenya) runs farmer training through extension staff, SMS/USSD and an app. It wants to know which farmers will adopt a practice after their first training, so it can follow up with them or target them. The Zindi challenge ran from January to March 2026 and asked for the probability of adoption within 7, 90 and 120 days, "using only information available at training time". The use case is real and the regime (temporal split on training_day) is right.

**Concerns, most serious first**
1. **Too few positives, unevenly spread over time.** There are 153 positives in total. 102 of them are in Nov-Dec 2024 (33+69) and 19 in Feb 2025. Eight of the 21 months have zero positives. I used four 10% time windows, each trained on all earlier rows. They held 1, 61, 60 and 14 positives. LightGBM AUC on those windows was 0.37, 0.47, 0.73 and 0.86. With so few positives, the score mostly reflects which campaign falls in which window, not model quality. **Change:** use the 90- or 120-day target from the same source (it should have more positives), or drop the dataset.
2. **Duplicates.** 6,590 rows (49%) are exact copies of another row, and 6,641 have identical features. There are 51 groups with identical features but conflicting labels. With no farmer ID, I cannot tell whether these are the same farmer trained several times or different members of the same group on the same day. Rows from one group-day can land on both sides of a split. **Change:** keep a farmer ID and use it to group or deduplicate, or document why the copies exist.
3. **Label driven by campaign and trainer.** Adoption rate by trainer ranges from 0.0% to 4.2%. The positives cluster in time, which suggests the label tracks campaign or recording practice rather than farmer behaviour.
4. **Preparation.**
   - topics_list is a free-text list. It has 2,250 unique values, spelling variants ("Poultry Health Management." vs "..") and up to 121 items per row. It should be parsed into multi-hot or count features.
   - "trainer" contains joined pairs, e.g. "TRA_kkzpfdtu, TRA_gertumxc".
   - The target is a "Yes"/"No" category; 0/1 would be cleaner.
5. **Leakage, not verified.** Rows with many topics have higher adoption rates (12% at 12 topics). If topics_list includes trainings held after training_day, it leaks future information. I could not check this.

**What I could not check**
- The data dictionary and the Prior.csv file: the Zindi data page needs a login.
- Source Train.csv has "17 features" against 11 here. I don't know which columns were dropped.
- The exact test windows used by the benchmark.
- Whether topics_list is limited to trainings up to training_day.

Sources: https://zindi.world/competitions/digicow-farmer-training-adoption-challenge/data ; https://zindi.africa/competitions/digicow-farmer-training-adoption-challenge

</details>

<details><summary>Precedent check</summary>

**Precedent check: digicow_farmer_training_adoption_challenge (2026-10-20)**

Inputs:
- the register of past decisions (808 decisions, 4 flags; none of the flags concerns digicow);
- the earlier `REVIEW.md`, the record and `dataset.py`;
- the rule texts in `.claude/skills/knowledge-curation/references/` (`task_probes.md`, `splits.md`, `leak_checks.md`) and `.claude/skills/knowledge-data-foundry/references/definitions.md`.

**Precedents used**

| Dataset | Date, by | Decision | Facts that matter | Source |
|---|---|---|---|---|
| ghanas_indigenous_intel | 2026-10-01, Lennart | `No (Retired)`; `Too Small`, `Data Quality Issue`; "Revisit if ... the organisers can say which rain-gauge readings are missing" | Zindi, agriculture, labels recorded by farmers. The 6 test windows hold rain from 3-6 farmer-days by 1-4 farmers, counted in label batches rather than rows. "No rain" mixes "did not rain" with "did not measure" (stated as likely, not proven). This is the only case of LEAK-25. | `curation/records/ghanas_indigenous_intel.md` (CC 2026-10-01); `leak_checks.md` LEAK-25 |
| seismic_bumps | 2026-09-30, Lennart | retired, `Too Small` (TP-9, SPLIT-16) | Temporal; 0-5 positives per window. Even 2-3 wider windows (14-26 positives each) were judged too noisy. No fallback to an IID split. | `curation/records/seismic_bumps.md`; `task_probes.md` TP-9; `splits.md` SPLIT-16 |
| alvin_smart_money_management_classification_challenge | 2026-10-12, Lennart | `No`, `Too Small` (TP-8). Never shipped, so `No`, not `No (Retired)` | Zindi, temporal windows of 27-41 test rows from 5-12 users | record; `task_probes.md` cases |
| parkinsons_biomedical_voice_measurements / musk | 2026-10-05 / 2026-10-06 | retired / kept (TP-5) | A handful of units per fold is `Too Small`. A small but balanced dataset is not. | `task_probes.md` cases |
| african_credit_scoring_challenge | 2026-10-07, case table; curator issues still open | kept (TP-1 to TP-3) | Zindi, temporal, binary. 289 test defaults from many customers, 20-56 per window, ROC AUC | `task_probes.md` cases; its `REVIEW.md` |
| 2_month_survival_rate_prediction | 2026-10-12, Lennart | drop adls/adlsc, keep adlp, edu, income | Drops only the columns tied to a process after the prediction point; keeps the inputs known at that point | record CC 2026-10-12 |
| bias_correction_r_bias_correction_r_2 | 2026-10-07 | one target per v2 task, the source's choice | The source has several targets | register, "post-outcome feature" |
| ashrae_great_energy_predictor_iii / alfa_battle_2_0_task_2 | 2026-10-15 / 2026-10-13 | damaged values restored from the origin (kWh units / ruble amounts) | P5, PROV-13, the remedy ladder | `CLEAN-1`, `CLEAN-19` cases |
| zillow_prize, force_2020, african_credit | 2026-10-20, open | open cross-dataset item "TP-6 and definitions.md disagree on a competition's metric" | Defaults kept; an amendment of TP-6 is proposed | `datasets/_dev/tabarena-v0pt2/REVIEW.md`, "Rules and the benchmark harness" |

**Per decision**

**Issue 1: retire as `No` with `Too Small` and `Data Quality Issue`. **Consistent.****

- **Follows ghanas_indigenous_intel (2026-10-01).** The facts match:
  - a Zindi agriculture task;
  - labels whose 0 mixes "no event" with "not recorded" (LEAK-25, a Must: "retire unless the recording process can be recovered");
  - test windows whose positives come from 1-4 recorders;
  - the same markers and the same "revisit if the organisers document the recording" clause.
- **The digicow evidence is stronger than ghanas'.** Ghanas' bias was "likely rather than proven". Here TRA_gertumxc has 0 adopters in 4,906 rows from 2025 at any horizon, after those windows had closed. Three dates hold 83% of the adopters.
- **Follows seismic_bumps (2026-09-30)** under TP-9 and SPLIT-16: the IID, grouped and leave-one-trainer-out options were considered, and an IID fallback was rejected.
- **Follows alvin (2026-10-12):** Zindi windows built from a handful of users. Never shipped, so `No`, not `No (Retired)`.
- **african_credit_scoring_challenge (kept 2026-10-07) is not a contrary precedent.** The facts that set it apart are written down:
  - its windows hold 20-56 defaults (289 in all) from many customers;
  - digicow's two newest windows hold 9 and 5 adopters, all from one trainer;
  - african_credit has no recording-wave evidence.
- **Gap in the write-up: no rule IDs.** Issue 1 cites none. LEAK-25 (Must) and TP-9 / SPLIT-16 (Must) carry it, and LEAK-25 alone would justify retirement, as it did for ghanas.
- **Gap in the write-up: no wider-window line.** TP-9 names wider windows as "the alternative to try" (SPLIT-17), and seismic recorded that 2-3 windows did not help. Issue 1 lists shorter windows only. The 50% floor fixes the test pool at 136 adopters, 33 of them in 2025 from about 3 trainers, so wider windows cannot add adopters. One line saying so would close it.

**Issue 1, sub-point: counting `Too Small` in trainers and sessions. **Departs from the wording of TP-5, with a stated reason.****

- TP-5 counts units "in the unit the task is scored on". The scored unit here is the farmer row.
- By rows, the September-December 2024 window holds 103 adopters. That is more than any african_credit window and more than seismic's wider windows. The verdict for that window rests on the adopters coming from 7 trainers and 52 sessions.
- The stated reason: labels are recorded per trainer, in waves. Ghanas used the same reasoning when it counted farmer-days and farmers (one label per batch).
- This is a reasonable exception (P-level validity over the literal unit). It is the second case of counting in the unit that records the label, ghanas being the first. A third would make an amendment of TP-5 due ("count in the unit the label is recorded or clustered on").

**Issue 2: date swap repaired. **Consistent.****

- Follows the remedy ladder ("repair from the origin" first; P5, PROV-13). Precedents: ashrae kWh units (2026-10-15) and alfa_battle restored amounts (2026-10-13).
- The evidence is in the definition and was confirmed by the verifier.
- Note for the editor, not a consistency issue: the REVIEW and the definition use different numbers.
  - Whole-week gaps: 49.3% in the REVIEW, 42.7% in `dataset.py`.
  - 7-day adopters among Aug-Oct 2024 adopters: "1 of 1,021" (REVIEW, Train+Prior) against "1 of the 95" (`dataset.py`, Train only).
  - Each place should name the base it counts on.

**Issue 3: Prior.csv not used. **Departs with a stated reason.****

- LEAK-34 (Must) makes an entity's history legitimate under a temporal split. TP-6 favours the version the source defines, and Zindi shipped Prior.csv with the task. The precedent for richer source-backed features is alfa_battle (CLEAN-19, 2026-10-13).
- The stated fact: Prior.csv as shipped is damaged, because the swap puts 20.3% of the Prior rows after their Train row. The rebuild in true dates carries the same recording waves.
- The point is moot if the dataset is retired. If Lennart ships it instead, LEAK-34 and the remedy ladder ("fix the definition" before excluding) favour the rebuilt history, which adds AUC -0.02 to +0.16 per window.

**Issue 4: `has_topic_trained_on`. **The implemented drop is consistent; the issue's framing departs without a reason.****

- **Dropping the flag only (implemented) follows LEAK-10 and 2_month_survival (Lennart, 2026-10-12).** That decision dropped the columns tied to the post-point process and kept the inputs known at the prediction point.
- **"Drop both" goes further than the precedents.** LEAK-2 sweeps for columns that carry the same post-outcome marker, as with anes' 56 "no post IW" items. `topics_list` is the day's topics, known when the farmer is scored (LEAK-37, a Must). It predicting the flag (AUC 0.87) does not make it post-outcome. Dropping it would break LEAK-37 unless a fact shows the topics were recorded after the training day.
- **"Keep both" departs from LEAK-10 (Must)** while the flag goes with the adoption: in mixed sessions the flagged farmers hold all 56 adopters. LEAK-38 (keep with a note) covers anonymised fields only, which this field is not. Keeping it needs a fact showing the flag is set before the outcome.

```text
**Consistency check (AI, 2026-10-20):** issue 4 offers "drop both columns or keep both" for has_topic_trained_on and
topics_list; the precedents (2_month_survival_rate_prediction, Lennart 2026-10-12: drop adls/adlsc, keep adlp; LEAK-2
sweeps only columns carrying the post-outcome marker; LEAK-37 keeps inputs known at the prediction point) support
dropping the flag and keeping topics_list, the option implemented. What sets this case apart?
(a) the topics list is filled in after the training day by the same follow-up visit that records the adoption, so it
is post-outcome too (needs evidence), recorded as an exception; (b) treat it like 2_month_survival: drop the flag, keep
topics_list, with a note giving the AUC 0.87; (c) reopen 2_month_survival to match; (d) change LEAK-2 (an amendment).
```

**Issue 5: 7-day target. **Consistent.****

- Follows TP-6: the source's own scoring rubric puts 0.80 of the weight on the 7-day target.
- Follows bias_correction (2026-10-07): one target per v2 task, as the source chose it.
- Dropping the 90- and 120-day labels, which contain the 7-day label, follows LEAK-10.
- The record has no `Multi-target` tag, which is correct under `selection.md`.

**Metric (`roc_auc`). **Follows definitions.md; departs from it on the notes, without a reason. The TP-6 conflict is pending.****

- **The default follows definitions.md and african_credit.**
- **The notes are missing.** definitions.md also requires that "the notes name the original metric". `dataset.py` only says "most of the leaderboard weight" and does not name the rubric (log loss 0.75, ROC AUC 0.25 in total). This is likely an omission, and the fix needs no decision. The record's Andrej comment ("logloss 25% / ROC-AUC 75%") has the weights reversed; the AI's assessment of 2026-10-07 already says so.
- **Under the proposed TP-6 amendment, log loss would replace ROC AUC.** It is a probability metric that can rank model outputs, and a house default. One fact to weigh: as african_credit's drift flag showed, log loss reacts to the moving base rate, which here is the recording waves. Add digicow to the cross-dataset item. The point is moot if the dataset is retired.

```text
**Consistency check (AI, 2026-10-20):** digicow keeps roc_auc but its notes do not name the competition's metric
(log loss 0.75 / ROC AUC 0.25 over the three horizons), which definitions.md requires; zillow_prize names MAE in its
notes. What sets digicow apart? (a) nothing: an omission, add the rubric to the notes; (b) treat it like zillow_prize
and list it under the open TP-6 metric item; (c) -; (d) change definitions.md (part of the proposed TP-6 amendment).
```

**Drift and repeated exceptions**

- **No drift.** Every curator `Too Small` decision on a binary or temporal task retires the dataset: open_soil_data (09-23), seismic (09-30), ghanas (10-01), parkinsons (10-05), alvin (10-12). The keeps are multiclass short classes (TP-8) and musk (TP-5, balanced).
- **No third exception.** Counting by recording unit would be the second such case, after ghanas.
- **The register's flags** (few_minority, one_feature, scaling over all rows, trivial) do not involve this dataset.

**Files**

- `curation/records/ghanas_indigenous_intel.md`
- `curation/records/seismic_bumps.md`
- `curation/records/alvin_smart_money_management_classification_challenge.md`
- `curation/records/2_month_survival_rate_prediction.md`
- `datasets/_dev/tabarena-v0pt2/african_credit_scoring_challenge/REVIEW.md`
- `datasets/_dev/tabarena-v0pt2/REVIEW.md` (metric item)
- `datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/dataset.py`
- `.claude/skills/knowledge-curation/references/task_probes.md` (TP-5, TP-6, TP-9, Cases)
- `.claude/skills/knowledge-curation/references/leak_checks.md` (LEAK-2, LEAK-10, LEAK-25, LEAK-34, LEAK-37, LEAK-38)
- `.claude/skills/knowledge-curation/references/splits.md` (SPLIT-16, SPLIT-17)

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: digicow_farmer_training_adoption_challenge (2026-10-20)**

**Position.** I argue for the definition as built, and I don't argue for shipping it into the benchmark now. The definition itself recommends `No`. Every evidence agent agrees: the claim audit, column audit, split audit, practitioner, blind review and precedent check. I could not find a ranked rule that overrides LEAK-25 or TP-9. Points 1 to 4 defend what the definition got right, so that a curator who ships, or a future rebuild, keeps it. Points 5 to 7 are the concessions, each with the mildest remedy.

**1. The task is valid at P2 to P4 for everything the definition controls (USE-1, USE-3, LEAK-1, LEAK-10, all Must)**
- **Evidence for the use case:** Zindi states it: "using only information available at the time of training" and "prioritise follow-ups" (claim audit #1, #2).
- **Evidence for the inputs:** every kept column is known at the end of the training day (column audit, all rows "yes").
- **Evidence for the leak fixes:**
  - The nested 90- and 120-day labels are dropped (7 ≤ 90 ≤ 120 holds in every row; claim #26).
  - The flag is dropped (claim #27: all 57 of those trainers' 7-day adopters are flagged).
  - 0.0% of test rows have an exact copy in train once the string and date columns are counted (leak probe).
- **Answers:** the blind reviewer's concerns 2 and 5 (duplicates, future topics).
  - The 6,590 duplicate rows are distinct farmers from the same session. The copies always fall in the same window: 0.0% of test rows have a session-mate in train (split audit).
- **Why it outranks the objection:** nothing here is in dispute. It establishes that the failures below are about the label and the size, not the build.

**2. The split is the honest one (SPLIT-3, SPLIT-9/10, SPLIT-14, SPLIT-16; Must)**
- **Evidence:** the split auditor's verdict is "right with notes".
  - The use case is a stream and the windows are temporal.
  - The train side ends 20 to 51 days before each test window, so every 7-day label has matured.
  - Every window keeps at least 50% of the rows on the train side.
- **Alternatives tested:**
  - An IID split would reward a trainer × month lookup (AUC 0.937), and 97.5% of its test rows would have a session-mate in train.
  - Grouped splits use the wrong entity (SPLIT-4).
- **Why it outranks the objection:** the critic shouldn't propose a re-split. SPLIT-16 (Must) bars the IID fallback (precedent: seismic_bumps). Wider windows break SPLIT-14: 6-month windows leave 2 windows, and 5-month windows give 11, 3 and 122 adopters.

**3. Repairing the dates is the right remedy (PROV-13, P5; the remedy ladder's top rung)**
- **Evidence:**
  - Swapped back, Sundays fall to 4.9% of rows and whole-week group gaps rise to 42.7% (14.5% as stored; claim #22).
  - The true day is ≤ 12 in every file.
- **Precedents:** ashrae units and alfa_battle amounts (precedent check, "consistent").
- **What follows:** Prior.csv stays out. As shipped, 20.3% of its rows for Train farmers come after the farmer's Train row (claim #24 holds), so LEAK-1 (Must) beats TP-6.

**4. `topics_list` stays, with a note; don't drop it (LEAK-37, Must; precedent 2_month_survival_rate_prediction)**
- **Evidence:** the topics are the day's sessions, known at the prediction point.
  - They predict the dropped flag at AUC 0.87 to 0.90.
  - They predict adoption at 0.649 inside the 82 mixed sessions. Adopters have 4.71 topics against 3.22, which the column audit reads two ways: more sessions attended (a real engagement signal) or the flag carried over.
- **Precedent:** Lennart dropped only the post-point columns of 2_month_survival and kept the inputs known at that point. The precedent check calls "drop both" a departure without a reason.
- **Mildest remedy:** a `Potential leak, kept on purpose:` note with these numbers (LEAK-30 tension row). This answers REVIEW issue 4's open "drop both or keep both".

**5. Conceded: LEAK-25 holds and can't be fixed from the data (P4, Must)**
- **Evidence:**
  - Of the 120-day adopters trained in Aug to Oct 2024, 1 of 95 adopted within 7 days, against 69 of 77 in December 2024 (D3, exact).
  - TRA_gertumxc has 0 adopters in 4,906 Train+Prior rows from March to July 2025, at any horizon.
  - The strongest single features are who recorded: subcounty 0.778 and trainer 0.762, against 0.691 for all features.
- **Precedent:** ghanas_indigenous_intel, which had weaker evidence.
- **Remedies checked:**
  - Filtering out the non-recording trainers or periods doesn't recover the 7-day timing, and it would shrink the adopter count further.
  - The 90- or 120-day target, the blind reviewer's suggestion, shows the same waves (REVIEW issue 5).
- **What follows:** `No` with `Data Quality Issue`. Revisit if DigiCow supplies per-farmer follow-up records, as the definition says. Ranking doesn't change this: USE-12 protects a task from a feature leak, not from a censored label.

**6. Conceded: TP-9 `Too Small` holds (P6, Must)**
- **My best counterargument:** TP-5 counts "in the unit the task is scored on", which is farmer rows. By rows, the Sep to Dec 2024 window holds 103 adopters, more than any african_credit window.
- **Why it fails:**
  - TP-9 counts per window, and the newest windows hold 9 and 5 rows, all from one trainer's 3 sessions.
  - Linear AUC is 0.49 on the 2024 window, whose 17 train adopters all belong to one trainer (split audit).
  - The probes flag `no_spread` under reading 2.
- **Precedents:** seismic_bumps and alvin. Counting units by trainer would be a second exception after ghanas (precedent check), but the verdict doesn't depend on it.
- **What follows:** `Too Small`. Under the "independent failures are not conflicts" principle, point 1's validity doesn't rescue it.

**7. The audits' findings need wording fixes, not code (procedure, writing.md; definitions.md)**
Mildest remedy for each:
- **U1:** Train.csv holds only true days 1-4 of each 2025 month, so the 2025 windows are a slice of each month. Say so in `row`, `splits_comment` and the curation comments.
- **#32:** the curation comment's 45/64/95% are Train+Prior figures. Name the file, or quote D3's Train figures (73/90/100%).
- **#55:** the record's log loss 25% / ROC AUC 75% is reversed. Strike or fix the line.
- **#61:** the REVIEW's 49.3/14.7% can't be reproduced. Use 42.7/14.5%.
- **Metric:** name Zindi's rubric (log loss 0.75 / ROC AUC 0.25) in the notes, as definitions.md requires. Keep `roc_auc`, which the practitioner backs for a fixed-capacity follow-up list.
- **#27:** reword "two trainers", since TRA_twwcfcum shows the same pattern.
- **Markers:** none of these changes the verdict. The record's front matter (`suggestion: 'Yes'`, no markers) is the curator's field to update.

**Judgment record (advocate's view):** don't ship.
- **Validity:** USE-1 and USE-3 hold; LEAK-10 was triggered and fixed (two later labels and the flag dropped); SPLIT-3 and SPLIT-14 hold; PROV-13 was repaired; LEAK-25 is triggered and can't be fixed.
- **Value:** TP-9, `Too Small`.
- **Quality:** CLEAN-1 (topic spellings), keep with a note.
- **For the curator:** keep `topics_list` with a note if the definition is ever revived (point 4).

Files: datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/dataset.py and the panel's reports this brief cites.

**Advocate rebuttal: digicow**

**1. The label records follow-up (LEAK-25, Must): conceded**
My brief conceded this as its point 5. The critic's added evidence holds:
- The trainer × month lookup scores 0.937 to 0.950 under a random split.
- Dropping subcounty lowers the all-features AUC from 0.691 to 0.669, so the signal sits in the label, not in a column.

What follows:
- Exclude, and keep the clause "revisit if DigiCow documents who was followed up and when".
- The ghanas_indigenous_intel precedent applies a fortiori, since its evidence was weaker.
- USE-12 does not help: it protects a task from a feature leak, not from a censored label.

**2. Too few adopters per window (TP-9, Must): conceded, with one dispute on the evidence**
The verdict stands on the counts alone:
- The windows hold 9 and 5 adopters, each from one trainer's 3 sessions.
- No legal width fixes it: SPLIT-14 and SPLIT-17 are exhausted, and SPLIT-16 bars an IID fallback.

The dispute: the critic cites "standard error of the best family's mean skill 0.157" as a sign of noise. The 2026-10-15 amendment to `unstable` (task_probes.md, flags table) says that for temporal tasks the standard error counts only when the best family loses to the dummy on a window. Here linear beats the dummy on 4 of 4 windows. The 0.157 is not admissible under that rule, and the critic's "±0.408" is the single-feature probe's spread, not a property of the methods.

The decisive evidence is TP-9's count of units, plus the atypical 2024 window:
- Linear scores 0.49 there.
- Its 17 train adopters all come from TRA_hyodnntj.

The verdict is unchanged. The judgment record should rest on the counts, not on the standard error.

The critic's `No` rather than `No (Retired)` is right: the dataset was never shipped (precedent: alvin).

**3. The 2025 windows hold days 1-4 only (Should): conceded, with one wording correction**
Claim audit U1 confirms the fact, and the remedy (a note) matches my brief's point 7.

The correction: "nothing in the definition says" overstates it. The definition does say "the release holds days 1-12 of each month only". What it misses is that Zindi's Train/Test cut, made in stored order, also leaves 2025 with days 1-4. The note should add exactly that sentence and nothing more. It is not a leak and not label-driven.

**4. `topics_list` (LEAK-10/LEAK-2 weak, LEAK-37): agreed**
The critic's remedy is my point 4:
- Keep `topics_list` with a `Potential leak, kept on purpose:` note.
- Precedent: 2_month_survival_rate_prediction (Lennart, 2026-10-12).

This settles REVIEW issue 4 in favour of option (b). "Drop both" has no fact to support it. I also agree with rewording "two trainers" (TRA_twwcfcum).

**5. Metric not named in the notes (definitions.md): agreed**
- Name the rubric: log loss 0.75 / ROC AUC 0.25, and 7-day log loss 0.65.
- Keep `roc_auc`.
- Add the dataset to the open TP-6 item.
- The record's Andrej line is stale (claim #55).

**6. Two sets of numbers, and the codebook against the data (EV-1, writing): agreed**
- Name the base of each figure (Train or Train+Prior).
- Replace REVIEW's 49.3/14.7% with 42.7/14.5%.
- Add one sentence saying the label is per training row: 18.8% of rows are not the farmer's first training (U2).

I agree U2 answers the split auditor's open SPLIT-9 question for the label as shipped.

**7. Record fields contradict the recommendation: agreed**
These are the curator's fields (`suggestion: 'Yes'`, no markers). Flag them for Lennart and change nothing.

**Net**
- **Disputed:** only the standard error behind point 2. It does not change the verdict.
- **No new points.**
- **Joint judgment record:** don't ship.
  - Validity: LEAK-10 was triggered and fixed. PROV-13 was repaired. SPLIT-3 and SPLIT-14 hold. LEAK-25 is triggered and cannot be fixed.
  - Value: TP-9, `Too Small` (counts per window).
  - Quality and writing: notes for U1, U2, #32, #55, #61, the metric rubric and `topics_list`.
  - For the curator: the verdict fields (point 7).

</details>

<details><summary>Critic</summary>

**Critic, opening brief: digicow_farmer_training_adoption_challenge (2026-10-20)**

**Ask: do not ship (`No`, never shipped, so not `No (Retired)`; markers `Data Quality Issue`, `Too Small`).** Points 1
and 2 are each an unfixable Must on its own. Points 3-6 are what to change if the curator ships it anyway, or before
the folder is archived; none of them is a reason to exclude.

**1. The label records follow-up, not adoption (P4, LEAK-25, Must; P3, USE-5)**

- **Problem.** A 0 mixes "did not adopt" with "nobody recorded it". Which trainer recorded, and in which month, sets the
  label.
- **Effect.** The model learns DigiCow's follow-up schedule. The actor would then use it to plan that same follow-up,
  which is circular (practitioner, gap 1). A benchmark score ranks methods on how well they recognise the recording
  waves.
- **Evidence.**
  - Among 120-day adopters, the share who adopted within 7 days is 1 of 95 for Aug-Oct 2024 trainings, against 33/45,
    69/77 and 19/19 for Nov 2024, Dec 2024 and Feb 2025 (D3, claim audit #47 holds).
  - TRA_gertumxc: 0 adopters at any horizon in 618 Train rows from Mar-Jul 2025 (0 of 4,906 in Train+Prior), although
    those windows had closed before the release. TRA_ubcgvofe has 0 adopters in 1,456 rows (claim audit #33, #51).
  - Each location or trainer column alone beats all features: subcounty 0.778, ward 0.775, trainer 0.762, all features
    0.691. Dropping subcounty gives 0.669, so the signal sits in the label, not in a column (leak probe; column
    audit, problem 1).
  - Under a random split, a trainer x month lookup scores 0.937-0.950 (split audit; claim audit #37).
- **Rule.** LEAK-25 says "retire unless the recording process can be recovered". It cannot be recovered: the release
  has no follow-up column, and Prior.csv carries the same waves (the earlier REVIEW.md, Train+Prior table). The precedent is
  ghanas_indigenous_intel (retired, LEAK-25), whose evidence was weaker than this (precedents, Issue 1).
- **Remedy.** Exclude. No drop, filter, re-split or re-target fixes a label (remedy ladder, last rung). Keep the
  "revisit if DigiCow documents who was followed up and when" clause.

**2. Too few adopters per window, under any legal split (P6, TP-9 narrows TP-5, Must; SPLIT-16, SPLIT-17)**

- **Problem.** The test windows hold 9, 5, 19 and 103 adopters. These come from 3, 3, 8 and 52 sessions and from 1, 1, 2
  and 7 trainers. Each of the two newest windows scores one trainer's 3 sessions.
- **Effect.** The scores cannot tell a good model from a lucky one.
  - The standard error of the best family's mean skill is 0.157.
  - The single-feature probe varies by +-0.408.
  - The Sep-Dec 2024 window scores AUC 0.49 (linear) and 0.51 (LightGBM), against 0.88-0.94 on the other windows.
    Its train side holds 17 adopters, all from TRA_hyodnntj, so the window measures the shift in recording (task
    probes; split audit, problem 2).
- **Evidence for "no split fixes it".**
  - With 3-month windows, Apr-Jun 2025 has no adopter (claim audit #42).
  - 5-month windows give 11, 3 and 122 adopters. 6-month windows give only 2 windows above the 50% train floor, which
    breaks SPLIT-14.
  - All of 2025 holds 33 adopters from 2 trainers (split audit).
  - IID is barred: 97.5% of test rows would have a session-mate in train (SPLIT-16, SPLIT-29).
- **Rule.** TP-9 (Must). The precedents are seismic_bumps and alvin (precedents: "no drift", every curator `Too Small`
  call on a binary temporal task retired it).
- **Remedy.** Exclude. The windows are already as wide as SPLIT-14 allows.

**3. The 2025 test windows are days 1-4 of each month, which nothing in the definition says (P4/P3, SPLIT and USE-8, Should)**

- **Problem.** Zindi cut Train and Test in stored-date order. Train.csv therefore holds true days 1-4 only of each 2025
  month (2,218 rows); days 5-12 went to the unlabelled Test.csv (claim audit U1, refuted).
- **Effect.** "Four calendar months of trainings" overstates the 2025 windows: they are a day-of-month slice, sampled
  differently from 2024. This is why they hold about 720-770 rows against 4,264. It adds to point 2 and is no leak.
- **Remedy.** A note: one sentence in `row`, `split`, `splits_comment` and the curation comments.

**4. `topics_list` still carries the dropped flag (P4, LEAK-10 / LEAK-2, weak, so Should)**

- **Evidence.** In the two flag trainers' rows, topics predict `has_topic_trained_on` with AUC 0.885-0.902 and the
  7-day label with 0.877. Within the 82 mixed sessions they give 0.649 on 56 adopters (column audit, problem 2; claim
  audit #28).
- **Remedy.** If shipped: drop the flag and keep `topics_list`, as implemented, with a
  `Potential leak, kept on purpose:` note giving these numbers (the precedent's option (b); LEAK-37 protects inputs
  known at the prediction point). Also reword "two trainers": TRA_twwcfcum's single flagged row is its single adopter,
  and a flag of 0 never adopts for any trainer (claim audit #27).

**5. The notes do not name the competition's metric (definitions.md house rule; TP-6 item open)**

- **Evidence.** Zindi scores log loss 75% and ROC AUC 25% (rubric: 7-day log loss 0.65, 7-day AUC 0.15). `dataset.py`
  says only "most of the leaderboard weight". The record's Andrej comment has the weights reversed (claim audit #55;
  precedents, Metric).
- **Remedy.** Name the rubric in the notes, and add the dataset to the open TP-6 metric item. Keep `roc_auc`: log loss
  would mostly score the guessed recording rate of the next window (practitioner, section 2).

**6. The definition counts the same thing with two different numbers, and the codebook disagrees with the data (EV-1, writing)**

- **Numbers.**
  - The curation comments give 0% / 45% / 64% / 95% (Train+Prior) for the wave, while D3 gives 1/95, 73%, 90% and 100%
    (Train), and neither names its file (claim audit #32, refuted as written).
  - REVIEW's 49.3% / 14.7% "trainer-days" cannot be reproduced; the definition's own figure is 42.7% / 14.5% (#61).
- **Codebook.** The codebook anchors the label and the date to the farmer's first training. The data anchor them to the
  row's own training: 2,540 rows (18.8%) are not the farmer's first training in true dates (claim audit U2; column
  audit, problem 3). This also settles the split auditor's SPLIT-9 question for the label as shipped.
- **Remedy.** Name the base of each figure, and add one sentence saying the label is per training row, not per first
  training.

**7. The record's fields contradict the recommendation (procedure; the curator's fields)**

- **Evidence.** The record has `suggestion: 'Yes'` and no `Too Small` or `Data Quality Issue` marker, while the
  definition and REVIEW recommend `No` (claim audit #53).
- **Remedy.** Nothing for the AI to change. Flag it for Lennart so the verdict fields match his decision.

Not raised: dropping the 90/120-day labels and `ID`/`farmer_name`, the date swap, and not using Prior.csv. All
are consistent with LEAK-10, PROV-13 and the precedents (precedents, Issues 2, 3 and 5), and Prior.csv is moot under
point 1. Topic spelling variants (CLEAN-1) are quality only: at most a note.

**Critic, rebuttal: digicow_farmer_training_adoption_challenge (2026-10-20)**

We agree on the verdict: don't ship, recorded as `No` with `Data Quality Issue` and `Too Small`, under LEAK-25 and TP-9
(advocate points 5 and 6). The remaining differences are about the rules cited and the wording. None of them changes
the verdict.

| Advocate point | Response | Evidence and rule |
|---|---|---|
| 1. Valid at P2-P4 for what the build controls | **Concede.** One addition for point 7: the codebook ties the label and the date to the farmer's *first* training, but in the data they belong to the row's own training. 2,540 rows (18.8%) are not the farmer's first training. | claim audit U2; column audit, problem 3; EV-1. The remedy is one sentence in the notes. |
| 2. The split is the honest one | **Concede.** I proposed no re-split. My point 2 rests on this same evidence. | split audit; SPLIT-14, SPLIT-16 |
| 3. The date repair is right; Prior.csv stays out because LEAK-1 beats TP-6 | **Concede the repair. Dispute the Prior.csv reason.** The 20.3% of Prior rows that come after the Train row are an artefact of the stored dates. A history rebuilt in true dates, using only rows before each Train row, is legal: LEAK-34 (Must) allows an entity's history under a temporal split. Prior.csv stays out because the task is retired, not because LEAK-1 bars it. If the task is ever revived, the rebuilt history is the remedy to try first. | precedents, Issue 3 (LEAK-34, alfa_battle CLEAN-19); practitioner, gap 3 (AUC -0.02 to +0.16 per window, untested: claim audit #62) |
| 4. Keep `topics_list` with a note | **Concede the outcome.** Drop the flag, keep the topics, and add a `Potential leak, kept on purpose:` note, as my point 4 asks. **Dispute the rule cited.** The LEAK-30 tension row covers transforms the source computed over all rows, and this is not one. The note rests on LEAK-2 / LEAK-10 graded weak (Should), with LEAK-37 (Must) keeping an input known at the prediction point. | column audit, problem 2 (0.885 for the flag, 0.649 inside mixed sessions, two readings); precedents, Issue 4, option (b) |
| 5. LEAK-25 conceded | Agreed. | |
| 6. TP-9 conceded | **Agreed, with one correction.** `no_spread` is a TP-3 flag about spread between model families. It is not evidence for `Too Small`. TP-9 rests on 9, 5, 19 and 103 adopters from 1, 1, 2 and 7 trainers, plus a standard error of 0.157 on mean skill. | task probes; TP-3, TP-9 |
| 7. Wording fixes | **Agreed**, item for item. It matches my points 3, 5, 6 and 7. The list should also take the U2 sentence from row 1. | claim audit #27, #32, #55, #61, U1, U2 |

The judgment record we share: don't ship.
- Validity: LEAK-25 is triggered and cannot be fixed. LEAK-10 was fixed. The weak LEAK-2 signal in `topics_list` is kept
  with a note.
- Value: TP-9, `Too Small`.
- Quality: CLEAN-1, kept with a note.
- For the curator: the record's front matter is still `suggestion: 'Yes'` with no markers.

</details>

<details><summary>Mediator</summary>

**Mediator: digicow**

**Recommendation (judgment record)**

```text
Verdict: don't ship. `No` (never shipped), markers `Data Quality Issue`, `Too Small`.
Validity: SEL-1, SEL-2 hold. USE-1, USE-3 hold (fit approximate). PROV-13 triggered, repaired (day/month swap).
  LEAK-10 triggered, fixed (90/120-day labels and has_topic_trained_on dropped). LEAK-37 keeps topics_list (note).
  SPLIT-3, SPLIT-14, SPLIT-16 hold. LEAK-25 triggered, cannot be fixed: the label records the trainer's follow-up
  waves (Aug-Oct 2024: 1 of 95 120-day adopters within 7 days, against 69 of 77 in Dec 2024; TRA_gertumxc 0 adopters
  in 4,906 Train+Prior rows of 2025); exclude.
Value: TP-9 (Must; narrows TP-5): the test windows hold 9, 5, 19 and 103 adopters; the two newest come from one
  trainer's 3 sessions each. Wider windows are exhausted (SPLIT-14, SPLIT-17); IID is barred (SPLIT-16). `Too Small`.
Quality: CLEAN-1 (topic spelling variants), kept with a note.
Weighed: real use case +, company source +, size -. None of these can override a Must.
For the curator: issue 1 (set the record's verdict fields); issue 2 (optional: a home rule for the topics_list kind
  of note).
```

**Independent failures, not conflicts.** USE-12 protects a real task from a feature leak, not from a label that mixes "did not adopt" with "nobody recorded it". LEAK-25 and TP-9 each hold on their own, and the remedy ladder ends at exclusion for both:
- **LEAK-25:** no drop, filter, re-split or re-target recovers the recording process. The 90- and 120-day targets show the same waves.
- **TP-9:** the windows are already as wide as SPLIT-14 allows.

**The four disputes**

1. **The standard error 0.157 as TP-9 evidence. The advocate wins.**
   - The 2026-10-15 amendment of `unstable` (task_probes.md flags table; evidence.md readings table) says that for a temporal task the standard error counts only when the best family loses to the dummy on a window.
   - The probe output says linear "beats the dummy on 100% of the splits", and the probe raised no `unstable` flag.
   - The amendment's reason applies equally when the 0.157 is cited loosely as "noise": the level drifts between windows.
   - The critic's ±0.408 is the single-feature probe's spread, not a property of the methods.
   - TP-9 rests on the counts per window, plus the atypical Sep-Dec 2024 window: linear AUC 0.49, with all 17 train adopters from TRA_hyodnntj.
2. **Whether `no_spread` counts for TP-9. The advocate wins, with the critic's caveat.**
   - In evidence.md's readings table, reading 2 of `no_spread` is "a handful of units of a class", which leads to TP-5 (Must) `Too Small`. Reading 1 fails because the label is the source's own.
   - Under EV-3 the first reading that holds decides. So the record may name the flag and its reading.
   - The flag is still a question, not evidence (EV-3, TP-1), and no tuned results are cached. The verdict rests on the counts, which are measured on the data and are not a flag.
3. **The rule behind the `topics_list` note. Neither side is right on the citation; both are right on the outcome.**
   - The critic is right that LEAK-30 is out of scope. It covers transforms computed over all rows, and the topic list is not one.
   - The critic is wrong that LEAK-2 or LEAK-10 is "graded weak, so Should". Both are ungraded Musts; only LEAK-30 is graded by strength.
   - LEAK-10 is not shown to be triggered. Predicting the dropped flag (AUC 0.885-0.902) does not make the topics post-outcome, and no fact shows they were recorded after the training day.
   - The keep therefore rests on LEAK-37 (Must: an input known at the prediction point). The precedent is 2_month_survival_rate_prediction (Lennart, 2026-10-12).
   - The note records an open reading under EV-3: within the 82 mixed sessions the topics predict adoption at AUC 0.649. That reads two ways: more sessions attended, or the flag carried over.
   - It borrows the `Potential leak, kept on purpose:` format from LEAK-38, by analogy only, because LEAK-38's scope is anonymised fields.
4. **Why Prior.csv stays out. The critic wins.**
   - LEAK-1 is the procedural rule ("write down the prediction point") and bars nothing by itself.
   - LEAK-34 (Must; narrows LEAK-10) makes an entity's own history legitimate under a temporal split, and it wins within its scope.
   - The 20.3% of Prior rows that fall after their Train row (0.0% in stored order) would be removed by a true-date filter that keeps only earlier rows.
   - Prior.csv stays out because the dataset is not shipped. If the dataset is revived, the true-date history is the first fix to try (remedy ladder "fix the definition"; TP-6; USE-10).
   - It carries the same recording waves, so it does not cure LEAK-25. Its AUC gain of -0.02 to +0.16 is untested (claim #62).

**Changes to make now (no decision needed)**

All of these are in the folder's `dataset.py`, its README (regenerated) and its REVIEW.md. None touches the curator's fields.
1. **U1, the 2025 windows** (USE-8, writing): add one sentence to `row`, `splits_comment` and the curation comments. Zindi cut Train/Test in stored-date order, so Train.csv holds true days 1-4 of each 2025 month. Days 5-12 went to Test.csv.
2. **U2, the label's anchor** (USE-5, EV-1): the label belongs to the row's own training, not the farmer's first training. 2,540 rows (18.8%) are not the farmer's first training in true dates. This also corrects comment 35 against the codebook.
3. **#32, the wave figures** (EV-1, writing): name the file each figure counts on. Train+Prior gives 45/64/95% and 1/1,021; Train gives 73/90/100% and 1/95.
4. **#61, REVIEW.md** (EV-1): replace 49.3/14.7% with 42.7/14.5% (Train, group gaps).
5. **#55, the record's comment** (writing): the Andrej comment reverses the metric weights. Add an AI correction line under it rather than rewriting it.
6. **Metric** (definitions.md): name Zindi's rubric in the notes. That is log loss 0.75 / ROC AUC 0.25 overall, with 7-day log loss 0.65 and 7-day AUC 0.15.
   - Keep `roc_auc`.
   - Add digicow to the open cross-dataset TP-6 metric item in the tabarena-v0pt2 REVIEW.md.
7. **#27, the flag pattern** (EV-1): reword "two trainers". TRA_twwcfcum's single flagged row is its single adopter, and a flag of 0 never adopts for any trainer.
8. **`topics_list` note** (LEAK-37 keep; EV-3): add a `Potential leak, kept on purpose:` note with the facts from dispute 3:
   - AUC 0.885-0.902 for the dropped flag;
   - AUC 0.649 inside the mixed sessions;
   - adopters average 4.71 topics against 3.22;
   - the two readings, and "revisit if the topics are shown to be recorded at follow-up".
9. **REVIEW issue 1** (TP-9, SPLIT-17; precedent checker): cite the rule IDs LEAK-25, TP-9 and SPLIT-16. Add the wider-window line: the 50% train floor fixes the test pool at 136 adopters, 33 of them in 2025, so wider windows cannot add adopters.
   - State TP-9 on adopter rows per window (9 and 5). Do not count trainers or sessions; that way no TP-5 counting-unit exception is created.
   - Drop the 0.157 and ±0.408 from the evidence (dispute 1).
10. **Prior.csv reason** (LEAK-34): it stays out because the task is not shipped; the true-date history is the first remedy if the task is revived.
11. **Domain** (writing): add a note that `environmental science & climate` is the closest fixed value for agriculture.

**Issues for the curator, ranked**

1. **The verdict fields (validity, Must: LEAK-25; value, Must: TP-9).**
   - **Problem:** the record has `suggestion: 'Yes'`, no `Too Small` or `Data Quality Issue` marker, and status `WIP (DF)`. Every report recommends `No`.
   - **Effect:** the record contradicts the recommendation until it is changed.
   - **Evidence:** both sides agree. There is no counter-evidence. The advocate's best case for keeping it was 103 adopter rows in Sep-Dec 2024, but TP-9 counts per window and the newest windows hold 9 and 5.
   - **Decision:** confirm `No` with `Data Quality Issue` and `Too Small`, plus the clause "revisit if DigiCow documents who was followed up and when".
2. **No rule fits a note on a known input that tracks a dropped post-outcome flag (P4, Should-level gap; moot while the dataset is out).**
   - **Problem:** LEAK-37 keeps the input, but no rule asks for the note. LEAK-30 is about all-row transforms, and LEAK-38 is about anonymised fields only.
   - **Effect:** none on this dataset. The next case will face the same citation question.
   - **Evidence:** the advocate cites the LEAK-30 tension row; the critic cites LEAK-2/LEAK-10 graded weak. Neither text supports its citation.
   - **Decision (optional):** leave it as a precedent, or widen LEAK-38 to host-released fields that may carry a post-outcome signal. Widening it would be an amendment.

**Agreed facts (all verified on the data or in the probe output)**

- **Rows:** 13,536 rows, one per farmer, from 2024-03 to 2025-12, with 153 adopters within 7 days.
- **Date swap:** day and month are swapped in the release. Swapped back, Sundays fall to 4.9% of rows and whole-week group gaps rise from 14.5% to 42.7%. The true day is at most 12 in every file.
- **Labels and flag:** the 90- and 120-day labels are nested (7 ≤ 90 ≤ 120 in every row) and are dropped. The flag `has_topic_trained_on` goes with adoption: flag 0 never adopts.
- **Recording waves:** in Aug-Oct 2024, 1 of 95 120-day adopters adopted within 7 days, against 69 of 77 in Dec 2024. TRA_gertumxc has 0 adopters in 4,906 Train+Prior rows of 2025.
- **Who recorded:** single-feature AUC is 0.778 for subcounty and 0.762 for trainer, against 0.691 for all features. Under a random split, a trainer × month lookup scores 0.937.
- **Windows:** the test windows hold 9, 5, 19 and 103 adopters, from 1, 1, 2 and 7 trainers. 2025 holds days 1-4 only (U1).
- **Duplicates:** the 6,590 duplicate rows are distinct farmers from the same session. 0.0% of test rows have a session-mate or an exact copy in train.
- **Task probes:**
  - linear beats the dummy on 4 of 4 windows (AUC 0.794);
  - the standard error of its mean skill is 0.157;
  - the only flag is `no_spread`;
  - the smallest test class holds 5 rows;
  - no tuned results are cached.
- **Prior.csv:** 20.3% of the Prior rows of Train farmers fall after the Train row in true dates. Its history gain is untested (#62).

No decisive experiment was needed. The facts behind the four disputes are not contested; each dispute is about which rule applies.

**Consistency with precedent**

- **Follows:**
  - ghanas_indigenous_intel (LEAK-25; same markers and revisit clause). Its evidence was weaker than digicow's.
  - seismic_bumps (TP-9, no IID fallback).
  - alvin (`No`, not `No (Retired)`, for a dataset never shipped).
  - 2_month_survival_rate_prediction (drop the post-point column, keep the inputs known at the point).
  - ashrae and alfa_battle (repair from the origin).
- **Set apart:** african_credit_scoring_challenge, which was kept. It has 20-56 defaults per window from many customers and no evidence of recording waves.
- **No departure needs a reason** once TP-9 is stated on adopter rows (change 9). Counting by trainer would be a second counting-unit exception after ghanas, and the verdict does not need it.
- **Prior.csv:** leaving it out departs from LEAK-34/TP-6 only while the dataset is out. That fact is why the departure is allowed.
- **No drift:** every curator `Too Small` call on a binary or temporal task has retired the dataset (open_soil_data, seismic, ghanas, parkinsons, alvin).

Files:
- datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/dataset.py
- datasets/_dev/tabarena-v0pt2/digicow_farmer_training_adoption_challenge/REVIEW.md
- curation/records/digicow_farmer_training_adoption_challenge.md
- .claude/skills/knowledge-curation/references/task_probes.md (TP-5, TP-9, the `unstable` flag)
- .claude/skills/knowledge-curation/references/evidence.md (EV-3, readings table)
- .claude/skills/knowledge-curation/references/leak_checks.md (LEAK-1, LEAK-10, LEAK-25, LEAK-30, LEAK-34, LEAK-37, LEAK-38)

</details>
