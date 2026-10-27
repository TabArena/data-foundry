---
unique_name: sports_bet_datasets
name: sports bet datasets
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> 2nd Tier
priority: 1
decision_markers:
- Needs extensive data wrangling
- TBD
tags:
- AI-Filled (Verify)
domain: Other
required_split:
- '?'
problem_type: TBD
source_links:
- https://arxiv.org/html/2410.21484v1#S6
source_row: 1047
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from public knowledge of this competition/dataset, NOT from inspecting the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-10-22):** `TBD -> 2nd Tier`, priority 1: the link is a review's list of data sources, not one dataset; split it into concrete records before anything else.
- Source: Galekwa, Tshimula, Tajeuna, Kyandoghere, "A Systematic Review of Machine Learning in Sports Betting: Techniques, Challenges, and Future Directions", arXiv 2410.21484 (28 October 2024), section 6.1 "Datasets": for soccer football-data.co.uk, transfermarkt and "more than 200,000 match results from 52 leagues, sourced from the Open International Soccer Database"; for basketball NBA seasons; for tennis Jeff Sackmann's dataset, Tennis-Data.co.uk and the Match Charting Project; cricket, NFL, baseball, horse racing, rugby, golf and hockey sources. As published: no table; each source is its own dataset.
- Use case: a bettor or bookmaker pricing a match outcome before kick-off is a real decision; it holds per source, not for the list. Regime temporal (seasons, matches in time) and grouped by team.
- Siblings and duplicates: no soccer, tennis or betting record exists; NBA records (`nba_draft`, `nba_shots`, `nba_players_2016_2019`, `basketball_c`) are other tasks. External collections: none found.
- Papers and pages: the strongest lead is the Open International Soccer Database (Dubitzky, Lopes, Davis, Berrar, Machine Learning 108, 2019) with the 2017 Soccer Prediction Challenge, scored by the ranked probability score; worth its own record.
- Metric: none for the list; section 6.3 names accuracy, RPS and others per sport. Decide per new record.
- Risks for /add-dataset: not addable as is (`Needs extensive data wrangling`: a collection to split into datasets); match tables need pre-match features only (LEAK) and a temporal split; some sources are scraped sites with unclear terms (a note, never a reason, EV-4).
- Priority: gap - (no thin value as a list), use case - (per source), source - (a review, not the publisher), shape - (no table), risk 0. The old `Missing source information` is dropped: the review names its sources.

An entry pointing only to an arXiv paper section on 'sports bet datasets', with no fields, target, or description in the record. Sports-betting data is frequently framed as odds/ranking or outcome prediction with temporal structure, and the vague 'datasets' framing suggests it may be a collection rather than one well-defined predictive task. There is not enough information to decide scope, uniqueness, or modality. A human must read the arXiv source to identify whether a concrete, well-targeted tabular classification/regression task exists and whether it risks ranking/CTR-style framing.
