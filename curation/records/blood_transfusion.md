---
unique_name: blood_transfusion
name: blood-transfusion-service-center / blood_transfusion
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: One Moment'
- 'Target: Later'
- Database Snapshot
original_source: UCI
year: '2008'
collection_period: Unknown
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://www.openml.org/search?type=data&id=1464
- https://doi.org/10.24432/C5GS39
notebook_path: datasets/beyond_iid/old_iid/blood_transfusion/blood_transfusion.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/blood_transfusion/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Nice task with time-invariant features to predict a future event, so already framed so it can be used with random splits. NNs outperform trees & linear performs similar to trees, so likely pretty simple task; known to make models overfit quickly

Potential issue: maybe trivial

Lennart: no objection

Andrej: Matches criteria

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The paper fits an RFMTC (Bernoulli sequence) model and compares predicted with actual response across donor groups and against plain RFM; no per-donor metric is named in what is accessible (full text paywalled). The ranking of donors to contact fits ROC AUC.

CC (2026-11-06, Andrej): time basis `DelayedTarget` accepted (Review issue 3, B, through the cross-dataset item on `DelayedTarget` issues of one-moment releases): 748 donors drawn at one moment before the March 2007 drive, the target whether each gave at that drive. The random split is IID here, as every row shares the moment and the outcome window, so no test row is later than a training row.

CC (2026-11-12, Andrej): no forced tag, the time basis is the `DelayedTarget` of the March 2007 drive (Review issue 1, A); `TotalBloodDonated` dropped (issue 2, B): it is 250 x `NumberOfDonations` on all 748 rows (250 cc per donation), a copy of the count; three features remain. The count most likely counts 250 ml units (noted in the definition).

CC (2026-11-16, Andrej): time basis `ForcedIIDFromTemporal` instead of `DelayedTarget`, which was dropped before it shipped:
- A shared scoring date with a target window closed for every row makes the random split valid within that date only; one date is one period, too few for three windows, so the split is forced (SPLIT-8).
- The random split stays.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk, cross-dataset item).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 4, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Use right after the moment counts for ASR, but behavioural response to a seasonal university drive moves, and similar behavioural sets measured not flat; mixed.

## Review

**Outcome:** added. The donor table of the Blood Transfusion Service Center in Hsin-Chu City, Taiwan (UCI 176): 748
donors drawn at random, their donation history and whether they gave blood in March 2007 (24% did); random splits,
ROC AUC (fallback). Reviewed on 2026-11-04 without a panel: the history is recorded before the March drive and nothing
gives the outcome away; methods separate (1 - ROC AUC 0.243 to 0.307), though a two-term model of purchase histories
ranks first. `TotalBloodDonated` was exactly 250 times `NumberOfDonations` on all rows: dropped (issue 2). The time
basis went from no tag over `DelayedTarget` (issues 1 and 3) to `ForcedIIDFromTemporal` (CC 2026-11-16); stationarity
reasoning of 2026-11-18: the forced tag stays (issue 4, A, Andrej).

**Main points:** Nothing open: no forced tag at first, the time basis `DelayedTarget` (issue 1, A, 2026-11-12; issue 3,
B, 2026-11-06), replaced by `ForcedIIDFromTemporal` on 2026-11-16; `TotalBloodDonated`, an exact multiple of the
donation count, is dropped, three features remain (issue 2, B, 2026-11-12); the forced tag stays, not
`AssumedStationaryRelation` (issue 4, A, 2026-11-18).

**Issues for Andrej:**

