---
unique_name: delivery_rider_response_challenge_by_galsenai
name: Delivery Rider Response Challenge by GalsenAI
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
decision_markers:
- Out-of-scope Task (CTR/RecSys/Ranking)
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2021'
domain: business & marketing
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://zindi.africa/competitions/indabax-senegal-2021
- https://zindi.africa/competitions/umojahack-africa-2021-2-sendy-challenge-intermediate
source_row: 1004
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: a real dispatch-response task (accept, decline or ignore) from Sendy's platform; the old reject as a ranking task rests on a reading, so the curator decides whether an offer-acceptance label falls under SEL-9.
- Source: first published as Zindi "UmojaHack Africa 2021 #2: Sendy - Delivery Rider Response Challenge (INTERMEDIATE)", 27-28 March 2021 (https://zindi.africa/competitions/umojahack-africa-2021-2-sendy-challenge-intermediate); this record's IndabaX Senegal hackathon (GalsenAI, 23-29 August 2021) is a re-run with the same files (Train.csv 28,686,419 bytes, Test.csv 12,096,330, Riders.csv 49,652 in both Zindi APIs). As published: "a subset of over 200,000 dispatches", "only includes direct orders (i.e. Sendy 'express' orders) with bikes in Nairobi", "fully anonymized while preserving the distribution"; Train/Test (one row per dispatch: order, client, rider ids, rider_amount, licence and carrier flags, pickup, drop-off and rider coordinates at dispatch, `dispatch_day` (day of month), `dispatch_day_of_week`, `dispatch_time`) joined to Riders.csv (rider information, not described on the page) on `rider_id`; target 0 ignore, 1 decline, 2 accept.
- Use case: Sendy's dispatch system, at the moment an order is sent to a rider, picks the rider most likely to accept ("Picking the best rider to service the order will improve the experience of the customer"); fit direct for the response label; regime grouped (by order, several dispatches each, or by rider) or temporal; the times carry day of month and weekday but no month or year, so a temporal split may not be possible (SPLIT-7); Zindi's own split is not described.
- Siblings and duplicates: no record for the UmojaHack 2021 #2 original, so this record is the dataset's only one (add the first-publication link, done); `sendy_logistics_challenge` and `sendy_logistics_challenge_2` are Sendy's 2019 ETA regression, other data and another task (PROV-7). External collections: none found.
- Papers and pages: no paper; the two Zindi pages only; top solutions not read.
- Metric: accuracy on hard labels, Zindi Evaluation page ("The evaluation metric for this challenge is Accuracy ... Where ignore is 0, decline is 1 and accept is 2"); a leaderboard choice (MET-4); inputs none (MET-1, MET-5, MET-6).
- Risks for /add-dataset: SEL-9 (an offer-acceptance label used to rank riders is close to a click-through task; the old marker stays as that concern); Riders.csv may hold per-rider aggregates (counts, ratings, acceptance rates) computed over the whole period, which would leak the target (LEAK; the page does not describe the file); "anonymized while preserving the distribution" may mean perturbed values (PROV-3); a join (Needs extensive data wrangling is not warranted for one key).
- Problem type changed from `Other` (AI-filled) to `Multiclass Classification`: the source names three classes.
- Priority: gap 0 (business & marketing, multiclass, temporal not thin), use case + (Sendy's dispatch decision, named by the source), source 0 (competition page only, anonymised subset), shape + (tens of thousands of dispatches, ids, coordinates, times and a rider table), risk - (SEL-9 doubt, rider-metric leak): 2.

Zindi/GalsenAI IndabaX Senegal 2021 challenge whose stated goal is to predict the best delivery rider for an order placed via the Sendy logistics company. Matching/selecting the best rider for an order is a ranking/recommendation-style task, which is explicitly excluded under criterion 3 (no recommendation/ranking). Even if it could be reframed as a per-rider accept/decline classification, the framing as described is out of scope. A human could confirm whether the actual target is a simple binary rider-response label (which might rescue it), but as described it is a reject.

---

predict who is the best delivery rider for an order placed via logistics company Sendy
