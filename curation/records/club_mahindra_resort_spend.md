---
unique_name: club_mahindra_resort_spend
name: 'Club Mahindra DataOlympics 2019: food-and-beverage spend per room night of a resort reservation'
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
original_source: Other
year: '2019'
domain: business & marketing
problem_type: Regression
source_links:
- https://www.analyticsvidhya.com/datahack/contest/club-mahindra-dataolympics/
- https://www.kaggle.com/datasets/lampubhutia/customer-spent-at-clubmahindra-resort
- https://github.com/bishwarup307/AV_ClubMahindra
- https://github.com/sharmaroshan/Predicting_Money_Spent_at_Resort
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: about 300,000 Club Mahindra resort reservations (Analytics Vidhya hackathon, May 2019) with booking-time fields and the food-and-beverage spend per room night as the target, scored by RMSE; a named company's data, but the target is scaled by an unstated transform and the documentation is thin.
- Source: Club Mahindra DataOlympics, run "in association with Analytics Vidhya", datasets live from 2019-05-03 (AV contest page; Club Mahindra is the holiday club of Mahindra Holidays & Resorts India). The contest page names the company's analytics work (resort recommendations, "prediction of booking cancellation", lead conversion) but not this target; external data not allowed. As published (data dictionary in public solution repositories; Kaggle mirror lampubhutia/customer-spent-at-clubmahindra-resort of 2019-10-23, licence "unknown": `train_clubmahindra.csv` 92 MB, `test_clubmahindra.csv` 38 MB unlabelled, `Data_Dictionary.xlsx`): `reservation_id`, `booking_date`, `checkin_date` and `checkout_date` ("recorded at the time of booking"), `channel_code`, `main_product_code`, `numberofadults`, `numberofchildren`, `persontravellingid`, `resort_region_code`, `resort_type_code`, `room_type_booked_code`, `roomnights`, `season_holidayed_code`, `state_code_residence`, `state_code_resort`, `total_pax`, `member_age_buckets`, `booking_type_code`, `memberid`, `cluster_code`, `reservationstatusid_code`, `resort_id`, and the target `amount_spent_per_room_night_scaled` ("Resort Spend Per Room Night"). The 2nd-place write-up (GitHub bishwarup307/AV_ClubMahindra): "the objective is to predict the average spend of customers per room per night stay", about 300,000 reservations at 32 resorts; rows not counted here.
- Use case: at booking, the club estimates a reservation's F&B spend to plan resort F&B and target offers (the Kaggle mirror: the model "predicts the spending in response to the offer"); the source names the actor, not the decision, so the fit is approximate. Regime: "the train and test dataset were split on `memberid`," so no member is in both (2nd place), a grouped split by member; the booking and stay dates ship, so a temporal split is possible; decide from the use case, a known member's next stay or a new member (USE-10; SPLIT-3, SPLIT-5).
- Siblings and duplicates: no record holds this data (grep by Mahindra, resort, Analytics Vidhya). Other AV hackathons: `hr_analytics` (accepted), `wns_hr_employee_promotion` and `av_healthcare_analytics_length_of_stay` (run candidates), `lt_vehicle_loan_default_prediction` (TBD -> Yes), `black_friday` (TBD -> 2nd Tier); `hotel_booking_demand` (Yes) is hotel cancellation, another task. External collections: none found on the pages read.
- Better data: from the curator's Zotero collection (item 90, the DataHack platform); no further search this round.
- Papers and pages: the AV contest page; the 2nd-place solution (member-level aggregates "the most important one"; reservations with the same member and dates that "had different target values"); sharmaroshan/Predicting_Money_Spent_at_Resort (the data dictionary).
- Metric: RMSE: the contest judges by "RMSE/MSE" against a baseline Club Mahindra sets (AV page), and the Kaggle mirror says the model "will be evaluated on the MSE/RMSE"; the leaderboard values near 95 suggest 100 x RMSE (from memory, not on the pages read), which ranks the same; a competition's metric (MET-4), so `rmse` on the scaled target; inputs none.
- Risks for /add-dataset: how the target was scaled (a log, or a standardisation over all rows: LEAK-30, MET-3); `reservationstatusid_code` may be set after booking (a cancellation or stay status; USE-3, LEAK-10); repeated reservations of one member and dates with different targets; the 2nd-place features aggregate members over train and test together (transductive; our split must not); member history needs the split to respect members; AV registration for the files, the mirror's licence unknown (EV-4).
- Priority: gap 0 (business, regression, grouped and temporal are covered), use case 0 (the decision is ours), source + (a named company's hackathon with a data dictionary), shape + (about 300,000 reservations, mixed types, members and dates), risk - (scaled target, a possibly post-booking status column).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 90: "DataHack Platform: Compete, Learn & Grow in Data Science".
- as published: About 300,000 reservations across 32 resorts and more than 100,000 members (2nd-place write-up); rows not counted. Kaggle mirror: train 92 MB, test 38 MB (unlabelled), plus a data dictionary. 24 ...; target: amount_spent_per_room_night_scaled: food-and-beverage spend per room night of the stay (scaled; regression, scored by RMSE); access: registration.
- Why: A real hospitality task from a named company, large, with booking-time features and a clean prediction point. The other AV contests mostly name no provider.
- Adds: A hospitality spend regression; no record covers hotel or resort spend. Caveats: AV terms and an unknown licence on the Kaggle mirror; the target is scaled; reservationstatusid_code may be set after booking (check before use); the 2nd-place solver found repeated reservations with different targets; codes are ...
