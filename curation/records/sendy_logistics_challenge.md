---
unique_name: sendy_logistics_challenge
name: sendy-logistics-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2019'
domain: business & marketing
required_split:
- Random (IID)
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/sendy-logistics-challenge/data
source_row: 929
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> Yes`, priority 3: predict the time from pickup to arrival of a Sendy motorbike delivery in Nairobi from the order, its timestamps up to pickup, distance, weather and rider metrics; a real ETA task with a named user, but no month or year in the data.
- Source: Zindi, "Sendy Logistics Challenge" (2019-08-23 to 2019-11-25, 2,201 participants, $7,000), hosted by Sendy and insight2impact. As published: Train.csv (4.1 MB), Test.csv (1.2 MB), Riders.csv, VariableDefinitions.csv; "a subset of over 20,000 orders and only includes direct orders (i.e. Sendy 'express' orders) with bikes in Nairobi. All data in this subset have been fully anonymized while preserving the distribution", with weather added; columns Order No, User Id, Vehicle Type, Platform Type, Personal or Business, day of month / weekday / time for placement, confirmation, arrival at pickup and pickup, Distance (KM), Temperature, Precipitation, pickup and destination lat/long, Rider Id; Arrival at Delivery times only in Train; target "Time from Pickup to Arrival" in seconds.
- Use case: Sendy tells the customer an arrival time when the rider picks up the package, and plans scheduling ("enhance customer communication ... improved resource management and planning for order scheduling"); fit direct at pickup; regime: a temporal task by nature, but the release has only day of month and weekday, no month or year ("Placement - Day of Month i.e 1-31"), so the windows SPLIT-14 asks for cannot be built and it ships IID, forced from temporal (SPLIT-8). The AI-filled `required_split` `Temporal (NON-IID)` is changed to `Random (IID)` for that reason.
- Siblings and duplicates: `sendy_logistics_challenge_2` (the Zindi Mentorship #2 and EDSA 2020 re-runs, both with this competition as parent and the same file sizes; proposed `Duplicate` in this batch); `delivery_rider_response_challenge_by_galsenai` (IndabaX Senegal 2021, Sendy rider matching, AI `No`, another task). External collections: none found.
- Papers and pages: https://zindi.africa/competitions/sendy-logistics-challenge (winners linked from the page, not read).
- Metric: `rmse` on seconds (Zindi Evaluation: "The error metric for this competition is the Root Mean Squared Error"), a leaderboard metric (MET-4); inputs none.
- Risks for /add-dataset: Riders.csv holds rider aggregates (number of orders, age on platform, average rating, number of ratings), probably taken at extraction time over all orders (LEAK check); drop the Arrival at Delivery columns; rider-marked times give many near-zero or implausible targets (known from the competition, to verify; CLEAN, not a reason to drop rows silently); join the rider table on Rider Id.
- Priority: gap 0, use case +, source +, shape +, risk - (rider aggregates, noisy target, forced IID).

Zindi Sendy logistics challenge to predict delivery ETA for parcel/motorbike deliveries in Nairobi, a genuine real-world tabular regression task with order, rider, and location features. This is a strong fit for the benchmark, though it likely involves joining multiple provided tables (orders + riders) and may need a temporal split since deliveries are time-ordered. A human must confirm the target (ETA/duration), table structure to be joined, size, split regime, and license; note potential overlap with the 'sendy_logistics_challenge_2' record.
