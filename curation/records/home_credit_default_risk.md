---
unique_name: home_credit_default_risk
name: Home Credit Default Risk
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
tags:
- Larger IID Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
- 'Entities: Recur'
collections:
- New (BeyondArena)
- TabSTAR
original_source: Kaggle
year: '2018'
domain: finance
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://www.kaggle.com/c/home-credit-default-risk/data?select=application_train.csv
- https://www.openml.org/search?type=data&id=45567
notebook_path: datasets/beyond_iid/new_iid/home_credit_default_risk/home_credit_default_risk.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/home_credit_default_risk/dataset.py
source_row: 653
type_adapter_id: curation-record-v1
---

## Comments

Kaggle solutions used IID splits

CC (2026-10-01, Lennart): Leak audit: no leak. The label-aware feature selection taken from the kernel only drops zero-importance features (242 of them); selecting inside folds or not selecting at all gives the same AUC (0.788), and no aggregate uses the target or dates after the application. The v2 definition was restructured (no change to the data, identical frame hash): `_load_raw` reads all seven tables, `_clean` calls one helper per kernel function, the long column lists are module constants, an unused categorical list was removed, and `_feature_types` lists only the 22 categorical columns that survive the selection (it listed 25 dropped ones, so the definition did not build).

CC (2026-10-19, Lennart): the v2 definition computes nothing over all rows: the kernel's median income per organisation type is dropped, the mean fill of `NEW_SCORES_STD` removed, and the kernel's importance-based column selection not applied (every column stays). The kernel computed these over Kaggle's train and test applications, as a competition allows; whether that transductive setting should stay for this task can be checked later. The 43 normalised building columns are kept, with a `Potential leak, kept on purpose` note in the definition: a scaling over all rows is no strong leak and often happens in reality. It is a reason for `No` only when a strong leak is suspected or the data can be rebuilt.

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: the 35 features that hold only 0 and 1: FLAG_MOBIL, FLAG_EMP_PHONE, FLAG_CONT_MOBILE, FLAG_EMAIL, the four REG/LIVE region and city flags, 17 FLAG_DOCUMENT columns and 10 CC_NAME_CONTRACT_STATUS min/max aggregates (found on the data in `_feature_types`).

