---
unique_name: umojahack_africa_2023_intermediate_challenge
name: umojahack-africa-2023-intermediate-challenge
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
collections:
- New (BeyondArena)
original_source: Zindi
year: '2023'
domain: technology & internet
required_split:
- Random (IID)
problem_type: Binary Classification
source_links:
- https://zindi.africa/competitions/umojahack-africa-2023-intermediate-challenge/data
- https://zindi.africa/competitions/indabax-ghana-2023/data
source_row: 973
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 2: cryptojacking detection from 18 host and network counters per visited website; the canonical Zindi copy (March 2023) of data first published by Hernandez-Suarez et al. (IPN, Applied Sciences 2022); three later Zindi re-runs share its files.
- Source: first publication Hernandez-Suarez et al., "Detecting Cryptojacking Web Threats: An Approach with Autoencoders and Deep Dense Neural Networks", Applied Sciences 12(7):3234, 2022 (doi:10.3390/app12073234, Instituto Politécnico Nacional): "9292 benign sites and 3434 sites labeled and validated as cryptojacking infected", 18 host and network features (processor idle states and usage, paging, disk I/O, bytes and packets sent and received), as described by the re-use paper Aponte-Novoa et al., Sensors 22(23):9219, 2022 (Universidad del Norte, <https://pmc.ncbi.nlm.nih.gov/articles/PMC9740044>), whose authors helped Zindi get the data. As published on Zindi (UmojaHack Africa 2023: Cryptojacking Detection Challenge (INTERMEDIATE), 18-19 March 2023, 435 participants, read through Zindi's API): Train.csv (1,374,711 B, "~9 000 readings", with the target), Test.csv (581,950 B, ~4,000 rows, no target), Variable_Definitions.csv; target 1 = cryptojacking, 0 = benign; one table. Whether the 2022 paper released the data was not read (the MDPI page returned 403).
- Use case: a browser or endpoint security tool flags and blocks a website as cryptojacking from its resource and traffic counters while it is open; the source states the classification goal ("classify network activity from various websites as either cryptojacking or not"), no actor, so fit approximate; regime IID (one row per site in the paper, no time column), grouped by site if rows turn out to be several windows of one site.
- Siblings and duplicates: the same Train.csv and Test.csv (identical byte sizes) in `indabax-ghana-2023` (Hack4Ghana, May 2023, this record's second link), `indabax-rwanda-2024-hacktathon` and `ai-national-summit-2024-competition` (record `ai_national_summit_2024_competition`), all with this competition as Zindi `parent`, and the Benin 2024 link of `indabax_hackathons`: this record is the canonical copy, the others are duplicates (PROV-4). No other cryptojacking record. External collections: none found.
- Papers and pages: the two papers above; <https://zindi.africa/competitions/umojahack-africa-2023-intermediate-challenge> (Description, Data, Evaluation); winners named (Team DSTune first), no solution read.
- Metric: F1 of the cryptojacking class ("The error metric for this competition is the F1 score", Evaluation tab); a competition's leaderboard metric on hard labels (MET-4); inputs none. The papers report accuracy, precision, recall and F1 side by side (no single one, MET-5).
- Risks for /add-dataset: the first source is the 2022 paper, so take its release if public and fix `original_source` and `year` (Zindi, 2023 now; PROV-8); only Train.csv is labelled (~9,000 rows); what one row is (a site or a time window of a site: SPLIT, grouping); duplicate rows; the Sensors paper finds simple models as good as deep ones, so check for a near-perfect score (TP-4).
- Priority: gap 0 (technology & internet, binary, IID not thin), use case 0 (no actor named), source + (a paper documents the collection), shape 0 (about 9,000 labelled rows, 18 numeric counters, no mixed types or structure), risk 0 (triviality unmeasured).

A 2023 UmojaHack Africa / IndabaX Ghana intermediate hackathon on Zindi, but the record gives no description of the underlying data or target, so the task type and domain cannot be determined from the record or general knowledge. Per the rules, too little information is not itself a reason to reject. A human must open the Zindi competition to determine the actual target, problem type, data modality (some hackathons use image/text/audio), size, and split regime before deciding.
