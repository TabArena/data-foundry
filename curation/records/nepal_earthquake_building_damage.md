---
unique_name: nepal_earthquake_building_damage
name: 2015 Nepal (Gorkha) earthquake building damage assessment (Open Data Portal; DrivenData Richter's Predictor)
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 3
tags:
- AI-Filled (Verify)
original_source: GOV Website
problem_type: Multiclass Classification
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- http://eq2015.npc.gov.np/#/download
- https://www.drivendata.org/competitions/57/nepal-earthquake/
- https://kathmandulivinglabs.org/our-work/earthquake-data-portal
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: the Government of Nepal's door-to-door survey of about 760,000 buildings in the 11 districts most affected by the 2015 Gorkha earthquake, with an assessed damage grade and pre-quake building attributes; DrivenData's Richter's Predictor serves a three-grade cut with obfuscated category values under micro F1; the portal did not answer, and its tables carry post-event columns to drop.
- Source: the 2015 Nepal Earthquake Open Data Portal (http://eq2015.npc.gov.np/, no response on 2026-10-31), built by Kathmandu Living Labs and handed to the National Planning Commission; KLL's page: a Government of Nepal door-to-door survey in the 11 most affected districts, "760,000 buildings and 3.6 million residents", each table and column documented on the portal. DrivenData competition 57 (https://www.drivendata.org/competitions/57/nepal-earthquake/): "The data was collected through surveys by Kathmandu Living Labs and the Central Bureau of Statistics, which works under the National Planning Commission Secretariat of Nepal"; 39 columns, building_id and 38 features (geo_level_1-3 ids, floors before the quake, age, normalised footprint area and height, land surface, foundation, roof and floor types, superstructure flags, legal ownership, families, secondary uses); "Categorical variables have been obfuscated random lowercase ascii characters"; target damage_grade, 1 low, 2 medium, 3 almost complete destruction; 260,601 labelled buildings per the run's Assessment (not on the pages read).
- Use case: an authority ranks buildings by expected damage to prioritise retrofitting before an earthquake, or to send inspectors first to the likely worst-hit buildings after one; the competition states no decision ("your goal is to predict the level of damage to buildings caused by the 2015 Gorkha earthquake in Nepal"); fit approximate (ours); regime IID as the competition drew its test set, or grouped by geography (ward or geo_level ids), since shaking is shared within an area and a model serves other areas (SPLIT-3, to decide).
- Siblings and duplicates: none for this survey (grep: nepal, gorkha, richter, damage grade); `ncei_significant_earthquakes` (`TBD -> 2nd Tier`) is another earthquake table. The DrivenData set is a cut of the portal's data (three grades, coded values; PROV-6), so the portal's tables are the source to build from when they can be reached. External collections: none found.
- Better data: no new search; found through the gap scout for multiclass tasks.
- Papers and pages: the DrivenData problem description and overview (read); the KLL portal page (read); the portal's table documentation (not reached).
- Metric: the competition's micro-averaged F1 (problem description: "sklearn.metrics.f1_score" with "average='micro'"), a leaderboard metric (MET-4); with one label per building it equals accuracy on hard labels; it holds for the three competition grades, while a portal build with five grades needs the curator's call (MET-2). Inputs: none.
- Risks for /add-dataset: the portal's damage-assessment tables hold post-event columns (condition after the quake, technical solution proposed, damage per component) that go (LEAK); how the competition merged the portal's grades into three is not published (to check); the DrivenData values are coded but every column is described (no `Anonymized` marker, Patterns); the normalised area and height; the geographic grouping; the portal's reachability.
- Priority: gap + (multiclass is thin; disaster risk is absent), use case 0 (no source names a decision), source + (a government survey with documented tables, and a competition), shape + (hundreds of thousands of buildings, mixed types, geographic groups), risk - (post-event columns; the portal could not be reached).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the gap scout for multiclass tasks.
- as published: portal: about 762,106 buildings and 3.6 million residents in the 11 most affected districts, building structure, ownership/use, damage assessment and household tables; DrivenData: 260,601 labelled ...; target: damage_grade: 3 levels in DrivenData (low, medium, almost complete destruction); grades 1-5 in the portal's damage assessment; access: open.
- Why: One of the largest post-disaster surveys published; the damage grade is an engineer's assessment, the features are building attributes known before the quake. The portal tables carry post-event columns (condition after the quake, proposed technical solution, component damage) that must be dropped; DrivenData scores ...
- Adds: A large multiclass (ordinal) task with mixed categorical and numeric features and a geographic grouping (district, municipality, ward) for a grouped split; disaster risk is not in the benchmark