1. **Tag the split as forced from temporal, since one month's outcome stands in for a forecast?**

   * **Problem:**
     - All 748 donors are labelled by the same March 2007 drive, and the definition's `fit_reason` already says that a
       service would train on earlier drives and predict the next one.
     - The split rules ship such a single-extract table in the closest regime, IID, tagged as forced from temporal,
       with a note of what a dated release would change[^1a].
     - The definition carries no such tag; add it?
   * **Background:** the tag tells a benchmark user that the IID score stands in for a temporal task. A forced split
     ships only when no row shares its outcome with the other side through a hidden group or the row order; our
     experiments found no hidden group (OpenML row ids carry no label, ROC AUC 0.50-0.56 for neighbours by id) and the
     repeated rows behave as natural repeats.
   * **Effect on the task:** none on rows, splits or scores; the regime metadata changes.
   * **Consistency:** follows the churn snapshots of one month or one extract (mobile_churn, bank_customer_churn,
     churn_telco_south_asia, tour_travels_churn), which carry `ForcedIIDFromTemporal`.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | IID, no tag (implemented) | random splits as now | none found | departs from the rule and the churn snapshots |
     | B | IID, tagged forced | `data_tags` gain `ForcedIIDFromTemporal`; a note says a release with several drives would allow a temporal split | follows the rule; tells users what the score stands for | none found |

   * **Recommendation:** B: the definition itself describes a forecast from one extract. **Decision:** no tag (A) or
     forced from temporal (B)?

   **Notes for the AI:** on B, add `ForcedIIDFromTemporal` the way the churn definitions declare it (check how
   `mobile_churn/dataset.py` sets it, so the automatic regime tags stay), add a sentence to `fit_reason` or the notes
   ("a release with several drives would allow a temporal split"), `dataset check`.

   [^1a]: **SPLIT-8** (Must): a task temporal in nature or by its use case whose release cannot give the windows
     ships in the closest regime that keeps the rows, tagged as forced from temporal; this covers a release with no
     dates at all (one extract, the status at that moment standing in for a forecast).

   **Answer (AI, 2026-11-06):** Since a release of one moment is no longer forced, close this issue on A and decide the
   tag in issue 3 (a), or keep the forced tag (b)?

   * **Problem:**
     - All 748 donors share one extract and one later outcome, the March 2007 drive, so no donor's row lies after another's and no period is mixed.
     - Since 2026-11-05 the split rules give a release of one moment a use-case prototype instead of the forced tag, and they cite this dataset's March 2007 drive as such a case[^1ta].
     - Issue 3 asks for the prototype that replaces B here; close this issue on A?
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | No forced tag; the time basis in issue 3 | this issue closes on A; issue 3 names the prototype | follows the amended rule; one decision per tag | none found |
     | b | Forced from temporal, as recommended before | B as written | marks the stand-in for a forecast | the amended rule keeps the forced tag for lost time and too few periods |

   * **Recommendation:** a. **Decision:** a or b?

   [^1ta]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`. **SPLIT-32** (Should): `Samples: One
     Moment` with the target at one shared later date is IID data, such as the March 2007 drive of blood_transfusion.

   **Andrej (2026-11-12, discuss):** Reply (a): No forced tag; the time basis in issue 3

   **Resolved (2026-11-12, Andrej):** A (answer a): no forced tag; the time basis is issue 3's `DelayedTarget`. Nothing
   changed in the definition. The time basis became `ForcedIIDFromTemporal` on 2026-11-16 (see issue 3).

2. **Drop `TotalBloodDonated`, which is exactly 250 times `NumberOfDonations`?**

   * **Problem:**
     - Each donation is 250 cc, so the volume column is the donation count times 250 on every one of the 748 rows
       (checked) and adds no information.
     - The cleaning rules drop exact copies of another column; a column leaves for being a copy, never for the number
       of columns[^2a].
     - Drop it, or keep the source's four columns?
   * **Background:** the source's RFM table lists recency, frequency, monetary value and time; here the "monetary"
     column is the frequency in another unit.
   * **Effect on the task:** a method that weighs a duplicated column twice sees the count twice; in model
     runs one method's lead depended on the copy being present, which is a property of the table, not of the donors.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | four features as UCI ships them | the source's columns | a copy of another column |
     | B | Drop | `TotalBloodDonated` dropped; three features | follows the copy rule; no information lost | departs from the published layout |

   * **Recommendation:** B: the column is the count in cc, nothing else. **Decision:** keep (A) or drop (B)?

   **Notes for the AI:** on B, drop `TotalBloodDonated` in `_clean` with a comment ("250 cc per donation: 250 x
   NumberOfDonations on all rows"), a curation note, and `known` in the task summary ("the number of donations");
   `dataset check`.

   [^2a]: **CLEAN-5** (Should): drop constant columns, all-missing columns and exact copies of another column.
     **CLEAN-22** (Must): columns leave for what they are (a leak, an identifier, a copy), never for how many there are.

   **Andrej (2026-11-05, discuss):** How can the total blood donated always be 250 times the number of doantions,
   meaning that 250 donations are made each time? Sounds unrealistic to me

   **Answer (AI, 2026-11-05):**

   * **Your question:** how can the volume always be 250 times the number of donations?
   * **Found:**
     - The factor is 250 cc per donation, not 250 donations. UCI describes the column as "M (Monetary - total blood
       donated in c.c.)", and in Taiwan whole blood is collected in 250 ml bags (one unit) or 500 ml (two units)
       (Taiwan FDA donor guidance, Taipei Times, 2017-11-02,
       https://taipeitimes.com/News/taiwan/archives/2017/11/02/2003681508).
     - So the column was computed from the count at one bag per donation (`TotalBloodDonated` = 250 x
       `NumberOfDonations` on all 748 rows). It was not measured, and a donor who gave 500 ml would make it wrong.
     - The count itself does not read as visits of one bag each. 34 donors have 2 to 5 donations in the month of
       their first donation (31 of them 2), and 51 of the 590 repeat donors have more donations than a gap of two
       months allows. Two months is the shortest wait after a 250 ml donation, three after 500 ml. The most likely
       reading is that the count is of 250 ml units, so a 500 ml donation counts twice; the source does not say.
       These 51 donors give blood in March 2007 at the same rate as the others (27% against 27%).
     - Neither changes the task: the count is still the donor's history as the service records it, and the volume
       adds nothing to it.
   * **Recommendation:** unchanged, B: drop `TotalBloodDonated`, the count in cc. If dropped, the curation note says
     the count most likely counts 250 ml units. **Decision:** keep (A) or drop (B)?

   **Notes for the AI:** checks on the UCI file (`transfusion.data`): `M == 250 * F` on all rows; rows with
   `T == R` and `F > 1`: 34; repeat donors with `F > (T - R) // 2 + 1`: 51 of 590 (132 for a three-month gap).

   **Resolved (2026-11-12, Andrej):** B: `TotalBloodDonated` dropped in `_clean` (with an assert that it is 250 x
   `NumberOfDonations` on every row), three features; a curation note says the count most likely counts 250 ml units
   (34 donors with 2 to 5 donations in their first month, 51 of 590 repeat donors above the two-month gap); `known` in
   the task summary now names the number of donations, and `fit_reason` says three history counts; record CC line.
   `dataset check` re-run.

