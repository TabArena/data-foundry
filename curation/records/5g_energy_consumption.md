---
unique_name: 5g_energy_consumption
name: aiml-for-5g-energy-consumption-modelling
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Data Quality Issue
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Dated'
- 'Entities: Recur'
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: technology & internet
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/aiml-for-5g-energy-consumption-modelling
- https://huggingface.co/datasets/netop/5G-Network-Energy-Consumption
- https://challenge.aiforgood.itu.int/match/matchitem/83
- https://github.com/ITU-AI-ML-in-5G-Challenge/5G-Energy-Consumption-Modelling-Solution-Team-Farzi-Data-Scientists/tree/main
notebook_path: datasets/beyond_iid/grouped/5g_energy_consumption/5g_energy_consumption.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/5g_energy_consumption/dataset.py
source_row: 890
type_adapter_id: curation-record-v1
---

## Comments

Would require grouped-temporal split, but not possible due to data size

We could do a grouped split as a validation study, but this would not exactly correspond to the actual task

CC (2026-10-21, Lennart): the declared metric documents the original use case's metric; overrule it only when it is biased or wrong (evidence from the paper); keep the note of the original metric (TP-6 amended).

**Assessment (AI, 2026-10-21):** metric stays `mape`: the challenge ranked the private leaderboard by weighted MAPE, the weights (higher for new stations or configurations) given in its test file (Zindi evaluation page). Here every test station is new and the weights are not in the released data, so unweighted MAPE is the nearest listed metric. The notes now name WMAPE. Needs a rebuild to reach the container (notes only).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: stand_in mape — stands in for Weighted MAPE (WMAPE), Zindi private leaderboard: false: the per-row WMAPE weights come with the test file and are not published; every test station here is new, so unweighted mape is the closest stand-in (https://zindi.africa/competitions/aiml-for-5g-energy-consumption-modelling).

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): codes shipped as numbers, left for the curator's review: `weekday_number`.

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): weekday_number a category.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `cetin_ran_base_station_energy` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): marks on the review board of PR #37: weekday_number is a number again (a position in the week's continuous cycle, shipped as a number: the curator's cycle rule).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: hourly energy of 923 Huawei base stations over one week, split by station to fill measurement gaps (a direct fit decided 2026-10-14); only two missing record fields. Priority 3: gap 0, use case 1, source 1, shape 1, risk -1.

CC (2026-11-10, Andrej): time basis (review page issue 1): option B, grouped by station, named `Snapshot` of the logged week (1 to 8 January 2023): the use case fills in the hours of unmetered stations inside that week. The `Time basis: Snapshot:` bullet is in `curation_comments`; the tag enters `data_tags` once PR #50 is in the working copy. Split unchanged.

CC (2026-11-11, Andrej): record fields set from the definition (review page field mark): `year` 2023; `domain` technology & internet.

## Review

**Outcome:** added. Hourly energy use of 923 Huawei 5G base stations over one week of January 2023 (92,629
station-hours), predicted from the station's hardware, the hour's traffic load and its energy-saving settings; the data
of the ITU AI/ML in 5G Challenge on Zindi (2023). The AI recommends shipping it as defined. Reviewed on 2026-11-04
without a review panel, from the gathered evidence (the record and its earlier decisions; no model run exists for
it). Validity: the task fills the gap for stations without energy measurements in a week, from the stations that were
measured, a direct fit on your call of 2026-10-14; whole stations are held out, so no station has hours on both sides of
a split, and the shared hours are the use case (the other stations of the same week are measured). The challenge itself
aimed at new station products, which a split by product and time would test; one week of data does not allow it, as the
notes say. Value: the task-probe sweep of 2026-10-06 raised no flag. Quality: the energy unit is not stated (values
rescaled to a maximum of 100), which leaves the stations' relative energy intact; `mape` stands in for the challenge's
weighted MAPE, whose weights were never published (settled 2026-10-21). Weighed: a challenge with a named operator
decision +, a split that mirrors gap filling +, one week and an unknown unit -, a better-documented sibling found
(`cetin_ran_base_station_energy`, a peer-reviewed release of a Slovak operator's stations, screened `TBD -> Yes`) -.

**Main points:** The time basis is settled (issue 1, `Snapshot`, 2026-11-10). Record `year` and `domain` set from the
definition (2026-11-11). Nothing open.

**Record judgment:** valid. The record's `Data Quality Issue` marker has no stated reason, and the facts on file (an
unknown energy unit, one week of data) do not reach what the marker means for a `No` (a leak or damage that cannot be
repaired), so it reads as a watch flag and could come off. `cetin_ran_base_station_energy` is a different operator and
source, so it is a sibling task, not a replacement: a valid task stays when a better version exists elsewhere.

