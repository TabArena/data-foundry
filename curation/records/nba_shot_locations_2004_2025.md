---
unique_name: nba_shot_locations_2004_2025
name: NBA Shot Location Data 2004-2025 (all regular-season shots from NBA.com stats)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- No Good Target (yet)
tags:
- AI-Filled (Verify)
original_source: Github
year: '2022'
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://github.com/DomSamangy/NBA_Shots_04_25
- https://www.kaggle.com/datasets/mexwell/nba-shots
- https://www.nba.com/stats
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: every NBA regular-season field-goal attempt of 22 seasons from NBA.com's statistics, with location, shot type and game clock: the made-shot target of `nba_shots` at many times its size, and as there no decision is named for a shot-probability prediction.
- Source: Dom Samangy, GitHub `DomSamangy/NBA_Shots_04_25` (created 2022-11-06, last push 2025-06-09; the older name `NBA_Shots_04_24` resolves to it): "NBA regular season shot location data from the 03-04 season to 24-25", "Data Source: NBA.com", the files on Google Drive (link in the README), no licence. Kaggle mirror `mexwell/nba-shots` (2024, seasons 2004-2024, licence "other"). As published: one CSV per season (32-45 MB each on Kaggle) and one combined file, with the README's dictionary: season, team, player and game ids, `GAME_DATE`, `EVENT_TYPE` ("Made Shot // Missed Shot"), `SHOT_MADE` (the target), `ACTION_TYPE`, `SHOT_TYPE`, zones, `LOC_X`, `LOC_Y`, `SHOT_DISTANCE`, `QUARTER`, `MINS_LEFT`, `SECS_LEFT`. Rows not counted (about 200,000 attempts a season, so about 4.5 million, an estimate).
- Use case: none in the README ("Hoping it can help inspire some cool projects", shot charts). The analytics use is an expected-field-goal model that values shot selection or a defence (our reading), a measure more than a decision; fit approximate. Regime temporal by game date.
- Siblings and duplicates: `nba_shots` (`TBD -> 2nd Tier`, `No Good Target (yet)`; 128,069 shots of 2014-15 with tracking columns: closest defender, touch time, dribbles, shot clock) and `vinnie` (`No`, `Outdated`, `Trivial`) are the records this was found for. This release lacks the tracking columns, so it is no superset of `nba_shots`; both come from NBA.com, so weigh them as cuts of one source if both stay (PROV-6, PROV-7). External collections: none among the records.
- Better data: found as better data for `nba_shots` and `vinnie`; no further search this run.
- Papers and pages: the GitHub README; the Kaggle mirror; no paper.
- Metric: none found (README, Kaggle page); the fallback `roc_auc` (MET-8); inputs none.
- Risks for /add-dataset: `EVENT_TYPE` restates the target and goes; `ACTION_TYPE` (dunk, layup, jump shot) is coded with the play, so check that it is known before the outcome (USE-3); millions of rows, so a `_1m` cap and season windows; players and teams are known entities whose past shooting is legitimate history (USE-10); a Google Drive download without a licence (EV-4, noted only).
- Priority: gap 0 (binary, temporal not thin), use case 0 (none named), source 0 (an individual's pull of NBA.com data with a data dictionary), shape + (millions of attempts, coordinates, shot types, a time axis), risk 0: 2.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `nba_shots`, `vinnie`.
- as published: Every NBA regular-season field-goal attempt from 2003-04 to 2024-25, one CSV per season (22 files, 32-45 MB each unzipped), 26 columns (player, team, game date, action type, shot type, zone, x/y ...; target: SHOT_MADE (binary); access: open, open (Google Drive link in the GitHub README; Kaggle mirror, license 'other').
- Why: The same target as nba_shots (shot made, FGM) on the same units (NBA field-goal attempts) with features of the same kind (shot distance, period, clock). | vinnie is field goals made against attempts for one player (Vinnie Johnson, 1985-89, per game, from the New York Times); this is the same quantity measured per ...
- Adds: 22 seasons instead of part of one (128,069 shots of 2014-15), the shot location and action type. It lacks the 2014-15 tracking columns (closest defender distance, touch time, dribbles, shot clock), which the old record has. The record's marker 'No Good Target (yet)' still applies to the use case; both tables come ...