CC (2026-10-21, Lennart): on which 0/1 columns are flags: "no if we can infer from the semantic context, keep it a number, this is a real-world bias. We want to make things categorical if we know from the context they are indeed such" (CLEAN-14, amended again). Kept categorical: FLAG_MOBIL, FLAG_EMP_PHONE, FLAG_CONT_MOBILE, FLAG_EMAIL, the four REG_/LIVE_..._NOT_... flags and 17 FLAG_DOCUMENT columns (explicit list). Reverted: the 10 CC_NAME_CONTRACT_STATUS min/max aggregates stay numeric.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source roc_auc — Area Under Receiver Operating Characteristic Curve (Kaggle API evaluationMetric) (https://www.kaggle.com/competitions/home-credit-default-risk/overview/evaluation).

**Assessment (AI, 2026-10-26):** an open doubt under CLEAN-14, from the cross-dataset item of 2026-10-21: the 10 `CC_NAME_CONTRACT_STATUS_*` min/max aggregates were typed categorical and then reverted to numeric as aggregates over the card history, but the max of a one-hot status reads as "ever had this status", a yes/no flag by meaning. Typing them categorical is the curator's call.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 1 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `NAME_EDUCATION_TYPE` (the README lists their levels); left unordered: `WEEKDAY_APPR_PROCESS_START` (a partial order); ordinal scales shipped as numbers, left as numbers for the curator's review: `REGION_RATING_CLIENT`, `REGION_RATING_CLIENT_W_CITY`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 2 ordinal scales shipped as numbers are ordered categories (point 3); 1 calendar or compass cycles ordered.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 2 scores are numbers (REGION_RATING_CLIENT, REGION_RATING_CLIENT_W_CITY).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-11, Andrej): the review page's marks of 2026-11-11 applied (review issues 1 to 3).
- Issue 3 ("Reply (B): Later application tested"): `_make_splits` tests each client's latest application and keeps the client's earlier ones in training only. The client is the same sex and the same days between birth and ID issue and between birth and registration (16,489 applications, 5.4%, share one; inside a client `DAYS_BIRTH` gives the order, and in 61% of the pairs the later application lists the earlier one). 299,590 applications are tested in stratified grouped 3x3 folds, the 7,917 earlier ones (2.6%) are in every train side and never tested, which is an accepted check warning with that reason. The key is computed in the split, not a feature; the cost is 0.001 ROC AUC or less (LightGBM 0.7862 against 0.7865 on the 504-feature frame).
- Issue 2 ("Option B: Forced, with a full Time basis: line"): the `Tagged ForcedIIDFromTemporal:` bullet is now a `Time basis:` line with the time probe (the default rate flat along `SK_ID_CURR`; the earlier applications' ids do not follow their decision day, Spearman 0.02) and the leak test across the split, naming issue 3's split and what the random split cannot test. `data_tags` stays `("ForcedIIDFromTemporal",)`.
- Issue 1 (`discuss`, "Is that issue redundant now with the new split definition?"): answered in the review and left open. It is the ship-or-retire decision, which the split does not take; nothing argues against shipping, and the split change removed the one route the review had measured. The two stale texts named in the record judgment are corrected: the task summary says 709 features and says the notebook's feature selection is not applied.
- `dataset check` (Slurm job 1378328): 0 errors, 0 warnings (2 accepted), 2 info (the heavy duplicate checks skipped over the cell budget); folds train 207,621 to 207,663 and test 99,844 to 99,886 of the 307,507 applications.

## Review

**Outcome:** added. The AI recommends shipping it as defined. Reviewed on 2026-11-04 without a panel, from the
evidence already gathered (the record and the curator's leak audit; there is no model run on this dataset).
The data are Home Credit's Kaggle competition (2018): 307,507 loan applications, each joined with summaries of the
client's earlier loans from six linked tables (credit bureau loans, earlier Home Credit applications, their
instalment, card and cash-loan payment records), built as a popular public competition notebook does (709 features);
the target is whether the client paid late on one of the loan's first instalments (8%). Validity: a real lending
decision at the application; the curator's leak audit (2026-10-01) found no aggregate that uses the target or dates
after the application, and since 2026-10-19 the definition computes no statistic over all rows (the notebook's median
income per organisation type and its importance-based column selection are dropped). Home Credit scaled its 43
building columns over all applications, a weak leak the curator kept with a note. The release has no application
dates, so the split is random (over clients' latest applications since issue 3) and tagged as forced from temporal. Value: no benchmark spread on this definition; in the
leak audit untuned LightGBM reached ROC AUC 0.788, a real but modest signal. Quality: nothing open. Weighed: the
lender's own competition and a direct decision +, a large multi-table task +, no dates (random split) -, spread not
yet measured on this definition -.

**Main points:** Ship as defined (issue 1, open: the mark of 2026-11-11 asks whether the split decisions make it
redundant and is answered there)? Issues 2 and 3 resolved: forced from temporal with a full `Time basis:` line; each
client's latest application is tested with the client's earlier applications in training only (2.6% of rows never
tested).

**Record judgment:** valid, ship. Text to correct at hand-over (no mark needed): `task_summary` still says "504
features" and "keep the features it selected", but the definition ships 709 features and applies no selection since
2026-10-19. The Assessment of 2026-10-26 (whether the 10 `CC_NAME_CONTRACT_STATUS` min/max aggregates are yes/no
flags) was settled by the curator on 2026-10-21: they stay numbers.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the record holds the curator's decisions (no statistic over all rows, 709 built features without the notebook's label-based selection, the building columns Home Credit scaled kept with a note, a random split for lack of dates), and no fact found since contradicts them.
     - The one gap is value: no benchmark method has run on the 709-feature definition yet, and the curator's leak audit measured a real but modest signal (untuned LightGBM ROC AUC 0.788).
     - Ship as defined, or retire it?
   * **Background:** the features follow a popular public notebook of the competition: the application table with a
     few ratios, and per client the counts, means, minima and maxima of the linked tables[^1a]. In the curator's leak
     audit (2026-10-01), on the earlier 504-feature version, untuned LightGBM reached ROC AUC 0.788 with the
     notebook's selection, with a selection inside each fold and with none alike, so the dropped selection carried no
     score. The building columns are "normalized information about building where the client lives", each spanning
     exactly 0 to 1, so Home Credit likely scaled them over all applications; no raw values exist[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 307,507 applications, 709 features, random 3x3 splits | the lender's own task with a real signal; a large multi-table credit task; no leak found | spread on this feature set not yet measured; no dates for a temporal split |
     | B | Retire | `No (Retired)`, a CC line, the folder removed | less weight on finance | no defect found; loses the benchmark's multi-table credit task |

   * **Recommendation:** A, as no fact found argues against the definition. **Decision:** A or B?

   **Notes for the AI:** on A, correct the `task_summary` text named in the record judgment and add `Andrej` to the
   record's `checked_by` with a CC line of his decision.

   [^1a]: **CLEAN-19** (Should; amended 2026-10-21, Lennart): a feature is built when the raw data cannot be used as
     they are, a history aggregated to one row per prediction, taking the best of a published baseline and the top
     solutions' features.
   [^1b]: **LEAK-30** (Should when weak): features the source scaled over all rows are a weak leak, kept with a
     `Potential leak, kept on purpose:` note when no raw values exist (Lennart, 2026-10-19).

   **Andrej (2026-11-11, discuss):** Is that issue redundant now with the new split definition?

   **Answer (AI, 2026-11-11):** Not redundant, but nothing is left in it to weigh: it is the ship-or-retire decision,
   which the split does not take, and the new split only strengthens the case for shipping. Close it as A, or keep it
   open?

   * **Problem:**
     - Issues 2 and 3 settled the time basis and the split; this issue asks whether the dataset ships at all, which
       no split decision answers.
     - Its option A is now stale in one word: the folds are no longer plain "random 3x3 splits" but random 3x3 folds
       over each client's latest application, with the earlier ones in training only.
     - Nothing found since contradicts the definition, so there is no new argument for B (retire).
   * **Background:** the split change removes the one route the review measured across the split (a client's later
     application in training to score the earlier one), so the dataset is sounder than when the issue was written;
     the issue's one open gap stays what it was, that no benchmark method has run on the 709-feature definition.
   * **Experiments:** the new split, LightGBM, 3 folds: ROC AUC 0.7862 on the 504-feature frame and 0.7573 on the
     application table alone (issue 3's answer of 2026-11-11), against 0.7865 and 0.7578 under the plain random
     split, so the change costs nothing measurable and the signal is as the leak audit found it (0.788).
   * **Effect on the task:** none beyond the split; the rows, the features and the metric are unchanged.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Close it as A (ship) | the issue is resolved with the definition as it now stands, the stale wording corrected | nothing is left to weigh; the split decisions removed its one measured concern | the value gap (no method spread measured on 709 features) is then recorded only in the outcome |
     | b | Keep it open | the ship decision waits until a benchmark run on the 709-feature definition exists | the spread would be measured before the dataset ships | no fact found argues against shipping, and the run is not part of this round |

   * **Recommendation:** a: the issue found no defect, and the split change answered the only thing it left measured.
     **Decision:** a or b?

   **Notes for the AI:** the record judgment's two stale texts are corrected whichever way it goes, and are already
   done: `task_summary.known` says 709 features, and `changes` says the notebook's feature selection is not applied.

2. **Time basis: keep the forced tag and write its `Time basis:` line with the leak test?**

   * **Problem:**
     - Applications arrived over a period Home Credit never states, each labelled by payment difficulties on its first instalments; every date in the release is relative to the application, and neither id carries time, so the time is lost.
     - The record's collection facts hold (`Samples: Over Time`, `Time: Lost`, `Target: Later`), and the definition already ships `ForcedIIDFromTemporal` with a short note.
     - A lender scores later applicants in a credit climate that moves, so the forced tag is the right basis; its line should carry the leak test across the split, which finds recurring clients (issue 3)[^2a].
   * **Background:**
     - Time probe: the default rate is flat along `SK_ID_CURR` (7.9% to 8.3% per tenth). The ids of the earlier
       Home Credit applications do not rise with their decision day inside a client (Spearman 0.02, 224,669
       clients), so the application dates cannot be rebuilt from them: a fit of each application's date from those
       ids is no better than with the ids shuffled (median error 223 days in both).
     - No prototype fits: the applications share no prediction moment. The duty a delayed target brings, every
       feature existing at the application, is met by the curator's leak audit (2026-10-01): the bureau and earlier
       loan records end before the application, except 17 bureau updates of 1.7M.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Forced, note as now (implemented) | `ForcedIIDFromTemporal`, the note "applications arrive over time, but the release has no application dates" | nothing to write | the leak test the forced tag asks for is not stated |
     | B | Forced, with a full `Time basis:` line | the same tag; the note becomes a `Time basis:` line with the time probe and the leak test | states what the random split stands in for and what the test found | none found |
     | C | Forced grouped | `ForcedGroupedFromTemporal` with the client grouping | follows issue 3 if it groups | only if issue 3 takes its option C |

   * **Recommendation:** B, or C with issue 3's grouping. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in this working copy, on B: replace the `Tagged ForcedIIDFromTemporal:`
   bullet of `curation_comments` with `- Time basis: ForcedIIDFromTemporal: loan applications over a period Home
   Credit does not state, the label payment difficulties on the first instalments; a lender scores later applicants.
   Every date is relative to the application ("time only relative to the application"), the default rate is flat
   along SK_ID_CURR, and the earlier applications' ids do not follow their decision day (Spearman 0.02), so no date
   can be rebuilt (Time: Lost). Leak test across the split: 5.4% of the applications share a client with another
   (issue 3); <issue 3's outcome>. Application dates would allow a split by time.`; `dataset check`. On C: the same
   line with `ForcedGroupedFromTemporal` and the grouping of issue 3.

   [^2a]: **SPLIT-32** (Should): the record's collection facts and the five questions; samples over time whose period
     moves the target, with the time lost, get a forced split. **SPLIT-8** (Must): the forced split, tagged, after a
     leak test across the split (a row sharing its outcome, its unit's outcome or its period's outcome with the other
     side); a leak found is removed where it can be.

   **Resolved (2026-11-11, Andrej):** B: the `Tagged ForcedIIDFromTemporal:` bullet of `curation_comments` is now a
   `Time basis: ForcedIIDFromTemporal:` line with the time probe and the leak test (recurring clients, grouping open
   in issue 3) and what the random split cannot test; `data_tags` stays `("ForcedIIDFromTemporal",)`. Dataset check
   (Slurm job 1377467): 0 errors, 0 warnings; the README changes in this line, the checksum and generated lines only. The tag
   stays the same; no grouping until issue 3 is decided.

   **Andrej (2026-11-11, change):** Option B: Forced, with a full Time basis: line.

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: the `Tagged ForcedIIDFromTemporal:` bullet of
   `curation_comments` is replaced by the `- Time basis: ForcedIIDFromTemporal: ...` line with the time probe (the
   default rate flat along `SK_ID_CURR`, the earlier applications' ids not following their decision day) and the
   leak test across the split, which now names issue 3's split (each client's latest application tested, the earlier
   ones in training only), and says what the random split cannot test. `data_tags` stays
   `("ForcedIIDFromTemporal",)`.

3. **Applications of the same client sit on both sides of the split: group by the client?**

   * **Problem:**
     - 16,489 applications (5.4%) share their sex and the days between birth and ID issue and between birth and registration with another application, about half a year apart: the same client applying twice.
     - Their outcomes agree: when one application of a pair had payment difficulties, the other had them too in 34% of cases, against 8.1% overall, and half of their earlier-loan summaries are identical (median 53% of the 350 history columns).
     - Under the random split one application can be in training while the other is tested; group the split by this client key, keep it with a note, or keep it as is?
   * **Background:** the key uses only values fixed for a person (birth, ID issue, registration), written as day
     counts relative to each application, so their differences stay the same across a client's applications; two
     people matching on both differences and sex are rare, and a client who renewed the ID or moved between the
     applications is missed. 7,676 keys hold two applications, 328 hold three to ten. A client's earlier loan shows
     in the later application's history columns, which is legitimate history; the route that is not is the later
     application in training when the earlier one is tested[^3a].
   * **Experiments:** Slurm jobs 1366183 and 1366213, LightGBM, ROC AUC:

     | Features | Split | All rows | Rows of recurring clients |
     |---|---|---|---|
     | application table only, 5 folds | random | 0.7589 | 0.7413 |
     | | grouped by client key | 0.7578 | 0.7278 |
     | shipped BeyondArena features (504), 3 folds | random | 0.7864 | 0.7687 |
     | | grouped by client key | 0.7859 | 0.7613 |

   * **Effect on the task:** a small lift on the 5% of applications whose client recurs (0.007 to 0.014 ROC AUC on
     those rows, 0.001 or less overall).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as is (implemented) | random applications | no change | a client's other application sits across the split, unstated |
     | B | Keep, with a note | as A, plus a curation note with the numbers above | documents it | a measured leak with an exact fix stays |
     | C | Group by the client key | key from sex and the two day differences, out of the features; `ForcedGroupedFromTemporal` (issue 2) | removes the route at no cost to the score; the key is exact values, not a similarity | about 2.7% of the clients form groups; misses clients who renewed an ID or moved |

   * **Recommendation:** C: the route is measured, the key is built from values that define a person, and grouping
     costs nothing overall[^3b]. **Decision:** A, B or C?

   **Notes for the AI:** on C, in `_clean` compute `client_key` = `CODE_GENDER` + (`DAYS_BIRTH` - `DAYS_ID_PUBLISH`)
   + (`DAYS_BIRTH` - `DAYS_REGISTRATION`, rounded) before the features are built, declare the grouping on it (labels
   per row), keep it out of the features, set `data_tags = ("ForcedGroupedFromTemporal",)` once PR #50 is in, and
   reword `split`; a curation note with the numbers above; `dataset check`. Scripts of the time review of 2026-11-06:
   `time_ids.py`, `client_split.py`, `client_split_full.py`.

   [^3a]: **LEAK-34** (Must): an entity's own history under a temporal split is legitimate. **LEAK-17** (Must):
     repeated entities in different rows leak the target across the split even when the rows differ: keep one row per
     entity or group.
   [^3b]: **SPLIT-24** (Must): group on a true id or on one constructed exactly from the data (identical values in the
     columns that define the entity). **LEAK-6** (Must): a confirmed leak goes even when small. **SPLIT-8** (Must):
     grouped by the entity when the entities recur.

   **Andrej (2026-11-11, discuss):** You said half a year apart - does that mean a temporal connection is there and a
   temporal split would be possible?

   **Answer (AI, 2026-11-11):** No temporal split is possible. Time is known only inside a recurring client, as the
   gap between that client's own applications; there is no common clock across clients.

   * Every date in the release is a day count back from the client's own application (`DAYS_BIRTH`, `DAYS_EMPLOYED`,
     `DAYS_DECISION` of earlier applications, bureau `DAYS_CREDIT`), and no table has an application date.
   * Inside a client: the two applications' `DAYS_BIRTH` differ by the gap between them (median 175 days). In 4,587 of
     7,521 pairs the later application lists the earlier one among its earlier Home Credit applications, decided that
     many days before (within 3 days) and in 4,563 of them with the same credit amount. This confirms the client key.
   * Across clients nothing links the clocks: no earlier application (`SK_ID_PREV`) belongs to two current ones, bureau
     loans are per client, `SK_ID_CURR` does not follow time (the later application has the higher id in 46.5% of
     pairs) and the default rate is flat along it. The fit of dates from the earlier applications' ids (issue 2) does
     no better than shuffled ids.
   * home_credit_default_stability (2024, also Home Credit) shows what is missing: its base table has `date_decision`
     (2019-01-01 to 2020-10-05) and `WEEK_NUM` (0 to 91), its other tables hold absolute dates that the definition
     turns into days before the decision, and the default rate moves with the week (2.7% to 3.9% per fifth). The 2018
     release ships those day counts without the decision date. The two releases share no id and cover different
     years, so the 2024 dates cannot be carried over.
   * What an order inside clients would test: training on the earlier application and testing the later one of the
     same client, on 2.6% of the rows. That is predicting a returning client from their own record, not scoring later
     applicants, and it is the route issue 3's grouping closes.

     | What | Value |
     |---|---|
     | applications sharing the client key | 16,489 (5.4%), 8,004 clients |
     | gap between a pair's applications, median (p25-p75) | 175 days (96-392); 562 pairs on the same day |
     | later application lists the earlier one (same day count, within 3 days) | 4,587 of 7,521 (61%) |
     | later application has the higher `SK_ID_CURR` | 46.5% |
     | weekday difference equals the gap mod 7 | 66% (chance 14%) |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No temporal split; decide grouping in issue 3 | random split stays forced (issue 2); grouping by the client key as issue 3 asks | matches what the data hold | cannot test drift for later applicants |
     | B | Within-client order | each recurring client's later application tested, the earlier trained | uses the only order there is | 2.6% of rows; tests returning clients, not later applicants; keeps the route issue 3 removes |

   * **Recommendation:** A, and in issue 3 option C (group by the client key), now confirmed for 61% of the pairs by
     the earlier-application link. **Decision:** A or B? (Issue 3's A, B or C stays open.)

   **Andrej (2026-11-11, discuss):** Mark the dataset to contain repeating entities. But we also can't just pretend
   this is a grouped split if its just 2.7 % of samples that are affected. Think about what would be the right custom
   split for this dataset, independent of our rules

   **Answer (AI, 2026-11-11):** a random split of applications in which a returning client's applications share a
   fold. It stays a random split (97% of the clients have one application) and is not tagged grouped.

   * Marked: the record already carries `Entities: Recur` (also in PR #50's copy); a CC line records your decision.
   * What a lender does: it scores every new application, returning clients included, and knows a returning client's
     earlier application and its payments (they already sit in the history columns for 61% of the pairs). It never
     knows the later application when scoring the earlier one.
   * The honest version, earlier application in training and later one tested, needs a single train/test cut. In the
     shipped 3x3 cross-validation every client split across folds trains on each application once, so the only way to
     close the backward route is one fold per client.
   * The other application's direction makes no difference under the random split: test rows whose client's later
     application is in training score like those whose earlier one is (ROC AUC 0.735 vs 0.735, application table).
   * Cost: 0.001 ROC AUC or less overall, 0.008 to 0.011 on the returning clients' rows. Keeping one application per
     client (option C) costs as little but drops 8,485 rows.
   * Slurm jobs 1377583 (application table, 5 seeds) and 1377584 (shipped 504 features, 3 seeds), LightGBM, 3 folds:

     | Split | Test rows whose client is in training | ROC AUC, application table | ROC AUC, 504 features | On returning clients' rows (504) |
     |---|---|---|---|---|
     | random (as shipped) | 3.7% | 0.7578 | 0.7865 | 0.7706 |
     | random, a client's applications in one fold | 0% | 0.7570 | 0.7857 | 0.7594 |
     | one application per client (latest), random | 0% | 0.7570 | 0.7864 | 0.7618 (later applications only) |

     The spread across seeds is 0.0002 to 0.001 overall.

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, with a note | as now, plus a note with the numbers above | no change | 3.7% of the test rows score with their own other application in training |
     | B | Random, a client's applications in one fold | the client key (sex and the two day differences) as split labels, not a feature; the split text says "random applications; a returning client's applications stay in one fold"; `ForcedIIDFromTemporal` stays | closes the route, keeps every row, still a random split of applications | uses the group mechanism for 8,004 clients; misses clients who renewed an ID or moved |
     | C | One application per client | keep each client's latest application (8,485 rows fewer), plain random split | simplest split; a returning client is still scored from their history | drops real rows and the earlier applications' labels |

   * **Recommendation:** B: the split stays what it is, a random split of applications, with the one constraint that
     removes the route at a cost of 0.001 ROC AUC. **Decision:** A, B or C? (It replaces issue 3's A, B or C.)

   **Notes for the AI:** on B, the edit of issue 3's option C without the `ForcedGroupedFromTemporal` tag: `client_key`
   in `_clean` before the features, declared as the split's group labels and kept out of the features; `split` and the
   `Time basis:` line's leak-test sentence say the returning clients stay in one fold; a curation note with the table;
   `dataset check`. On C, drop all but each key's most negative `DAYS_BIRTH` row in `_clean`, a note with the row
   count; `dataset check`. Scripts: `~/claude_jobs/marks_1111/home_credit_default_risk/custom_split.py`.

   **Andrej (2026-11-11, discuss):** In the actual task, it makes sense that the same client could apply twice. Hence,
   the ideal split would place a later application of a customer in test. Is that possible? If not, we go with random.

   **Answer (AI, 2026-11-11):** Yes. The order inside a client is exact, so each returning client's latest application
   can be tested with the earlier ones in training, at no cost to the score.

   * Order: `DAYS_BIRTH` counts back from each application, so the client's older (more negative) row is the later
     application; in 61% of the pairs the later one lists the earlier among its earlier Home Credit applications,
     decided that many days before. 568 latest rows are same-day ties, kept in one fold.
   * The split: each client's latest application (singletons included) goes into the random 3x3 folds; the 7,917
     earlier applications (2.6% of rows) sit in training in every fold and are never tested. A hand-built split
     (`_make_splits`); `dataset check` warns that these rows are never tested.
   * The earlier application helps the later one legitimately (0.006 ROC AUC on those rows), mostly when they are under
     180 days apart (0.010 vs 0.003); whether the earlier loan's label is known by then is unclear, since Home Credit
     does not say how many instalments it covers.
   * Slurm jobs 1378052 (application table, 5 seeds) and 1378053 (shipped 504 features, 3 seeds), LightGBM, 3 folds,
     ROC AUC:

     | Split | Test rows whose client is in training | All test rows (app / 504) | Returning clients' later applications (504) |
     |---|---|---|---|
     | random (as shipped) | 3.7% | 0.7578 / 0.7865 | 0.7643 |
     | later application tested, earlier ones in training | 2.5% | 0.7573 / 0.7862 | 0.7613 |
     | same folds, earlier applications dropped | 0% | 0.7570 / 0.7861 | 0.7556 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | as shipped | no change | half of the 3.7% train on the client's later application to test the earlier |
     | B | Later application tested | client key (sex and the two day differences) and `DAYS_BIRTH` order in `_make_splits`; earlier applications train only; split text "random clients' latest applications; earlier applications of a returning client only in training"; `ForcedIIDFromTemporal` stays | the task as a lender meets it; keeps every row | 2.6% of rows never tested; misses clients who renewed an ID or moved |
     | C | Random, a client's applications in one fold | the earlier answer's B | every row tested | drops the legitimate earlier-to-later route too |

   * **Recommendation:** B, the split you describe, and it is possible. **Decision:** A, B or C?

   **Notes for the AI:** on B, in `_clean` compute `client_key` (as issue 3's option C) and keep it out of the features;
   `_make_splits`: latest rows per key (max `-DAYS_BIRTH`, ties together) into 3 repeats of `StratifiedGroupKFold(3)`,
   the other rows appended to every train set; reword `split`, the `Time basis:` leak-test sentence and a curation note
   with the table; `dataset check` (accept the never-tested warning). Script:
   `~/claude_jobs/marks_1111/home_credit3/later_test.py`.

   **Andrej (2026-11-11, discuss):** Reply (B): Later application tested

   **Resolved (2026-11-11, Andrej):** B: `_make_splits` puts each client's latest application (most negative
   `DAYS_BIRTH` per client key of sex and the two day differences; one-application clients included, same-day ties in
   one fold) into stratified grouped 3x3 folds (299,590 rows) and adds the 7,917 earlier applications (2.6%) to every
   train side; the key is computed in the split, not a feature. `ForcedIIDFromTemporal` stays. `split`, `fit_reason`,
   the `Time basis:` leak-test sentence, a curation note with the table and a `splits_comment` are updated;
   `splits_rows_never_tested` is an accepted check warning with the reason. CC line in the record. Dataset check
   (Slurm job 1378120): 0 errors, 0 warnings (2 accepted); folds train 207,621 to 207,663, test 99,844 to 99,886 rows.

   **Andrej (2026-11-11, discuss):** Reply (B): Later application tested

   **Resolved (2026-11-11, Andrej):** B, now applied on this branch: `_make_splits` builds the client key (sex and
   the days between birth and ID issue and between birth and registration) inside the split, puts each client's
   latest application (most negative `DAYS_BIRTH`, same-day ties together, one-application clients included) into
   stratified grouped 3x3 folds and adds the earlier applications to every train side; the key is not a feature.
   `splits_comment`, `task_summary.split` and `fit_reason`, the `Time basis:` leak-test sentence and a curation
   bullet with the table say so, and `splits_rows_never_tested` is an accepted check warning with its reason.
   `dataset check` (Slurm job 1378328): 0 errors, 0 warnings (2 accepted), 2 info (the heavy duplicate checks
   skipped over the cell budget); the folds train 207,621 to 207,663 and test 99,844 to 99,886 rows, as on the
   branch the decision was taken on.

## Reference

Anna Montoya, inversion, KirillOdintsov, and Martin Kotek. Home Credit Default Risk. https://kaggle.com/competitions/home-credit-default-risk, 2018. Kaggle.
