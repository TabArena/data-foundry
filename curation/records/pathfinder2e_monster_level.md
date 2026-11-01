---
unique_name: pathfinder2e_monster_level
name: Pathfinder 2e monster level prediction
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
original_source: Github
year: '2026'
required_split:
- Temporal (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://github.com/tunczyk101/Monster-level-prediction-in-TTRPG
- https://arxiv.org/abs/2607.09196
- https://github.com/foundryvtt/pf2e
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-31):** `TBD -> 2nd Tier`, priority 2: 6,007 Pathfinder 2e monsters from 302 books with 33 numeric statistics and the level the publisher assigned; real published design data with a chronological split, but the level is close to a lookup of the statistics (random forest: 89% exact, 99% within one level), so the task risks `Trivial`.
- Source: Śliwa and Adamczyk, "Application of machine learning to monster level prediction in tabletop RPG game design", arXiv 2607.09196 (v1 2026-07-10, v3 2026-08-24), with code and data on GitHub (tunczyk101/Monster-level-prediction-in-TTRPG, created 2026-07-08, no licence file); the statistics come from the Foundry VTT pf2e system's monster packs (github.com/foundryvtt/pf2e), community encodings of Paizo's books. As published (file preview): `preprocessed_bestiaries/bestiaries_full.csv`, 6,007 rows x 37 columns: 33 features (abilities, AC, HP, saves, perception, focus, immunities, speeds, spells per level, attack bonuses and damage, spell DC and attack) plus `book`, `level`, `name` and an index; levels -1 to 21, where 21 stands for 21 to 25 ("only 89 in total across levels 21-25", Sec. 3.1); basic (8) and expanded (20) feature sets too.
- Use case: a game designer or game master building a new monster checks which level its statistics correspond to, to balance encounters (the paper's computer-aided monster balancing; Sec. 4.2 cites the rulebook on "estimating a monster's level by comparison with the most similar monsters in official books"); fit approximate, since the published levels were set by the publisher's designers ("obtained through expert estimation and extensive practical gameplay", Sec. 3.1), who choose the statistics for a level. Regime temporal: books dated 2019-08-01 to 2026-04-26, the paper's chronological split tests on monsters from 2025-08-01 on, about 20% (Sec. 4.5), plus an expanding window (SPLIT-19).
- Siblings and duplicates: no other tabletop game or monster record (grep: monster, pathfinder). External collections: none.
- Better data: from the curator's Zotero collection, item 224; no new search this run.
- Papers and pages: the arXiv paper (HTML v3: Sec. 3, 4.5, 4.6, 5.1, 5.3, Tables 2 and 3).
- Metric: seven reported (RMSE, MAE, macro-averaged MAE and RMSE, accuracy, accuracy within one level, Somers' D; Sec. 4.6), with tuning by MAE (Sec. 5.1) and model ranking by macro-averaged MAE (Sec. 5.3): two criteria, so the fallback `rmse` (MET-5), or MAE if the curator reads Sec. 5.3 as the choice; inputs none.
- Risks for /add-dataset: a near-deterministic target (Table 2, chronological split: random forest macro-averaged MAE 0.12, accuracy 89%, accuracy within one level 99%, Somers' D 0.99), so run the trivial probes (TP-4); designed content rather than a measured outcome, a SEL-16 question ("handmade") for the curator; `book` and `name` are identifiers, not features; the domain has no vocabulary value (`Other`), left empty.
- Priority: gap 0 (regression and temporal are not thin; the domain would be `Other`, never thin), use case 0 (approximate), source + (paper with code and data), shape + (6,007 rows, 33 features, dated by book), risk - (`Trivial` likely).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 224: "Application of machine learning to monster level prediction in tabletop RPG game design".
- as published: 6,007 monsters (one row each) x 33 features (8 ability, AC, HP; saves, perception, attacks and damage, spell DC and attack; speeds, immunity count, spells per level) plus source book and name; 302 ...; target: monster level, integer -1..20 with 21 meaning 'over 20' (ordinal regression); access: open.
- Why: Real published design data with a documented designer use case, and a chronological split by book publication date (the paper's protocol) that mirrors how new books are designed from old ones
- Adds: A new domain (game design) and an ordinal target with a temporal split. Caveats: the level is close to deterministic given Paizo's creature-building tables (the paper reports near-perfect ranking, so the task may be easy); the repo has no LICENSE file although the content is published under OGL 1.0a / ORC.