3. **Time basis: name the random split a `DelayedTarget`, one draw of donors scored for the March 2007 drive?**

   * **Problem:**
     - All 748 donors were drawn at one moment before the March 2007 drive, with their history counted to one shared reference date, and the target is whether each gave at that one drive, so every donor shares the prediction moment and the target comes after it.
     - The record's collection facts fit (`Samples: One Moment`, `Target: Later`), and the random split carries no time basis.
     - Name it a `DelayedTarget`, with the line below?
   * **Background:** a delayed target needs its window closed for every row and every feature in existence at the
     moment[^3t1]. Both hold: the drive is past for every donor, and no history count includes it (the 5 donors
     whose last donation is 0 months back gave in March at 40%, like those at 2 to 4 months at 38%, not at 100%). What
     the split cannot test is the next drive, as training and test donors share the March 2007 response level; the
     definition's `fit_reason` already says so.
   * **Effect on the task:** none on rows, splits or scores.
   * **Unknown:** the reference date of the counts (just before the drive, or earlier) is not stated on the UCI page;
     the paper is paywalled.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `DelayedTarget` | `data_tags` gain `DelayedTarget`; a `Time basis:` line names the extract and the drive | states one moment and one drive; the amended rule cites this drive | none found |
     | C | Random, forced from temporal (issue 1's B) | `data_tags` gain `ForcedIIDFromTemporal` | marks the stand-in for a forecast | the amended rule keeps the forced tag for lost time and too few periods[^3t2] |

   * **Recommendation:** B. **Decision:** A, B or C?

   **Notes for the AI:** on B: `data_tags = ("DelayedTarget",)` (no tag is listed now, so the
   automatic `IID` stays) and the curation bullet "- Time basis: DelayedTarget: one random draw of 748 donors from the
   donor database before the March 2007 drive, with months since the last and the first donation and the number of
   donations counted to one shared reference date; the target is whether the donor gave at the March 2007 drive, one
   date closed for every donor, and no history count includes it (donors with recency 0 give at 40%, as at 2 to 4
   months). Not tested: the next drive."; `dataset check`. Issue 1 then closes on A. The record's facts stay.

   [^3t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. A `DelayedTarget` has one prediction moment for all rows and the target after it; its line
     names the moment and the window, the window has closed for every row, and every feature existed at the moment.
     **LEAK-10** (Must): a feature holds only what existed at the prediction point.
   [^3t2]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment is not forced; SPLIT-32 gives it
     `Snapshot` or `DelayedTarget`.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the `DelayedTarget` issues of
   one-moment releases with one mark?" The `Time basis: DelayedTarget:` bullet is in `curation_comments`; it says why
   the random split is IID here (every row shares the moment and the outcome window, so no test row is later than a
   training row) and ends with what the split cannot test (the next drive). The split and `data_tags` are unchanged; the
   tag `DelayedTarget` was to enter `data_tags` with the time-basis tags. Issue 1 (the forced tag) stays open for its
   own mark.

   **Later (2026-11-16, Andrej):** `DelayedTarget` was retired before it shipped; one drive is one period, too few for
   three windows, so the time basis is `ForcedIIDFromTemporal` with the random split unchanged (CC 2026-11-16; kept in
   issue 4).

4. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: One moment: one draw of 748 donors before the March 2007 drive, history counted to one reference date; no earlier or later drive in the release.
     - Use: The service picks donors to contact before the next drive, about three months after the data.
     - Mechanism: Recency, frequency and tenure to turning up at a university bus drive: donor behaviour, which moves with the academic calendar, campaigns and drive timing.
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | online_shoppers_purchasing_intention_dataset | v3 stationary-relation test by month | not flat | RFM-style behavioural response |
     | mobile_churn (splits.md Cases) | trained on June, tested on later joiners | not flat: ROC AUC 0.661 vs 0.690 IID | one-moment behavioural customer base |

   * **For a stationary use case:**
     - use right after the collected moment (next drive, ~3 months)
     - the RFM relation is a long-known regularity.
   * **Against:**
     - behaviour, not physiology: response depends on campaigns and calendar.
     - the bus collects at a university: a summer drive meets students away.
     - one drive is one period: nothing measured.
     - similar behavioural sets test not flat.
   * **Earlier views:**
     - CC 2026-11-16 (Andrej): ForcedIIDFromTemporal instead of DelayedTarget; one drive is one period.
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | behaviour, not physiology: response depends on campaigns and calendar; the bus collects at a university: a summer drive meets students away |

   * **Recommendation:** A, use right after the moment counts for ASR, but behavioural response to a seasonal university drive moves, and similar behavioural sets measured not flat; mixed. Confidence: medium. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Use right after the moment counts for ASR, but behavioural response to a seasonal university drive moves, and similar behavioural sets measured not flat; mixed.)

## Reference

Yeh, I-Cheng, Yang, King-Jang, and Ting, Tao-Ming, "Knowledge discovery on RFM model using Bernoulli sequence", Expert Systems with Applications, 2008.