**Issues for Andrej:**

1. **Time basis: name the split by station a `Snapshot` of the one logged week?**

   * **Problem:**
     - Every row is one hour of a week already logged (1 to 8 January 2023), with the energy metered in the same hour as the load and settings, so the use case fills in the hours of unmetered stations inside that week rather than predicting a later one.
     - The record's collection facts fit (`Samples: Over Time`, `Time: Dated`, no target tag), and the split holds out whole stations, tagged `Non-IID` and `Grouped`, with no time basis.
     - Name the split a `Snapshot` of the week, or a forced split for the challenge's forward aim?
   * **Background:** a definition can name the use-case prototype it follows, with a `Time basis:` line that states
     the fact; filling in a period the data covers is a `Snapshot`, whose line names the period[^1t1]. Such a split
     also checks that no row of a test row's time carries its target. Here the other stations of the same hour share
     the network's load pattern, and day and hour are features; the use case has those stations, as they are the
     measured part of the same week (your call of 2026-10-14), so they are not future information. Grouping by hour
     would test a station-hour with no measured station in that hour, which is not the use case.
   * **Effect on the task:** none on rows, splits or scores; the tag and the line say what the score stands for and
     what it cannot test: a later week, or a station product before it runs, which the challenge aimed at and one
     week cannot test[^1t2].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Grouped by station, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Grouped by station, named `Snapshot` | `data_tags` gain `Snapshot`; a `Time basis:` line names the week and the fill-in | states the decided use case, gap filling; says why stations of the same hours sit in training | does not cover the challenge's forward aim |
     | C | Grouped by station, forced from temporal | `data_tags` gain `ForcedGroupedFromTemporal`; a note that a longer release would allow a split by station and week | matches the challenge's aim, new station products | contradicts the decided use case; the week is the whole period of the use case, not lost time |

   * **Recommendation:** B: the use case you decided fills in the logged week, which is what the prototype names.
     **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Snapshot",)` (the definition lists no tag now, so the
   automatic `Non-IID` and `Grouped` stay), and the curation bullet "- Time basis: Snapshot: one logged week of 923
   stations, 2023-01-01 01:00 to 2023-01-08 00:00, hourly; the energy is metered in the same hour as the load and
   energy-saving settings, and the use case fills in the hours of stations without meters in that week while the other
   stations of the same hours are measured (day and hour are features). Not tested: a later week, or a new station
   product before it runs, the challenge's aim."; `dataset check` (no date column ships, so no
   `meta_time_present_unused`). On C: `data_tags = ("ForcedGroupedFromTemporal",)` and the note. The record's facts
   stay as they are.

   [^1t1]: **SPLIT-32** (Should): how the data was collected is information for the split; a definition can name the
     use-case prototype it follows, with a `Time basis:` line stating the fact. A `Snapshot` only fills in a time the
     data covers (one census, one scrape, the gaps of a logged week); its line names the moment or the period, and no
     row of a test row's time may carry its target, else the split groups by that time unit. Cases: houses and
     5g_energy_consumption.
   [^1t2]: **SPLIT-8** (Must; reworded 2026-11-05): a forward use case whose release has lost its time or has too few
     periods ships in the closest regime, tagged as forced from temporal (`ForcedGroupedFromTemporal` when grouped).

   **Resolved (2026-11-10, Andrej):** B, grouped by station, named `Snapshot`: the `Time basis: Snapshot:` bullet is in
   `curation_comments` (the logged week, the fill-in, and what the split cannot test: a later week or a new station
   product). Split and rows unchanged. The tag `Snapshot` enters `data_tags` once PR #50 is in the working copy.
