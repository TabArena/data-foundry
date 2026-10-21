# rain_in_australia

**Outcome:** added. Verdict: ship (not built yet). Will more than 1 mm of rain fall at a location by 9 am tomorrow,
predicted at 9 am from that morning's observations and the day before's later readings, on rattle's full weatherAUS
file (2007-2026, 49 locations of the Bureau of Meteorology, BoM); nine 14-day test windows, one every six weeks. The
panel's changes are in `dataset.py`; the cleaning fixes change the data. Validity: no input is read after 9 am
(LEAK-10 holds after the ten later columns are replaced by the day before's); the forecasting-scope test passes its
first leg on the shipped windows (SEL-11, TP-10 leg 1: the model clearly beats each location's naive forecast);
whether its second leg (no lagged target) needs an amendment is open (issue 4); the fit is approximate, since a
forecaster also has weather-model output (USE-8). Value: not trivial (ROC AUC 0.847 against 0.661 for yesterday's
rain and 0.672 for the location's monthly rain rate). Quality: a calm wind's blank direction set to "Calm", and the
impossible relative humidity of 0% set to missing (CLEAN-10, CLEAN-11). Weighed: size, real sensors and no similar
dataset, against the approximate fit. Left for the curator: issues 4, 5, 2, 3 and 6.

**Main points:** Amend TP-10 leg 2 so the 9 am rain reading can stay (issue 4)? Confirm the dropped rows (issue 5)?
Accept 14-day windows spaced six weeks apart (issue 2)? Confirm the rattle file as the source (issue 3). Add other
locations' morning observations (issue 6)?

**Record fields that disagree with the definition:**

- `year`: record `2017`, definition `2026`.

**Record judgment:** valid. rattle's weatherAUS, compiled from the Bureau of Meteorology's Daily Weather
Observations; the Kaggle upload the record names is a 2017 snapshot of it (the rattle and BoM links are in
`source_links`).

**Issues for Lennart:**

4. **TP-10 leg 2: may the 9 am rain reading, which is yesterday's label, stay as a feature?** TP-10 (Must) admits a
   panel that looks like forecasting (one series per location) only if a model clearly beats each location's naive
   forecast (leg 1) and "the source's top solutions used no lagged target" (leg 2). Here the label is rain from 9 am
   today to 9 am tomorrow, and `Rainfall`/`RainToday` are the gauge reading of 9 am today, i.e. the label of the day
   before (a lagged target). The source has no competition and so no top solutions; the public Kaggle notebooks use
   RainToday. The g_research review (2026-10-20) reads leg 2 strictly: features that are the lagged target fail it.
   Effect: on the 9 shipped windows LightGBM reaches ROC AUC 0.8495 with the two columns and 0.8467 without (paired
   SE 0.0013, better in 7 of 9 windows; log loss 0.3516 against 0.3549), so the skill does not come from the lagged
   target. Leg 1 holds: all features 0.847 against 0.661 for persistence (tomorrow as today), 0.672 for the location's
   monthly rain rate and 0.743 for the location's own rain series with the calendar, ahead in 9 of 9 windows.
   Precedent: follows ashrae_great_energy_predictor_iii and bias_correction (TP-10 tested on the shipped windows);
   departs from g_research_crypto_forecasting, where lagged sums of the target carry the signal and leg 1 fails. The
   counter-case el_nino_dataset predates TP-10, and its source's goal was a two-year forecast of the series.
   Implemented: both columns kept and the measured fact written into the notes (USE-6, Must: a known 9 am input
   stays; LEAK-34). The critic, and the mediator with it: LEAK-37 (P4) shows the reading is no leak, but a P4 rule
   cannot clear a P2 test; only the measured lack of skill can. Alternatives: keep the wording of leg 2 and confirm the recorded fact for this
   dataset only; or read leg 2 strictly and drop both columns (costs 0.003 AUC and departs from USE-6). The
   cross-dataset item "Amend TP-10 to keep g_research_crypto_forecasting?" (Rules from the G-Research review)
   proposes another leg 2, "no lag of the target column itself"; under it RainToday, the label of the day before,
   fails, so the two amendments are decided together. g_research fails leg 1 under either wording. Recommendation: amend leg 2 to "the skill does not come
   from the lagged target, measured by dropping it on the shipped windows", so every dataset without a competition is
   read the same way. Decision needed: amend leg 2, confirm for this dataset only, or drop the two columns.

5. **Drop the 2,571 rows without their own 9 am rain reading and the 201 rows whose next row is far later?** After a
   missing reading BoM's next value can be "accumulated over several days rather than the normal one day", so the
   label of such a row can cover 48 hours or more (42.6% rain days against 21.8%). rattle takes the label from the
   location's next row in the file, which before the periods missing from the file is 29-401 days later (201 rows,
   184 of them labelled). Effect: kept, they would score the model on a label of two days or more, not the 24-hour
   call of the task. Implemented: both kinds dropped, the far-next-row rows first; with the 8,076 rows without a
   label, 264,562 of 275,410 rows remain (LEAK-26 by analogy, a label that covers a different window than the task's,
   and PROV-13, repair the damage the source left; both Must). Precedent: follows bias_correction (2026-10-15).
   Alternative: keep the rows without their own reading, and the model learns a missing reading as a rain signal.
   Recommendation: keep the drops. Decision needed: confirm.

2. **Test windows of 14 days spaced six weeks apart?** SPLIT-15 (Should) rolls the windows back from the newest
   data, one after the other; this is the first dataset in the copy whose step between windows (42 days) is larger
   than the window (14 days). The 14 days follow your horizon for weather ("one or two weeks at most", on
   climate_model_weather_forecasting; SPLIT-18). Effect: the nine windows, 2025-02-15 to 2026-01-30, cover every
   season of the last year (622-642 rows and 63-205 rain days each, train at least 94%); contiguous 14-day windows
   would cover only September to January. Window sizes were chosen from row counts, not scores (SPLIT-21). The panel
   did not dispute it. Implemented: `TemporalSplits(window=14, unit="days", n_windows=9, step=42)`. Alternatives:
   contiguous 14-day windows (test only September to January, so SPLIT-20's season check fails), or monthly windows
   (May 2025 to January 2026, 1,333-1,417 rows; longer than SPLIT-18's one to two weeks). Recommendation: accept the
   spacing as an exception to SPLIT-15 with the stated reason (SPLIT-20), to become a Cases row of SPLIT-20. Decision needed: accept the spacing, or choose contiguous or monthly windows.

3. **Source: rattle's full file (2007-2026), not the Kaggle snapshot?** The Kaggle upload ends on 2017-06-25 and is a
   later re-upload of rattle's file (an earlier count; the panel had no Kaggle file to retest it, nor the 2017-06-25
   end date); rattle's file runs to 2026-01-30 but lacks 2016-01-27 to 2017-02-28, which the
   snapshot holds. The two versions differ in 0.9% of the rows both hold (same
   earlier count), so patching the gap from Kaggle would be
   our own rebuild (PROV-14, Must). Implemented: rattle's file, pinned by an Internet Archive capture and the CRAN
   rattle 5.6.2 package, which holds the same 275,410 x 24 values. Precedent: follows consumer_complaints,
   hr_analytics and loan_ibrd (the full original over an older upload; PROV-8). Alternative: the Kaggle snapshot
   (ten years, no 2017-2026). Recommendation: keep rattle's file. Decision needed: confirm.

6. **Add other locations' observations of the same morning?** A forecaster reads the weather upwind: rain, pressure
   and humidity at other locations at 9 am. The file holds them (same date, other location). The domain practitioner
   added every location's 9 am Rainfall, Pressure9am and Humidity9am to each row: ROC AUC rises from 0.850 to 0.873
   on the shipped windows (better in 7 of 9). Against it: it changes the table as published (each location-day row
   gains 147 columns, three 9 am readings of every location), and Perth's 9 am reading is taken at 11:00-11:30
   eastern time, after an eastern row's prediction point, so each row may use only locations whose 9 am is not later
   than its own (USE-3). It is no defect of the shipped task
   (USE-1, a weighing call). Implemented: not added. Recommendation: leave it out; the task stays the published one.
   Decision needed: add the neighbour features or not.

**Review panel:** ship after changes (mediator). Claim audit: 51 claims; "49 stations" (a location can combine
several stations) refuted (fixed), the task summary's changes and the record's links refuted (fixed; the record's year
is the field row above), the Kaggle snapshot facts untested. Blind review: would include with changes; main concern the source link (Kaggle against the
rattle file). Debate: agreed on the leak checks, the split, the source, the approximate fit and the cleaning fixes;
disputed: what TP-10 leg 2 needs (issue 4) and whether a blank Cloud9am is a potential leak (settled by the mediator's
test: mostly a clear sky at 9 am, a plain anomaly note). The mediator numbers the
issues 1-5; they are this file's issues 4, 2, 3, 5 and 6.

<details><summary>Claim audit</summary>

Tests: raw, cleaned and split checks; rattle against the BoM DWO pages of January 2026 at 7 locations; LightGBM
ablations on the 9 shipped splits; the CRAN rattle 5.6.2 RData against the CSV; the breakdown of the dropped rows.
Licence and pretraining overlap were not used as evidence.

**Table**

| # | claim (short) | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | > 1 mm in next 24 h | task_summary | RainTomorrow vs RISK_MM; RISK_MM == 1 rows | holds | 100% RainTomorrow == RISK_MM > 1; all 3,249 rows with exactly 1.0 mm are No | USE-5 |
| 2 | actor: farmer / local forecaster at 9 am | task_summary | none possible on data | untested (judgment) | inputs are all known at 9 am (see 5) | USE-1 |
| 3 | 49 BoM stations, 2007-11 to 2026-01, 264,562 rows | task_summary | count; BoM DWO headers | numbers hold; "station" refuted (wording) | 264,562 rows, 49 Locations, 2007-11-01..2026-01-30. A Location is a BoM DWO *location page* that combines 1-4 stations: Sydney 3 (066214 rain/temp, 066037 cloud/pressure/sunshine, 066022 wind), Perth 4, Brisbane 2, Hobart 2. Sunshine is identical on 100% of shared days for Perth/PerthAirport, Sydney/SydneyAirport, Melbourne/MelbourneAirport | PROV (writing) |
| 4 | 22% rain days | task_summary | mean of label | holds | 21.84% | - |
| 5 | known at 9 am | task_summary | BoM DWO Jan 2026 cell compare at 7 locations; AUC to RainToday vs label | holds | rattle row D = BoM date D for every column (19 cols, 100% at Sydney, Canberra, Perth, Brisbane, Darwin; shift by one day matches 0-23%); RECORDED windows consistent with AUC pattern (MinTemp, Evaporation, Humidity9am tied to RainToday; Sunshine, gust, 3 pm tied to label) | LEAK-1, SPLIT-9 |
| 6 | 9 windows of 14 days every 6 weeks, Feb 2025-Jan 2026, newest first, train all earlier | task_summary | rebuilt splits | holds | windows 2026-01-17..30 back to 2025-02-15..28, each train ends the day before, starts 2007-11-01 | SPLIT-4 |
| 7 | changes: ten columns lagged, RISK_MM dropped, next-row-gap rows dropped | task_summary | diff raw vs clean; drop breakdown | holds but incomplete | does all three, but also drops 8,093 unlabelled rows and 2,571 rows whose own 9 am reading is missing (10,848 total) without saying so here (curation_comments do say it) | writing |
| 8-9 | fit direct; every input read by 9 am | task_summary | ablation; leak variant | holds | shipped 0.849 mean AUC; adding the 8 same-day after-9 am values gives 0.902 (+0.053): the lag removes a real leak; no remaining column is after 9 am | USE-1, LEAK-1 |
| 10 | source GOV Website, BoM DWO | class | BoM DWO fetch | holds | DWO pages reachable (Dec 2025-Feb 2026), match rattle; DWO keeps only ~14 months online, so the rows before late 2024 exist only in rattle | PROV-8 |
| 11 | year 2026 | class | PROV-9 (growing source takes the pinned snapshot's year) | holds | snapshot last modified 2026-02-07; rattle 5.6.2 packaged 2026-02-08 | PROV-9 |
| 12 | domain, Spatial | class | definitions.md | holds | Location is a geographic place | - |
| 13 | licence text | class | - | untested (licence is never evidence) | rattle Rd quotes BoM permission email of 17 Dec 2008 | - |
| 14 | Kaggle is a snapshot ending 2017-06-25 | download_description | no Kaggle file locally | untested | - | PROV |
| 15 | archive capture byte-identical, sha256 | download_description | re-downloaded archive URL, sha256 | holds | both 6598e685...549fc | PROV-10 |
| 16 | CRAN 5.6.2 sha and same 275,410 x 24 values | download_description | downloaded tarball, sha256, pyreadr cell compare | holds | sha 8b226e45...2fd; 0 differing cells | PROV |
| 17 | bibtex DOI | bibtex | doi.org resolve | holds | 302 to link.springer.com/10.1007/978-1-4419-9890-3 | - |
| 18 | target, binary, roc_auc | class/README | README front matter | holds | - | - |
| 19 | 49 stations 2007-11-01..2026-01-30 | curation_comments | as 3 | holds (numbers); "stations" as in 3 | | |
| 20 | prediction point 9 am D, inputs to 9 am D and D-1 | curation_comments | as 5 | holds | | LEAK-1 |
| 21 | ten after-9 am columns; five tied closer to label (Sunshine 0.805 vs 0.733) | curation_comments | AUCs on raw | holds | label vs RainToday: Sunshine .805/.733, WindGustSpeed .650/.597, Humidity3pm .802/.767, Pressure3pm .642/.558, Cloud3pm .746/.670 (five); note Pressure9am .659/.615 and Cloud9am .696/.689 also lean to the label although they are known at 9 am, so the AUC ordering is not itself the reason; the BoM timing is | LEAK-1 |
| 22 | RainTomorrow = RISK_MM > 1 in every labelled row | curation_comments | equality | holds | 100%, 0 NaN RISK_MM among labelled | - |
| 23 | next row 29-401 days later before gaps; dropped | curation_comments | gap computation | holds | 184 labelled rows across gaps, 29-401 days, RISK_MM == next row Rainfall in 184/184; consecutive rows: RISK_MM == next Rainfall 100% | USE-5 |
| 24 | last row keeps label; matches BoM next day at 15 stations | curation_comments | BoM Jan 2026 at 7 locations | holds at 7/7 checked; partly untested | 46 Locations end 2026-01-30 (7 checked match BoM 01-31, e.g. Darwin 23.8 mm Yes); 3 end earlier (Adelaide 2020-07-30, Newcastle 2021-04-15, Katherine 2024-11-29) and keep a label whose source cannot be checked (DWO no longer online) | USE-5 |
| 25 | drop unlabelled and missing-9 am-reading rows | curation_comments | counts | holds | 8,093 + 2,571 (4 more overlap with gap rows) | |
| 26 | RainToday = Rainfall > 1 everywhere | curation_comments | equality | holds | 100% | |
| 27 | dtypes | curation_comments | dtypes of frame | holds | Location, WindDir9am, RainToday, 2 prev-day dirs categorical; Date datetime | CLEAN |
| 28 | temporal, not grouped; same stations later | curation_comments | unseen stations per test | holds | 0 unseen stations in all 9 windows; probe: Location test rows seen in train 100% | SPLIT-3 |
| 29 | no rows 2011-04, 2012-12, 2013-02, 2016-01-27..2017-02-28 | curation_comments | months/days present | holds | exactly those months; 399 days 2016-01-27..2017-02-28 | |
| 30 | Cloud 9 in 3 rows | curation_comments | count | holds | Cloud9am 2, Cloud3pm 1 | |
| 31 | Sunshine/Evap missing 34-46% (2009-13) to 66-79% (2017-25) | curation_comments | yearly missing share | holds | Sunshine .37-.46 / .74-.79, Evaporation .34-.39 / .66-.76 (2026: .87/.89) | |
| 32 | Cloud9am missing more on dry mornings | curation_comments | missing by RainToday | holds | 47.1% (No) vs 36.9% (Yes) | LEAK (MNAR, known at 9 am) |
| 33 | BoM terms note | curation_comments | - | untested (licence) | | |
| 34 | 1-2 week horizon set by curators for climate_model_weather_forecasting | splits_comment | record grep | holds | record line 37 (Lennart's comment) | SPLIT-4 |
| 35 | windows 2025-02-15..2026-01-30, train from 2007-11-01 | splits_comment | rebuilt splits | holds | | |
| 36 | 622-642 rows, 46 stations, 63-205 rain days | splits_comment | rebuilt splits | holds | 622-642, 46, 63-205 | TP |
| 37 | 3 x 3 splits of the protocol for this size | splits_comment | splits.py REPEATS_BY_TRAIN_SIZE | holds | n_train = 2/3 x 264,562 = 176k < 250k -> 3 repeats x 3 folds | |
| 38 | decision 1 | _decisions | as 21 | holds | | LEAK-1 |
| 39 | 184 rows = 46+45+44+9+40 | _decisions | gap rows by date | holds | 2011-03-31: 46, 2012-11-30: 45, 2013-01-31: 44, 2016-01-25: 9, 2016-01-26: 40 | |
| 40 | 2,575 rows; 42.6% vs 21.8%; median 0.4 vs 0.0 | _decisions | recompute | holds | 2,575; 42.56% vs 21.84%; 0.4 vs 0.0 | USE-5 |
| 41 | alternative window options | _decisions | not rerun (output of the same function) | holds by construction | | |
| 42 | Andrej's screening comment | record | - | opinion | | |
| 43 | front matter: year 2017, source_links Kaggle only | record | PROV-9, definition | refuted | year: a growing source takes the pinned snapshot's year (2026), and Kaggle is not the first publication (rattle had weatherAUS since at least 2008-12, Rd permission date, NEWS); source_links lacks rattle/BoM | PROV-9, PROV-8 |
| 44-46 | assessment facts | record | as 10, 22-23, 21 | hold | | |
| 47 | LightGBM 0.846 vs 0.900 as published | record | LightGBM 9 shipped splits | holds (reproduced) | 0.849 shipped vs 0.902 with same-day columns | |
| 48 | priority 2 weighing | record | - | opinion | | |
| 49 | Kaggle file 145,460 rows; 1,135 of 125,900 rows differ | the previous REVIEW.md | no Kaggle file in the warehouse | untested | | PROV |
| 50 | 0.856 / 0.855 / 0.732 / 0.650 (monthly windows, first version) | the previous REVIEW.md | same ablation on the shipped splits | holds in direction (exact numbers untested) | 0.849 / 0.847 / 0.749 (station rain lags 0-3, station, calendar) / 0.670 (station, calendar) | SEL-10/11 |
| 51 | climate_model_weather_forecasting and bias_correction are Yes | the previous REVIEW.md | record grep | holds | suggestion 'Yes' in both records | precedent |

**Implied claims attacked**

| implied claim | test | result | evidence |
|---|---|---|---|
| every feature known at the prediction point | BoM timing + cell compare at 7 locations | holds | see 5, 8 |
| rattle data equals BoM | Jan 2026 cell compare, 7 locations | holds except cloud | 17 of 19 columns 100% (Rainfall and WindDir9am 29/30 at two places); Cloud9am/Cloud3pm differ: Melbourne rattle has 20 Cloud9am values where BoM now shows none, Hobart rattle has none where BoM shows 21. A revision or source difference; the shipped values are rattle's |
| no row is a copy across the split | probe exact copies 0.0%; same-day shared station values | holds | paired Locations share Sunshine (100%) and partly Rainfall (58-72%) on the same date, but a date is never on both sides of a split |
| the target is the real-world target | label = BoM's next 9 am reading > 1 mm | holds | 100% match on consecutive rows and at BoM |
| no train row has a label unknown at refit | last train day = T-1, its label is the reading at 9 am on T | holds | SPLIT-9 |
| features after a missing reading are one-day values | rows whose previous reading is missing | departs, kept | 2,648 kept rows have a Rainfall/RainToday that may cover several days (BoM accumulation). Feature quality only; label unaffected |

**Refuted, ranked**

1. **Record front matter (43), PROV-9 / PROV-8, Must (P5).** `year: 2017` and Kaggle-only `source_links` contradict
   the definition and PROV-9. Changes: the record, not the data. Remedy: on the curator's settlement of REVIEW issue 3,
   set the record's year to 2026 and add the rattle URL and BoM DWO to source_links.
2. **"49 stations" (3, 19), P5 wording.** A Location is a BoM location page combining up to 4 stations (Sydney 3,
   Perth 4); paired Locations share Sunshine. Changes nothing in the split. Remedy: write "49 locations (BoM DWO
   pages, some combining several stations)".
3. **task_summary.changes (7), writing.** Omits the 2,571 + 8,093 dropped rows. Remedy: add "and the rows without a
   label or without their own 9 am rain reading".

Findings, not refutations: Cloud9am/Cloud3pm in rattle differ from current BoM at Melbourne and Hobart (P5, Weigh:
keep with an anomaly note); 2,648 kept rows carry a possibly multi-day Rainfall (P7: note).

**Untested, ranked**

1. 24 for the 3 Locations that end early (Adelaide, Newcastle, Katherine): label source unverifiable (DWO offline);
   their 3 rows are in train only. Remedy: none needed or drop those 3 last rows.
2. 14, 49: the Kaggle snapshot facts (no Kaggle file in the warehouse).
3. 50 exact numbers (first version); direction reproduced.
4. 2 (actor), 13, 33 (licence, never evidence).

</details>

<details><summary>Column audit</summary>

Frame: the definition's cleaned frame (`dataset_io.from_definition`), 264,562 rows x 23 columns (21 features, target,
Date). Prediction point (first `curation_comments` bullet): 9 am on day D at a station; label = rain > 1 mm from
9 am D to 9 am D+1. Meanings from the BoM DWO notes (IDCJDW0000) as quoted in `dataset.py` (`RECORDED`); the BoM
page returned 403 in this run, so no new quotes.

**Column table**

| column | meaning | known at 9 am D? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| Date | observation day D | yes | datetime64; 6,174 days, no NA | fine (also the temporal split column) | SPLIT-1, CLEAN-14 |
| Location | BoM station (49) | yes | category, no NA | fine; known entity under a temporal split | LEAK-34, USE-10 |
| MinTemp | min temp, 24 h to 9 am D | yes | float; -8.7..33.9; 11 rows MinTemp > Temp9am (impossible by definition, tiny) | fine (note) | CLEAN-11 |
| Rainfall | rain mm, 24 h to 9 am D | yes | float; 0..474 (Cairns 2018-12-31, real); NA rows dropped. 2,648 rows (1.0%) follow a missing D-1 reading or row, where BoM may accumulate several days: RainToday 40.6% vs 21.8%, median 0.4 vs 0.0 mm | cleaning note: multi-day totals in the feature, undocumented | CLEAN-1, CLEAN-21 |
| Evaporation | Class A pan, 24 h to 9 am D | yes | float; 57% NA (16 stations never); max 138.7, 272 rows > 30 mm (multi-day totals, noted) | fine (noted) | CLEAN-11 |
| WindDir9am | wind direction at 9 am | yes | category, 16 points; 7.5% NA, of which 15,003 rows have WindSpeed9am = 0: calm, not unknown (raw: every speed-0 row has NA direction) | cleaning problem: NA means "Calm" | CLEAN-10, CLEAN-14 |
| WindSpeed9am | km/h at 9 am | yes | float; 0..87; 0 = calm | fine | |
| Humidity9am | RH % at 9 am | yes | float; 0..100; 1 row = 0 (Woomera 2013-10-20); NA 0.9% (rain 30.1% vs 21.8%) | fine; 0% -> NA optional | CLEAN-11 |
| Pressure9am | MSL pressure hPa at 9 am | yes | float; 978.6..1042.5; 4 stations never | fine | |
| Cloud9am | oktas at 9 am (9 = obscured) | yes | float 0..9; 9 in 2 rows (kept as recorded, noted); 44.8% NA (12 stations never). Among recording stations NA rows rain 11.0% vs 24.2%, and the gap holds inside every RainToday x Humidity9am quintile (e.g. 4.7% vs 9.0%, 50.5% vs 59.3%): not explained by "dry mornings". NA rate rises 3% (2009) to 45% (2026), highest at arid stations; 0 oktas only 8.5% of present values: consistent with a blank meaning "no cloud" at automatic stations (inference) | question for the curator; weak: LightGBM 9 windows 0.8502 all, 0.8476 NA filled (no indicator), 0.8472 without Cloud9am | LEAK-10 / LEAK-37, CLEAN-10 |
| Temp9am | temp at 9 am | yes | float; -6.2..41.0 | fine | |
| RainToday | Rainfall > 1 mm (source) | yes | category Yes/No; equals Rainfall > 1 in every row | fine (derived copy kept as shipped, documented) | CLEAN-5 |
| RainTomorrow | target: rain > 1 mm 9 am D to 9 am D+1 | target | category; 21.8% Yes; rows labelled across file gaps and rows with own reading missing dropped | fine | USE-5, CLEAN-15 |
| MaxTemp_prev_day | max temp, 24 h from 9 am D-1 | yes (ends 9 am D) | float; lag verified = raw D-1 in 100% of rows; 8 rows below Temp3pm_prev_day | fine | LEAK-7 |
| Sunshine_prev_day | sunshine h to midnight D-1 | yes | float 0..14.5 (15 rows > 14 h, southern stations in summer, plausible); 61.5% NA (19 stations never) | fine | LEAK-7 |
| WindGustDir_prev_day | strongest gust dir to midnight D-1 | yes | category; lag verified 100% | fine | LEAK-7 |
| WindGustSpeed_prev_day | strongest gust km/h to midnight D-1 | yes | float 2..154; 3 rows below WindSpeed3pm_prev_day | fine | LEAK-7 |
| WindDir3pm_prev_day | wind dir at 3 pm D-1 | yes | category; NA includes calm 3 pm readings (raw: 1,664 speed-0 rows, all NA direction) | cleaning problem: NA means "Calm" | CLEAN-10, CLEAN-14 |
| WindSpeed3pm_prev_day | km/h at 3 pm D-1 | yes | float 0..87 | fine | LEAK-7 |
| Humidity3pm_prev_day | RH % at 3 pm D-1 | yes | float; 4 rows = 0 (all Woomera) | fine; 0% -> NA optional | CLEAN-11 |
| Pressure3pm_prev_day | MSL hPa at 3 pm D-1 | yes | float 972..1040.3 | fine | LEAK-7 |
| Cloud3pm_prev_day | oktas at 3 pm D-1 | yes | float 0..9; 9 in 1 row; 47.2% NA (rain 20.0% vs 23.4%) | fine (same NA mechanism as Cloud9am, weaker) | CLEAN-10 |
| Temp3pm_prev_day | temp at 3 pm D-1 | yes | float -5.1..48.2; lag verified 100% | fine | LEAK-7 |

Dropped and absent: RISK_MM (the label's amount, LEAK-10, correctly dropped); the ten after-9 am columns of D
(replaced by D-1, LEAK-10/LEAK-7; lag checked equal to the raw D-1 value at the same station for MaxTemp, Sunshine,
WindGustDir, Humidity3pm, Temp3pm). 230 rows have no D-1 row (all lagged columns NA, rain 20.9%): no outcome link.
No identifier columns, no object columns, no all-row statistics (CLEAN-7, CLEAN-9 hold).

**Problems, ranked**

1. P4, question (LEAK-10 against LEAK-37), weak. Cloud9am missingness carries label information that the 9 am
   state does not explain (rain 11.0% vs 24.2% among recording stations, gap within every RainToday x humidity
   stratum). The likely mechanism (inference: rising with automation, highest at arid stations, few 0-okta values) is
   a blank for "no cloud detected", which is known at 9 am and not a leak. Strength: 0.003 ROC AUC (0.8502 vs 0.8476
   with NA filled). Mildest remedy: keep; reword the anomaly bullet ("missing more often on dry mornings" understates
   it) to give the stratified numbers and the suspected mechanism, as a `Potential leak, kept on purpose:` note if the
   curator cannot rule out a later fill.
2. P7, CLEAN-10/CLEAN-14 (Should). Calm wind is a missing direction: WindDir9am NA in 15,003 rows with speed 0 (all
   speed-0 rows), WindDir3pm likewise. Remedy: set direction "Calm" where speed is 0 (one line per column), or a note.
   Low impact (speed 0 tells a model the same).
3. P7, CLEAN-1 (note). Rainfall (and RainToday) is a multi-day total in about 2,648 rows after a missing D-1 reading
   or row (BoM's accumulation rule, already used to drop rows for the label). Remedy: one anomaly bullet; optionally
   drop or mark those rows.
4. P7, CLEAN-11 (Should, trivial). RH 0% at Woomera (1 Humidity9am, 4 Humidity3pm_prev_day): impossible, set to NA;
   11 MinTemp > Temp9am, 8 MaxTemp_prev_day < Temp3pm_prev_day, 3 gust < 3 pm speed: keep as recorded.

No column holds a value after the prediction point; no leak beyond item 1.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** Temporal on `Date`, expanding train, nine 14-day windows every 42 days; it mirrors
"a station's forecaster at 9 am, model refit every two weeks, at known stations". No problem needs a re-split.

Loaded with `dataset_io.load(..., built=False)` (origin `rebuilt`, 264,562 rows). Models: LightGBM 300 trees, lr 0.05,
63 leaves, untuned; 2 threads.

**Regime (SPLIT-1 to SPLIT-4, USE-10, SPLIT-13)**

- The use case predicts for the same stations on later days (known entity, USE-10): temporal is right, Location stays a
  feature. Hidden-group probe: Location seen in train for 100% of test rows (by design); near copies 0.4%, seen 0.5%.
- Alternative run (cold start, a third of the stations held out per window, Location dropped): ROC AUC 0.829 on new
  stations against 0.849 for the shipped model on the same rows (mean of 9 windows). Location adds little (all
  features 0.847, without Location 0.832). The alternative is a different use case (a new station), not a fix.

**Windows (SPLIT-11, SPLIT-12, SPLIT-14 to SPLIT-18, SPLIT-20)**

| window | train (rows, share) | test days | test rows | rain days | stations |
|---|---|---|---|---|---|
| 0 | 263,940 (99.8%) | 2026-01-17..2026-01-30 | 622 | 83 | 46 |
| 1 | 262,058 (99.1%) | 2025-12-06..2025-12-19 | 627 | 102 | 46 |
| 2 | 260,171 (98.3%) | 2025-10-25..2025-11-07 | 633 | 205 | 46 |
| 3 | 258,259 (97.6%) | 2025-09-13..2025-09-26 | 642 | 111 | 46 |
| 4 | 256,352 (96.9%) | 2025-08-02..2025-08-15 | 632 | 180 | 46 |
| 5 | 254,450 (96.2%) | 2025-06-21..2025-07-04 | 627 | 141 | 46 |
| 6 | 252,536 (95.5%) | 2025-05-10..2025-05-23 | 639 | 161 | 46 |
| 7 | 250,639 (94.7%) | 2025-03-29..2025-04-11 | 631 | 119 | 46 |
| 8 | 248,740 (94.0%) | 2025-02-15..2025-02-28 | 625 | 63 | 46 |

- Train ends the day before each window in all 9 splits; 0 train rows on or after a test start. Expanding train from
  2007-11-01, newest window first (SPLIT-11). Train share >= 94% (SPLIT-14).
- 14-day windows match SPLIT-18 (weather: one to two weeks) and the refit story. Spacing (step 42 > window 14) puts one
  window in every season of the last year (Feb, Mar-Apr, May, Jun-Jul, Aug, Sep, Oct-Nov, Dec, Jan): the season check
  of SPLIT-20 passes. 2025 is a typical year (rain rate 0.219, all-years 0.17-0.28). Rows per window 622-642 and
  63-205 positives: well above SPLIT-17's floor. Per-window ROC AUC 0.788-0.920.
- Splits claims 35-36 hold exactly.

**Gap and late labels (SPLIT-9, SPLIT-10, LEAK-10)**

- Label of day D = rain 9 am D to 9 am D+1, known at 9 am D+1. The last train day is window start - 1, whose label is
  read at 9 am on the window's first day: every training label is known at the refit, and no gap is needed (gap 0,
  `time_gap` null, correct). The `_prev_day` features of the first test day come from the last train day, known by
  9 am. No training row carries an outcome after the prediction point.
- Window 0's last day (46 rows) takes its label from BoM's 2026-01-31 reading, outside the file (claim 24, 15 stations
  checked against BoM); cannot re-verify offline.

**Training history (SPLIT-20, SPLIT-21)**

- History has a break: 1,125 rows in 2016 (2016-01-27 to 2017-02-28 missing) and Sunshine_prev_day missing jumps from
  53% (2015-16) to 74% (2017) and 79-87% (2025-26). Info only (SPLIT-21 forbids deciding from it): train from
  2017-03-01 gives ROC AUC 0.842 against 0.847 with the full history, so the old years do no harm.

**Forecasting scope on the shipped windows (TP-10, SEL-11; the checklist's "not re-run on 14-day windows")**

Mean of 9 windows: persistence (RainToday) AUC 0.661; station x month climatology from train 0.672; LightGBM on the
station's rain series + station + calendar 0.743 (log-loss skill +0.107); station + calendar 0.667 (-0.023); all
features 0.847 (+0.301). The covariate model beats the best naive forecast in every window (smallest margin window 2,
0.791 vs 0.616). TP-10's test passes on the shipped split; the scope call stays the curator's (REVIEW issue 4).

**Problems, ranked (principles.md)**

1. **P4, note: the training history is not argued (SPLIT-20, Should).** The splits_comment says "train is every
   earlier day (from 2007-11-01)" without naming the 2016 break or the Sunshine/Evaporation missingness jump.
   Evidence above (0.842 vs 0.847). Mildest remedy: one sentence in `splits_comment`; no change to the split.
2. **Writing, minor: "the 3 x 3 splits of the v2 protocol" (claim 37).** Holds as a count: 3 repeats x 3 folds = 9 splits for this size; the layout is the temporal convention (one repeat per window, fold 0; definitions.md, `splits_temporal_layout`), which the plan follows. Optional rewording: "the 9 splits the v2 protocol gives this size".
3. **P4, open (curator): window spacing (REVIEW issue 2).** Step > window is new in the copy; the evidence supports it
   (seasons covered, SPLIT-18 horizon). No remedy needed.

</details>

<details><summary>Domain practitioner</summary>

Actor played: a farmer or a local forecaster at one of the 49 BoM stations, at 9 am on day D, deciding whether to act
(spray, cut hay, irrigate, plan field work) on rain of more than 1 mm before 9 am on D+1.

**Fit: approximate (the definition says direct)**

The rows, the label's timing, the prediction point and the split mirror the decision (USE-3, USE-10), but the input I
would always act on, the BoM forecast built from weather models (NWP post-processed at stations by OCF / IMPROVER), is
absent, so the task is "predict tomorrow's rain from this station's own observations alone", a stand-in with a known
gap (USE-8). The definition's own `fit_reason` already names that gap ("A forecaster would also have weather-model
output, which the data lack"); USE-8 puts a named stand-in under approximate, not direct.

USE-9 check: is there another use case the data mirrors directly? The candidates (a farm's own station without
internet, a statistical backup when NWP fails, Zambretti-style on-device forecasts of home weather stations) are rare
and do not use BoM's synoptic stations; adopting one would be a use case rephrased to excuse the gap (weighed factor
against USE-9). So approximate stands. This does not argue against shipping: USE-12 and the siblings show a task with
a named gap is kept.

**1. Inputs at 9 am on D**

Known and present (USE-3 holds after the fix): 9 am temperature, humidity, pressure, cloud, wind; the minimum
temperature, rain (`Rainfall`, `RainToday`) and evaporation to 9 am; D-1's max temperature (24 h from 9 am on D-1, so
it ends at 9 am on D), sunshine and gust (to midnight D-1), D-1's 3 pm readings; station and date. The replacement of
the ten after-9-am columns by their D-1 values is exactly what I would have; none of the shipped columns is later than
9 am on D. Pressure tendency (9 am D minus 3 pm D-1) is derivable by the model.

Missing that I would always have, ranked:

1. **NWP-based forecast** (BoM's daily "chance of any rain" and "possible rainfall", OCF/IMPROVER station guidance).
   It is the main input of every real decision; the realistic ML task in weather is post-processing it, as the
   siblings `bias_correction_r_bias_correction_r_2` and `climate_model_weather_forecasting_1m` do (USE-6). Not in the
   source; cannot be added.
2. **Other stations' observations of the same morning.** A forecaster reads the synoptic picture: rain and pressure
   upwind. The file holds them (same Date, other Location). Test (LightGBM 400
   trees, nine 14-day windows at the shipped cadence): adding every station's 9 am Rainfall, Pressure9am and
   Humidity9am of the same date lifts mean ROC AUC 0.850 -> 0.873 and log loss 0.350 -> 0.331, better in 7 of 9
   windows (up to +0.046). Caveat: Perth's 9 am is 11:00-11:30 am in the east, so a strict version uses only stations
   whose 9 am is not later than the row's (a time-zone check, LEAK-10 / USE-3).
3. Hourly overnight observations (radar, pressure trend through the night): a forecaster has them; the DWO is daily.
   Not addable from the source; small next to 1 and 2.

None I would not have.

**2. Target**

`RainTomorrow` (> 1 mm, 9 am D to 9 am D+1) is close to what I act on (USE-5): 1 mm is the climatological "rain day"
and a sensible threshold for field work. Differences from the product I read: BoM's chance of rain is > 0.2 mm over the
calendar day (midnight to midnight), and my real decision often needs a shorter window (a rain-free 6 h for spraying)
or a longer one (3-5 days for hay). These are resolution differences, not a proxy. I want a calibrated probability,
not a class: the shipped metric is `roc_auc` (README), which ranks but does not reward calibration; `log_loss` would
match the use (a farmer acts at a threshold of their own cost ratio).

**3. Rows and test data**

One row = one station-morning = one decision (USE-1). The stations are known entities with history (USE-10): temporal
split, Location as a feature, test on the next two weeks at the same stations, refit every two weeks, every season
covered (SPLIT-18 horizon). That is what I would face. The dropped rows (label across a gap in the file, missing own
9 am reading whose next value may be accumulated) are rows I would never score as a 24 h decision (USE-7 spirit).
Sunshine and Evaporation missing at 66-79% of recent rows is real: most stations do not measure them.

Forecasting scope (REVIEW issue 4, SEL-10/SEL-11, TP-10): as the actor, I am not extrapolating a rain series; I classify
tomorrow's event from this morning's state across 46 stations in one model. The verifier's numbers (station's rain
series + station + calendar 0.732 ROC AUC; all features 0.856; without Rainfall/RainToday 0.855) show the skill comes
from the morning's state, not the lagged target, which is what TP-10 asks. From the domain side it is a fixed
predictive task with a temporal split, in scope.

**4. Would I use it?**

As the farmer: no, not instead of BoM's forecast; a station-only model at ROC AUC ~0.82-0.85 is far below an NWP-based
next-day forecast. I would use it as a fallback for a site without guidance, or as a feature in a post-processing model.
As a benchmark user: yes, it is an honest, large, real-sensor next-day classification with a correct prediction point.

Trust: the 9 am cut (no afternoon data of D), seasons covered, per-station calibration. Distrust: no NWP, so the
absolute skill says nothing about operational value; ROC AUC hides miscalibration; the 2016-17 gap and the growing
missingness of Sunshine/Evaporation shift the inputs over time.

**Gaps ranked by how much they change the task**

1. No NWP forecast (USE-6, USE-8): changes the task from "post-process the forecast" to "forecast from local
   observations"; the reason for approximate. Cannot be fixed from the source.
2. No same-morning observations of other stations: +0.023 ROC AUC when added; addable from the file (time-zone-safe).
3. Metric `roc_auc` where the actor acts on a calibrated probability: consider `log_loss`.
4. Label window and threshold (9 am-9 am, > 1 mm) differ from BoM's product (calendar day, > 0.2 mm): resolution only.
5. Daily, not hourly, observations: small.

**What an expert would change**

* Set `fit="approximate"` and lead `fit_reason` with the missing NWP forecast (USE-8): "a station-only forecast
  standing in for the forecast-informed decision". Optionally say "for example" use case is a fallback forecast.
* Optionally add time-zone-safe same-morning observations of the other stations (or the nearest/upwind ones) as
  features; a curator's choice, since it reshapes the table (USE-1, USE-3).
* Consider `log_loss` as the metric for a probability the actor thresholds.
* Keep the 9 am prediction point, the D-1 replacement, the row drops and the 14-day windows.

**Sources**

* BoM, Daily Weather Observations and their notes (IDCJDW0000): https://www.bom.gov.au/climate/dwo/
* BoM "chance of rain" (> 0.2 mm, midnight to midnight): https://farmpoint.tas.gov.au/news/interpreting-bom-forecasts,
  https://media.bom.gov.au/social/blog/828/a-week-of-rain-detailed-rainfall-information-to-land-on-all-prcis-forecasts
* BoM OCF / IMPROVER post-processing: https://publish.csiro.au/ES/ES19047, https://mssanz.org.au/modsim2025/files/K02.owen.pdf
* Definition, README, REVIEW.md of datasets/_dev/tabarena-v0pt2/rain_in_australia/; the panel's task probe
* Rules: use_case.md USE-1, USE-3, USE-5, USE-6, USE-7, USE-8, USE-9, USE-10, USE-12; selection.md SEL-10, SEL-11;
  task_probes.md TP-10; splits.md SPLIT-18
* Experiment: the neighbour test above

</details>

<details><summary>Blind review</summary>

**Verdict:** I would include it with changes. The table is honestly prepared and has real signal. The provenance in task.md is wrong and needs fixing.

**Task**
The model makes a next-day rain/no-rain call at a station, using the 9am observations. In BoM data, Rainfall on date D is the 24 h to 9am D, so RainTomorrow means rain of more than 1 mm between 9am D and 9am D+1. Real forecasters use NWP, so this is a well-known teaching task (the rattle weatherAUS data) rather than an operational one. Still, the setting is coherent and the data are real BoM observations.

**Concerns, most serious first**
1. **The source link does not match the data.** task.md cites the Kaggle "Rain in Australia" dataset. That release has about 145k rows covering 2008 to mid-2017. The table here has 264,562 rows dated 2007-11-01 to 2026-01-30, so it must come from the regularly updated rattle `weatherAUS` (CRAN docs: "regularly updated"; about 275k rows in 2026). Fix: cite rattle/rattle.data with its version or date, and state that rows without a target were dropped (275k to 265k).
2. **There is a gap in the dates.** In the 200k sample, data stop after 2016-01 (835 rows) and resume in 2017-03. This is probably a gap in the source. Fix: document it and check that no test window lands on or across it.
3. **The target is the next row's RainToday.** For 149,738 consecutive same-station day pairs, RainTomorrow equals the next day's RainToday in 100.0% of cases. A row-wise model cannot exploit this. Any model given neighbouring rows, or "previous target" features, could. Fix: state in the task that rows must not be joined across dates.
4. **Use is mostly educational.** The task is also partly saturated: in the sample, a LightGBM trained on dates before 2022 reaches test AUC 0.850, against 0.768 with 4 features and 0.68 from Humidity9am alone. That is enough signal to be useful. Prevalence is 21.8% Yes.
5. **Missing values are structural.** Evaporation is 57% missing, Sunshine_prev_day 62% and Cloud about 45%. They depend on the station, which is fine for a benchmark. Keep them as NaN; no change needed.

**What is handled well**
- Afternoon and whole-day variables (MaxTemp, Sunshine, gusts, 3pm readings) are shifted to `_prev_day`, so nothing observed after 9am D leaks in. MinTemp and Evaporation are 24 h to 9am, so they are available at prediction time.
- RainToday is consistent with Rainfall > 1 in every row.
- There are no duplicate (Date, Location) pairs and no fully duplicated rows.
- The temporal split matches how the model would be used.

**Not checked**
- The exact source version.
- Whether the 9 test windows avoid the 2016-17 gap.
- The 64,562 rows not included in the sample.

</details>

<details><summary>Precedents</summary>

Precedent checker. Inputs: the decision register (808 decisions), the record
`curation/records/rain_in_australia.md`, the definition and README in `datasets/_dev/tabarena-v0pt2/rain_in_australia/`,
the previous REVIEW.md, the verification checklist, sibling records (weather, forecasting scope, version swaps) and the Cases tables of
`selection.md`, `splits.md`, `task_probes.md`, `provenance.md`, `leak_checks.md`. The register has no decision on
rain_in_australia beyond the two AI assessments of the record (2026-10-07, 2026-10-20) and Andrej's undated comment.

**Summary**

| # | Decision | Rule | Verdict |
|---|---|---|---|
| A | Forecasting scope (issue 4) | SEL-10, SEL-11, TP-10 (Must) | follows bias_correction / climate_model / ashrae in substance; **the issue cites the wrong precedent** (el_nino, pre-TP-10); the TP-10 test has not run on the shipped windows |
| B | Lagged target shipped as features (`Rainfall`, `RainToday`) | TP-10 leg 2; ashrae, g_research | **departs without a stated reason** (reflection prompt below) |
| C | 14-day windows (issue 2) | SPLIT-18 | consistent (climate_model, bias_correction, aeolus) |
| D | Windows spaced every 6 weeks (issue 2) | SPLIT-11, SPLIT-15 (Should) vs SPLIT-20 | departs with a stated reason; first case of its kind |
| E | No gap between train and test | SPLIT-10 | consistent; reason evident from the data but not written down (bias_correction, aeolus use gap=1) |
| F | rattle file, not the Kaggle snapshot (issue 3) | PROV-8, PROV-13, PROV-14 | consistent (consumer_complaints, hr_analytics, house_prices_nominal, stroke_prediction) |
| G | Year 2026 / source_links (record fields) | PROV-9, PROV-8 | definition consistent; **record is not** (fix, no curator call needed) |
| H | Drop 2,575 rows without their own 9 am reading (issue 5) and 184 rows with a far next row | LEAK-26 pattern, PROV-13 | consistent (bias_correction 2026-10-15, LEAK-26 cases) |
| I | Uniqueness | PROV-4 to PROV-7 | no sibling found: unique |

No drift and no third exception of one kind found.

**A. Forecasting scope (issue 4)**

**Governing rule.** SEL-10 (Must) excludes forecasting; SEL-11 (Must; narrows SEL-10) and TP-10 (Must) let a
per-entity panel in when (1) a model on the features clearly beats each entity's naive forecast *on the shipped
windows* and (2) the source's top solutions used no lagged target. The tension row "A real task against a scope
pattern (P3 informs P2)" also applies.

**Precedents, out (`Time-series (Forecasting)`, `No`):**

* `appliances_energy_prediction` (Lennart, 2026-07-27) and `combined_cycle_power_plant` (Cases of SEL-10): a stream
  whose own future values are the target, no per-entity decision.
* `us_accidents` (Lennart, 2026-09-23): the authors' own task is a 15-minute grid-cell forecast.
* `el_nino_dataset` (undated, `No`, `Wrong Domain`, `Time-series (Forecasting)`): multivariate buoy series, the
  source's goal a two-year forecast; "We do not predict a target that we would not automatically obtain at time point
  t".
* `wind` (undated, `No`) and `wind_speed_prediction_dataset` (`No`, no comment): the target is read off at t.
* `g_research_crypto_forecasting` (AI, 2026-10-07 and 2026-10-20; REVIEW issue 1 still open): fails TP-10 leg 1
  (per-asset R^2 about 0) and, by measurement, leg 2 (features are sums of lagged targets, median r 0.80-0.83).

**Precedents, in:**

* `bias_correction_r_bias_correction_r_2` (Lennart ship, 2026-10-15): next-day Tmin per station, NWP forecast as input,
  model beats per-station MOS on 7 of 9 windows.
* `climate_model_weather_forecasting_1m` (`DF: Yes`; Lennart's comment sets weather windows to 1-2 weeks): next-day
  temperature with forecast features (TabRed).
* `ashrae_great_energy_predictor_iii` (Lennart, 2026-10-15; TP-10 Cases): in scope after the naive-profile test on the
  shipped windows; the top teams used no lagged readings.

**Comparison.** The facts that matter under TP-10 are the skill of the covariates against the station's own series and
whether the lagged target carries it. Measured (verifier, monthly windows of the first version): ROC AUC 0.856 all
features, 0.855 without `Rainfall`/`RainToday`, 0.732 for rain series + station + calendar, 0.650 for station +
calendar. That passes leg 1 with a clear margin, like ashrae and bias_correction, and unlike g_research. So the
dataset follows the "in" precedents in substance.

Two points where it does not line up:

1. **The issue argues from el_nino, not from the rule.** The el_nino sentence predates SEL-11 and TP-10 (both rest on
   ashrae, 2026-10-15), and read literally it would also exclude bias_correction and climate_model (their next-day
   temperatures are "automatically obtained" too), which Lennart shipped. The distinguishing facts between el_nino and
   this case are: el_nino's source goal is a two-year forecast of the series, rain_in_australia's target is a next-day
   threshold from same-morning observations of other quantities. Recommend the issue cite SEL-11 / TP-10 and the
   ashrae / bias_correction precedents, with el_nino as the counter-case.
2. **TP-10 is a Must with a test; the issue treats it as a weighing call.** The test has not run on the shipped
   windows (checklist, P2 row: "Not re-run on the shipped 14-day windows"). ashrae was settled only after that test on
   its shipped windows. By "facts first" (EV-1), run it on the 9 shipped windows (naive: persistence `RainToday`,
   station x month climatology, station rain series + calendar; then LightGBM with all features and without
   `Rainfall`/`RainToday`). If the margin holds, issue 4 is settled by the rule and the curator only confirms; if not,
   SEL-10 decides.

One difference from the "in" precedents to state in the issue, not a reason to depart: bias_correction and
climate_model carry an NWP forecast as input, rain_in_australia does not (README names this gap in the use-case fit).

**B. The lagged target as features (`Rainfall`, `RainToday`)**

`Rainfall` on day D is the RISK_MM of the station's row D-1 and `RainToday` is its RainTomorrow (README: "RainToday is
Rainfall > 1 mm in every row; we keep both, as the source ships them"). They are the lagged target itself, not an
aggregate of it. TP-10 leg 2 asks that the top solutions used no lagged target; ashrae shipped none, and the g_research
review reads the leg strictly (features that are sums of lagged targets fail it). There is no competition here, so
"top solutions" has no direct reading; the public Kaggle notebooks use `RainToday`.

The only reason written down is "as the source ships them", which is not a fact that sets the case apart under TP-10.
A distinguishing fact is evident from the measurement (dropping both costs 0.001 ROC AUC: the skill does not come
from the lag), and the 9 am gauge reading is a real morning observation a forecaster has. Neither is in the README or
the record. Treated alike with g_research, the two columns either go (remedy ladder: fix the definition) or stay with
the measured fact recorded.

**Consistency check (AI, 2026-10-20):** the definition keeps `Rainfall` and `RainToday`, which are the station's
lagged target (yesterday's RISK_MM and RainTomorrow), while TP-10 admits a forecasting-like panel only when no lagged
target is used (ashrae, 2026-10-15, shipped none; the g_research review of 2026-10-20 reads the leg strictly). What
sets rain_in_australia apart?
(a) the lag carries no skill (ROC AUC 0.856 with, 0.855 without; to be re-measured on the shipped windows) and the
9 am gauge reading is a same-morning observation the forecaster has, recorded as an exception to the reading of TP-10
leg 2 (serves P3: the use case reads the gauge); (b) treat it like g_research's strict reading: drop `Rainfall` and
`RainToday`; (c) relax the reading in g_research to match (it fails leg 1 anyway, so its outcome would not change);
(d) amend TP-10 leg 2 to "the skill does not come from the lagged target", measured by the drop-the-lag test.

**C. Window length (issue 2)**

SPLIT-18 (Should): weather test windows of one to two weeks at most; case `climate_model_weather_forecasting` (Lennart's
comment, undated: "For weather this is a bit much. I would argue for one or two weeks at most?"). Siblings:
`climate_model_weather_forecasting_1m` 7 days x 3; `bias_correction_r_bias_correction_r_2` 7 days x 9, gap 1
(Lennart ship 2026-10-15); `aeolus_1m` 14 days x 3, gap 1 (Lennart, 2026-10-12). 14 days follows them. Monthly
windows (an alternative in the issue) would depart from SPLIT-18 without a reason; the README gives none for them.

**D. Window spacing, 14 days every 6 weeks (issue 2)**

No dataset in the working copy spaces its windows (step > window): ashrae (`cutoffs` 2017-01/05/09, 4-month windows)
and apistox (10-year windows from 1984/1994/2004/2014) use cutoffs that tile the period; every other temporal folder
walks back contiguously. So this departs from SPLIT-11/SPLIT-15 (Should: roll the windows back from the newest data).
The reason is written (README decision 4): contiguous 14-day windows cover only 2025-09-27 to 2026-01-30, and
SPLIT-20 asks that the newest windows not all fall in one season, while SPLIT-18 forbids widening them. That is a
stated reason serving a rule of the same part, chosen from coverage and row counts, not from scores (SPLIT-21 holds:
the decision table lists rows and rain days only). Departs with a stated reason; first case, so no amendment is due.
If the curator accepts it, it becomes a Cases row of SPLIT-20 (or SPLIT-15). Related: aeolus met SPLIT-20 by placing
one of three contiguous windows in the holiday peak (2026-10-12), not by spacing.

**E. No gap between train and test**

`bias_correction` and `aeolus_1m` ship `gap=1`; `nyc_taxi_trip_duration` too. SPLIT-10: train on rows whose label is
known at the window's start. Here the label of the last training row (D-1) is the rain to 9 am on D, read at the
prediction point of the first test row: it is known in time, so no gap is needed. Consistent; the reason is evident
but the README states no gap reasoning (SPLIT-10: "The gap is part of the task and is stated with it"). One sentence in
the split note would close it.

**F. Source version (issue 3)**

PROV-8 (the first publication, not the re-upload), PROV-9 (a growing source takes the year of the pinned snapshot),
PROV-14 (a rebuild that would not match the release exactly is a new dataset). Precedents of a newer or fuller file
from the origin replacing the record's copy:

* `consumer_complaints` (Lennart, 2026-10-01): rebuilt from the CFPB's own archive; record `GOV Website`, year 2026.
* `hr_analytics` (2026-10-14, Cases of the task-probe table): rebuilt from the hackathon's own file, kept the record's
  name after the swap.
* `house_prices_nominal` (open REVIEW, 2026-10-20): De Cock's full file instead of the Kaggle half; recommends adding
  the origin to `source_links`.
* `stroke_prediction` (open issue): the contest's full training file, not the record's Kaggle cut.
* `loan_ibrd` (curator comment, undated): "we can and should take the newest data!"

Using rattle's file follows these. Not patching the 2016-01-27 to 2017-02-28 gap from the Kaggle snapshot is also
consistent: the two versions differ in 0.9% of the shared rows, so a merge would be a rebuild of our own (PROV-14, the
eryhemato tension: a version the source defines replaces ours, a fix of our own invention does not). The gap lies on
the training side only.

**G. Record fields**

The definition's `year = "2026"` and `source = "GOV Website"` follow PROV-9 and PROV-8 (consumer_complaints: same
pair). The record still says `year: '2017'` and lists only the Kaggle link in `source_links`. That is the record
lagging the definition, a Must fix with a direct precedent (house_prices_nominal item 10: add the origin link,
PROV-8), not a curator weighing call: add `https://rattle.togaware.com/weatherAUS.csv` (or the pinned archive URL) and
the BoM DWO page, set the year to 2026, keep Kaggle as a link to the snapshot.

**H. Rows dropped for a label that covers more than one day (issue 5)**

* `bias_correction_r_bias_correction_r_2` (Lennart, 2026-10-15): the three days without an LDAPS run dropped, because
  the task's premise fails on them.
* LEAK-26 (Cases: the house-price and runtime datasets): a target that does not mean what it means elsewhere (capped)
  is dropped or documented.
* The definition's own decision 2 (184 rows whose next row is 29-401 days later), the same mechanism.

Dropping the 2,575 rows follows these; the filter uses only what is known at 9 am on D (the missing reading), so it is
applicable at prediction time (SPLIT-9). Keeping them would depart from bias_correction without a stated reason (the
"missing reading as a rain signal" alternative names a side effect, not a fact that sets the case apart).

**I. Uniqueness**

`grep -il` over `curation/records/` for weatherAUS, rattle, RainTomorrow, the Kaggle slug and Bureau of Meteorology
finds only this record; no other folder in the working copy uses the data. `ghanas_indigenous_intel` (rain-gauge
target, retired 2026-10-01 as `Too Small`, `Data Quality Issue`) is another source and another task.

**For the mediator**

* Follows: 14-day windows (SPLIT-18), the rattle version (PROV-8, consumer_complaints / hr_analytics), the dropped rows
  (bias_correction), no gap (SPLIT-10, evident), uniqueness.
* Departs with a reason: spaced windows (SPLIT-15 Should, for SPLIT-20 season coverage; first case).
* Departs without a reason: the lagged target kept as features (TP-10 leg 2; prompt in B).
* Process: issue 4 should be settled by running TP-10 on the shipped windows and citing SEL-11 / ashrae /
  bias_correction, not left as a weighing call argued from el_nino.
* Record fix with no decision: year and source_links (G).

</details>

<details><summary>Advocate</summary>

Recommendation: ship. The validity Musts hold or are fixed in the definition already. The open findings are a USE-8
wording fix, two record fields and a few P7 notes, all handled by the mildest step on the remedy ladder.

**1. No leak: every input is known at 9 am (P4, LEAK-10 Must, holds; USE-12)**

- Evidence: in the claim audit, rattle row D matches BoM date D in every column at 7 locations (Jan 2026; a one-day
  shift matches 0-23%). The column audit finds no column recorded after 9 am on D, with the lag equal to the raw
  value of D-1 in 100% of rows. Putting the same-day after-9 am values back raises LightGBM from 0.849 to 0.902
  ROC AUC, so the lag removes a real leak and leaves none behind. RISK_MM, the label's amount, is dropped.
- Split side (SPLIT-9/SPLIT-10): the last training label is read at 9 am on the first test day, so gap 0 is correct
  (split audit).
- Why it outranks the objections: the "real task against a leak" tension (USE-12) says fix the leak and keep the task.
  That is done.

**2. In scope: TP-10 passes on the shipped windows (P2, SEL-11 Must narrows SEL-10; TP-10 Must)**

- Evidence (split audit, mean of the 9 shipped windows):
  - persistence (RainToday): 0.661 ROC AUC;
  - station x month climatology: 0.672;
  - the station's rain series + station + calendar: 0.743;
  - all features: 0.847.
- The model beats the best naive forecast in every window. The smallest margin is window 2, 0.791 vs 0.616. The
  checklist's gap ("not re-run on 14-day windows") is closed, and the fact is settled by experiment (EV-1).
- Precedents: the in-scope cases ashrae, bias_correction and climate_model_weather_forecasting_1m share these facts.
  el_nino predates TP-10, and read literally it would also exclude bias_correction, which was shipped (precedent
  check, A). "P3 informs P2": the actor classifies tomorrow's event from this morning's state; nobody here is
  extrapolating a series.
- Concession, TP-10 leg 2: Rainfall and RainToday are yesterday's label. They are also the 9 am gauge reading the
  actor has (LEAK-37/USE-6 Must), and they carry no skill: 0.856 with them vs 0.855 without (first version, monthly
  windows). Mildest remedy: record that measured fact as the distinguishing fact (precedent check, option a/d), with
  no data change. Even the strict reading (drop both, option b) costs about 0.001 and keeps the dataset. Either way,
  leg 2 is not a reason to withhold it.

**3. The split mirrors the use (P4; USE-10, SPLIT-11, SPLIT-18 hold; SPLIT-15 departure with a reason)**

- Regime: known stations on later days. Location is seen in train for 100% of test rows. A cold-start split is a
  different use case (0.829), not a fix (USE-10).
- Windows: 14-day windows follow Lennart's 1-2 week horizon for weather (SPLIT-18; siblings aeolus, bias_correction).
  Each holds 622-642 rows and 63-205 rain days, train is at least 94%, and train ends the day before every window.
- Spacing: the spacing departs from SPLIT-15 (Should). The fact that sets it apart is written: contiguous windows
  cover only Sep-Jan, and spacing gives every season (SPLIT-20, same part). It was chosen from row counts, not scores
  (SPLIT-21 holds). This is a Should departure with a stated reason, i.e. a valid exception, not a defect.

**4. Faithful, pinned data from the origin (P5, PROV-8/PROV-9 Must, hold in the definition)**

- The rattle file is the first publication; Kaggle is a 2017 re-upload. It is pinned: the archive sha256 was
  re-verified, and the CRAN 5.6.2 RData equals the CSV in all 275,410 x 24 cells. 17 of 19 columns match BoM's own
  pages 100%.
- Precedents for taking the origin's newer file: consumer_complaints, hr_analytics, loan_ibrd ("take the newest
  data").
- Concession: the record's `year: 2017` and Kaggle-only `source_links` are wrong. This is a record fix (year 2026; add
  the rattle and BoM links) and changes no data.
- Concession, wording: "49 stations" should read "49 locations (BoM pages, some combining several stations)". This is
  writing only; no split is affected, because a date is never on both sides of the split.

**5. A real use case; I concede the fit is approximate (P3, USE-8 Must)**

- The practitioner is right that a station-only model stands in for the NWP-informed decision. The definition's own
  fit_reason already names that gap. USE-8 puts a named stand-in under "approximate".
- Remedy: set `fit="approximate"` and lead fit_reason with the missing NWP forecast. This is a one-word definition
  fix. Approximate tasks ship (account_debt_south_africa, kick, alfa_battle, USE-8 Cases), so it is no ground to
  withhold.
- Everything else holds: inputs at 9 am, rows = decisions, a target that is the climatological rain day (USE-1,
  USE-3, USE-5).

**6. Worth benchmarking (P6, TP-1 to TP-10 pass)**

- Size and probes: 264,562 rows. Task probe flags: none. LightGBM beats the dummy on 100% of splits, and the smallest
  class in a test fold is 83.
- Not saturated: LightGBM - linear is +0.047 (paired SE 0.023), and per-window AUC ranges 0.788-0.920. The data are
  real sensors, and the dataset is unique in the collection (PROV-4 to PROV-7).
- Neighbour stations (+0.023 AUC, practitioner) are an optional enrichment that reshapes the table and needs a
  time-zone guard. It is a curator's choice, not a defect of the shipped task.

**7. The remaining findings are P7 or writing: fix cheaply or note (remedy ladder; "real task against imperfect cleaning")**

- Cloud9am missingness: 0.003 AUC (0.8502 vs 0.8476 with NA filled). The likely mechanism is a blank written for "no
  cloud" by automatic stations, which is known at 9 am (LEAK-37). Remedy: keep, and reword the anomaly bullet with the
  stratified numbers.
- Calm wind as a missing direction (CLEAN-10 Should): one line per column sets "Calm" where speed is 0, or a note.
- RH 0% at Woomera (5 cells): set to missing.
- 2,648 rows whose Rainfall may be a multi-day total: an anomaly bullet.
- Writing:
  - task_summary.changes should name the 10,664 dropped unlabelled or no-reading rows;
  - splits_comment should name the 2016-17 break (0.842 vs 0.847, no harm).
- The metric (ROC AUC vs log_loss) is a collection-level house choice, not a validity issue for this dataset.
- None of these touches a Must of P1-P5, so none outranks shipping.

</details>

<details><summary>Critic</summary>

**Position: ship only after changes.** The 9 am prediction point, the D-1 lag, the dropped rows and the 14-day
windows hold up (claim audit 5, 8-9, 23; split audit). I do not argue to exclude. Two Must problems in how the
task is described and justified, one record fix, and some notes are what stand between the definition and shipping.

**1. The fit is written as `direct` although the definition names a gap (P3, USE-8, Must)**

- Problem: `fit="direct"`, yet `fit_reason` itself says "A forecaster would also have weather-model output, which the
  data lack." USE-8 puts a named stand-in under approximate, not direct.
- Effect: the benchmark tells users this is the forecaster's real decision; it is "forecast tomorrow's rain from one
  location's own observations, without NWP", a station-only stand-in. Absolute skill (ROC AUC ~0.85) says nothing about
  operational value.
- Evidence: practitioner report (fit: approximate; NWP / OCF-IMPROVER guidance is the main input of every real
  decision). USE-9 was checked: the candidate direct use cases (offline farm station, NWP fallback) are rare and would
  be a use case rephrased to excuse the gap. The blind reviewer independently calls it a teaching task rather than an
  operational one.
- Remedy (fix the definition): `fit="approximate"`, `fit_reason` leading with the missing NWP forecast. The siblings
  bias_correction and climate_model carry NWP and are direct; this one differs by exactly that fact.

**2. The lagged target is kept as features with no reason that TP-10 accepts (P2 via TP-10, Must)**

- Problem: `Rainfall` on D is row D-1's `RISK_MM` and `RainToday` is row D-1's `RainTomorrow`: the lagged target
  itself. TP-10 admits a forecasting-like panel only when it beats the naive forecast on the shipped windows and no
  lagged target is used. The only stated reason is "we keep both, as the source ships them".
- Effect: without a recorded fact, the task is inconsistent with g_research (strict reading of leg 2) and the scope
  question (REVIEW issue 4) stays argued from el_nino, a pre-TP-10 precedent that would also exclude shipped siblings.
- Evidence: precedents B and A. Leg 1 now passes on the shipped windows (split audit: all features 0.847 vs
  persistence 0.661, station x month climatology 0.672, station rain series + calendar 0.743; covariates win in 9 of
  9 windows). Dropping the lag costs about nothing (claim audit 50: 0.849 vs 0.847).
- Remedy (a note, not a drop): write the measured fact into the definition and record an exception to the reading of
  TP-10 leg 2 (the 9 am gauge reading is a same-morning observation the actor has; the skill does not come from it),
  or the curator amends leg 2 to "the skill does not come from the lagged target" (consistency prompt in
  precedents.md B). Rewrite issue 4 to cite SEL-11 / TP-10 / ashrae / bias_correction with the shipped-window numbers,
  so it becomes a confirmation, not an open weighing call.

**3. Cloud9am missingness carries label information the note understates (P4, LEAK-10 against LEAK-37; weak)**

- Problem: the anomaly bullet says Cloud9am "is missing more often on dry mornings". Among recording stations, rows
  with NA rain 11.0% vs 24.2%, and the gap holds inside every RainToday x Humidity9am stratum, so the 9 am state does
  not explain it. The likely mechanism (automatic stations leaving "no cloud" blank, rising 3% to 45% over time) is
  inference, not shown.
- Effect: small, 0.003 ROC AUC (0.8502 vs 0.8476 with NA filled). Not a reason to change the data.
- Evidence: column audit, problem 1; leak probe: Cloud9am missing indicator alone AUC 0.588.
- Remedy (a note): replace the bullet with a `Potential leak, kept on purpose:` note giving the stratified numbers,
  the suspected mechanism, the 0.003 effect and when to revisit (LEAK-30 tension row: weak, kept with a note).

**4. The record contradicts the definition on year and source (P5, PROV-8, PROV-9, Must)**

- Problem: the record says `year: '2017'` and lists only the Kaggle link; the definition uses rattle / BoM and 2026.
  Kaggle is a later snapshot (rattle had weatherAUS since 2008).
- Evidence: claim audit 43; precedents G (consumer_complaints, house_prices_nominal).
- Remedy (repair the record, no curator call): year 2026, add the rattle URL (or the pinned archive capture) and the
  BoM DWO page to `source_links`, keep Kaggle as the snapshot. REVIEW issue 3 then only confirms.

**5. "49 stations" is refuted: a Location is a BoM page that combines stations (P5 wording, Should)**

- Problem: Sydney combines 3 stations (rain/temp 066214, cloud/pressure/sunshine 066037, wind 066022), Perth 4;
  Perth/PerthAirport, Sydney/SydneyAirport and Melbourne/MelbourneAirport share Sunshine on 100% of shared days.
- Effect: the row is not "one station", and paired locations are near copies on some columns. No split harm: a date
  is never on both sides (claim audit, implied claims).
- Remedy (fix the text): "49 locations (BoM DWO pages, some combining several stations)" in `task_summary.row` and
  `curation_comments`, with one anomaly bullet on the shared Sunshine.

**6. The split note leaves the training history and the gap unargued (P4, SPLIT-20, SPLIT-10, Should)**

- Problem: `splits_comment` says "train is every earlier day (from 2007-11-01)" without the 2016-01-27..2017-02-28
  break or the Sunshine/Evaporation missingness jump, and gives no reason for gap 0 (SPLIT-10: the gap is stated with
  the task).
- Evidence: split audit (train from 2017-03 0.842 vs full 0.847; label of the last train day is read at 9 am on the
  first test day); precedents E (bias_correction, aeolus ship gap 1).
- Remedy (a note): two sentences in `splits_comment`. No re-split.

**7. Cleaning gaps, cheap to fix or note (P7, CLEAN-10, CLEAN-1, CLEAN-11, Should; quality, not a reason to exclude)**

- WindDir9am / WindDir3pm_prev_day are NA for every calm reading (15,003 and 1,664 raw rows with speed 0): set
  "Calm" where speed is 0, or note it (CLEAN-10).
- Rainfall / RainToday is a possibly multi-day total in 2,648 kept rows after a missing reading (40.6% vs 21.8%
  RainToday): one anomaly bullet (CLEAN-1). The same BoM rule already justifies the row drop for the label.
- Humidity 0% at Woomera (5 values): set NA (CLEAN-11).
- `task_summary.changes` omits the 8,093 unlabelled and 2,571 missing-reading rows dropped: add one clause (claim
  audit 7).

Evidence: column audit problems 2-4; claim audit 7, 25.

**Judgment record (as I argue it)**

Verdict: ship after changes.
Validity: SEL-11 / TP-10 leg 1 holds on the shipped windows, leg 2 needs a recorded fact or amendment (point 2);
USE-8 triggered, fix fit to approximate (1); LEAK-1 / LEAK-10 hold after the lag, Cloud9am weak signal kept with a
note (3); PROV-8 / PROV-9 record fix (4); SPLIT-1 to SPLIT-4 hold.
Value: TP probes pass (LightGBM beats dummy on every split, smallest test class 83).
Quality: CLEAN-10, CLEAN-1, CLEAN-11 cheap fixes or notes (7).
For the curator: point 2 (exception or amendment of TP-10 leg 2), window spacing (REVIEW issue 2, not disputed here).

</details>

<details><summary>Advocate rebuttal</summary>

Neither side asks to exclude the dataset or to re-split it, and the critic's remedies match mine. I concede the
verdict should be "ship after changes" rather than "ship as is". Every change is a definition field, a note or a
record field, with no data change except the optional cleaning in 7. The only disagreement is how heavy two notes
should be (points 2 and 3).

1. **Fit should be approximate (USE-8, Must). Conceded.** This was my point 5. The fix: set `fit="approximate"` and
   start `fit_reason` with the missing NWP forecast. The fact that sets it apart from bias_correction and
   climate_model is that they carry NWP and this one does not. Approximate tasks ship (USE-8 Cases), so the dataset
   stays.

2. **Lagged target as features (TP-10 leg 2, Must). Remedy conceded; one framing point disputed.**
   - Conceded: the definition gives "as the source ships them" as its only reason, and that does not count under
     TP-10. Write the measured fact into the definition and rewrite issue 4 to cite SEL-11, TP-10, ashrae and
     bias_correction with the shipped-window numbers (0.847 against 0.743 or less, ahead in 9 of 9 windows).
   - Disputed: the critic calls this an exception to a Must. principles.md allows no exceptions to a Must ("A Must has
     no exceptions ... anything else is an amendment"). So there are two clean routes:
     - Route (a): LEAK-37/USE-6 (Must) says the 9 am gauge reading is a same-morning observation the actor knows, and
       TP-10 leg 2 is about competition top solutions, which this dataset does not have. Recording that fact is an
       application of the rules, not an exception.
     - Route (b): the curator amends leg 2 to "the skill does not come from the lagged target" (precedent check d).
   - Dropping both columns costs about 0.002 AUC (0.849 vs 0.847), so even the strict reading keeps the dataset. The
     choice of route goes to the curator.

3. **Cloud9am missingness (LEAK-10 vs LEAK-37, weak). Partly conceded.**
   - Conceded: the bullet understates the effect. Add the stratified numbers (11.0% vs 24.2% rain among recording
     stations) and the 0.003 AUC effect.
   - Disputed: the heading. A `Potential leak, kept on purpose:` note (LEAK-38/LEAK-30 pattern) is meant for a
     signal that may come after the outcome. Here the blank is written in the 9 am report, which LEAK-37 makes
     legitimate. The evidence points the same way: the missing rate rises with automation (3% to 45%), it is highest
     at arid stations, and 0 oktas is rare.
   - Mild remedy either way: use the potential-leak heading only if the curator cannot rule out a later fill;
     otherwise use a plain anomaly bullet with the mechanism. Both keep the data.

4. **Record year and source_links (PROV-8, PROV-9). Conceded.** Fix the record (year 2026; add the rattle URL or the
   archive URL and the BoM DWO page; keep Kaggle as the snapshot). This needs no curator call.

5. **"49 stations" (writing). Conceded.** Change it to "49 locations (BoM DWO pages, some combining several
   stations)" and add a bullet on the shared Sunshine. The split is unaffected: a date is never on both sides.

6. **History break and gap 0 unargued (SPLIT-20, SPLIT-10, Should). Conceded.** Add two sentences to
   `splits_comment`:
   - the 2016-17 break, with train from 2017-03 at 0.842 against 0.847 for the full history;
   - gap 0, because the last training label is read at 9 am on the first test day.

   No re-split.

7. **Cleaning (CLEAN-10, CLEAN-1, CLEAN-11). Conceded.**
   - Fix: "Calm" where the wind speed is 0, and RH 0% set to missing.
   - Notes: an anomaly bullet for the 2,648 possibly multi-day Rainfall rows, and one clause in
     `task_summary.changes` for the 10,664 dropped rows.

   These are quality items (P7) and none outranks shipping ("real task against imperfect cleaning").

Agreed judgment record:

```text
Verdict: ship after changes.
Validity: SEL-11/TP-10 leg 1 holds; leg 2 needs the recorded fact (LEAK-37) or an amendment; USE-8 changed to approximate; LEAK-10 holds; PROV-8/9 record fix.
Value: the task probes pass.
Quality: notes and cheap fixes.
For the curator: the TP-10 leg-2 route and the window spacing.
```

</details>

<details><summary>Critic rebuttal</summary>

The advocate's brief asks to "ship as defined", but it concedes USE-8, the record fields, the wording and the P7
fixes. So we agree on the verdict, **ship after changes**. What remains in dispute is narrow: how two of the
changes are recorded. No new points.

**1. No leak (LEAK-10 holds; gap 0 correct): concede, with one remainder**

I agree the lag removes a real leak (0.902 to 0.849) and that gap 0 is right. SPLIT-10 (Should) still asks for the gap
to be "stated with the task"; `splits_comment` does not state it. Remedy as in my point 6: one sentence.

**2. TP-10 passes: concede leg 1; leg 2 partly disputed**

- Leg 1: conceded. The shipped-window numbers settle it (EV-1).
- Leg 2: we agree on the remedy (record the fact, option a or d; no data change). I dispute the evidence the advocate
  cites. The 0.856 vs 0.855 comes from the first version's monthly windows, not from the shipped definition. The
  number to record is the claim audit's run on the 9 shipped windows: 0.849 with the lag, 0.847 without
  (claim audit 50).
- LEAK-37 does not answer leg 2. LEAK-37 says the reading is not a leak. TP-10 asks something else: whether a
  forecasting-like panel relies on its lagged target. The fact that settles leg 2 is the measured lack of skill
  (0.002), not that the actor knows the reading.
- Until an exception or amendment is written into the definition and the record, the departure has no recorded
  reason (principles: a Should/Must departure needs the fact written). So "ship as defined" does not hold here.

**3. The split mirrors the use: concede**

The spacing is a SPLIT-15 departure with a stated reason (SPLIT-20 season coverage, chosen without scores,
SPLIT-21). I raised no point against it. One part is still open: the training history (SPLIT-20) is not argued in
`splits_comment`. The advocate concedes this under its point 7.

**4. Faithful data: concede**

The origin, pinning and CRAN equality hold. The record fix (PROV-8/PROV-9) and the "locations" wording are conceded
by both sides. One addition: the shared Sunshine between paired locations (100% on shared days) belongs in an
anomaly bullet, not only in the corrected word.

**5. Fit approximate: agreed**

Same remedy as my point 1. I agree it is no ground to withhold (USE-8 Cases ship approximate tasks).

**6. Worth benchmarking: concede**

The TP probes pass, and the neighbour-station enrichment is the curator's choice. I made no point here.

**7. P7 findings: concede, except the Cloud9am wording**

- I dispute "keep, reword the bullet" as enough. The advocate rests the "not a leak" claim on LEAK-37 through a
  mechanism ("no cloud" left blank by automatic stations). The column audit marks that mechanism as inference, not
  shown.
- The stratified gap (11.0% vs 24.2% rain within every RainToday x humidity stratum) is not explained by the 9 am
  state.
- An unverified mechanism cannot invoke LEAK-37. The matching rule is the weak-leak tension row (LEAK-30 pattern): keep it,
  under a `Potential leak, kept on purpose:` note with the mechanism marked as suspected, the 0.003 effect and when
  to revisit (e.g. a BoM statement on blank cloud at automatic stations).
- The remedy is the same mildest step (a note, no data change). Only the note's form differs.
- The metric: agreed, not a point of mine.

**Remaining disputes for the mediator**

1. TP-10 leg 2: which number goes into the recorded fact. I say the shipped-window 0.849 / 0.847 (EV-2: a
   measurement on the shipped definition).
2. Cloud9am: an anomaly bullet (advocate) or a `Potential leak, kept on purpose:` note (critic). It turns on whether
   the "no cloud" mechanism is shown (LEAK-37) or only inferred (LEAK-10, weak; LEAK-30 tension).

</details>

<details><summary>Mediator</summary>

**Summary (mediator, rain_in_australia, 2026-10-20)**

I recommend shipping after changes. Both sides already agree on that, and no point of validity calls for a data change. I ran two experiments, which settle both disputed facts:

- **Lagged target (`Rainfall`/`RainToday`).** On the 9 shipped windows, ROC AUC is 0.8495 with these columns and 0.8467 without them (difference 0.0027, paired SE 0.0013; log loss 0.3516 against 0.3549). This replaces both the first version's 0.856/0.855 and the "0.001-0.002" both briefs quote.
- **Cloud9am blanks are mostly clear skies seen at the time of the observation.** On days with a blank cloud reading, sunshine falls between the 0-1 okta and the 2-6 okta days. The stations with the most blanks record almost no 0 oktas. So this is a plain anomaly note under LEAK-37, not a potential leak.

On leg 2 of TP-10, neither side's route holds. LEAK-37 is a P4 rule and cannot clear a P2 test, and a Must has no exceptions. What settles it is the tension row "P3 informs P2", the measured fact above, and USE-6. The curator still decides whether to amend the wording of leg 2.

---

**Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-1 holds. SEL-11/TP-10 leg 1 holds on the shipped windows (all features 0.847 vs station rain series
  + calendar 0.743, persistence 0.661, station x month climatology 0.672; ahead in 9 of 9 windows). TP-10 leg 2:
  no top solutions exist; the lagged target adds 0.0027 AUC (measured), so the skill does not come from it; the
  columns stay under USE-6 and LEAK-34, the fact recorded (wording of leg 2 for the curator, issue 1).
  USE-8 triggered, fixed (fit approximate: no NWP forecast). LEAK-10 holds after the D-1 lag (0.902 -> 0.849);
  Cloud9am blank = sky state at 9 am, LEAK-37 (anomaly note). SPLIT-1..4, SPLIT-9, SPLIT-10 hold (gap 0 correct);
  SPLIT-15 departure with a stated reason (SPLIT-20), first case (issue 2). PROV-8/PROV-9 hold in the definition,
  record links fixed, year open (field row).
Value: TP-1..TP-9 pass (no probe flags; smallest test class 83; LightGBM - linear +0.047, SE 0.023).
Quality: CLEAN-10 (Calm wind), CLEAN-11 (RH 0%) cheap fixes; CLEAN-1 note (2,648 possibly multi-day Rainfall rows).
Weighed: size +, real sensors +, unique +, fit approximate -, no NWP -.
For the curator: issue 1 (wording of TP-10 leg 2: amend, or drop the two columns), issue 2 (window spacing).
```

**Changes to make now (no decision needed)**

1. **Fit (USE-8, Must).** Set `fit="approximate"` and start `fit_reason` with the missing NWP forecast: "a forecast from the station's own observations, standing in for the forecast-informed decision". Both sides concede this.
2. **Record front matter (PROV-8, PROV-9, Must).** Set `year: 2026`. Add the rattle URL (or the pinned archive capture) and the BoM DWO page to `source_links`, and keep Kaggle as the 2017 snapshot. Both sides concede this.
3. **"Stations" becomes "locations" (P5 wording).**
   - Write "49 locations (BoM DWO pages, some combining several stations)" in `task_summary.question`, `task_summary.row`, `task_summary.use_case`, `curation_comments` and `splits_comment` ("46 locations").
   - Add one anomaly bullet: paired locations (Perth/PerthAirport, Sydney/SydneyAirport, Melbourne/MelbourneAirport) share Sunshine on 100% of shared days. No harm to the split, because a date is never on both sides of it.
4. **`task_summary.changes` (writing).** Add "and the rows without a label (8,093) or without their own 9 am rain reading (2,571)".
5. **`splits_comment` (SPLIT-20, SPLIT-10, Should).** Add two sentences:
   - The 2016-01-27..2017-02-28 break and the jump in Sunshine/Evaporation missingness. Training from 2017-03 gives 0.842 against 0.847 with the full history, so the old years do no harm.
   - Why there is no gap: the last training day's label is read at 9 am on the first test day.
   - Optionally replace "the 3 x 3 splits" with "the 9 splits the protocol gives this size".
6. **The bullet "RainToday is Rainfall > 1 mm... as the source ships them" (SEL-11/TP-10).** Replace the reason with the measured fact: Rainfall and RainToday are the station's 9 am gauge reading, i.e. yesterday's label. They add 0.0027 ROC AUC on the 9 shipped windows (0.8495 vs 0.8467; log loss 0.3516 vs 0.3549). Covariates without the station's rain series beat persistence and climatology in 9 of 9 windows. Kept under USE-6 and LEAK-34.
   - Rewrite REVIEW issue 4 to cite SEL-11, TP-10, ashrae and bias_correction with these numbers, and give el_nino as the counter-case (pre-TP-10; its source's goal was a two-year series forecast).
7. **Cloud9am anomaly bullet (LEAK-37; settled below).** Replace "missing more often on dry mornings" with the measured numbers:
   - Among recording stations, rain follows 11.7% of blank mornings against 24.2% overall. The gap holds within RainToday x humidity strata.
   - A blank is mostly a clear or near-clear sky: Cloud3pm blanks have 8.5 h of sunshine against 10.3-11.1 h for 0-1 oktas and 4.7 h for 7 oktas.
   - The high-blank stations record almost no 0 oktas (Uluru 76% blank, 0.1% zeros).
   - Effect: 0.003 AUC.
   - Revisit if BoM states otherwise. Rattle's cloud values also differ from current BoM pages at Melbourne and Hobart, a revision between versions.
8. **Cleaning (CLEAN-10, CLEAN-11 Should; CLEAN-1).** Both sides agree on all three.
   - Set `WindDir9am` / `WindDir3pm_prev_day` to "Calm" where the speed is 0 (15,003 and 1,664 raw rows).
   - Set RH 0% at Woomera to missing (5 cells).
   - Add one anomaly bullet for the 2,648 kept rows whose Rainfall/RainToday may be a multi-day total (RainToday 40.6% vs 21.8%).
   - Items 1 and 3-8 are text only. The Calm and RH edits change the data, so they need a CHANGELOG entry and a rebuild, which happens only when the curator asks for one.
9. **Record Assessment numbers (writing).** Quote the shipped-window figures (0.849 shipped, 0.902 with the same-day columns) in place of the earlier 0.846 and the first version's monthly-window numbers.

**Issues for the curator, ranked**

**1. TP-10 leg 2 (P2 Must, through SEL-11): what the shipped lagged target needs.**

- **Problem.** The rule admits a forecasting-like panel only if "the source's top solutions used no lagged target". This source has no competition and no top solutions; the public Kaggle notebooks use RainToday. The g_research review (2026-10-20) reads the leg strictly: features that are the lagged target fail it.
- **Effect on the score.** Dropping the two columns costs 0.0027 ± 0.0013 AUC. The columns help in 7 of 9 windows, and the task stays in scope either way.
- **Advocate's best case.** The 9 am gauge reading is an observation the actor has (LEAK-37/USE-6), so recording it is applying the rules, not departing from them.
- **Critic's best case.** LEAK-37 says the reading is not a leak. It does not answer the scope test. Only the measured lack of skill does, and it must be written down.
- **Settlement of the dispute.**
  - The critic is right that LEAK-37 (P4) cannot clear a P2 test. These are independent requirements.
  - The advocate is right that a Must takes no exception.
  - What decides is the tension row "a real task against a scope pattern (P3 informs P2: the use case decides whether the scope rule applies)", together with USE-6 (Must, P3). Dropping a known 9 am input changes the task. Literal leg 2 has nothing to test here, and its purpose (the skill does not come from the series) is met by measurement.
  - The number to record is the shipped-window one (EV-2), not the first version's.
- **Decision needed.** Pick one:
  - (d) Amend TP-10 leg 2 to "the skill does not come from the lagged target, measured by the drop-the-lag test on the shipped windows". This is recommended: it makes the reading explicit for every dataset and does not change g_research's outcome, which fails leg 1 anyway.
  - Keep the current wording and confirm the recorded fact as the application for this dataset.
  - (b) Treat it like the strict g_research reading and drop both columns. This costs 0.003 AUC and departs from USE-6.

**2. Window spacing (P4, SPLIT-15 Should vs SPLIT-20): 14 days every 6 weeks.**

- **Problem.** This is the first dataset in the copy whose spacing between windows is larger than the window.
- **Effect.** Every season of 2025 is covered. Contiguous 14-day windows would cover only Sep-Jan.
- **Evidence.** Each window has 622-642 rows and 63-205 rain days, and train is at least 94%. Window sizes were chosen from row counts, not scores (SPLIT-21 holds). The precedent check finds no conflict, and nobody disputed the point.
- **Decision needed.** Accept the spacing as an exception to SPLIT-15 (which would become a Cases row of SPLIT-20), or choose contiguous or monthly windows.

**3. Source version (P5, PROV-8/PROV-14).** Rattle's full file (2007-2026), not the Kaggle snapshot.

- This is consistent with consumer_complaints, hr_analytics and loan_ibrd.
- Not patching the 2016-17 gap from Kaggle is right: the two versions differ in 0.9% of shared rows, so a merge would be our own rebuild (the eryhemato tension).
- **Decision needed:** confirm.

**4. Dropped rows (P4/P5).** 2,575 rows without their own 9 am reading and 184 rows labelled across gaps in the file.

- This is consistent with bias_correction (2026-10-15).
- **Decision needed:** confirm.

**5. Weighing call (P3 against the table as published): neighbour-station observations from the same morning.**

- Practitioner: adding other stations' 9 am Rainfall, Pressure and Humidity lifts AUC from 0.850 to 0.873.
- Against: it reshapes the table and needs a time-zone guard (Perth's 9 am is 11:00-11:30 in the east).
- Optional; it is not a defect of the shipped task.
- The metric (log_loss for a farmer who thresholds a probability) is a collection-level choice, not one for this dataset.

**Agreed facts**

- **Prediction point.** 9 am on D. The label is rain > 1 mm from 9 am D to 9 am D+1, and equals RISK_MM > 1 in 100% of rows.
  - Rattle's row D matches BoM date D at 7 locations (17 of 19 columns 100%).
  - The ten after-9 am columns are replaced by their D-1 values; the lag equals the raw D-1 value in 100% of rows.
  - Putting the same-day columns back gives 0.902 against 0.849.
  - RISK_MM is dropped.
- **Size.** 264,562 rows, 49 locations, 2007-11-01..2026-01-30, 21.84% rain days. A location is a BoM DWO page combining 1-4 stations.
- **Split.** Temporal: 9 windows of 14 days every 42 days, 2025-02-15..2026-01-30.
  - Train ends the day before each window. Every test location is seen in train.
  - Gap 0 is correct.
  - A cold-start split (0.829) would be a different use case.
- **Scope test on the shipped windows.**
  - Persistence 0.661; station x month climatology 0.672; station rain series + calendar 0.743; all features 0.847.
  - The covariates win in 9 of 9 windows; the smallest margin is window 2, 0.791 vs 0.616.
- **Source.**
  - Pinned archive sha256 re-verified.
  - The CRAN 5.6.2 RData equals the CSV in all 275,410 x 24 cells.
  - Kaggle is a later re-upload.
  - The record's `year: 2017` and its Kaggle-only links are wrong.
- **Probes.** No flags. LightGBM beats the dummy on 100% of splits. Smallest test class 83. Unique in the collection.
- **Fit.** Approximate: there is no NWP forecast (USE-8).
- **Cleaning gaps.** Calm wind is coded as a missing direction. RH 0% at Woomera. 2,648 possibly multi-day Rainfall rows. 10,664 dropped rows are not named in `task_summary.changes`.

**Disputed facts, settled by experiment**

**1. Lagged-target ablation on the 9 shipped windows.** Same LightGBM as the claim audit (400 trees, lr 0.05, 63 leaves, 2 threads).

| Features | ROC AUC | Log loss |
|---|---|---|
| All (shipped) | 0.8495 | 0.3516 |
| Without Rainfall and RainToday | 0.8467 | 0.3549 |

- Difference: +0.0027 AUC (paired SE 0.0013), positive in 7 of 9 windows.
- These are the numbers to record. The first version's 0.856/0.855 come from other windows and are superseded (EV-2).

**2. Cloud blanks.** Twelve stations record both sunshine and partly-blank Cloud3pm; I compared the D-1 sunshine across cloud readings.

| Cloud3pm of D-1 | Mean sunshine of D-1 |
|---|---|
| 0 oktas | 11.1 h |
| 1 okta | 10.3 h |
| Blank | 8.5 h |
| 6 oktas | 6.9 h |
| 7 oktas | 4.7 h |
| 8 oktas | 3.0 h |

- Within station-month, blank days have 0.9 h less sunshine than 0-1 okta days, 0.9 h more than 2-6 okta days, and 4.3 h more than 7-8 okta days.
- Rain after a blank Cloud9am is 11.7%, between 1 okta (9.6%) and 2 oktas (14.2%).
- The stations with the most blanks record almost no 0 oktas: Uluru 76% blank / 0.1% zeros, Albury, Richmond and Wollongong 0.0% zeros.
- So a blank is mostly a clear or near-clear sky at the time of the observation, mixed with true gaps. It is not a fill after the outcome.
- This settles the second dispute for the advocate: LEAK-37 applies, the plain anomaly bullet goes in with the numbers, and the `Potential leak, kept on purpose:` heading is not used. A recode to 0 is not safe, because blanks mix clear skies with real gaps (CLEAN-10: keep, say why).

**Consistency with precedent**

- **Followed.**
  - Scope: ashrae, bias_correction and climate_model (TP-10 tested on the shipped windows).
  - 14-day windows: climate_model, bias_correction, aeolus (SPLIT-18).
  - Source version: consumer_complaints, hr_analytics, loan_ibrd.
  - Dropped rows: bias_correction.
  - Uniqueness.
  - An approximate fit that ships: account_debt_south_africa, kick, alfa_battle.
- **Departs, with the fact that sets this case apart.**
  - g_research (strict leg 2): here the lag carries 0.0027 AUC and leg 1 passes by +0.10 AUC over the station's rain series. In g_research the lagged sums carry the signal and leg 1 fails.
  - el_nino: its source's goal was a two-year forecast of the series, and it predates TP-10. Here the target is a next-day threshold from same-morning observations of other quantities.
- **First case, for the curator.** Spaced windows (issue 2).
- **Reflection question for issue 1.** Would you read leg 2 the same way for every source without a competition? If yes, amend the rule rather than decide case by case.

</details>
